import webbrowser

import click
import dotenv
from textual.app import App
from textual.widgets import Button

import spotcli.cli.spotify


class SpotcliApp(App):
    def on_mount(self) -> None:
        self.title = "Spotcli"
        self.screen.styles.background = "#1ED760"
        self.screen.styles.border = ("heavy", "white")
        self.screen.styles.align_horizontal = "center"
        self.screen.styles.align_vertical = "middle"

    def compose(self):
        yield Button(
            "Authenticate",
            "default",
        )


@click.group(
    commands=[
        spotcli.cli.spotify.group,
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
    app = SpotcliApp()
    app.run()


if __name__ == "__main__":
    group()
