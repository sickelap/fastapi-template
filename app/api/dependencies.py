import uuid
from typing import Annotated

from app.models import User, UserInDB
from app.service.token import verify_access_token
from app.service.user import UserService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[UserService, Depends()],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_access_token(token)
        if not payload:
            raise credentials_exception
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = user_service.find_one_by_id(uuid.UUID(user_id))
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    user: Annotated[UserInDB, Depends(get_current_user)],
) -> User | None:
    if not user.is_active:
        return None
    return user
