from discord.ext import tasks
from cogs.base_cog import BaseCog
from config.adventurer_square import username, password
from database.models import SubscriptionRecord, BazaarItemRecord
from adventurer_square import AdventurerSquare
from embed import bazaar_market_price
from timezone import JST
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)


class Bazaar(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.notify.start()

    @tasks.loop(minutes=1.0)
    async def notify(self):
        now_time = datetime.now(JST).strftime('%H:%M')
        if now_time != '09:00' and now_time != '21:00':
            return

        item_records = BazaarItemRecord.all()

        if len(item_records) <= 0:
            return

        adventurer_square = AdventurerSquare().login(username=username, password=password)

        item_list = []
        for item_record in item_records:
            market_price = adventurer_square.get_market_price(item_record.id)
            item_list.append((item_record.name, market_price))

        adventurer_square.close()

        subscription_records = SubscriptionRecord.where('type', 'bazaar').get()
        for subscription_record in subscription_records:
            channel = await self.bot.fetch_channel(subscription_record.channel_id)
            await channel.send(embed=bazaar_market_price(item_list=item_list, is_task=True))

    @notify.before_loop
    async def notify_before(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.notify.cancel()


def setup(bot):
    bot.add_cog(Bazaar(bot))
