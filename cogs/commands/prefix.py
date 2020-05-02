from discord.ext import commands
from discord.ext.commands import Context, CommandInvokeError
from discord.ext.commands.errors import MissingRequiredArgument
from database.models import GuildRecord
from embed import on_error_message, update_prefix_success, prefix_missing_required_argument
from errors import GuildNotFoundError
from cogs.base_cog import BaseCog
from logging import getLogger

logger = getLogger(__name__)


class Prefix(BaseCog):
    @commands.command()
    async def prefix(self, ctx: Context, prefix: str):
        guild_id = ctx.guild.id
        guild_record = GuildRecord.find(guild_id)
        if guild_record is None:
            raise GuildNotFoundError(guild_id=guild_id)

        guild_record.prefix = prefix
        guild_record.save()

        await ctx.send(embed=update_prefix_success(ctx.prefix, prefix))

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(embed=prefix_missing_required_argument(ctx.prefix))
            return

        if isinstance(error, CommandInvokeError):
            original = error.original
            if isinstance(original, GuildNotFoundError):
                logger.exception('Raise Exception: %s', original)
                await ctx.send(
                    embed=on_error_message(error_message='[0101] guild not found. guild_id={guild_id}'.format(
                        guild_id=original.guild_id
                    )))
                return

        logger.exception('Raise Exception: %s', error)
        await ctx.send(embed=on_error_message())


def setup(bot):
    bot.add_cog(Prefix(bot))
