from fastapi import APIRouter, Request, HTTPException, Depends
from app.dependencies import get_api_key
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()


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


@router.get("/guild/{guild_id}", response_model=GuildInformation)
async def guild_info(request: Request, guild_id, security_profile=Depends(get_api_key)):
    """
    The current commentator in voice channel by Discord Guild ID
    """
    info = await request.state.db.get_org_info({"discordGuildID": f"{guild_id}"})
    if info:
        return {
            "guild_id": info.guild_id,
            "twitch_channel": info.twitch_channel,
            "bracket_link": info.bracket_link,
            "tournament_name": info.tournament_name
        }
    else:
        raise HTTPException(status_code=404, detail="No commentator")


@router.get("/twitch/{twitch_name}", response_model=GuildInformation)
async def twitch_info(request: Request, twitch_name, security_profile=Depends(get_api_key)):
    """
    The current commentator in voice channel by Twitch Channel Name
    """
    info = await request.state.db.get_org_info({"twitchChannelName": f"{twitch_name}"})
    if info:
        return {
            "guild_id": info.guild_id,
            "twitch_channel": info.twitch_channel,
            "bracket_link": info.bracket_link,
            "tournament_name": info.tournament_name
        }
    else:
        raise HTTPException(status_code=404, detail="No commentator")
