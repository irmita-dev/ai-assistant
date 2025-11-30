from src.core.models import Conversation, Role
from src.core.app import AssistantSession


class DummyCore:
    """Fake core used only for testing AssistantSession."""
    def __init__(self) -> None:
        self.last_prompt: str | None = None

    def start_conversation(self, mode: str) -> Conversation:
        return Conversation(mode=mode)

    def generate_reply(self, conversation: Conversation):
        # Remember what user said (for assertions)
        self.last_prompt = conversation.last_user_message()
        # Fake AI reply
        conversation.add_assistant_message(f"AI: {self.last_prompt}")
        return conversation.messages[-1]


class FakeHistory:
    """In-memory history store for tests."""
    def __init__(self) -> None:
        self.saved: list[Conversation] = []

    def save(self, conversation: Conversation) -> None:
        self.saved.append(conversation)

    def load_all(self) -> list[Conversation]:
        return list(self.saved)


def test_session_handles_user_message_and_saves_history():
    core = DummyCore()
    history = FakeHistory()
    session = AssistantSession.start(core=core, history=history, mode="chat")

    reply_text = session.handle_user_input("Hello AI")

    # AI core got the right text
    assert core.last_prompt == "Hello AI"
    # We returned assistant reply text
    assert reply_text.startswith("AI:")
    # Conversation was saved to history
    assert len(history.saved) == 1
    conv = history.saved[0]
    assert conv.messages[-1].role is Role.ASSISTANT


def test_session_exit_command_returns_exit_token():
    core = DummyCore()
    history = FakeHistory()
    session = AssistantSession.start(core=core, history=history, mode="chat")

    result = session.handle_user_input("/exit")

    assert result == session.EXIT_TOKEN


def test_session_history_command_shows_previous_messages():
    core = DummyCore()
    history = FakeHistory()
    session = AssistantSession.start(core=core, history=history, mode="chat")

    # ustvarimo eno sporočilo, da bo nekaj v zgodovini
    session.handle_user_input("Hello history")
    out = session.handle_user_input("/history")

    assert "hello history" in out.lower()
    assert "user" in out.lower()