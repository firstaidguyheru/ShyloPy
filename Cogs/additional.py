
import time

import discord
from discord.ext import commands

from doc_search import AsyncScraper


class Docs:
    def __init__(self, *, url: str, aliases: tuple = ()):
        self.url = url
        self.aliases = aliases


class Additional(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scraper = AsyncScraper()
        
        self.page_types = {
            'discord.py': Docs(
                url='https://discordpy.readthedocs.io/en/latest',
                aliases=('d.py', 'dpy', 'discordpy', 'discord'),
            ),
            'python': Docs(
                url='https://docs.python.org/3',
                aliases=('py', 'p'),
            ),
            'pillow': Docs(
                url='https://pillow.readthedocs.io/en/stable',
                aliases=('pil',),
            ),
            'asyncpg': Docs(
                url='https://magicstack.github.io/asyncpg/current',
            ),
            'aiohttp': Docs(
                url='https://docs.aiohttp.org/en/stable',
            ),
            'wand': Docs(
                url='https://docs.wand-py.org/en/0.6.5',
            ),
            'numpy': Docs(
                url='https://numpy.org/doc/1.20',
                aliases=('np',),
            ),
            'beautifulsoup': Docs(
                url='https://www.crummy.com/software/BeautifulSoup/bs4/doc',
                aliases=('bs4', 'beautifulsoup4'),
            ),
            'flask': Docs(
                url='https://flask.palletsprojects.com/en/1.1.x',
            ),
            'pymongo': Docs(
                url='https://pymongo.readthedocs.io/en/stable',
                aliases=('mongo',)
            ),
            'yarl': Docs(
                url='https://yarl.readthedocs.io/en/latest',
            ),
            'requests': Docs(
                url='https://docs.python-requests.org/en/master',
            ),
            'selenium-py': Docs(
                url='https://www.selenium.dev/selenium/docs/api/py',
                aliases=('selenium-python', 'selenium')
            ),
            'pandas': Docs(
                url='https://pandas.pydata.org/pandas-docs/stable',
                aliases=('pd',)
            ),
            'pygame': Docs(
                url='https://www.pygame.org/docs',
            ),
            'matplotlib': Docs(
                url='https://matplotlib.org/stable',
                aliases=('mpl',)
            ),
            'sqlalchemy': Docs(
                url='https://docs.sqlalchemy.org/en/14',
            ),
            'wavelink': Docs(
                url='https://wavelink.readthedocs.io/en/latest/', 
            ),
            'motor': Docs(
                url='https://motor.readthedocs.io/en/stable/', 
            ),
            'praw': Docs(
                url='https://praw.readthedocs.io/en/latest/', 
            ),
            'twitchio': Docs(
                url='https://twitchio.readthedocs.io/en/latest/',  
                aliases=('twitch',)
            ),
            'ipython': Docs(
                url='https://ipython.readthedocs.io/en/stable/',  
            ), 
            'sympy': Docs(
                url='https://docs.sympy.org/latest/',   
            ), 
            'scipy': Docs(
                url='https://docs.scipy.org/doc/scipy/reference', 
            ),
            'opencv': Docs(
                url='https://opencv-python.readthedocs.io/en/latest/', 
                aliases=('cv', 'cv2')
            ),
            'quart': Docs(
                url='https://pgjones.gitlab.io/quart/'
            ),
            'jinja': Docs(
                url='https://jinja.palletsprojects.com/en/3.0.x/'
            ),
            'c': Docs(
                url='c', 
                aliases=('clang',)
            ),
            'cpp': Docs(
                url='cpp', 
                aliases=('cplusplus', 'c++')
            ),
        }

    @commands.command()
    async def ping(self, ctx: commands.Context):
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

        embed = discord.Embed(title='Stats.', color=color)
        embed.add_field(name='Latency', value=f'{int(ping)}ms')
        embed.add_field(name='API', value=f'{round(self.bot.latency * 1000)}ms')
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        return await message.edit(content=None, embed=embed)

    @commands.command(aliases=['docs', 'documentation', 'rtfd'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rtfm(self, ctx, library_or_lang: str, query: str):
        page_ = library_or_lang.lower()
        page = self.page_types.get(page_)

        if not page:
            matches = [d for d in self.page_types.values() if page_ in d.aliases]
            if not matches:
                return await ctx.send(
                    '**That  [language | library] is not supported yet! Try one of these:**\n'
                    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
                    f'`{'` `'.join(self.page_types)}`'
                )
            page = matches[0]
        page = page.url

        if not query:
            return await ctx.send(f'**{page}**')

        if page == 'c':
            matches = await self.scraper.search_c(query)
        elif page == 'cpp':
            matches = await self.scraper.search_cpp(query)
        else:
            matches = await self.scraper.search(query, page=page)

        if not matches:
            return await ctx.send('No matches were found...')

        embed = discord.Embed(colour=discord.Colour.gold())
        embed.title = f'{library_or_lang} Documentation'
        embed.url = matches[0][1]
        embed.description = (
            f'**Results for | `{query}`**\n━━━━━━━━━━━━━━\n'+'\n'.join(
                f'[`{key}`]({url})' for key, url in matches[:10]
            )
        )

        return await ctx.reply(embed=embed, mention_author=False)

    @rtfm.error
    async def rtfm_error(self, ctx: commands.Context, error: Exception):
        embed = discord.Embed(title='An error has occurred', description='', colour=discord.Colour.red())

        if isinstance(error, commands.MissingRequiredArgument):
            embed.description+=f'You did not use the command properly\n**Usage:** shylo!{ctx.command.qualified_name} {ctx.command.signature}'

        elif isinstance(error, commands.CommandOnCooldown):
            embed.description+=f'You are on cooldown! Please wait {round(error.retry_after)} second(s).'

        return await ctx.send(embed=embed)

    @commands.command(aliases=['a'])
    async def announce(self, ctx: commands.Context, channel: discord.TextChannel, *, msg: str):
        if ctx.author.guild_permissions.administrator:
            await ctx.send('Gotcha.')
            await channel.send(msg)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.nick != after.nick:
            if after.nick.startswith('!'):
                nick = [char for char in after.nick if char != '!']
                await after.edit(nick=''.join(nick))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        if member.bot:
            featured = discord.utils.get(member.guild.roles, name='Featured Bots')
            beloved  = discord.utils.get(member.guild.roles, name='Beloved Bots')
            bot_dev  = discord.utils.get(member.guild.roles, name='Bot Developer')
            
            featured_bots_channel = self.bot.get_channel(858828635124006943)
            featured_bots_messages = [
                m.author async for m in featured_bots_channel.history(limit=15) if str(member.id) in m.content or member.name in m.content
            ]

            bot_owner = featured_bots_messages[0]
            
            owner_roles = [bot_dev]
            roles = [featured, beloved]
            flags = [flag.lower() for flag, has_flag in member.public_flags if has_flag]
     
            if 'verified_bot' in flags:
                verified = discord.utils.get(member.guild.roles, name='Verified Bot Developer/Bot')
                roles.append(verified)
                owner_roles.append(verified)
            
            await member.add_roles(*roles)
            return await bot_owner.add_roles(*owner_roles)


def setup(bot: commands.Bot):
    bot.add_cog(Additional(bot))
