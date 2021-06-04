from fastapi import APIRouter, Request, Query
from typing import List
from app.models import CommInfo, GuildInformation, CommentatorProfile, CreateCommentatorProfile, CustomCommands

router = APIRouter()


def live_mock(num_comms: str):
    return_list = []
    try:
        num = int(num_comms)
    except ValueError:
        num = 3
    for x in range(num):
        return_list.append({
            "discord_user_id": f"{x + 1}",
            "twitter": f"caster_{x + 1}",
            "name": f"caster_{x + 1}",
            "pronouns": "They/Them",
        })
    return return_list


@router.get("/live/guild/{guild_id}", response_model=List[CommInfo])
async def guild_live_commentators(request: Request, guild_id: str):
    """
    Mock for `/live/guild/` with `guild_id` being number of commentators you want returned.
    """
    return live_mock(guild_id)


@router.get("/live/twitch/{twitch_name}", response_model=List[CommInfo])
async def twitch_live_commentators(request: Request, twitch_name: str):
    """
    Mock for `/live/twitch/` with `twitch_name` being number of commentators you want returned.
    """
    return live_mock(twitch_name)


@router.get("/organisation/guild/{guild_id}", response_model=GuildInformation)
async def guild_info(request: Request, guild_id):
    """
    Mock for `/organisation/guild/`
    """
    return {
        "guild_id": f"{guild_id}",
        "twitch_channel": "MockExample",
        "bracket_link": "https://iplabs.ink/mocking",
        "tournament_name": "Unnamed Tournament: Mock Edition"
    }


@router.get("/organisation/twitch/{twitch_name}", response_model=GuildInformation)
async def twitch_info(request: Request, twitch_name):
    """
    Mock for `/organisation/twitch/`
    """
    return {
        "guild_id": "01101000011010010111100101100001",
        "twitch_channel": f"{twitch_name}",
        "bracket_link": "https://iplabs.ink/bracket",
        "tournament_name": "Unnamed Tournament: Ladder Edition"
    }


@router.get("/commentators/profile/twitter/{twitter_handle}", response_model=CommentatorProfile)
async def twitter_profile(request: Request, twitter_handle: str):
    """
    Mock for `/profile/twitter/`
    """
    return {
        "discord_user_id": "011010000110100100001010",
        "twitter": f"{twitter_handle}",
        "name": "MockingUser",
        "pronouns": "They/Them",
        "no_show": False,
        "no_alert": False
    }


@router.get("/commentators/profile/discord/{discord_id}", response_model=CommentatorProfile)
async def discord_profile(request: Request, discord_id: str):
    """
    Mock for `/profile/discord/`
    """
    return {
        "discord_user_id": f"{discord_id}",
        "twitter": "mock_user",
        "name": "MockingUser",
        "pronouns": "They/Them",
        "no_show": False,
        "no_alert": False
    }


@router.post("/commentators/profile/discord/{discord_id}", response_model=CommentatorProfile)
async def set_commentator_profile(request: Request, commentator: CreateCommentatorProfile,
                                  discord_id: str = Query(None, regex=r"^[0-9]*$")):
    """
    Mock for `/profile/discord/` POST
    """
    data = commentator.dict()
    # Remove @ Symbol if present
    if data["twitter"][0] == "@":
        data["twitter"] = data["twitter"][1:]
    data['discord_user_id'] = discord_id
    return data


def custom_command(count: str) -> List[dict]:
    return_list = []
    try:
        num = int(count)
    except ValueError:
        num = 3
    for x in range(num):
        return_list.append({
            "name": f"command{x+1}",
            "contents": f"This custom return for custom command {x+1}"
        })
    return return_list


@router.get("/commands/guild/{guild_id}", response_model=List[CustomCommands])
async def guild_commands(request: Request, guild_id):
    """
    Mock for `/commands/guild/` with, with `guild_id` being number of commands you want returned.
    """
    return custom_command(guild_id)


@router.get("/commands/twitch/{twitch_name}", response_model=List[CustomCommands])
async def twitch_commands(request: Request, twitch_name):
    """
    Mock for `/commands/twitch/` with,, with `twitch_name` being number of commands you want returned.
    """
    return custom_command(twitch_name)
