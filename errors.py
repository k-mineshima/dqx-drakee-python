from abc import ABCMeta


class GuildError(Exception, metaclass=ABCMeta):
    def __init__(self, error_message: str, guild_id: int):
        super().__init__('{error_message} guild_id={guild_id}'.format(error_message=error_message, guild_id=guild_id))


class GuildNotFoundError(GuildError):
    def __init__(self, guild_id: int):
        super().__init__('guild not found.', guild_id=guild_id)
        self.guild_id = guild_id
