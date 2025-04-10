from typing import Annotated

from app.domain.models import User
from app.infrastructure.api.dependencies import get_current_active_user
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/profile")


@router.get("", response_model=User)
async def get_me(user: Annotated[User, Depends(get_current_active_user)]):
    return user
