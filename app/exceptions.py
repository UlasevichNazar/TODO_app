from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse

from app.controllers import app


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_msg = exc.errors()[0]["msg"]
    return PlainTextResponse(f"Wrong client data: {error_msg}", status_code=400)
