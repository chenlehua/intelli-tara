"""Project-related Pydantic schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base project schema."""

    name: str = Field(..., min_length=1, max_length=200)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: Optional[str] = Field(None, max_length=200)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    status: Optional[str] = None


class ProjectConfigUpdate(BaseModel):
    """Schema for updating project configuration."""

    item_name: Optional[str] = None
    item_boundary: Optional[str] = None
    functional_description: Optional[str] = None
    config_json: Optional[dict] = None


class ProjectResponse(BaseModel):
    """Schema for project response."""

    id: int
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    status: str
    owner_id: int
    owner_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    asset_count: int = 0
    threat_count: int = 0
    report_count: int = 0

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Schema for project list response."""

    id: int
    name: str
    code: Optional[str] = None
    status: str
    owner_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectVersionCreate(BaseModel):
    """Schema for creating a project version."""

    version: str = Field(..., max_length=20)
    description: Optional[str] = None


class ProjectVersionResponse(BaseModel):
    """Schema for project version response."""

    id: int
    project_id: int
    version: str
    description: Optional[str] = None
    status: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectMemberAdd(BaseModel):
    """Schema for adding a project member."""

    user_id: int
    role: str = Field(default="viewer")


class ProjectMemberResponse(BaseModel):
    """Schema for project member response."""

    user_id: int
    username: str
    display_name: Optional[str] = None
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True


class ProjectStatsResponse(BaseModel):
    """Schema for project statistics."""

    project_count: int = 0
    asset_count: int = 0
    threat_count: int = 0
    high_risk_count: int = 0
    risk_distribution: dict = Field(default_factory=dict)
