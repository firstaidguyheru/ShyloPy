import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from asyncio import sleep as s
from discord.utils import get
from asyncio import sleep

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('shylo!'), case_insensitive=True, help_command=None, intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has Awoken!')
    await client.wait_until_ready()

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
            
        channel = get(client.get_all_channels(), guild__name="Clark's Chamber", name='monke-chain')

@client.event
async def on_message(message):
    if message.author == client.user:
        pass

    else:
        channel = get(client.get_all_channels(), guild__name="Clark's Chamber", name='monke-chain')
        if message.channel.id == channel.id:
            if not message.content == 'monke'.casefold():
                await message.delete()
            else:
                pass
    await client.process_commands(message)

@client.event
async def on_message_edit(after):
    if after.author == client.user:
        pass

    else:
        channel = get(client.get_all_channels(), guild__name="Clark's Chamber", name='monke-chain')
        if message.channel.id == channel.id:
            if not after.content == 'monke'.casefold():
                await after.delete()

## Channel's starting to get annoying to moderate!

@client.command()
async def reply(ctx, user: discord.User, *, msg): # placing in args needed for specification of user and message sent through the bot to the user.
    if ctx.author.guild_permissions.administrator:
        try:
            await user.send(f'{msg} [{ctx.author}]')
            await ctx.send('Success.')
        except:
            await ctx.send(f'Error when sending message to {user}.')
    
# notifier for modmail.

extensions = ['Cogs.additional', 'Cogs.modmail']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)


client.run(os.getenv("TOKEN"))
