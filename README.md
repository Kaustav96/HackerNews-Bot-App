# HackerNews-Bot-App

## Features
- Sit back & relax - you will get news having points more than 100 to your slack channel.
- Get Slack Notification
- Its ROBUST! 
  - What if script fails?
  - You get Slack notifications about the exceptions too.
  - You have log files (check `bot.log`) too, to evaluate what went wrong

## Installation
- You need Python.
- You need a Slack account + Slack Webhook to send slack notifications to your account.
- Install dependencies by running
```bash

pip install requests
pip install beautifulsoup4
```
- Clone this repo and create auth.py
```bash
git clone https://github.com/Kaustav96/Joke-Bot-App.git
cd Joke-Bot-App
touch auth.py
```
- Write your Slack Webhook into auth.py
```python
DEFAULT_SLACK_WEBHOOK = 'https://hooks.slack.com/services/<your custome webhook url>'
```
