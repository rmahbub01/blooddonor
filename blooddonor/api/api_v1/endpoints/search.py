from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from blooddonor.api import deps
from blooddonor.crud.crud_utility import user
from blooddonor.schemas.user import (
    BloodGroupEnum,
    DistrictEnum,
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
