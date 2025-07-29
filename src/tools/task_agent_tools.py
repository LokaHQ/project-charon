import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)
from loguru import logger
from strands import tool

from agents.file_search_agent import FileSearchAgent
from agents.google_calendar_agent import CalendarAgent


@tool(
    name="file_search_agent_query",
    description="Query the file search agent to find and analyze files in a project. Useful for understanding project structure, finding specific files, or analyzing code for implementation tasks.",
)
def file_search_agent_query(question: str) -> str:
    """
    Query the file search agent with a specific question about files or project structure.

    Args:
        question (str): The question to ask the file search agent. Examples:
                       - "For the project called Charon, how long would it take me to implement a file writing tool?"
                       - "What files in the CleanEnergy project handle data processing?"
                       - "Show me the structure of the authentication module"

    Returns:
        Union[str, Dict[str, Any]]: The agent's response, which could be a string or structured output
    """
    logger.info(f"Querying file search agent with question: {question}")

    try:
        agent = FileSearchAgent()
        response = agent.query(question)
        logger.success("File search agent query completed successfully")
        return response

    except Exception as e:
        error_msg = f"Error querying file search agent: {str(e)}"
        logger.error(error_msg)
        return error_msg


# @tool(
#     name="file_search_agent_interactive_session",
#     description="Start an interactive session with the file search agent for multiple queries. Use this when you need to have a conversation about project structure or multiple file-related questions."
# )
# def file_search_agent_interactive_session():
#     """
#     Start an interactive session with the file search agent.
#     Note: This will start a command-line interactive session.

#     Returns:
#         str: Status message about starting the interactive session
#     """


@tool(
    name="google_calendar_agent_query",
    description="Query the Google Calendar agent to manage calendar events. Can retrieve events, create new events, and provide scheduling assistance.",
)
def google_calendar_agent_query(query: str) -> str:
    """
    Query the Google Calendar agent with a calendar-related request.

    Args:
        query (str): The calendar-related query. Examples:
                    - "What events do I have today?"
                    - "Create a meeting for tomorrow at 2 PM"
                    - "Show me my schedule for the next 3 days"
                    - "When am I free this week?"

    Returns:
        str: The agent's response regarding calendar operations
    """
    try:
        logger.info(f"Querying calendar agent with: {query}")
        agent = CalendarAgent()
        response = agent.query(query)
        logger.success("Calendar agent query completed successfully")
        return str(response)
    except Exception as e:
        error_msg = f"Error querying calendar agent: {str(e)}"
        logger.error(error_msg)
        return error_msg


# @tool(
#     name="google_calendar_agent_interactive_session",
#     description="Start an interactive session with the Google Calendar agent for multiple calendar operations."
# )
# def google_calendar_agent_interactive_session() -> str:
#     """
#     Start an interactive session with the Google Calendar agent.
#     This allows for multiple calendar queries in a conversational format.

#     Returns:
#         str: Status message about the interactive session
#     """
