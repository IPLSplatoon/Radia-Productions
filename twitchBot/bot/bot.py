"""
Holds the custom Bot subclass.
"""
import logging

from twitchio.ext import commands
from .database import DBConnector


class Bot(commands.Bot):

    def __init__(self, irc_token: str, client_id: str, nick: str, command_prefix: str,
                 initial_channels: list, mongo_uri: str, redis_url: str):
        self.db = DBConnector(mongo_uri, "radiaTwitch", redis_url)

        super().__init__(irc_token=irc_token, client_id=client_id, nick=nick, prefix=command_prefix,
                         initial_channels=initial_channels)

    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            # If the command is not a present system command, then we check if a custom command exists
            channel_data = await self.db.get_twitch_info(str(ctx.channel.name))
            custom_command = channel_data.retrieve_custom_command(str(ctx.message.clean_content))
            if custom_command:  # If the custom command exists then we send to the user
                await ctx.send(custom_command.message)
            return  # We ignore this kind of error so Sentry doesn't capture it
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You're missing fields needed for command")
        else:
            logging.error(error)
            raise error

    async def event_ready(self):
        logging.info("Logged in as: %s", self.nick)
