from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.tools.home_agent_tools import (
    add_book_to_reading_list,
    get_book_lists,
    mark_book_read,
    search_book,
)
from src.utils.config_loader import load_config
from utils.prompts import BOOKS_AGENT_PROMPT
from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands.models import BedrockModel
from strands.agent.conversation_manager import SlidingWindowConversationManager
import os


class BookAgent:
    """
    A book agent that can manage tasks related to books.
    It can add books to a reading list, mark books as read, and search for books.
    """

    def __init__(self):
        self.config = load_config()
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.model_id = self.config.home_agent.model.model_id
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
        """Initialize the agent with the necessary tools and prompts."""
        system_prompt = BOOKS_AGENT_PROMPT
        conversation_manager = SlidingWindowConversationManager(window_size=10)

        return Agent(
            tools=[
                add_book_to_reading_list,
                get_book_lists,
                mark_book_read,
                search_book,
            ],
            model=self.model,
            system_prompt=system_prompt,
            conversation_manager=conversation_manager,
        )

    def query(self, user_input: str):
        """
        Run the agent with the provided user input.
        This method can be called to process commands related to book management.
        """
        response = self.agent(user_input)
        return response
