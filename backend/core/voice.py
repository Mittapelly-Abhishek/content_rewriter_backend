from gtts import gTTS
from io import BytesIO

def text_to_speech(text):
    """
    Convert text to speech (MP3) using gTTS.
    Returns MP3 binary buffer.
    """
    mp3_buffer = BytesIO()
    tts = gTTS(text, lang="en")
    tts.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)
    return mp3_buffer
