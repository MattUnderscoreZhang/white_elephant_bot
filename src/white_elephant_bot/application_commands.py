from dataclasses import dataclass
import os

from white_elephant_bot.data_types import ResponseType


@dataclass
class ApplicationCommandOption:
    name: str
    value: str
    option_type: int


async def handle_application_command(
    command_name: str,
    command_options: list[ApplicationCommandOption],
):
    options_dict = _process_command_options(command_options)
    if command_name == "test":
        return _perform_test(options_dict["message"])


def _process_command_options(command_options: list[ApplicationCommandOption]) -> dict:
    return {
        option.name: option.value
        for option in command_options
    }


async def _perform_test(message: str):
    test_key = os.getenv("TEST_KEY")
    return {
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": f"You said {message}.\nSecret key is {test_key}"
        }
    }
