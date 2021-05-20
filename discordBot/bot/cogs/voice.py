"""
Handles all commands & event handler for voice channels
"""
import discord
from discord.ext import commands

from bot.mongo import MongoConnector
from bot import utils


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def database(self):
        assert isinstance(self.bot.mongo, MongoConnector)
        return self.bot.mongo

    @commands.group()
    async def voice(self, ctx):
        """Group of commands handling the voice channel info setting."""

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild_info = await self.database.get_guild_info(str(member.guild.id))
        if guild_info:  # If guild exists
            if after.channel:  # User join channel
                if str(after.channel.id) == guild_info.vc_channel_id:  # if the join the vc channel
                    member_comms_info = await self.database.get_comms_info(str(member.id))
                    if member_comms_info and (not member_comms_info.no_show):
                        await self.database.upsert_server_comm(str(member.guild.id), member_comms_info)
                    elif member_comms_info and member_comms_info.no_show and (not member_comms_info.no_alert):
                        # Alert member they are not being shown
                        alert_channel = self.bot.get_channel(int(guild_info.alert_channel_id))
                        embed = utils.Embed(title="Commentator Warning",
                                            description=f"{member.mention} you're not shown as a commentator")
                        await alert_channel.send(embed=embed)
                    elif not member_comms_info:
                        # Alert member they don't have a profile setup
                        alert_channel = self.bot.get_channel(int(guild_info.alert_channel_id))
                        embed = utils.Embed(title="Commentator Error",
                                            description=f"{member.mention} you don't have a commentator profile!\n"
                                                        f"use `!help commentators set_profile` to get started")
                        await alert_channel.send(embed=embed)
            elif before.channel and (str(before.channel.id) == guild_info.vc_channel_id):  # Member leave channel
                # Remove them from the guild current live comms list
                await self.database.remove_server_comm(str(member.guild.id), str(member.id))

    @voice.command(aliases=["refreshComms", "refreshcomms", "refresh"])
    async def refresh_commentators(self, ctx):
        """
        Force refresh the commentator in a the live voice channel
        """
        guild_info = await self.database.get_guild_info(str(ctx.message.guild.id))
        if guild_info:
            voice_channel = ctx.guild.get_channel(int(guild_info.vc_channel_id))
            comms_list = []
            for member in voice_channel.members:
                member_comms_info = await self.database.get_comms_info(str(member.id))
                if member_comms_info and (not member_comms_info.no_show):
                    comms_list.append(member_comms_info)
                elif member_comms_info and member_comms_info.no_show and (not member_comms_info.no_alert):
                    # Alert member they are not being shown
                    embed = utils.Embed(title="Commentator Warning",
                                        description=f"{member.mention} you're not shown as a commentator")
                    await ctx.send(embed=embed)
                elif not member_comms_info:  # Alert member they don't have a profile setup
                    embed = utils.Embed(title="Commentator Error",
                                        description=f"{member.mention} you don't have a commentator profile!\n"
                                                    f"use `^help commentators set_profile` to get started")
                    await ctx.send(embed=embed)
            await self.database.set_server_comms(str(ctx.message.guild.id), comms_list)
            await ctx.message.add_reaction("👍")


def setup(bot):
    bot.add_cog(Voice(bot))
