"""Complete pipeline example"""

import asyncio
from src.core.orchestrator import DevSecOpsOrchestrator


async def main():
    """Run the complete DevSecOps pipeline"""
    
    # Replace with your repository
    repo_url = "Cenrax/agno"
    
    print("🚀 AI DevSecOps Pipeline Orchestrator")
    print("=" * 50)
    print(f"Repository: {repo_url}\n")
    
    orchestrator = DevSecOpsOrchestrator()
    result = await orchestrator.run_pipeline(repo_url)
    
    print("\n" + "=" * 50)
    print("📊 Pipeline Results:")
    print(f"  Vulnerabilities Found: {result.vulnerabilities_found}")
    print(f"  Patches Generated: {result.patches_generated}")
    print(f"  Tests Passed: {result.tests_passed}")
    print(f"  PR Created: {'✓' if result.pr_created else '✗'}")
    
    if result.pr_url:
        print(f"  PR URL: {result.pr_url}")


if __name__ == "__main__":
    asyncio.run(main())
