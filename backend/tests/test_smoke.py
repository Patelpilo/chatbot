import time
import uuid
import requests
import json
from websocket import create_connection

BASE = "http://127.0.0.1:8000"
WS_BASE = "ws://127.0.0.1:8000"


def random_email():
    return f"smoke+{uuid.uuid4().hex[:8]}@example.com"


def test_register_login_and_bot_reply():
    email = random_email()
    password = "smokepass"

    # Register
    r = requests.post(f"{BASE}/auth/register", json={"email": email, "password": password}, timeout=5)
    assert r.status_code == 200
    assert r.json().get("message") == "User registered successfully"

    # Login
    r = requests.post(f"{BASE}/auth/login", json={"email": email, "password": password}, timeout=5)
    assert r.status_code == 200
    token = r.json().get("access_token")
    assert token

    # Open websocket and send message to bot
    url = f"{WS_BASE}/ws/chat?token={token}"
    ws = create_connection(url, timeout=5)

    msg = {"recipient": "whatease_bot", "content": "Hello bot"}
    ws.send(json.dumps(msg))

    # Expect echo and bot reply
    recv1 = json.loads(ws.recv())
    recv2 = json.loads(ws.recv())

    senders = {recv1.get("sender"), recv2.get("sender")}
    contents = {recv1.get("content"), recv2.get("content")}

    assert email in senders
    assert "whatease_bot" in senders
    assert any("hello" in (c or "").lower() for c in contents)

    ws.close()
