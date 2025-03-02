import click

from spotcli.clients.http_server import OAuthCallbackHttpServer
from spotcli.clients.spotify_api import SpotifyClient
from spotcli.common.config import config
from spotcli.common.logger import log
from spotcli.models import client_info
from spotcli.models.client_info import OAuth2ClientInfo


@click.group("spotify")
def group() -> None:
    pass


def get_current_song():
    print("Getting current song")


@group.command("authenticate")
def authenticate():
    oauth_client_info = OAuth2ClientInfo(
        config.spotify_authorization_url,
        config.spotify_token_url,
        config.spotify_client_id,
        config.spotify_client_secret,
        [
            "user-read-private",
            "user-read-email",
            "user-read-playback-state",
            "user-modify-playback-state",
        ],
    )
    click.echo("Opening browser for authentication")
    try:
        callback_server = OAuthCallbackHttpServer(3000)

        auth_url = client_info.get_auth_url(
            oauth_client_info, callback_server.callback_url
        )
        client_info.open_browser(auth_url)
        code = callback_server.wait_for_code()

        with SpotifyClient(
            config.spotify_client_id,
            config.spotify_client_secret,
            config.spotify_redirect_uri,
        ) as client:
            access_token, _ = client.get_tokens(code)
            click.echo(f"Access token: {access_token}")
    except ValueError:
        log.error(f"Failed to obtain token")
