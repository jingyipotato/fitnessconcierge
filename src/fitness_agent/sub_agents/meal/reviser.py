"""Meal Reviser Agent Definition."""

from typing import Sequence
from google.adk.agents import LlmAgent

from . import prompt
from ...config import config
from fitness_agent.infra.llm import create_worker_llm


def create_meal_reviser_agent(mcp_tools: Sequence) -> LlmAgent:
    """Create the meal reviser agent with injected MCP tools.
    
    Args:
        mcp_tools: List of allowed mcp tools.
        
    Returns:
        Meal reviser LlmAgent.
    """
    return LlmAgent(
        model=create_worker_llm(config.model.worker_model),
        name="meal_agent_reviser",
        description="Revises meal plan based on user feedback",
        instruction=prompt.MEAL_REVISER_INSTRUCTION,
        tools=[*mcp_tools],
        output_key="meal_plan"
    )