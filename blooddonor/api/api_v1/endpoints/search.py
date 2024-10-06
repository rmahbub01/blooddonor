from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from blooddonor.api import deps
from blooddonor.crud.crud_utility import user
from blooddonor.models.usermodel import DonorModel
from blooddonor.schemas.user import (
    BloodGroupEnum,
    DepartmentsEnum,
    DistrictEnum,
    DonorFilterSchema,
    GenderEnum,
    StudentShipStatusEnum,
    UserApi,
)

router = APIRouter()


@router.get("/gender", response_model=list[UserApi])
async def get_donor_by_gender(
    *,
    gender: GenderEnum | None = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
) -> Any:
    donors = await user.get_by_gender(db, gender=gender, skip=skip, limit=limit)
    if not donors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor/s not found with selected gender",
        )
    return donors


@router.get("/district", response_model=list[UserApi])
async def get_donor_by_district(
    *,
    district: DistrictEnum | None = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
) -> Any:
    donors = await user.get_by_district(db, district=district, skip=skip, limit=limit)
    if not donors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor/s not found with selected district",
        )
    return donors


@router.get("/blood_group", response_model=list[UserApi])
async def get_donor_by_blood_group(
    *,
    blood_group: BloodGroupEnum | None = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
) -> Any:
    donors = await user.get_by_blood_group(
        db, blood_group=blood_group, skip=skip, limit=limit
    )
    if not donors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor/s not found with selected blood group",
        )
    return donors


@router.get("/studentship_status", response_model=list[UserApi])
async def get_donor_by_studentship_status(
    *,
    studentship_status: StudentShipStatusEnum | None = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
) -> Any:
    donors = await user.get_by_studentship_status(
        db, studentship_status=studentship_status, skip=skip, limit=limit
    )
    if not donors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor/s not found with selected Studentship status",
        )
    return donors


@router.get("/name", response_model=list[UserApi])
async def get_donor_by_name(
    *,
    name: str | None = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
) -> Any:
    donors = await user.get_by_name(db, name=name, skip=skip, limit=limit)
    if not donors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor/s not found with this name",
        )
    return donors


@router.get("/department", response_model=list[UserApi])
async def get_donor_by_department(
    *,
    department: DepartmentsEnum | None = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
) -> Any:
    donors = await user.get_by_department(
        db, department=department, skip=skip, limit=limit
    )
    if not donors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor/s not found at this department.",
        )
    return donors


@router.get("/student_id", response_model=list[UserApi])
async def get_donor_by_student_id(
    *,
    student_id: str | None = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
) -> Any:
    donors = await user.get_by_student_id(
        db, student_id=student_id, skip=skip, limit=limit
    )
    if not donors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor/s not found with this student id.",
        )
    return donors


@router.get("/filter_donors", response_model=list[UserApi])
async def filter_donors(
    filters: DonorFilterSchema = Depends(), db: Session = Depends(deps.get_db)
) -> Any:
    # Start with a base select query
    query = select(DonorModel)

    # Dynamically apply filters using where conditions
    conditions = []

    if filters.full_name:
        conditions.append(DonorModel.full_name.ilike(f"%{filters.full_name}%"))

    if filters.student_id:
        conditions.append(DonorModel.student_id.in_([filters.student_id]))

    if filters.gender:
        conditions.append(DonorModel.gender.in_([filters.gender.value]))

    if filters.district:
        conditions.append(DonorModel.district.in_([filters.district.value]))

    if filters.blood_group:
        conditions.append(DonorModel.blood_group.in_([filters.blood_group.value]))

    if filters.studentship_status:
        conditions.append(
            DonorModel.studentship_status.in_([filters.studentship_status.value])
        )

    if filters.department:
        conditions.append(DonorModel.department.in_([filters.department.value]))

    # Add the conditions to the query if any exist
    if conditions:
        query = query.where(and_(*conditions))

    # Execute the query asynchronously
    result = await db.execute(query)  # noqa

    # Fetch all the matching rows
    users = result.scalars().all()

    return users
