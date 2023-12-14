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
        return await perform_test.perform_test(message=command_options["message"])
    elif command_name == "summarize":
        return await summarize.summarize(
            guild_id=request_body["guild_id"],
            channel_id=request_body["channel_id"],
            n_messages=command_options["n_messages"],
            interaction_id=request_body["id"],
            token=request_body["token"],
        )
    elif command_name == "summarize_since_last_message":
        return await summarize.summarize_since_last_message(
            guild_id=request_body["guild_id"],
            channel_id=request_body["channel_id"],
            user_id=request_body["member"]["user"]["id"],
            interaction_id=request_body["id"],
            token=request_body["token"],
        )
