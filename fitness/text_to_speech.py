from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from decouple import config


def text_to_speech(text):
    elevenlabs = ElevenLabs(
        api_key=config('ELEVENLABS_API_KEY', cast=str)
    )

    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=config('VOICE_ID', cast=str),
        model_id=config('MODEL_ID', cast=str),
        output_format=config('OUTPUT_FORMAT', cast=str),
    )

    speech = play(audio)
    return speech
