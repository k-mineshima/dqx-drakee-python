from discord.ext import commands
from discord.ext.commands import Context
from cogs.base_cog import BaseCog
from logging import getLogger
from embed import on_error_message, duplicate_subscription, create_tengoku_subscription, update_tengoku_subscription, tengoku_opened, tengoku_closed, tengoku_update_failed
from database.models import SubscriptionRecord
import discord

logger = getLogger(__name__)


class Tengoku(BaseCog):
    @commands.group(invoke_without_command=True)
    async def tengoku(self, ctx: Context):
        has_error = self.bot.tengoku_has_error
        if has_error:
            await ctx.send(embed=tengoku_update_failed())
            return

        status = self.bot.tengoku_status
        if status['opened']:
            await ctx.send(file=discord.File('img/tengoku/open.png', 'open.png'), embed=tengoku_opened(
                period=status['period'],
                battle_conditions=status['battle_conditions'],
                item_conditions=status['item_conditions']
            ))
        else:
            await ctx.send(file=discord.File('img/tengoku/close.png', 'close.png'), embed=tengoku_closed())

    @tengoku.command()
    async def subscribe(self, ctx: Context):
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id

        subscription_record = SubscriptionRecord.where('guild_id', guild_id).where('type', 'tengoku').first()

        if subscription_record is None:
            SubscriptionRecord.create(guild_id=guild_id, channel_id=channel_id, type='tengoku')
            await ctx.send(embed=create_tengoku_subscription(ctx.channel))
            return

        if subscription_record.channel_id == channel_id:
            await ctx.send(embed=duplicate_subscription(channel=ctx.channel))
            return

        before_channel = await self.bot.fetch_channel(subscription_record.channel_id)

        subscription_record.channel_id = channel_id
        subscription_record.save()

        await ctx.send(embed=update_tengoku_subscription(before_channel, ctx.channel))

    async def cog_command_error(self, ctx: Context, error):
        logger.exception('Raise Exception: %s', error)
        await ctx.send(embed=on_error_message())


def setup(bot):
    bot.add_cog(Tengoku(bot))
