import discord
import logging
import requests

import traceback
from discord import app_commands

from ..constants import HEADERS, GENERIC_ERROR_MESSAGE, SET_CHANNEL_MESSAGE
from ..helpers import getRaiderIOBaseUrlPerChar
from ..bot import client
from ..models import Character, Guild

@client.tree.command(name="character-add-user", description="Add a character to the M+ run tracking list and assign a discord user")
@app_commands.describe(
    character_name="Name of the character",
    realm="Realm of the character",
    user="Discord user the character belongs to"
)
async def add_user(interaction: discord.Interaction, character_name: str, realm: str, user: discord.User):
    try:
        await interaction.response.defer(thinking=True)

        guild: Guild = Guild.get_or_none(Guild.guild_id == interaction.guild.id)
        if guild.runs_channel_id is None:
            await interaction.edit_original_response(
            content=SET_CHANNEL_MESSAGE
            )
            return
        
        await add_character_func(interaction=interaction, character_name=character_name, realm=realm, user=user)
    except:
        await interaction.edit_original_response(
            content=GENERIC_ERROR_MESSAGE
        )
        logging.error(f"Adding character failed for {character_name}-{realm}")
        traceback.print_exc()


@client.tree.command(name="character-add", description="Add a character to the M+ run tracking list")
@app_commands.describe(
    character_name="Name of the character",
    realm="Realm of the character"
)
async def add(interaction: discord.Interaction, character_name: str, realm: str):
    try:
        
        await interaction.response.defer(thinking=True)

        guild: Guild = Guild.get_or_none(Guild.guild_id == interaction.guild.id)
        if guild.runs_channel_id is None:
            await interaction.edit_original_response(
            content=SET_CHANNEL_MESSAGE
            )
            return

        await add_character_func(interaction=interaction, character_name=character_name, realm=realm, user=interaction.user)
      
    except:
        await interaction.edit_original_response(
            content=GENERIC_ERROR_MESSAGE
        )
        logging.error(f"Adding character failed for {character_name}-{realm}")
        traceback.print_exc()

async def add_character_func(interaction: discord.Interaction, character_name: str, realm: str, user: discord.User):
    character_name = character_name
    realm = realm
    score = 0

    url = (
            f"{getRaiderIOBaseUrlPerChar(character_name, realm)}"
            "&fields=mythic_plus_scores_by_season%3Acurrent"
        )

    response = requests.get(url, headers=HEADERS)

    if not response.ok:
        await interaction.edit_original_response(
                content=f"Raider.io did not find a character by the name `{character_name}-{realm}`. 😢"
            )
        return

    char_info = response.json()
    score = char_info.get('mythic_plus_scores_by_season')[0].get('scores').get('all')
    char_name = char_info.get('name')
    char_realm = char_info.get('realm')

    if (db_entry := Character.get_or_none((Character.guild_id == interaction.guild.id) & (Character.name == char_name) & (Character.realm == char_realm))) is not None:
        db_entry: Character
        await interaction.edit_original_response(
        content=f"This character has already been added to the track list!"
        )
        return
    character: Character = Character.create(guild_id=interaction.guild.id, name=char_name, realm=char_realm, score=score, user_id=user.id)
    await interaction.edit_original_response(
        content=f"The character `{character.name}-{character.realm}` has been added to the track list and has been assigned to <@{character.user_id}>! 🎉"
        )


@client.tree.command(name="character-remove", description="Delete a character from the M+ run tracking list")
@app_commands.describe(
    character_name="Name of the character",
    realm="Realm of the character"
)
async def remove(interaction: discord.Interaction, character_name: str, realm: str):
    try:
        await interaction.response.defer(thinking=True)
        character_name = character_name.capitalize()
        realm = realm.title()

        if (db_entry := Character.get_or_none((Character.guild_id == interaction.guild.id) & (Character.name == character_name) & (Character.realm == realm))) is not None:
            db_entry: Character
            db_entry.delete_instance()
            await interaction.edit_original_response(
                content=f"The character `{character_name}-{realm}` has been removed from the list. 💥"
            )
        else:            
            await interaction.edit_original_response(
                content=f"We couldn't find `{character_name}-{realm}` on our list.")
    except:
        await interaction.edit_original_response(
            content=GENERIC_ERROR_MESSAGE
        )
        logging.error(f"Removing character failed for {character_name}-{realm}")
        traceback.print_exc()