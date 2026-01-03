from fastapi import APIRouter, WebSocket
from jose import jwt
from app.ai_bot import generate_bot_reply

router = APIRouter()

SECRET_KEY = "secret123"
ALGORITHM = "HS256"


@router.websocket("/ws/chat")
async def chat_socket(ws: WebSocket, token: str):
    await ws.accept()

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = payload["sub"]

    while True:
        data = await ws.receive_json()
        content = data["content"]
        recipient = data["recipient"]

        await ws.send_json({
            "sender": user,
            "content": content
        })

        if recipient == "whatease_bot":
            bot_reply = generate_bot_reply(content)
            await ws.send_json({
                "sender": "whatease_bot",
                "content": bot_reply
            })
