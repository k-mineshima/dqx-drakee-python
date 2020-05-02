from database.settings import db
from orator import Model

Model.set_connection_resolver(db)


class GuildRecord(Model):
    __table__ = 'guilds'
    __fillable__ = [
        'id',
        'name'
    ]


class BazaarItemRecord(Model):
    __table__ = 'bazaar_items'
    __fillable__ = [
        'id',
        'name'
    ]


class SubscriptionRecord(Model):
    __table__ = 'subscriptions'
    __fillable__ = [
        'guild_id',
        'channel_id',
        'type'
    ]


if __name__ == '__main__':
    import logging
    logging.basicConfig(level='DEBUG')
    record = SubscriptionRecord.where('guild_id', '123').where('type', 'tengoku').first()
    print(record.id)
    print(record.guild_id)
    print(record.channel_id)
    print(record.type)

