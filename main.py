"""
Minimal terminal chat UI for the AI Assistant.
"""

from src.ai.provider import FakeAIProvider
from src.core import AICore
from src.core.app import AssistantSession
from src.storage.history import FileHistoryStorage


HISTORY_FILE = "history.jsonl"


def main():
    print("🤖 AI Assistant CLI")
    print("Type your messages. Commands: /exit, /history\n")

    core = AICore(FakeAIProvider())
    history = FileHistoryStorage(HISTORY_FILE)
    session = AssistantSession.start(core=core, history=history, mode="chat")

    while True:
        user = input("You: ").strip()
        reply = session.handle_user_input(user)

        if reply == session.EXIT_TOKEN:
            print("Goodbye 👋")
            break

        print(f"AI: {reply}")


if __name__ == "__main__":
    main()