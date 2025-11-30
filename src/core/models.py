from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict

class Role(str, Enum):
  """Role of a message in a conversation."""
  USER = "user"
  ASSISTANT = "assistant"
  SYSTEM = "system"
  AI = "ai"

@dataclass
class Message:
  """A single message in the conversation."""
  role: Role
  content: str

@dataclass
class Conversation:
  """Represents a full conversation with the AI Assistant.
  'mode' can be used to switch behavior:
  e.g. "chat", "coder", "translatior", "explainer",...
  """
  mode: str
  messages: List[Message] = field(default_factory=list)

  def add_user_message(self, content: str) -> None:
    self.messages.append(Message(role=Role.USER, content=content))

  def add_assistant_message(self, content: str) -> None:
    self.messages.append(Message(role=Role.ASSISTANT, content=content))

  def add_system_message(self, content: str) -> None:
    self.messages.append(Message(role=Role.SYSTEM, content=content))

  def add_message(self, message: Message) -> None:
    """Apend a pre-built Message object."""
    self.messages.append(message)

  def last_user_message(self) -> str:
    for msg in reversed(self.messages):
      if msg.role == Role.USER:
        return msg.content
    return ""

  def to_ai_payload(self) -> List[Dict[str, str]]:
    """Convert messages into a list of dicts compatible with common AI APIs.

    Example output:
    [
      {"role": "system", "content", "..."},
      {"role": "user", "content": "..."}
    ]
    """
    return[
      {"role": msg.role.value, "content": msg.content}
      for msg in self.messages
    ]