from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import hash
from app import models
from app import schemas


####################### User Data Layer Begins #############################################
# query to check if there is the new email matches email from the database
async def get_user_by_email(email:str,db:AsyncSession):
    result=await db.scalar(select(models.Users).where(models.Users.email==email))
    return result


#query to register a new user
async def create_user(data:schemas.UserCreate,db:AsyncSession,role:str):
    user=models.Users(
        email=data.email,
        password_hash=hash(data.password),
        role=role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

####################### User Data Layer Ends #############################################

# query  to check if there is the same business_name in the database
async def get_business_by_name(business_name:str,db:AsyncSession):
    result=await db.scalar(select(models.BusinessOwners).where(models.BusinessOwners.business_name==business_name))
    return result


# query to register business_owner 
async def create_business(data:schemas.BusinessOwnerCreate,db:AsyncSession):
    
    
        user=models.Users(
            email=data.email,
            password_hash=hash(data.password),
            role="BUSINESS_OWNER"
        )
        db.add(user)
        await db.flush()        #.flush() - "Send to Database BUT Don't Save Yet" don't save permanently
        
        business=models.BusinessOwners(
            id=user.id,
            business_type=data.business_type.upper(),
            business_name=data.business_name,
            description=data.description,
            status="PENDING"
        )
        db.add(business)
        await db.commit()
        return business,user