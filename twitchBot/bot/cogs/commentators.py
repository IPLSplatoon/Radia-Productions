from twitchio.ext import commands
from bot.mongo import MongoConnector


class CommentatorsCog:
    def __init__(self, bot):
        self.bot = bot

    @property
    def database(self):
        assert isinstance(self.bot.mongo, MongoConnector)
        return self.bot.mongo

    @commands.command(aliases=["mic"])
    async def commentators(self, ctx):
        channel_data = await self.database.get_twitch_info(str(ctx.channel))
        if channel_data and channel_data.current_comms:
            message = " On Mic (pronouns, twitter): "
            after_first = False  # Used to know if we need to place an & between comms
            for x in channel_data.current_comms:
                if after_first:
                    message += f" & "
                message += f"{x['name']} ({x['pronouns']}, @{x['twitter']})"
                after_first = True
            await ctx.send(message)
        elif channel_data:
            await ctx.send("No commentators currently on")


def prepare(bot):
    bot.add_cog(CommentatorsCog(bot))
