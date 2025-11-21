"""MCP client for Docker gateway"""

import asyncio
from typing import Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class MCPClient:
    """Client for Docker MCP Gateway"""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self._read = None
        self._write = None
        self._context = None
        
    async def connect(self) -> None:
        """Connect to Docker MCP Gateway"""
        logger.info("Connecting to Docker MCP Gateway...")
        
        server_params = StdioServerParameters(
            command="docker",
            args=["mcp", "gateway", "run"]
        )
        
        try:
            self._context = stdio_client(server_params)
            self._read, self._write = await self._context.__aenter__()
            self.session = ClientSession(self._read, self._write)
            
            # Initialize with timeout
            await asyncio.wait_for(self.session.initialize(), timeout=30.0)
            
            logger.info("✓ Connected to Docker MCP Gateway")
        except asyncio.TimeoutError:
            logger.error("Connection timeout - MCP Gateway took too long to initialize")
            raise
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
        
    async def disconnect(self) -> None:
        """Disconnect from gateway"""
        try:
            if self._context:
                await self._context.__aexit__(None, None, None)
                logger.info("Disconnected from Docker MCP Gateway")
        except Exception as e:
            logger.warning(f"Error during disconnect: {e}")
    
    async def list_tools(self) -> list[str]:
        """List available tools from all MCP servers"""
        if not self.session:
            raise RuntimeError("Not connected. Call connect() first.")
        
        result = await self.session.list_tools()
        tools = [tool.name for tool in result.tools]
        logger.info(f"Available tools: {len(tools)}")
        return tools
    
    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Call a tool on MCP server"""
        if not self.session:
            raise RuntimeError("Not connected. Call connect() first.")
        
        logger.debug(f"Calling tool: {name} with args: {arguments}")
        result = await self.session.call_tool(name, arguments=arguments)
        return result
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
