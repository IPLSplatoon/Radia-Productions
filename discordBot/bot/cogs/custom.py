"""
Handles all commands for custom Twtich Commands
"""
from discord.ext import commands

from bot import utils
from bot.database import DBConnector

# Stores the predefined commands on the Twitch bot
predefined_commands = [
    "discord_link",
    "discord",
    "bracket_link",
    "bracket",
    "tournament",
    "mic",
    "commentators",
    "uptime"
]


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def database(self):
        assert isinstance(self.bot.db, DBConnector)
        return self.bot.db

    @commands.group()
    async def custom(self, ctx):
        """Group of commands handling the custom Twitch commands."""

    @custom.command(aliases=["add"])
    async def add_command(self, ctx, command_name: str, command_message: str):
        """
        Add custom command for server's Twitch Channel
        """
        if command_name in predefined_commands:  # Check if command is not already defined
            await ctx.send(embed=utils.Embed(title="Added Twitch Command Error",
                                             description=f"Can not override a pre-existing command"))
            return
        try:
            if await self.database.add_custom_command(str(ctx.message.guild.id), command_name, command_message):
                embed = utils.Embed(title="Added Twitch Command")
                embed.add_field(name=command_name, value=command_message, inline=False)
                await ctx.send(embed=embed)
                return
        except Exception as err:
            await ctx.send(embed=utils.Embed(title="Error", description=f"```\n{err}\n```"))
            pass

    @custom.command(aliases=["remove"])
    async def remove_command(self, ctx, command_name: str):
        """
        Remove custom command for server's Twitch Channel
        """
        try:
            if await self.database.remove_custom_command(str(ctx.message.guild.id), command_name):
                embed = utils.Embed(title="Removed Twitch Command", description=f"Removed command `{command_name}`")
                await ctx.send(embed=embed)
                return
        except Exception as err:
            await ctx.send(embed=utils.Embed(title="Error", description=f"```\n{err}\n```"))
            pass

    @custom.command(aliases=["list"])
    async def list_commands(self, ctx):
        """
        View custom commands for server's Twitch channel.
        """
        guild_info = await self.database.get_guild_info(str(ctx.message.guild.id))
        if guild_info:
            embed = utils.Embed(title=f"Custom Commands for {guild_info.twitch_channel}")
            for com in guild_info.get_all_commands():
                embed.add_field(name=com.name, value=com.message, inline=False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Custom(bot))
