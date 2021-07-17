from motor.motor_asyncio import AsyncIOMotorClient
from .objects import CommentatorProfile, AccessKey, GuildInfo
from typing import Optional


class DBConnector:
    def __init__(self, mongo_uri: str, db_name: str):
        """
        Constructor
        :param mongo_uri: MongoDB Connection URI
        :param db_name: DB
        """
        self.__uri = mongo_uri
        self.__db_name = db_name
        self.client: AsyncIOMotorClient = None
        self.db = None

    async def connect_db(self):
        """Create database connection."""
        self.client = AsyncIOMotorClient(self.__uri)
        self.db = self.client[self.__db_name]

    async def close_mongo_connection(self):
        """Close database connection."""
        self.client.close()

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
