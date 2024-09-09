from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from blooddonor.core.config import settings

# engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
