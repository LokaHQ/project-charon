import yaml
from dataclasses import dataclass
from typing import Dict, Any
from pathlib import Path

@dataclass
class ModelConfig:
    model_id: str
    api_key_env: str


@dataclass
class FilesAgentConfig:
    root_directory:str
    model: ModelConfig

@dataclass
class Config:
    files_agent: FilesAgentConfig

def load_config(config_path: str = None) -> Config:
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "project-config.yaml"
    
    with open(config_path, 'r') as file:
        raw_config = yaml.safe_load(file)
    
    # Create ModelConfig instance
    model_config = ModelConfig(
        model_id=raw_config['files_agent']['model']['model_id'],
        api_key_env=raw_config['files_agent']['model']['api_key_env']
    )
    
    # Create FilesAgentConfig instance  
    files_agent_config = FilesAgentConfig(
        model=model_config,
        root_directory=raw_config['files_agent']['root_directory']
    )
    
    # Create Config instance
    return Config(
        files_agent=files_agent_config
    )
