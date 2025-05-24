from fastapi import  FastAPI,APIRouter,status
from fastapi import FastAPI
from app.routers import users,auth,register_routes,wishlist,services,admin,payment,notifications,purchases
app=FastAPI()




app.include_router(users.router)
app.include_router(auth.router)
app.include_router(register_routes.router)
app.include_router(wishlist.router)
app.include_router(services.router)
app.include_router(admin.router)
app.include_router(payment.router)
app.include_router(notifications.router)
app.include_router(purchases.router)

@app.get("/")
async def root():
    return{"message":"Hello World"}






