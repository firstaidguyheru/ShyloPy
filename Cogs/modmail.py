import discord
from discord.ext import commands
from datetime import datetime


class Modmail(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 795663906018033735
        self.modmail_channel = self.bot.get_channel(self.channel_id)
        self.last_timeStamp  = datetime.utcfromtimestamp(0)

    @commands.Cog.listener()
    @commands.dm_only()
    async def on_message(self, message: discord.Message):
        """simple modmail event, it works, that's all that matters."""
        
        if message.author.bot:
            return
        try:
            if message.channel == message.author.dm_channel:
                time_difference = (datetime.utcnow() - self.last_timeStamp).total_seconds()
                
                if time_difference < 5:
                    return await message.channel.send("You are on cooldown!")
                
                embed = discord.Embed(
                    title = f"Modmail From `{message.author}`", 
                    description = f"{message.content}", 
                    color = 0x2c2f33
                )
                embed.set_footer(text=f'ID: {message.author.id}')
                
                await self.modmail_channel.send(embed=embed)
                await message.channel.send('Your message has been sent!', delete_after = 7)
                self.last_timeStamp = datetime.utcnow()
        except:
            pass

def setup(bot):
    bot.add_cog(Modmail(bot))
