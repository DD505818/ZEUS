import os
import requests

WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

def send_alert(message: str) -> None:
    if not WEBHOOK_URL:
        return
    requests.post(WEBHOOK_URL, json={'text': message}, timeout=5)
