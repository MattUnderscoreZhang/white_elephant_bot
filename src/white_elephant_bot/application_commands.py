import os

from white_elephant_bot.data_types import ResponseType, ApplicationCommandOption


async def handle_application_command(
    command_name: str,
    command_options: list[ApplicationCommandOption],
):
    options_dict = _process_command_options(command_options)
    if command_name == "test":
        return _handle_test(options_dict["message"])
    elif command_name == "summarize":
        return _handle_summarize()


def _process_command_options(command_options: list[ApplicationCommandOption]) -> dict:
    return {
        option.name: option.value
        for option in command_options
    }


async def _handle_test(message: str):
    test_key = os.getenv("TEST_KEY")
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": f"You said {message}.\nSecret key is {test_key}"
        }
    }


async def _handle_summarize():
    # You'll need to use Discord API to fetch unread messages in the current channel for the current user
    # Summarize the unread messages
    # Return a formatted response
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": "Summary of unread messages: ..."
        }
    }
