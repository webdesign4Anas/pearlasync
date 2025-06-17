# main.py

from fastapi import FastAPI,Depends,Request
from app.dependencies.rate_limit import rate_limit_by_ip
from contextlib import asynccontextmanager
# Your application's router imports
from app.routers import auth, login, users, wishlist, services, admin, payment, notifications, purchases
from app.redis_config import redis_config

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Startup
    print(" Pearl API is starting up...")
    yield
    # Shutdown
    print(" Pearl API is shutting down...")
    await redis_config.close()

app = FastAPI(lifespan=lifespan)


# Include all your application routers
app.include_router(users.router)
app.include_router(login.router)
app.include_router(auth.router)
app.include_router(wishlist.router)
app.include_router(services.router)
app.include_router(admin.router)
app.include_router(payment.router)
app.include_router(notifications.router)
app.include_router(purchases.router)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Hello World, the Pearl API is running!"}


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    try:
        # Test Redis connection
        redis_client = await redis_config.get_client()
        await redis_client.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "redis": redis_status
    }



@app.get("/test-rate-limit", tags=["Testing"])
async def test_rate_limit(
    request: Request,
    _: bool = Depends(rate_limit_by_ip)
):
    """
    Endpoint specifically for testing IP rate limiting.
    Limited to 5 requests per IP per minute for easy testing.
    """
    client_ip = request.client.host
    import time
    return {
        "message": "Rate limit test endpoint",
        "your_ip": client_ip,
        "timestamp": int(time.time()),
        "limit": "5 requests per minute per IP"
    }