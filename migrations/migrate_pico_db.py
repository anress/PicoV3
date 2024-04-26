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

    char.realm = char.realm.capitalize()

    if char.realm == "Cthun":
        char.realm = "C'Thun"

    if "tarren" in char.realm.lower():
        char.realm = "Tarren Mill"
    char.name = char.name.capitalize()

    if char.name == "Frenchfries":
        char.emoji_id = 1231567733154381925
        char.emoji_name = "charFrenchfries"
    if char.name == "Emilicia":
        char.emoji_id = 1066539645694902422
        char.emoji_name = "charEmilicia" 
    if char.name == "Galeshra":
        char.emoji_id = 1153428321170903222
        char.emoji_name = "charGaleshra" 
    if char.name == "Lepaan":
        char.emoji_id = 1066628681621065738
        char.emoji_name = "charLepaan"
    if char.name == "Laitmon":
        char.emoji_id = 1066491400948035665
        char.emoji_name = "charLaitmon"
    if char.name == "Moosekey":
        char.emoji_id = 988532701629919322
        char.emoji_name = "charMoosekey"
    if char.name == "Phindror":
        char.emoji_id = 1210218237959348264
        char.emoji_name = "charPhindror"
    if char.name == "Picassu":
        char.emoji_id = 860184017574952991
        char.emoji_name = "charPicassu"
    if char.name == "Picowsu":
        char.emoji_id = 1169211093256765471
        char.emoji_name = "charPicowsu"
    if char.name == "Picursu":
        char.emoji_id = 1106213678916837477
        char.emoji_name = "charPicursu"
    if char.name == "Pockets":
        char.emoji_id = 1066663086787940352
        char.emoji_name = "charPockets"   
    if char.name == "Riptus":
        char.emoji_id = 1066489147117809796
        char.emoji_name = "charRiptus"    
    if char.name == "Serenica":
        char.emoji_id = 1105099409634644011
        char.emoji_name = "charSerenica"    
    if char.name == "Serenicorpse":
        char.emoji_id = 1210217608662614026
        char.emoji_name = "charSerenicorpse" 
    if char.name == "Sereniscale":
        char.emoji_id = 1128676085081583757
        char.emoji_name = "charSereniscale"    
    if char.name == "Sorenn":
        char.emoji_id = 860184017957158942
        char.emoji_name = "charSorenn"    
    if char.name == "Tiggsy":
        char.emoji_id = 1066663192786386964
        char.emoji_name = "charTiggsy"   
    if char.name == "Xabalbar":
        char.emoji_id = 1210218181902204998
        char.emoji_name = "charXabalbar"    
    if char.name == "Orënne":
        char.emoji_id = 988519368822521857
        char.emoji_name = "charOrenne"    
    if char.name == "Cramorant":
        char.emoji_id = 860184017374412811
        char.emoji_name = "charCramorant"

    char.save()