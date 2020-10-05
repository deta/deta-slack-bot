import os
import hmac
import json
from datetime import datetime


WEBHOOK_SECRET = os.getenv("SECRET_TOKEN")
GITHUB_LINK = os.getenv("GITHUB_LINK")


def calc_signature(version: str, timestamp: str, body: str):
    base_string = f"{version}:{timestamp}:{body}"

    digest = hmac.new(
        key=WEBHOOK_SECRET.encode("utf-8"),
        msg=base_string.encode("utf-8"),
        digestmod="sha256",
    ).hexdigest()

    return f"{version}={digest}"


# checks if incoming http request is authorized
def is_authorized(timestamp: str, signature: str, body: bytes):
    # prevent replay atttacks
    if (datetime.now().timestamp() - int(timestamp)) > 60:
        return False

    # verify the signature
    expected_signature = calc_signature("v0", timestamp, body.decode())
    return hmac.compare_digest(signature, expected_signature)


def welcome_message(user_id):
    return """Hello <@%s>, welcome to Deta's Slack.

Our docs and quickstart guides: https://docs.deta.sh

Our channels:

#bugs: report any bugs to us
#feature_requests: if you want to request a feature get shipped
#show: show off your Deta projects
#programming_help: if you need help on anything

You can message @mustafa, @Max or @Aavash anytime you want for any feedback or questions.

I run on Deta myself, you can check out my source code here: %s
""" % (
        user_id,
        GITHUB_LINK,
    )
