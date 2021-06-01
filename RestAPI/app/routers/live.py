from fastapi import APIRouter, Request, HTTPException, Depends
from app.dependencies import get_api_key
from pydantic import BaseModel, Field
from typing import Optional, List

router = APIRouter()


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


@router.get("/guild/{guild_id}", response_model=List[CommInfo])
async def guild_live_commentators(request: Request, guild_id, security_profile=Depends(get_api_key)):
    """
    The current commentator in voice channel by Discord Guild ID
    """
    info = await request.state.db.get_org_info({"discordGuildID": f"{guild_id}"})
    if info:
        return info.live_comms_dict
    else:
        raise HTTPException(status_code=404, detail="No such guild")


@router.get("/twitch/{twitch_name}", response_model=List[CommInfo])
async def twitch_live_commentators(request: Request, twitch_name, security_profile=Depends(get_api_key)):
    """
    The current commentator in voice channel by Twitch Channel Name
    """
    info = await request.state.db.get_org_info({"twitchChannelName": f"{twitch_name}"})
    if info:
        return info.live_comms_dict
    else:
        raise HTTPException(status_code=404, detail="No such channel")
