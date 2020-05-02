from discord import Message, DMChannel
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.errors import ExtensionNotFound
from config.application import token, default_prefix, extensions
from config.logging import config_dict
from database.models import GuildRecord
import logging.config
import traceback


def get_prefix(ctx: Context, message: Message):
    if isinstance(message.channel, DMChannel):
        return default_prefix

    guild_record = GuildRecord.find(message.guild.id)
    return guild_record.prefix


class DqxDrakee(commands.Bot):
    def __init__(self):
        super().__init__(get_prefix)
        self.remove_command('help')
        logging.config.dictConfig(config_dict)

        for cog in extensions:
            try:
                self.load_extension(cog)
            except ExtensionNotFound:
                traceback.print_exc()


# if __name__ == '__main__':
#     adventurer_square = AdventurerSquare()
#     adventurer_square.get_tokoyami_strength()

if __name__ == '__main__':
    bot = DqxDrakee()
    bot.run(token)
