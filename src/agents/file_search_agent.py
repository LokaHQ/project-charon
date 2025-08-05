import sys
from pathlib import Path

from dotenv import load_dotenv
from strands_tools import file_read

sys.path.append(str(Path(__file__).parent.parent))

from src.tools.file_search_tools import find_folder_from_name
from src.agents.agent import AgentAbstract
from src.utils.prompts import FILE_AGENT_PROMPT

load_dotenv()


class FileSearchAgent(AgentAbstract):
    """File Search Agent that can search for files and folders based on user queries."""

    def get_agent_config(self):
        """Return the specific configuration section for this agent."""
        return self.config.files_agent

    def get_prompt(self):
        """Return the system prompt for this agent."""
        return FILE_AGENT_PROMPT

    def get_tools(self):
        """Return the list of tools available for this agent."""

        return [
            file_read,
            find_folder_from_name,
        ]
