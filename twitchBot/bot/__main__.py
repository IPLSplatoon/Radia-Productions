"""
Initializes the bot

This includes importing the bot, loading the cogs, setting the prefix, etc.
"""

import os
import logging

from bot import cogs
from bot.bot import Bot

if not (mongo_uri := os.getenv("MONGODBURI")):
    logging.error("static.env - 'MONGODBURI' key not found. Cannot start bot.")
    raise EnvironmentError

if not (twitch_client_id := os.getenv("TWITCHCLIENTID")):
    logging.error("static.env - 'TWITCHCLIENTID' key not found. Cannot start bot.")
    raise EnvironmentError

if not (twitch_oauth := os.getenv("TWITCHOAUTH")):
    logging.error("static.env - 'TWITCHOAUTH' key not found. Cannot start bot.")
    raise EnvironmentError

if not (twitch_nick := os.getenv("TWITCHNICK")):
    logging.error("static.env - 'TWITCHNICK' key not found. Cannot start bot.")
    raise EnvironmentError

if not (twitch_channels_string := os.getenv("TWITCHCHANNELS")):
    logging.error("static.env - 'TWITCHCHANNELS' key not found. Cannot start bot.")
    raise EnvironmentError

if not (debug := os.getenv("DEBUG")):
    redis_url = "redis://redis:6379"
elif debug == "1":
    if not (redis_url := os.getenv("REDISURL")):
        redis_url = "redis://redis:6379"
else:
    redis_url = "redis://redis:6379"

# Forms list of channels
channels = []
for c in twitch_channels_string.split(','):
    channels.append(c)

# Create Bot
bot = Bot(irc_token=twitch_oauth, client_id=twitch_client_id, nick=twitch_nick, initial_channels=channels,
          mongo_uri=mongo_uri, redis_url=redis_url, command_prefix="!" if not os.getenv("DEBUG") else "^")

for cog in cogs.names:
    bot.load_module("bot.cogs." + cog)

# Start bot
bot.run()
