from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas, models, oauth2
from app.database import get_db
from app.services import users_services

router = APIRouter(prefix="/users", tags=["Authentication"])

@router.get("/my-purchases", response_model=List[schemas.PurchaseOut])
async def get_user_purchases(
    db: AsyncSession = Depends(get_db),
    user: models.Users = Depends(oauth2.get_authenticated_user)
):
    return await users_services.list_user_purchases(db, user.id)
