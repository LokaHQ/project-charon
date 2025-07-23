import yaml
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from schemas.config_schema import Config, ModelConfig, FilesAgentConfig


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

    model_config = ModelConfig(
        model_id=raw_config["files_agent"]["model"]["model_id"],
    )

    files_agent_config = FilesAgentConfig(
        model=model_config, root_directory=raw_config["files_agent"]["root_directory"]
    )

    return Config(files_agent=files_agent_config)
