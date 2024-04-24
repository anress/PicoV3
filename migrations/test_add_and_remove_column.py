"""Simple test file illustrating how to write database migrations.

Run via `python migrations/test_add_and_remove_columns.py`.

Make sure to make the corresponding changes in the respective `models.py` file.
"""
import peewee as pw

from playhouse.migrate import SqliteMigrator, migrate
from picov3.models import BOT_DB

migrator = SqliteMigrator(BOT_DB)


## add a new column belonging to a TextField to the guild table
# comment_field = pw.TextField(default='')
migrate(
    migrator.add_column('characterrun', 'guild_id', pw.IntegerField(default=0))
)

# migrate(
#     migrator.add_column('mplusrun', 'dungeon_name', pw.TextField(default=""))
# )

# migrate(
#     migrator.add_column('mplusrun', 'key_level', pw.IntegerField(default=0))
# )


## remove column again
# migrate(
#     migrator.drop_column('mplusrun', 'character_id')
# )