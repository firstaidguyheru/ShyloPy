import discord as d
import random
from discord.ext import commands
from discord.ext.commands import BucketType




class videos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


"""    @commands.command(name='playlist', aliases=['Playlist'])
    async def playlist(self, ctx):
        mbed = d.Embed()
        mbed.title = 'Python Tutorials'
        mbed.url = 'https://www.youtube.com/playlist?list=PLTQslEOnCcC3-kXFlBhqYW5yUKYA5z_Hn'
        await ctx.send(embed=mbed)
"""

## putting this out of the way for now.

def setup(bot):
    bot.add_cog(videos(bot))
