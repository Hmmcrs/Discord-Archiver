import os
from pathlib import Path
import requests
import time
from datetime import datetime
from dateutil import parser
import json

def find_desktop():
    onedrive_path = Path.home() / "OneDrive" / "Desktop"
    if onedrive_path.exists():
        return onedrive_path

    desktop_path = Path.home() / "Desktop"
    if desktop_path.exists():
        return desktop_path

    raise FileNotFoundError("Desktop not found.")

desktop_path = find_desktop()
config_path = desktop_path / 'config.json'

if not config_path.exists():
    raise FileNotFoundError(f"config.json not found at {config_path}")

with open(config_path, 'r') as config_file:
    config = json.load(config_file)
    token = config['token']
    channel_id = config['channel_id']

log_file_path = 'discord_messages.txt'
error_log_path = 'error_log.txt'

last_message_id = None
start_time = None
first_run = True

def fetch_messages():
    global last_message_id, start_time, first_run
    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json'
    }
    url = f'https://discord.com/api/v10/channels/{channel_id}/messages?limit=100'
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            messages = response.json()
            new_messages = []

            for msg in messages:
                if last_message_id is None or int(msg['id']) > last_message_id:
                    msg_time = parser.isoparse(msg['timestamp'])
                    if start_time is None:
                        start_time = msg_time
                    if msg_time >= start_time:
                        new_messages.append(msg)

            if messages:
                last_message_id = max(int(msg['id']) for msg in messages)

            if new_messages:
                new_messages.reverse()

                for index, msg in enumerate(new_messages):
                    username = msg['author']['username']
                    content = msg['content']
                    timestamp = msg['timestamp']
                    try:
                        timestamp_dt = parser.isoparse(timestamp)
                        formatted_time = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        formatted_time = 'Unknown time'
                    
                    if first_run and index == 0:
                        print(f"---\nUser: {username}\nTime: {formatted_time} (newest at script start)\nContent: {content}\n---")
                    else:
                        print(f"---\nUser: {username}\nTime: {formatted_time}\nContent: {content}\n---")

                log_messages(new_messages)
            first_run = False
        return response.status_code

    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching messages: {e}\n"
        print(error_message)
        log_error(str(e))
        time.sleep(5)
        return None

def log_error(message):
    """Log errors to a separate error log file."""
    with open(error_log_path, 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

def log_messages(messages):
    with open(log_file_path, 'a') as f:
        for index, message in enumerate(messages):
            user_id = message['author']['id']
            username = message['author']['username']
            content = message['content']
            timestamp = message['timestamp']

            try:
                timestamp_dt = parser.isoparse(timestamp)
                formatted_time = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                formatted_time = 'Unknown time'

            if all(ord(char) < 128 for char in content):
                if first_run and index == 0:
                    f.write(f"---\nUser: {username} (ID: {user_id})\n")
                    f.write(f"  Time: {formatted_time} (newest at script start)\n")
                    f.write(f"  Content: {content}\n")
                    f.write("---\n\n")
                else:
                    f.write(f"---\nUser: {username} (ID: {user_id})\n")
                    f.write(f"  Time: {formatted_time}\n")
                    f.write(f"  Content: {content}\n")
                    f.write("---\n\n")
            else:
                f.write(f"---\nUser: {username} (ID: {user_id})\n")
                f.write(f"  Time: {formatted_time}\n")
                f.write(f"  Content: Ignored due to unsupported characters\n")
                f.write("---\n\n")

if __name__ == "__main__":
    while True:
        status = fetch_messages()
        if status == 200:
            time.sleep(0.2)  # cooldown. (can be changed)

