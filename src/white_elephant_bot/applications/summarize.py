from dotenv import load_dotenv
from gpt_interface import GptInterface
import os
import requests
from time import sleep
from typing import cast

from white_elephant_bot.data_types import ResponseType


def _fetch_recent_messages(
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


def _fetch_messages_since_last_user_message(
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


def _fetch_guild_nicknames(guild_id: str) -> dict[str, str]:
    response = requests.get(
        url=f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000",
        headers={
            "Authorization": f"Bot {os.getenv('BOT_TOKEN')}",
            "User-Agent": "WhiteElephantBot",
        },
    )
    if response.status_code != 200:
        print(f"Error fetching member data: {response.status_code} - {response.json()}")
        return {}
    members = response.json()
    return {
        member['user']['id']: (
            member['nick']
            if member['nick']
            else member['user']['global_name']
        )
        for member in members
    }


def _summarize_recent_messages(messages: list[str]) -> str:
    print(f"Summarizing {messages}")
    if len([m for m in messages if not m.startswith("None:")]) == 0:
        return "There is no new non-bot activity on this channel since your last message."
    interface = GptInterface(
        openai_api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-4",
    )
    interface.set_system_message(
        "These are my missed Discord messages. Summarize the content of the logs in a paragraph, without additional commentary. Assume users labelled 'None' are bots, and ignore what they say unless human users comment on it.",
    )
    try:
        summary = interface.say(("\n").join(messages))
    except Exception as e:
        return f"Error: {e}"
    return summary


async def _acknowledge_request(interaction_id: str, token: str) -> None:
    requests.post(
        url=f"https://discord.com/api/v9/interactions/{interaction_id}/{token}/callback",
        json={
            "type": ResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {
                "content": "Processing your request..."
            }
        },
    )


async def _send_followup_message(token: str, message: str) -> None:
    requests.post(
        url=f"https://discord.com/api/v9/webhooks/{os.getenv('BOT_ID')}/{token}",
        json={
            "content": message
        }
    )


async def summarize(
    guild_id: str,
    channel_id: str,
    n_messages: int,
    interaction_id: str,
    token: str,
):
    if type(n_messages) is not int or n_messages <= 0:
        return {
            "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {
                "content": "n_messages parameter must be an integer greater than 0."
            }
        }
    load_dotenv()
    await _acknowledge_request(interaction_id, token)
    recent_messages = _fetch_recent_messages(
        channel_id=channel_id,
        n_messages=n_messages,
    )
    nickname_map = _fetch_guild_nicknames(guild_id)
    message_contents = [
        f'{nickname_map[message["author"]["id"]]}: {message["content"]}'
        for message in recent_messages[::-1]
    ]
    summary = _summarize_recent_messages(message_contents)
    await _send_followup_message(token, summary)
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    }


async def summarize_since_my_last_message(
    guild_id: str,
    channel_id: str,
    user_id: str,
    interaction_id: str,
    token: str,
):
    load_dotenv()
    await _acknowledge_request(interaction_id, token)
    recent_messages = _fetch_messages_since_last_user_message(
        channel_id=channel_id,
        user_id=user_id,
    )
    nickname_map = _fetch_guild_nicknames(guild_id)
    message_contents = [
        f'{nickname_map[message["author"]["id"]]}: {message["content"]}'
        for message in recent_messages[::-1]
    ]
    summary = _summarize_recent_messages(message_contents)
    await _send_followup_message(token, summary)
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    }
