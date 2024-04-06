import discord
import spoilers

intents = discord.Intents.default()
client = discord.Client(intents=intents)

TOKEN = 'MTIyNTk0MzYxNjUzNTUyNzQ4NA.GlHkRB.mI1bm2Uje2-vr6YTz8iB6QrGe7QZt-B_MPc4YM'

channel_id = 1225949347976446068

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await send_message()
    await client.close()
    
async def send_message():
    channel = client.get_channel(channel_id)
    url = 'https://www.reddit.com/r/magicTCG/comments/ptzv3e/innistrad_midnight_hunt_spoilers_912_full_set/'
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


