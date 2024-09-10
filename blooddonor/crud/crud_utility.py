import uuid
from typing import Any, override

from sqlalchemy import select
from sqlalchemy.orm import Session

from blooddonor.core import security
from blooddonor.models.usermodel import DonorModel, ProfileModel
from blooddonor.schemas.user import (
    UpdateProfile,
    UserCreateBase,
    UserProfile,
    UserUpdateBase,
)

from ..core.config import settings
from .base import CRUDBase


# CRUD functionalities for Normal User models
class CRUDUser(CRUDBase[DonorModel, UserCreateBase, UserUpdateBase]):
    async def get_by_mobile(self, db: Session, mobile: str) -> DonorModel | None:
        query = select(DonorModel).where(DonorModel.mobile == mobile)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_email(self, db: Session, email: str) -> DonorModel | None:
        query = select(DonorModel).where(DonorModel.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_blood_group(
        self, db: Session, *, blood_group: str, skip: int = 0, limit: int = 100
    ) -> list[DonorModel]:
        query = (
            select(self.model)
            .where(self.model.blood_group == blood_group)
            .offset(skip)
            .limit(limit)
        )
        results = await db.execute(query)
        return results.scalars().all()

    async def get_by_gender(
        self, db: Session, *, gender: str, skip: int = 0, limit: int = 100
    ) -> list[DonorModel]:
        query = (
            select(self.model)
            .where(self.model.gender == gender)
            .offset(skip)
            .limit(limit)
        )
        results = await db.execute(query)
        return results.scalars().all()

    async def get_by_district(
        self, db: Session, *, district: str, skip: int = 0, limit: int = 100
    ) -> list[DonorModel]:
        query = (
            select(self.model)
            .where(self.model.district == district)
            .offset(skip)
            .limit(limit)
        )
        results = await db.execute(query)
        return results.scalars().all()

    async def get_by_studentship_status(
        self, db: Session, *, studentship_status: str, skip: int = 0, limit: int = 100
    ) -> list[DonorModel]:
        query = (
            select(self.model)
            .where(self.model.studentship_status == studentship_status)
            .offset(skip)
            .limit(limit)
        )
        results = await db.execute(query)
        return results.scalars().all()

    async def get_by_availability(
        self, db: Session, *, availability: bool, skip: int = 0, limit: int = 100
    ) -> list[DonorModel]:
        query = (
            select(self.model)
            .where(self.model.is_available == availability)
            .offset(skip)
            .limit(limit)
        )
        results = await db.execute(query)
        return results.scalars().all()

    async def get_by_name(
        self, db: Session, *, name: str, skip: int = 0, limit: int = 100
    ) -> list[DonorModel]:
        query = (
            select(self.model)
            .where(self.model.full_name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
        )
        results = await db.execute(query)
        return results.scalars().all()

    @override
    async def create(self, db: Session, obj_in: UserCreateBase) -> DonorModel | None:
        db_obj: DonorModel = DonorModel(**obj_in.model_dump(exclude_unset=True))  # noqa
        hashed_password = await security.get_password_hash(obj_in.password)
        db_obj.hashed_password = hashed_password
        # profile data
        ProfileModel(donor=db_obj)  # noqa
        # adding user to database
        db.add(db_obj)
        await db.commit()  # noqa
        await db.refresh(db_obj)  # noqa
        return db_obj

    @override
    async def update(
        self, db: Session, db_obj: DonorModel, obj_in: UserUpdateBase | dict[str, Any]
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
        return await super().update(db, db_obj=db_obj, obj_in=user_data)

    async def authenticate(
        self, db: Session, *, mobile: str, password: str
    ) -> DonorModel | None:
        users = await self.get_by_mobile(db, mobile=mobile)

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
