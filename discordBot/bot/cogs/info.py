"""
Handles all commands for information
"""
import discord
from discord.ext import commands

from bot.database import DBConnector
from bot import utils


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def database(self):
        assert isinstance(self.bot.db, DBConnector)
        return self.bot.db

    async def info_compiler(self, ctx):
        guild_info = await self.database.get_guild_info(str(ctx.message.guild.id))
        if guild_info:
            embed = utils.Embed(title="Current Information")
            embed.add_field(name="Tournament", value=f"{guild_info.tournament_name}", inline=False)
            embed.add_field(name="Bracket Link(s)", value=f"{guild_info.bracket_link}", inline=False)
            for n in range(len(guild_info.current_comms)):
                x = guild_info.current_comms[n]
                embed.add_field(name=f"Comm {n + 1}",
                                value=f"```\nName: {x['name']}\n"
                                      f"Twitter: {x['twitter']}\n"
                                      f"Pronouns: {x['pronouns']}\n```",
                                inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=utils.Embed(title="Display Info Error", description=f"Guild has no data stored"))

    @commands.group(invoke_without_command=True)
    async def info(self, ctx):
        """Group of commands handling the guild/server info & setting."""
        await self.info_compiler(ctx)

    @info.command(aliases=["display"])
    async def display_info(self, ctx):
        """
        The current Commentator shown by bot
        """
        await self.info_compiler(ctx)

    @info.command(aliases=["setTournamentName", "tournamentname", "tournament"])
    async def set_tournament_name(self, ctx, *, arg):
        """
        Set tournament name
        """
        if await self.database.set_server_tournament_name(str(ctx.message.guild.id), arg):
            await ctx.message.add_reaction("👍")

    @info.command(aliases=["setBracketLink", "bracketlink", "bracket"])
    async def set_bracket_link(self, ctx, *, arg):
        """
        Set bracket link
        """
        if await self.database.set_server_bracket_link(str(ctx.message.guild.id), arg):
            await ctx.message.add_reaction("👍")


def setup(bot):
    bot.add_cog(Info(bot))
