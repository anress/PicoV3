HEADERS = {'accept': 'application/json'}

REGION = "eu"
RAIDER_IO_BASE_URL = f"https://raider.io/api/v1/characters/profile?region={REGION}"
LINK_BASE_URL = f"https://raider.io"

SEASON = "season-df-2"
EXPANSION = 9
TIER = 31

GENERIC_ERROR_MESSAGE = "**ERROR:** Something unexpected went wrong. I send my best steward to work on it! ⚙️🛠️"

SET_CHANNEL_MESSAGE = f"Please contact a moderator to first set a channel with the `/set-runs-channel` command."

# discord message max len - 6 characters for pre- and appending "..."
MESSAGE_MAX_LEN = 1994

HEALER_CLASSES = ["Monk", "Shaman", "Paladin", "Druid", "Evoker", "Priest"]

TANK_CLASSES = ["Death Knight", "Warrior", "Druid", "Paladin", "Demon Hunter", "Monk"]

SPECS = {
    "Death Knight": ["Blood", "Frost", "Unholy"],
    "Demon Hunter": ["Havoc", "Vengeance"],
    "Druid": ["Balance", "Feral", "Guardian", "Restoration"],
    "Evoker": ["Devastation", "Preservation", "Augmentation"],
    "Hunter": ["Beast Mastery", "Marksmanship", "Survival"],
    "Mage": ["Arcane", "Fire", "Frost"],
    "Monk": ["Brewmaster", "Mistweaver", "Windwalker"],
    "Hunter": ["Beast Mastery", "Marksmanship", "Survival"],
    "Paladin": ["Holy", "Protection", "Retribution"],
    "Rogue": ["Assassination", "Outlaw", "Subtlety"],
    "Priest": ["Discipline", "Holy", "Shadow"],
    "Shaman": ["Elemental", "Enhancement", "Restoration"],
    "Warlock": ["Affliction", "Demonology", "Destruction"],
    "Warrior": ["Arms", "Fury", "Protection"],
}