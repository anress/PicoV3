import peewee as pw

from pathlib import Path

# database is created in parent directory of this file
BOT_DB = pw.SqliteDatabase(Path(__file__).parent.parent / 'picov3.db')

class Guild(pw.Model):
    guild_id = pw.IntegerField(null=False, unique=True)
    runs_channel_id = pw.IntegerField(null=True)
    score_channel_id = pw.IntegerField(null=True)
    is_admin_guild = pw.BooleanField(default=False)

    def __repr__(self) -> str:
        return f"<Guild: {self.get_id()}, guild_id={self.guild_id}>"

    class Meta:
        database = BOT_DB

class Character(pw.Model):
    guild_id = pw.IntegerField(null=False)
    realm = pw.TextField(null=False)
    name = pw.TextField(null=False)
    score = pw.IntegerField(null=True)
    user_id = pw.IntegerField(null=True)
    emoji_id = pw.IntegerField(null=True)
    emoji_name = pw.TextField(null=True)

    def __repr__(self) -> str:
        return f"<Character: {self.get_id()}, guild_id={self.guild_id}, realm={self.realm}, name={self.name}, score={self.score}>"

    class Meta:
        database = BOT_DB

class MPlusRun(pw.Model):
    guild_id = pw.IntegerField(null=False)
    run_id = pw.IntegerField(null=False)
    season = pw.TextField(null=False)
    dungeon_name = pw.TextField(null=False)
    key_level = pw.IntegerField(null=False)

    def __repr__(self) -> str:
        return f"<MPlusRun: {self.get_id()}, guild_id={self.guild_id}, run_id={self.run_id}, season={self.season}, dungeon_name={self.dungeon_name}, key_level={self.key_level}>"

    class Meta:
        database = BOT_DB

class CharacterRun(pw.Model):
    run_id = pw.IntegerField(null=False)
    character_id = pw.IntegerField(null=False)  
    guild_id = pw.IntegerField(null=False)    

    def __repr__(self) -> str:
        return f"<CharacterRun: {self.get_id()}, run_id={self.run_id}, character_id={self.character_id}, guild_id={self.guild_id}>"

    class Meta:
        database = BOT_DB

BOT_DB.create_tables([Guild, Character, MPlusRun, CharacterRun])