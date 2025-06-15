from fastapi import HTTPException,status,APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models,schemas,utils,oauth2
from app.services import login_services
router=APIRouter(tags=["Authentication"])

@router.post("/login",response_model=schemas.Token,status_code=status.HTTP_201_CREATED)
async def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:AsyncSession=Depends(get_db)):
    return await login_services.login_user(user_credentials,db)


