from fastapi import FastAPI, Request, Response, status

from white_elephant_bot.application_commands import handle_application_command
from white_elephant_bot.data_types import (
    RequestType,
    ResponseType,
    ApplicationCommandType,
)
from white_elephant_bot.validation import validate_request


app = FastAPI()


@app.post("/")
async def _(request: Request, response: Response):
    # validate request
    if not await validate_request(request):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Invalid request signature"
    request_body = await request.json()
    request_type = request_body["type"]
    # respond to ping
    if request_type == RequestType.PING:
        return {
            "type": ResponseType.PONG
        }
    # handle application command
    elif request_type == RequestType.APPLICATION_COMMAND:
        application_command_type = request_body["data"]["type"]
        if application_command_type == ApplicationCommandType.CHAT_INPUT:
            return await handle_application_command(
                request_body,
            )
        else:
            return "I currently don't have this functionality."
    else:
        return "I currently don't have this functionality."
