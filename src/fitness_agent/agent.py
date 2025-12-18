"""Fitness Concierge Root Agent.
Orchestrates the end-to-end fitness planning for users.
"""

from typing import Sequence
from google.adk.agents import LlmAgent

from .infra.llm import create_worker_llm
from .config import config
from .sub_agents.meal.agent import create_meal_planning_agent
from .sub_agents.meal.reviser import create_meal_reviser_agent
from .sub_agents.workout.agent import create_workout_agent
from .sub_agents.workout.reviser import create_workout_reviser_agent


# Create Root Agent
def create_root_agent(mcp_tools: Sequence) -> LlmAgent:
    """"""
    meal_reviser_agent = create_meal_reviser_agent(mcp_tools)
    meal_planning_agent = create_meal_planning_agent(
        mcp_tools=mcp_tools,
        meal_reviser_agent=meal_reviser_agent)
    
    workout_reviser_agent = create_workout_reviser_agent()
    workout_agent = create_workout_agent(workout_reviser_agent)
    
    return LlmAgent(
        model=create_worker_llm(config.model.worker_model),
        name="fitness_concierge_agent",
        instruction="""
        You are a fitness concierge agent that coordinates personalized fitness planning (workout + meal).

        STEP 1: Gather core user information
        Ask the user for:
        1. Primary fitness goals? (muscle gain, fat loss, strength, general fitness)
        2. Experience level (beginner, intermediate, advanced)

        STEP 2: Workout
        Say: "Great! Let's start with your workout plan."
        Transfer to workout_agent.

        (workout_agent will handle everything and transfer back when done)

        STEP 3: Meal
        When workout_agent transfers back to you:
        Say: "Excellent! Now let's create your meal plan."
        Transfer to meal_planning_agent.
        (meal_planning_agent will handle everything and transfer back when done)

        STEP 4: Finalize
        When meal_planning_agent transfers back to you:
        Present both plans together:
        - Show the workout_plan
        - Show the meal_plan
        Congratulate them on starting their fitness journey!
    
        Be professional, encouraging and supportive
        """,
        sub_agents=[workout_agent, meal_planning_agent]
    )

def create_root_agent_for_deployment() -> LlmAgent:
    """
    Deployment-safe root agent creation.
    MCP tools are intentionally disabled."""
    return create_root_agent(mcp_tools=[])


root_agent = create_root_agent(mcp_tools=[])