from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.repositories import service_repoository


async def create_service(service_data: schemas.ServiceCreate, db: AsyncSession, user: models.Users):
    service = models.Services(
        name=service_data.name,
        description=service_data.description,
        price=service_data.price,
        category=service_data.category,
        owner_id=user.id
    )
    return await service_repoository.create_service(db, service)


async def list_services(db: AsyncSession, **filters):
    return await service_repoository.list_services(db, **filters)


async def get_one_service(db: AsyncSession, service_id: int):
    service = await service_repoository.get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service


async def upload_service_image(
    db: AsyncSession,
    service_id: int,
    image_data: schemas.CreateServiceImage,
    user: models.Users
):
    is_owner = await service_repoository.is_owner_of_service(db, service_id, user.id)
    if not is_owner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of the service")

    image = models.ServiceImage(
        description=image_data.description,
        image_url=image_data.image_url,
        service_id=service_id
    )
    return await service_repoository.create_service_image(db, image)
