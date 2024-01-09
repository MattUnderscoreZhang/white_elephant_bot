from white_elephant_bot.applications import perform_test, summarize, emojify


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
    elif command_name == "summarize_since_my_last_message":
        return await summarize.summarize_since_my_last_message(
            guild_id=request_body["guild_id"],
            channel_id=request_body["channel_id"],
            user_id=request_body["member"]["user"]["id"],
            interaction_id=request_body["id"],
            token=request_body["token"],
        )
    elif command_name == "emojify_last_message":
        return await emojify.emojify_last_message(
            channel_id=request_body["channel_id"],
            interaction_id=request_body["id"],
            token=request_body["token"],
        )


if __name__ == "__main__":
    from dotenv import load_dotenv
    from asyncio import run
    from typing import cast
    import os
    load_dotenv()
    channel_id = cast(str, os.getenv("TEST_CHANNEL_ID"))
    interaction_id = cast(str, os.getenv("TEST_INTERACTION_ID"))
    token = cast(str, os.getenv("BOT_TOKEN"))
    message = run(handle_application_command({"data": {"name": "emojify_last_message"}, "channel_id": channel_id, "id": interaction_id, "token": token, "guild_id": ""}))
    print(message)
