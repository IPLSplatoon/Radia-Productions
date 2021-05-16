from fastapi import APIRouter, Request, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class GuildInformation(BaseModel):
    guild_id: Optional[str]
    twitch_channel: Optional[str]
    bracket_link: Optional[str]
    tournament_name: Optional[str]


@router.get("/guild/{guild_id}", response_model=GuildInformation)
async def guild_info(request: Request, guild_id, Authorization: str = Header(...)):
    """
    The current commentator in voice channel by Discord Guild ID
    """
    auth = await request.state.db.get_access_key_details(Authorization)
    if not auth:
        raise HTTPException(status_code=401, detail="Not Authorised")
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
async def twitch_info(request: Request, twitch_name, Authorization: str = Header(...)):
    """
    The current commentator in voice channel by Twitch Channel Name
    """
    auth = await request.state.db.get_access_key_details(Authorization)
    if not auth:
        raise HTTPException(status_code=401, detail="Not Authorised")
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
