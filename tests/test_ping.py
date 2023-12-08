from dotenv import load_dotenv
import os
import requests
from typing import cast


load_dotenv()
bot_token=cast(str, os.getenv("DISCORD_BOT_TOKEN"))
bot_id=cast(str, os.getenv("BOT_ID"))
guild_id=cast(str, os.getenv("GUILD_ID"))


url = f"https://whiteelephantbot-production.up.railway.app"


response = requests.post(
    url,
    headers={
        "Authorization": f"Bot {bot_token}"
    },
    json={
        "type": 1,
    },
)
print(response.json())


# command_id = "1182814737927503934"
# response = requests.delete(
    # f"applications/{bot_id}/guilds/{guild_id}/commands/{command_id}",
    # headers={
        # "Authorization": f"Bot {bot_token}"
    # },
# )
# print(response.json())
