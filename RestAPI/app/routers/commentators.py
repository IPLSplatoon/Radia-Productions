from fastapi import APIRouter, Request, HTTPException, Depends, Query
from app.dependencies import get_api_key
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()


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


@router.get("/profile/twitter/{twitter_handle}", response_model=CommentatorProfile, responses={
    404: {"description": "Profile not found"},
    401: {"description": "Invalid API Key"},
    403: {"description": "Not Authenticated"}
})
async def twitter_profile(request: Request, twitter_handle: str, security_profile=Depends(get_api_key)):
    """
    Details on a commentator via their twitter handle
    """
    info = await request.state.db.get_commentator_profile({"twitter": f"{twitter_handle}"})
    if info:
        return info.dict
    else:
        raise HTTPException(status_code=404, detail="Profile not found")


@router.get("/profile/discord/{discord_id}", response_model=CommentatorProfile, responses={
    404: {"description": "Profile not found"},
    401: {"description": "Invalid API Key"},
    403: {"description": "Not Authenticated"}
})
async def discord_profile(request: Request, discord_id: str, security_profile=Depends(get_api_key)):
    """
    Details on a commentator via their Discord ID
    """
    info = await request.state.db.get_commentator_profile({"discordUserID": f"{discord_id}"})
    if info:
        return info.dict
    else:
        raise HTTPException(status_code=404, detail="Profile not found")


@router.post("/profile/discord/{discord_id}", response_model=CommentatorProfile, responses={
    500: {"description": "Internal error writing to database"},
    401: {"description": "Invalid API Key"},
    403: {"description": "FORBIDDEN: You're disabled from setting commentator details. / Not Authenticated"}
})
async def set_commentator_profile(request: Request, commentator: CreateCommentatorProfile,
                                  discord_id: str = Query(None, regex=r"^[0-9]*$"),
                                  security_profile=Depends(get_api_key)):
    """
    Set Details commentator via their Discord ID
    """
    data = commentator.dict()
    # Remove @ Symbol if present
    if data["twitter"][0] == "@":
        data["twitter"] = data["twitter"][1:]
    response = await request.state.db.set_commentator_profile({"discordUserID": f"{discord_id}"}, commentator.dict())
    if response:
        return response.dict
    else:
        raise HTTPException(status_code=500, detail="Internal error writing to database.")
