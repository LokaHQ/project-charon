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
)
from utils.prompts import HOME_AGENT_PROMPT

load_dotenv()


def main():
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

    model = LiteLLMModel(
        model_id="openrouter/mistralai/devstral-small",
        client_args={"api_key": openrouter_api_key},
    )

    agent = Agent(
        model=model,
        tools=[
            get_movies_and_show_list,
            mark_movie_or_show_watched,
            add_movie_or_show_to_watchlist,
            get_book_lists,
            mark_book_read,
            add_book_to_reading_list,
            search_omdb_movie_or_show,
        ],
        system_prompt=HOME_AGENT_PROMPT,
    )

    agent("Add the show Young Justice to my watchlist please.")


if __name__ == "__main__":
    main()
