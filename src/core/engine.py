from src.core.models import Conversation, Message, Role


class AICore:
    """Fake AI engine (placeholder until real LLM integration)."""

    def generate_reply(self, conversation: Conversation) -> str:
        # last user message
        last = conversation.last_user_message()

        # simple fake intelligence
        reply = f"I see you said: '{last}'. I'm here to help!"

        # add AI reply to conversation
        conversation.add_message(Message(role=Role.AI, content=reply))

        return reply