from fastapi import APIRouter, Depends
from datetime import datetime
from app.database import messages_collection
from app.utils import get_current_user
from app.models import Message
from app.ai_bot import generate_bot_reply

router = APIRouter()


@router.post("/messages/send")
def send_message(data: Message, user=Depends(get_current_user)):
    message = {
        "sender": user,
        "recipient": data.recipient,
        "content": data.content,
        "timestamp": datetime.utcnow(),
        "is_bot": False
    }
    messages_collection.insert_one(message)

    # AI BOT RESPONSE
    if data.recipient == "whatease_bot":
        bot_reply_text = generate_bot_reply(data.content)

        bot_message = {
            "sender": "whatease_bot",
            "recipient": user,
            "content": bot_reply_text,
            "timestamp": datetime.utcnow(),
            "is_bot": True
        }
        messages_collection.insert_one(bot_message)

    return {"status": "Message sent"}


@router.get("/chats/{recipient}")
def get_chat(recipient: str, user=Depends(get_current_user)):
    chats = messages_collection.find({
        "$or": [
            {"sender": user, "recipient": recipient},
            {"sender": recipient, "recipient": user}
        ]
    }).sort("timestamp", 1)

    return [
        {
            "sender": chat["sender"],
            "content": chat["content"]
        }
        for chat in chats
    ]
