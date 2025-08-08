from kokoro import KPipeline
import sounddevice as sd
import numpy as np
from rich import print as rprint
from rich.status import Status


def tts_callback_handler(**kwargs):
    """
    Custom callback handler for the agent.
    This can be used to handle specific events or logging.
    """
    with Status(
        "[bold dark_magenta]Navigating your request...",
        spinner="bouncingBar",
    ):
        if "message" in kwargs and kwargs["message"].get("role") == "assistant":
            pipeline = KPipeline(lang_code="a")
            bm_lewis = pipeline.load_voice("bm_lewis")
            am_michael = pipeline.load_voice("am_michael")
            blend = np.add(bm_lewis * 0.8, am_michael * 0.2)

            for content in kwargs["message"]["content"]:
                if isinstance(content, dict) and "text" in content:
                    text = content["text"]

                    formatted_parts = [
                        part.strip() for part in text.split("\n") if part.strip()
                    ]

                    clean_parts = []
                    for part in formatted_parts:
                        clean_part = (
                            part.replace("**", "").replace("[", "").replace("]", "")
                        )
                        clean_parts.append(clean_part)

                    text_readable = "\n".join(clean_parts)

                    generator = pipeline(
                        text_readable, voice=blend, speed=1.2, split_pattern=r"\n+"
                    )

                    audio_parts = list(generator)
                    rprint("\n [bold dark_magenta]💀🛶 Charon:[/bold dark_magenta]")
                    for i, (formatted_part, (gs, ps, audio)) in enumerate(
                        zip(formatted_parts, audio_parts)
                    ):
                        rprint(f"{formatted_part}")

                        sd.play(audio, 24000)
                        sd.wait()

        if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
            tool_name = kwargs["current_tool_use"]["name"]
            if "home_agent_query" == tool_name or "task_agent_query" == tool_name:
                rprint(
                    "   🔄 [dim yellow]Consulting specialized agents...[/dim yellow]"
                )


def silent_callback_handler(**kwargs):
    """
    A silent callback handler that does nothing.
    This is used when the agent operates in silent mode.
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
