from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from blooddonor.api import deps
from blooddonor.models.usermodel import DonorModel
from blooddonor.schemas.user import (
    DonorFilterSchema,
    UserApi,
)

router = APIRouter()


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
