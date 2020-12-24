import discord as d
import random
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import BucketType



class modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = self.bot.get_all_channels()
        channel = get(guild, guild__name="Clark's Chamber", name='private')
        if message.channel == message.author.dm_channel:
            await channel.send(message.content)
            await message.channel.send('Your message has been sent!', delete_after=7)
        
## simple and pretty bad modmail command, it works, that's all that matters.

def setup(bot):
    bot.add_cog(modmail(bot))