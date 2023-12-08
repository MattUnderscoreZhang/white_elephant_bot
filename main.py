from fastapi import FastAPI, Header
import os
from typing import Annotated


app = FastAPI()


@app.post("/")
async def _(request: dict):
    print(request)
    if request["type"] == 1:
        return {
            "type": 1
        }


@app.post("/test")
async def _():
    test_key = os.getenv("TEST_KEY")
    return {"message": test_key}









"""
const signature = req.get("X-Signature-Ed25519");
const timestamp = req.get("X-Signature-Timestamp");
const body = req.rawBody; // rawBody is expected to be a string, not raw bytes

const isVerified = nacl.sign.detached.verify(
    Buffer.from(timestamp + body),
    Buffer.from(signature, "hex"),
    Buffer.from(PUBLIC_KEY, "hex")
);

if (!isVerified) {
    return res.status(401).end("invalid request signature");
}
"""
