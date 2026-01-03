def generate_bot_reply(message: str) -> str:
    msg = message.lower()

    if "hello" in msg or "hi" in msg:
        return "Hello! I am WhatsEase AI Bot. How can I help you?"

    if "help" in msg:
        return "You can chat with users or ask me general questions."

    if "bye" in msg:
        return "Goodbye! Have a great day 😊"

    return "I'm still learning. Please ask something else!"
