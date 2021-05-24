from fastapi import APIRouter, Request, HTTPException, Depends
from app.dependencies import get_api_key
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class CommInfo(BaseModel):
    twitter: Optional[str]
    name: Optional[str]
    pronouns: Optional[str]


class CreateCommInfo(BaseModel):
    discordUserID: str
    twitter: str
    name: str
    pronouns: str


class RemoveCommInfo(BaseModel):
    discordUserID: str


@router.get("/guild/{guild_id}", response_model=List[CommInfo])
async def guild_live_commentators(request: Request, guild_id, security_profile=Depends(get_api_key)):
    """
    The current commentator in voice channel by Discord Guild ID
    """
    info = await request.state.db.get_current_commentators_guild(guild_id)
    if info:
        return_list = []
        for x in info:
            return_list.append(x.dict)
        return return_list
    else:
        raise HTTPException(status_code=404, detail="No commentator")


@router.get("/twitch/{twitch_name}", response_model=List[CommInfo])
async def twitch_live_commentators(request: Request, twitch_name, security_profile=Depends(get_api_key)):
    """
    The current commentator in voice channel by Twitch Channel Name
    """
    info = await request.state.db.get_current_commentators_twitch(twitch_name)
    if info:
        return_list = []
        for x in info:
            return_list.append(x.dict)
        return return_list
    else:
        raise HTTPException(status_code=404, detail="No commentator")


@router.post("/guild/{guild_id}", response_model=List[CommInfo])
async def set_guild_live_commentators(request: Request, guild_id,
                                      commentators: List[CreateCommInfo], security_profile=Depends(get_api_key)):
    """
    Set guild live commentators
    """
    if not security_profile.check_guilds(guild_id):
        raise HTTPException(status_code=401, detail="Not Authorised for guild")
    comms_list = []
    for x in commentators:
        comms_list.append(x.dict())
    response = await request.state.db.set_guild_commentators(guild_id, comms_list)
    if response:
        return_list = []
        for x in response:
            return_list.append(x.dict)
        return return_list
    else:
        raise HTTPException(status_code=404, detail="No commentator")


@router.patch("/guild/{guild_id}/remove", response_model=List[CommInfo])
async def remove_guild_live_commentators(request: Request, guild_id, commentator: RemoveCommInfo,
                                         security_profile=Depends(get_api_key)):
    """
    Remove a commentator from guild love commentators
    """
    if not security_profile.check_guilds(guild_id):
        raise HTTPException(status_code=401, detail="Not Authorised for guild")
    response = await request.state.db.remove_guild_commentator(guild_id, commentator.discordUserID)
    if response:
        return_list = []
        for x in response:
            return_list.append(x.dict)
        return return_list
    else:
        raise HTTPException(status_code=404, detail="No commentator")


@router.patch("/guild/{guild_id}/add", response_model=List[CommInfo])
async def add_guild_live_commentators(request: Request, guild_id, commentator: CreateCommInfo,
                                      security_profile=Depends(get_api_key)):
    """
    Add a commentator to guild love commentators
    """
    if not security_profile.check_guilds(guild_id):
        raise HTTPException(status_code=401, detail="Not Authorised for guild")
    response = await request.state.db.add_guild_commentator(guild_id, commentator)
    if response:
        return_list = []
        for x in response:
            return_list.append(x.dict)
        return return_list
    else:
        raise HTTPException(status_code=404, detail="No commentator")
