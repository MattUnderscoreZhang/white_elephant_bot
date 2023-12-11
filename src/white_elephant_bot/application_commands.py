from white_elephant_bot.applications import perform_test, summarize


async def handle_application_command(
    request_body: dict,
):
    command_name = request_body["data"]["name"]
    command_options = {
        option["name"] : option["value"]
        for option in request_body["data"].get("options", [])
    }
    if command_name == "test":
        return await perform_test.handle(message=command_options["message"])
    elif command_name == "summarize":
        return await summarize.handle(
            guild_id=request_body["guild_id"],
            channel_id=request_body["channel_id"],
            n_messages=command_options["n_messages"],
            interaction_id=request_body["id"],
            token=request_body["token"],
        )
