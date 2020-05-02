from discord.ext import tasks
from cogs.base_cog import BaseCog
from adventurer_square import AdventurerSquare, AdventurerSquareError
import discord
from config.config import management_channel_id
from database.models import SubscriptionRecord
from embed import tengoku_opened, tengoku_closed
from logging import getLogger

logger = getLogger(__name__)


class Tengoku(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.notify.start()
        self.bot.tengoku_status = None
        self.bot.tengoku_has_error = False

    def cog_unload(self):
        self.notify.cancel()

    @tasks.loop(minutes=5.0)
    async def notify(self):
        try:
            status = AdventurerSquare().get_tengoku_status()
        except AdventurerSquareError as error:
            self.bot.tengoku_has_error = True
            logger.exception('Raise Exception: %s', error)
            await self.bot.management_channel.send('an error has occurred in tengoku task.\nplease check logs.')
            return

        self.bot.tengoku_has_error = False
        if self.bot.tengoku_status is None:
            self.bot.tengoku_status = status

        is_open = status['opened']

        if is_open == self.bot.tengoku_status['opened']:
            return

        subscription_records = SubscriptionRecord.where('type', 'tengoku').get()
        for subscription_record in subscription_records:
            channel = await self.bot.fetch_channel(subscription_record.channel_id)

            if not is_open and self.bot.tengoku_status['opened']:
                await channel.send(file=discord.File('img/tengoku/close.png', 'close.png'), embed=tengoku_closed(
                    is_task=True
                ))
            else:
                await channel.send(file=discord.File('img/tengoku/open.png', 'open.png'), embed=tengoku_opened(
                    period=status['period'],
                    battle_conditions=status['battle_conditions'],
                    item_conditions=status['item_conditions'],
                    is_task=True
                ))

        self.bot.tengoku_status = status

    @notify.before_loop
    async def notify_before(self):
        await self.bot.wait_until_ready()
        self.bot.management_channel = await self.bot.fetch_channel(management_channel_id)


def setup(bot):
    bot.add_cog(Tengoku(bot))
