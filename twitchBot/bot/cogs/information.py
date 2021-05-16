from twitchio.ext import commands
from bot.mongo import MongoConnector


class InformationCog:
    def __init__(self, bot):
        self.bot = bot

    @property
    def database(self):
        assert isinstance(self.bot.mongo, MongoConnector)
        return self.bot.mongo

    @commands.command(aliases=["discord"])
    async def discord_link(self, ctx):
        channel_data = await self.database.get_twitch_info(str(ctx.channel))
        if channel_data and channel_data.discord_link:
            await ctx.send(f"Discord: {channel_data.discord_link}")

    @commands.command(aliases=["bracket", "tournament"])
    async def bracket_link(self, ctx):
        channel_data = await self.database.get_twitch_info(str(ctx.channel))
        if channel_data and channel_data.bracket_link and channel_data.tournament_name:
            await ctx.send(f"{channel_data.tournament_name}: {channel_data.bracket_link}")


def prepare(bot):
    bot.add_cog(InformationCog(bot))
