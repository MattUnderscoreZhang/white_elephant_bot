from dotenv import load_dotenv
from fastapi import Request
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import os
from typing import cast


async def validate_request(request: Request) -> bool:
    load_dotenv()
    public_key=cast(str, os.getenv("BOT_PUBLIC_KEY"))
    verify_key = VerifyKey(bytes.fromhex(public_key))
    try:
        signature = request.headers["X-Signature-Ed25519"];
        timestamp = request.headers["X-Signature-Timestamp"];
        raw_body = await request.body()
        verify_key.verify(f'{timestamp}{raw_body}'.encode(), bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False
