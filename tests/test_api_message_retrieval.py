import asyncio
from dotenv import load_dotenv
from gpt_interface import GptInterface
import os
import requests
from typing import cast


def _fetch_recent_messages(
    channel_id: str,
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
        member['user']['username']: member.get('nick', member['user']['username'])
        for member in members
    }


def _summarize_recent_messages(messages: dict) -> str:
    interface = GptInterface(
        openai_api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-3.5-turbo",
    )
    interface.set_system_message(
        "You get passed a log of Discord messages. Summarize what was said, without additional commentary.",
    )
    summary = interface.say(str(messages))
    return summary


async def handle(
    guild_id: str,
    channel_id: str,
    user_name: str,
    max_n_messages: int = 300,
):
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
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": summary,
        }
    }


if __name__ == "__main__":
    load_dotenv()
    messages = asyncio.run(
        handle(
            guild_id=cast(str, os.getenv("GUILD_ID")),
            channel_id=cast(str, os.getenv("TEST_CHANNEL_ID")),
            user_name=cast(str, os.getenv("TEST_USER_NAME")),
        )
    )
    print(messages)
