from fastapi import APIRouter,FastAPI,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result,select
from app.database import get_db
from app import models,schemas,oauth2

router=APIRouter(tags=['Payment'])

#payment for signup
@router.post("/business/payment",status_code=status.HTTP_202_ACCEPTED)
async def business_payment_signup(payment_data:schemas.PaymentRequest,db:AsyncSession=Depends(get_db),user:models.Users=Depends(oauth2.require_business_owner)):
    result_owner=await db.execute(select(models.BusinessOwners).where(models.BusinessOwners.id==user.id))
    owner=result_owner.scalar_one_or_none()
    if owner.status=="PAID":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User Already Paid")

    if len(payment_data.card_nubmer)!=16:
        payment_status="FAILED"
    
    elif payment_data.amount<200:
        payment_status="FAILED"
    
    else: payment_status="SUCCESS"

    payment=models.Payments(
        user_id=user.id,
        amount=payment_data.amount,
        payment_type="SIGNUP",
        status=payment_status
    )
    db.add(payment)

    if payment_status=="SUCCESS":
        owner.status="PAID"
        owner.approved=True
    await db.commit()    
    if payment_status!="SUCCESS":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Payment Failed")
    

    return{"message":"Payment is successfull and the account is actived now","PaymentId":payment.id,"Status":payment.status}

       

        
