import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    @property
    def spotify_client_secret(self) -> str:
        return os.getenv("SPOTIFY_CLIENT_SECRET", "")

    @property
    def spotify_client_id(self) -> str:
        return os.getenv("SPOTIFY_CLIENT_ID", "")

    @property
    def spotify_redirect_uri(self) -> str:
        return os.getenv("SPOTIFY_REDIRECT_URI", "")


config = Config()
