"""Create an LLM factory."""

from google.adk.models.google_llm import Gemini
from fitness_agent.infra.retry import default_retry_config


def create_worker_llm(model_name: str) -> Gemini:
    """Create a Gemini LLM client for generation/reviser agents.
    
    This is configured for tasks such as:
    - meal plan generation
    - workout plan generation
    - iterative revision
    
    Args:
        model_name (str): The name of the Gemini model to use for generation.
        
    Returns:
        Gemini: A Gemini LLM cient configured with retry behaviour suitable
            for generation-heavy workloads.
    """
    return Gemini(
        model=model_name,
        retry_options=default_retry_config(),
    )
