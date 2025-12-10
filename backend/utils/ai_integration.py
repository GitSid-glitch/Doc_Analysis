# import openai

# def ask_ai(question, snippet, api_key):
#     openai.api_key = api_key
#     prompt = f"{question}\n\nContext:\n{snippet}"
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message['content']





# backend/utils/ai_integration.py
# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# # default model – the one you said you're using:
# DEFAULT_MODEL = "google/gemini-2.0-flash-exp:free"

# def ask_ai(question: str, snippet: str, model: str = DEFAULT_MODEL) -> str:
#     """
#     Ask a question about some context snippet using OpenRouter.
#     Returns answer text.
#     """
#     if not OPENROUTER_API_KEY:
#         return "OPENROUTER_API_KEY is not set on the server."

#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "http://localhost:5173",
#         "X-Title": "Doc Analyzer",
#     }
#     prompt = f"{question}\n\nContext:\n{snippet}"

#     payload = {
#         "model": model,
#         "messages": [
#             {"role": "system", "content": "You are a helpful assistant for document analysis."},
#             {"role": "user", "content": prompt},
#         ],
#         "max_tokens": 512,
#         "temperature": 0.2,
#     }

#     try:
#         resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
#         resp.raise_for_status()
#         data = resp.json()
#         return data["choices"][0]["message"]["content"].strip()
#     except Exception as e:
#         print("OpenRouter / ask_ai error:", e)
#         return "AI service temporarily unavailable. Please try again later."





# backend/utils/ai_integration.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

DEFAULT_MODEL = "google/gemini-2.0-flash-exp:free"


def ask_ai(question: str, snippet: str, model: str = DEFAULT_MODEL) -> str:
    if not OPENROUTER_API_KEY:
        return (
            "AI configuration error: OPENROUTER_API_KEY is not set on the server.\n"
            "Please configure the API key in the backend environment."
        )

    # keep context reasonable to reduce token usage
    snippet = (snippet or "")[:12000]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "AI Document Analyzer (Demo)",
    }

    prompt = f"{question}\n\nContext:\n{snippet}"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant for document analysis. "
                    "Use the provided context to answer questions clearly and concisely."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "max_tokens": 512,
        "temperature": 0.2,
    }

    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)

        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()

        # 🔴 Rate limit / free tier exceeded
        if resp.status_code == 429:
            print("OpenRouter 429 (rate limit / quota):", resp.text)
            return (
                "AI request limit reached.\n\n"
                "This project is running on a **free AI API tier** "
                f"using the model `{model}` via OpenRouter.\n\n"
                "Free tiers enforce strict limits on how many requests and tokens "
                "can be used in a short period of time. The application logic is "
                "working correctly, but the external AI provider has blocked further "
                "requests until the quota resets or the plan is upgraded.\n\n"
            )

        # 🔐 Auth issue
        if resp.status_code == 401:
            return (
                "AI authentication failed (HTTP 401).\n\n"
                "The OpenRouter API key is invalid or not authorized. "
                "Update the key in the backend environment."
            )

        # 🛠 Server-side provider issue
        if 500 <= resp.status_code < 600:
            return (
                f"AI provider error (HTTP {resp.status_code}).\n\n"
                "The external AI service is currently having issues. "
                "This is not an application bug; please try again later."
            )

        # Other client errors
        return f"AI request failed with status {resp.status_code}."

    except Exception as e:
        print("OpenRouter / ask_ai exception:", e)
        return (
            "AI request could not be completed.\n\n"
            "The document processing UI is working, but the external AI service "
            "is currently unreachable (network or provider issue)."
        )