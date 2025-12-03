from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def speech_to_text(django_file, language="en"):
    """
    Convert audio to text using Groq Whisper (whisper-large-v3).
    django_file: request.FILES["audio"]
    """
    audio_bytes = django_file.read()

    response = client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=("audio.wav", audio_bytes),  # name, content
        # language parameter is optional; whisper can auto-detect
        # language=language,
    )

    # Groq follows OpenAI-style response
    return response.text
