import os
import requests

class SlackClient:
    def __init__(self):
        self.__root = "https://slack.com/api"
        self.__auth_token = os.getenv("AUTH_TOKEN")

        # load channel id on init 
        channel_name = os.getenv("CHANNEL_NAME") 
        channel = self.__get_channel_id(channel_name) 
        if not channel:
            raise Exception(f"No channel {channel_name} found")
        self.__channel = channel

    # return channel id from channel name
    def __get_channel_id(self, channel_name: str):
        params = {"token": self.__auth_token}
        url = f"{self.__root}/conversations.list"

        resp = requests.get(url, params=params)
        body = resp.json() 

        for channel in body.get("channels"):
            if channel.get("name") == channel_name:
                return channel.get("id")
    
    @property
    def channel(self):
        return self.__channel
    
    # opens a new conversation
    def open_conv(self, user_id: str):
        url = f"{self.__root}/conversations.open"
        payload = {
            "token": self.__auth_token,
            "users": [user_id]
        }

        res = requests.post(url, data=payload)
        return res.json()["channel"]["id"]

    def post_message(self, channel_id:str, message: str):
        url = f"{self.__root}/chat.postMessage"
        payload = {
            "token": self.__auth_token,
            "channel": channel_id,
            "text": message,
        }

        requests.post(url, data=payload)