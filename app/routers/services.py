from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.database import get_db
from app import schemas, models, oauth2
from app.services import service_services

router = APIRouter(tags=["Services"])


@router.post("/services", response_model=schemas.ServiceOut, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: schemas.ServiceCreate,
    db: AsyncSession = Depends(get_db),
    user: models.Users = Depends(oauth2.require_paid_business_owner)
):
    return await service_services.create_service(service_data, db, user)


@router.get("/services", response_model=List[schemas.ServiceOut], status_code=status.HTTP_200_OK)
async def get_services(
    skip: Optional[int] = Query(default=0),
    limit: Optional[int] = Query(default=10),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    return await service_services.list_services(
        db,
        skip=skip,
        limit=limit,
        category=category,
        min_price=min_price,
        max_price=max_price
    )


@router.get("/services/{service_id}", response_model=schemas.ServiceOut, status_code=status.HTTP_200_OK)
async def get_service(service_id: int, db: AsyncSession = Depends(get_db)):
    return await service_services.get_one_service(db, service_id)


@router.post("/services/{service_id}/images", response_model=schemas.ServiceImageOut)
async def create_service_image(
    service_id: int,
    image_data: schemas.CreateServiceImage,
    db: AsyncSession = Depends(get_db),
    user: models.Users = Depends(oauth2.require_paid_business_owner)
):
    return await service_services.upload_service_image(db, service_id, image_data, user)
