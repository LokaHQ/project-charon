from kokoro import KPipeline
import sounddevice as sd
import numpy as np


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
                generator = pipeline(text, voice=blend, speed=1.2, split_pattern=r"\n+")
                for i, (gs, ps, audio) in enumerate(generator):
                    print(gs)
                    sd.play(audio, 24000)
                    sd.wait()
