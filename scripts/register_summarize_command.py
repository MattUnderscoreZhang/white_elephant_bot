from dotenv import load_dotenv
import os
import requests
from typing import cast

from white_elephant_bot.data_types import ApplicationCommandOptionType


load_dotenv()
bot_token=cast(str, os.getenv("BOT_TOKEN"))
bot_id=cast(str, os.getenv("BOT_ID"))
guild_id=cast(str, os.getenv("GUILD_ID"))


url = f"https://discord.com/api/v10/applications/{bot_id}/guilds/{guild_id}/commands"


response = requests.post(
    url,
    headers={
        "Authorization": f"Bot {bot_token}"
    },
    json={
        "name": "summarize",
        "description": "Summarize recent messages",
        "type": 1,  # slash command
        "options": [
            {
                "name": "n_messages",
                "description": "Number of messages to summarize",
                "type": ApplicationCommandOptionType.INTEGER,
                "required": True,
            },
        ],
    },
)
print(response.json())
