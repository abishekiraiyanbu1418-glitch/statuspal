import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Fast model first, bigger model as backup
MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]

SYSTEM_PROMPT = """
You explain PayPal payment statuses to everyday users in plain language.

Rules:
- Only explain what the transaction data supports.
- Label each point either "Confirmed by data" or "Common cause, not confirmed".
- If the data does not explain the status, say "I can't tell from this data"
  and suggest where the user can get an answer.
- End with numbered next steps.
- Never claim to know PayPal's internal risk decisions.
- "Confirmed by data" may ONLY be used for facts literally present in the
  transaction fields provided (for example the amount, currency, or status value).
- Anything about what a status generally means, or why it happens, must be
  labeled "Common cause, not confirmed".
- Keep the whole answer under 150 words.
"""


def build_request(transaction):
    return "Explain this transaction:\n" + json.dumps(transaction, indent=2)


def explain(transaction):
    """Full answer at once. Used for terminal testing."""
    last_error = None
    for attempt in range(3):
        for model_name in MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=build_request(transaction),
                    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
                )
                return response.text
            except Exception as e:
                last_error = e
                print(f"[{model_name}] failed: {str(e)[:120]}")
        time.sleep(3)
    print("All attempts failed. Last error:", last_error)
    return "Sorry, the AI service is busy right now. Please try again in a moment."


def explain_stream(transaction):
    """Answer word by word. Used by the web page so text appears quickly."""
    started = False
    for model_name in MODELS:
        try:
            stream = client.models.generate_content_stream(
                model=model_name,
                contents=build_request(transaction),
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            for chunk in stream:
                if chunk.text:
                    started = True
                    yield chunk.text
            return
        except Exception as e:
            print(f"[{model_name}] failed: {str(e)[:120]}")
            if started:
                return
    yield "Sorry, the AI service is busy right now. Please try again in a moment."


if __name__ == "__main__":
    test = {"status": "ON_HOLD", "amount": "300.00", "currency": "USD"}
    print(explain(test))