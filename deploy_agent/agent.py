"""Agent file for deployment."""

from fitness_agent.agent import create_root_agent_for_deployment

root_agent = create_root_agent_for_deployment()

__all__ = ["root_agent"]