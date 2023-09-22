from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import UJSONResponse
from sqlalchemy.exc import IntegrityError

from app.exceptions.exceptions import AutorizingException
from app.exceptions.exceptions import EmptyParametersException
from app.exceptions.exceptions import ObjectNotFoundException
from app.exceptions.exceptions import PermissionDeniedException


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(ObjectNotFoundException)
    def objects_not_found_handler(
        request: Request, exc: ObjectNotFoundException
    ) -> UJSONResponse:
        return UJSONResponse(content={"detail": exc.detail}, status_code=exc.error_code)

    @app.exception_handler(IntegrityError)
    def integrity_handler(request: Request, exc: IntegrityError) -> UJSONResponse:
        return UJSONResponse(
            content={"detail": str(exc.orig).split("DETAIL:  ")[-1]}, status_code=503
        )

    @app.exception_handler(RequestValidationError)
    def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> UJSONResponse:
        return UJSONResponse(
            content={"detail": exc.errors()[0]["msg"]}, status_code=422
        )

    @app.exception_handler(PermissionDeniedException)
    def permission_handler(
        request: Request, exc: PermissionDeniedException
    ) -> UJSONResponse:
        return UJSONResponse(content={"detail": exc.detail}, status_code=exc.error_code)

    @app.exception_handler(AutorizingException)
    def autorizing_exception_handler(
        request: Request, exc: AutorizingException
    ) -> UJSONResponse:
        return UJSONResponse(content={"detail": exc.detail}, status_code=exc.error_code)

    @app.exception_handler(EmptyParametersException)
    def empty_parameters_handler(
        request: Request, exc: EmptyParametersException
    ) -> UJSONResponse:
        return UJSONResponse(content={"detail": exc.detail}, status_code=exc.error_code)
