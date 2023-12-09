from fastapi import FastAPI, Request, Response, status

from white_elephant_bot.application_commands import handle_application_command
from white_elephant_bot.data_types import RequestType, ResponseType, ApplicationCommandType
from white_elephant_bot.validation import validate_request


app = FastAPI()


@app.post("/")
async def _(request: Request, response: Response):
    # validate request
    if not await validate_request(request):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Invalid request signature"
    request_body = await request.json()
    # respond to ping
    if request_body["type"] == RequestType.PING:
        return {
            "type": ResponseType.PONG
        }
    # handle application command
    elif request_body["type"] == RequestType.APPLICATION_COMMAND:
        request_body_data = request_body["data"]
        if request_body_data["type"] == ApplicationCommandType.CHAT_INPUT:
            return await handle_application_command(
                request_body_data["name"],
                request_body_data["options"],
            )
        else:
            return "I currently don't have this functionality."
    else:
        return "I currently don't have this functionality."
