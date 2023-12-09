from white_elephant_bot.data_types import ApplicationCommandOption, ApplicationCommandOption
from white_elephant_bot.applications import perform_test, summarize


async def handle_application_command(
    request_body: dict,
):
    command_name = request_body["data"]["name"]
    command_options = _process_command_options(
        [
            ApplicationCommandOption(
                name=option["name"],
                value=option["value"],
                option_type=option["type"],
            )
            for option in request_body["data"]["options"]
        ]
    )
    if command_name == "test":
        return perform_test.handle(message=command_options["message"])
    elif command_name == "summarize":
        return summarize.handle(
            channel_id=request_body["channel_id"],
            user_name=request_body["member"]["user"]["username"],
        )


def _process_command_options(command_options: list[ApplicationCommandOption]) -> dict:
    return {
        option.name: option.value
        for option in command_options
    }
