from fastapi import HTTPException,status
from app.redis_config import redis_config
import time

class RateLimitService():

    @staticmethod
    async def check_login_rate_limit(username:str,max_attempts:int=5,window_minutes:int=15):
        redis_client= await redis_config.get_client()
        key=f"login_attempts:{username} "
        current_time=int(time.time())
        window_start=current_time-(window_minutes*60)

        # Remove old attempts outside the time window
        await redis_client.zremrangebyscore(key,0,window_start)

        # Count current attempts in the window
        current_attempts=await redis_client.zcard(key)

        if current_attempts>= max_attempts:
            oldest_attempt=await redis_client.zrange(key,0,0,withscores=True)
            if oldest_attempt:
                retry_after=int(oldest_attempt[0][1]+(window_minutes*60)-current_time)
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail=f"Too many login attempts for '{username}'. Try again in '{retry_after} Seconds'", headers={"Retry-After":str(retry_after)})
            
        await redis_client.zadd(key,{str(current_time):current_time})
        await redis_client.expire(key,window_minutes*60)   
        return True 
    

    @staticmethod
    async def clear_login_rate_limit(username:str):
        """Clear rate limit counter for successful login"""                                
        redis_client=await redis_config.get_client()
        key=f"login attempts: {username}"
        await redis_client.delete(key)

    @staticmethod
    async def check_general_rate_limit(key:str,max_attempts:int=10,window_minutes:int=1):
        redis_client=await redis_config.get_client()
        full_key=f"rate_limit: {key}"
        current_time=int(time.time())
        window_start=current_time-(window_minutes*60)
        
        await redis_client.zremrangebyscore(full_key,0,window_start)

        current_attempts=await redis_client.zcard(full_key)

        if  current_attempts>= max_attempts:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later.",
                headers={"Retry-After": str(window_minutes * 60)}
            )


        await redis_client.zadd(full_key,{str(current_time):current_time})

        await redis_client.expire(full_key,window_minutes*60)
        return True