from rich import print as rprint
from rich.status import Status
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.tts_manager import TTSManager

tts_manager = TTSManager()


def tts_callback_handler(**kwargs):
    """
    Optimized callback handler that reuses TTS initialization.
    """
    with Status(
        "[bold dark_magenta]Navigating your request...",
        spinner="bouncingBar",
    ):
        if "message" in kwargs and kwargs["message"].get("role") == "assistant":
            for content in kwargs["message"]["content"]:
                if isinstance(content, dict) and "text" in content:
                    text = content["text"]

                    rprint("\n [bold dark_magenta]💀🛶 Charon:[/bold dark_magenta]")

                    # Use the singleton TTS manager
                    if tts_manager.is_available():
                        tts_manager.speak(text)
                    else:
                        # Fallback to text-only if TTS fails
                        rprint(text)

        if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
            tool_use = kwargs["current_tool_use"]
            tool_name = tool_use.get("name")
            tool_input = tool_use.get("input", "")
            if tool_name in ["home_agent_query", "task_agent_query"]:
                try:
                    if tool_input and tool_input.endswith('"}'):
                        parsed_input = json.loads(tool_input)
                        query = parsed_input.get("query", "")

                        agent_name = (
                            tool_name.replace("_query", "").replace("_", " ").title()
                        )

                        rprint(f"\n🔄 [bold cyan]Consulting {agent_name}[/bold cyan]")
                        rprint(f"   [dim]Query: {query}[/dim]")

                except json.JSONDecodeError:
                    pass
                except Exception as e:
                    rprint(f"[dim red]Debug: Error parsing tool input: {e}[/dim red]")


def silent_callback_handler(**kwargs):
    """
    Silent callback handler (no TTS, just text).
    """
    with Status(
        "[bold dark_magenta]Navigating your request...",
        spinner="bouncingBar",
    ):
        if "message" in kwargs and kwargs["message"].get("role") == "assistant":
            for content in kwargs["message"]["content"]:
                if isinstance(content, dict) and "text" in content:
                    text = content["text"]

                    rprint("\n [bold dark_magenta]💀🛶 Charon: [/bold dark_magenta]")
                    rprint(text)

        if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
            tool_use = kwargs["current_tool_use"]
            tool_name = tool_use.get("name")
            tool_input = tool_use.get("input", "")
            if tool_name in ["home_agent_query", "task_agent_query"]:
                try:
                    if tool_input and tool_input.endswith('"}'):
                        parsed_input = json.loads(tool_input)
                        query = parsed_input.get("query", "")

                        agent_name = (
                            tool_name.replace("_query", "").replace("_", " ").title()
                        )

                        rprint(f"\n🔄 [bold cyan]Consulting {agent_name}[/bold cyan]")
                        rprint(f"   [dim]Query: {query}[/dim]")

                except json.JSONDecodeError:
                    pass
                except Exception as e:
                    rprint(f"[dim red]Debug: Error parsing tool input: {e}[/dim red]")


# Optional: Pre-initialize TTS at module load (uncomment if you want immediate initialization)
def initialize_tts():
    """Call this at startup if you want to pre-load TTS"""
    global tts_manager
    if tts_manager.is_available():
        rprint("[green]✅ TTS pre-initialized successfully[/green]")
    else:
        rprint("[yellow]⚠️ TTS initialization failed, will use text-only mode[/yellow]")
