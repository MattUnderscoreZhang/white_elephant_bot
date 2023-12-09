import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import cast


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.messages = True
    intents.members = True

    bot = commands.Bot(command_prefix='/', intents=intents)

    @bot.slash
    async def test(ctx: SlashContext):
        print("HI")

    load_dotenv()
    bot_token=cast(str, os.getenv("DISCORD_BOT_TOKEN"))
    bot.run(bot_token)
