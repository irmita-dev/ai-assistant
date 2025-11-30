from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, List

from .models import Conversation, Message, Role


class CorePort(Protocol):
    """Minimal interface that our session needs from the AI core."""
    def start_conversation(self, mode: str) -> Conversation: ...
    def generate_reply(self, conversation: Conversation) -> Message: ...


class HistoryPort(Protocol):
    """Minimal interface that our session needs from history storage."""
    def save(self, conversation: Conversation) -> None: ...
    def load_all(self) -> List[Conversation]: ...


@dataclass
class AssistantSession:
    """High-level chat session: handles commands + normal messages."""
    core: CorePort
    history: HistoryPort
    conversation: Conversation

    # Special token used to signal the CLI loop to exit
    EXIT_TOKEN: str = "__EXIT__"

    @classmethod
    def start(
        cls,
        core: CorePort,
        history: HistoryPort,
        mode: str = "chat",
    ) -> "AssistantSession":
        conv = core.start_conversation(mode)
        return cls(core=core, history=history, conversation=conv)

    # ──────────────────────────────────────────────────────────────
    # Public API used by CLI
    def handle_user_input(self, text: str) -> str:
        """Handle a single line of user input and return reply text.

        - normal text → send to AI, save history, return AI reply
        - /exit → return EXIT_TOKEN
        - /history → render history as multiline string
        """
        text = text.strip()
        if not text:
            return ""

        if text.startswith("/"):
            return self._handle_command(text)

        # Normal chat message
        self.conversation.add_user_message(text)
        reply = self.core.generate_reply(self.conversation)
        # Persist updated conversation
        self.history.save(self.conversation)
        return reply.content

    # ──────────────────────────────────────────────────────────────
    # Internal helpers
    def _handle_command(self, cmd: str) -> str:
        if cmd == "/exit":
            return self.EXIT_TOKEN

        if cmd == "/history":
            conversations = self.history.load_all()
            lines: list[str] = []

            for conv in conversations:
                for msg in conv.messages:
                    prefix = self._role_label(msg.role)
                    lines.append(f"{prefix}: {msg.content}")

            return "\n".join(lines) if lines else "(no history yet)"

        return "Unknown command. Try typing a message, /history, or /exit."

    @staticmethod
    def _role_label(role: Role) -> str:
        if role is Role.USER:
            return "User"
        if role is Role.ASSISTANT:
            return "Assistant"
        return "System"