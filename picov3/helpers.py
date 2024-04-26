from .constants import RAIDER_IO_BASE_URL, LINK_BASE_URL, REGION, MESSAGE_MAX_LEN, HEALER_CLASSES, TANK_CLASSES, SPECS
import string
import math
import datetime
import discord

def getEmbedColorForKeystoneLevel(keystoneLevel):
    if keystoneLevel > 20:
        return 0xbd3fcf # pink
    if keystoneLevel > 16:
        return 0xff8000 # orange
    if keystoneLevel > 13:
        return 0xa335ee # purple
    if keystoneLevel > 9:
        return 0x0070dd # blue
    if keystoneLevel > 6:
        return 0x1eff00 # green
    return 0xffffff

def getRaiderIOBaseUrlPerChar(character_name, realm):
    return f"{RAIDER_IO_BASE_URL}&realm={realm}&name={character_name}"

def getRaiderIOLinkUrlPerChar(character_name, realm):
    return f"{LINK_BASE_URL}/characters/{REGION}/{realm}/{character_name}"

def nameToSlug(name):
    return string.capwords(name).replace("'", '').replace(":", '').replace(' ', '-')

def getDungeonImageUrl(dungeonName, expansion):
    return f"https://cdnassets.raider.io/images/dungeons/expansion{expansion}/base/{nameToSlug(dungeonName)}.jpg"

def hasHealerSpec(className):
    return className in HEALER_CLASSES

def hasTankSpec(className):
    return className in TANK_CLASSES

def getSpecName(className, orderNumber):
    match orderNumber:
        case "spec_0": return SPECS.get(className)[0]
        case "spec_1": return SPECS.get(className)[1]
        case "spec_2": return SPECS.get(className)[2]
        case "spec_3": return SPECS.get(className)[3]

def getRoleEmoji(role):
    match role:
        case "dps": return ":crossed_swords:"
        case "tank": return ":shield:"
        case "healer": return ":green_heart:"

def date_formatter(date: datetime):
   return f"{date.strftime('%A')}, {date.strftime('%d')}/{date.strftime('%m')}/{date.strftime('%Y')}, {date.strftime('%H')}:{date.strftime('%M')}"

def format_ms(ms):
    seconds =(ms/1000)%60
    seconds = int(seconds)
    minutes =(ms/(1000*60))%60
    minutes = int(minutes)

    seconds = f"{seconds:02d}"
    minutes = f"{minutes:02d}"

    return f"{minutes}:{seconds}"

def getPercentRemainingString(time_remaining_ms, keystone_time_ms):
    percentRemaining = (time_remaining_ms/keystone_time_ms) * 100
    if percentRemaining > 0:
        return str(round(percentRemaining, 2))
    else:
        percentRemaining = percentRemaining * -1
        str(round(percentRemaining, 2))

def colorToNumber(color):
    color = color[1:]
    color = "0x" + color
    return int(color, 16)

def checkIfNewMilestone(score_old, score_new):
    if score_old < 750 and score_new >= 750:
        return "Keystone Explorer"
    elif score_old < 1500 and score_new >= 1500:
        return "Keystone Conquerer"
    elif score_old < 2000 and score_new >= 2000:
        return "Keystone Master"
    elif score_old < 2500 and score_new >= 2500:
        return "Keystone Hero"
    elif score_old < 3000 and score_new >= 3000:
        return "3k"
    elif score_old < 3500 and score_new >= 3500:
        return "3.5k"
    elif score_old < 4000 and score_new >= 4000:
        return "4k"
    else:
        return None

async def send_long_message(message: str, interaction: discord.Interaction, already_responded: bool = False):
    if len(message) > MESSAGE_MAX_LEN:
        start_index = 0
        max_iterations =  (math.ceil(len(message) / MESSAGE_MAX_LEN))
        
        if not already_responded:
            await interaction.edit_original_response(content=message[0:MESSAGE_MAX_LEN])
            start_index = 1
        for part in range(start_index, max_iterations):      
            string_part = message[MESSAGE_MAX_LEN * part:min(MESSAGE_MAX_LEN * (part +1), len(message))]
            if part != 0:
                string_part = "..." + string_part
            if part is not max_iterations-1:
                string_part = string_part + "..."
            await interaction.followup.send(content=string_part, ephemeral=True)
    else:
        if not already_responded:
            await interaction.edit_original_response(content=message)
        else:
            await interaction.followup.send(content=message, ephemeral=True)
