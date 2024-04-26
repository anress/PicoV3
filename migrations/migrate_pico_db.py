import peewee as pw

from pathlib import Path
from playhouse.migrate import SqliteMigrator, migrate
from picov3.models import BOT_DB, Character, Guild, MPlusRun, CharacterRun
from picov3.pico_models import PICO_DB, MPlusRuns, Characters

migrator = SqliteMigrator(PICO_DB)

# migrate(
#     migrator.add_column('characters', 'id', pw.IntegerField(default=0))
# )

# migrate(
#     migrator.add_column('mplusruns', 'id', pw.IntegerField(default=0))
# )


for char in Character.select():
    char: Character
    if "tarren" in char.realm.lower():
        char.realm = "Tarren Mill"
    char.name = char.name.capitalize()

    char.save()