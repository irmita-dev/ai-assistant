import pytest

from src.core import AICore
from src.core.models import Conversation, Message, Role


class FakeEngine:
    """Fake AI engine for testing."""
    def generate_reply(self, conv: Conversation) -> str:
        last = conv.last_user_message()
        return f"[FAKE-REPLY] You said: {last}"


def test_start_conversation():
    core = AICore(engine=FakeEngine())
    conv = core.start_conversation("chat")

    assert isinstance(conv, Conversation)
    assert conv.mode == "chat"
    assert conv.messages == []


def test_core_ask_generates_reply():
    core = AICore(engine=FakeEngine())
    conv = core.start_conversation("chat")

    reply = core.ask("Hello AI")

    # Reply should match fake engine output
    assert reply == "[FAKE-REPLY] You said: Hello AI"

    # Conversation should now contain USER + ASSISTANT messages
    assert len(conv.messages) == 2
    assert conv.messages[0].role == Role.USER
    assert conv.messages[0].content == "Hello AI"

    assert conv.messages[1].role == Role.ASSISTANT
    assert conv.messages[1].content == reply


def test_get_history_returns_all_messages():
    core = AICore(engine=FakeEngine())
    core.start_conversation("chat")

    core.ask("Hi")
    core.ask("How are you?")

    history = core.get_history()

    assert len(history) == 4 # 2 user + 2 assistant
    assert history[0].role == Role.USER
    assert history[-1].role == Role.ASSISTANT