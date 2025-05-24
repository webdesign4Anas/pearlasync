from fastapi import Depends,HTTPException,APIRouter,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,Result
from app.database import get_db
from app.utils import hash,verify
from app import schemas,models,oauth2

router=APIRouter(tags=['Authentication'])

# Registeration for Users
@router.post("/register/user",status_code=status.HTTP_201_CREATED,response_model=schemas.Token)
async def register_user(data:schemas.UserCreate,db:AsyncSession=Depends(get_db)):
    result_email:Result=await db.scalar(select(models.Users).where(models.Users.email==data.email))
    if result_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email Already Exists")

    user= models.Users(
        email=data.email,
        password_hash=hash(data.password),
        role="USER",
        )
    db.add(user)
    await db.commit()
    await db.refresh(user)
     
    access_token=oauth2.create_access_token(data={"user_id":str(user.id)})
    return{"access_token":access_token,"token_type":"Bearer","role":user.role,"id":user.id}

#Register for Business_Owners
@router.post("/register/business",status_code=status.HTTP_201_CREATED,response_model=schemas.Token)
async def register_business(data:schemas.BusinessOwnerCreate,db:AsyncSession=Depends(get_db)):
    result_email:Result=await db.execute(select(models.Users).where(models.Users.email==data.email))
    if result_email.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email Already Exists")
    result_business_name:Result=await db.execute(select(models.BusinessOwners).where(models.BusinessOwners.business_name==data.business_name))
    if result_business_name.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Business Name Already Exists")

    user= models.Users(
        email=data.email,
        password_hash=hash(data.password),
        role="BUSINESS_OWNER",
        )
    db.add(user)
    await db.commit()
    await db.refresh(user)
     
    business=models.BusinessOwners(
        id=user.id,
        business_type=data.business_type.upper(),
        business_name=data.business_name,
        description=data.description,
        status="PENDING"
    )

    db.add(business)
    await db.commit()
    await  db.refresh(business)

    access_token=oauth2.create_access_token(data={"user_id":str(user.id)})
    return{"access_token":access_token,"token_type":"Bearer","status": "PENDING_APPROVAL","role":user.role,"id":user.id}
    
    
    




