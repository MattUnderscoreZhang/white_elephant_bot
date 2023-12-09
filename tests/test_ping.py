from dotenv import load_dotenv
import os
import requests
from typing import cast


load_dotenv()
bot_token=cast(str, os.getenv("DISCORD_BOT_TOKEN"))
bot_id=cast(str, os.getenv("BOT_ID"))
guild_id=cast(str, os.getenv("GUILD_ID"))


url = f"https://whiteelephantbot-production.up.railway.app"


response = requests.post(
    url,
    headers={
        "Authorization": f"Bot {bot_token}"
    },
    json={
        "type": 1,
    },
)
print(response.json())


# command_id = "1182814737927503934"
# response = requests.delete(
    # f"applications/{bot_id}/guilds/{guild_id}/commands/{command_id}",
    # headers={
        # "Authorization": f"Bot {bot_token}"
    # },
# )
# print(response.json())



{
    'application_id': '1180929424556818483',
    'entitlements': [],
    'id': '1182833390400061573',
    'token': 'aW50ZXJhY3Rpb246MTE4MjgzMzM5MDQwMDA2MTU3Mzp1N05YaEZRNDNONkV0dGtmUGRaTU4zdFBURkRpWkRNVzBKMkZrQnprbTFFc1NQTk53RmxjOUVjQXdtZHhhTVZtamhwZHQ3dDExRTF6VVB5dVFXUm5KeVJjQ1BxRmNkeEhRMnlKVnRkNGdrclNlaGlJcmZ0NWpxUk81V05oYTRBZw',
    'type': 1,
    'user': {
        'avatar': '917e7cc19d0edaacf10e1dd6434be676',
        'avatar_decoration_data': None,
        'discriminator': '0',
        'global_name': 'BucketOfFish',
        'id': '526072162826715157',
        'public_flags': 0,
        'username': 'bucketoffish',
        },
    'version': 1,
    ,
}

{
    'application_id': '1180929424556818483',
    'entitlements': [],
    'id': '1182833390400061572',
    'token': 'aW50ZXJhY3Rpb246MTE4MjgzMzM5MDQwMDA2MTU3MjpWWXVGa01mOExaWlU2SjZMRWtxRnEya3dmeTJpalFHZ3RYSExtamtLcHg0eW9DekFOM3I2bVBTM1VaODZxUlk5eE9GdzNmc1Rja2xYU2czemxZejN0MVJwdkxIOHpBYWFvOHZRMnhHbmNzRVB4TUROYkFUVHFKdFRoN1RuaVkyRA',
    'type': 1,
    'user': {
        'avatar': '917e7cc19d0edaacf10e1dd6434be676',
        'avatar_decoration_data': None,
        'discriminator': '0',
        'global_name': 'BucketOfFish',
        'id': '526072162826715157',
        'public_flags': 0,
        'username': 'bucketoffish',
        },
    'version': 1,
}

{
    'application_id': '1180929424556818483',
    'entitlements': [],
    'id': '1182833459127930921',
    'token': 'aW50ZXJhY3Rpb246MTE4MjgzMzQ1OTEyNzkzMDkyMTp5N2xzSVprZVMwdjJzb3dxUlV5bnlkTFA3Nm1yOVcyd3BZQm5SczJxdXRjVTFkUlI2dm5MWVhhYzR4MlFmZ0lPTkZiajZOQmw5eG4yaUwyMXFFWExsNU9QVXRVNHJieGY2SXlUeEhvQXFRT0kxRU5LZzc0OUVKcnNHOTZ3aGZYSQ',
    'type': 1,
    'user': {
        'avatar': '917e7cc19d0edaacf10e1dd6434be676',
        'avatar_decoration_data': None,
        'discriminator': '0',
        'global_name': 'BucketOfFish',
        'id': '526072162826715157',
        'public_flags': 0,
        'username': 'bucketoffish',
        },
    'version': 1,
}

{
    'application_id': '1180929424556818483',
    'entitlements': [],
    'id': '1182833459127930920',
    'token': 'aW50ZXJhY3Rpb246MTE4MjgzMzQ1OTEyNzkzMDkyMDoxbk1LUnpLUFcwTTdlWXBqOWZGamZnRU9OemVHMW93NUNmTE9PakptU3F1WFFLQmsxalZnRE16TklhR0pHY3g2d3dDQVFCV3c0WjV3M252OWxYcmVLQUpEWm53enlzSFppSWkzMGlpSm80MVpBWUwzOFZlazAwSkFuQlBaVkxPYw',
    'type': 1,
    'user': {
        'avatar': '917e7cc19d0edaacf10e1dd6434be676',
        'avatar_decoration_data': None,
        'discriminator': '0',
        'global_name': 'BucketOfFish',
        'id': '526072162826715157',
        'public_flags': 0,
        'username': 'bucketoffish',
        },
    'version': 1,
}
