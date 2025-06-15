from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import models,schemas,oauth2
from app.services import paymnet_services
router=APIRouter(tags=['Payment'])

#payment for signup
@router.post("/business/payment",status_code=status.HTTP_202_ACCEPTED)
async def business_payment_signup(payment_data:schemas.PaymentRequest,db:AsyncSession=Depends(get_db),user:models.Users=Depends(oauth2.require_business_owner)):
    return await paymnet_services.process_business_signup_payment(user,db,payment_data)
       

        
