from orator.migrations import Migration


class CreateBazaarItems(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('bazaar_items') as table:
            table.string('id', 255)
            table.string('name', 255)
            table.timestamps()

            table.primary('id')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('bazaar_items')
