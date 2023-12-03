import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
from typing import cast


def assign_targets(participants: list[str]) -> dict[str, str]:
    if len(participants) < 2:
        raise ValueError("Need at least two participants")

    assigned = participants.copy()
    while any(a == b for a, b in zip(participants, assigned)):
        random.shuffle(assigned)

    return dict(zip(participants, assigned))


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.messages = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    with open('participants.txt') as f:
        participants = [line.strip() for line in f]
    assignments = assign_targets(participants)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')
        guild = discord.utils.get(bot.guilds)
        if guild:
            for member in guild.members:
                if member.name in assignments:
                    try:
                        await member.send(assignments[member.name])
                    except discord.errors.Forbidden:
                        print(f"Couldn't send message to {member.name}")
        await bot.close()

    load_dotenv()
    bot_token=cast(str, os.getenv("DISCORD_BOT_TOKEN"))
    bot.run(bot_token)
