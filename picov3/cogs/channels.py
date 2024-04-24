import discord
import logging

from ..models import Guild
from discord import app_commands

from ..bot import client

@client.tree.command(
    name="set-runs-channel",
    description="Set the default channel for the bot to post M+ run updates in.",
)
@app_commands.describe(
     channel="A text channel."
)
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer(thinking=True, ephemeral=True)
    if (db_entry := Guild.get_or_none(Guild.guild_id == channel.guild.id)) is not None:
        db_entry: Guild
        db_entry.runs_channel_id = channel.id
        db_entry.save()
    else:
        Guild.create(guild_id=channel.guild.id, runs_channel_id=channel.id)
    await interaction.edit_original_response(
        content=f"Set the default M+ runs channel to <#{channel.id}>!"
    )

    
@client.tree.command(
    name="set-scores-channel",
    description="Set the default channel for the bot to post score achievements in.",
)
@app_commands.describe(
     channel="A text channel."
)
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer(thinking=True, ephemeral=True)
    if (db_entry := Guild.get_or_none(Guild.guild_id == channel.guild.id)) is not None:
        db_entry: Guild
        db_entry.score_channel_id = channel.id
        db_entry.save()
    else:
        Guild.create(guild_id=channel.guild.id, score_channel_id=channel.id)
    await interaction.edit_original_response(
        content=f"Set the default score achievments channel to <#{channel.id}>!"
    )