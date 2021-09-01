import asyncio
import os

import aiohttp
import discord
from discord.ext import commands

from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('shylo!'), case_insensitive=True, help_command=None, intents=intents)
bot.session = aiohttp.ClientSession()

@bot.event
async def on_ready():
    print(f'{bot.user} has Awoken!')
    await bot.wait_until_ready()

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='welcome') # specifying channel name.
    channel_2 = discord.utils.get(member.guild.channels, name='general')

    mbed = discord.Embed(
        title=f'Welcome To {member.guild.name}',
        url='https://discord.gg/csUnYsr',
        color=0x2c2f33
    )
    mbed.set_image(url=f'{member.avatar_url}')
    mbed.set_footer(text=f'New Member Count: {member.guild.member_count} | ID: {member.id}')

    mbed_2 = discord.Embed(
        description=f'{member.mention} hopped into the Chamber. If you have any coding-related questions, feel free to ask in <#857670125176356874> <:readthedocs:857736664381915157>',
        color=0x2c2f33
    )
    mbed_2.set_footer(text=f'New Member Count: {member.guild.member_count}')

    await channel.send(embed=mbed)
    await channel_2.send(embed=mbed_2, delete_after=60*60)

    await asyncio.sleep(60*10) # Waiting 10 minutes before updating member count channel so I don't get rate-limited.

    null = bot.get_channel(857704020063682580)

    await null.edit(name=f'Null: {member.guild.member_count}')

# ^ This event is used to welcome users to my server, server members intent needed for it to work.


@bot.event
async def on_member_remove(member): # Member remove event to counter-act join event.
    mbed = discord.Embed(
        description=f'{member.mention} escaped the Chamber.',
        color=0x2c2f33
    )
    mbed.set_footer(text=f'New Member Count: {member.guild.member_count}')
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(embed=mbed, delete_after=60*60)

    await asyncio.sleep(60*10) # Wait 10 minutes before updating.

    null = bot.get_channel(857704020063682580)
    await null.edit(f'Null: {member.guild.member_count}')
            
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    else:
        channel = discord.utils.get(bot.get_all_channels(), guild__name="Clark's Chamber", name='monke-chain')

        if message.channel.id == channel.id:

            if not message.content.lower() == 'monke':
                await message.delete()

            else:
                return

    await bot.process_commands(message)

# If someone edits the message in #monke-chain and the message isnt "monke", we will delete it.

@bot.event
async def on_message_edit(before, after):
    if after.author == bot.user:
        return

    else:
        channel = discord.utils.get(bot.get_all_channels(), guild__name="Clark's Chamber", name='monke-chain')

        if after.channel.id == channel.id:
            if not after.content.lower() == 'monke':
                await after.delete()

# Channel's starting to get annoying to moderate!

@bot.command()
async def reply(ctx, user: discord.User, *, msg:str): # placing in args needed for specification of user and message sent through the bot to the user.
    if ctx.author.guild_permissions.administrator:
        try:
            mbed = discord.Embed(
                description=f'{msg}',
                color=0x2c2f33
            )
            mbed.set_footer(text=f'Message Sent By: {ctx.author}')

            await user.send(embed=mbed)
            return await ctx.send('Success.')

        except Exception:
            return await ctx.send(f'Error when sending message to {user}.')
    
# notifier for modmail.

extensions = ['Cogs.additional', 'Cogs.modmail']

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)


bot.run(os.getenv("TOKEN"))
