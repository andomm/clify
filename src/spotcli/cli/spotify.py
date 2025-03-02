import click

from spotcli.clients.spotify_api import SpotifyClient
from spotcli.common import logic


@click.group("spotify")
def group() -> None:
    pass


@group.command("authenticate")
def authenticate():
    logic.authenticate()


@group.command("current-song")
def current_song():
    token = logic.authenticate()
    current_song = SpotifyClient.get_current_song(token)
    click.echo(current_song)
