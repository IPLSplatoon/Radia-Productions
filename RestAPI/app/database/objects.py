"""
Class design for objects
"""
from typing import Optional, List


class Command:
    def __init__(self, name: str, contents: str):
        self.name = name
        self.contents = contents

    @property
    def dict(self) -> dict:
        return {
            "name": self.name,
            "contents": self.contents
        }


class CommentatorProfile:
    discord_user_id: Optional[str]
    twitter: Optional[str]
    name: Optional[str]
    pronouns: Optional[str]
    no_show: bool
    no_alert: bool

    def __init__(self, query_data: dict):
        self.discord_user_id = query_data.get("discordUserID")
        self.twitter = query_data.get("twitter")
        self.name = query_data.get("name")
        self.pronouns = query_data.get("pronouns")
        self.no_show = query_data.get("noShow", False)
        self.no_alert = query_data.get("noAlert", False)

    @property
    def dict(self) -> dict:
        return {
            "discord_user_id": self.discord_user_id,
            "twitter": self.twitter,
            "name": self.name,
            "pronouns": self.pronouns,
            "no_show": self.no_show,
            "no_alert": self.no_alert
        }

    @property
    def live_dict(self) -> dict:
        return {
            "discord_user_id": self.discord_user_id,
            "twitter": self.twitter,
            "name": self.name,
            "pronouns": self.pronouns,
        }


class GuildInfo:
    guild_id: Optional[str]
    twitch_channel: Optional[str]
    vc_channel_id: Optional[str]
    alert_channel_id: Optional[str]
    current_comms: Optional[List[CommentatorProfile]]
    bracket_link: Optional[str]
    tournament_name: Optional[str]

    def __init__(self, query_data: dict):
        """
        Init
        :param query_data:
        """
        self.guild_id = query_data.get("discordGuildID")
        self.twitch_channel = query_data.get("twitchChannelName")
        self.vc_channel_id = query_data.get("discordVCID")
        self.alert_channel_id = query_data.get("alertChannelID")
        self.bracket_link = query_data.get("bracketLink")
        self.tournament_name = query_data.get("tournamentName")
        self.custom_command = query_data.get("customCommands", {})
        self.commands = []
        for name in self.custom_command.keys():
            self.commands.append(Command(name, self.custom_command[name]))
        self.current_comms = []
        comms = query_data.get("currentComms")
        if comms:
            for x in comms:
                self.current_comms.append(CommentatorProfile(x))

    @property
    def live_comms_dict(self) -> List[dict]:
        return_dict = []
        for x in self.current_comms:
            return_dict.append(x.live_dict)
        return return_dict

    @property
    def custom_command_list(self) -> List[dict]:
        return_list = []
        for x in self.commands:
            return_list.append(x.dict)
        return return_list


class AccessKey:
    def __init__(self, query_data: dict):
        self.username = query_data.get("username")
        self.__access_key = query_data.get("accessKey")
        self.__guilds = query_data.get("guilds")

    def check_access_key(self, access_key: str) -> bool:
        if self.__access_key == access_key:
            return True
        else:
            return False

    def check_guilds(self, guild: str) -> bool:
        if guild in self.__guilds:
            return True
        else:
            return False
