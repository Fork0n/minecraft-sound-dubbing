# python
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Static
from textual.containers import Vertical, Center
from textual.screen import Screen

import audioScreen


class MainScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("название ресурспака (рекомендуем латинскими буквами и без пробелов):"),
            Input(placeholder="resourcepack name", id="name"),
            Static("Путь до места где хотите сохранить:"),
            Input(placeholder="directory", id="directory"),
            Center(Button("Приступить к созданию", id="create")),
            Static("", id="result"),
            id="layout",
        )
        # yield Input(id="test")

    def on_mount(self) -> None:
        # Ensure the first input has focus so typing is visible
        self.query_one("#name", Input).focus()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create":
            name = self.query_one("#name", Input).value.strip()
            directory = self.query_one("#directory", Input).value.strip()
            if not name or not directory:
                self.query_one("#result", Static).update("Please enter both fields.")
                return
            target = Path(directory) / name / "assets" / "minecraft" / "sounds"
            try:
                target.mkdir(parents=True, exist_ok=True)
                self.query_one("#result", Static).update(f"Created: {target}")
                self.app.push_screen("audio")
            except Exception as e:
                self.query_one("#result", Static).update(f"Error: {e}")

class mainApp(App):
    # CSS_PATH = "main.tcss"
    SCREENS = {
        "main": MainScreen,
        "audio": audioScreen.Audio,
    }
    BINDINGS = [("q", "quit", "Quit")]

    def on_mount(self) -> None:
        self.push_screen("main")

if __name__ == "__main__":
    app = mainApp()
    app.run()
