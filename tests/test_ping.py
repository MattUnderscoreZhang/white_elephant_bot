from dotenv import load_dotenv
import os
import requests
from typing import cast


def test_ping():
    load_dotenv()
    bot_id=cast(str, os.getenv("BOT_ID"))

    # url = f"whiteelephantbot-production.up.railway.app"
    url = "localhost:8000"

    response = requests.post(
        url,
        headers={
            'host': url,
            'x-signature-timestamp': '1111111111',
            'x-signature-ed25519': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'content-type': 'application/json',
            'user-agent': 'Discord-Interactions/1.0 (+https://discord.com)',
            'content-length': '111',
            'x-forwarded-for': 'xx.xxx.xx.xxx',
            'x-forwarded-proto': 'https',
            'x-envoy-external-address': 'xx.xxx.xx.xxx',
            'x-request-id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
        },
        json={
            'application_id': bot_id,
            'entitlements': [],
            'id': '1111111111111111111',
            'token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'type': 1,
            'user': {
                'avatar': '11111111111111111111111111111111',
                'avatar_decoration_data': None,
                'discriminator': '0',
                'global_name': 'xxxxxxxxxxxx',
                'id': '111111111111111111',
                'public_flags': 0,
                'username': 'xxxxxxxxxxxx',
                },
            'version': 1,
        },
    )
    assert response.status_code == 200
