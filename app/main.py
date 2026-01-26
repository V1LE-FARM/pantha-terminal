from __future__ import annotations

import os
import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Input, Static, RichLog
from textual.reactive import reactive


def resource_path(relative: str) -> str:
    """
    Works in dev + PyInstaller.
    Lets us find styles.tcss even when packed into an exe/app.
    """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative)


class PanthaBanner(Static):
    """Top ASCII banner."""

    def on_mount(self) -> None:
        self.update(
            r"""
██████╗  █████╗ ███╗   ██╗████████╗██╗  ██╗ █████╗
██╔══██╗██╔══██╗████╗  ██║╚══██╔══╝██║  ██║██╔══██╗
██████╔╝███████║██╔██╗ ██║   ██║   ███████║███████║
██╔═══╝ ██╔══██║██║╚██╗██║   ██║   ██╔══██║██╔══██║
██║     ██║  ██║██║ ╚████║   ██║   ██║  ██║██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝

        ░▒▓█▓▒░  P A N T H A   T E R M I N A L  ░▒▓█▓▒░
        """
        )


class PanthaTerminal(App):
    """
    Main Textual App
    """

    TITLE = "Pantha Terminal"
    SUB_TITLE = "Purple ASCII Terminal"

    # We will load CSS manually to ensure it works in PyInstaller
    CSS_PATH = None

    # reactive status line
    status_text: reactive[str] = reactive("Ready")

    def __init__(self) -> None:
        super().__init__()
        self.command_history: list[str] = []
        self.history_index: int = -1

    def load_tcss(self) -> None:
        """
        Loads app/styles.tcss safely for both dev + packaged builds.
        """
        # In dev repo: app/styles.tcss exists
        dev_path = Path(__file__).parent / "styles.tcss"

        if dev_path.exists():
            self.stylesheet.read(dev_path)
            return

        # In PyInstaller: we bundled it into app/styles.tcss
        packed_path = Path(resource_path("app/styles.tcss"))
        if packed_path.exists():
            self.stylesheet.read(packed_path)
            return

        # If missing, do not crash — just continue
        self.log("⚠ styles.tcss not found (continuing without custom theme).")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="root"):
            yield PanthaBanner(id="banner")

            with Horizontal(id="main_row"):
                with Vertical(id="left_panel"):
                    yield Static("SYSTEM", id="panel_title")
                    yield Static("• Pantha Terminal\n• Textual UI\n• Purple Glow\n• ASCII Mode", id="system_info")

                    yield Static("HOTKEYS", id="panel_title2")
                    yield Static(
                        "ENTER  → run command\n"
                        "UP/DOWN → history\n"
                        "CTRL+C → quit\n"
                        "CTRL+L → clear log",
                        id="hotkeys",
                    )

                with Vertical(id="right_panel"):
                    yield Static("OUTPUT", id="output_title")

                    with ScrollableContainer(id="log_wrap"):
                        yield RichLog(id="log", highlight=True, markup=True, wrap=True)

                    yield Static("", id="status_line")

                    yield Input(placeholder="Type a command... (try: help)", id="command_input")

        yield Footer()

    def on_mount(self) -> None:
        self.load_tcss()

        log = self.query_one("#log", RichLog)
        log.write("[bold #ff4dff]Pantha Terminal Online.[/]")
        log.write("[#b066ff]Type [bold]help[/] for commands.[/]")
        self.update_status("Ready")

        # Focus input immediately
        self.query_one("#command_input", Input).focus()

    def update_status(self, text: str) -> None:
        self.status_text = text
        self.query_one("#status_line", Static).update(f"STATUS: {text}")

    def run_command(self, cmd: str) -> None:
        log = self.query_one("#log", RichLog)

        cmd = cmd.strip()
        if not cmd:
            return

        self.command_history.append(cmd)
        self.history_index = len(self.command_history)

        log.write(f"[bold #ff4dff]»[/] [#ffffff]{cmd}[/]")

        # Built-in commands
        if cmd.lower() in ("help", "?"):
            log.write("[#b066ff]Commands:[/]")
            log.write("  [#ff4dff]help[/]      - show this menu")
            log.write("  [#ff4dff]clear[/]     - clear output")
            log.write("  [#ff4dff]about[/]     - about Pantha Terminal")
            log.write("  [#ff4dff]ascii[/]     - show the pantha banner")
            log.write("  [#ff4dff]exit[/]      - quit")
            self.update_status("Help displayed")
            return

        if cmd.lower() == "clear":
            log.clear()
            log.write("[#b066ff]Output cleared.[/]")
            self.update_status("Cleared")
            return

        if cmd.lower() == "about":
            log.write("[bold #ff4dff]Pantha Terminal[/]")
            log.write("[#b066ff]A purple ASCII terminal UI built with Textual.[/]")
            log.write("[#b066ff]GitHub: [underline]https://github.com/V1LE-FARM/pantha-terminal[/][/]")
            self.update_status("About shown")
            return

        if cmd.lower() == "ascii":
            log.write("[#ff4dff]" + r"""
        /\_/\ 
   ____/ o o \
  /~____  =ø= /
 (______)__m_m)
            """ + "[/]")
            log.write("[#b066ff]Pantha mode: ENABLED[/]")
            self.update_status("ASCII shown")
            return

        if cmd.lower() in ("exit", "quit"):
            self.update_status("Exiting...")
            self.exit()
            return

        # Default: unknown command
        log.write("[bold red]Unknown command.[/]")
        log.write("[#b066ff]Try: help[/]")
        self.update_status("Unknown command")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        cmd = event.value
        event.input.value = ""
        self.run_command(cmd)

    def on_key(self, event) -> None:
        """
        UP/DOWN history + CTRL+L clear
        """
        inp = self.query_one("#command_input", Input)

        # CTRL+L to clear log
        if event.key == "ctrl+l":
            log = self.query_one("#log", RichLog)
            log.clear()
            log.write("[#b066ff]Output cleared.[/]")
            self.update_status("Cleared")
            event.stop()
            return

        # History navigation
        if event.key == "up":
            if not self.command_history:
                return
            self.history_index = max(0, self.history_index - 1)
            inp.value = self.command_history[self.history_index]
            inp.cursor_position = len(inp.value)
            event.stop()
            return

        if event.key == "down":
            if not self.command_history:
                return
            self.history_index = min(len(self.command_history), self.history_index + 1)
            if self.history_index >= len(self.command_history):
                inp.value = ""
            else:
                inp.value = self.command_history[self.history_index]
                inp.cursor_position = len(inp.value)
            event.stop()
            return


if __name__ == "__main__":
    PanthaTerminal().run()
