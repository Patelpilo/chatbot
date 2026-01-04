import os
import asyncio
from dotenv import load_dotenv

# Load .env so OPENAI_API_KEY can be set via a .env file locally
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

try:
    import openai
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
except Exception:
    openai = None


def _rule_based_reply(message: str) -> str:
    msg = message.lower().strip()

    if "hello" in msg or "hi" in msg:
        return "Hello! I am WhatsEase AI Bot. How can I help you?"

    if "help" in msg:
        return "You can chat with users or ask me general questions."

    if "bye" in msg or "goodbye" in msg:
        return "Goodbye! Have a great day 😊"

    if "what" in msg and ("do" in msg or "can" in msg or "are" in msg):
        return "I can chat, fetch chat history, and answer simple questions. Ask me anything!"

    if "how are you" in msg or "how r you" in msg:
        return "I'm a bot — I don't have feelings, but I'm here to chat and help you."

    if msg.endswith("?"):
        return "Good question — I'm still learning, but I can try: could you rephrase or ask something simpler?"

    return "I'm still learning. Please ask something else!"


async def generate_bot_reply(message: str) -> str:
    """Generate a reply for the bot. Uses OpenAI when OPENAI_API_KEY is set and the `openai` package
    is available; otherwise falls back to the built-in rule-based replies. Adds logs so workers show whether AI was used.
    """
    if OPENAI_API_KEY and openai is not None:
        try:
            print("Using OpenAI for bot reply")
            resp = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are WhatsEase AI Bot that replies briefly and helpfully."},
                    {"role": "user", "content": message},
                ],
                temperature=0.6,
                max_tokens=150,
            )
            reply = resp.choices[0].message.content.strip()
            print("OpenAI reply length:", len(reply))
            return reply
        except Exception as e:
            print("OpenAI error, falling back to rule-based reply:", e)
            return _rule_based_reply(message)

    print("OpenAI not configured or unavailable — using rule-based reply")
    return _rule_based_reply(message)
