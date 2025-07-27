import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from strands import Agent
from strands.models.litellm import LiteLLMModel

sys.path.append(str(Path(__file__).parent.parent))
from src.schemas.calendar_agent_returns_schema import CalendarEventInput
from src.tools.celander_tools import create_event, get_events
from src.utils.config_loader import load_config
from src.utils.prompts import CALENDAR_AGENT_PROMPT


# Add this to your main function for testing
def test_create_event():
    test_event = CalendarEventInput(
        title="Test Meeting",
        start_time="2025-07-29T10:00:00",
        end_time="2025-07-29T11:00:00",
        description="Test description",
        location="Test location",
    )

    result = create_event(test_event)
    print(f"Direct function call result: {result}")


load_dotenv()


def main():
    """
    Main function to run the Google Calendar agent.
    It initializes the agent with the necessary tools and configurations,
    """

    config = load_config()

    api_key = os.getenv("OPENROUTER_API_KEY")

    model = LiteLLMModel(
        model_id=config.calendar_agent.model.model_id,
        client_args={
            "api_key": api_key,
        },
    )

    system_prompt = CALENDAR_AGENT_PROMPT

    agent = Agent(
        tools=[get_events, create_event], model=model, system_prompt=system_prompt
    )

    agent(
        "I need to have a meeting with John tomorrow for 1 hour. Create an event for 28th July 2025 from 17:00 to 18:00."
    )
    # print(test_create_event())


if __name__ == "__main__":
    main()
