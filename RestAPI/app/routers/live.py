from fastapi import APIRouter, Request, HTTPException, Depends
from app.dependencies import get_api_key
from typing import List
from app.models import CommInfo

router = APIRouter()


@router.get("/guild/{guild_id}", response_model=List[CommInfo], responses={
    404: {"description": "No such organisation"},
    401: {"description": "Invalid API Key"},
    403: {"description": "Not Authenticated"}
})
async def guild_live_commentators(request: Request, guild_id, security_profile=Depends(get_api_key)):
    """
    The current commentator in voice channel by Discord Guild ID
    """
    info = await request.state.db.get_org_info({"discordGuildID": f"{guild_id}"})
    if info:
        return info.live_comms_dict
    else:
        raise HTTPException(status_code=404, detail="No such organisation")


@router.get("/twitch/{twitch_name}", response_model=List[CommInfo], responses={
    404: {"description": "No such organisation"},
    401: {"description": "Invalid API Key"},
    403: {"description": "Not Authenticated"}
})
async def twitch_live_commentators(request: Request, twitch_name, security_profile=Depends(get_api_key)):
    """
    The current commentator in voice channel by Twitch Channel Name
    """
    info = await request.state.db.get_org_info({"twitchChannelName": f"{twitch_name}"})
    if info:
        return info.live_comms_dict
    else:
        raise HTTPException(status_code=404, detail="No such organisation")
