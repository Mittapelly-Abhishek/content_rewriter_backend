import requests
from groq import Groq
from django.conf import settings
from itertools import cycle


# -------------------------------
# KEY ROTATION
# -------------------------------
groq_keys_cycle = cycle(settings.GROQ_API_KEYS)
openrouter_keys_cycle = cycle(settings.OPENROUTER_API_KEYS)

# AI rotation
AI_SEQUENCE = cycle(["groq", "openrouter"])


# -------------------------------
# GROQ FUNCTION (multi-key)
# -------------------------------
def groq_rewrite(prompt):
    api_key = next(groq_keys_cycle)
    client = Groq(api_key=api_key)

    print(f"Using Groq key: {api_key[:8]}...")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert content rewriter."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content


# -------------------------------
# OPENROUTER FUNCTION (multi-key)
# -------------------------------
def openrouter_rewrite(prompt):
    api_key = next(openrouter_keys_cycle)

    print(f"Using OpenRouter key: {api_key[:8]}...")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data, timeout=10)
    result = response.json()

    return result["choices"][0]["message"]["content"]


# ------------------------------------------------
# MAIN REWRITE FUNCTION (AI + KEY ROTATION)
# ------------------------------------------------
def rewrite_content(text, tone="formal", language="english"):

    language = (language or "").lower().strip()

    if language in ["english", "en", ""]:
        prompt = f"Rewrite the following text in a {tone} tone:\n\n{text}"
    else:
        prompt = (
            f"Rewrite the following text in a {tone} tone and respond ONLY in "
            f"{language} language:\n\n{text}"
        )

    #  AI rotation
    ai_choice = next(AI_SEQUENCE)
    print(f"\nUsing AI: {ai_choice}")

    try:
        if ai_choice == "groq":
            return groq_rewrite(prompt)

        elif ai_choice == "openrouter":
            return openrouter_rewrite(prompt)

    except Exception as e:
        print(f"{ai_choice} failed:", e)

    # -------------------------------
    # FALLBACK (extra safety)
    # -------------------------------
    print("Fallback to Groq")

    try:
        return groq_rewrite(prompt)
    except:
        return "All AI services are busy. Try again later."

