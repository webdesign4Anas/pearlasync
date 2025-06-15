from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import schemas, models, oauth2
from app.services import wishlist_services as wishlist_service
from typing import List

router = APIRouter(tags=["WishList"])

@router.post("/wishlist",status_code=status.HTTP_201_CREATED)
async def create_wishlist(wishlist_item: schemas.WishListItem, db: AsyncSession = Depends(get_db), user: models.Users = Depends(oauth2.get_authenticated_user)):
    try:
        return await wishlist_service.add_to_wishlist(db, wishlist_item.service_id,user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/wishlist")
async def get_wishlist(db: AsyncSession = Depends(get_db), user: models.Users = Depends(oauth2.get_authenticated_user)):
    return await wishlist_service.get_user_wishlist(db, user)

@router.delete("/wishlist/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wishlist_item(item_id: int, db: AsyncSession = Depends(get_db), user: models.Users = Depends(oauth2.get_authenticated_user)):
    try:
        await wishlist_service.remove_from_wishlist(db, user, item_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
