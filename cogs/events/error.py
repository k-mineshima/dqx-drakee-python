from discord.ext import commands
from cogs.base_cog import BaseCog
from embed import on_management_error
import traceback


class ErrorEvent(BaseCog):
    @commands.Cog.listener()
    async def on_error(self, event: str):
        self.bot.management_channel.send(embed=on_management_error(traceback.format_exc(), event))


def setup(bot):
    bot.add_cog(ErrorEvent(bot))
