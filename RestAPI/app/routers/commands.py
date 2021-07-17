from fastapi import APIRouter, Request, HTTPException, Depends
from app.dependencies import get_api_key
from typing import List
from app.models import CustomCommands

router = APIRouter()


@router.get("/guild/{guild_id}", response_model=List[CustomCommands], responses={
    404: {"description": "No such organisation"},
    401: {"description": "Invalid API Key"},
    403: {"description": "Not Authenticated"}
})
async def guild_commands(request: Request, guild_id, security_profile=Depends(get_api_key)):
    """
    The custom commands by Discord Guild ID
    """
    info = await request.state.db.get_org_info({"discordGuildID": f"{guild_id}"})
    if info:
        return info.custom_command_list
    else:
        raise HTTPException(status_code=404, detail="No such organisation")


@router.get("/twitch/{twitch_name}", response_model=List[CustomCommands], responses={
    404: {"description": "No such organisation"},
    401: {"description": "Invalid API Key"},
    403: {"description": "Not Authenticated"}
})
async def twitch_commands(request: Request, twitch_name, security_profile=Depends(get_api_key)):
    """
    The custom commands by Twitch Channel Name
    """
    info = await request.state.db.get_org_info({"twitchChannelName": f"{twitch_name}"})
    if info:
        return info.custom_command_list
    else:
        raise HTTPException(status_code=404, detail="No such organisation")
