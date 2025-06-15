from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, models
from app.repositories import purchase_repository
from fastapi_mail import FastMail, MessageSchema, MessageType
from app.config import conf

async def handle_purchase(purchase_data: schemas.PurchaseCreate, user: models.Users, db: AsyncSession, background_tasks: BackgroundTasks):
    service = await purchase_repository.get_service_by_id(purchase_data.service_id, db)
    if not service:
        raise HTTPException(status_code=404, detail="Service Not Found")

    category = service.category
    if category == "dress":
        if service.quantity <= 0:
            raise HTTPException(status_code=400, detail="Out of Stock")
        service.quantity -= 1

    if category in ["makeup", "photographer"]:
        if not purchase_data.booking_date:
            raise HTTPException(status_code=400, detail="Booking Date Required")

        exists = await purchase_repository.check_service_booking_exists(purchase_data.service_id, purchase_data.booking_date, db)
        if exists:
            raise HTTPException(status_code=400, detail="Already booked at this time")

        await purchase_repository.add_service_booking(service.id, user.id, purchase_data.booking_date, db)

    commision = service.price * 0.10
    purchase = await purchase_repository.create_purchase(
        user_id=user.id,
        service_id=service.id,
        amount=service.price,
        commision=commision,
        booking_date=purchase_data.booking_date,
        db=db
    )

    await purchase_repository.add_notification(
        business_owner_id=service.owner_id,
        message=f"New purchase for service {service.name} by user {user.email}",
        db=db
    )

    await db.commit()
    await db.refresh(purchase)

    business_owner = await purchase_repository.get_user_by_id(service.owner_id, db)
    if business_owner:
        message = MessageSchema(
            subject="New Purchase Notification",
            recipients=[business_owner.email],
            body=f"Hello {business_owner.email}, you received a purchase for service: {service.name}.",
            subtype=MessageType.plain,
        )
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)

    return purchase
