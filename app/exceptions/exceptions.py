class BaseAppException(Exception):
    DEFAULT_STATUS_CODE = 500
    DEFAULT_ERROR_MESSAGE = "Unexpected error occurred"

    def __init__(
        self, detail: str | None = None, status_code: int | None = None
    ) -> None:
        self.error_code = status_code or self.DEFAULT_STATUS_CODE
        self.detail = detail or self.DEFAULT_ERROR_MESSAGE


class ObjectNotFoundException(BaseAppException):
    DEFAULT_STATUS_CODE = 404
    DEFAULT_ERROR_MESSAGE = "No such object was found. Check the details you entered."


class PermissionDeniedException(BaseAppException):
    DEFAULT_STATUS_CODE = 403
    DEFAULT_ERROR_MESSAGE = (
        "Forbidden. You dont have any permissions to perform this action."
    )


class AutorizingException(BaseAppException):
    DEFAULT_STATUS_CODE = 401
    DEFAULT_ERROR_MESSAGE = "Could not validate credentials"


class EmptyParametersException(BaseAppException):
    DEFAULT_STATUS_CODE = 422
    DEFAULT_ERROR_MESSAGE = (
        "At least one parameter for task update info should be provided"
    )
