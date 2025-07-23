from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """Configuration for the LLM model."""

    model_id: str = Field(
        ..., description="Model identifier (e.g., 'openrouter/deepseek/deepseek-r1')"
    )


class FilesAgentConfig(BaseModel):
    """Configuration for the files agent."""

    root_directory: str = Field(
        ..., description="Root directory to search for projects"
    )
    model: ModelConfig = Field(..., description="Model configuration")


class Config(BaseModel):
    """Main configuration schema."""

    files_agent: FilesAgentConfig = Field(..., description="Files agent configuration")
