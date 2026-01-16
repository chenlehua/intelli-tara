"""Custom exception definitions."""

from typing import Any, Optional


class BaseAPIException(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        code: int,
        message: str,
        data: Optional[Any] = None
    ):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(message)


# System Errors (10000-19999)
class InternalServerError(BaseAPIException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(10001, message)


class DatabaseError(BaseAPIException):
    def __init__(self, message: str = "Database error"):
        super().__init__(10002, message)


class ExternalServiceError(BaseAPIException):
    def __init__(self, message: str = "External service error"):
        super().__init__(10003, message)


# Authentication Errors (20000-29999)
class AuthenticationError(BaseAPIException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(20001, message)


class TokenExpiredError(BaseAPIException):
    def __init__(self, message: str = "Token expired"):
        super().__init__(20002, message)


class InvalidTokenError(BaseAPIException):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(20003, message)


class PermissionDeniedError(BaseAPIException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(20004, message)


# Validation Errors (30000-39999)
class ValidationError(BaseAPIException):
    def __init__(self, message: str = "Validation error", data: Optional[Any] = None):
        super().__init__(30001, message, data)


class InvalidParameterError(BaseAPIException):
    def __init__(self, message: str = "Invalid parameter"):
        super().__init__(30002, message)


# Business Errors (40000-49999)
class NotFoundError(BaseAPIException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(40001, message)


class AlreadyExistsError(BaseAPIException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(40002, message)


class BusinessLogicError(BaseAPIException):
    def __init__(self, message: str = "Business logic error"):
        super().__init__(40003, message)


class FileUploadError(BaseAPIException):
    def __init__(self, message: str = "File upload failed"):
        super().__init__(40004, message)


class DocumentParseError(BaseAPIException):
    def __init__(self, message: str = "Document parsing failed"):
        super().__init__(40005, message)


class ReportGenerationError(BaseAPIException):
    def __init__(self, message: str = "Report generation failed"):
        super().__init__(40006, message)


# External Service Errors (50000-59999)
class AIServiceError(BaseAPIException):
    def __init__(self, message: str = "AI service error"):
        super().__init__(50001, message)


class StorageServiceError(BaseAPIException):
    def __init__(self, message: str = "Storage service error"):
        super().__init__(50002, message)


class GraphDatabaseError(BaseAPIException):
    def __init__(self, message: str = "Graph database error"):
        super().__init__(50003, message)


class VectorDatabaseError(BaseAPIException):
    def __init__(self, message: str = "Vector database error"):
        super().__init__(50004, message)
