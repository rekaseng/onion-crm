from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from config import settings

engine = create_async_engine(settings.POSTGRES_CONNECTION_STRING, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

EngineSync = create_engine(settings.POSTGRES_SYNC_CONNECTION_STRING, pool_pre_ping=True)
SessionLocalSync = sessionmaker(autocommit=False, autoflush=False, bind=EngineSync)
