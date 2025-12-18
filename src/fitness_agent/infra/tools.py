"""ToolUsagePlugin for agents."""

import time
from typing import Any, Dict

from google.adk.plugins import BasePlugin
from google.adk.tools import BaseTool
from google.adk.agents.callback_context import CallbackContext

from fitness_agent.infra.logging import get_logger

logger = get_logger(__name__)


# Tool Usage Plugin
class ToolUsagePlugin(BasePlugin):
    """A plugin that tracks tool usage patterns across agent conversations.
    
    It monitors all tool calls made by agent, recording:
    - No. of times each tool is called
    - Average execution time per tool
    
    Attributes:
        tool_calls: Dict storing call counts and timing for each tool.
        tool_start_times: Temporary storage for tracking call durations.
    """
    def __init__(self) -> None:
        """Initialize the ToolUsagePlugin with empty tracking dictionaries."""
        super().__init__(name="tool_usage")
        self.tool_calls: Dict[str, Dict[str, float]] = {}
        self.tool_start_times: Dict[int, float] = {}  # Track start times separately

    async def before_tool_callback(
        self, 
        *,
        tool: BaseTool,
        tool_args: Dict[str, Any],
        tool_context: CallbackContext,
        **kwargs: Any
    ) -> None:
        """
        Callback executed before a tool is invoked.

        Records the start time for duration tracking and initializes
        the tool's entry in the tracking dictionary if needed.

        Args:
            tool: Tool object being invoked.
            tool_args: Dictionary of arguments being passed to the tool.
            tool_context: Context object containing session and state information.
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        tool_name: str = getattr(tool, 'name', str(tool))

        if tool_name not in self.tool_calls:
            self.tool_calls[tool_name] = {"count": 0, "total_time": 0}

        self.tool_start_times[id(tool_context)] = time.time()
        logging.info(f"[TOOL] Starting: {tool_name}")

    async def after_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: Dict[str, Any],
        tool_context: CallbackContext,
        result: Any,
        **kwargs: Any
    ) -> None:
        """
        Callback executed after a tool completes.

        Calculates the execution duration and updates the tool's
        statistics in the tracking dictionary.

        Args:
            tool: Tool object that was invoked.
            tool_args: Dictionary of arguments that were passed to the tool.
            tool_context: Context object containing session and state information.
            result: The return value from the tool execution.
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        tool_name: str = getattr(tool, 'name', str(tool))

        # Calculate duration
        start_time: float = self.tool_start_times.pop(id(tool_context), time.time())
        duration: float = time.time() - start_time

        if tool_name in self.tool_calls:
            self.tool_calls[tool_name]["count"] += 1
            self.tool_calls[tool_name]["total_time"] += duration

        logger.info(f"[TOOL] Completed: {tool_name} | Duration: {duration:.2f}s")

    def get_summary(self) -> Dict[str, Dict[str, float]]:
        """
        Generate a summary of tool usage statistics.


        Returns:
            Dictionary mapping tool names to their usage statistics.
            Each tool entry contains:
            - total_calls: No. of times the tool was invoked.
            - avg_time: Average execution time in seconds.
        """
        return {
            tool_name: {
                "total_calls": data["count"],
                "avg_time": data["total_time"] / data["count"] if data["count"] > 0 else 0
            }
            for tool_name, data in self.tool_calls.items()
        }



