import os
import requests

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(message: str):
    if not WEBHOOK_URL:
        return
    requests.post(WEBHOOK_URL, json={"text": message})
