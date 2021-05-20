"""Holds the custom Bot subclass."""

import random
import logging

import discord
from discord.ext import commands, tasks

from bot import utils
from .database import DBConnector


class Bot(commands.Bot):

    db: DBConnector

    def __init__(self, mongo_uri: str, redis_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_command = utils.HelpCommand()
        self.db = DBConnector(mongo_uri, "radiaTwitch", redis_url)  # Used for MongoDb

    async def on_ready(self):
        logging.info("Logged in as: %s", self.user.name)
        self.update_presence.start()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=utils.Embed(
                title=f"Error: **Missing Required Argument: '{error.param.name}'**",
                description=f"You can use `{ctx.prefix}help {ctx.command.full_parent_name} {ctx.command.name}` for help."))
        elif isinstance(error, (commands.CommandNotFound, commands.MissingRole)):
            return
        else:
            logging.error(error)
            raise error

    @tasks.loop(minutes=1)
    async def update_presence(self):
        """Loop to update the bot presence by selecting one of the strings at random."""
        await self.change_presence(activity=discord.Game(random.choice([
            "Powered by High Ink!",
            "Investing in buying LUTI.",
            "Get your coffee grounds 45% off this weekend at Testing Grounds.",
            "Sink or Swim or Swim or Sink",
            "According to all known laws of aviation",
            # Round 4
            "Round 4, here we go again!",
            "The real round 4 were the friends we made along the way.",
            # uwu stuff
            "Sprinkles!",
            "Wawa!",
        ])))
