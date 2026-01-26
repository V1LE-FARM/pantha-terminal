from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Input, Static, RichLog
from textual.reactive import reactive


def resource_path(relative: str) -> str:
    """Works in dev + PyInstaller."""
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
    TITLE = "Pantha Terminal"
    SUB_TITLE = "Purple ASCII Terminal"

    CSS_PATH = None
    status_text: reactive[str] = reactive("Ready")

    def __init__(self) -> None:
        super().__init__()
        self.command_history: list[str] = []
        self.history_index: int = -1

        # Prompt config
        self.username = os.environ.get("USERNAME") or os.environ.get("USER") or "pantha"
        self.hostname = os.environ.get("COMPUTERNAME") or os.uname().nodename if hasattr(os, "uname") else "local"

    def load_tcss(self) -> None:
        """Load styles.tcss for dev + packaged builds."""
        dev_path = Path(__file__).parent / "styles.tcss"
        if dev_path.exists():
            self.stylesheet.read(dev_path)
            return

        packed_path = Path(resource_path("app/styles.tcss"))
        if packed_path.exists():
            self.stylesheet.read(packed_path)
            return

        self.log("⚠ styles.tcss not found (continuing without custom theme).")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="root"):
            yield PanthaBanner(id="banner")

            with Horizontal(id="main_row"):
                with Vertical(id="left_panel"):
                    yield Static("SYSTEM", id="panel_title")
                    yield Static(
                        f"• User: {self.username}\n"
                        f"• Host: {self.hostname}\n"
                        "• Pantha Terminal\n"
                        "• Textual UI\n"
                        "• Purple Glow\n"
                        "• ASCII Mode",
                        id="system_info",
                    )

                    yield Static("HOTKEYS", id="panel_title2")
                    yield Static(
                        "ENTER   → run command\n"
                        "UP/DOWN → history\n"
                        "CTRL+C  → quit\n"
                        "CTRL+L  → clear log",
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
        log.write("[#b066ff]Try [bold]ascii[/] to enable pantha mode.[/]")
        self.update_status("Ready")

        self.query_one("#command_input", Input).focus()

    def update_status(self, text: str) -> None:
        self.status_text = text
        self.query_one("#status_line", Static).update(f"[#ff4dff]STATUS:[/] [#ffffff]{text}[/]")

    def prompt(self) -> str:
        return f"[#b066ff]{self.username}[/]@[#ff4dff]{self.hostname}[/]:[#ffffff]~$[/]"

    def write_cmd(self, cmd: str) -> None:
        log = self.query_one("#log", RichLog)
        log.write(f"{self.prompt()} [#ffffff]{cmd}[/]")

    def write_info(self, text: str) -> None:
        self.query_one("#log", RichLog).write(f"[#b066ff]{text}[/]")

    def write_err(self, text: str) -> None:
        self.query_one("#log", RichLog).write(f"[bold red]{text}[/]")

    def show_ascii(self) -> None:
        logo = r"""
[#ff4dff]
                /\_/\ 
           ____/ o o \
         /~____  =ø= /
        (______)__m_m)
[/]

[#b066ff]
     ██████╗  █████╗ ███╗   ██╗████████╗██╗  ██╗ █████╗
     ██╔══██╗██╔══██╗████╗  ██║╚══██╔══╝██║  ██║██╔══██╗
     ██████╔╝███████║██╔██╗ ██║   ██║   ███████║███████║
     ██╔═══╝ ██╔══██║██║╚██╗██║   ██║   ██╔══██║██╔══██║
     ██║     ██║  ██║██║ ╚████║   ██║   ██║  ██║██║  ██║
     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝

            ░▒▓█▓▒░  PANTHA MODE ENABLED  ░▒▓█▓▒░
[/]
"""
        self.query_one("#log", RichLog).write(logo)

    def run_shell_command(self, cmd: str) -> None:
        """Run unknown commands in system shell."""
        log = self.query_one("#log", RichLog)

        try:
            # Windows uses cmd.exe
            if os.name == "nt":
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.stdout.strip():
                for line in result.stdout.splitlines():
                    log.write(f"[#ffffff]{line}[/]")

            if result.stderr.strip():
                for line in result.stderr.splitlines():
                    log.write(f"[bold red]{line}[/]")

            self.update_status("Command executed")

        except Exception as e:
            self.write_err(f"Command failed: {e}")
            self.update_status("Command failed")

    def run_command(self, cmd: str) -> None:
        cmd = cmd.strip()
        if not cmd:
            return

        self.command_history.append(cmd)
        self.history_index = len(self.command_history)

        self.write_cmd(cmd)

        low = cmd.lower()

        if low in ("help", "?"):
            self.write_info("Commands:")
            self.query_one("#log", RichLog).write(
                "[#ffffff]"
                "  help       - show this menu\n"
                "  clear      - clear output\n"
                "  about      - about Pantha Terminal\n"
                "  ascii      - show the pantha banner\n"
                "  exit       - quit\n"
                "  shell on   - enable shell execution\n"
                "  shell off  - disable shell execution\n"
                "[/]"
            )
            self.update_status("Help displayed")
            return

        if low == "clear":
            log = self.query_one("#log", RichLog)
            log.clear()
            self.write_info("Output cleared.")
            self.update_status("Cleared")
            return

        if low == "about":
            self.query_one("#log", RichLog).write(
                "[bold #ff4dff]Pantha Terminal[/]\n"
                "[#b066ff]A purple ASCII terminal UI built with Textual.[/]\n"
                "[#b066ff]GitHub: [underline]https://github.com/V1LE-FARM/pantha-terminal[/][/]"
            )
            self.update_status("About shown")
            return

        if low == "ascii":
            self.show_ascii()
            self.update_status("ASCII shown")
            return

        if low in ("exit", "quit"):
            self.update_status("Exiting...")
            self.exit()
            return

        # default: run shell command (nice for real terminal feel)
        self.run_shell_command(cmd)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        cmd = event.value
        event.input.value = ""
        self.run_command(cmd)

    def on_key(self, event) -> None:
        inp = self.query_one("#command_input", Input)

        if event.key == "ctrl+l":
            log = self.query_one("#log", RichLog)
            log.clear()
            self.write_info("Output cleared.")
            self.update_status("Cleared")
            event.stop()
            return

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
