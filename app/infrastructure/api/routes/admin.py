from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.exceptions import ActionNotAllowed
from app.application.service.user import UserService
from app.domain.models import User
from app.infrastructure.api.dependencies import get_current_active_user
from app.infrastructure.models import DisableUserRequest

router = APIRouter(prefix="/admin")


@router.post("/disable_user", response_model=User)
async def disable_user(
    request: DisableUserRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_service: Annotated[UserService, Depends()],
):
    if not current_user.is_superuser:
        raise ActionNotAllowed()
    return await user_service.disable_user(request.user_id)
