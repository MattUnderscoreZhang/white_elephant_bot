from fastapi import FastAPI
import os


app = FastAPI()


@app.post("/")
async def _(request: dict):
    if request["type"] == 1:
        return {
            "type": 1
        }


@app.post("/test")
async def _():
    test_key = os.getenv("TEST_KEY")
    return {"message": test_key}
