from sqlalchemy.ext.asyncio import AsyncSession as Session

from blooddonor.core.config import settings
from blooddonor.crud.crud_utility import user
from blooddonor.db.base import Base  # noqa
from blooddonor.db.session import engine  # noqa
from blooddonor.schemas.user import UserCreateBase

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines

    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    users = await user.get_by_mobile(db, mobile=settings.FIRST_SUPERUSER_MOBILE)
    if not users:
        user_in: UserCreateBase = UserCreateBase(
            full_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            mobile=settings.FIRST_SUPERUSER_MOBILE,
            department=settings.FIRST_SUPERUSER_DEPARTMENT,
            student_id=settings.FIRST_SUPERUSER_STUDENT_ID,
            gender=settings.FIRST_SUPERUSER_GENDER,
            district=settings.FIRST_SUPERUSER_DISTRICT,
            blood_group=settings.FIRST_SUPERUSER_BLOOD_GROUP,
            academic_year=settings.FIRST_SUPERUSER_ACADEMIC_YEAR,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            is_admin=True,
        )
        await user.create(db, obj_in=user_in)
    await db.close()  # noqa
