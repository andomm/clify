import click

from clify.clients.spotify_api import SpotifyClient
from clify.common import logic
from clify.common.config import config


@click.group("spotify")
def group() -> None:
    pass


@group.command("authenticate")
def authenticate():
    logic.authenticate()


@group.command("current-song")
def current_song():
    with SpotifyClient(
        config.spotify_client_id,
        config.spotify_client_secret,
        config.spotify_redirect_uri,
    ) as client:
        if current_song := client.get_current_song():
            click.echo(current_song.name)


@group.command("playlists")
def playlists():
    with SpotifyClient(
        config.spotify_client_id,
        config.spotify_client_secret,
        config.spotify_redirect_uri,
    ) as client:
        playlists = client.get_user_playlists()
        if playlists:
            for playlist in playlists:
                click.echo(f"{playlist.name} - {playlist.id}")
