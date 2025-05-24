from fastapi import HTTPException,status,APIRouter,Depends
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result,select
from app.database import get_db
from app import schemas,oauth2,models
from typing import List
router=APIRouter(prefix="/users",tags=["Authentication"])


#review user-purchases
@router.get("/my-purchases", response_model=List[schemas.PurchaseOut])
async def get_user_purchases(
    db: AsyncSession = Depends(get_db),
    user: models.Users = Depends(oauth2.get_authenticated_user)
):
    purchases:Result=await db.execute(select(models.Purchase).where(models.Purchase.user_id==user.id))
    purchases_list=purchases.scalars().all()
    return purchases_list
