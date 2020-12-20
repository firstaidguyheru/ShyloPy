import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
from asyncio import sleep as s

load_dotenv()

intents = None
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
    if member.guild.id == 719972123879407678: ## specifying which server the bot should welcome users in.
        mbed = discord.Embed(
            title = 'Welcome To The Chamber',
        )
        mbed.set_image(url=f'{member.avatar_url}')
        mbed.set_footer(text=f'Members: {member.guild.member_count}')
        await member.send(embed=mbed)

## ^ This event is used to welcome users to my server, id is specified.

client.run(os.getenv('TOKEN'))
