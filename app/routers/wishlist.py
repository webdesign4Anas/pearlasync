from fastapi import Depends,APIRouter,HTTPException,status
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,Result
from app import schemas,models,oauth2
from app.database import get_db
router=APIRouter(tags=["WishList"])
from typing import List
#Adding Item to  User's Wishlist
@router.post("/wishlist", response_model=schemas.WishListItemOut, status_code=status.HTTP_201_CREATED)
async def create_wishlist(
    wishlist_item: schemas.WishListItem,
    db: AsyncSession = Depends(get_db),
    user: models.Users = Depends(oauth2.get_authenticated_user)
) -> models.Wishlists:
    # Check if item already exists
    existing_item = await db.scalar(
        select(models.Wishlists).where(
            models.Wishlists.service_id == wishlist_item.service_id,
            models.Wishlists.user_id == user.id
        )
    )
    
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item already exists in your wishlist"
        )

    # Create new item
    new_item = models.Wishlists(
        user_id=user.id,
        service_id=wishlist_item.service_id
    )
    
    # Persist to database
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    
    return new_item

#Viewing User's Specefic Wishlist
@router.get("/wishlist", response_model=List[schemas.WishListItemOut])
async def get_wishlist(
    db: AsyncSession = Depends(get_db),
    user: models.Users = Depends(oauth2.get_authenticated_user)
):
    # Ask the database nicely (and wait while playing)
    result = await db.execute(
        select(models.Wishlists)
        .options(joinedload(models.Wishlists.service).joinedload(models.Services.images))
        .where(models.Wishlists.user_id == user.id)
    )
    
    wishlist = result.scalars().all()
    
    # Add  pictures 
    for item in wishlist:
        service = item.service
        service.image_preview_url = service.images[0].image_url if service.images else None
    
    return wishlist


#Deleteing Item From User's WishList
@router.delete("/wishlist/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wishlist_item(
    item_id: int,
    user: models.Users = Depends(oauth2.get_authenticated_user),
    db: AsyncSession = Depends(get_db)
):
    # Get the wishlist item first
    result = await db.scalar(
        select(models.Wishlists).where(
            models.Wishlists.service_id == item_id,
            models.Wishlists.user_id == user.id
        )
    )

    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item Not Found"
        )
    
    # Delete the actual item (not the query result)
    await db.delete(result)
    await db.commit()
    
    return  # 204 No Content should return nothing










#@router.get("/wishlist",response_model=[schemas.ServiceSummaryOut],status_code=status.HTTP_200_OK)
#def view_wishlist(user:models.Users=Depends(oauth2.get_authenticated_user),db:Session=Depends(get_db)):
 #   query=db.query(models.Wishlists).filter(models.Wishlists.user_id==user.id).all()
  #  return query