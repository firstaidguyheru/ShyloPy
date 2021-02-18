import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from asyncio import sleep as s
from discord.utils import get
from asyncio import sleep
from googleapiclient.discovery import build

load_dotenv()

intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('shylo!'), case_insensitive=True, help_command=None, intents=intents)

## YOUTUBE

async def upload_event(): ## Making a request to youtube for an upload every 30 mins.
    while True:
        try:
            youtube = build('youtube','v3', developerKey=os.getenv("YT"))
            r = youtube.playlistItems().list(
                playlistId='PLTQslEOnCcC3-kXFlBhqYW5yUKYA5z_Hn', # Setting the id to my tutorial playlist id.
                part='snippet',
                maxResults=1
            )
            data = r.execute()
            video_id = data['items'][0]['snippet']['resourceId']['videoId'] # Given the index, I am accessing a dict that provides me with the video id.
            link = f"https://www.youtube.com/watch?v={video_id}"
            ch = get(client.get_all_channels(), guild__name="Clark's Chamber", name='uploads')

            async for msg in ch.history(limit=1): # searching channel history incase if the link taken from the json is already uploaded to the channel.      
                if str(link) != str(msg.content):
                    await ch.send(f'Clark just uploaded a vid.\n{link}')
                else:
                    pass

        except IndexError:
            print('Something went wrong when getting video id from response.')
        await s(60*30)


## OTHER STUFF

@client.event
async def on_ready():
    print(f'{client.user} has Awoken!')
    await client.wait_until_ready()
    await client.loop.create_task(upload_event())


@client.event
async def on_member_join(member):
    channel = get(member.guild.channels, name='welcome') ## specifying channel name.
    channel_2 = get(member.guild.channels, name='general')
    mbed = discord.Embed(
        title = f'Welcome To {member.guild.name}',
        url = 'https://discord.gg/csUnYsr',
        color = 0x2c2f33
    )
    mbed.set_image(url=f'{member.avatar_url}')
    mbed.set_footer(text=f'New Member Count: {member.guild.member_count} | ID: {member.id}')
    mbed_2 = discord.Embed(
        description = f'{member.mention} hopped into the Chamber. <:readthedocs:775801469685071893>',
        color = 0x2c2f33
    )
    mbed_2.set_footer(text=f'New Member Count: {member.guild.member_count}')
    await channel.send(embed=mbed)
    await channel_2.send(embed=mbed_2, delete_after=60*60)
    await sleep(60*10) ## Waiting 10 minutes before updating member count channel so I don't get rate-limited.
    for channel_3 in member.guild.channels:
        if channel_3.name.startswith('N'):
            await channel_3.edit(name=f'Null: {member.guild.member_count}')
            break

## ^ This event is used to welcome users to my server, server members intent needed for it to work.


@client.event
async def on_member_remove(member): ## Member remove event to counter-act join event.
    mbed = discord.Embed(
        description = f'{member.mention} escaped the Chamber.',
        color = 0x2c2f33
    )
    mbed.set_footer(text=f'New Member Count: {member.guild.member_count}')
    channel = get(member.guild.channels, name='general')
    await channel.send(embed=mbed)
    await sleep(60*10) ## Wait 10 minutes before updating.
    for channel_2 in member.guild.channels:
        if channel_2.name.startswith('N'):
            await channel_2.edit(name=f'Null: {member.guild.member_count}')
            break
            
## ^ Read the docs | Switch Cases in python!

@client.command()
async def reply(ctx, user: discord.User, *, msg): # placing in args needed for specification of user and message sent through the bot to the user.
    if ctx.author.guild_permissions.administrator:
        try:
            await user.send(f'{msg} [{ctx.author.mention}]')
            await ctx.send('Success.')
        except:
            await ctx.send(f'Error when sending message to {user}.')
    
# notifier for modmail.

extensions = ['Cogs.additional', 'Cogs.modmail']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)


client.run(os.getenv("TOKEN"))
