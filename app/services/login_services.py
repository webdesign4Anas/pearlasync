from fastapi import status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import login_repository
from app import utils
from app.oauth2 import create_access_token
async def login_user(user_credentials:OAuth2PasswordRequestForm,db:AsyncSession):
    user=await login_repository.get_user_by_email(user_credentials.username,db)

    if not user or not utils.verify(user_credentials.password,user.password_hash):

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="credentials not matched")
    
    access_token=create_access_token(data={"user_id":user.id,"role":user.role})
    
    return{
        "access_token":access_token, "token_type":"bearer","role":user.role,"id":user.id
    }

    
