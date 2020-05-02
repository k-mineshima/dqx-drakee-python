from discord.ext import commands
from discord.ext.commands import Context, CommandInvokeError
from orator.exceptions.query import QueryException
from embed import on_error_message, item_nothing_registered, wait_for_get_market_prices, bazaar_market_price, item_registered, item_not_found, delete_item_nothing, delete_items, item_registered_list, create_bazaar_subscription, update_bazaar_subscription, duplicate_subscription
from cogs.base_cog import BaseCog
from config.adventurer_square import username, password
from adventurer_square import AdventurerSquare
from database.models import BazaarItemRecord, SubscriptionRecord
from database.settings import db
from logging import getLogger

logger = getLogger(__name__)


class Bazaar(BaseCog):
    @commands.group(invoke_without_command=True)
    async def bazaar(self, ctx: Context):
        item_records = BazaarItemRecord.all()

        if len(item_records) <= 0:
            await ctx.send(embed=item_nothing_registered())
            return

        wait_message = await ctx.send(embed=wait_for_get_market_prices())

        adventurer_square = AdventurerSquare().login(username=username, password=password)

        item_list = []
        for item_record in item_records:
            market_price = adventurer_square.get_market_price(item_record.id)
            item_list.append((item_record.name, market_price))

        adventurer_square.close()
        await wait_message.delete()
        await ctx.send(embed=bazaar_market_price(item_list=item_list))

    @bazaar.command()
    async def add(self, ctx: Context, *args):
        id_list = set(args)

        adventurer_square = AdventurerSquare().login(username=username, password=password)
        item_list = []
        for item_id in id_list:
            item_name = adventurer_square.get_item_name_by_id(item_id)
            if item_name is None:
                await ctx.send(embed=item_not_found(item_id=item_id))
                return

            item_list.append({
                'item_id': item_id,
                'item_name': item_name,
                'already_registered': False
            })

        with db.transaction():
            for item_dict in item_list:
                already_exists = BazaarItemRecord.find(item_dict['item_id']) is not None
                if already_exists:
                    item_dict['already_registered'] = True

                BazaarItemRecord.create(id=item_dict['item_id'], name=item_dict['item_name'])

            db.commit()

        await ctx.send(embed=item_registered(item_list=item_list))

    @bazaar.command()
    async def delete(self, ctx: Context, *args):
        item_list = set(args)
        item_records = BazaarItemRecord.all()

        deleted_items = []
        for item_identifier in item_list:
            for item_record in item_records:
                item_id = item_record.id
                item_name = item_record.name
                if item_id != item_identifier and item_name != item_identifier:
                    continue

                deleted_items.append(item_name)
                item_record.delete()

        if len(deleted_items) <= 0:
            await ctx.send(embed=delete_item_nothing())
            return

        await ctx.send(embed=delete_items(deleted_items=deleted_items))

    @bazaar.command()
    async def list(self, ctx: Context):
        item_list = BazaarItemRecord.all()
        if len(item_list) <= 0:
            await ctx.send(embed=item_nothing_registered())
            return

        item_names = list(map(lambda record: record.name, item_list))
        await ctx.send(embed=item_registered_list(item_list=item_names))

    @bazaar.command()
    async def subscribe(self, ctx: Context):
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id

        subscription_record = SubscriptionRecord.where('guild_id', guild_id).where('type', 'bazaar').first()

        if subscription_record is None:
            SubscriptionRecord.create(guild_id=guild_id, channel_id=channel_id, type='bazaar')
            await ctx.send(embed=create_bazaar_subscription(ctx.channel))
            return

        if subscription_record.channel_id == channel_id:
            await ctx.send(embed=duplicate_subscription(channel=ctx.channel))
            return

        before_channel = await self.bot.fetch_channel(subscription_record.channel_id)

        subscription_record.channel_id = channel_id
        subscription_record.save()

        await ctx.send(embed=update_bazaar_subscription(before_channel, ctx.channel))

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, CommandInvokeError):
            original = error.original
            if isinstance(original, QueryException):
                logger.exception('Raise Exception: %s', original)
                await ctx.send(embed=on_error_message(error_message='[1001] {error_message}'.format(
                    error_message=str(original.previous)
                )))
                return

        logger.exception('Raise Exception: %s', error)
        await ctx.send(embed=on_error_message())


def setup(bot):
    bot.add_cog(Bazaar(bot))
