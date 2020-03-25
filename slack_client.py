import requests
import json
from Auth import DEFAULT_SLACK_WEBHOOK
HEADERS = {
    'Content-type': 'application/json'
}

file_path = 'final_news_list.txt'

def slacker(webhook_url=DEFAULT_SLACK_WEBHOOK):
    def slackit(msg):
        payload = {'text': msg, 'attachments': msg}

        return requests.post(webhook_url, headers=HEADERS, data=json.dumps(payload))
    return slackit


def slacker_file():
    def slackerfile():
        with open(file_path, 'rb') as f:
            payload = {"filename": file_path,
                       "token": YOUR_SLACK_TOKEN,
                       "channels": "news"}
            requests.post("https://slack.com/api/files.upload", params=payload, files={'file': f})

    return slackerfile()