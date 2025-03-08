import click

from clify.clients.auth import OAuthCallbackHttpServer
from clify.clients.spotify_api import SpotifyClient
from clify.common.config import config
from clify.models import client_info
from clify.models.client_info import OAuth2ClientInfo


def authenticate() -> str:
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
            access_token, refresh_token = client.get_tokens(code)
            with open("access_token.txt", "w") as f:
                f.write(access_token)
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

    except ValueError:
        click.echo(f"Failed to obtain token")

    return ""
