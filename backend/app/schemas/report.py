"""Report-related Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReportCreate(BaseModel):
    """Schema for creating a report."""

    title: str = Field(..., max_length=255)
    report_version: Optional[str] = Field(None, max_length=20)
    author: Optional[str] = Field(None, max_length=100)
    reviewer: Optional[str] = Field(None, max_length=100)
    approver: Optional[str] = Field(None, max_length=100)
    version_id: Optional[int] = None


class ReportResponse(BaseModel):
    """Schema for report response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    version_id: Optional[int] = None
    report_number: Optional[str] = None
    title: str
    report_version: Optional[str] = None
    status: str
    storage_path: Optional[str] = None
    file_size: Optional[int] = None
    generated_by: int
    generator_name: Optional[str] = None
    author: Optional[str] = None
    reviewer: Optional[str] = None
    approver: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime


class ReportGenerateRequest(BaseModel):
    """Schema for report generation request."""

    title: Optional[str] = None
    report_version: Optional[str] = None
    author: Optional[str] = None
    reviewer: Optional[str] = None
    approver: Optional[str] = None
    version_id: Optional[int] = None
