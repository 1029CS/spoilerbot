import discord
import spoilers
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await send_message()
    await client.close()
    
async def send_message():
    channel = client.get_channel(CHANNEL_ID)
    for i in range(len(spoilers.get_spoilers())):
        try :
            embed = discord.Embed(title=spoilers.get_title(spoilers.get_spoilers_url()[i]), url=spoilers.get_spoilers_url()[i])
            embed.set_image(url=spoilers.get_spoilers()[i])
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Error: {e}")
            continue    
        

client.event(on_ready)
client.run(TOKEN)


