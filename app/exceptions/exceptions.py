from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse

from app import app


class ExceptionService:
    @staticmethod
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        error_msg = exc.errors()[0]["msg"]
        return PlainTextResponse(f"Wrong client data: {error_msg}", status_code=422)

    @staticmethod
    async def get_error_message(message: str):
        lines = message.split("\n")
        detail_line = next((line for line in lines if "DETAIL:" in line), None)
        if detail_line:
            detail = detail_line.split("DETAIL:")[1].strip()
            return detail
