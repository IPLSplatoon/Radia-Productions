from pydantic import BaseModel, Field
from typing import Optional


class CommInfo(BaseModel):
    discord_user_id: Optional[str] = Field(description="User's Discord User ID")
    twitter: Optional[str] = Field(description="User's Twitter handle without '@' symbol")
    name: Optional[str] = Field(description="User's Name")
    pronouns: Optional[str] = Field(description="User's preferred pronouns")

    class Config:
        schema_extra = {
            "example": {
                "discord_user_id": "113026708071821312",
                "twitter": "vlee888",
                "name": "Vincent",
                "pronouns": "They/Them",
            }
        }


class GuildInformation(BaseModel):
    guild_id: Optional[str] = Field(description="Entry's Discord Guild ID")
    twitch_channel: Optional[str] = Field(description="Entry's Twitch channel name")
    bracket_link: Optional[str] = Field(description="Entry's URL link to last set bracket")
    tournament_name: Optional[str] = Field(description="Entry's last set tournament name")

    class Config:
        schema_extra = {
            "example": {
                "guild_id": "805933686745726987",
                "twitch_channel": "iplsplatoon",
                "bracket_link": "https://iplabs.ink/bracket",
                "tournament_name": "Unnamed Tournament: Ladder Edition"
            }
        }


class CommentatorProfile(BaseModel):
    discord_user_id: Optional[str] = Field(description="User's Discord User ID")
    twitter: Optional[str] = Field(description="User's Twitter handle without '@' symbol")
    name: Optional[str] = Field(description="User's Name")
    pronouns: Optional[str] = Field(description="User's preferred pronouns")
    no_show: bool = Field(description="If the user set not to show up on commentator list. If TRUE, then they do NOT "
                                      "show up")
    no_alert: bool = Field(description="if the user wants any alerts to be disabled.")

    class Config:
        schema_extra = {
            "example": {
                "discord_user_id": "113026708071821312",
                "twitter": "vlee888",
                "name": "Vincent",
                "pronouns": "They/Them",
                "no_show": False,
                "no_alert": False
            }
        }


class CreateCommentatorProfile(BaseModel):
    twitter: str = Field(description="User's Twitter handle.", regex=r"^@?(\w){1,15}$")
    name: str = Field(description="User's Name", max_length=48)
    pronouns: str = Field(description="User's preferred pronouns", max_length=48)
    no_show: Optional[bool] = Field(description="If the user set not to show up on commentator list. If TRUE, "
                                                "then they do NOT show up", default=False)
    no_alert: Optional[bool] = Field(description="if the user wants any alerts to be disabled.", default=False)


class CustomCommands(BaseModel):
    name: str = Field(description="Name of custom command")
    contents: str = Field(description="Contents of custom command")

    class Config:
        schema_extra = {
            "example": {
                "name": "helpus",
                "contents": "Staff Application Form: https://iplabs.ink/helpus",
            }
        }
