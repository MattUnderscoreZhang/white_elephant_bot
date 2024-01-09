from dotenv import load_dotenv
from gpt_interface import GptInterface
import os
from typing import cast

from white_elephant_bot.data_types import ResponseType
from white_elephant_bot.utils.async_function import (
    acknowledge_request,
    send_followup_message,
)
from white_elephant_bot.utils.fetch_messages import fetch_recent_messages


async def emojify_last_message(
    channel_id: str,
    interaction_id: str,
    token: str,
):
    load_dotenv()
    await acknowledge_request(interaction_id, token)
    interface = GptInterface(
        openai_api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-4",
    )
    last_message = fetch_recent_messages(
        channel_id=channel_id,
        n_messages=1,
    )[0]["content"]
    emojified_message = interface.say(
        "Repeat this message back to me using only emojis. Translate the meaning rather than the literal words. The message: "
        + last_message
    )
    await send_followup_message(token, emojified_message)
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    }


if __name__ == "__main__":
    from asyncio import run
    load_dotenv()
    channel_id = cast(str, os.getenv("TEST_CHANNEL_ID"))
    interaction_id = cast(str, os.getenv("TEST_INTERACTION_ID"))
    token = cast(str, os.getenv("BOT_TOKEN"))
    message = run(emojify_last_message(channel_id, interaction_id, token))
    print(message)
