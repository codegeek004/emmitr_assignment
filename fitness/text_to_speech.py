from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
# library used for importing variables from .env
from decouple import config

# This function returns the text to speech translation as a variable, takes text as argument


def text_to_speech(text):
    elevenlabs = ElevenLabs(
        api_key=config('ELEVENLABS_API_KEY', cast=str)
    )
    # calls the elevenlabs api
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=config('VOICE_ID', cast=str),
        model_id=config('MODEL_ID', cast=str),
        output_format=config('OUTPUT_FORMAT', cast=str),
    )
    # stores the audio in speech variable
    speech = play(audio)
    return speech
