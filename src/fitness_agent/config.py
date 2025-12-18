"""Configurations for fitness agent package."""

from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Configuration for fitness-related models.
    
    Attributes:
        worker_model: Model for generation/reviser tasks.
    """
    worker_model: str = "gemini-2.5-flash-lite"


@dataclass
class McpConfig:
    """Configuration for MCP OpenNutrition Server.
    
    Attributes:
        server_path: Path to MCP server entrypoint.
        timeout: Timeout (sec) for MCP communication.
    """
    server_path: str = "mcp-opennutrition/build/index.js"
    timeout: int = 30
    

@dataclass
class PluginConfig:
    """Configuration for plugin tools.
    
    Attributes:
        enable_logging: Option to enable LogginPlugin()
        enable_toolusage: Option to enable ToolUsagePlugin()
    """
    enable_logging: bool = True
    enable_toolusage: bool = True


@dataclass
class FitnessConfig:
    model: ModelConfig = field(default_factory=ModelConfig)
    mcp: McpConfig = field(default_factory=McpConfig)
    plugin: PluginConfig = field(default_factory=PluginConfig)

config = FitnessConfig()