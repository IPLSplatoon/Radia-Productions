from fastapi import APIRouter, Request, HTTPException, Depends
from app.dependencies import get_api_key
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class GuildInformation(BaseModel):
    guild_id: Optional[str]
    twitch_channel: Optional[str]
    bracket_link: Optional[str]
    tournament_name: Optional[str]


@router.get("/guild/{guild_id}", response_model=GuildInformation)
async def guild_info(request: Request, guild_id, security_profile=Depends(get_api_key)):
    """
    The current commentator in voice channel by Discord Guild ID
    """
    info = await request.state.db.get_guild_info(guild_id)
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
    info = await request.state.db.get_twitch_info(twitch_name)
    if info:
        return {
            "guild_id": info.guild_id,
            "twitch_channel": info.twitch_channel,
            "bracket_link": info.bracket_link,
            "tournament_name": info.tournament_name
        }
    else:
        raise HTTPException(status_code=404, detail="No commentator")
