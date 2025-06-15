from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import schemas, oauth2, models
from app.services.purchase_services import handle_purchase

router = APIRouter(tags=["Purchases"])

@router.post("/purchase", response_model=schemas.PurchaseOut, status_code=status.HTTP_201_CREATED)
async def purchase_service(
    purchase_data: schemas.PurchaseCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user: models.Users = Depends(oauth2.get_authenticated_user)
):
    return await handle_purchase(purchase_data, user, db, background_tasks)
