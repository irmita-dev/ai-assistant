from src.core.models import Role, Message, Conversation

def test_message_holds_role_and_content():
  msg = Message(role=Role.USER, content="Hello AI!")
  assert msg.role == Role.USER
  assert msg.content == "Hello AI!"

def test_conversation_adds_messages_in_order():
  conv = Conversation(mode="chat")

  conv.add_user_message("Hi")
  conv.add_assistant_message("Hello, how can I help you?")

  assert len(conv.messages) == 2
  assert conv.messages[0].role == Role.USER
  assert conv.messages[0].content == "Hi"
  assert conv.messages[1].role == Role.ASSISTANT
  assert "help" in conv.messages[1].content

def test_conversation_as_payload_for_ai():
  conv = Conversation(mode="coder")

  conv.add_system_message("You are a helpful coding assistant.")
  conv.add_user_message("Explain list comprehensions in Python.")

  payload = conv.to_ai_payload()

  assert payload[0]["role"] == "system"
  assert "coding assistant" in payload[0]["content"]
  assert payload[1]["role"] == "user"
  assert "list comprehensions" in payload[1]["content"]