"""E2B sandbox management"""

from typing import Optional
from dataclasses import dataclass
from e2b_code_interpreter import Sandbox
from src.core.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class TestResult:
    """Test execution result"""
    success: bool
    output: str
    error: Optional[str] = None


class SandboxManager:
    """Manage E2B sandboxes for testing"""
    
    def __init__(self):
        self.sandbox: Optional[Sandbox] = None
    
    async def create_sandbox(self) -> Sandbox:
        """Create a new E2B sandbox"""
        logger.info("Creating E2B sandbox...")
        
        self.sandbox = await Sandbox.create(api_key=settings.e2b_api_key)
        logger.info(f"✓ Sandbox created: {self.sandbox.sandbox_id}")
        return self.sandbox
    
    async def close_sandbox(self) -> None:
        """Close the sandbox"""
        if self.sandbox:
            await self.sandbox.close()
            logger.info("Sandbox closed")
    
    async def install_requirements(self, requirements: str) -> TestResult:
        """Install requirements in sandbox"""
        if not self.sandbox:
            raise RuntimeError("Sandbox not created")
        
        logger.info("Installing requirements in sandbox...")
        
        # Write requirements.txt
        await self.sandbox.filesystem.write("requirements.txt", requirements)
        
        # Install packages
        execution = await self.sandbox.run_code(
            "!pip install -q -r requirements.txt"
        )
        
        success = not execution.error
        if success:
            logger.info("✓ Requirements installed successfully")
        else:
            logger.error(f"Failed to install requirements: {execution.error}")
        
        return TestResult(
            success=success,
            output=execution.text,
            error=execution.error.value if execution.error else None
        )
    
    async def run_test(self, test_code: str) -> TestResult:
        """Run test code in sandbox"""
        if not self.sandbox:
            raise RuntimeError("Sandbox not created")
        
        logger.info("Running test in sandbox...")
        
        execution = await self.sandbox.run_code(test_code)
        
        success = not execution.error
        if success:
            logger.info("✓ Test passed")
        else:
            logger.error(f"Test failed: {execution.error}")
        
        return TestResult(
            success=success,
            output=execution.text,
            error=execution.error.value if execution.error else None
        )
    
    async def __aenter__(self):
        await self.create_sandbox()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_sandbox()
