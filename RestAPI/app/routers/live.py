from fastapi import APIRouter, Request, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class CommInfo(BaseModel):
    twitter: Optional[str]
    name: Optional[str]
    pronouns: Optional[str]


@router.get("/guild/{guild_id}", response_model=List[CommInfo])
async def guild_live_commentators(request: Request, guild_id, Authorization: str = Header(...)):
    """
    The current commentator in voice channel by Discord Guild ID
    """
    auth = await request.state.db.get_access_key_details(Authorization)
    if not auth:
        raise HTTPException(status_code=401, detail="Not Authorised")
    info = await request.state.db.get_current_commentators_guild(guild_id)
    if info:
        return_list = []
        for x in info:
            return_list.append(x.dict)
        return return_list
    else:
        raise HTTPException(status_code=404, detail="No commentator")


@router.get("/twitch/{twitch_name}", response_model=List[CommInfo])
async def twitch_live_commentators(request: Request, twitch_name, Authorization: str = Header(...)):
    """
    The current commentator in voice channel by Twitch Channel Name
    """
    auth = await request.state.db.get_access_key_details(Authorization)
    if not auth:
        raise HTTPException(status_code=401, detail="Not Authorised")
    info = await request.state.db.get_current_commentators_twitch(twitch_name)
    if info:
        return_list = []
        for x in info:
            return_list.append(x.dict)
        return return_list
    else:
        raise HTTPException(status_code=404, detail="No commentator")

