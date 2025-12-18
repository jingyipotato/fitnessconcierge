"""Workout Agent Definition."""

from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

from . import prompt
from ...config import config
from fitness_agent.infra.llm import create_worker_llm


def create_workout_agent(workout_reviser_agent: LlmAgent) -> LlmAgent:
    """Create the workout planning agent.

    Args:
        workout_reviser_agent: LlmAgent for workout reviser plan.

    Returns:
        Workout LlmAgent.
    """
    return LlmAgent(
        model=create_worker_llm(config.model.worker_model),
        name="workout_program_agent",
        description="Creates and manages training plan based on provided user profile",
        instruction=prompt.WORKOUT_INSTRUCTION,
        tools=[AgentTool(agent=workout_reviser_agent)],
        output_key="workout_plan"
    )
