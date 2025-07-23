from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands_tools import file_read
from dotenv import load_dotenv
from pathlib import Path
import sys
import os
sys.path.append(str(Path(__file__).parent.parent))
from src.tools.file_search_tools import find_folder_from_name

from src.utils.prompts import file_agent_prompt

from src.utils.config_loader import load_config


load_dotenv()

def main():

    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

    config= load_config()

    print(config)



    model = LiteLLMModel(
                model_id=config.files_agent.model.model_id,
                client_args={
                    "api_key": openrouter_api_key,
                }
            )
    
    system_prompt = file_agent_prompt()

    
    conversation_manager=SlidingWindowConversationManager(
        window_size=10,
    )

    agent=Agent(
                tools=[file_read, find_folder_from_name],
                model=model,
                system_prompt=system_prompt,
                conversation_manager=conversation_manager
            )
    
    while True:
        user_input = input("Enter a command (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        response = agent(user_input)    

    #print(find_folder_from_name("project-charon"))

if __name__ == "__main__":
    main()