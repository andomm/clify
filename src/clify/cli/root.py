import click
import dotenv
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, Label

import clify.cli.spotify
from clify.common import logic


class ClifyApp(App):

    current_song = reactive("")

    def on_mount(self) -> None:
        self.title = "clify"
        self.screen.styles.background = "#1ED760"
        self.screen.styles.border = ("heavy", "white")
        self.screen.styles.align_horizontal = "center"
        self.screen.styles.align_vertical = "middle"

    def compose(self) -> ComposeResult:
        self.song_label = Label(f"Currently playing: {self.current_song}")
        yield Horizontal(
            VerticalScroll(
                Button(
                    "Authenticate",
                    "default",
                    name="authenticate",
                ),
                Button(
                    "Current Song",
                    "default",
                    name="current-song",
                ),
                self.song_label,
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.name == "authenticate":
            logic.authenticate()
        elif event.button.name == "current-song":
            self.current_song = logic.get_current_song()
            self.song_label.update(self.current_song)


@click.group(
    commands=[
        clify.cli.spotify.group,
    ],
)
@click.option(
    "--env-file",
    "-e",
    type=click.Path(exists=True),
    help="The environment file to load.",
)
def group(
    env_file: str | None,
) -> None:
    if env_file:
        dotenv.load_dotenv(env_file)


@group.command("run")
def cmd_run() -> None:
    app = ClifyApp()
    app.run()


if __name__ == "__main__":
    group()
