from sqlalchemy.orm import Session

from blooddonor.core.config import settings
from blooddonor.crud.crud_utility import user
from blooddonor.db.base import Base
from blooddonor.db.session import engine
from blooddonor.schemas.user import UserCreateBase

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    users = await user.get_by_mobile(db, mobile=settings.FIRST_SUPERUSER_MOBILE)
    if not users:
        user_in: UserCreateBase = UserCreateBase(
            full_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            mobile=settings.FIRST_SUPERUSER_MOBILE,
            nid=settings.FIRST_SUPERUSER_NID,
            gender=settings.FIRST_SUPERUSER_GENDER,
            district=settings.FIRST_SUPERUSER_DISTRICT,
            blood_group=settings.FIRST_SUPERUSER_BLOOD_GROUP,
            studentship_status=settings.FIRST_SUPERUSER_STUDENTSHIP_STATUS,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            is_admin=True,
        )
        await user.create(db, obj_in=user_in)
    await db.close()
