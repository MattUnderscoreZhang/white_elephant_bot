from fastapi import FastAPI, Request, Response, status
import os

from white_elephant_bot.validation import validate_request


app = FastAPI()


class RequestType:
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class ResponseType:
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE =  7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9


async def test_key():
    test_key = os.getenv("TEST_KEY")
    return {"message": test_key}


@app.post("/")
async def _(request: Request, response: Response):
    if not await validate_request(request):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Invalid request signature"
    request_body = await request.json()
    if request_body["type"] == RequestType.PING:
        return {
            "type": ResponseType.PONG
        }
    print(request_body)
