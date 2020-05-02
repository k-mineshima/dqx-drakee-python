from discord.ext import commands
from discord.ext.commands import Context, CommandInvokeError
from embed import on_error_message, on_strong, on_strong_updating_notice
from cogs.base_cog import BaseCog
from discord import File
from logging import getLogger

logger = getLogger(__name__)


class Strength(BaseCog):
    @commands.command()
    async def strength(self, ctx: Context):
        if self.bot.is_updating_strength:
            await ctx.send(embed=on_strong_updating_notice())
            return
        await ctx.send(file=File('img/tokoyami/merged_image.png', 'strength.png'), embed=on_strong('strength.png'))

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, CommandInvokeError):
            original = error.original
            if isinstance(original, FileNotFoundError):
                logger.exception('Raise Exception: %s', original)
                await ctx.send(embed=on_error_message(error_message='[0301] merged_image.png not found.'))
                return

        logger.exception('Raise Exception: %s', error)
        await ctx.send(embed=on_error_message())


def setup(bot):
    bot.add_cog(Strength(bot))
