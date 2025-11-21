"""AI-powered patch generation using OpenAI"""

from openai import AsyncOpenAI
from src.vulnerability.scanner import Vulnerability
from src.core.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PatchGenerator:
    """Generate patches using OpenAI"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def generate_dependency_patch(self, vuln: Vulnerability) -> str:
        """Generate patch for dependency vulnerability"""
        logger.info(f"Generating patch for {vuln.package}")
        
        prompt = f"""You are a security expert. Generate a patch for this vulnerability:

Package: {vuln.package}
Current Version: {vuln.current_version}
Vulnerability: {vuln.vulnerability_id}
Severity: {vuln.severity}
Description: {vuln.description}
Fixed Version: {vuln.fixed_version}

Generate ONLY the updated requirements.txt line. No explanation.
Format: package==version
"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a security patch generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=50
        )
        
        patch = response.choices[0].message.content.strip()
        logger.info(f"Generated patch: {patch}")
        return patch
    
    async def generate_requirements_patch(
        self,
        original_content: str,
        vulnerabilities: list[Vulnerability]
    ) -> str:
        """Generate complete patched requirements.txt"""
        logger.info(f"Generating requirements patch for {len(vulnerabilities)} vulnerabilities")
        
        patched_content = original_content
        
        for vuln in vulnerabilities:
            old_line = f"{vuln.package}=={vuln.current_version}"
            new_line = await self.generate_dependency_patch(vuln)
            patched_content = patched_content.replace(old_line, new_line)
        
        return patched_content
    
    async def generate_test_script(self, package: str) -> str:
        """Generate basic test script for package"""
        logger.info(f"Generating test script for {package}")
        
        prompt = f"""Generate a simple Python test script that imports and tests basic functionality of the '{package}' package.
Keep it minimal - just verify the package works after upgrade.
Return ONLY the Python code, no markdown or explanation."""
        
        response = await self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a Python test generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        test_code = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        test_code = test_code.replace("```python", "").replace("```", "").strip()
        
        return test_code
