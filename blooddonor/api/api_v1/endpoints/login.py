import datetime
from typing import Any

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from blooddonor.api import deps
from blooddonor.core import security
from blooddonor.core.config import settings
from blooddonor.core.security import get_password_hash
from blooddonor.crud.crud_utility import user
from blooddonor.helper.email import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
from blooddonor.models.usermodel import DonorModel
from blooddonor.schemas.msg import Msg
from blooddonor.schemas.token import Token
from blooddonor.schemas.user import UserChangePassword

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    users = await user.authenticate(
        db, mobile=form_data.username, password=form_data.password
    )
    if not users:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not await user.is_active(users):
        raise HTTPException(status_code=400, detail="Inactive User")
    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = await security.create_access_token(
        users.id, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {access_token}",
        domain=str(settings.SERVER_HOST).split("/")[-1],
        httponly=True,
        expires=access_token_expires,  # type: ignore
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("Authorization")
    return {"success": "User logged out successfully."}


@router.post("/password-recovery/{email}", response_model=Msg)
async def recover_password(
    request: Request,
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Password Recovery
    """
    users = await user.get_by_email(db, email=email)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system.",
        )

    password_reset_token = await generate_password_reset_token(email=email)
    # email will be sent in the background
    background_tasks.add_task(
        send_reset_password_email,
        username=users.full_name,
        email=users.email,
        token=password_reset_token,
    )

    return {"msg": "Password recovery email sent"}


@router.post("/change_password/", response_model=Msg)
async def change_password(
    db: Session = Depends(deps.get_db),
    new_password: UserChangePassword = Body(...),
    current_user: DonorModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Reset password
    """
    hashed_password = await get_password_hash(new_password.password)
    current_user.hashed_password = hashed_password
    db.add(current_user)
    await db.commit()  # noqa
    return {"msg": "Password updated successfully"}


@router.post("/reset-password")
async def reset_password(
    body: UserChangePassword,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = await verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
    donor = await user.get_by_email(db, email=email)
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist in the system.",
        )
    elif not donor.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    hashed_password = await get_password_hash(body.password)
    donor.hashed_password = hashed_password
    db.add(donor)
    await db.commit()  # noqa
    return Msg(msg="Password reset successful!")
