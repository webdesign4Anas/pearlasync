from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.repositories import payment_repository

async def process_business_signup_payment(user:models.Users,db:AsyncSession,payment_data:schemas.PaymentRequest):
    owner:models.BusinessOwners=await payment_repository.get_business_owner_by_id(user.id,db)

    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Business owner not found")
    
    if owner.status=="PAID":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already paid")
    
        # Payment validation logic
    if len(payment_data.card_nubmer)!= 16 or payment_data.amount<200:
        payment_status="FAILED"
    else:
        payment_status="SUCCESS"    
    # Create payment model
    payment=models.Payments(
        user_id=user.id,
        amount=payment_data.amount,
        payment_type="SIGNUP",
        status=payment_status
    )
    #add to database

    await payment_repository.create_payment(payment,db)

    if payment_status !="SUCCESS":
        owner.status="Rejected"
        owner.approved=False
        raise HTTPException(status_code=400, detail="Payment Failed")
    # Mark as paid
    owner.status = "PAID"
    owner.approved = True
    await db.commit()

    return {
        "message": "Payment is successful and the account is activated now",
        "PaymentId": payment.id,
        "Status": payment.status
    }