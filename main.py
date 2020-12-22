import os
from dotenv import load_dotenv
from discord.ext import commands

import discord
from asyncio import sleep as s
from discord.utils import get

load_dotenv()

intents = discord.Intents.members()
client = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('shylo!', 'shylo can you?', 'shylo'), help_comamnd = None, intents = intents)



@client.event
async def on_ready():
    print(f'{client.user} has Awoken!')
    await client.wait_until_ready()


@client.command(name='notify', aliases=['Notify'])
async def hi_cmd(ctx, user: discord.User, *, msg): 
    if ctx.author.id == 461287425625554950:
        await user.send(f'{msg}')
        await ctx.send('Success!')

## ^ This command is to DM a user for example: *why* their discord bot wasn('t) added/removed onto the server, can be used for other reason's but im choosing to be mature in this case.

@client.event
async def on_member_join(member):
    channel = get(member.guild.channels, name='welcome') ## specifying channel name.
    mbed = discord.Embed(
        title = f'Welcome To {member.guild.name} | [Invite Link](https://discord.gg/csUnYsr)',
    )
    mbed.set_image(url=f'{member.avatar_url}')
    mbed.set_footer(text=f'New Member Count: {member.guild.member_count}')
    await channel.send(embed=mbed)

## ^ This event is used to welcome users to my server, server members intent needed for it to work.

client.run(os.getenv('TOKEN'))
