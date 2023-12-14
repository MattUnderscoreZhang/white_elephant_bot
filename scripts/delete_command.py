from dotenv import load_dotenv
import os
import requests
import sys
from typing import cast


load_dotenv()
bot_token=cast(str, os.getenv("BOT_TOKEN"))
bot_id=cast(str, os.getenv("BOT_ID"))
guild_id=cast(str, os.getenv("GUILD_ID"))


if __name__ == "__main__":
    command_id = sys.argv[1]
    requests.delete(
        url=f"https://discord.com/api/v10/applications/{bot_id}/guilds/{guild_id}/commands/{command_id}",
        headers={
            "Authorization": f"Bot {bot_token}"
        },
    )
