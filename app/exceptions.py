from fastapi import Request
from fastapi.responses import JSONResponse

from app.application.exceptions import (
    EmailInUse,
    InvalidCredentials,
    PasswordRulesError,
    RegistrationNotAllowed,
    UserInactive,
    UserNotFound,
)


def map_exceptions(app):
    def handle_exception(code: int, e: type[Exception]):
        @app.exception_handler(e)
        def _(_: Request, e):
            return JSONResponse(status_code=code, content={"message": str(e)})

    handle_exception(404, UserNotFound)
    handle_exception(400, PasswordRulesError)
    handle_exception(409, EmailInUse)
    handle_exception(403, RegistrationNotAllowed)
    handle_exception(401, InvalidCredentials)
    handle_exception(403, UserInactive)
