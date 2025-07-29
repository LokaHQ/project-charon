import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.models import BedrockModel
from strands.models.litellm import LiteLLMModel
from strands_tools import file_read

sys.path.append(str(Path(__file__).parent.parent))
from typing import Optional

from src.schemas.file_agent_output_schema import FileAgentOutputSchema
from src.tools.file_search_tools import find_folder_from_name
from src.utils.config_loader import load_config
from src.utils.prompts import FILE_AGENT_PROMPT

load_dotenv()


class FileSearchAgent:
    """
    A file search agent that can be initialized with different model configurations
    and provides methods for running queries and interactive sessions.
    """

    def __init__(self, config: Optional[object] = None):
        """
        Initialize the FileSearchAgent with the necessary tools and configurations.

        Args:
            config: Optional configuration object. If None, will load from load_config()
        """
        self.config = config or load_config()
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.model_id = self.config.files_agent.model.model_id
        self.model = self._initialize_model()
        self.agent = self._initialize_agent()

    def _initialize_model(self):
        """Initialize the appropriate model based on configuration."""
        if self.model_id.startswith("openrouter"):
            return LiteLLMModel(
                model_id=self.model_id,
                client_args={"api_key": self.openrouter_api_key},
                max_tokens=10000,
                streaming=True,
            )
        elif self.model_id.startswith("anthropic"):
            return BedrockModel(
                model_id=self.model_id,
                client_args={"region_name": "us-east-1"},
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_id}")

    def _initialize_agent(self):
        """Initialize the agent with tools, model, and conversation manager."""
        system_prompt = FILE_AGENT_PROMPT
        conversation_manager = SlidingWindowConversationManager(window_size=10)

        return Agent(
            tools=[file_read, find_folder_from_name],
            model=self.model,
            system_prompt=system_prompt,
            conversation_manager=conversation_manager,
        )

    def query(self, question: str):
        """
        Run a single query against the agent.

        Args:
            question: The question to ask the agent

        Returns:
            The agent's response
        """

        if self.model_id.startswith("anthropic"):
            return self.agent.structured_output(FileAgentOutputSchema, question)
        else:
            return self.agent(question)
