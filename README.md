<!-- Banner -->
<p align="center">
  <img src="https://raw.githubusercontent.com/irmita-dev/ai-assistant/refs/heads/main/ai_assistant_banner_irmita_dev.png" width="65%" alt="Irma's GitHub banner ai assistant">
</p>

<h1 align="center">🤖 AI ASSISTANT</h1>

<p align="center">Built in Python • Clean Architecture • TDD • CLI & GUI Demo</p>


<p align="center">
A modular, fully tested, extensible AI Assistant built with
Python, Clean Architecture, and Test-Driven Development (TDD).
</p>

<p align="center">
It includes:
</p>

<p align="center">🧠 AI Core Engine (role-based messages, conversation tracking)</p>

<p align="center">⚙️ Pluggable AI Providers (FakeAI now, real API ready)</p>

<p align="center">💾 JSONL History Storage</p>

<p align="center">💬 CLI Chat Interface</p>

<p align="center">🎨 GUI Prototype (Tkinter)</p>

<p align="center">🧪 100% green tests</p>

<p align="center">
My portfolio project to showcase software architecture, testing discipline and Python engineering.
</p>

<hr/>

<h2 align="center">📌 Table of Contents</h2>

<p align="center">
Features<br>
<br>
Project Structure<br>
<br>
Getting Started<br>
<br>
Usage<br>
<br>
CLI<br>
<br>
GUI
</p>

<hr/>

<h2 align="center">🚀 Features</h2>

<p align="center">
🧠 AI Core Engine (conversation model, roles, payload builder)<br>
<br>
🔧 Pluggable Provider Interface (FakeAI now → easy switch to real LLM API)<br>
<br>
💬 Conversation Manager with clean state handling<br>
<br>
💾 JSONL history storage<br>
<br>
🧱 Clean Architecture layers<br>
<br>
🧪 Full TDD workflow (tests for every module)<br>
<br>
🖥 CLI + GUI prototype<br>
<br>
🔌 Extensible → add new modes (coder, translator, teacher, chatbot…) 
</p>

<hr/>

<h2 align="center">📁 Project Structure</h2>

<pre><code>ai_assistant/
│
├── src/
│ ├── ai/
│ │ ├── provider.py # FakeAI + interface for real AI providers
│ │
│ ├── core/
│ │ ├── models.py # Role, Message, Conversation
│ │ ├── engine.py # AICore → build replies
│ │ └── app.py # AssistantSession (conversation flow)
│ │
│ ├── storage/
│ │ ├── history.py # FileHistoryStorage (JSONL)
│ │
│ └── __init__.py
│
├── tests/
│ ├── test_models.py
│ ├── test_engine.py
│ ├── test_core.py
│ └── test_history.py
│
├── assets/
│ ├── banner.png # Project banner
│ └── demo.gif (optional)
│
├── main.py # CLI interface
├── gui.py # Simple Tkinter prototype
├── requirements.txt
└── README.md
</code></pre>

<hr/>

<h2 align="center">🧭 Getting Started</h2>

<p align="center">
Requirements
</p>

<p align="center">
Python 3.10+
</p>

<p align="center">
pip
</p>

<h3 align="center">Install</h3>

<pre><code>git clone https://github.com/irmita-dev/ai-assistant.git
cd ai-assistant

python3 -m venv .venv
source .venv/bin/activate # Linux/macOS
.venv\Scripts\activate # Windows

pip install -r requirements.txt
</code></pre>

<hr/>

<h2 align="center">▶️ Usage</h2>

<h3 align="center">🧑‍💻 CLI</h3>

<p align="center">Run:</p>

<pre><code>python3 main.py
</code></pre>

<p align="center">Example:</p>

<p align="center">You: Hello AI<br>
AI: I see you said 'Hello AI'. I'm here to help!</p>

<p align="center">Commands:</p>

<p align="center">/exit — quit</p>

<p align="center">/history — show chat history</p>

<hr/>

<h3 align="center">🪟 GUI</h3>

<p align="center">Run:</p>

<pre><code>python3 gui.py
</code></pre>

<p align="center">Features:</p>

<p align="center">Chat window</p>

<p align="center">Scrollable conversation</p>

<p align="center">Minimal layout (demo-ready)</p>

<hr/>

<h2 align="center">🧪 Testing</h2>

<pre><code>python3 -m pytest -q
</code></pre>

<p align="center">Should show:</p>

<p align="center">100% passed ✔</p>

<hr/>

<h2 align="center">✨ Roadmap</h2>

<p align="center">🌐 Add real AI provider (OpenAI / Anthropic / HuggingFace)</p>

<p align="center">🧠 Add AI modes: coder, teacher, translator</p>

<p align="center">🎨 Modern GUI (customtkinter / PySide / web frontend)</p>

<p align="center">🗂 Multi-conversation support</p>

<p align="center">🔒 Encrypted history</p>

<p align="center">🤖 Voice input (Whisper)</p>

<hr/>

<h2 align="center">📜 License</h2>

<p align="center">MIT License. Free to use.</p>

<hr/>

<h2 align="center">👩‍💻 Author</h2>

<p align="center">
Irmita Dev<br>
Python Developer • TDD • Clean Architecture<br>
Building & learning every day.
</p>

<hr/>

<h2 align="center">📫 Contact</h2>

<p align="center">
GitHub: https://github.com/irmita-dev<br>
Email: ljubijankicirma3@gmail.com
</p>
