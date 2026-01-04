import time
import uuid
import requests
import json
import subprocess
import pytest
from websocket import create_connection

BASE = "http://127.0.0.1:8000"
WS_BASE = "ws://127.0.0.1:8000"


@pytest.fixture(scope="session", autouse=True)
def start_server():
    """Ensure the FastAPI server is running. If not, start uvicorn as a background process for the test session."""
    # Quick check to see if server is reachable
    try:
        requests.get(BASE, timeout=1)
        started = False
    except Exception:
        started = True
        import sys
        proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Wait for the server to accept connections
        for _ in range(60):
            try:
                requests.get(BASE, timeout=1)
                break
            except Exception:
                time.sleep(0.5)
        else:
            proc.terminate()
            raise RuntimeError("Failed to start uvicorn server for tests")

    yield

    # Teardown: stop the server we started
    if started:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()

def random_email():
    return f"smoke+{uuid.uuid4().hex[:8]}@example.com"

def test_register_login_and_bot_reply():
    email = random_email()
    password = "smokepass"

    r = requests.post(f"{BASE}/auth/register", json={"email": email, "password": password}, timeout=5)
    assert r.status_code == 200
    assert r.json().get("message") == "User registered successfully"

    r = requests.post(f"{BASE}/auth/login", json={"email": email, "password": password}, timeout=5)
    assert r.status_code == 200
    token = r.json().get("access_token")
    assert token

    url = f"{WS_BASE}/ws/chat?token={token}"
    ws = create_connection(url, timeout=5)

    msg = {"recipient": "whatease_bot", "content": "Hello bot"}
    ws.send(json.dumps(msg))

    recv1 = json.loads(ws.recv())
    recv2 = json.loads(ws.recv())

    senders = {recv1.get("sender"), recv2.get("sender")}
    contents = {recv1.get("content"), recv2.get("content")}

    assert email in senders
    assert "whatease_bot" in senders
    assert any("hello" in (c or "").lower() for c in contents)

    ws.close()
