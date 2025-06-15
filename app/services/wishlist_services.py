from app import models
from app.repositories import wishlist_repository  
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status


async def add_to_wishlist(db:AsyncSession,service_id:int,user:models.Users):
    existing=await wishlist_repository.get_wishlist_item(service_id,user.id,db)
    print(existing)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Item already exists in your wishlist")
    item=models.Wishlists(
        user_id=user.id,
        service_id=service_id
    )
    return await wishlist_repository.add_wishlist_item(db,item)



async def get_user_wishlist(db:AsyncSession,user:models.Users):
    wishlists=await wishlist_repository.get_all_user_wishlist(user.id,db)

    for item in wishlists:
        service = item.service
        # Safer way to get first image
        service.image_preview_url = (
            service.images[0].image_url 
            if service.images and len(service.images) > 0 
            else None
        )
    return wishlists

    
    

async def remove_from_wishlist(db: AsyncSession, user: models.Users, service_id: int):
    item = await wishlist_repository.get_wishlist_item(service_id, user.id, db)
    if not item:
        raise ValueError("Item not found")
    await wishlist_repository.delete_wishlist_item(db, item)    