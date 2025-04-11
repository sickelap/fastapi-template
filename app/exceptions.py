from fastapi import Request
from fastapi.responses import JSONResponse

from app.application import exceptions


def map_exceptions(app):
    def handle_exception(code: int, e: type[Exception]):
        @app.exception_handler(e)
        def _(_: Request, e):
            return JSONResponse(status_code=code, content={"message": str(e)})

    handle_exception(404, exceptions.UserNotFound)
    handle_exception(400, exceptions.PasswordRulesError)
    handle_exception(409, exceptions.EmailInUse)
    handle_exception(403, exceptions.RegistrationNotAllowed)
    handle_exception(401, exceptions.InvalidCredentials)
    handle_exception(403, exceptions.ActionNotAllowed)
    handle_exception(403, exceptions.UserInactive)
