"""Misc cog."""

from random import randint

import discord
from discord.ext import commands

from bot import utils


class Misc(commands.Cog):
    """All the miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['🏓'])
    async def ping(self, ctx):
        """Get the latency of the bot."""
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: `{round(self.bot.latency*1000)}ms`", color=0xde2e43)
        await ctx.send(embed=embed)

    @commands.command()
    async def pet(self, ctx, num: int = None):
        """Get a picture of a pet."""
        embed = utils.Embed(title="Pets!")
        embed.set_image(url=f"https://cdn.vlee.me.uk/TurnipBot/pets/{num if num else randint(0, 140)}.png")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
