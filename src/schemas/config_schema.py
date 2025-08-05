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


class CalendarAgentConfig(BaseModel):
    """Configuration for the calendar agent."""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for calendar agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )


class BooksAgentConfig(BaseModel):
    """Configuration for the books agent."""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for books agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )


class MoviesAgentConfig(BaseModel):
    """Configuration for the movies agent."""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for movies agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )


class TaskAgentConfig(BaseModel):
    """Configuration for the task agent"""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for task agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )


class GitHubAgentConfig(BaseModel):
    """Configuration for the GitHub agent."""

    github_username: str = Field(
        ..., description="GitHub username for the agent to interact with repositories"
    )
    model: ModelConfig = Field(
        ...,
        description="Model configuration for GitHub agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )


class Config(BaseModel):
    """Main configuration schema."""

    files_agent: FilesAgentConfig = Field(..., description="Files agent configuration")
    calendar_agent: CalendarAgentConfig = Field(
        ..., description="Calendar agent configuration"
    )
    books_agent: BooksAgentConfig = Field(..., description="Books agent configuration")
    movies_agent: MoviesAgentConfig = Field(
        ..., description="Movies agent configuration"
    )
    task_agent: TaskAgentConfig = Field(..., description="Task agent configuration")

    github_agent: GitHubAgentConfig = Field(
        ..., description="GitHub agent configuration"
    )
