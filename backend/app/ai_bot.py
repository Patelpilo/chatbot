import os
import asyncio

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

try:
    import openai
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
except Exception:
    openai = None

def _rule_based_reply(message: str) -> str:
    msg = message.lower()

    if "hello" in msg or "hi" in msg:
        return "Hello! I am WhatsEase AI Bot. How can I help you?"

    if "help" in msg:
        return "You can chat with users or ask me general questions."

    if "bye" in msg:
        return "Goodbye! Have a great day 😊"

    return "I'm still learning. Please ask something else!"

async def generate_bot_reply(message: str) -> str:
    """Generate a reply for the bot. Uses OpenAI when OPENAI_API_KEY is set and the `openai` package
    is available; otherwise falls back to the built-in rule-based replies.
    """
    if OPENAI_API_KEY and openai is not None:
        try:
            resp = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are WhatsEase AI Bot that replies briefly and helpfully."},
                    {"role": "user", "content": message},
                ],
                temperature=0.6,
                max_tokens=150,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print("OpenAI error, falling back to rule-based reply:", e)
            return _rule_based_reply(message)

    return _rule_based_reply(message)
