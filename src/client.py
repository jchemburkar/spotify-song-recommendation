""" client for making requests to the spotify api """
import requests
import logging
from base64 import b64encode
from datetime import datetime, timedelta
from time import sleep

# TODO: put your CLIENT_ID:SECRET in this string!
CLIENT_ID_AND_SECRET = ""
AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1"


class Client:
    def __init__(self):
        self.access_token = None
        self.token_expiration_timestamp = None
        self.base_url = BASE_URL

    def get_access_token(self):
        """ gets a new auth token if current one is stale / doesn't exist """

        # set up headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {b64encode(CLIENT_ID_AND_SECRET.encode('utf8')).decode('utf8')}"
        }
        params = {"grant_type": "client_credentials"}

        # make request and handle the response
        response = requests.post(AUTH_URL, headers=headers, params=params)
        if response.status_code == 200:
            response_data = response.json()
            self.access_token = response_data["access_token"]
            self.token_expiration_timestamp = datetime.utcnow() + timedelta(seconds=response_data["expires_in"])

        else:
            logging.error("Could not get access token: %s", response.text)

    def make_spotify_request(self, endpoint, request_type="get"):
        """ makes request to spotify api, managing access token as needed """

        # refresh the access token if needed
        if not self.access_token or datetime.utcnow() >= self.token_expiration_timestamp:
            self.get_access_token()

        url = f"{self.base_url}{endpoint}"
        if request_type == "get":
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            response = requests.get(url, headers=headers)

            # log any errors
            if response.status_code in (401, 404, 502):
                logging.warning("First attempt to retrieve %s is %s, retrying...", endpoint, str(response.status_code))
                sleep(5)
                response = requests.get(url, headers=headers)

            # handle data if success:
            if response.status_code == 200:
                return response.json()
