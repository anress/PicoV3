import discord
import logging
import string

import traceback
from discord import app_commands

from ..constants import GENERIC_ERROR_MESSAGE
from ..helpers import send_long_message
from ..bot import client
from ..models import Character

@client.tree.command(name="list", description="Print a list of tracked characters that are assigned to you")
async def list(interaction: discord.Interaction):
    try:
        await interaction.response.defer(thinking=True)

        character_string = "Your characters:\n\n"
        for db_entry in Character.select().where((Character.guild_id == interaction.guild.id) & (Character.user_id == interaction.user.id)).order_by(Character.realm):
            db_entry: Character
            emojiString = ""
            if db_entry.emoji_id:
                emojiString = f" <:{db_entry.emoji_name}:{db_entry.emoji_id}> "
            character_string = character_string + f"- `{db_entry.name}-{string.capwords(db_entry.realm.replace('-', ' '))}` {emojiString}\n"
        await send_long_message(message=character_string, interaction=interaction)
       
    except:
        await interaction.edit_original_response(
            content=GENERIC_ERROR_MESSAGE
        )
        logging.error(f"Listing characters failed for user {interaction.user.id} - {interaction.user.display_name}")
        traceback.print_exc()

@client.tree.command(name="list-all", description="Print a list of all tracked characters")
async def listAll(interaction: discord.Interaction):
    try:
        await interaction.response.defer(thinking=True)

        character_string = "Pico is tracking the following characters:\n\n"
        for db_entry in Character.select().where(Character.guild_id == interaction.guild.id).order_by(Character.realm):
            db_entry: Character
            emojiString = ""
            if db_entry.emoji_id:
                emojiString = f" <:{db_entry.emoji_name}:{db_entry.emoji_id}> "
            character_string = character_string + f"- `{db_entry.name}-{string.capwords(db_entry.realm.replace('-', ' '))}`  {emojiString} <@{db_entry.user_id}>\n"
        await send_long_message(message=character_string, interaction=interaction)
    except:
        await interaction.edit_original_response(
            content=GENERIC_ERROR_MESSAGE
        )
        logging.error(f"Listing characters failed for user {interaction.user.id} - {interaction.user.display_name}")
        traceback.print_exc()
