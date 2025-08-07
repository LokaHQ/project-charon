from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.agent import AgentAbstract
from src.tools.big_boss_orchestrator_tools import (
    home_agent_query,
    task_agent_query,
)
from src.tools.sleep_tracking_tools import (
    add_sleep_data,
    get_sleep_data,
    update_weekly_summary,
)
from src.utils.prompts import BIG_BOSS_ORCHESTRATOR_AGENT_PROMPT
from src.utils.tts_callback_handler import tts_callback_handler
from strands_tools import journal


class BigBossOrchestratorAgent(AgentAbstract):
    """
    The Big Boss Orchestrator Agent that coordinates between different agents.
    It can query the Task Agent and Home Agent.
    """

    def get_agent_config(self):
        """Return the specific configuration section for this agent."""
        return self.config.big_boss_orchestrator_agent

    def get_prompt(self):
        """Return the system prompt for this agent."""
        return BIG_BOSS_ORCHESTRATOR_AGENT_PROMPT

    def get_tools(self):
        """Return the list of tools available for this agent."""
        return [
            task_agent_query,
            home_agent_query,
            add_sleep_data,
            get_sleep_data,
            update_weekly_summary,
            journal,
        ]

    def pass_callback_handler(self):
        """
        Pass a callback handler to the agent's model.

        Returns:
            The callback handler passed to the model.
        """
        return tts_callback_handler
