from discord.ext import tasks
from cogs.base_cog import BaseCog
from datetime import datetime
from adventurer_square import AdventurerSquare
from timezone import JST
import cv2


def update_strong_image():
    strength = AdventurerSquare().get_tokoyami_strength()
    image_file_names = list(map(lambda value: '{idx}_{s}.png'.format(idx=value[0], s=value[1]), enumerate(strength.values())))
    tokoyami_image_urls = list(map(lambda filename: 'img/tokoyami/' + filename, image_file_names))
    tokoyami_images = list(map(lambda url: cv2.imread(url), tokoyami_image_urls))
    merged_image = cv2.hconcat(tokoyami_images)
    cv2.imwrite('img/tokoyami/merged_image.png', merged_image)


class Strong(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        update_strong_image()
        self.update_strong.start()
        self.bot.is_updating_strength = False

    @tasks.loop(minutes=1.0)
    async def update_strong(self):
        now_time = datetime.now(JST).strftime('%H:%M')
        if now_time == '05:59':
            self.bot.is_updating_strength = True
            return

        if now_time == '06:05':
            self.bot.is_updating_strength = False
            return

        if now_time != '06:03':
            return

        update_strong_image()

    @update_strong.before_loop
    async def update_strong_before(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Strong(bot))
