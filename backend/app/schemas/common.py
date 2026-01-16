"""Common Pydantic schemas."""

from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    """Standard API response model."""

    code: int = Field(default=0, description="Response code, 0 means success")
    message: str = Field(default="success", description="Response message")
    data: Optional[T] = Field(default=None, description="Response data")
    timestamp: int = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000),
        description="Response timestamp in milliseconds"
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model."""

    items: List[T] = Field(default_factory=list, description="List of items")
    total: int = Field(default=0, description="Total count")
    page: int = Field(default=1, description="Current page")
    page_size: int = Field(default=20, description="Page size")


class Token(BaseModel):
    """Token response model."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class ErrorDetail(BaseModel):
    """Error detail model."""

    loc: Optional[List[str]] = None
    msg: str
    type: str


class HealthCheck(BaseModel):
    """Health check response model."""

    status: str = "healthy"
    version: str
    timestamp: datetime
