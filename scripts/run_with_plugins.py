"""Script for local run with plugins."""

import asyncio
import logging
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.plugins.logging_plugin import LoggingPlugin

from fitness_agent.infra.logging import get_logger
from fitness_agent.infra.tools import ToolUsagePlugin
from fitness_agent.agent import create_root_agent
from fitness_agent.config import config

load_dotenv()
logger = get_logger(__name__)

APP_NAME = "run_local_logs"
USER_ID = "local_user"
SESSION_ID = "local_session_logs"


async def main():
    mcp_tools = []
    orchestrator = create_root_agent(mcp_tools=mcp_tools)

    plugins = []

    if config.plugin.enable_logging:
        plugins.append(LoggingPlugin())
        logger.info("Using LoggingPlugin.")
    
    if config.plugin.enable_toolusage:
        plugins.append(ToolUsagePlugin())
        logger.info("Using ToolUsagePlugin.")

    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    runner = Runner(
        agent=orchestrator,
        app_name=APP_NAME,
        session_service=session_service,
        plugins=plugins,
    )

    logger.info("Starting Fitness Agent! (type 'exit' to quit)\n")

    while True:
        user_input = input("Enter Message: ")

        if user_input.lower() in {"exit", "quit"}:
            logging.info("Ending chat...")
            break

        # Construct ADK-style user message
        content = types.Content(role="user", parts=[types.Part(text=user_input)])

        # Stream events
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=content,
        ):
            # Only prints the final response
            if (
                event.is_final_response()
                and event.content
                and event.content.parts
            ):
                response = "".join(
                    part.text
                    for part in event.content.parts
                    if hasattr(part, "text")
                )
                print(f"Agent: {response}")


if __name__ == "__main__":
    asyncio.run(main())