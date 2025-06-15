from app.repositories import admin_repository
from fastapi import HTTPException,status



async def get_all_users(db,role,is_active,skip,limit):
    return await admin_repository.get_users(db,role,is_active,skip,limit)


async def get_all_payments(db,status,payment_type,skip,limit):
    return await admin_repository.get_payments(db,status,payment_type,skip,limit)


async def get_all_business_owners(db,status,business_type,skip,limit):
    return await admin_repository.get_business_owners(db,status,business_type,skip,limit)


async def block_user(id,db):
    user=await admin_repository.get_user_by_id(id,db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    user.is_active=False
    await db.commit()
    return{f"User({user.email}) is Blocked Successfully"}



async def unblock_user(id,db):
    user=await admin_repository.get_user_by_id(id,db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    user.is_active=True
    await db.commit()
    return{f"User({user.email}) is Un-Blocked Successfully"}



async def get_revenue_summary(db):
    total_sales,total_commission=await admin_repository.get_revenues(db)
    return{
        "total_sales":total_sales,
        "total_commission":total_commission
    }
