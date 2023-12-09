from dotenv import load_dotenv
import os
import requests
from typing import cast


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
        "name": "test",
        "description": "Test slash command",
        "type": 1,  # slash command
        "options": [
            {
                "name": "message",
                "description": "Message to echo back",
                "type": 3,  # string
                "required": True,
            },
        ],
    },
)
print(response.json())
