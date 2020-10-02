import os
import hmac
import json
from datetime import datetime


WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

def calc_signature(version: str, timestamp: str, body: str):
    base_string = f"{version}:{timestamp}:{body}"

    digest = hmac.new(
        key=WEBHOOK_SECRET.encode("utf-8"),
        msg = base_string.encode("utf-8"),
        digestmod="sha256"
    ).hexdigest()

    return f"{version}={digest}"

# checks if incoming http request is authorized
def is_authorized(timestamp: str, signature: str, body: bytes):
    # prevent replay atttacks
    if (datetime.now().timestamp() - int(timestamp)) > 60 :
        return False

    # verify the signature
    expected_signature = calc_signature("v0", timestamp, body.decode())
    print("cacluclated sign:", expected_signature)
    print("got sign:", signature)
    return hmac.compare_digest(signature, expected_signature)