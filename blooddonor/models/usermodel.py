import datetime
import uuid
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blooddonor.db.base_class import Base
from blooddonor.schemas.user import (
    AcademicYearEnum,
    BloodGroupEnum,
    DepartmentsEnum,
    DistrictEnum,
    EmploymentStatusEnum,
    GenderEnum,
)


class DonorModel(Base):
    id: Mapped[UUID] = mapped_column(
        String, default=lambda: str(uuid.uuid4()), primary_key=True
    )

    # personal details
    full_name: Mapped[str] = mapped_column(nullable=False, index=True)
    email: Mapped[str] = mapped_column(index=True, default=None, unique=True)
    mobile: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    department: Mapped[DepartmentsEnum] = mapped_column(index=True, nullable=False)
    student_id: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    gender: Mapped[GenderEnum] = mapped_column(nullable=False, index=True)
    district: Mapped[DistrictEnum] = mapped_column(nullable=False, index=True)
    blood_group: Mapped[BloodGroupEnum] = mapped_column(nullable=False, index=True)
    academic_year: Mapped[AcademicYearEnum] = mapped_column(nullable=False, index=True)
    is_available: Mapped[bool] = mapped_column(default=True)
    # relationship
    profile: Mapped["ProfileModel"] = relationship(
        "ProfileModel",
        back_populates="donor",
        uselist=False,
        cascade="all, delete",
        lazy="selectin",
    )

    # credentials
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    # permissions
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_on: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(datetime.UTC)
    )
    donated_on: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(datetime.UTC)
    )


class ProfileModel(Base):
    id: Mapped[UUID] = mapped_column(
        String, default=lambda: str(uuid.uuid4()), primary_key=True
    )
    profile_img: Mapped[str] = mapped_column(nullable=True, default="profile_img.png")
    facebook: Mapped[str] = mapped_column(nullable=True, default=None)
    instagram: Mapped[str] = mapped_column(nullable=True, default=None)
    linkedin: Mapped[str] = mapped_column(nullable=True, default=None)
    website: Mapped[str] = mapped_column(nullable=True, default=None)
    employment_status: Mapped[EmploymentStatusEnum] = mapped_column(
        default=EmploymentStatusEnum.STUDENT
    )
    # relationship
    donor_id: Mapped[UUID] = mapped_column(
        ForeignKey("donormodel.id", ondelete="CASCADE")
    )
    donor: Mapped["DonorModel"] = relationship("DonorModel", back_populates="profile")
