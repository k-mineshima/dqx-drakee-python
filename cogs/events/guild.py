from discord.ext import commands
from discord import Guild
from cogs.base_cog import BaseCog
from database.models import GuildRecord


class GuildEvent(BaseCog):
    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        guild_record = GuildRecord.find(guild.id)
        if guild_record is not None:
            guild_record.name = guild.name
        else:
            guild_record = GuildRecord(id=guild.id, name=guild.name)

        guild_record.save()

    @commands.Cog.listener()
    async def on_guild_update(self, before: Guild, after: Guild):
        GuildRecord.find(after.id).update(name=after.name)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        GuildRecord.destroy(guild.id)


def setup(bot):
    bot.add_cog(GuildEvent(bot))
