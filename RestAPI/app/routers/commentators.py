from fastapi import APIRouter, Request, HTTPException, Depends
from app.dependencies import get_api_key
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class CommentatorProfile(BaseModel):
    discord_user_id: Optional[str]
    twitter: Optional[str]
    name: Optional[str]
    pronouns: Optional[str]
    no_show: bool
    no_alert: bool


class CreateCommentatorProfile(BaseModel):
    twitter: Optional[str]
    name: Optional[str]
    pronouns: Optional[str]
    noShow: Optional[bool]
    noAlert: Optional[bool]


@router.get("/profile/twitter/{twitter_handle}", response_model=CommentatorProfile)
async def twitter_profile(request: Request, twitter_handle: str, security_profile=Depends(get_api_key)):
    """
    Details on a commentator via their twitter handle
    """
    info = await request.state.db.get_commentator_profile_twitter(twitter_handle)
    if info:
        return info.dict
    else:
        raise HTTPException(status_code=404, detail="Profile not found")


@router.get("/profile/discord/{discord_id}", response_model=CommentatorProfile)
async def discord_profile(request: Request, discord_id: str, security_profile=Depends(get_api_key)):
    """
    Details on a commentator via their Discord ID
    """
    info = await request.state.db.get_commentator_profile_discord(discord_id)
    if info:
        return info.dict
    else:
        raise HTTPException(status_code=404, detail="Profile not found")


@router.post("/profile/discord/{discord_id}", response_model=CommentatorProfile)
async def set_commentator_profile(request: Request, discord_id: str, commentator: CreateCommentatorProfile,
                                  security_profile=Depends(get_api_key)):
    """
    Set Details commentator via their Discord ID
    """
    response = await request.state.db.set_commentators_profile(discord_id, commentator.dict())
    if response:
        return response.dict
    else:
        raise HTTPException(status_code=500, detail="Internal error writing to database.")

