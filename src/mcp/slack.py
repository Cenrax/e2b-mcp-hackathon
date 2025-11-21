"""Slack operations via MCP"""

from src.mcp.client import MCPClient
from src.utils.logger import setup_logger
from src.core.config import settings

logger = setup_logger(__name__)


class SlackMCP:
    """Slack operations using MCP server"""
    
    def __init__(self, client: MCPClient):
        self.client = client
    
    async def send_message(self, message: str, channel: str = None) -> bool:
        """Send message to Slack channel"""
        channel = channel or settings.slack_channel
        logger.info(f"Sending Slack message to {channel}")
        
        try:
            await self.client.call_tool(
                "slack_post_message",
                arguments={
                    "channel": channel,
                    "text": message
                }
            )
            logger.info("✓ Slack message sent")
            return True
        except Exception as e:
            logger.error(f"Failed to send Slack message: {e}")
            return False
    
    async def send_alert(
        self,
        title: str,
        description: str,
        severity: str = "info",
        channel: str = None
    ) -> bool:
        """Send formatted alert to Slack"""
        
        emoji_map = {
            "critical": "🚨",
            "high": "⚠️",
            "medium": "⚡",
            "low": "ℹ️",
            "info": "📢"
        }
        
        emoji = emoji_map.get(severity, "📢")
        message = f"{emoji} *{title}*\n{description}"
        
        return await self.send_message(message, channel)
