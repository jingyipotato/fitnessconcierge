"""Meal Agent Definition."""
from typing import Sequence

from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

from . import prompt
from ...config import config
from fitness_agent.infra.llm import create_worker_llm
from .tools import calculate_daily_calories


def create_meal_planning_agent(
    *,
    mcp_tools: Sequence,
    meal_reviser_agent: LlmAgent
    ) -> LlmAgent:
    """Create the meal planning agent with injected MCP tools.
    
    Args:
        mcp_tools: List of allowed mcp tools.
        meal_reviser_agent: LlmAgent for meal reviser plan.
        
    Returns:
        Meal planning LlmAgent.
    """
    return LlmAgent(
        model=create_worker_llm(config.model.worker_model),
        name="meal_planning_agent",
        description="Creates initial meal plan based on provided user profile",
        instruction=prompt.MEAL_INSTRUCTION,
        tools=[calculate_daily_calories,
               *mcp_tools,
               AgentTool(agent=meal_reviser_agent)],
        output_key="meal_plan"
    )
