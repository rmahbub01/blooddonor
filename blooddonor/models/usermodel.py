import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

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
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True)

    # personal details
    full_name = Column(String, nullable=False, index=True)
    email = Column(String, index=True, default=None, unique=True)
    mobile = Column(String, unique=True, index=True, nullable=False)
    department = Column(SQLEnum(DepartmentsEnum), index=True, nullable=False)
    student_id = Column(String, unique=True, nullable=False, index=True)
    gender = Column(SQLEnum(GenderEnum), nullable=False, index=True)
    district = Column(SQLEnum(DistrictEnum), nullable=False, index=True)
    blood_group = Column(SQLEnum(BloodGroupEnum), nullable=False, index=True)
    academic_year = Column(SQLEnum(AcademicYearEnum), nullable=False, index=True)
    is_available = Column(Boolean(), default=True)
    # relationship
    profile = relationship(
        "ProfileModel",
        back_populates="donor",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # credentials
    hashed_password = Column(String, nullable=False)

    # permissions
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
    created_on = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    donated_on = Column(DateTime, default=datetime.datetime.now(datetime.UTC))


class ProfileModel(Base):
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True)
    profile_img = Column(String, nullable=True, default="profile_img.png")
    facebook = Column(String, nullable=True, default=None)
    instagram = Column(String, nullable=True, default=None)
    linkedin = Column(String, nullable=True, default=None)
    website = Column(String, nullable=True, default=None)
    employment_status = Column(
        SQLEnum(EmploymentStatusEnum), default=EmploymentStatusEnum.STUDENT
    )
    # relationship
    donor_id = Column(String, ForeignKey("donormodel.id", ondelete="SET NULL"))
    donor = relationship("DonorModel", back_populates="profile")
