from discord.ext import commands
from cogs.base_cog import BaseCog
from config.config import management_channel_id
from database.models import GuildRecord
from embed import on_management_notice


class ReadyEvent(BaseCog):
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.management_channel = await self.bot.fetch_channel(management_channel_id)
        for guild in self.bot.guilds:
            guild_record = GuildRecord.find(guild.id)
            if guild_record is None:
                guild_record = GuildRecord(id=guild.id, name=guild.name)
            else:
                guild_record.name = guild.name

            guild_record.save()

        await self.bot.management_channel.send(embed=on_management_notice(
            event='on_ready',
            description='execute on_ready process.'
        ))


def setup(bot):
    bot.add_cog(ReadyEvent(bot))
