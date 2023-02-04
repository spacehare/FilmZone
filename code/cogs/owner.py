from discord.ext import commands


class OwnerModule(commands.Cog):
    '''owner only commands'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def sync(self, ctx: commands.Context):
        await self.bot.tree.sync()


async def setup(bot):
    await bot.add_cog(OwnerModule(bot))
