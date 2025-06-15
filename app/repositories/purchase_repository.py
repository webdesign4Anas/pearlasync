from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models
from datetime import date

async def get_service_by_id(service_id: int, db: AsyncSession):
    return await db.scalar(select(models.Services).where(models.Services.id == service_id))

async def check_service_booking_exists(service_id: int, booking_date: date, db: AsyncSession):
   return await db.scalar(
    select(models.ServiceBooking).where(
        models.ServiceBooking.service_id == service_id,
        models.ServiceBooking.booking_date == booking_date
    )
)

async def add_service_booking(service_id: int, user_id: int, booking_date: date, db: AsyncSession):
    booking = models.ServiceBooking(service_id=service_id, user_id=user_id, booking_date=booking_date)
    db.add(booking)
    return booking

async def create_purchase(user_id: int, service_id: int, amount: float, commision: float, booking_date, db: AsyncSession):
    purchase = models.Purchase(
        user_id=user_id,
        service_id=service_id,
        amount=amount,
        commission=commision,
        booking_date=booking_date
    )
    db.add(purchase)
    return purchase

async def add_notification(business_owner_id: int, message: str, db: AsyncSession):
    notification = models.Notification(business_owner_id=business_owner_id, message=message)
    db.add(notification)
    return notification

async def get_user_by_id(user_id: int, db: AsyncSession):
    return await db.scalar(select(models.Users).where(models.Users.id == user_id))
