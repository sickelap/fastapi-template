from fastapi import APIRouter

from app.infrastructure.api.routes.admin import router as admin_router
from app.infrastructure.api.routes.health import router as health_router
from app.infrastructure.api.routes.security import router as secrity_router
from app.infrastructure.api.routes.user import router as user_router

router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(admin_router)
router.include_router(secrity_router)
router.include_router(user_router)
