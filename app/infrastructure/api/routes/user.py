from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.service.user import UserService
from app.domain.models import User
from app.infrastructure.api.dependencies import get_current_active_user
from app.infrastructure.models import ChangePasswordRequest

router = APIRouter()


@router.get("/profile", response_model=User)
async def get_me(user: Annotated[User, Depends(get_current_active_user)]):
    return user


@router.post("/profile")
async def update_password(
    user: Annotated[User, Depends(get_current_active_user)],
    request: ChangePasswordRequest,
    user_service: Annotated[UserService, Depends()],
):
    try:
        await user_service.change_password(
            user.id, request.old_password, request.new_password
        )
    except Exception as e:
        raise HTTPException(400, str(e))
