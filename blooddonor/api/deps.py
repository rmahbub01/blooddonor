from fastapi import Depends, HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from blooddonor.core import security
from blooddonor.core.config import settings
from blooddonor.crud.crud_utility import user
from blooddonor.db.session import SessionLocal
from blooddonor.models.usermodel import DonorModel
from blooddonor.schemas.token import TokenPayload


class OAuth2PasswordBearerCookie(OAuth2):
    """this class replaces the OAuthPasswordBearer to set cookie and read the cookie so the user don't have to put
    credentials every time."""

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(status_code=403, detail="Not authenticated")
            else:
                return None
        return param


reusable_oauth2 = OAuth2PasswordBearerCookie(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


async def get_db() -> AsyncSession:
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
    except (jwt.JWTError, ValidationError):
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
