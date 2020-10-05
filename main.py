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

    # slack sometimes sends same event multiple times
    # if response isn't fast enough
    # TODO: make everything async
    if req.headers.get("X-Slack-Retry-Reason") == "http_timeout" and req.headers.get("X-Slack-Retry-Num"):
        return "ok"

    raw_body = await req.body()

    if not utils.is_authorized(timestamp, signature, raw_body):
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await req.json()
    event = body.get("event")

    # ignore other events
    if event.get("type") != "team_join":
        return "ok"

    user_id = event.get("user").get("id")

    # open a conv
    channel_id = slack_client.open_conv(user_id)

    # send post message
    slack_client.post_message(channel_id, utils.welcome_message(user_id))
    return "ok"
