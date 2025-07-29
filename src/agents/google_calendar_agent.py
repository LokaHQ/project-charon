import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from strands import Agent
from strands.models.litellm import LiteLLMModel

sys.path.append(str(Path(__file__).parent.parent))
from src.tools.celander_tools import create_event, get_events
from src.utils.config_loader import load_config
from src.utils.prompts import CALENDAR_AGENT_PROMPT

load_dotenv()


class CalendarAgent:
    """
    Main class to run the Google Calendar agent.
    It initializes the agent with the necessary tools and configurations,
    and starts an interactive loop for user commands.
    """

    def __init__(self):
        self.config = load_config()
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        self.model = LiteLLMModel(
            model_id=self.config.calendar_agent.model.model_id,
            client_args={
                "api_key": self.api_key,
            },
        )

        self.agent = Agent(
            tools=[get_events, create_event],
            model=self.model,
            system_prompt=CALENDAR_AGENT_PROMPT,
        )

    def query(self, user_input: str):
        """
        Run the agent with the provided user input.
        This method can be called to process commands related to calendar events.
        """
        response = self.agent(user_input)
        return response
