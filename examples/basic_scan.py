"""Basic vulnerability scan example"""

import asyncio
from src.mcp.client import MCPClient
from src.mcp.github import GitHubMCP
from src.vulnerability.scanner import DependencyScanner


async def main():
    """Run a basic vulnerability scan"""
    
    # Replace with your repository
    repo_url = "owner/repo"
    
    scanner = DependencyScanner()
    
    async with MCPClient() as client:
        github = GitHubMCP(client)
        
        # Read requirements.txt
        print(f"📖 Reading requirements.txt from {repo_url}...")
        requirements = await github.read_file(repo_url, "requirements.txt")
        
        if not requirements:
            print("❌ No requirements.txt found")
            return
        
        print(f"✓ Found requirements.txt\n")
        
        # Scan for vulnerabilities
        print("🔍 Scanning for vulnerabilities...")
        vulnerabilities = scanner.scan_dependencies(requirements)
        
        if not vulnerabilities:
            print("✅ No vulnerabilities found!")
            return
        
        # Display results
        print(f"\n⚠️  Found {len(vulnerabilities)} vulnerabilities:\n")
        for vuln in vulnerabilities:
            print(f"  • {vuln.package} {vuln.current_version}")
            print(f"    ID: {vuln.vulnerability_id}")
            print(f"    Severity: {vuln.severity.upper()}")
            print(f"    Fix: Upgrade to {vuln.fixed_version}")
            print()


if __name__ == "__main__":
    asyncio.run(main())
