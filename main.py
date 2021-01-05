import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from asyncio import sleep as s
from discord.utils import get

load_dotenv()

intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('shylo!'), case_insensitive=True, help_comamnd = None, intents = intents)


@client.event
async def on_ready():
    print(f'{client.user} has Awoken!')
    await client.wait_until_ready()


@client.event
async def on_member_join(member):
    channel = get(member.guild.channels, name='welcome') ## specifying channel name.
    mbed = discord.Embed(
        title = f'Welcome To {member.guild.name}',
        url = 'https://discord.gg/csUnYsr',
        color = 0x2c2f33
    )
    mbed.set_image(url=f'{member.avatar_url}')
    mbed.set_footer(text=f'New Member Count: {member.guild.member_count} | ID: {member.id}')
    await channel.send(embed=mbed)

## ^ This event is used to welcome users to my server, server members intent needed for it to work.

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    checks = ('help me', 'how to', 'i need help', 'how do i', 'can someone help', 'i have a question')
    if 'help me' in message.content:
        await message.channel.send('<:readthedocs:775801469685071893>')
    elif 'how to' in message.content:
        await message.channel.send('<:readthedocs:775801469685071893>')
    elif 'i need help' in message.content:
        await message.channel.send('<:readthedocs:775801469685071893>')
    elif 'how do i' in message.content:
        await message.channel.send('<:readthedocs:775801469685071893>')
    elif 'can someone help' in message.content:
        await message.channel.send('<:readthedocs:775801469685071893>')
    elif 'i have a question' in message.content:
        await message.channel.send('<:readthedocs:775801469685071893>')

## ^ Read the docs | Switch Cases in python!

@client.command()
async def reply(ctx, user: discord.User, *, msg): # placing in args needed for specification of user and message sent through the bot to the user.
    if ctx.author.guild_permissions.administrator:
        try:
            await user.send(f'{msg} [{ctx.author.mention}]')
            await ctx.send('Success.')
        except:
            await ctx.send('Error when sending message to {user}.')

# notifier for modmail.

extensions = ['Cogs.additional', 'Cogs.modmail']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)


client.run(os.getenv('TOKEN'))
