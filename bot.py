import discord
import scrape
import time



def create_message(chapters):

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

    @client.event
    async def on_ready():
        print(f"{client.user} is now running.")

        channel = client.get_channel(1134582687085109454)

        while True:

            new_chapters = scrape.get_newest_chapters(True)

            if channel:
                if len(new_chapters) > 0:
                    message = create_message(new_chapters)
                    await channel.send(message)
                else:
                    await channel.send("No new chapters in the last hour.")

            else:
                print(f'Channel not found.')

            time.sleep(3600)

    client.run(TOKEN)
