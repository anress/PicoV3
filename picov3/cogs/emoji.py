import discord
import logging
import requests

import traceback
from discord import app_commands
from PIL import Image
import urllib.request
import io
from unidecode import unidecode

from ..constants import HEADERS, GENERIC_ERROR_MESSAGE
from ..helpers import getRaiderIOBaseUrlPerChar, normalizeRealmName
from ..bot import client
from ..models import Character

@client.tree.command(name="emoji-add", description="Add a custom emoji of a character")
@app_commands.describe(
    character_name="Name of the character",
    realm="Realm of the character"
)
async def add(interaction: discord.Interaction, character_name: str, realm: str):
    try:
        await interaction.response.defer(thinking=True)

        emojiLimit = interaction.guild.emoji_limit
        emojisCount = len(interaction.guild.emojis)

        # if emojisCount+10 >= emojiLimit:
        # owner = interaction.guild.owner   
        # print(interaction.guild.owner_id)
        # own = discord.User(id=interaction.guild.owner_id)
        # print(own)        
        # dmChannel = await client.create_dm()
        # await dmChannel.send(content=f"Hi! Your server has reached {emojisCount}/{emojiLimit} emojis. Maybe time to sort out a few? 🤔")
        if emojisCount == emojiLimit:           
            premiumTier = interaction.guild.premium_tier
            await interaction.edit_original_response(
            content="**Oh no!** We reached the emoji limit 🫠 "
            f"Your server mod {owner.nick} has been informed 👍\n\n"
            "However, feel free to take matters in your own hands and **increase" 
            " the emoji limit** by supporting the server with a boost to reach "
            f"Level {premiumTier + 1}"               
            )
            return

        character_name = character_name.capitalize()
        realm = normalizeRealmName(realm)

        response = requests.get(getRaiderIOBaseUrlPerChar(character_name, realm), headers=HEADERS)

        if not response.ok:
            await interaction.edit_original_response(
                    content=f"Raider.io did not find a character by the name `{character_name}-{realm}`. 😢"
                )
            return
        
        image_url = response.json().get('thumbnail_url')
        with urllib.request.urlopen(image_url) as url:
            img = Image.open(url)
            resizedImg = img.resize((128, 128))
            img_byte_arr = io.BytesIO()
            resizedImg.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

        emojiName = "char" + unidecode(character_name)
        
        existing = [emoji for emoji in interaction.guild.emojis if emoji.name == emojiName]
        for emoji in existing:
            await interaction.guild.delete_emoji(emoji)
        
        emoji = await interaction.guild.create_custom_emoji(name=emojiName, image=img_byte_arr)
        
        await interaction.edit_original_response(content=f"Added Emoji of **{character_name}**! {emoji} \n\n"
            f"✨  *Use it by typing* `:{emojiName}:`! ✨")
    
        if (db_entry := Character.get_or_none((Character.guild_id == interaction.guild.id) & (Character.name == character_name) & (Character.realm == realm))) is not None:
            db_entry: Character
            db_entry.emoji_id = emoji.id
            db_entry.emoji_name = emojiName
            db_entry.save()

    except:
        await interaction.edit_original_response(
            content=GENERIC_ERROR_MESSAGE
        )
        logging.error(f"Adding emoji failed for {character_name}-{realm}")
        traceback.print_exc()


@client.tree.command(name="emoji-remove", description="Remove the custom emoji of a character")
@app_commands.describe(
    character_name="Name of the character"
)
async def remove(interaction: discord.Interaction, character_name: str):
    try:
        await interaction.response.defer(thinking=True) 
        character_name = character_name.capitalize()

        emojiName = "char" + unidecode(character_name)
        existing = [emoji for emoji in interaction.guild.emojis if emoji.name == emojiName]
        for emoji in existing:
            if (db_entry := Character.get_or_none((Character.guild_id == interaction.guild.id) & (Character.emoji_id == emoji.id))) is not None:
                db_entry: Character
                db_entry.emoji_id = None
                db_entry.emoji_name = None
            
            await interaction.guild.delete_emoji(emoji)
        await interaction.edit_original_response(content=f"Deleted Emoji of {character_name}! 💥")
    except:
        await interaction.edit_original_response(
            content=GENERIC_ERROR_MESSAGE
        )
        logging.error(f"Deleting emoji of {character_name} failed")
        traceback.print_exc()


