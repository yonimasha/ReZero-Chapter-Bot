import discord
import requests
import asyncio
from bs4 import BeautifulSoup

def run_discord_bot():
    TOKEN = "MTEzNDU3ODU3NTQwMDUwMTMxMA.GUK3Yx.9gZVgSA5c0RilQMnUUqv3vWS1JS_apd5cdIlTo"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running.")


    client.run(TOKEN)
