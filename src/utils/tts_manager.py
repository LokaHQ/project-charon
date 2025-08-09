from kokoro import KPipeline
import sounddevice as sd
import numpy as np
from rich import print as rprint
from typing import Optional


class TTSManager:
    """Singleton TTS manager that initializes Kokoro only once"""

    _instance: Optional["TTSManager"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.pipeline = None
            self.voice_blend = None
            self._load_tts()
            TTSManager._initialized = True

    def _load_tts(self):
        """Initialize the TTS pipeline and voices once"""
        try:
            rprint("[dim]🔊 Initializing TTS system...[/dim]")

            # Initialize pipeline once
            self.pipeline = KPipeline(lang_code="a")

            # Load voices once
            bm_lewis = self.pipeline.load_voice("bm_lewis")
            am_michael = self.pipeline.load_voice("am_michael")

            # Create blend once
            self.voice_blend = np.add(bm_lewis * 0.8, am_michael * 0.2)

            rprint("[dim]✅ TTS system ready![/dim]")

        except Exception as e:
            rprint(f"[red]❌ Failed to initialize TTS: {e}[/red]")
            self.pipeline = None
            self.voice_blend = None

    def is_available(self) -> bool:
        """Check if TTS is available"""
        return self.pipeline is not None and self.voice_blend is not None

    def speak(self, text: str, speed: float = 1.2) -> bool:
        """Convert text to speech and play it"""
        if not self.is_available():
            return False

        try:
            # Clean up text for TTS
            formatted_parts = [
                part.strip() for part in text.split("\n") if part.strip()
            ]

            clean_parts = []
            for part in formatted_parts:
                clean_part = (
                    part.replace("**", "")
                    .replace("[", "")
                    .replace("]", "")
                    .replace("#", "")
                )
                clean_parts.append(clean_part)

            text_readable = "\n".join(clean_parts)

            # Generate audio using pre-loaded pipeline and voice
            generator = self.pipeline(
                text_readable, voice=self.voice_blend, speed=speed, split_pattern=r"\n+"
            )

            audio_parts = list(generator)

            # Play audio synchronously (you could make this async if needed)
            for i, (formatted_part, (gs, ps, audio)) in enumerate(
                zip(formatted_parts, audio_parts)
            ):
                rprint(f"{formatted_part}")
                sd.play(audio, 24000)
                sd.wait()

            return True

        except Exception as e:
            rprint(f"[red]TTS Error: {e}[/red]")
            return False
