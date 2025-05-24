from fastapi import FastAPI,Depends,HTTPException,status,APIRouter,Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func,select,Result
from  app.database import get_db
from app import schemas,models,oauth2
from typing import Optional,List




router=APIRouter(prefix="/admin",tags=["Admin"])

#retrieve all users for admin
@router.get("/users",status_code=status.HTTP_200_OK,response_model=list[schemas.UserOut])
async def retireve_all_users(
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
    role:Optional[str]=Query(None),
    is_active:Optional[bool]=Query(None),
    skip:int=0 ,
    limit:int=20,
    ):
    query=select(models.Users)
    if role:
        query=query.where(models.Users.role==role.upper())
    if is_active is not None:
        query=query.where(models.Users.is_active==is_active)

    result=await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

#retrieve all payments for admin
@router.get("/payments",status_code=status.HTTP_200_OK,response_model=List[schemas.PaymentOut])
async def get_all_payments(
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
    status:Optional[str]=Query(None),
    payment_type:Optional[str]=Query(None),
    skip:int=0 ,
    limit:int=20,
):
    query=select(models.Payments)
    if status:
        query=query.where(models.Payments.status==status.upper())

    if payment_type:
        query=query.where(models.Payments.payment_type==payment_type.upper())

    payment:Result=await db.execute(query.offset(skip).limit(limit))  

    return  payment.scalars().all()    

#retrieve all business_owner
@router.get("/business_owners",response_model=schemas.BusinessOwnersOut,status_code=status.HTTP_200_OK)
async def get_all_business_owners(
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
    status:Optional[str]=Query(None),
    business_type:Optional[str]=Query(None),
    skip:int=0 ,
    limit:int=20,
):
    query=select(models.BusinessOwners)
    
    if status:
        query=query.where(models.BusinessOwners.status==status.upper())

    if business_type:
        query=query.where(models.BusinessOwners.business_type==business_type.upper())

    results:Result=await db.execute(query.offset(skip).limit(limit))
    busines_owners=results.scalars().all()
    return busines_owners

#Approve business_owner
@router.put("/business_owners/{owner_id}/approve",status_code=status.HTTP_200_OK)
async def accept_user(
    owner_id:int,
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
):
    owner:Result=await db.execute(select(models.BusinessOwners).where(models.BusinessOwners.id==owner_id))
    if not owner.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Owner Not Found")
    if owner.status != "PAID":
        raise HTTPException(status_code=400, detail="Owner has not completed payment")

    owner.approved = True
    await db.commit()

    return {"detail": "Business approved"}
#Reject Business_Owner
@router.put("/business_owners/{owner_id}/reject",status_code=status.HTTP_200_OK)
async def accept_user(
    owner_id:int,
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
):
    owner:Result=await db.execute(select(models.BusinessOwners).where(models.BusinessOwners.id==owner_id))
    if not owner.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Owner Not Found")
    owner.status="Rejected"
    await db.commit()
    return {"detail": "Rejected Successfully"}  

#Blocking User
@router.put("/users/{user_id}/block",status_code=status.HTTP_200_OK)
async def block_user(
    user_id:int,
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
):
    user:Result=await db.execute(select(models.Users).where(models.Users.id==user_id))
    if not user.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    user.is_active=False
    await db.commit()
    return{f"User({user.email}) is Blocked Successfully"}

#Un-Blocking User
@router.put("/users/{user_id}/unblock",status_code=status.HTTP_200_OK)
async def block_user(
    user_id:int,
    db:AsyncSession=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
):
    user:Result=await db.execute(select(models.Users).where(models.Users.id==user_id))
    if not user.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    user.is_active=True
    await db.commit()
    return{f"User({user.email}) is Un-Blocked Successfully"}


#reviewing all revenues
@router.get("/revenues", status_code=status.HTTP_200_OK)
async def get_all_revenues(
    db: AsyncSession = Depends(get_db),
    admin: models.Users = Depends(oauth2.require_admin_user),
):
    # Async query for total sales
    total_sales_result = await db.execute(
        select(func.sum(models.Purchase.amount))
    )
    total_sales = total_sales_result.scalar() or 0.0  # Returns None if no rows → convert to 0.0

    # Async query for total commission (fixed typo from 'commision' to 'commission')
    total_commission_result = await db.execute(
        select(func.sum(models.Purchase.commission))  # Note: corrected field name
    )
    total_commission = total_commission_result.scalar() or 0.0

    return {
        "total_sales": total_sales,
        "total_commission": total_commission  # Consistent naming
    }