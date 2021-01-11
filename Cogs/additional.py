import discord
import random
from discord.ext import commands
from discord.ext.commands import BucketType
import time
import datetime



class additional(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send('Pinging...')
        ping = (time.monotonic() - before) * 1000
        if ping < 200:
            color = 0x35fc03
        elif ping < 350:
            color = 0xe3f51d
        elif ping < 500:
            color = 0xf7700f
        else:
            color = 0xf7220f
        pEmbed = discord.Embed(title="Stats.", color=color)
        pEmbed.add_field(name="Latency", value=f'{int(ping)}ms')
        pEmbed.add_field(name="API", value=f'{round(self.bot.latency * 1000)}ms')
        pEmbed.set_thumbnail(url=self.bot.user.avatar_url)
        await message.edit(content=None, embed=pEmbed)

## *more python switch cases*

    @commands.command()
    async def a(self, ctx, channel: discord.TextChannel, *, msg: str):
        if ctx.author.guild_permissions.administrator:
            await ctx.send('Gotcha.)
            await channel.send(msg)
 
## ^ Announce command lol

def setup(bot):
    bot.add_cog(additional(bot))
