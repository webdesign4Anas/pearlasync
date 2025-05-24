from fastapi import Depends,HTTPException,APIRouter,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result,select
from app.database import get_db
from app.utils import hash,verify
from app import schemas,models,oauth2
from typing import Optional,List
router=APIRouter(tags=['Services'])

# Creating New Service
@router.post("/services",response_model=schemas.ServiceOut,status_code=status.HTTP_201_CREATED)
async def CreateService(service_data:schemas.ServiceCreate,db:AsyncSession=Depends(get_db),user:models.Users=Depends(oauth2.require_paid_business_owner)):
    service=models.Services(
    name=service_data.name,
    description=service_data.description,
    price=service_data.price ,
    category=service_data.category,
    owner_id=user.id
    )
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service


#Retrieving all services
@router.get("/services",response_model=List[schemas.ServiceOut],status_code=status.HTTP_200_OK)
async def list_services(skip:Optional[int]=None,limit:Optional[int]=None,category:Optional[str]=None,min_price:Optional[float]=None,max_price:Optional[float]=None,db:AsyncSession=Depends(get_db)): #they are query parameters ?category
    query:Result=select(models.Services)

    if category:
        query=query.where(models.Services.category==category)
    
    if min_price is not None:
         query=query.where(models.Services.price>=min_price)

    if max_price is not None:
         query=query.where(models.Services.price<=max_price)         
    query = query.offset(skip).limit(limit)
    result:Result=await db.execute(query)
    services=result.scalars().all()
    return services


#Retrieving one service
@router.get("/services/{service_id}",status_code=status.HTTP_200_OK,response_model=schemas.ServiceOut)
async def get_one_service(service_id:int , db:AsyncSession=Depends(get_db)):
    service:Result =await  db.execute(select(models.Services).where(models.Services.id==service_id))
    if not service.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Service not found")
    return service



#CreateServiceImages
@router.post("/services/{serviice_id}/images",response_model=schemas.ServiceImageOut)
async def upload_image(serviice_id:int,image_data:schemas.CreateServiceImage,db:AsyncSession=Depends(get_db),user:models.Users=Depends(oauth2.require_paid_business_owner)):
    service:Result=await db.execute(select(models.Services).where(models.Services.id==serviice_id,models.BusinessOwners.id==user.id))
    if not service.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="you are not the owner of the service")
    image=models.ServiceImage(
        description=image_data.description,
        image_url=image_data.image_url,
        service_id=image_data.service_id
    )
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image