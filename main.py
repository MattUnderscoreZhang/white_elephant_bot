from fastapi import FastAPI, Request, Response, status
import os

from .src.validation import validate_request


app = FastAPI()


@app.post("/")
async def _(request: Request, response: Response):
    if not validate_request(request):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Invalid request signature"

    if request["type"] == 1:
        return {
            "type": 1
        }


async def test_key():
    test_key = os.getenv("TEST_KEY")
    return {"message": test_key}
