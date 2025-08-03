import sys
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).parent.parent))
from schemas.config_schema import (
    CalendarAgentConfig,
    Config,
    FilesAgentConfig,
    ModelConfig,
    TaskAgentConfig,
    GitHubAgentConfig,
)


def load_config(config_path: str = "") -> Config:
    """
    Load configuration from YAML file and return validated Pydantic model.

    Args:
        config_path: Path to config file. If None, uses default location.

    Returns:
        Config: Validated configuration object

    Raises:
        ValidationError: If configuration is invalid
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML is malformed
    """
    if config_path == "":
        config_path = (
            Path(__file__).parent.parent.parent / "config" / "project-config.yaml"
        )

    with open(config_path) as file:
        raw_config = yaml.safe_load(file)

    files_model_config = ModelConfig(
        model_id=raw_config["files_agent"]["model"]["model_id"],
    )
    files_agent_config = FilesAgentConfig(
        model=files_model_config,
        root_directory=raw_config["files_agent"]["root_directory"],
    )

    calendar_model_config = ModelConfig(
        model_id=raw_config["calendar_agent"]["model"]["model_id"],
    )

    calendar_agent_config = CalendarAgentConfig(model=calendar_model_config)

    task_model_config = ModelConfig(
        model_id=raw_config["task_agent"]["model"]["model_id"],
    )
    task_agent_config = TaskAgentConfig(model=task_model_config)

    github_model_config = ModelConfig(
        model_id=raw_config["github_agent"]["model"]["model_id"],
    )
    github_agent_config = GitHubAgentConfig(
        model=github_model_config,
        github_username=raw_config["github_agent"]["github_username"],
    )

    return Config(
        files_agent=files_agent_config,
        calendar_agent=calendar_agent_config,
        task_agent=task_agent_config,
        github_agent=github_agent_config,
    )
