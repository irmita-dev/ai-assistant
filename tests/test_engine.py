from src.core.engine import AICore
from src.core.models import Conversation, Role


def test_ai_core_generates_reply():
    engine = AICore()

    conv = Conversation(mode="chat")
    conv.add_user_message("Hello AI, how are you?")

    reply = engine.generate_reply(conv)

    # reply must be a non-empty string
    assert isinstance(reply, str)
    assert len(reply) > 0

    # engine should add AI message to the conversation
    assert conv.messages[-1].role == Role.AI

    # reply should include context from user message (fake intelligence)
    assert "hello" in reply.lower() or "you" in reply.lower()