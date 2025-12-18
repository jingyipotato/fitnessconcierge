"""Nutrition MCP Toolset setup."""

from typing import Sequence

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from .logging import get_logger

logger = get_logger(__name__)


def create_nutrition_mcp_toolset(
    server_path: str,
    timeout: int = 30,
) -> McpToolset:
    """Create an MCP toolset connected to the OpenNutrition MCP server.

    Args:
        server_path: Path to the built MCP server entrypoint.
        timeout: Timeout (sec) for MCP communication.

    Returns:
        Configured MCP toolset.
    """
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="node",
                args=[server_path]
            ),
            timeout=timeout,
        )
    )

async def get_filtered_mcp_tools(
    toolset: McpToolset,
    allowed: Sequence[str],
):
    """Retrieve and filter MCP tools by name.

    Args:
        toolset: MCP toolset instance.
        allowed: Tool names to allow.

    Returns:
        List of filtered MCP tools.
    """
    tools = await toolset.get_tools()
    filtered = [t for t in tools if t.name in allowed]

    logger.info(f"Using MCP tools: {[t.name for t in filtered]}")
    return filtered

async def bootstrap_mcp_tools(
    server_path: str,
    allowed: Sequence[str],
    timeout: int = 30,
):
    """Bootstrap MCP tools for application usage.

    This is a convenience wrapper that composes MCP toolset creation
    and tool filtering into a single async call.

    Args:
        server_path: Path to MCP server entrypoint.
        allowed: Names of MCP tools to enable.
        timeout: Timeout (sec) for MCP communication.

    Returns:
        List of MCP tools ready to be injected into agents.
    """
    toolset = create_nutrition_mcp_toolset(
        server_path=server_path,
        timeout=timeout,
    )

    return await get_filtered_mcp_tools(
        toolset=toolset,
        allowed=allowed,
    )
