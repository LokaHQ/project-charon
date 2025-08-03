import sys
from pathlib import Path

from dotenv import load_dotenv
from strands import Agent
from strands.models.litellm import LiteLLMModel

sys.path.append(str(Path(__file__).parent.parent))
import os


from src.tools.home_agent_tools import (
    add_book_to_reading_list,
    add_movie_or_show_to_watchlist,
    get_book_lists,
    get_movies_and_show_list,
    mark_book_read,
    mark_movie_or_show_watched,
    search_omdb_movie_or_show,
    search_book,
)
from utils.prompts import HOME_AGENT_PROMPT
from src.utils.config_loader import load_config
from strands.models import BedrockModel
from strands.agent.conversation_manager import SlidingWindowConversationManager
from src.schemas.file_agent_output_schema import FileAgentOutputSchema

load_dotenv()


class HomeAgent:
    """
    A home agent that can manage tasks related to movies, shows, and books.
    It can add items to watchlists, mark items as watched or read, and search for movies or shows.
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
        """Initialize the agent with tools, model, and conversation manager."""
        system_prompt = HOME_AGENT_PROMPT
        conversation_manager = SlidingWindowConversationManager(window_size=10)

        return Agent(
            tools=[
                get_movies_and_show_list,
                mark_movie_or_show_watched,
                add_movie_or_show_to_watchlist,
                get_book_lists,
                mark_book_read,
                add_book_to_reading_list,
                search_omdb_movie_or_show,
                search_book,
            ],
            model=self.model,
            system_prompt=system_prompt,
            conversation_manager=conversation_manager,
        )

    def query(self, question: str) -> str:
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
