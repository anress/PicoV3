import discord
import logging
import requests

import traceback
from discord import app_commands

from ..constants import HEADERS, GENERIC_ERROR_MESSAGE
from ..helpers import colorToNumber, getRaiderIOBaseUrlPerChar, hasHealerSpec, hasTankSpec, nameToSlug, getSpecName
from ..bot import client

import json

@client.tree.command(name="score", description="Get the current M+ scores for a character.")
@app_commands.describe(
    character_name="Name of the character",
    realm="Realm of the character"
)
async def score(interaction: discord.Interaction, character_name: str, realm: str):
    try:
        
        await interaction.response.defer(thinking=True)
    
        character_name = character_name
        realm = realm

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
  
        character_infos = response.json()
        class_name = character_infos.get("class")
        segments = character_infos.get('mythic_plus_scores_by_season')[0].get('segments')

        
        scores = f"**Overall:** `{segments.get('all').get('score')}`\n---\n"

        scores = scores + f"**DPS:** `{segments.get('dps').get('score')}`\n"

        if hasHealerSpec(class_name):
            scores = scores + f"**Healer:** `{segments.get('healer').get('score')}`\n"

        if hasTankSpec(class_name):
            scores = scores + f"**Tank:** `{segments.get('tank').get('score')}`\n"

        
        scores = scores + f"\n\n*{getSpecName(class_name, 'spec_0')}:* `{segments.get('spec_0').get('score')}`\n"
        scores = scores + f"*{getSpecName(class_name, 'spec_1')}:* `{segments.get('spec_1').get('score')}`\n"

        if class_name != "Demon Hunter":
            scores = scores + f"*{getSpecName(class_name, 'spec_2')}:* `{segments.get('spec_2').get('score')}`\n"        
        
        if class_name == "Druid":
            scores = scores + f"*{getSpecName(class_name, 'spec_3')}:* `{segments.get('spec_3').get('score')}`\n"
        
        color = colorToNumber(segments.get('all').get('color'))
       
        profile_url = character_infos.get('profile_url')
        scores = scores + "\n" + profile_url

        embed: discord.Embed = discord.Embed(title=f"M+ scores for `{character_name}-{nameToSlug(realm)}`", description=scores, color=color)
        embed.set_image(url=character_infos.get("thumbnail_url"))
                       
        await interaction.edit_original_response(embed=embed)

        with open('some_file.json', 'w') as f:
            json.dump(character_infos, f, indent=4)    

    except:
        await interaction.edit_original_response(
            content=GENERIC_ERROR_MESSAGE
        )
        logging.error(f"Adding character failed for {character_name}-{realm}")
        traceback.print_exc()

