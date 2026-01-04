import os
import asyncio
import pytest
from unittest.mock import AsyncMock, patch

import sys
sys.path.insert(0, '/workspaces/chatbot/backend')

from app import ai_bot

@pytest.mark.asyncio
async def test_generate_bot_reply_fallback():
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']

    resp = await ai_bot.generate_bot_reply('hello')
    assert 'hello' in resp.lower() or 'help' in resp.lower() or 'goodbye' in resp.lower()

@pytest.mark.asyncio
async def test_generate_bot_reply_with_openai(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'fake')
    ai_bot.OPENAI_API_KEY = 'fake'

    from types import SimpleNamespace

    fake_resp = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='This is an AI reply.'))])

    with patch.object(ai_bot, 'openai') as mock_openai:
        mock_openai.ChatCompletion.acreate = AsyncMock(return_value=fake_resp)
        resp = await ai_bot.generate_bot_reply('How are you?')
        assert 'ai reply' in resp.lower() or 'this is' in resp.lower()
