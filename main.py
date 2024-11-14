"""
	Project name: Droptop Four Discord Bot
	Discord: https://discord.gg/hQGDm4F5Ef
	Author: Bunz (bunz#3066)
	Date created: 21/10/2022
	Bot Version: 4.2
	Python Version: 3.11.4
	Cogs: 5
"""

import json
import logging
import os
import re
import traceback
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from utils import (
    command_mention,
    date_time,
    initialize_firebase,
    initialize_logger,
    initialize_mongodb,
)

load_dotenv()

BOT_ENVIRONMENT = os.getenv("DEBUG", "True") == "True"

if BOT_ENVIRONMENT:
    load_dotenv(".env.local")
else:
    load_dotenv(".env.prod")

logger = logging.getLogger("main")

main_prefix = ()

bot = commands.Bot(
    command_prefix=main_prefix,
    intents=discord.Intents.all(),
    description="Official discord bot for the Droptop Four discord server",
    activity=discord.Activity(
        type=discord.ActivityType.listening, name="slash commands"
    ),
    strip_after_prefix=True,
    case_insensitive=True,
)

bot.launch_time = datetime.utcnow()

try:
    logger_status = initialize_logger(os.getenv("sentry_dsn"))
except Exception as e:
    logger_status = False
    logger.critical(f"Logger failed to initialize!\n{e}")

db_id, config_cluster = os.getenv("mongodb_id"), os.getenv("config_cluster")

db_status, bot.db_client = initialize_mongodb(db_id)

if db_status:
    db = bot.db_client[config_cluster]
    config_collection = db["Configs"]
    bot.configs = config_collection.find_one({}, {"_id": 0})

    firebase_status, firebase_error = initialize_firebase(
        json.loads(bot.configs["firebase_creds"])
    )

    bot.cari_logo = bot.configs["cari_logo"]
    bot.droptopfour_logo = bot.configs["droptopfour_logo"]
else:
    firebase_status = False
    firebase_error = "Database failed to initialize, so Firebase was not initialized."


@bot.event
async def on_ready():

    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    for guild in bot.guilds:
        logger.info("Connected to server: {}".format(guild))
    logger.info("------")


@bot.event
async def setup_hook():
    cogs = [
        "cogs.cog_admin",
        "cogs.cog_dev",
        "cogs.cog_mod",
        "cogs.cog_droptop",
        "cogs.cog_misc",
    ]

    for cog in cogs:
        await bot.load_extension(cog)
    bot.tree.clear_commands(guild=discord.Object(id=bot.configs["server_id"]))
    guild = await bot.tree.sync()
    for synced in guild:
        command = bot.tree.get_command(synced.name, type=synced.type)
        if command is None:
            continue
        command.extras["mention"] = synced.mention
        if isinstance(command, app_commands.Group):
            for child in command.walk_commands():
                child.extras["mention"] = command_mention(
                    child.qualified_name, synced.id
                )
        if command.name == "solved":
            bot.solved_command = command_mention(child.qualified_name, synced.id)


@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    if re.fullmatch(rf"<@!?{bot.user.id}>", msg.content):
        return await msg.channel.send(
            "You can use me with slash commands now!\nType `/` to see a list of possible commands."
        )
    return await bot.process_commands(msg)


@bot.event
async def on_thread_create(thread):
    if thread.parent.id == bot.configs["help_bug_report_channel"]:
        await thread.add_tags(discord.Object(bot.configs["unsolved_forum_tag"]))
        await thread.starter_message.pin()
        msg = await thread.send(
            f"To close this message use {command_mention('solved', 1078282304876707891)}"
        )
        await msg.pin()


@bot.event
async def on_app_command_completion(interaction, command):
    channel = bot.get_channel(bot.configs["commandlog_channel"])

    embed = discord.Embed(title="Command")
    embed.add_field(name="User", value=f"<@{interaction.user.id}>", inline=False)
    embed.add_field(name="Channel", value=f"<#{interaction.channel_id}>", inline=False)
    embed.add_field(name="Command", value=f"{command.qualified_name}", inline=False)
    embed.add_field(
        name="Command mention", value=f"{command.extras['mention']}", inline=False
    )
    params = []
    for parameter in interaction.namespace:
        params.append(parameter)
    embed.add_field(name="Params", value=f"{params}", inline=False)

    await channel.send(embed=embed)

    logger.info(
        f"User: <@{interaction.user.id}>; Channel: <#{interaction.channel_id}>; Command: {command.qualified_name}; Params: {params}"
    )


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {error}")

    channel = bot.get_channel(bot.configs["commandlog_channel"])

    embed = discord.Embed(title="!!ERROR!!", color=discord.Color.from_rgb(255, 0, 0))
    embed.add_field(name="User", value=f"<@{ctx.author.id}>", inline=False)
    embed.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)
    embed.add_field(name="Command", value=f"{ctx.command.qualified_name}", inline=False)
    embed.add_field(
        name="Command mention", value=f"{ctx.command.extras['mention']}", inline=False
    )
    params = []
    for parameter in ctx.args:
        params.append(parameter)
    embed.add_field(name="Params", value=f"{params}", inline=False)
    embed.add_field(name="Error", value=error, inline=False)
    traceback_str = "".join(traceback.format_tb(error.__traceback__))
    embed.add_field(
        name="Traceback", value=f"```fix\n{traceback_str}\n```", inline=False
    )

    await channel.send(embed=embed)

    logger.error(
        f"User: <@{ctx.author.id}>; Channel: <#{ctx.channel.id}>; Command: {ctx.command.qualified_name}; Params: {params}; Error: {error}; Traceback: {traceback_str}"
    )


@bot.tree.error
async def on_tree_error(interaction, error):
    try:
        await interaction.response.send_message(f"Error: {error}", ephemeral=True)
    except discord.InteractionResponded:
        await interaction.followup.send(f"Error: {error}", ephemeral=True)

    channel = bot.get_channel(bot.configs["commandlog_channel"])

    embed = discord.Embed(title="!!ERROR!!", color=discord.Color.from_rgb(255, 0, 0))
    embed.add_field(name="User", value=f"<@{interaction.user.id}>", inline=False)
    embed.add_field(name="Channel", value=f"<#{interaction.channel_id}>", inline=False)
    embed.add_field(
        name="Command", value=f"{interaction.command.qualified_name}", inline=False
    )
    embed.add_field(
        name="Command mention",
        value=f"{interaction.command.extras['mention']}",
        inline=False,
    )
    params = []
    for parameter in interaction.namespace:
        params.append(parameter)
    embed.add_field(name="Params", value=f"{params}", inline=False)
    embed.add_field(name="Error", value=error, inline=False)
    traceback_str = "".join(traceback.format_tb(error.__traceback__))
    embed.add_field(
        name="Traceback", value=f"```fix\n{traceback_str}\n```", inline=False
    )

    await channel.send(embed=embed)
    logger.error(
        f"User: <@{interaction.user.id}>; Channel: <#{interaction.channel_id}>; Command: {interaction.command.qualified_name}; Params: {params}; Error: {error}; Traceback: {traceback_str}"
    )


if db_status and firebase_status and logger_status:
    logger.info("Bot is ready to start")

    if not os.path.exists("tmp"):
        os.makedirs("tmp")
        logger.info("Created temp folder")
        with open(os.path.join("tmp", "placeholder"), "w") as fp:
            pass
        logger.info("Created placeholder file")

    try:
        bot.run(bot.configs["discord_token"])
    except discord.HTTPException as e:
        if e.status == 429:
            logger.warning("Rate limit detected. Restarting...")
            os.kill(1, 1)
        logger.warning(e)
else:
    logger.warning("Bot is not ready")
    if not db_status:
        logger.warning("MongoDB is not ready")
    if not firebase_status:
        logger.warning("Firebase is not ready")
    if not logger_status:
        logger.warning("Logger is not ready")
