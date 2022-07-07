"""
Handles all commands for commentators
"""
import discord
from discord.ext import commands
import re

from bot.database import DBConnector
from bot import utils

discord_mention = re.compile(r"<@!(\d+)>")


class Commentators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def database(self):
        assert isinstance(self.bot.db, DBConnector)
        return self.bot.db

    @commands.group(aliases=["commentator", "comms"])
    async def commentators(self, ctx):
        """Group of commands handling the commentators info."""

    @commentators.command(aliases=["setProfile", "setprofile"])
    async def set_profile(self, ctx, name: str, twitter: str, pronouns: str):
        """
        Set your commentator profile for stream
        """
        try:
            if twitter[0] == "@":  # If the user add @, remove it from string
                twitter = twitter[1:]
            elif "https://twitter.com/" in twitter:  # if they gave the full link, remove the link portion
                twitter = twitter.replace("https://twitter.com/home", "")
            elif re.search(discord_mention, twitter):
                await ctx.send(embed=utils.Embed(title="Set Commentator Twitter Handle Error!",
                                                 description=f"You Twitter handle contains a Discord mention!\n"
                                                             f"Try the command again without the `@` in your "
                                                             f"Twitter handle"))
                return
            response = await self.database.set_comms_info(str(ctx.message.author.id), name, twitter, pronouns)
            if response:
                embed = utils.Embed(title=f"Set Commentator Profile", description="We've set your profile")
                embed.add_field(name="Name", value=f"{name}", inline=False)
                embed.add_field(name="Twitter", value=f"@{twitter}", inline=False)
                embed.add_field(name="Pronouns", value=f"{pronouns}", inline=False)
                await ctx.send(embed=embed)
        except Exception as err:
            await ctx.send(embed=utils.Embed(title="Error", description=f"```\n{err}\n```"))
            pass

    @commentators.command()
    async def profile(self, ctx, profile=None):
        """
        View profile for yourself or a server member
        """
        if profile:
            if re.match(r"<@!(\d+)>", profile):
                query = await self.database.get_comms_info(profile[3:-1])
                description = f"Commentator profile for {profile}"
            else:
                query = await self.database.get_comms_info(profile)
                description = f"Commentator profile for <@!{profile}>"
        else:
            query = await self.database.get_comms_info(str(ctx.message.author.id))
            description = f"Your Commentator profile"
        if query:
            embed = utils.Embed(title="Commentator Profile", description=f"{description}")
            embed.add_field(name="Name", value=f"{query.name}", inline=False)
            embed.add_field(name="Twitter", value=f"@{query.twitter}", inline=False)
            embed.add_field(name="Pronouns", value=f"{query.pronouns}", inline=False)
            embed.add_field(name="No Show", value=f"{query.no_show}")
            embed.add_field(name="No Alert", value=f"{query.no_alert}")
            await ctx.send(embed=embed)
            return
        else:
            await ctx.send(embed=utils.Embed(title="No Profile Found",
                                             description="Query has no commentator profile"))
            return

    @commentators.command(aliases=["setNoShow", "setnoshow"])
    async def set_no_show(self, ctx, no_show: str):
        """
        Set the no show, to avoid showing on commentators details
        """
        if no_show.upper() in ["TRUE", "YES"]:
            response = await self.database.set_comms_no_show(str(ctx.message.author.id), True)
            try:
                if response:
                    embed = utils.Embed(title="Commentator No Show", description=f"Set your no show state")
                    embed.add_field(name="No Show", value=f"True")
                    await ctx.send(embed=embed)
                    return
            except Exception as err:
                await ctx.send(embed=utils.Embed(title="Error", description=f"```\n{err}\n```"))
        elif no_show.upper() in ["FALSE", "NO"]:
            response = await self.database.set_comms_no_show(str(ctx.message.author.id), False)
            try:
                if response:
                    embed = utils.Embed(title="Commentator No Show", description=f"Set your no show state")
                    embed.add_field(name="No Show", value=f"False")
                    await ctx.send(embed=embed)
                    return
            except Exception as err:
                await ctx.send(embed=utils.Embed(title="Error", description=f"```\n{err}\n```"))
                pass

    @commentators.command(aliases=["setNoAlert", "setnoalert"])
    async def set_no_alert(self, ctx, no_alert: str):
        """
        Set the no alert, to avoid showing system alerts
        """
        if no_alert.upper() in ["TRUE", "YES"]:
            response = await self.database.set_comms_no_alert(str(ctx.message.author.id), True)
            try:
                if response:
                    embed = utils.Embed(title="Commentator No Alert", description=f"Set your no alert state")
                    embed.add_field(name="No Alert", value=f"True")
                    await ctx.send(embed=embed)
                    return
            except Exception as err:
                await ctx.send(embed=utils.Embed(title="Error", description=f"```\n{err}\n```"))
        elif no_alert.upper() in ["FALSE", "NO"]:
            response = await self.database.set_comms_no_alert(str(ctx.message.author.id), False)
            try:
                if response:
                    embed = utils.Embed(title="Commentator No Alert", description=f"Set your no alert state")
                    embed.add_field(name="No Alert", value=f"False")
                    await ctx.send(embed=embed)
                    return
            except Exception as err:
                await ctx.send(embed=utils.Embed(title="Error", description=f"```\n{err}\n```"))
                pass


def setup(bot):
    bot.add_cog(Commentators(bot))
