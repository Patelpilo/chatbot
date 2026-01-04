import sys
sys.path.insert(0, '/workspaces/chatbot/backend')

from app import ai_bot


def test_generate_bot_reply_basic():
    resp = ai_bot.generate_bot_reply('hello')
    assert 'hello' in resp.lower() or 'help' in resp.lower() or 'goodbye' in resp.lower()


def test_generate_bot_reply_empty():
    resp = ai_bot.generate_bot_reply('')
    assert resp == 'Please send a message.'
