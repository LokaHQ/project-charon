import sys
from pathlib import Path

from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.models.litellm import LiteLLMModel

sys.path.append(str(Path(__file__).parent.parent))
import os

from dotenv import load_dotenv

from src.tools.task_agent_tools import (
    file_search_agent_query,
    google_calendar_agent_query,
)
from src.utils.config_loader import load_config
from utils.prompts import TASK_AGENT_PROMPT

load_dotenv()


class TaskAgent:
    """
    A main agent that can delegate tasks to specialized sub-agents.
    This agent can handle both file/project analysis and calendar management.
    """

    def __init__(self):
        self.config = load_config()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = LiteLLMModel(
            model_id=self.config.task_agent.model.model_id,
            client_args={
                "api_key": self.api_key,
            },
        )
        self.conversation_manager = SlidingWindowConversationManager(window_size=10)
        self.agent = Agent(
            tools=[google_calendar_agent_query, file_search_agent_query],
            model=self.model,
            system_prompt=TASK_AGENT_PROMPT,
            conversation_manager=self.conversation_manager,
        )

    def query(self, question: str) -> str:
        """
        Run a single query against the agent.

        Args:
            question: The question to ask the agent

        Returns:
            The agent's response
        """
        return self.agent(question)
