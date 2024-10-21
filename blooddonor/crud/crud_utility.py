import datetime
import uuid
from typing import Any, override

from blooddonor.core import security
from blooddonor.models.usermodel import DonorModel, ProfileModel
from blooddonor.schemas.user import (
    UpdateProfile,
    UserCreateBase,
    UserProfile,
    UserUpdateBase,
)
from pydantic import EmailStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession as Session

from .base import CRUDBase


# CRUD functionalities for Normal User models
class CRUDUser(CRUDBase[DonorModel, UserCreateBase, UserUpdateBase]):
    async def get_by_mobile(self, db: Session, mobile: str) -> DonorModel | None:
        query = select(DonorModel).where(DonorModel.mobile == mobile)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_student_id(
        self, db: Session, student_id: str
    ) -> DonorModel | None:
        query = select(DonorModel).where(DonorModel.student_id == student_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_email(self, db: Session, email: str) -> DonorModel | None:
        query = select(DonorModel).where(DonorModel.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_user_count(self, db: Session) -> dict | None:
        # Query for total users
        total_query = select(func.count(DonorModel.id))
        total_result = await db.execute(total_query)
        total_count = total_result.scalar()

        # Query for active users
        active_query = select(func.count(DonorModel.id)).where(
            DonorModel.is_available == bool(True)
        )
        active_result = await db.execute(active_query)
        active_count = active_result.scalar()

        # new donors this month
        this_month = datetime.datetime.now(datetime.UTC).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        new_reg_query = select(func.count(DonorModel.id)).where(
            DonorModel.created_on >= this_month
        )
        new_donors_result = await db.execute(new_reg_query)
        new_donors_count = new_donors_result.scalar()

        # Calculate the percentage of each blood group
        blood_group_query = select(
            DonorModel.blood_group, func.count(DonorModel.id)
        ).group_by(DonorModel.blood_group)
        blood_group_result = await db.execute(blood_group_query)
        blood_group_data = blood_group_result.all()

        blood_group_percentages = {
            blood_group: round((count / total_count), 2) * 100 if total_count > 0 else 0
            for blood_group, count in blood_group_data
        }

        # Return both counts in a dictionary
        return {
            "total_user_count": total_count,
            "active_user_count": active_count,
            "new_donors_this_month": new_donors_count,
            "blood_group_percentages": blood_group_percentages,
        }

    @override
    async def create(self, db: Session, obj_in: UserCreateBase) -> DonorModel | None:
        db_obj: DonorModel = DonorModel(**obj_in.model_dump(exclude_unset=True))  # noqa
        hashed_password = await security.get_password_hash(obj_in.password)
        db_obj.hashed_password = hashed_password
        # profile data
        profile_obj = ProfileModel(donor=db_obj)  # noqa
        db.add(profile_obj)
        # adding user to database
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @override
    async def update(
        self,
        db: Session,
        db_obj: DonorModel,
        obj_in: UserUpdateBase | dict[str, Any],
    ) -> DonorModel:
        if isinstance(obj_in, dict):
            user_data = obj_in
        else:
            user_data = obj_in.model_dump(exclude_unset=True)
        if user_data.get("password"):
            hashed_password = await security.get_password_hash(
                user_data.get("password")
            )
            del user_data["password"]
            user_data["hashed_password"] = hashed_password
        if "profile" in user_data and isinstance(user_data["profile"], dict):
            profile_data = {key: str(val) for key, val in user_data["profile"].items()}
            user_data["profile"] = ProfileModel(**profile_data)  # noqa
        return await super().update(db, db_obj=db_obj, obj_in=user_data)

    async def authenticate(
        self, db: Session, *, mobile: str = None, email: EmailStr = None, password: str
    ) -> DonorModel | None:
        if mobile:
            users = await self.get_by_mobile(db, mobile=mobile)
        else:
            users = await self.get_by_email(db, email=email)

        if not users:
            return None

        if not await security.verify_password(password, users.hashed_password):
            return None
        return users

    async def is_active(self, user: DonorModel) -> bool:
        return user.is_active

    async def is_superuser(self, user: DonorModel) -> bool:
        return user.is_superuser

    async def is_admin(self, user: DonorModel) -> bool:
        return user.is_admin


class CRUDProfile(CRUDBase[ProfileModel, UserProfile, UpdateProfile]):
    @override
    async def get(self, db: Session, donor_id: uuid.UUID) -> ProfileModel | None:
        query = select(self.model).where(self.model.donor_id == donor_id)
        result = await db.execute(query)
        return result.scalars().first()


user = CRUDUser(DonorModel)
profile = CRUDProfile(ProfileModel)
