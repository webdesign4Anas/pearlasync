from fastapi import Request,Depends
from app.services import rate_limit
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

async def rate_limit_login(user_credentials:OAuth2PasswordRequestForm=Depends()):
    """
    Dependency to check login rate limit before processing login
    This runs BEFORE the login attempt is processed
    """
    await rate_limit.RateLimitService.check_login_rate_limit(user_credentials.username)
    return user_credentials


async def rate_limit_by_ip(request:Request):
    client_ip=request.client.host

    await rate_limit.RateLimitService.check_general_rate_limit(f"ip {client_ip}",max_attempts=10,window_minutes=1)

    return True
