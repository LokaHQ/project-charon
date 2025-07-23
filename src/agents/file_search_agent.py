import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.models.litellm import LiteLLMModel
from strands_tools import file_read

sys.path.append(str(Path(__file__).parent.parent))
from src.tools.file_search_tools import find_folder_from_name
from src.utils.config_loader import load_config
from src.utils.prompts import FILE_AGENT_PROMPT

load_dotenv()


def main():
    """
    Main function to run the file search agent.
    It initializes the agent with the necessary tools and configurations,
    and starts an interactive loop for user commands.
    """

    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

    config = load_config()

    print(config)

    model = LiteLLMModel(
        model_id=config.files_agent.model.model_id,
        client_args={
            "api_key": openrouter_api_key,
        },
    )

    system_prompt = FILE_AGENT_PROMPT

    conversation_manager = SlidingWindowConversationManager(
        window_size=10,
    )

    agent = Agent(
        tools=[file_read, find_folder_from_name],
        model=model,
        system_prompt=system_prompt,
        conversation_manager=conversation_manager,
    )

    while True:
        user_input = input("Enter a command (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        agent(user_input)

    # print(find_folder_from_name("project-charon"))


if __name__ == "__main__":
    main()
