import asyncio
from dotenv import load_dotenv
import os
from typing import cast

from white_elephant_bot.applications import summarize


if __name__ == '__main__':
    load_dotenv()
    summary = asyncio.run(
        summarize.summarize_since_my_last_message(
            guild_id=cast(str, os.getenv("GUILD_ID")),
            channel_id=cast(str, os.getenv("TEST_CHANNEL_ID")),
            user_id=cast(str, os.getenv("TEST_USER_ID")),
            interaction_id="1",
            token="",
        )
    )
    print(summary)
    breakpoint()
