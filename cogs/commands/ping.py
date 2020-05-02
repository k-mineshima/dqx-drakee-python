from discord.ext import commands
from cogs.base_cog import BaseCog


class TestCog(BaseCog):
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')


def setup(bot):
    bot.add_cog(TestCog(bot))
