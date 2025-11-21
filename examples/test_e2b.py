"""Test E2B sandbox functionality"""

import asyncio
from src.sandbox.manager import SandboxManager


async def main():
    """Test E2B sandbox"""
    
    print("🧪 Testing E2B Sandbox\n")
    
    async with SandboxManager() as sandbox:
        # Test 1: Install a package
        print("Test 1: Installing requests package...")
        result = await sandbox.install_requirements("requests==2.31.0")
        print(f"  Result: {'✓ Success' if result.success else '✗ Failed'}")
        
        # Test 2: Run simple code
        print("\nTest 2: Running test code...")
        test_code = """
import requests
print(f"Requests version: {requests.__version__}")
print("✓ Package working correctly")
"""
        result = await sandbox.run_test(test_code)
        print(f"  Result: {'✓ Success' if result.success else '✗ Failed'}")
        if result.output:
            print(f"  Output: {result.output}")


if __name__ == "__main__":
    asyncio.run(main())
