from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.database import get_db
from app import  schemas
from app.services import login_services
from app.services.rate_limit import RateLimitService
from app.dependencies.rate_limit import rate_limit_login


router = APIRouter(tags=["Authentication"])


@router.post(
    "/login",
    response_model=schemas.Token,
    status_code=status.HTTP_201_CREATED,
)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(rate_limit_login), db: AsyncSession = Depends(get_db)):
    """
    User login endpoint with rate limiting
    - Limited to 5 attempts per username per 15 minutes
    - Rate limit is cleared on successful login
    """
    try:
         result=await login_services.login_user(user_credentials, db)
         # On successful login, clear the rate limit counter
         await RateLimitService.clear_login_rate_limit(user_credentials.username)
         return result
    except HTTPException as e:
         raise e
         



