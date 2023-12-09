import os

from white_elephant_bot.data_types import ResponseType


async def handle(message: str):
    test_key = os.getenv("TEST_KEY")
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": f"You said {message}.\nSecret key is {test_key}"
        }
    }
