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
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from blooddonor.api import deps
from blooddonor.core.config import settings
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
    BloodGroupEnum,
    DepartmentsEnum,
    DistrictEnum,
    GenderEnum,
    ProfileResponse,
    StudentShipStatusEnum,
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
    users = await user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/create_user", response_model=UserApi)
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreateBase,
    background_tasks: BackgroundTasks,
    current_user: DonorModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    users = await user.get_by_mobile(db, mobile=user_in.mobile)
    if users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
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
    full_name: str | None = Body(None),
    mobile: str | None = Body(None),
    district: DistrictEnum | None = Body(None),
    studentship_status: StudentShipStatusEnum | None = Body(None),
    is_available: bool | None = Body(None),
    password: str | None = Body(None),
    current_user: DonorModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update thyself.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdateBase(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if mobile is not None:
        user_in.mobile = mobile
    if district is not None:
        user_in.district = district
    if studentship_status is not None:
        user_in.studentship_status = studentship_status
    if is_available is not None:
        user_in.is_available = is_available
    users = await user.update(db, db_obj=current_user, obj_in=user_in)
    return users


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
    "/create_user_open",
    response_model=UserApi,
)
async def create_user_open(
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
    studentship_status: StudentShipStatusEnum = Body(...),
    password: str = Body(...),
) -> Any:
    """
    Create new user without the need to be logged in.
    Structure of department naming. User will prove just an integer.
    # Arts and Humanities
    ARABIC = "1"
    BANGLADESH_STUDIES = "2"
    BANGLA = "3"
    DRAMATICS = "4"
    EDUCATION_AND_RESEARCH = "5"
    ENGLISH = "6"
    ENGLISH_TEACHERS_OF_ARTS_AND_HUMANITIES_FACULTY = "7"
    FINE_ARTS = "8"
    HISTORY = "9"
    ISLAMIC_HISTORY_AND_CULTURE = "10"
    ISLAMIC_STUDIES = "11"
    MODERN_LANGUAGES = "12"
    MUSIC = "13"
    PALI = "14"
    PERSIAN_LANGUAGE_AND_LITERATURE = "15"
    PHILOSOPHY = "16"
    SANSKRIT = "17"

    # Science
    APPLIED_CHEMISTRY_AND_CHEMICAL_ENGINEERING = "18"
    CHEMISTRY = "19"
    ENGLISH_TEACHERS_OF_SCIENCE_FACULTY = "20"
    FORESTRY_AND_ENVIRONMENTAL_SCIENCES = "21"
    JAMAL_NAZRUL_ISLAM_RESEARCH_CENTRE = "22"
    MATHEMATICS = "23"
    PHYSICS = "24"
    STATISTICS = "25"

    # Business Administration
    ACCOUNTING = "26"
    BANKING_AND_INSURANCE = "27"
    BUREAU_OF_BUSINESS_RESEARCH = "28"
    CENTER_FOR_BUSINESS_ADMINISTRATION = "29"
    ENGLISH_TEACHERS_OF_BUSINESS_ADMINISTRATION_FACULTY = "30"
    FINANCE = "31"
    HUMAN_RESOURCE_MANAGEMENT = "32"
    MANAGEMENT = "33"
    MARKETING = "34"

    # Social Sciences
    ANTHROPOLOGY = "35"
    COMMUNICATION_AND_JOURNALISM = "36"
    CRIMINOLOGY_AND_POLICE_SCIENCE = "37"
    DEVELOPMENT_STUDIES = "38"
    ECONOMICS = "39"
    ENGLISH_TEACHERS_OF_SOCIAL_SCIENCES_FACULTY = "40"
    INTERNATIONAL_RELATIONS = "41"
    POLITICAL_SCIENCE = "42"
    PUBLIC_ADMINISTRATION = "43"
    SOCIAL_SCIENCE_RESEARCH = "44"
    SOCIOLOGY = "45"

    # Law
    LAW = "46"

    # Biological Sciences
    BIOCHEMISTRY_AND_MOLECULAR_BIOLOGY = "47"
    BOTANY = "48"
    ENGLISH_TEACHERS_OF_BIOLOGICAL_SCIENCES_FACULTY = "49"
    GEOGRAPHY_AND_ENVIRONMENTAL_STUDIES = "50"
    GENETIC_ENGINEERING_AND_BIOTECHNOLOGY = "51"
    MICROBIOLOGY = "52"
    PHARMACY = "53"
    PSYCHOLOGY = "54"
    SOIL_SCIENCE = "55"
    ZOOLOGY = "56"

    # Engineering
    COMPUTER_SCIENCE_AND_ENGINEERING = "57"
    ELECTRICAL_AND_ELECTRONIC_ENGINEERING = "58"

    # Education
    PHYSICAL_EDUCATION_AND_SPORTS_SCIENCE = "59"

    # Marine Sciences and Fisheries
    FISHERIES = "60"
    MARINE_SCIENCES = "61"
    OCEANOGRAPHY = "62"

    # Medicine
    COMMUNITY_OPHTHALMOLOGY = "63"
    PAEDIATRICS = "64"
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is forbidden on this server",
        )
    users = await user.get_by_mobile(db, mobile=mobile) or await user.get_by_email(
        db, email
    )
    if users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username or email already exists in the system",
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
        studentship_status=studentship_status,
        password=password,
    )

    users = await user.create(db, obj_in=user_in)
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

    return users


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
    await db.commit()  # noqa
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
    full_name: str | None = Body(None),
    mobile: str | None = Body(None),
    district: DistrictEnum | None = Body(None),
    studentship_status: StudentShipStatusEnum | None = Body(None),
    is_available: bool | None = Body(None),
    password: str | None = Body(None),
    current_user: DonorModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user_ = await user.get_by_email(db, email=user_email)
    user_in = UserUpdateBase(**jsonable_encoder(user_))
    if not user_in:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )

    if full_name is not None:
        user_in.full_name = full_name
    if mobile is not None:
        user_in.mobile = mobile
    if district is not None:
        user_in.district = district
    if studentship_status is not None:
        user_in.studentship_status = studentship_status
    if is_available is not None:
        user_in.is_available = is_available
    if password is not None:
        user_in.password = password

    users = await user.update(db, db_obj=user_, obj_in=user_in)
    return users


@router.post("/upload_profile_img")
async def upload_profile_img(
    file: UploadFile,
    db: Session = Depends(deps.get_db),
    current_user: DonorModel = Depends(deps.get_current_active_user),
):
    try:
        save_image(file, current_user.id)
        profile_data = await profile.get(db, donor_id=current_user.id)
        profile_data.profile_img = f"{current_user.id}.png"
        await profile.update(
            db, db_obj=profile_data, obj_in=jsonable_encoder(profile_data)
        )
    except:  # noqa
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
    user_in = jsonable_encoder(current_user)
    await user.update(db, db_obj=current_user, obj_in=UserUpdateBase(**user_in))
    return Msg(
        msg=f"Availability status has been changed. Now {"available" if current_user.is_available else "unavailable"}"
    )
