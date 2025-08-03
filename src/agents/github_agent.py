from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters
from dotenv import load_dotenv
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from src.utils.config_loader import load_config
from src.utils.prompts import GITHUB_AGENT_PROMPT
from strands.models.litellm import LiteLLMModel
from strands.models import BedrockModel

load_dotenv()


class GitHubAgent:
    """
    A GitHub agent that can interact with GitHub repositories using the Model Context Protocol (MCP).
    It can list repositories and fetch README files from the most recent project.
    """

    def __init__(self):
        self.config = load_config()
        self.api_key = os.getenv("GITHUB_TOKEN")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.github_client = self._initialize_github_client()
        self.model_id = self.config.github_agent.model.model_id
        self.model = self.initialize_model()

    def initialize_model(self):
        """
        Load the model for the GitHub agent.
        This method is called during initialization to set up the agent's model.
        """
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

    def _initialize_github_client(self):
        """Initialize the GitHub client using MCP."""
        return MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-github"],
                    env={"GITHUB_PERSONAL_ACCESS_TOKEN": self.api_key},
                )
            )
        )

    def query(self, user_input: str):
        """
        Run the agent with the provided user input.
        This method can be called to process commands related to GitHub repositories.
        """
        with self.github_client:
            agent = Agent(
                model=self.model,
                tools=self.github_client.list_tools_sync(),
                system_prompt=GITHUB_AGENT_PROMPT,
            )

            response = agent(user_input)

        return response
