import os
import requests

from white_elephant_bot.data_types import ResponseType


async def acknowledge_request(interaction_id: str, token: str) -> None:
    requests.post(
        url=f"https://discord.com/api/v9/interactions/{interaction_id}/{token}/callback",
        json={
            "type": ResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {
                "content": "Processing your request..."
            }
        },
    )


async def send_followup_message(token: str, message: str) -> None:
    requests.post(
        url=f"https://discord.com/api/v9/webhooks/{os.getenv('BOT_ID')}/{token}",
        json={
            "content": message
        }
    )
