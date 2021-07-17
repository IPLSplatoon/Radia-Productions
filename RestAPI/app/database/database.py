from motor.motor_asyncio import AsyncIOMotorClient
from .objects import CommentatorProfile, AccessKey, GuildInfo
from aredis import StrictRedis
from typing import Optional, Union
import msgpack


class DBConnector:
    def __init__(self, mongo_uri: str, db_name: str, redis_uri: str):
        """
        Constructor
        :param mongo_uri: MongoDB Connection URI
        :param db_name: DB
        :param redis_uri: Redis Connection URI
        """
        self.__mongo_uri = mongo_uri
        self.__redis_uri = redis_uri
        self.__db_name = db_name
        self.__redis_client: Optional[StrictRedis] = None
        self.mongo_client: AsyncIOMotorClient = None
        self.db = None

    async def connect_db(self):
        """Create database connection."""
        self.mongo_client = AsyncIOMotorClient(self.__mongo_uri)
        self.db = self.mongo_client[self.__db_name]
        self.__redis_client = StrictRedis.from_url(self.__redis_uri)

    async def close_mongo_connection(self):
        """Close database connection."""
        self.mongo_client.close()

    async def __update_redis_twitch(self, query: dict, expire: Union[int, None] = 1800) -> Optional[GuildInfo]:
        db_query = await self.db.server.find_one(query)
        if db_query:
            if "twitchChannelName" in db_query:
                data = GuildInfo(db_query).dict
                if isinstance(expire, int):  # If we've given a key expiry time
                    if await self.__redis_client.set(f"twitch:{db_query['twitchChannelName']}",
                                                     msgpack.packb(data, use_bin_type=True), ex=expire):
                        return GuildInfo(db_query)
                else:
                    if await self.__redis_client.set(f"twitch:{db_query['twitchChannelName']}",
                                                     msgpack.packb(data, use_bin_type=True)):
                        return GuildInfo(db_query)
        return None

    async def get_access_key_details(self, access_key: str) -> Optional[AccessKey]:
        """
        Get access details via Access Key
        :param access_key: user access key
        :return: AccessKey object is valid key is provided
        """
        query = await self.db.access.find_one({"accessKey": f"{access_key}"})
        if query:
            return AccessKey(query)

    async def get_commentator_profile(self, query: dict) -> Optional[CommentatorProfile]:
        """
        Get commentator profile
        :param query: query for commentator
        :return: CommentatorProfile
        """
        query = await self.db.commenators.find_one(query)
        if query:
            return CommentatorProfile(query)

    async def get_org_info(self, query: dict) -> Optional[GuildInfo]:
        """
        Get Organisation Profile
        :param query: query for organisation
        :return: GuildInfo
        """
        query = await self.db.server.find_one(query)
        if query:
            return GuildInfo(query)

    async def set_guild_bracket_info(self, query: dict, bracket_link: str,
                                     tournament_name: str) -> Optional[GuildInfo]:
        """
        Set Guild bracket link and Tournament name
        :param query: query for organisation
        :param bracket_link: bracket link
        :param tournament_name: tournament name
        :return: GuildInfo
        """
        instance = {
            "$set": {
                "bracketLink": bracket_link,
                "tournamentName": tournament_name,
            }
        }
        await self.db.server.update_one(query, instance, upsert=True)
        return await self.__update_redis_twitch(query)

    async def set_commentator_profile(self, query: dict, data: dict) -> Optional[CommentatorProfile]:
        """
        Set a commentator profile
        :param query: Query to set by
        :param data: Data dict to set commentator by
        :return: CommentatorProfile
        """
        instance = {
            "$set": data
        }
        response = await self.db.commenators.update_one(query, instance, upsert=True)
        if response:
            query = await self.db.commenators.find_one(query)
            if query:
                return CommentatorProfile(query)
