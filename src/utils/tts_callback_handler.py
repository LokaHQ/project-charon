from kokoro import KPipeline
import sounddevice as sd
import numpy as np
from rich import print as rprint


def tts_callback_handler(**kwargs):
    """
    Custom callback handler for the agent.
    This can be used to handle specific events or logging.
    """
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        pipeline = KPipeline(lang_code="a")
        bm_lewis = pipeline.load_voice("bm_lewis")
        am_michael = pipeline.load_voice("am_michael")
        blend = np.add(bm_lewis * 0.8, am_michael * 0.2)

        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                # Split original text (keeping formatting)
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

                rprint("[bold dark_magenta]💀🛶  Charon: [/bold dark_magenta]")

                for i, (formatted_part, (gs, ps, audio)) in enumerate(
                    zip(formatted_parts, audio_parts)
                ):
                    # Display with original formatting
                    rprint(f"{formatted_part}")
                    # Play corresponding audio
                    sd.play(audio, 24000)
                    sd.wait()
