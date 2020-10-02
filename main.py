import json
from fastapi import FastAPI, Request, HTTPException

import utils
from client import SlackClient

app = FastAPI()
slack_client = SlackClient()

@app.post("/")
async def events_handler(req: Request):
    timestamp = req.headers.get("X-Slack-Request-Timestamp")
    signature = req.headers.get("X-Slack-Signature")
    raw_body = await req.body()

    if not utils.is_authorized(timestamp, signature, raw_body):
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await req.json() 
    event = body.get("event")

    # ignore other events
    if event.get("type") != "member_joined_channel":
        return "ok"

    # ignore if channel is not channel we want to notify on
    if event.get("channel") != slack_client.channel:
        return "ok"

    user = event.get("user")

    # open a conv
    channel_id = slack_client.open_conv(user)

    # send post message
    msg = f'Hello <@{user}>!, welcome to our workspace!'
    slack_client.post_message(channel_id, msg)
    return "ok"

@app.get("/")
def index():
    return "ok"