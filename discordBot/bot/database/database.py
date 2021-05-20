import motor.motor_asyncio
from .objects import GuildInfo, CommInfo
from typing import List, Optional, Union
from aredis import StrictRedis
import msgpack


class DBConnector:
    def __init__(self, mongo_uri: str, mongo_db_name: str, redis_url: str):
        """
        Constructor
        :param mongo_uri: Mongo DB URI
        :param mongo_db_name: Database Name
        :param redis_url: Redis database URL
        """
        self.__client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.__db = self.__client[mongo_db_name]
        self.__redis_client = StrictRedis.from_url(redis_url)

    async def __fetch_set_redis(self, query: dict, key: str, expire: Union[int, None] = 1800) -> Optional[GuildInfo]:
        db_query = await self.__db.server.find_one(query)
        if db_query:
            data = GuildInfo(db_query).dict
            if isinstance(expire, int):  # If we've given a key expiry time
                if await self.__redis_client.set(key, msgpack.packb(data, use_bin_type=True), ex=expire):
                    return GuildInfo(db_query)
            else:
                if await self.__redis_client.set(key, msgpack.packb(data, use_bin_type=True)):
                    return GuildInfo(db_query)
        return None

    async def __update_redis_twitch(self, query: dict, expire: Union[int, None] = 1800) -> Optional[GuildInfo]:
        db_query = await self.__db.server.find_one(query)
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

    async def __retrieve_from_redis(self, key: str) -> Optional[GuildInfo]:
        query = await self.__redis_client.get(key)
        if query:
            return GuildInfo(msgpack.unpackb(query, raw=False))

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
        query = await self.__retrieve_from_redis(f"twitch:{twitch_name}")
        if query:
            return query
        else:
            query = await self.__fetch_set_redis({"twitchChannelName": twitch_name}, f"twitch:{twitch_name}")
            if query:
                return query

    async def set_server_vc(self, guild_id: str, vc_id: str):
        instance = {
            "$set": {
                "discordVCID": vc_id,
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": guild_id}, instance, upsert=True)
        await self.__update_redis_twitch({"discordGuildID": guild_id})
        return response

    async def set_server_bracket_link(self, guild_id: str, bracket_link: str):
        instance = {
            "$set": {
                "bracketLink": bracket_link,
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": guild_id}, instance, upsert=True)
        await self.__update_redis_twitch({"discordGuildID": guild_id})
        return response

    async def set_server_tournament_name(self, guild_id: str, tournament_name: str):
        instance = {
            "$set": {
                "tournamentName": tournament_name,
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": guild_id}, instance, upsert=True)
        await self.__update_redis_twitch({"discordGuildID": guild_id})
        return response

    async def set_server_comms(self, guild_id: str, commentators: List[CommInfo]):
        comms_list = []
        for x in commentators:
            comms_list.append(x.mongo_dict)
        instance = {
            "$set": {
                "currentComms": comms_list,
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": guild_id}, instance, upsert=True)
        await self.__update_redis_twitch({"discordGuildID": guild_id})
        return response

    async def upsert_server_comm(self, guild_id: str, commentators: CommInfo):
        instance = {
            "$addToSet": {
                "currentComms": {
                    "$each": [commentators.mongo_dict]
                }
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": guild_id}, instance, upsert=True)
        await self.__update_redis_twitch({"discordGuildID": guild_id})
        return response

    async def remove_server_comm(self, guild_id: str, commentators_discord_id: str):
        instance = {
            "$pull": {
                "currentComms": {
                    "discordUserID": commentators_discord_id
                }
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": guild_id}, instance)
        await self.__update_redis_twitch({"discordGuildID": guild_id})
        return response

    # ======== Commentator related ========

    async def get_comms_info(self, discord_user_id: str) -> Optional[CommInfo]:
        query = await self.__db.commenators.find_one({"discordUserID": discord_user_id})
        if query:
            return CommInfo(query)

    async def set_comms_info(self, discord_user_id: str, name: str, twitter: str, pronouns: str):
        instance = {
            "$set": {
                "name": name,
                "twitter": twitter,
                "pronouns": pronouns
            }
        }
        return await self.__db.commenators.update_one({"discordUserID": discord_user_id}, instance, upsert=True)

    async def set_comms_no_show(self, discord_user_id: str, no_show: bool):
        instance = {
            "$set": {
                "noShow": no_show,
            }
        }
        return await self.__db.commenators.update_one({"discordUserID": discord_user_id}, instance, upsert=True)

    async def set_comms_no_alert(self, discord_user_id: str, no_alert: bool):
        instance = {
            "$set": {
                "noAlert": no_alert,
            }
        }
        return await self.__db.commenators.update_one({"discordUserID": discord_user_id}, instance, upsert=True)

    # ======== Custom Twitch Commands ========

    async def add_custom_command(self, guild_id: str, command_name: str, command_message: str):
        instance = {
            "$set": {
                "customCommands": {
                    command_name: command_message
                }
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": guild_id}, instance, upsert=True)
        await self.__update_redis_twitch({"discordGuildID": guild_id})
        return response

    async def remove_custom_command(self, guild_id: str, command_name: str):
        instance = {
            "$unset": {
                f"customCommands.{command_name}": 1
            }
        }
        response = await self.__db.server.update_one({"discordGuildID": guild_id}, instance)
        await self.__update_redis_twitch({"discordGuildID": guild_id})
        return response
