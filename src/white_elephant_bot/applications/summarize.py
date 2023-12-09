import discord
from discord.ext import commands
from dotenv import load_dotenv
from gpt_interface import GptInterface
import os
from typing import cast

from white_elephant_bot.data_types import ResponseType


def _fetch_recent_messages(
    channel_id: int,
    user_name: str,
    max_n_messages: int | None = 300,
) -> list[discord.Message]:
    intents = discord.Intents.default()
    intents.messages = True
    intents.members = True

    bot = commands.bot.Bot(command_prefix='!', intents=intents)
    messages = []

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')
        channel = bot.get_channel(channel_id)
        if isinstance(channel, discord.TextChannel):
            nonlocal messages
            async for message in channel.history(limit=cast(int, max_n_messages)):
                if message.author.name == user_name:
                    break
                messages.append(message)
            await bot.close()
        await bot.close()

    load_dotenv()
    bot_token=cast(str, os.getenv("BOT_TOKEN"))
    bot.run(bot_token)
    return messages


def _summarize_recent_messages(messages: dict) -> str:
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


async def handle(
    channel_id: int,
    user_name: str,
    max_n_messages: int | None = 300,
):
    recent_messages = _fetch_recent_messages(
        channel_id=channel_id,
        user_name=user_name,
        max_n_messages=max_n_messages,
    )
    message_contents = {
        message.author.nick: message.content
        for message in recent_messages[::-1]
    }
    print(message_contents)
    summary = _summarize_recent_messages(message_contents)
    print(summary)
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": summary,
        }
    }
