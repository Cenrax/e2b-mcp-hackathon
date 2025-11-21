"""Main DevSecOps orchestration engine"""

from dataclasses import dataclass
from src.mcp.client import MCPClient
from src.mcp.github import GitHubMCP
from src.mcp.slack import SlackMCP
from src.vulnerability.scanner import DependencyScanner
from src.patch.generator import PatchGenerator
from src.sandbox.manager import SandboxManager
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class PipelineResult:
    """Pipeline execution result"""
    repo: str
    vulnerabilities_found: int
    patches_generated: int
    tests_passed: int
    pr_created: bool
    pr_url: str = None


class DevSecOpsOrchestrator:
    """Main orchestration engine"""
    
    def __init__(self):
        self.mcp_client = MCPClient()
        self.scanner = DependencyScanner()
        self.patch_generator = PatchGenerator()
    
    async def run_pipeline(self, repo_url: str) -> PipelineResult:
        """Run complete DevSecOps pipeline"""
        logger.info(f"🚀 Starting DevSecOps pipeline for {repo_url}")
        
        result = PipelineResult(
            repo=repo_url,
            vulnerabilities_found=0,
            patches_generated=0,
            tests_passed=0,
            pr_created=False
        )
        
        async with self.mcp_client:
            github = GitHubMCP(self.mcp_client)
            slack = SlackMCP(self.mcp_client)
            
            # Step 1: Scan repository
            logger.info("Step 1: Scanning repository for vulnerabilities")
            requirements = await github.read_file(repo_url, "requirements.txt")
            
            if not requirements:
                logger.warning("No requirements.txt found")
                await slack.send_alert(
                    "Scan Complete",
                    f"No requirements.txt found in {repo_url}",
                    "info"
                )
                return result
            
            # Step 2: Detect vulnerabilities
            logger.info("Step 2: Detecting vulnerabilities")
            vulnerabilities = self.scanner.scan_dependencies(requirements)
            result.vulnerabilities_found = len(vulnerabilities)
            
            if not vulnerabilities:
                logger.info("✓ No vulnerabilities found")
                await slack.send_alert(
                    "Scan Complete",
                    f"No vulnerabilities found in {repo_url}",
                    "info"
                )
                return result
            
            # Notify team about vulnerabilities
            vuln_summary = "\n".join([
                f"• {v.package} {v.current_version}: {v.vulnerability_id} ({v.severity})"
                for v in vulnerabilities
            ])
            await slack.send_alert(
                "Vulnerabilities Detected",
                f"Found {len(vulnerabilities)} vulnerabilities:\n{vuln_summary}",
                "high"
            )
            
            # Step 3: Generate patches
            logger.info("Step 3: Generating patches with AI")
            patched_requirements = await self.patch_generator.generate_requirements_patch(
                requirements,
                vulnerabilities
            )
            result.patches_generated = len(vulnerabilities)
            
            # Step 4: Test patches in E2B sandbox
            logger.info("Step 4: Testing patches in isolated sandbox")
            async with SandboxManager() as sandbox:
                # Install patched requirements
                install_result = await sandbox.install_requirements(patched_requirements)
                
                if not install_result.success:
                    logger.error("Patch installation failed")
                    await slack.send_alert(
                        "Patch Test Failed",
                        f"Failed to install patched dependencies:\n{install_result.error}",
                        "critical"
                    )
                    return result
                
                # Run basic tests for each patched package
                tests_passed = 0
                for vuln in vulnerabilities:
                    test_code = await self.patch_generator.generate_test_script(vuln.package)
                    test_result = await sandbox.run_test(test_code)
                    
                    if test_result.success:
                        tests_passed += 1
                
                result.tests_passed = tests_passed
            
            # Step 5: Create PR if all tests passed
            if result.tests_passed == len(vulnerabilities):
                logger.info("Step 5: Creating pull request")
                
                pr_body = f"""## Security Patch - Automated Vulnerability Fix

**Vulnerabilities Fixed:** {len(vulnerabilities)}

### Changes:
{vuln_summary}

### Testing:
- ✅ All {tests_passed} packages tested successfully in isolated E2B sandbox
- ✅ Dependencies installed without errors
- ✅ Basic functionality verified

**Generated by AI DevSecOps Orchestrator**
"""
                
                # Note: In real implementation, would create a branch first
                # For demo, we'll just log the PR creation
                logger.info("PR would be created with:")
                logger.info(f"Title: Security patch - Fix {len(vulnerabilities)} vulnerabilities")
                logger.info(f"Body: {pr_body}")
                
                result.pr_created = True
                
                await slack.send_alert(
                    "Patch Ready",
                    f"✅ All tests passed! Ready to merge security patches for {repo_url}",
                    "info"
                )
            else:
                logger.warning(f"Only {tests_passed}/{len(vulnerabilities)} tests passed")
                await slack.send_alert(
                    "Patch Incomplete",
                    f"⚠️ Only {tests_passed}/{len(vulnerabilities)} patches passed testing",
                    "medium"
                )
        
        logger.info(f"✓ Pipeline complete: {result}")
        return result
