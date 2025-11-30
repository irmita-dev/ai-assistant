"""
Visual chat UI for the AI Assistant.

- Cute robot on the left
- Chat history on the right
- Input box at the bottom

Only standard library: tkinter.
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk

from src.ai.provider import FakeAIProvider, AICore
from src.core.app import AssistantSession
from src.storage.history import FileHistoryStorage

HISTORY_FILE = "history.jsonl"

# --- Simple design tokens -----------------------------------------------------

BG_DARK = "#111827" # dark slate background
BG_PANEL = "#1f2937" # panel background
BG_INPUT = "#020617"
FG_TEXT = "#e5e7eb" # light gray text
FG_MUTED = "#9ca3af"
ACCENT = "#f97316" # orange
ACCENT_SOFT = "#fed7aa"
FONT_BASE = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 9)


class ChatApp(tk.Tk):
    """Main window for the assistant GUI."""

    def __init__(self) -> None:
        super().__init__()
        self.title("AI Assistant · Chat")
        self.geometry("980x620")
        self.minsize(820, 520)
        self.configure(bg=BG_DARK)

        # Core domain pieces
        core = AICore(FakeAIProvider())
        history = FileHistoryStorage(HISTORY_FILE)
        self.session = AssistantSession.start(
            core=core,
            history=history,
            mode="chat",
        )

        self._build_layout()
        self._load_initial_history()

    # ------------------------------------------------------------------ UI setup
    def _build_layout(self) -> None:
        # Overall 2-column layout
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Left: robot panel
        self._build_robot_panel()

        # Right: chat panel
        self._build_chat_panel()

        # Bottom: input area
        self._build_input_panel()

    def _build_robot_panel(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.configure(style="Side.TFrame")

        # Title
        title = ttk.Label(
            frame,
            text="IRMA's\nAI Assistant",
            justify="left",
            style="Title.TLabel",
        )
        title.pack(anchor="nw")

        # Robot canvas
        canvas = tk.Canvas(
            frame,
            width=220,
            height=260,
            bg=BG_PANEL,
            highlightthickness=0,
        )
        canvas.pack(pady=16)

        # Simple “robot”
        # Head
        canvas.create_rounded_rect = rounded_rect # small helper for clarity
        rounded_rect(canvas, 40, 40, 180, 170, radius=20, fill="#020617", outline=ACCENT, width=3)

        # Eyes
        canvas.create_oval(70, 70, 95, 95, fill=ACCENT_SOFT, outline="")
        canvas.create_oval(125, 70, 150, 95, fill=ACCENT_SOFT, outline="")

        # Mouth
        canvas.create_line(80, 130, 140, 130, fill=ACCENT_SOFT, width=3, capstyle=tk.ROUND)

        # Antenna
        canvas.create_line(110, 30, 110, 40, fill=ACCENT, width=3)
        canvas.create_oval(104, 20, 116, 32, fill=ACCENT, outline="")

        # Small label under robot
        ttk.Label(
            frame,
            text="Friendly dev helper bot.\nAlways in dev mode 👩‍💻",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(8, 0))

        # “Bubble” with last reply
        self.bubble_var = tk.StringVar(
            value="Tip: Ask me about your next Python task."
        )
        bubble = ttk.Label(
            frame,
            textvariable=self.bubble_var,
            wraplength=220,
            style="Bubble.TLabel",
        )
        bubble.pack(anchor="w", pady=(16, 0))

    def _build_chat_panel(self) -> None:
        frame = ttk.Frame(self, padding=(8, 16))
        frame.grid(row=0, column=1, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Header
        header = ttk.Label(
            frame,
            text="Chat",
            style="Title.TLabel",
        )
        header.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Text area with scrollbar
        container = ttk.Frame(frame)
        container.grid(row=1, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self.text = tk.Text(
            container,
            bg=BG_PANEL,
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
            wrap="word",
            font=FONT_BASE,
            padx=10,
            pady=10,
        )
        scrollbar = ttk.Scrollbar(container, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)

        self.text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Make text read-only by default
        self.text.config(state="disabled")

    def _build_input_panel(self) -> None:
        frame = ttk.Frame(self, padding=(16, 12))
        frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        entry = ttk.Entry(
            frame,
            textvariable=self.entry_var,
            width=10,
        )
        entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        entry.bind("<Return>", self._on_send)

        send_btn = ttk.Button(
            frame,
            text="Send ▶",
            command=self._on_send,
        )
        send_btn.grid(row=0, column=1)

        hint = ttk.Label(
            frame,
            text="Type your message · /history to see previous chats · /exit to close",
            style="Muted.TLabel",
        )
        hint.grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # Focus on entry when window opens
        self.after(200, entry.focus_set)

    # ----------------------------------------------------------------- behavior
    def _append_line(self, prefix: str, content: str) -> None:
        """Append a new line into the chat text widget."""
        self.text.config(state="normal")
        self.text.insert("end", f"{prefix} {content}\n")
        self.text.see("end")
        self.text.config(state="disabled")

    def _load_initial_history(self) -> None:
        """Load a bit of history into the chat area on startup."""
        self._append_line("AI:", "Hi, I'm your local dev assistant. What are we coding today?")

    def _on_send(self, event: tk.Event | None = None) -> None:
        user_input = self.entry_var.get().strip()
        if not user_input:
            return

        self.entry_var.set("")
        self._append_line("You:", user_input)

        reply = self.session.handle_user_input(user_input)

        if reply == self.session.EXIT_TOKEN:
            self._append_line("AI:", "Goodbye 👋")
            self.after(300, self.destroy)
            return

        self._append_line("AI:", reply)
        # Update little bubble above the robot with a short preview
        self.bubble_var.set(reply[:80] + ("…" if len(reply) > 80 else ""))


# --- Small drawing helper -----------------------------------------------------


def rounded_rect(canvas: tk.Canvas, x1, y1, x2, y2, radius=10, **kwargs):
    """Draw a rounded rectangle on the canvas."""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# --- ttk style setup ----------------------------------------------------------


def setup_styles(root: tk.Tk) -> None:
    style = ttk.Style(root)
    # Use default theme but override colors
    style.theme_use("clam")

    style.configure(
        "Side.TFrame",
        background=BG_DARK,
    )
    style.configure(
        "Title.TLabel",
        background=BG_DARK,
        foreground=FG_TEXT,
        font=("Segoe UI Semibold", 14),
    )
    style.configure(
        "Muted.TLabel",
        background=BG_DARK,
        foreground=FG_MUTED,
        font=FONT_BASE,
    )
    style.configure(
        "Bubble.TLabel",
        background=BG_PANEL,
        foreground=FG_TEXT,
        padding=8,
        wraplength=220,
        font=FONT_BASE,
    )
    style.configure(
        "TFrame",
        background=BG_DARK,
    )
    style.configure(
        "TLabel",
        background=BG_DARK,
        foreground=FG_TEXT,
        font=FONT_BASE,
    )
    style.configure(
        "TEntry",
        fieldbackground=BG_INPUT,
        background=BG_INPUT,
        foreground=FG_TEXT,
        insertcolor=FG_TEXT,
    )
    style.configure(
        "TButton",
        background=ACCENT,
        foreground="#111827",
        padding=(10, 4),
    )


# --- entrypoint ---------------------------------------------------------------


def main() -> None:
    app = ChatApp()
    setup_styles(app)
    app.mainloop()


if __name__ == "__main__":
    main()