from motor.motor_asyncio import AsyncIOMotorClient
from .objects import CommentatorProfile, CommInfo, AccessKey, GuildInfo
from typing import List, Optional


class MongoConnector:
    def __init__(self, mongo_uri: str, db_name: str):
        """
        Constructor
        """
        self.__uri = mongo_uri
        self.__db_name = db_name
        self.__client: AsyncIOMotorClient = None
        self.__db = None

    async def connect_db(self):
        """Create database connection."""
        self.__client = AsyncIOMotorClient(self.__uri)
        self.__db = self.__client[self.__db_name]

    async def close_mongo_connection(self):
        """Close database connection."""
        self.__client.close()

    async def get_commentator_profile_twitter(self, twitter_handle: str) -> Optional[CommentatorProfile]:
        query = await self.__db.commenators.find_one({"twitter": twitter_handle})
        if query:
            return CommentatorProfile(query)

    async def get_commentator_profile_discord(self, discord_id: str) -> Optional[CommentatorProfile]:
        query = await self.__db.commenators.find_one({"discordUserID": discord_id})
        if query:
            return CommentatorProfile(query)

    async def get_current_commentators_guild(self, discord_guild_id: str) -> Optional[List[CommInfo]]:
        query = await self.__db.server.find_one({"discordGuildID": discord_guild_id})
        if query:
            return_list = []
            for x in query["currentComms"]:
                return_list.append(CommInfo(x))
            return return_list

    async def get_current_commentators_twitch(self, twitch_name: str) -> Optional[List[CommInfo]]:
        query = await self.__db.server.find_one({"twitchChannelName": twitch_name})
        if query:
            return_list = []
            for x in query["currentComms"]:
                return_list.append(CommInfo(x))
            return return_list

    async def get_access_key_details(self, access_key: str) -> Optional[AccessKey]:
        query = await self.__db.access.find_one({"accessKey": f"{access_key}"})
        if query:
            return AccessKey(query)

    async def get_guild_info(self, guild_id: str) -> Optional[GuildInfo]:
        """
        Get info on a guild
        :param guild_id: Discord Guild ID
        :return: GuildInfo or None
        """
        query = await self.__db.server.find_one({"discordGuildID": guild_id})
        if query:
            return GuildInfo(query)

    async def get_twitch_info(self, twitch_name: str) -> Optional[GuildInfo]:
        query = await self.__db.server.find_one({"twitchChannelName": twitch_name})
        if query:
            return GuildInfo(query)

    async def set_commentators_profile(self, discord_user_id: str, information: dict) -> Optional[CommentatorProfile]:
        instance = {
            "$set": information
        }
        response = await self.__db.commenators.update_one({"discordUserID": discord_user_id}, instance, upsert=True)
        if response:
            query = await self.__db.commenators.find_one({"discordUserID": discord_user_id})
            if query:
                return CommentatorProfile(query)

    async def set_guild_commentators(self, discord_guild_id: str, commentators: List[dict]):
        instance = {
            "$set": {
                "currentComms": commentators,
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": discord_guild_id}, instance, upsert=True)
        if response:
            query = await self.__db.server.find_one({"discordGuildID": discord_guild_id})
            if query:
                return_list = []
                for x in query["currentComms"]:
                    return_list.append(CommInfo(x))
                return return_list

    async def add_guild_commentator(self, discord_guild_id: str, commentator: dict):
        instance = {
            "$addToSet": {
                "currentComms": {
                    "$each": commentator
                }
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": discord_guild_id}, instance, upsert=True)
        if response:
            query = await self.__db.server.find_one({"discordGuildID": discord_guild_id})
            if query:
                return_list = []
                for x in query["currentComms"]:
                    return_list.append(CommInfo(x))
                return return_list

    async def remove_guild_commentator(self, guild_id: str, commentators_discord_id: str):
        instance = {
            "$pull": {
                "currentComms": {
                    "discordUserID": f"{commentators_discord_id}"
                }
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": guild_id}, instance)
        if response:
            query = await self.__db.server.find_one({"discordGuildID": discord_guild_id})
            if query:
                return_list = []
                for x in query["currentComms"]:
                    return_list.append(CommInfo(x))
                return return_list