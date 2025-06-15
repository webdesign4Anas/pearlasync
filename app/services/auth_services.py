from app import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import auth_repository
from fastapi import HTTPException,status
from app.oauth2 import create_access_token

# Logic For Registering The User To The Database
async def register_user(data:schemas.UserCreate,db:AsyncSession):
    existing_user= await auth_repository.get_user_by_email(data.email,db)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email Already Exists")
    
    user=await auth_repository.create_user(data,db,role="USER")

    access_token=create_access_token(data={"user_id":str(user.id)})
    
    return{
        "access_token":access_token,
        "token_type":"Bearer",
        "role":user.role,
        "id":user.id
    }








# Logic For Registering The Business_owner To The Database

async def register_business(data:schemas.BusinessOwnerCreate,db:AsyncSession):
    if await auth_repository.get_user_by_email(data.email, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exists")
    
    existing_business= await auth_repository.get_business_by_name(data.business_name,db)
    if existing_business:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Business Name Already Exists")
    
    business,user= await auth_repository.create_business(data,db)
    access_token=create_access_token(data={"user_id":str(user.id)})
    return{
        "access_token":access_token,
        "token_type":"Bearer",
        "role":user.r,
        "id":user.id,
        "status":"PENDING"
    }
    

 