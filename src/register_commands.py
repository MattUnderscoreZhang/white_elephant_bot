from dotenv import load_dotenv
import os
import requests
from typing import cast


bot_id = "1180929424556818483"
whalefall_guild_id = "220331615749013514"
url = f"https://discord.com/api/v10/applications/{bot_id}/guilds/{whalefall_guild_id}/commands"


load_dotenv()
bot_token=cast(str, os.getenv("DISCORD_BOT_TOKEN"))


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


command_id = "1182814737927503934"
response = requests.delete(
    f"applications/{bot_id}/guilds/{whalefall_guild_id}/commands/{command_id}",
    headers={
        "Authorization": f"Bot {bot_token}"
    },
)
print(response.json())
