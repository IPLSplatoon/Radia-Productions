"""
Initializes the bot

This includes importing the bot, loading the cogs, setting the prefix, etc.
"""

import os
import logging

from discord import Intents

from bot import cogs
from bot.bot import Bot

if not (mongo_uri := os.getenv("MONGODBURI")):
    logging.error("static.env - 'MONGODBURI' key not found. Cannot start bot.")
    raise EnvironmentError

if not (debug := os.getenv("DEBUG")):
    redis_url = "redis://redis:6379"
elif debug == "1":
    if not (redis_url := os.getenv("REDISURL")):
        redis_url = "redis://redis:6379"
else:
    redis_url = "redis://redis:6379"

# Create Bot
intents = Intents.default()
intents.members = True
bot = Bot(mongo_uri=mongo_uri, redis_url=redis_url,
          command_prefix="!" if not os.getenv("DEBUG") else "^", intents=intents)

# Load Cogs
for cog in cogs.names:
    try:
        bot.load_extension("bot.cogs." + cog)
        logging.debug("Loaded cogs.%s", cog)
    except Exception as e:
        logging.warning("Failed to load cogs.%s", cog)
        logging.error(type(e).__name__, e)

# Run Bot
if not (token := os.getenv("DISCORDTOKEN")):
    logging.error("static.env - 'DISCORDTOKEN' key not found. Cannot start bot.")
    raise EnvironmentError

bot.run(token)
