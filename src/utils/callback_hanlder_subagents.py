from rich.panel import Panel
from rich import print as rprint
from rich.padding import Padding


def home_agent_callback(**kwargs):
    """
    Custom callback handler for the Home Agent.
    This can be used to handle specific events or logging.
    """
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                rprint(
                    Padding(
                        Panel(
                            f" [cyan] 🎭 Home Agent: [/cyan] {text}",
                            title="🎭 Home Agent",
                            subtitle="Ready for leisure & entertainment",
                            border_style="cyan",
                        ),
                        pad=(0, 0, 0, 8),
                    )
                )


def recommender_agent_callback(**kwargs):
    """
    Custom callback handler for the Home Agent.
    This can be used to handle specific events or logging.
    """
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                rprint(
                    Padding(
                        Panel(
                            f" [dark blue] ⏯️ Recommender Agent: [/dark blue] {text}",
                            title="⏯️ Recommender Agent",
                            subtitle="Ready for youtube or substack recommendations",
                            border_style="dark_blue",
                        ),
                        pad=(0, 0, 0, 16),
                    )
                )


def book_agent_callback(**kwargs):
    """
    Custom callback handler for the Book Agent.
    This can be used to handle specific events or logging.
    """
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                rprint(
                    Padding(
                        Panel(
                            f" [green] 📚 Book Agent: [/green] {text}",
                            title="📚 Book Agent",
                            subtitle="Ready to manage your book collection",
                            border_style="green",
                        ),
                        pad=(0, 0, 0, 16),
                    )
                )


def movie_agent_callback(**kwargs):
    """
    Custom callback handler for the Movie Agent.
    This can be used to handle specific events or logging.
    """
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                rprint(
                    Padding(
                        Panel(
                            f" [red] 🎬 Movie Agent: [/red] {text}",
                            title="🎬 Movie Agent",
                            subtitle="Ready to manage your movie collection",
                            border_style="red",
                        ),
                        pad=(0, 0, 0, 16),
                    )
                )


def task_agent_callback(**kwargs):
    """
    Custom callback handler for the Task Agent.
    This can be used to handle specific events or logging.
    """
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                rprint(
                    Padding(
                        Panel(
                            f" [green] 📝 Task Agent: [/green] {text}",
                            title="📝 Task Agent",
                            subtitle="Ready to manage your tasks",
                            border_style="green",
                        ),
                        pad=(0, 0, 0, 8),
                    )
                )


def file_agent_callback(**kwargs):
    """
    Custom callback handler for the File Agent.
    This can be used to handle specific events or logging.
    """
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                rprint(
                    Padding(
                        Panel(
                            f" [blue] 📂 File Agent: [/blue] {text}",
                            title="📂 File Agent",
                            subtitle="Ready to manage your files",
                            border_style="blue",
                        ),
                        pad=(0, 0, 0, 24),
                    )
                )


def calendar_agent_callback(**kwargs):
    """
    Custom callback handler for the Calendar Agent.
    This can be used to handle specific events or logging.
    """
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                rprint(
                    Padding(
                        Panel(
                            f" [red] 📅 Calendar Agent: [/red] {text}",
                            title="📅 Calendar Agent",
                            subtitle="Ready to manage your calendar",
                            border_style="red",
                        ),
                        pad=(0, 0, 0, 24),
                    )
                )


def github_agent_callback(**kwargs):
    """
    Custom callback handler for the GitHub Agent.
    This can be used to handle specific events or logging.
    """
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                rprint(
                    Padding(
                        Panel(
                            f" [blue] 🐙 GitHub Agent: [/blue] {text}",
                            title="🐙 GitHub Agent",
                            subtitle="Ready to manage your GitHub repositories",
                            border_style="blue",
                        ),
                        pad=(0, 0, 0, 24),
                    )
                )
