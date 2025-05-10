# Version: 1.0.1

from pathlib import Path
import requests
import time
from datetime import datetime
from dateutil import parser
import json

last_message_id = None
start_time = None
first_run = True

def get_desktop_path():
    return next(
        (Path.home() / p for p in ["OneDrive/Desktop", "Desktop"] if (Path.home() / p).exists()),
        None
    ) or (_ for _ in ()).throw(FileNotFoundError("Desktop not found."))

def load_config():
    config_path = get_desktop_path() / 'config.json'
    if not config_path.exists():
        raise FileNotFoundError(f"config.json not found at {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def log_error(message):
    with open('error_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()}: {message}\n")

def format_timestamp(timestamp):
    try:
        return parser.isoparse(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return 'Unknown time'

def safe_content(text):
    return text.replace('\r', '').replace('\n', '\\n')

def print_and_log(messages):
    global first_run
    if not messages:
        return

    messages.reverse()
    with open('discord_messages.txt', 'a', encoding='utf-8') as f:
        for i, msg in enumerate(messages):
            user = msg['author']
            timestamp = msg['timestamp']
            formatted_time = format_timestamp(timestamp)
            content = safe_content(msg['content'])
            first_tag = " (newest at script start)" if first_run and i == 0 else ""

            log_text = (
                f"---\nUser: {user['username']} (ID: {user['id']})\n"
                f"  Time: {formatted_time}{first_tag}\n"
                f"  Content: {content}\n---\n\n"
            )
            print(log_text.strip())
            f.write(log_text)
    first_run = False

def fetch_messages(token, channel_id):
    global last_message_id, start_time
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    url = f'https://discord.com/api/v10/channels/{channel_id}/messages?limit=100'

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        messages = response.json()

        new_msgs = []
        for msg in messages:
            msg_time = parser.isoparse(msg['timestamp'])
            if start_time is None:
                start_time = msg_time
            if last_message_id is None or int(msg['id']) > last_message_id:
                if msg_time >= start_time:
                    new_msgs.append(msg)

        if messages:
            last_message_id = max(int(m['id']) for m in messages)
        if new_msgs:
            print_and_log(new_msgs)

        return 200

    except requests.exceptions.RequestException as e:
        print(f"Error fetching messages: {e}")
        log_error(str(e))
        time.sleep(5)
        return None

if __name__ == "__main__":
    config = load_config()
    token = config['token']
    channel_id = config['channel_id']

    while True:
        if fetch_messages(token, channel_id) == 200:
            time.sleep(5)
