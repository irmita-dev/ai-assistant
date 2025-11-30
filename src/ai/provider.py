"""
Fake AI provider (later can be replaced with real API: OpenAI, Gemini, etc.)
"""

from typing import Protocol
from src.core.models import Conversation, Message, Role


class AIProvider(Protocol):
    """Protocol for plugging different AI backends."""
    def generate(self, conversation: Conversation) -> str:
        ...


class FakeAIProvider:
    """Simple fake AI — echoes the user message."""
    def generate(self, conversation: Conversation) -> str:
        last_user = conversation.last_user_message()
        if not last_user:
            return "Hello! How can I help you?"
        return f"🤖 I hear you said: {last_user}"


class AICore:
    """Bridge between Conversation and an AIProvider."""

    def __init__(self, provider: AIProvider):
        self.provider = provider

    def start_conversation(self, mode: str) -> Conversation:
        return Conversation(mode=mode)

    def generate_reply(self, conversation: Conversation) -> Message:
        reply_text = self.provider.generate(conversation)
        msg = Message(role=Role.ASSISTANT, content=reply_text)
        conversation.messages.append(msg)
        return msg