from fastapi import Depends,HTTPException,APIRouter,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,Result
from app.database import get_db
from app.utils import hash,verify
from app import schemas,models,oauth2
from app.services import auth_services
router=APIRouter(tags=['Authentication'])

# Registeration for Users
@router.post("/register/user",status_code=status.HTTP_201_CREATED,response_model=schemas.Token)
async def register_user(data:schemas.UserCreate,db:AsyncSession=Depends(get_db)):
    return await auth_services.register_user(data,db)

#Register for Business_Owners
@router.post("/register/business",status_code=status.HTTP_201_CREATED,response_model=schemas.Token)
async def register_business(data:schemas.BusinessOwnerCreate,db:AsyncSession=Depends(get_db)):
    return await auth_services.register_business(data,db)
    
    
    




