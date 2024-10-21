from blooddonor.core import security
from blooddonor.core.config import settings
from blooddonor.crud.crud_utility import user
from blooddonor.db.session import SessionLocal
from blooddonor.models.usermodel import DonorModel
from blooddonor.schemas.token import TokenPayload
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession as Session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


async def get_db() -> Session:
    try:
        async with SessionLocal() as session:
            yield session
    finally:
        await session.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> DonorModel:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    users = await user.get(db, id=token_data.sub)
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users


async def get_current_active_user(
    current_user: DonorModel = Depends(get_current_user),
) -> DonorModel:
    if not await user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: DonorModel = Depends(get_current_user),
) -> DonorModel:
    if not await user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_active_superuser_or_admin(
    current_user: DonorModel = Depends(get_current_user),
) -> DonorModel:
    if not await user.is_superuser(current_user) or not await user.is_admin(
        current_user
    ):
        raise HTTPException(
            status_code=400, detail="The user does not have enough privileges"
        )
    return current_user
