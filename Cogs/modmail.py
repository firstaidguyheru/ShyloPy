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
            await channel.send(message.content + f"\n{message.author}[`{message.author.id}`]")
            await message.channel.send('Your message has been sent!', delete_after=7)
        
    ## ^ simple modmail command, it works, that's all that matters.

    @commands.command()
    @commands.has_any_role('Staff')
    async def notify_cmd(self, ctx, user: d.Member, *, msg):
        await user.send(f'{msg}\nNotifier: {ctx.author}')
        await ctx.send('Success!')

    ## ^ This command is to DM a user for example: *why* their discord bot was(n't) added/removed onto the server and replies to modmail, can be used for other reasons but im choosing to be mature in this case.



def setup(bot):
    bot.add_cog(modmail(bot))