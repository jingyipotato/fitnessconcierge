"""For ADK web usage."""

import asyncio

from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.sessions import DatabaseSessionService

from fitness_agent.agent import create_root_agent
from fitness_agent.infra.mcp import bootstrap_mcp_tools
from fitness_agent.infra.logging import get_logger
from .config import config

logger = get_logger(__name__)


def create_app():
    logger.info("create_app started!")

    mcp_tools = asyncio.run(
        bootstrap_mcp_tools(
            server_path=config.mcp.server_path,
            allowed=["search-food-by-name", "get-foods"],
            timeout=config.mcp.timeout,
        )
    )

    root_agent = create_root_agent(mcp_tools=mcp_tools)
    
    return App(
        name="fitness_concierge",
        root_agent=root_agent,
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=7,
            overlap_size=3,
        ),
    )


app = create_app()

    