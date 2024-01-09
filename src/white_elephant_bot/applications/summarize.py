from dotenv import load_dotenv
from gpt_interface import GptInterface
import os
import requests
from typing import cast

from white_elephant_bot.utils.async_function import acknowledge_request, send_followup_message
from white_elephant_bot.utils.fetch_messages import fetch_recent_messages, fetch_messages_since_last_user_message


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
    await acknowledge_request(interaction_id, token)
    recent_messages = fetch_recent_messages(
        channel_id=channel_id,
        n_messages=n_messages,
    )
    nickname_map = _fetch_guild_nicknames(guild_id)
    message_contents = [
        f'{nickname_map[message["author"]["id"]]}: {message["content"]}'
        for message in recent_messages[::-1]
    ]
    summary = _summarize_recent_messages(message_contents)
    await send_followup_message(token, summary)
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
    await acknowledge_request(interaction_id, token)
    recent_messages = fetch_messages_since_last_user_message(
        channel_id=channel_id,
        user_id=user_id,
    )
    nickname_map = _fetch_guild_nicknames(guild_id)
    message_contents = [
        f'{nickname_map[message["author"]["id"]]}: {message["content"]}'
        for message in recent_messages[::-1]
    ]
    summary = _summarize_recent_messages(message_contents)
    await send_followup_message(token, summary)
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    }
