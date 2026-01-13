from typing import Any, Dict, Optional


class BaseException(Exception):
    """
    Base exception for the application.

    Attributes:
        message (str): A human-readable error message.
        code (str): An internal error code (e.g., 'INVALID_CATEGORY_AGE').
        payload (dict): Optional dictionary with additional context.
    """

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        payload: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.code = code
        self.payload = payload or {}
        super().__init__(self.message)


class DomainException(BaseException):
    """
    Base exception for Domain Layer errors.
    Used when a business rule or invariant is violated.
    """

    def __init__(
        self,
        message: str,
        code: str = "DOMAIN_ERROR",
        payload: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, code, payload)


class ResourceNotFoundException(BaseException):
    """
    Exception raised when a requested resource does not exist.
    """

    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} with id {identifier} not found",
            code="RESOURCE_NOT_FOUND",
            payload={"resource": resource, "identifier": str(identifier)},
        )
