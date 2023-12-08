from fastapi import FastAPI
import os


app = FastAPI()


@app.post("/")
async def _():
    test_key = os.getenv("TEST_KEY")
    return {"message": test_key}
