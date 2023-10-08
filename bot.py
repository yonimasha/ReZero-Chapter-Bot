import discord
import scrape
import asyncio
from scrape import ChapterScraper


def create_message(chapters):
    """
    Create message when new chapters are detected
    :param chapters: dictionary with chapter titles and word counts
    :return: message
    """

    message = f"Detected {len(chapters)} new chapter(s): \n\n"

    for chapter, word_count in chapters.items():
        message += f'• {chapter}\n\t-- There are roughly around {word_count} words in this chapter.\n\n'

    message += "I will let you know if any more chapters appear in the future."

    return message


def run_discord_bot():

    TOKEN = "MTEzNDU3ODU3NTQwMDUwMTMxMA.GUK3Yx.9gZVgSA5c0RilQMnUUqv3vWS1JS_apd5cdIlTo"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    scraper = ChapterScraper()
    new_chapters = {}

    @client.event
    async def on_ready():
        print(f"{client.user} is now running.")

        channel = client.get_channel(1134582687085109454)

        while not client.is_closed():

            new_chapters = scraper.get_newest_chapters()

            if channel:
                if len(new_chapters) > 0:
                    message = create_message(new_chapters)
                    await channel.send(message)
            else:
                print(f'Channel not found.')

            await asyncio.sleep(3600)

    @client.event
    async def on_message(message):
        print("Message recieved!")
        if message.content == "!wordcount":
            await message.channel.send(f"Current arc's word count: Approximately {sum(new_chapters.values())} words ")

    client.run(TOKEN)
