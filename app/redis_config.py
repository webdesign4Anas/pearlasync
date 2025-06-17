import redis.asyncio as redis
import os
from typing import Optional

class RedisConfig():
    def __init__(self):
        self.host=os.getenv("REDIS_HOST","localhost")
        self.port=int(os.getenv("REDIS_PORT","6379"))
        self.db=int(os.getenv("REDIS_DB","0"))
        self.password=os.getenv("REDIS_PASSWORD",None)
        self._client:Optional[redis.Redis]=None


    async def get_client(self) -> redis.Redis:
        if self._client is None:
            self._client=redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True
            )
        return self._client



    async def close(self):
        if self._client:
            await self._client.close()



redis_config=RedisConfig()