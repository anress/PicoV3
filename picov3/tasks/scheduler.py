import datetime
from dateutil import parser
import discord
from discord.ext import commands, tasks

import aiohttp
import traceback
import logging
import json

import requests
from ..models import Guild, Character, MPlusRun, CharacterRun
from ..constants import RAIDER_IO_BASE_URL, HEADERS, LINK_BASE_URL
from ..helpers import getRaiderIOBaseUrlPerChar, getEmbedColorForKeystoneLevel, getRoleEmoji, getPercentRemainingString, date_formatter, format_ms, checkIfNewMilestone, colorToNumber

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

class Scheduler:
    def __init__(self, client):
        self.client = client
        self.fetch_runs.start()

    def cog_unload(self):
        self.fetch_runs.start()

    @tasks.loop(minutes=20)
    async def fetch_runs(self):
        print("My task is running!")
        logging.info("This runs!")
        try:
            logging.info("Checking for new M+ runs")
           
            for db_entry_guild in Guild.select():
                db_entry_guild: Guild
                if db_entry_guild.runs_channel_id is not None:                 
                    logging.info(f"Guild: {db_entry_guild.guild_id}")   
                    guild: discord.Guild = await self.client.fetch_guild(db_entry_guild.guild_id)
                    runs_channel: discord.TextChannel = await guild.fetch_channel(db_entry_guild.runs_channel_id)
                    for db_entry in Character.select().where(Character.guild_id == db_entry_guild.guild_id):
                        db_entry: Character
                        
                        logging.info("---- " + db_entry.name + " ----")
                        await get_recent_mplus_runs(db_entry, runs_channel, db_entry_guild.guild_id)
                        season = "season-tww-3"
                        url = (f"{getRaiderIOBaseUrlPerChar(db_entry.name, db_entry.realm)}"
                                f"&fields=mythic_plus_scores_by_season{season}"
                            )

                        response = requests.get(url, headers=HEADERS)

                        if response.ok:
                            score_all = response.json().get('mythic_plus_scores_by_season')[0].get('segments').get('all')
                            score_new = score_all.get('score')
                            score_old = db_entry.score
                            
                            if db_entry_guild.score_channel_id is not None:                                
                                score_channel: discord.TextChannel = await guild.fetch_channel(db_entry_guild.score_channel_id)
                                logging.info(f"Score old: {score_old}")
                                logging.info(f"Score new: {score_new}")
                                if score_old is None:
                                    score_old = 0
                                # achievement = checkIfNewMilestone(score_old, score_new)
                                # if achievement is not None:
                                    # embed = createScoreEmbed(response.json(), db_entry, achievement, score_all)                                    
                                    # await score_channel.send(embed=embed) 
                            db_entry.score = score_new
                            db_entry.save()
            logging.info("Finished checking all characters")
                                                    
        except:                           
            logging.error(f"Unexpected error in message loop")   
            traceback.print_exc()      

async def get_recent_mplus_runs(character: Character, channel: discord.TextChannel, guild_id):
    url = f"{RAIDER_IO_BASE_URL}&realm={character.realm}&name={character.name}&fields=mythic_plus_recent_runs"
    async with aiohttp.ClientSession() as session:
        for retries in range(3):
            async with session.get(url, headers=HEADERS) as response:
                try:
                    response_json = await response.json()
                    break
                except:
                    logging.error(
                        f"raider.io returned status code {response.status} when "
                        f"querying {character.name}, retrying ..."
                    )
        else:
            logging.error(f"{character.name} could not be parsed due to raider.io error. continuing.")
            return []
        lastTenRuns = response_json.get('mythic_plus_recent_runs')
        if lastTenRuns is None:
            return []
        runs = []
        for run in reversed(lastTenRuns):
            try:
                link = run.get('url')
                url_parts = link.split("/")
                season = url_parts[4]
                run_id = url_parts[5].split("-")[0]                
                
                # check if run hasn't been previously posted already
                if (db_entry_run := MPlusRun.get_or_none((MPlusRun.guild_id == character.guild_id) & (MPlusRun.run_id == run_id))) is None:                    
                    logging.info(f"Adding run {run_id}")
                    url = f"{LINK_BASE_URL}/api/v1/mythic-plus/run-details?season={season}&id={run_id}"
                    response = requests.get(url, headers=HEADERS)
                    if not response.ok:
                        logging.error("Couldnt fetch run details")
                    else:
                        embed = generate_run_embed(response.json(), link, guild_id)
                        mentions = discord.AllowedMentions(users=False)
                        await channel.send(embed=embed, allowed_mentions=mentions)  
            except:
                logging.error(f"Unexpected Error for run {link}")
                traceback.print_exc()    
        return runs

def generate_run_embed(mplusrun, url, guild_id):

    # times
    keystone_level = mplusrun.get('mythic_level')
    keystone_time_ms = mplusrun.get('keystone_time_ms')
    clear_time_ms = mplusrun.get('clear_time_ms')
    time_remaining_ms = mplusrun.get('time_remaining_ms') # negative when not timed
  
    percent = getPercentRemainingString(time_remaining_ms, keystone_time_ms)

    keystone_time_formatted = format_ms(keystone_time_ms)
    clear_time_formatted = format_ms(clear_time_ms)

    # score and chests
    num_chests = mplusrun.get('num_chests')
    score = mplusrun.get('score')

    # date
    completed_at = mplusrun.get('completed_at')

    dateTimeObj = parser.parse(completed_at)          
    date_time = date_formatter(dateTimeObj)          

    # dungeon infos
    dungeon = mplusrun.get('dungeon')
    dungeon_slug = dungeon.get('slug')
    dungeon_name = dungeon.get('name')
    dungeon_expansion = dungeon.get('expansion_id')
    dungeon_image =  f"https://cdnassets.raider.io/images/dungeons/expansion{dungeon_expansion}/base/{dungeon_slug}.jpg"

    season = mplusrun.get('season')
    keystone_run_id = mplusrun.get('keystone_run_id')


    MPlusRun.create(guild_id = guild_id, run_id=keystone_run_id, season=season, dungeon_name=dungeon_slug, key_level=keystone_level)

    # embed texts
    title = f"New M+ Run! +{keystone_level}: {dungeon_name}"

    embed_text = f"Cleared in {clear_time_formatted} of {keystone_time_formatted} "

    if num_chests > 0:
        embed_text = embed_text + f"({percent} % remaining - keystone level upgraded by {num_chests})"
    else:
        embed_text = embed_text + f"({percent} % over)"
    
    embed_text = embed_text + f" for {score} points."

    # characters in run group
    group_comp = ""
    dps = ""
    healer = ""
    tank = ""

    for character in mplusrun.get('roster'):
        char = character.get('character')

        name = char.get('name')
        realm = char.get('realm').get('name')
 
        tracked_char = ""

        if (db_entry := Character.get_or_none((Character.guild_id == guild_id) & (Character.name == name) & (Character.realm == realm))) is not None:
            db_entry: Character
            
            if db_entry.emoji_id:
                tracked_char = f" <:{db_entry.emoji_name}:{db_entry.emoji_id}> "

            if db_entry.user_id:                
                tracked_char = tracked_char + f" - <@{db_entry.user_id}>"
            character_run: CharacterRun = CharacterRun.create(run_id=keystone_run_id, character_id=db_entry.id, guild_id=guild_id)

        
        char_url = f"https://raider.io" + char.get('path')
        spec = char.get('spec').get('name')
        wow_class = char.get('class').get('name')

        role = character.get('role')
        role_emoji = getRoleEmoji(role)
        ilvl = character.get('items').get('item_level_equipped')
        score = character.get('ranks').get('score')
        guild = ""

        if character.get('guild') is not None:
            if character.get('guild').get('id') == 1909321: # lobster guild id
                guild = " 🦞"
        character_infos =  f" {role_emoji} [{name}]({char_url}){tracked_char}{guild}\n{spec} {wow_class} - {ilvl} ilvl - **{score}** Score\n\n"
        if role == "dps":
            dps = dps + character_infos
        if role == "tank":
            tank = character_infos
        if role == "healer":
            healer = character_infos
    
    group_comp = tank + dps + healer

    affixes = ""
    for affix in mplusrun.get('weekly_modifiers'):
        affixes = affixes + " " + affix.get('name')
    
    deaths = "-"
    if mplusrun.get('logged_details') is not None:
        deaths = len(mplusrun.get('logged_details').get('deaths'))
    
    embed: discord.Embed = discord.Embed(title=title, description=embed_text, color=getEmbedColorForKeystoneLevel(keystone_level), url=url)
    
    embed.add_field(name="Date and time of run", value=date_time, inline=False)
    embed.add_field(name="Group", value=group_comp, inline=False)
    embed.add_field(name="Deaths", value=deaths, inline=True)
    embed.add_field(name="Affixes", value=affixes, inline=True)
    embed.set_image(url=dungeon_image)

    embed.set_footer(text="Powered by anjress", icon_url="https://anja.codes/logo192.png")
    return embed
   
def createScoreEmbed(response, character: Character, achievement, score_all):
    
    embed_text = f"<@{character.user_id}>'s {response.get('active_spec_name')} {response.get('class')} **[{response.get('name')}]({response.get('profile_url')})** just hit **{score_all.get('score')}** Score! \n\n Congrats on \n# {achievement} 🥳"
    embed: discord.Embed = discord.Embed(title="New M+ Milestone!", description=embed_text, color=colorToNumber(score_all.get('color')))
    
    embed.set_image(url=response.get('thumbnail_url'))
    return embed


    