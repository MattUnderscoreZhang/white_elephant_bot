from fastapi import FastAPI, Request, Response, status
import os

from white_elephant_bot.validation import validate_request


app = FastAPI()


def ping_response():
    return {
        "type": 1
    }


async def test_key():
    test_key = os.getenv("TEST_KEY")
    return {"message": test_key}


@app.post("/")
async def _(request: Request, response: Response):
    if not validate_request(request):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Invalid request signature"
    request_body = await request.json()
    if request_body["type"] == 1:
        return ping_response()
