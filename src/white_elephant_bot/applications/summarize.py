from dotenv import load_dotenv
from gpt_interface import GptInterface
import os
import requests
from typing import cast

from white_elephant_bot.data_types import ResponseType


def _fetch_recent_messages(
    channel_id: int,
    n_messages: int = 300,
) -> list[dict]:
    messages = []
    last_message_id = None
    while True:
        n_messages_in_current_batch = min(100, n_messages - len(messages))
        if n_messages_in_current_batch <= 0:
            return messages
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
        member['user']['id']: member.get('nick', member['user']['username'])
        for member in members
    }


def _summarize_recent_messages(messages: dict) -> str:
    if len(messages) == 0:
        return "No messages since your last interaction in this channel."
    interface = GptInterface(
        openai_api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-4",
    )
    interface.set_system_message(
        "The user will pass you their missed Discord messages. Summarize the content of the logs, without additional commentary.",
    )
    summary = interface.say(str(messages))
    return summary


async def _acknowledge_request(interaction_id: int, token: str) -> None:
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


async def handle(
    guild_id: int,
    channel_id: int,
    n_messages: int,
    interaction_id: int,
    token: str,
):
    load_dotenv()
    await _acknowledge_request(interaction_id, token)
    recent_messages = _fetch_recent_messages(
        channel_id=channel_id,
        n_messages=n_messages,
    )
    nickname_map = _fetch_guild_nicknames(guild_id)
    message_contents = {
        nickname_map[message["author"]["id"]]: message["content"]
        for message in recent_messages[::-1]
    }
    requests.post(  # debugging
        url=f"https://discord.com/api/v9/webhooks/{os.getenv('BOT_ID')}/{token}",
        json=message_contents,
    )
    summary = _summarize_recent_messages(message_contents)
    await _send_followup_message(token, summary)
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    }
