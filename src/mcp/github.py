"""GitHub operations via MCP"""

from typing import Optional
from src.mcp.client import MCPClient
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class GitHubMCP:
    """GitHub operations using MCP server"""
    
    def __init__(self, client: MCPClient):
        self.client = client
    
    async def read_file(self, repo: str, path: str, branch: str = "main") -> Optional[str]:
        """Read a file from repository"""
        logger.info(f"Reading {path} from {repo}")
        
        try:
            result = await self.client.call_tool(
                "github_read_file",
                arguments={
                    "repo": repo,
                    "path": path,
                    "branch": branch
                }
            )
            return result.content[0].text if result.content else None
        except Exception as e:
            logger.error(f"Failed to read file: {e}")
            return None
    
    async def list_files(self, repo: str, path: str = "", branch: str = "main") -> list[str]:
        """List files in repository directory"""
        logger.info(f"Listing files in {repo}/{path}")
        
        try:
            result = await self.client.call_tool(
                "github_list_files",
                arguments={
                    "repo": repo,
                    "path": path,
                    "branch": branch
                }
            )
            return result.content[0].text.split("\n") if result.content else []
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return []
    
    async def create_pull_request(
        self,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str = "main"
    ) -> Optional[str]:
        """Create a pull request"""
        logger.info(f"Creating PR: {title}")
        
        try:
            result = await self.client.call_tool(
                "github_create_pull_request",
                arguments={
                    "repo": repo,
                    "title": title,
                    "body": body,
                    "head": head,
                    "base": base
                }
            )
            pr_url = result.content[0].text if result.content else None
            logger.info(f"✓ PR created: {pr_url}")
            return pr_url
        except Exception as e:
            logger.error(f"Failed to create PR: {e}")
            return None
