from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from app import models
from typing import List




# query to get all the users in the database
async def get_users(db:AsyncSession,role=None,is_active=None,skip=0,limit=20):
    query=select(models.Users)
    if role:
        query=query.where(models.Users.role==role.upper())

    if is_active is not None:
        query = query.where(models.Users.is_active==is_active)

    return await db.scalars(query.offset(skip).limit(limit))


# query to get all the payments in the database

async def get_payments(db:AsyncSession,status=None,payment_type=None,skip=0,limit=20):
    query=select(models.Payments)

    if status:
        query=query.where(models.Payments.status==status)

    if payment_type:
        query=query.where(models.Payments.payment_type==payment_type)

    return await db.scalars(query.offset(skip).limit(limit))




# query to retrieve all business_owners for the admin 
async def get_business_owners(db:AsyncSession,status=None,business_type=None,skip=0,limit=20)-> List[models.BusinessOwners]:
    query=select(models.BusinessOwners)

    if status:
        query=query.where(models.BusinessOwners.status==status)

    if business_type:
        query=query.where(models.BusinessOwners.business_type==business_type)

    return await db.scalars(query.offset(skip).limit(limit))        



# Block selected User
async def get_user_by_id(id:int,db:AsyncSession):
    user=await db.scalar(select(models.Users).where(models.Users.id==id))
    return user



#retrieve all revenues for the admin
async def get_revenues(db:AsyncSession):
    total_sales=await db.scalar(select(func.sum(models.Purchase.amount)))
    
    total_commission=await db.scalar(select(func.sum(models.Purchase.commision)))

    return total_sales,total_commission