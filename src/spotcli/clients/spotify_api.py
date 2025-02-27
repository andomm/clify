import base64

import requests


class SpotifyClient:

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_url = "https://accounts.spotify.com/api/token"
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.access_token = None
        self.refresh_token = None

    def get_authorization_url(self, scope):
        auth_url = f"{self.auth_url}?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&scope={scope}"
        return auth_url

    def get_tokens(self, authorization_code):
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
        self.access_token = response_data.get("access_token")
        self.refresh_token = response_data.get("refresh_token")
        return response_data

    def refresh_access_token(self):
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
        return response_data
