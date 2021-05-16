"""
Holds the custom Bot subclass.
"""
import logging

from twitchio.ext import commands
from .mongo import MongoConnector


class Bot(commands.Bot):

    def __init__(self, irc_token: str, client_id: str, nick: str, command_prefix: str,
                 initial_channels: list, mongo_uri: str):
        self.mongo = MongoConnector(mongo_uri, "radiaTwitch")  # Used for MongoDb

        super().__init__(irc_token=irc_token, client_id=client_id, nick=nick, prefix=command_prefix,
                         initial_channels=initial_channels)

    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            return
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You're missing fields needed for command")
        else:
            logging.error(error)
            raise error

    async def event_ready(self):
        logging.info("Logged in as: %s", self.nick)
