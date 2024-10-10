from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from blooddonor.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
