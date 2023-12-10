import asyncio
from dotenv import load_dotenv
from gpt_interface import GptInterface
import os
import requests
from typing import cast

from white_elephant_bot.data_types import ResponseType


def _fetch_recent_messages(
    channel_id: int,
    user_name: str,
    max_n_messages: int = 300,
) -> list[dict]:
    messages = []
    last_message_id = None
    while True:
        n_messages_to_fetch = min(100, max_n_messages - len(messages))
        if n_messages_to_fetch <= 0:
            return messages
        response = requests.get(
            url=(
                f"https://discord.com/api/v9/channels/{channel_id}/messages" +
                (
                    f"?before={last_message_id}&limit={n_messages_to_fetch}"
                    if last_message_id
                    else f"?limit={n_messages_to_fetch}"
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
            if message['author']['username'] == user_name:
                return messages
            messages.append(message)


def _fetch_guild_nicknames(guild_id: int) -> dict[str, str]:
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
        member['user']['username']: member.get('nick', member['user']['username'])
        for member in members
    }


def _summarize_recent_messages(messages: dict) -> str:
    if len(messages) == 0:
        return "No messages since your last interaction in this channel."
    load_dotenv()  # load the OpenAI API key from a .env file
    interface = GptInterface(
        openai_api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-3.5-turbo",
    )
    interface.set_system_message(
        "You get passed a log of Discord messages. Summarize what was said, without additional commentary.",
    )
    summary = interface.say(str(messages))
    return summary


async def _acknowledge_request(interaction_id: int, token: str) -> None:
    requests.post(
        url=f"https://discord.com/api/v9/interactions/{interaction_id}/{token}/callback",
        json={
            "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {
                "content": "Processing your request..."
            }
        },
    )


async def _send_followup_message(token: str, message: str) -> None:
    load_dotenv()
    requests.post(
        url=f"https://discord.com/api/v9/webhooks/{os.getenv('BOT_ID')}/{token}",
        json={
            "content": message
        }
    )


async def handle(
    guild_id: int,
    channel_id: int,
    interaction_id: int,
    token: str,
    user_name: str,
    max_n_messages: int = 300,
):
    asyncio.create_task(_acknowledge_request(interaction_id, token))
    recent_messages = _fetch_recent_messages(
        channel_id=channel_id,
        user_name=user_name,
        max_n_messages=max_n_messages,
    )
    nickname_map = _fetch_guild_nicknames(guild_id)
    message_contents = {
        nickname_map[message["author"]["username"]]: message["content"]
        for message in recent_messages[::-1]
    }
    summary = _summarize_recent_messages(message_contents)
    asyncio.create_task(_send_followup_message(token, summary))
    return {
        "type": ResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
    }
