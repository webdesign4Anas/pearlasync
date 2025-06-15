from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models
from typing import Optional, List


async def create_service(db: AsyncSession, service: models.Services) -> models.Services:
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service


async def list_services(
    db: AsyncSession,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> List[models.Services]:
    query = select(models.Services)

    if category:
        query = query.where(models.Services.category == category)
    if min_price is not None:
        query = query.where(models.Services.price >= min_price)
    if max_price is not None:
        query = query.where(models.Services.price <= max_price)

    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


async def get_service_by_id(db: AsyncSession, service_id: int) -> Optional[models.Services]:
    result = await db.execute(select(models.Services).where(models.Services.id == service_id))
    return result.scalar_one_or_none()


async def create_service_image(db: AsyncSession, image: models.ServiceImage) -> models.ServiceImage:
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def is_owner_of_service(db: AsyncSession, service_id: int, user_id: int) -> bool:
    result = await db.execute(
        select(models.Services).where(models.Services.id == service_id, models.Services.owner_id == user_id)
    )
    return result.scalar_one_or_none() is not None
