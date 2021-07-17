from fastapi import APIRouter, Request, HTTPException, Depends
from app.dependencies import get_api_key
from app.models import GuildInformation, SetGuildInformation

router = APIRouter()


@router.get("/guild/{guild_id}", response_model=GuildInformation, responses={
    404: {"description": "No such organisation"},
    401: {"description": "Invalid API Key"},
    403: {"description": "Not Authenticated"}
})
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
        raise HTTPException(status_code=404, detail="No such organisation")


@router.get("/twitch/{twitch_name}", response_model=GuildInformation, responses={
    404: {"description": "No such organisation"},
    401: {"description": "Invalid API Key"},
    403: {"description": "Not Authenticated"}
})
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
        raise HTTPException(status_code=404, detail="No such organisation")


@router.post("/guild/{guild_id}", response_model=GuildInformation, responses={
    404: {"description": "No such organisation"},
    401: {"description": "Invalid API Key"},
    403: {"description": "Not Authenticated"},
    500: {"description": "Internal Server Error"}
})
async def set_guild_info(request: Request, guild_id: str, tournament_info: SetGuildInformation,
                         security_profile=Depends(get_api_key)):
    """Set a guild's tournament info"""
    if not security_profile.check_guilds(guild_id):
        raise HTTPException(status_code=403, detail="Not Authorised for guild")
    else:
        info = await request.state.db.get_org_info({"discordGuildID": f"{guild_id}"})
        if info:
            response = await request.state.db.set_guild_bracket_info({"discordGuildID": f"{guild_id}"},
                                                                     tournament_info.bracket_link,
                                                                     tournament_info.tournament_name)
            if response:
                return {
                    "guild_id": response.guild_id,
                    "twitch_channel": response.twitch_channel,
                    "bracket_link": response.bracket_link,
                    "tournament_name": response.tournament_name
                }
            else:
                raise HTTPException(status_code=500, detail="Internal Server Error")
        else:
            raise HTTPException(status_code=404, detail="No such organisation")
