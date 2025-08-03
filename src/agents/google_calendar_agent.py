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
from strands.models import BedrockModel

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
        self.model_id = self.config.calendar_agent.model.model_id
        self.model = self.initialize_model()

        self.agent = Agent(
            tools=[get_events, create_event],
            model=self.model,
            system_prompt=CALENDAR_AGENT_PROMPT,
        )

    def initialize_model(self):
        """
        Load the model for the calendar agent.
        This method is called during initialization to set up the agent's model.
        """
        if self.model_id.startswith("openrouter"):
            return LiteLLMModel(
                model_id=self.model_id,
                client_args={"api_key": self.api_key},
                max_tokens=10000,
                streaming=True,
            )
        elif self.model_id.startswith("anthropic"):
            return BedrockModel(
                model_id=self.model_id,
                client_args={"region_name": "us-east-1"},
            )

    def query(self, user_input: str):
        """
        Run the agent with the provided user input.
        This method can be called to process commands related to calendar events.
        """
        response = self.agent(user_input)
        return response
