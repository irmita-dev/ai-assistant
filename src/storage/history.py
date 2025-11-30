import json
from pathlib import Path
from typing import List
from src.core.models import Conversation, Message, Role


class FileHistoryStorage:
    """
    Saves full conversations to a JSONL file (one conversation per line).
    """

    def __init__(self, file_path: str | Path):
        self.path = Path(file_path)

    def save(self, conversation: Conversation) -> None:
        data = {
            "mode": conversation.mode,
            "messages": [
                {"role": msg.role.value, "content": msg.content}
                for msg in conversation.messages
            ],
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")

    def load_all(self) -> List[Conversation]:
        if not self.path.exists():
            return []

        conversations: List[Conversation] = []

        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                raw = json.loads(line)
                conv = Conversation(mode=raw["mode"])
                for m in raw["messages"]:
                    conv.messages.append(
                        Message(
                            role=Role(m["role"]),
                            content=m["content"]
                        )
                    )
                conversations.append(conv)

        return conversations