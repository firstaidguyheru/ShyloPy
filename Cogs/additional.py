import discord
import random
from discord.ext import commands
from discord.ext.commands import BucketType
import time
import datetime


class additional(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
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

    @commands.command(aliases=['announce'])
    async def a(self, ctx, channel: discord.TextChannel, *, msg: str):
        if ctx.author.guild_permissions.administrator:
            await ctx.send('Gotcha.')
            await channel.send(msg)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            if after.nick.startswith('!'):
                nick = [char for char in after.nick if char != '!']
                await after.edit(nick="".join(nick))
    
## ^ Anti-hoisting

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            featured = discord.utils.get(member.guild.roles, name="Featured Bots")
            beloved = discord.utils.get(member.guild.roles, name="Beloved Bots")
            
            flags = [k.lower() for k, v in dict(member.public_flags).items() if v]
            if "verified_bot" in flags:
                verified = discord.utils.get(member.guild.roles, name="Verified Bot Developer/Bot")

                await member.add_roles([featured, beloved, verified])
                return
            
            await member.add_roles([featured, beloved])


def setup(bot):
    bot.add_cog(additional(bot))
