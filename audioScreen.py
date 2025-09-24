# import json
# import pygame
# from textual.app import App, ComposeResult
# from textual.screen import Screen
# from textual.widgets import Footer, Static, Input, ListView, ListItem, Label
#
#
# class AudioSelector(Screen):
#     BINDINGS = [("q", "quit", "Quit")]
#
#     def compose(self) -> ComposeResult:
#         # Load JSON
#         with open("assets_index.json", "r", encoding="utf-8") as f:
#             data = json.load(f)  # this is a list of dicts
#
#         # Build items — you can show only the "name" or both name + location
#         yield ListView(
#             *[
#                 ListItem(Label(item["name"]))  # just the name
#                 for item in data
#             ]
#         )
#
#         yield Footer()
#
# class AudioScreen(App):
#     # CSS_PATH = "audioScreen.tcss"
#     BINDINGS = [
#         ("q", "quit", "Quit"),
#         ("space", "space", "Play/Pause"),
#         ("p", "play", "Play"),
#         ("s", "save", "Save"),
#         ("r", "record", "Record"),
#         ("c", "check", "Check"),
#     ]
#     SCREENS = {
#         "audio": AudioSelector,
#     }
#
#     def on_mount(self) -> None:
#             self.push_screen("audio")
#
# if __name__ == "__main__":
#     app = AudioScreen()
#     app.run()

import json
import os
import pygame
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, ListView, ListItem, Label


class Audio(Screen):
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        # Load JSON once so we can reuse it later
        with open("assets_index.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def compose(self) -> ComposeResult:
        yield ListView(
            *[ListItem(Label(item["name"])) for item in self.data]
        )
        yield Footer()


class AudioScreen(App):
    # CSS_PATH = "audioScreen.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("space", "space", "Play/Pause"),
        ("p", "play", "Play"),
        ("s", "save", "Save"),
        ("r", "record", "Record"),
        ("c", "check", "Check"),
    ]
    SCREENS = {"audio": Audio}

    def on_mount(self) -> None:
        # init pygame mixer
        pygame.mixer.init()
        self.push_screen("audio")

    def action_space(self) -> None:
        """Play or pause currently selected audio"""
        screen: Audio = self.get_screen("audio")
        list_view: ListView = screen.query_one(ListView)

        if list_view.index is None:
            return  # nothing selected

        selected = screen.data[list_view.index]
        file_path = selected["location"]
        abs_path = os.path.join(os.getcwd(), file_path)

        if pygame.mixer.music.get_busy():
            # If something is playing, pause/unpause instead
            if pygame.mixer.music.get_pos() > -1:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
        else:
            # Load and play fresh file
            pygame.mixer.music.load(abs_path)
            pygame.mixer.music.play()


if __name__ == "__main__":
    app = AudioScreen()
    app.run()
