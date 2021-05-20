"""
Class design for objects
"""
from typing import Optional


class GuildInfo:
    bracket_link: Optional[str]

    def __init__(self, query_data: dict):
        """
        Init
        :param query_data:
        """
        self.guild_id = query_data.get("discordGuildId")
        self.twitch_channel = query_data.get("twitchChannelName")
        self.vc_channel_id = query_data.get("discordVCID")
        self.alert_channel_id = query_data.get("alertChannelID")
        self.current_comms = query_data.get("currentComms")
        self.bracket_link = query_data.get("bracketLink")
        self.tournament_name = query_data.get("tournamentName")

    @property
    def dict(self) -> dict:
        return {
            "discordGuildId": self.guild_id,
            "twitchChannelName": self.twitch_channel,
            "discordVCID": self.vc_channel_id,
            "alertChannelID": self.alert_channel_id,
            "currentComms": self.current_comms,
            "bracketLink": self.bracket_link,
            "tournamentName": self.tournament_name
        }


class CommInfo:
    def __init__(self, query_data: dict):
        self.discord_user_id = query_data.get("discordUserID")
        self.twitter = query_data.get("twitter")
        self.name = query_data.get("name")
        self.pronouns = query_data.get("pronouns")
        self.no_show = query_data.get("noShow", False)
        self.no_alert = query_data.get("noAlert", False)

    @property
    def mongo_dict(self) -> dict:
        """
        returns a dict for MongoDB
        :return: dict for MongoDB
        """
        return {
            "discordUserID": self.discord_user_id,
            "twitter": self.twitter,
            "name": self.name,
            "pronouns": self.pronouns
        }
