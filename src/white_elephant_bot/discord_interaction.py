import discord
import os


client = discord.Client()


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.content.startswith('/summarize'):
        channel = message.channel
        # Fetch a specific number of messages from the channel
        messages = await channel.history(limit=100).flatten() # Adjust the limit as needed
        # Process these messages to determine which ones are unread


client.run(os.getenv('YOUR_BOT_TOKEN'))
