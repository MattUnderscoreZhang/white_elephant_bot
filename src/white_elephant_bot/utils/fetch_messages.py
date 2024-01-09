import os
import requests
from time import sleep


def fetch_recent_messages(
    channel_id: str,
    n_messages: int,
    max_messages: int = 400,
) -> list[dict]:
    messages = []
    last_message_id = None
    while True:
        if len(messages) >= max_messages:
            return messages
        n_messages_in_current_batch = min(100, n_messages + 1 - len(messages))  # add one to account for the bot's own message
        if n_messages_in_current_batch <= 0:
            return messages
        sleep(0.1)  # rate limit
        response = requests.get(
            url=(
                f"https://discord.com/api/v9/channels/{channel_id}/messages" +
                (
                    f"?before={last_message_id}&limit={n_messages_in_current_batch}"
                    if last_message_id
                    else f"?limit={n_messages_in_current_batch}"
                )
            ),
            headers={
                "Authorization": f"Bot {os.getenv('BOT_TOKEN')}",
                "User-Agent": "WhiteElephantBot",
            },
        )
        if response.status_code != 200:
            print(f"Error fetching messages: {response.status_code} - {response.json()}")
            return messages
        messages += [
            message
            for message in response.json()
        ]
        last_message_id = messages[-1]['id']


def fetch_messages_since_last_user_message(
    channel_id: str,
    user_id: str,
    max_messages: int = 400,
) -> list[dict]:
    messages = []
    last_message_id = None
    while True:
        if len(messages) >= max_messages:
            return messages
        n_messages_in_current_batch = 100
        sleep(0.1)  # rate limit
        response = requests.get(
            url=(
                f"https://discord.com/api/v9/channels/{channel_id}/messages" +
                (
                    f"?before={last_message_id}&limit={n_messages_in_current_batch}"
                    if last_message_id
                    else f"?limit={n_messages_in_current_batch}"
                )
            ),
            headers={
                "Authorization": f"Bot {os.getenv('BOT_TOKEN')}",
                "User-Agent": "WhiteElephantBot",
            },
        )
        if response.status_code != 200:
            print(f"Error fetching messages: {response.status_code} - {response.json()}")
            return messages
        for message in response.json():
            if message['author']['id'] == user_id:
                return messages
            messages.append(message)
        last_message_id = messages[-1]['id']
