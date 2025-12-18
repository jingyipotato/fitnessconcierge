"""Workout Reviser Agent Definition."""

from google.adk.agents import LlmAgent

from . import prompt
from ...config import config
from fitness_agent.infra.llm import create_worker_llm


def create_workout_reviser_agent() -> LlmAgent:
    """Create the workout reviser agent.
    
    Returns:
        Workout reviser LlmAgent.
    """
    return LlmAgent(
        model=create_worker_llm(config.model.worker_model),
        name="workout_reviser",
        description="Revises workout plan based on user feedback",
        instruction=prompt.WORKOUT_REVISER_INSTRUCTION,
        output_key="workout_plan"
    )
