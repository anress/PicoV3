import peewee as pw

from pathlib import Path
from playhouse.migrate import SqliteMigrator, migrate
from picov3.models import BOT_DB, Character, Guild, MPlusRun, CharacterRun
from picov3.pico_models import PICO_DB, MPlusRuns, Characters
from picov3.helpers import normalizeRealmName

migrator = SqliteMigrator(PICO_DB)

# migrate(
#     migrator.add_column('characters', 'id', pw.IntegerField(default=0))
# )

# migrate(
#     migrator.add_column('mplusruns', 'id', pw.IntegerField(default=0))
# )


for char in Characters.select():
    char: Characters
    realm = normalizeRealmName(char.realm)
    if "tarren" in char.realm.lower():
        realm = "tarren-mill"
    guildId = char.guildId
    if guildId is None:
        guildId = 860106409839689728
    Character.create(guild_id=guildId, realm=realm, name=char.name, user_id=char.userId)
    print(char.userId)
    print(realm)
    print(".-.")