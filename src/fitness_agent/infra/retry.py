"""Configure retry options."""

from google.genai import types


def default_retry_config() -> types.HttpRetryOptions:
    """Create the default HTTP retry configuration for LLM API calls.
    
    Returns:
        types.HttpRetryOptions: A retry configuration specifying:
            - maximum retry attempts
            - exponential backoff behaviour
            - initial delay before retry
            - HTTP status codes that should trigger a retry
    """
    return types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
)
