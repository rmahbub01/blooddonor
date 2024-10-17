import datetime
import os
from typing import Any

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession as Session

from blooddonor.api import deps
from blooddonor.core.config import settings
from blooddonor.core.security import verify_password
from blooddonor.crud.crud_utility import profile, user
from blooddonor.helper.email import (
    generate_password_reset_token,
    send_new_account_email,
    verify_password_reset_token,
)
from blooddonor.helper.image import save_image
from blooddonor.models.usermodel import DonorModel
from blooddonor.schemas.msg import Msg
from blooddonor.schemas.token import AccountVerifyToken
from blooddonor.schemas.user import (
    AcademicYearEnum,
    BloodGroupEnum,
    DepartmentsEnum,
    DistrictEnum,
    GenderEnum,
    ProfileResponse,
    UpdateBySuperUser,
    UpdateProfile,
    UserApi,
    UserCreateBase,
    UserUpdateBase,
)

router = APIRouter()


@router.get("/read_users", response_model=list[UserApi])
async def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    users = await user.get_multi(db, skip=skip, limit=limit, order_by="created_on desc")
    return users


@router.post("/create_user_by_superuser", response_model=UserApi)
async def create_user_by_superuser(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreateBase,
    current_user: DonorModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user (Need Super User privilege).
    """
    users = (
        await user.get_by_mobile(db, mobile=user_in.mobile)
        or await user.get_by_email(db, email=user_in.email)
        or await user.get_by_student_id(db, student_id=user_in.student_id)
    )
    if users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this mobile, email or student_id already exists in the system.",
        )
    users = await user.create(db, obj_in=user_in)
    return users


@router.delete("/delete_user/{email}", response_model=Msg)
async def delete_user(
    *,
    email: EmailStr,
    db: Session = Depends(deps.get_db),
    current_user: DonorModel = Depends(deps.get_current_active_superuser),
):
    """Delete a user/donor by email (Need Super User privilege)"""
    donor = await user.get_by_email(db, email=email)
    if donor:
        await user.remove(db, id=donor.id)
        return Msg(msg="The user has been removed!")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="There is no user with this email!",
    )


@router.patch("/update/me", response_model=UserApi)
async def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdateBase,
    current_user: DonorModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update thyself.
    """
    if user_in.password and await verify_password(
        user_in.password, current_user.hashed_password
    ):
        users = await user.update(db, db_obj=current_user, obj_in=user_in)
        return users
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Password doesn't match!"
    )


@router.get("/me", response_model=UserApi)
async def read_user_me(
    current_user: DonorModel = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/read_profile/{user_id}", response_model=ProfileResponse)
async def read_profile(
    user_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Read current user/donor profile.
    """
    donor_profile = await profile.get(db, donor_id=user_id)
    if not donor_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile found with this user id.",
        )
    return donor_profile


@router.patch("/update_profile/me", response_model=ProfileResponse)
async def update_profile(
    user_in: UpdateProfile,
    db: Session = Depends(deps.get_db),
    current_user: DonorModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Read current user/donor profile.
    """
    donor_profile = await profile.get(db, donor_id=current_user.id)
    if not donor_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile found with this user id.",
        )
    await profile.update(db, db_obj=donor_profile, obj_in=user_in)
    return donor_profile


@router.post(
    "/create_user",
    response_model=Msg,
)
async def create_user(
    *,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    full_name: str = Body(...),
    email: EmailStr = Body(...),
    mobile: str = Body(...),
    department: DepartmentsEnum = Body(...),
    student_id: str = Body(...),
    gender: GenderEnum = Body(...),
    district: DistrictEnum = Body(...),
    blood_group: BloodGroupEnum = Body(...),
    academic_year: AcademicYearEnum = Body(...),
    password: str = Body(...),
) -> Any:
    """
    Create new user without the need to be logged in.
    department_code (str): A string representing the department code. The available department codes are:

    - Faculty of Arts and Humanities:
        * "101" - Bangla
        * "102" - English
        * "103" - History
        * "104" - Islamic History and Culture
        * "105" - Philosophy
        * "106" - Fine Arts
        * "107" - Arabic
        * "108" - Pali
        * "110" - Islamic Studies
        * "111" - Dramatics
        * "112" - Persian Language and Literature
        * "113" - Education and Research
        * "114" - Modern Languages
        * "115" - Sanskrit
        * "116" - Music
        * "117" - Bangladesh Studies

    - Faculty of Science:
        * "201" - Physics
        * "202" - Chemistry
        * "203" - Mathematics
        * "204" - Statistics
        * "208" - Forestry and Environmental Sciences
        * "209" - Applied Chemistry and Chemical Engineering

    - Faculty of Business Administration:
        * "301" - Accounting
        * "302" - Management
        * "303" - Finance
        * "304" - Marketing
        * "305" - Human Resource Management
        * "306" - Banking and Insurance

    - Faculty of Social Sciences:
        * "401" - Economics
        * "402" - Political Science
        * "403" - Sociology
        * "404" - Public Administration
        * "405" - Anthropology
        * "406" - International Relations
        * "407" - Communication and Journalism
        * "408" - Development Studies
        * "409" - Criminology and Police Science

    - Faculty of Law:
        * "501" - Law

    - Faculty of Biological Sciences:
        * "601" - Zoology
        * "602" - Botany
        * "603" - Geography and Environmental Studies
        * "604" - Biochemistry and Molecular Biology
        * "605" - Microbiology
        * "606" - Soil Science
        * "607" - Genetic Engineering and Biotechnology
        * "608" - Psychology
        * "609" - Pharmacy

    - Faculty of Engineering:
        * "701" - Computer Science and Engineering
        * "702" - Electrical and Electronic Engineering

    - Faculty of Education:
        * "801" - Physical Education and Sports Science

    - Faculty of Marine Sciences and Fisheries:
        * "901" - Marine Sciences
        * "902" - Oceanography
        * "903" - Fisheries
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is forbidden on this server",
        )
    user_in = UserCreateBase(
        full_name=full_name,
        email=email,
        mobile=mobile,
        department=department,
        student_id=student_id,
        gender=gender,
        district=district,
        blood_group=blood_group,
        academic_year=academic_year,
        password=password,
    )
    users = (
        await user.get_by_mobile(db, mobile=mobile)
        or await user.get_by_email(db, email=email)
        or await user.get_by_student_id(db, student_id=student_id)
    )
    if users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The user with this mobile, email or student_id already exists in the system",
        )

    if settings.EMAILS_ENABLED and user_in.email:
        user_in.is_active = False
        # email will be sent in the background
        password_reset_token = await generate_password_reset_token(email=email)
        background_tasks.add_task(
            send_new_account_email,
            username=user_in.full_name,
            email=user_in.email,
            token=password_reset_token,
        )
    users = await user.create(db, obj_in=user_in)
    return Msg(msg="Account has been created")


@router.post("/verify-account")
async def verify_account(
    body: AccountVerifyToken, db: Session = Depends(deps.get_db)
) -> Any:
    email = await verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
    donor = await user.get_by_email(db, email=email)
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system.",
        )
    donor.is_active = True
    db.add(donor)
    await db.commit()
    return Msg(msg="Account verification successful.")


@router.get("/read_user/{user_email}", response_model=UserApi)
async def read_user_by_email(
    user_email: EmailStr,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by email.
    """
    users = await user.get_by_email(db, email=user_email)
    if users:
        return users
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )


@router.patch("/update/{user_email}", response_model=UserApi)
async def update_user_by_email(
    *,
    db: Session = Depends(deps.get_db),
    user_email: EmailStr,
    user_in: UpdateBySuperUser,
    current_user: DonorModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user (Super User Privilege needed).
    """
    user_ = await user.get_by_email(db, email=user_email)
    if not user_in:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )
    users = await user.update(db, db_obj=user_, obj_in=user_in)
    return users


@router.post("/upload_profile_img")
async def upload_profile_img(
    file: UploadFile,
    db: Session = Depends(deps.get_db),
    current_user: DonorModel = Depends(deps.get_current_active_user),
):
    try:
        await save_image(file, current_user.id)
        profile_data = await profile.get(db, donor_id=current_user.id)
        profile_data.profile_img = f"{current_user.id}.png"
        await profile.update(
            db, db_obj=profile_data, obj_in=jsonable_encoder(profile_data)
        )
    except HTTPException:
        raise HTTPException(
            status_code=status.WS_1011_INTERNAL_ERROR,
            detail="There is an error in the server. Pls try again.",
        )
    finally:
        return {"success": "Profile image upload successful."}


@router.patch("/change_availability", response_model=Msg)
async def change_availability(
    db: Session = Depends(deps.get_db),
    current_user: DonorModel = Depends(deps.get_current_active_user),
) -> Msg:
    if current_user.is_available:
        current_user.is_available = False
    else:
        current_user.is_available = True
    # update the donated_on field
    current_user.donated_on = datetime.datetime.now(datetime.UTC)
    user_in = jsonable_encoder(current_user)
    await user.update(db, db_obj=current_user, obj_in=UserUpdateBase(**user_in))
    return Msg(
        msg=f"Availability status has been changed. Now {"available" if current_user.is_available else "unavailable"}"
    )


@router.get("/get/profile_img/{user_id}", response_class=FileResponse)
async def get_profile_img(user_id: str) -> str:
    static_dir = "./blooddonor/static/images"
    img_path = f"{static_dir}/{user_id}.png"
    if os.path.isfile(img_path):
        return img_path
    else:
        return f"{static_dir}/profile_img.png"


@router.get("/counts")
async def get_total_users(db: Session = Depends(deps.get_db)) -> dict:
    donors_count: dict = await user.get_user_count(db)
    return donors_count
