import os
import requests


class SlackClient:
    def __init__(self):
        self.__root = "https://slack.com/api"
        self.__auth_token = os.getenv("AUTH_TOKEN")

    # opens a new conversation
    def open_conv(self, user_id: str):
        url = f"{self.__root}/conversations.open"
        payload = {"token": self.__auth_token, "users": [user_id]}

        res = requests.post(url, data=payload)
        return res.json()["channel"]["id"]

    def post_message(self, channel_id: str, message: str):
        url = f"{self.__root}/chat.postMessage"
        payload = {
            "token": self.__auth_token,
            "channel": channel_id,
            "text": message,
        }

        requests.post(url, data=payload)
