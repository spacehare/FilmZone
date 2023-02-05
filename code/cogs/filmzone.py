import discord
from random import randint
from datetime import date, datetime, timedelta
from discord.ext import commands
from gsheet import gsheet
from deserialize import TFFZ
# from typing import Dict, List
from pprint import pformat
from json import dump, load
from views.raw import RawView, RerollView
from os.path import getmtime
from random import choice

TEMP_DATA_PATH = r'.temp/gsheet.json'


class FilmZoneModule(commands.Cog):
    '''film zone'''

    raw_data = {}

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # discord.ui.View.add_item(bot, discord.ui.Button(bot))

    async def cog_check(self, ctx: commands.Context):
        return TFFZ(self.bot).exhibitors in ctx.author.roles

    # def get_lucky_ones():
    #     lucky_ones = [self.guild.fetch_member(
    #             lo) for lo in self.raw_data['lucky_ones']]

    @commands.command()
    async def rand(self, ctx: commands.Context, num: int = 2):
        await ctx.reply(randint(1, num))

    @commands.command()
    async def rands(self, ctx: commands.Context, num: int = 2, amount: int = 2):
        rv = []
        for _ in range(amount):
            rv.append(randint(1, num))
        await ctx.reply(rv)

    # @commands.command()
    # async def rawdisplay(self, ctx: commands.Context):
    #     if self.raw_data:
    #         view = RawView(self.raw_data, self.bot)
    #         await ctx.send(view=view)
    #         await view.wait()
    #         # view.apply_lucky_ones.disabled = True
    #     else:
    #         await ctx.send('No data.')

    @commands.command()
    async def addrem(self, ctx: commands.Context, member: discord.Member):
        await member.remove_roles(TFFZ(self.bot).role) if TFFZ(
            self.bot).role in member.roles else await member.add_roles(TFFZ(self.bot).role)
        # await ctx.defer()

    @commands.command(aliases=['rr'])
    async def reroll(self, ctx: commands.Context):
        c = choice(self.raw_data['mane_list'])
        view = RerollView(
            await TFFZ(self.bot).guild.fetch_member(c['uid']), self.bot)
        await ctx.send(f"{self.format_film(c['film'], c['year'])} — {c['freak']}", view=view)

    @commands.command()
    async def raw(self, ctx: commands.Context):
        """display raw .json"""
        if self.raw_data:
            await ctx.send(f"```json\n{pformat(self.raw_data['picks'])}\n```")
        else:
            await ctx.send('No data.')

    @commands.command(name='load', aliases=['get'])
    async def load_temp(self, ctx):
        """load previous data from storage"""
        with open(TEMP_DATA_PATH, 'r') as file:
            self.raw_data = load(file)
        await ctx.send(f'Loaded {datetime.utcfromtimestamp(getmtime(TEMP_DATA_PATH))} utc')

    @commands.command()
    async def fz(self, ctx: commands.Context) -> None:
        """Grabs 6 picks, lucky ones. Stores in .temp/ as json."""
        self.raw_data = gsheet()  # grab random movies
        if not ctx.interaction:
            await ctx.message.add_reaction("🎲")

        if self.raw_data:
            with open(TEMP_DATA_PATH, 'w') as file:
                dump(self.raw_data, file)
            view = RawView(self.raw_data, self.bot)
            await ctx.send(view=view)
            # view.apply_lucky_ones.disabled = True
            guild = TFFZ(self.bot).guild
            lucky_ones = [await guild.fetch_member(
                lo) for lo in self.raw_data['lucky_ones']]
            today = date.today()
            later_dates = today + timedelta(days=4)
            # reply
            # pick['film'] for pick in self.raw_data['picks']
            # "\n".join(str(member) for member in lucky_ones)

            await ctx.reply(f"today: {today.strftime('%A, %B %e')}\n"
                            + f"in 4 days: {later_dates.strftime('%A, %B %e')}\n\n"
                            + "\n".join(f"{idx+1}. {self.format_film(pick['film'], pick['year'])} — {pick['freak']}"
                                        for idx, pick in enumerate(self.raw_data['picks']))
                            )
            # await view.wait()
        else:
            await ctx.send('No data.')

    @commands.command()
    async def spoil(self, ctx: commands.Context):
        await ctx.send(self.spoildisplay())

    def spoildisplay(self):
        rv = ''  # [pick['film'] for pick in self.raw_data['picks']]
        for pick in self.raw_data['picks']:
            rv += f'||{pick["film"]}|| — {pick["freak"]}\n'
        return rv

    def format_film(self, film: str, year: str):
        return f'{film} ({year})' if year else f'{film}'


async def setup(bot):
    await bot.add_cog(FilmZoneModule(bot))
