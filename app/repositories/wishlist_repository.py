from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models
from sqlalchemy.orm import joinedload


async def get_all_user_wishlist(user_id:int,db:AsyncSession):
    items=await db.scalars(select(models.Wishlists).options(joinedload(models.Wishlists.service).joinedload(models.Services.images)).where(models.Wishlists.user_id==user_id))
    return items.unique().all()




async def get_wishlist_item(service_id:int,user_id:int,db:AsyncSession):
    wishlist_item=await db.scalar(select(models.Wishlists).where(models.Wishlists.service_id==service_id,models.Wishlists.user_id==user_id))
    return wishlist_item




async def add_wishlist_item(db:AsyncSession,wishlist_item:models.Wishlists):
    db.add(wishlist_item)

    await db.commit()

    await db.refresh(wishlist_item)

    return wishlist_item


async def delete_wishlist_item(db:AsyncSession,wishlist_item:models.Wishlists):
   await db.delete(wishlist_item)
   await db.commit()



