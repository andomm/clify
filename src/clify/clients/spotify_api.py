import base64
from dataclasses import dataclass

import requests


@dataclass()
class SpotifyClient:

    client_id: str
    client_secret: str
    redirect_uri: str
    token_url: str = "https://accounts.spotify.com/api/token"
    auth_url: str = "https://accounts.spotify.com/authorize"
    access_token: str = ""
    refresh_token: str = ""

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        pass

    def get_tokens(self, authorization_code) -> tuple[str, str]:
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
        }
        response = requests.post(self.token_url, headers=headers, data=data)
        response_data = response.json()
        self.access_token = response_data.get("access_token", "")
        self.refresh_token = response_data.get("refresh_token", "")
        return self.access_token, self.refresh_token

    def refresh_access_token(self) -> None:
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}
        response = requests.post(self.token_url, headers=headers, data=data)
        response_data = response.json()
        self.access_token = response_data.get("access_token")

    @staticmethod
    def get_current_song(access_token: str) -> dict:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            "https://api.spotify.com/v1/me/player/currently-playing", headers=headers
        )
        return response.json()["item"]["name"]
