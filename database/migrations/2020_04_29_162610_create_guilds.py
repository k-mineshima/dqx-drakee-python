from orator.migrations import Migration


class CreateGuilds(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('guilds') as table:
            table.big_integer('id')
            table.string('name', 255)
            table.string('prefix', 255).default('!')
            table.timestamps()

            table.primary('id')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('guilds')
