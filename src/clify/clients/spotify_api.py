import base64
from dataclasses import dataclass
from typing import Optional

import requests
from dacite import from_dict

from clify.clients import auth


@dataclass()
class Song:
    name: str


@dataclass()
class Track:
    name: str
    id: str


@dataclass()
class Playlist:
    name: str
    id: str
    description: Optional[str]


@dataclass()
class SpotifyClient:

    client_id: str
    client_secret: str
    redirect_uri: str
    token_url: str = "https://accounts.spotify.com/api/token"
    auth_url: str = "https://accounts.spotify.com/authorize"

    def __enter__(self):
        self.access_token = auth.get_token_from_file("access_token.txt")
        self.refresh_token = auth.get_token_from_file("refresh_token.txt")
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
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

    def get_current_song(self) -> Song | None:
        response = requests.get(
            "https://api.spotify.com/v1/me/player/currently-playing",
            headers=self.headers,
        )
        if response.status_code == 401:
            self.refresh_access_token()
            self.headers = {"Authorization": f"Bearer {self.access_token}"}
        if response.status_code != 200:
            return None

        return from_dict(Song, response.json())

    def get_user_playlists(self):
        response = requests.get(
            "https://api.spotify.com/v1/me/playlists",
            headers=self.headers,
        )
        if response.status_code == 401:
            self.refresh_access_token()
            self.headers = {"Authorization": f"Bearer {self.access_token}"}
        if response.status_code != 200:
            return None

        return [from_dict(Playlist, item) for item in response.json().get("items", [])]

    def get_playlist_items(self, playlist_id: str):
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
            headers=self.headers,
        )
        if response.status_code == 401:
            self.refresh_access_token()
            self.headers = {"Authorization": f"Bearer {self.access_token}"}
        if response.status_code != 200:
            return None

        return [
            from_dict(Track, item.get("track"))
            for item in response.json().get("items", [])
        ]
