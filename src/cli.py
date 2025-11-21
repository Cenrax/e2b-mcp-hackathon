"""CLI interface"""

import asyncio
import click
from rich.console import Console
from rich.table import Table
from src.core.orchestrator import DevSecOpsOrchestrator

console = Console()


@click.group()
def main():
    """AI DevSecOps Pipeline Orchestrator"""
    pass


@main.command()
@click.argument("repo_url")
def pipeline(repo_url: str):
    """Run complete DevSecOps pipeline"""
    console.print(f"\n[bold blue]AI DevSecOps Pipeline[/bold blue]")
    console.print(f"Repository: {repo_url}\n")
    
    orchestrator = DevSecOpsOrchestrator()
    result = asyncio.run(orchestrator.run_pipeline(repo_url))
    
    # Display results
    table = Table(title="Pipeline Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Vulnerabilities Found", str(result.vulnerabilities_found))
    table.add_row("Patches Generated", str(result.patches_generated))
    table.add_row("Tests Passed", str(result.tests_passed))
    table.add_row("PR Created", "✓" if result.pr_created else "✗")
    
    console.print(table)


@main.command()
def test_connection():
    """Test MCP connection"""
    from src.mcp.client import MCPClient
    
    async def _test():
        async with MCPClient() as client:
            tools = await client.list_tools()
            console.print(f"\n[green]✓ Connected to Docker MCP Gateway[/green]")
            console.print(f"Available tools: {len(tools)}")
            for tool in tools[:5]:
                console.print(f"  • {tool}")
    
    asyncio.run(_test())


if __name__ == "__main__":
    main()
