from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.tools.home_agent_tools import (
    add_movie_or_show_to_watchlist,
    get_movies_and_show_list,
    mark_movie_or_show_watched,
    search_omdb_movie_or_show,
)
from src.utils.config_loader import load_config
from utils.prompts import MOVIES_AGENT_PROMPT
from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands.models import BedrockModel
from strands.agent.conversation_manager import SlidingWindowConversationManager
import os


class MoviesAgent:
    """
    A movies agent that can manage tasks related to movies and shows.
    It can add movies or shows to a watchlist, mark them as watched, and search for them.
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
        system_prompt = MOVIES_AGENT_PROMPT
        conversation_manager = SlidingWindowConversationManager(window_size=10)

        return Agent(
            tools=[
                add_movie_or_show_to_watchlist,
                get_movies_and_show_list,
                mark_movie_or_show_watched,
                search_omdb_movie_or_show,
            ],
            model=self.model,
            system_prompt=system_prompt,
            conversation_manager=conversation_manager,
        )

    def query(self, user_input: str):
        """
        Run the agent with the provided user input.
        This method can be called to process commands related to movies and shows.
        """
        response = self.agent(user_input)
        return response
