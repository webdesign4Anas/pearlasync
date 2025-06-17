from pydantic import BaseModel,EmailStr
from typing import Optional,Literal
from datetime import datetime


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class TokenData(BaseModel):
    id: Optional[int]


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    id: int
    class Config:
        from_attributes = True # In Pydantic v2, formerly orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str
   

class BusinessOwnerCreate(UserCreate):
    business_type: Literal['MAKEUP_ARTIST', 'PHOTOGRAPHER', 'DRESS_RETAILER']
    business_name:str
    description:Optional[str]=None


class ServiceImageOut(BaseModel):
    id: int
    description: str
    image_url: str
    uploaded_at: str

    class Config:
        from_attributes = True

class ServiceCreate(BaseModel):
    name:str
    description:str
    price:float
    category:Literal["dress","makeup","photographer"]

class ServiceOut(ServiceCreate):
    id: int
    name: str
    description: str
    price: float
    category: str
    owner_id: int
    image_preview_url: Optional[str] = None

    class Config:
        orm_mode = True


class CreateServiceImage(BaseModel):
    image_url:str
    description:str
    service_id:int

class ServiceSummaryOut(BaseModel):
    id:int
    name:str
    price:float
    image_preview_url:Optional[str]=None
    class Config:
        from_attributes=True

class WishListItem(BaseModel):
    service_id:int

class WishListItemOut(BaseModel):
    id: int
    service: ServiceOut

    class Config:
        orm_mode = True

class PaymentRequest(BaseModel):
    card_nubmer:str
    amount:float


class UserOut(BaseModel):
    id:int
    email:str
    role:str
    is_active:bool
    created_at:datetime
    class Config:
        from_attributes=True

class PaymentOut(BaseModel):
    id:int
    user_id:int
    amount:float
    status:str
    payment_type:str
    created_at:datetime
    class Config:
        from_attributes=True

class BusinessOwnersOut(BaseModel):
    id:int
    business_type:str
    status:str
    business_name:str
    class Config:
        from_attributes=True

class PurchaseCreate(BaseModel):
    service_id:int
    booking_date:Optional[datetime]=None

class PurchaseOut(BaseModel):
    id:int
    user_id:int
    service_id:int
    commission:float
    amount:float
    booking_date:Optional[datetime]
    created_at:datetime
    class Config:
        from_attributes=True


class NotificationsOut(BaseModel):
    id:int
    message:str
    is_read:bool
    created_at:datetime
    class Config:
        from_attributes=True
