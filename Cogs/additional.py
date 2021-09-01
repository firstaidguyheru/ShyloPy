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
            bot_dev = discord.utils.get(member.guild.roles, name="Bot Developer")
            
            featured_bots_channel = self.bot.get_channel(858828635124006943)
            featured_bots_messages = [m.author for m in await featured_bots_channel.history(limit=15).flatten() if str(member.id) in m.content or member.name in m.content]
            bot_owner = featured_bots_messages[0]
            
            owner_roles = [bot_dev]
            roles = [featured, beloved]
            flags = [flag.lower() for flag, has_flag in dict(member.public_flags).items() if has_flag]
     
            if "verified_bot" in flags:
                verified = discord.utils.get(member.guild.roles, name="Verified Bot Developer/Bot")
                roles.append(verified)
                owner_roles.append(verified)
            
            await member.add_roles(*roles)
            return await bot_owner.add_roles(*owner_roles)


def setup(bot):
    bot.add_cog(additional(bot))
