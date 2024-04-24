import peewee as pw

from pathlib import Path

# database is created in parent directory of this file
PICO_DB = pw.SqliteDatabase(Path(__file__).parent.parent / 'raiderio.db')

class Characters(pw.Model):
    realm = pw.TextField(null=False)
    name = pw.TextField(null=False)
    url = pw.TextField(null=True)
    userId = pw.IntegerField(null=True)
    guildId = pw.IntegerField(null=False)

    def __repr__(self) -> str:
        return f"<Character: {self.get_id()}, guild_id={self.guildId}, realm={self.realm}, name={self.name}>"

    class Meta:
        database = PICO_DB

class MPlusRuns(pw.Model):
    link = pw.TextField(null=False)
    date = pw.TextField(null=False)

    def __repr__(self) -> str:
        return f"<MPlusRun: {self.get_id()}>"

    class Meta:
        database = PICO_DB

PICO_DB.create_tables([Characters, MPlusRuns])