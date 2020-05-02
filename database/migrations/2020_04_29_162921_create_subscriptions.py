from orator.migrations import Migration


class CreateSubscriptions(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('subscriptions') as table:
            table.increments('id')
            table.big_integer('guild_id')
            table.big_integer('channel_id')
            table.enum('type', ['tengoku', 'bazaar'])
            table.timestamps()

            table.foreign('guild_id').references('id').on('guilds').on_delete('cascade').on_update('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('subscriptions')
