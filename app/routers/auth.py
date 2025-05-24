from fastapi import HTTPException,status,APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,Result
from app.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models,schemas,utils,oauth2
router=APIRouter(tags=["Authentication"])

@router.post("/login",response_model=schemas.Token,status_code=status.HTTP_201_CREATED)
async def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:AsyncSession=Depends(get_db)):
    result_user:Result=await db.execute(select(models.Users).where(models.Users.email==user_credentials.username))
    user=result_user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="credentials not matched")
    if not utils.verify(user_credentials.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="credentials not matched")
    access_token=oauth2.create_access_token(data={"user_id":user.id,"role":user.role})
    return{"access_token":access_token, "token_type":"bearer","role":user.role,"id":user.id}



