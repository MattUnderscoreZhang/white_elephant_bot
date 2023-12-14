import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import cast


def fetch_recent_messages(
    channel_id: str,
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
            async for message in channel.history(limit=max_n_messages):
                if message.author.name == user_name:
                    break
                messages.append(message)
            await bot.close()
        await bot.close()

    bot_token=cast(str, os.getenv("BOT_TOKEN"))
    bot.run(bot_token)
    return messages


if __name__ == '__main__':
    load_dotenv()
    messages = fetch_recent_messages(
        channel_id=cast(str, os.getenv("TEST_CHANNEL_ID")),
        user_name=cast(str, os.getenv("TEST_USER_NAME")),
        max_n_messages=20,
    )
    message_contents = {
        message.author.nick: message.content
        for message in messages[::-1]
    }
    breakpoint()
