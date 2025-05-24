from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from sqlalchemy.orm import declarative_base,sessionmaker
from app.config import settings

SQL_ALCHEMY_URL=f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine=create_async_engine(SQL_ALCHEMY_URL,echo=True) # that is what connect the postgresql with sqlalchemy/# (echo) Optional: logs SQL queries for debugging

SessionLocal=async_sessionmaker(autoflush=False,autocommit=False,bind=engine,class_=AsyncSession,expire_on_commit=False)   # responsible for talking to the database 
                                                                                                                     #expire_on_commit=False (no need for additinal queres)
Base=declarative_base()                                                    # serve as base class for all the orm models that all the models will inherit from then turned into tables

async def get_db():                                                              # a dependency

    async with SessionLocal() as db:
        try:
            yield db                                                          # yield db: Passes the session to path operation functions.
        finally:
           await db.close()    


