from __future__ import annotations

from src.core.models import Conversation


class AICore:
    """Coordinates Conversation and AI engine."""

    def __init__(self, engine):
        self.engine = engine
        self.conversation: Conversation | None = None

    def start_conversation(self, mode: str) -> Conversation:
        self.conversation = Conversation(mode=mode)
        return self.conversation

    def ask(self, user_text: str) -> str:
        if self.conversation is None:
            raise RuntimeError("Conversation not started")

        # Add user message
        self.conversation.add_user_message(user_text)

        # Generate reply
        reply = self.engine.generate_reply(self.conversation)

        # Add assistant message
        self.conversation.add_assistant_message(reply)

        return reply

    def get_history(self):
        if self.conversation is None:
            return []
        return self.conversation.messages