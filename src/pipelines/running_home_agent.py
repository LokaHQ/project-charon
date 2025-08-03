import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from agents.home_agent import HomeAgent


def main():
    """
    Main function to run the Home Agent.
    It initializes the agent with the necessary tools and configurations,
    and starts an interactive loop for user commands.
    """
    home_agent = HomeAgent()

    print("Welcome to the Home Agent!")
    print("You can ask me to manage your movies, shows, and books.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = home_agent.agent(user_input)
        print(
            f"Agent: {response.message if hasattr(response, 'message') else response}"
        )


if __name__ == "__main__":
    main()
