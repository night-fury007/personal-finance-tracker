class WealthEngineException(Exception):
    """Base exception for all Wealth Engine business logic errors."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(WealthEngineException):
    """Raised when a requested resource does not exist (Maps to 204 No Content)."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=204)


class BadRequestException(WealthEngineException):
    """Raised when the request syntax or data is invalid (Maps to 400 Bad Request)."""

    def __init__(self, message: str = "Bad request"):
        super().__init__(message=message, status_code=400)


class UnauthorizedException(WealthEngineException):
    """Raised when the user is not authenticated (Maps to 401 Unauthorized)."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message=message, status_code=401)


class DatabaseOperationException(WealthEngineException):
    """Raised when a database transaction fails (Maps to 400 or custom status)."""

    def __init__(self, message: str = "A database operation error occurred"):
        super().__init__(message=message, status_code=400)
