from fastapi import Request
from fastapi.responses import JSONResponse

from app.infrastructure.exceptions import PasswordError, UserNotFound


def map_exceptions(app):
    @app.exception_handler(UserNotFound)
    async def _(r: Request, e: UserNotFound):
        return JSONResponse(status_code=404, content={"message": "not found"})

    @app.exception_handler(PasswordError)
    async def _(r: Request, e: PasswordError):
        return JSONResponse(status_code=400, content={"message": e.message})
