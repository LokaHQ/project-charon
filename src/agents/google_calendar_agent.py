from dotenv import load_dotenv
from pathlib import Path
import sys
from strands.models.litellm import LiteLLMModel
from strands import Agent
import os


sys.path.append(str(Path(__file__).parent.parent))
from src.tools.celander_tools import get_events, create_event
from src.utils.config_loader import load_config


# Add this to your main function for testing
def test_create_event():
    result = create_event(
        title="Test Event",
        start_time="2025-07-28T11:00:00",
        end_time="2025-07-28T13:00:00",
    )
    print(f"Direct function call result: {result}")


load_dotenv()


def main():
    config = load_config()

    api_key = os.getenv("OPENROUTER_API_KEY")

    model = LiteLLMModel(
        model_id=config.calendar_agent.model.model_id,
        client_args={
            "api_key": api_key,
        },
    )

    system_prompt = """
    You are a helpful assistant that can interact with Google Calendar. 
    You need to recommend available time slots for a user based on their calendar events. 
    You can also create new events in the calendar. 
    If the user asks for available time slots, you can call the get_events function with a duration parameter to get the next available time slots. 
    If the user wants to create an event, you can call the create_event function with the required parameters."""

    agent = Agent(
        tools=[get_events, create_event], model=model, system_prompt=system_prompt
    )

    agent(
        "Create an event in my calendar from july 28th 2025 at 2pm until 4pm with the title 'Test Event' and description 'This is a test event'. Location is 'Virtual Meeting'."
    )
    # print(test_create_event())


if __name__ == "__main__":
    main()
