def generate_bot_reply(message: str) -> str:
    """Synchronous rule-based reply generator.
    This is prototype bot.
    """
    msg = (message or "").lower().strip()

    if not msg:
        return "Please send a message."

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
