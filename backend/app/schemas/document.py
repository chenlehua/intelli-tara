"""Document-related Pydantic schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    """Schema for creating a document record."""

    name: str = Field(..., max_length=255)
    original_name: str = Field(..., max_length=255)
    file_type: str = Field(..., max_length=20)
    file_size: Optional[int] = None
    storage_path: str = Field(..., max_length=500)
    category: str = Field(default="other")


class DocumentUpdate(BaseModel):
    """Schema for updating a document."""

    name: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = None


class DocumentResponse(BaseModel):
    """Schema for document response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    version_id: Optional[int] = None
    name: str
    original_name: str
    file_type: str
    file_size: Optional[int] = None
    category: str
    parse_status: str
    uploaded_by: int
    uploader_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class DocumentParseResult(BaseModel):
    """Schema for document parse result."""

    text_blocks: List[str] = Field(default_factory=list)
    tables: List[List[List[str]]] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ParsedContentResponse(BaseModel):
    """Schema for parsed content response."""

    document_id: int
    status: str
    result: Optional[DocumentParseResult] = None
    error: Optional[str] = None
