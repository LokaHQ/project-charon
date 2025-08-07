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
                    Panel(
                        Padding(
                            f" [cyan] 🎭 Home Agent: [/cyan] {text}", pad=(0, 0, 0, 1)
                        ),
                        title="🎭 Home Agent",
                        subtitle="Ready for leisure & entertainment",
                        border_style="cyan",
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
                    Panel(
                        Padding(
                            f" [dark blue] ⏯️ Recommender Agent: [/dark blue] {text}",
                            pad=(0, 0, 0, 2),
                        ),
                        title="⏯️ Recommender Agent",
                        subtitle="Ready for youtube or substack recommendations",
                        border_style="dark_blue",
                    )
                )
