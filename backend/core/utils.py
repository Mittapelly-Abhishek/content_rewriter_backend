from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def rewrite_content(text, tone="formal"):
    """
    Rewrite text using Groq API (Latest models)
    """

    prompt = f"Rewrite the following text in a {tone} tone:\n\n{text}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # New working model
        messages=[
            {"role": "system", "content": "You are an expert content rewriter."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    # ✅ Groq uses: response.choices[0].message.content
    return response.choices[0].message.content
