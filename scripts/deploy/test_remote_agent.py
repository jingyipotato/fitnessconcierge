"""Script for testing the deployed remote agent."""

import os
import asyncio
from dotenv import load_dotenv

import vertexai
from vertexai import agent_engines

from fitness_agent.infra.logging import get_logger

logger = get_logger(__name__)

async def main():
    # Initialize Vertex AI
    vertexai.init(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location="us-east4"  # Change accordingly
    )
    
    # Get the most recently deployed agent
    agents_list = list(agent_engines.list())
    
    if not agents_list:
        logger.error("No agents found. Please deploy first.")
        return
    
    # Pick the most recent agent
    remote_agent = agents_list[0]
    logger.info(f"Connected to deployed agent: {remote_agent.resource_name}")
    
    # Stream response from the deployed agent
    async for item in remote_agent.async_stream_query(
        message="I want to stay fit!",
        user_id="fitspo",
    ):
        logger.info(item)   
    
    # Delete remote agent after testing
    agent_engines.delete(resource_name=remote_agent.resource_name, force=True)
    logger.info("Agent successfully deleted.")


if __name__ == "__main__":
    asyncio.run(main())