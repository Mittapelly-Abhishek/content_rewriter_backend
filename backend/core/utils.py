from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY)


# ------------------------------------------------
# 1. REWRITE TEXT (already working for you)
# ------------------------------------------------
def rewrite_content(text, tone="formal", language="english"):
    """
    Rewrite text using Groq API with tone + target language.
    language: e.g. "english", "hindi", "telugu", "tamil", "spanish"
    """

    language = (language or "").lower().strip()

    if language in ["english", "en", ""]:  # default behaviour
        prompt = f"Rewrite the following text in a {tone} tone:\n\n{text}"
    else:
        prompt = (
            f"Rewrite the following text in a {tone} tone, and respond ONLY in "
            f"{language} language:\n\n{text}"
        )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert content rewriter."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


# ------------------------------------------------
# 2. SPEECH → TEXT + TRANSLATION (NEW)
# ------------------------------------------------
from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def speech_to_text(audio_file, target_language="english"):
    """
    1. Transcribe audio using Groq Whisper
    2. Translate to target_language using Llama (optional)
    """

    target_language = (target_language or "english").lower().strip()

    # ---- Convert UploadedFile → bytes ----
    audio_bytes = audio_file.read()

    # ---------- STEP 1: TRANSCRIBE ----------
    transcription = client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=("audio.mp3", audio_bytes),  # REQUIRED format (filename, bytes)
    )

    # Groq response object → use `.text` (NOT index)
    original_text = transcription.text

    # If translation is NOT needed
    if target_language in ["original", "same", "auto", "none"]:
        return original_text

    # ---------- STEP 2: TRANSLATE ----------
    prompt = f"Translate the following text to {target_language}:\n\n{original_text}"

    translation = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    translated_text = translation.choices[0].message.content

    return translated_text
