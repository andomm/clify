import click
from oauth2_cli_auth import OAuth2ClientInfo, get_access_token_with_browser_open

from spotcli.common.config import config
from spotcli.common.logger import log


@click.group("spotify")
def group() -> None:
    pass


def get_current_song():
    print("Getting current song")


@group.command("authenticate")
def authenticate():
    client_info = OAuth2ClientInfo(
        "https://accounts.spotify.com/authorize",
        "https://accounts.spotify.com/api/token",
        config.spotify_client_id,
        [
            "user-read-private",
            "user-read-email",
            "user-read-playback-state",
            "user-modify-playback-state",
        ],
    )
    try:
        token = get_access_token_with_browser_open(client_info, 3000)
        log.info(f"Token obtained: {token}")
    except ValueError:
        log.error(f"Failed to obtain token")
