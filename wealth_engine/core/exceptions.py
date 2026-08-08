class WealthEngineException(Exception):
    """Base exception for all Wealth Engine business logic errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(WealthEngineException):
    """Raised when a requested resource does not exist or user lacks permission."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404)

class DatabaseOperationException(WealthEngineException):
    """Raised when a database transaction or integrity constraint fails."""
    def __init__(self, message: str = "A database operation error occurred"):
        super().__init__(message=message, status_code=400)
