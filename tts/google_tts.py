import os
from dotenv import load_dotenv
from google.cloud import texttospeech

load_dotenv()

# Set credentials
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

client = texttospeech.TextToSpeechClient()

def generate_google_tts(text):

    synthesis_input = texttospeech.SynthesisInput(
        text=text
    )

    voice = texttospeech.VoiceSelectionParams(
        language_code="id-ID",
        name="id-ID-Standard-A"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return response.audio_content