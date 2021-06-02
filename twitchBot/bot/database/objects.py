"""
Class design for objects
"""
from typing import Optional, List


class CommandInfo:
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message


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
        self.discord_link = query_data.get("discordLink")
        self.custom_command = query_data.get("customCommands", {})

    @property
    def dict(self) -> dict:
        return {
            "discordGuildId": self.guild_id,
            "twitchChannelName": self.twitch_channel,
            "discordVCID": self.vc_channel_id,
            "alertChannelID": self.alert_channel_id,
            "currentComms": self.current_comms,
            "bracketLink": self.bracket_link,
            "tournamentName": self.tournament_name,
            "customCommands": self.custom_command,
            "discordLink": self.discord_link
        }

    def retrieve_custom_command(self, command_name: str) -> Optional[CommandInfo]:
        command_message = self.custom_command.get(command_name)
        if command_message:
            return CommandInfo(command_name, command_message)

    def get_all_commands(self) -> List[CommandInfo]:
        return_list = []
        for c in self.custom_command.items():
            return_list.append(CommandInfo(c[0], c[1]))
        return return_list


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
            "discordUserID": f"{self.discord_user_id}",
            "twitter": f"{self.twitter}",
            "name": f"{self.name}",
            "pronouns": f"{self.pronouns}"
        }
