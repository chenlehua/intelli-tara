"""Asset-related Pydantic schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AssetBase(BaseModel):
    """Base asset schema."""

    asset_id: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)
    category: str = Field(..., max_length=50)
    subcategory: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    remarks: Optional[str] = None


class SecurityAttributes(BaseModel):
    """Security attributes schema."""

    authenticity: bool = False
    integrity: bool = False
    non_repudiation: bool = False
    confidentiality: bool = False
    availability: bool = False
    authorization: bool = False


class AssetCreate(AssetBase):
    """Schema for creating an asset."""

    authenticity: bool = False
    integrity: bool = False
    non_repudiation: bool = False
    confidentiality: bool = False
    availability: bool = False
    authorization: bool = False
    source_document_id: Optional[int] = None


class AssetUpdate(BaseModel):
    """Schema for updating an asset."""

    asset_id: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = Field(None, max_length=200)
    category: Optional[str] = Field(None, max_length=50)
    subcategory: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    remarks: Optional[str] = None
    authenticity: Optional[bool] = None
    integrity: Optional[bool] = None
    non_repudiation: Optional[bool] = None
    confidentiality: Optional[bool] = None
    availability: Optional[bool] = None
    authorization: Optional[bool] = None
    is_confirmed: Optional[bool] = None


class AssetResponse(BaseModel):
    """Schema for asset response."""

    id: int
    project_id: int
    version_id: Optional[int] = None
    asset_id: str
    name: str
    category: str
    subcategory: Optional[str] = None
    description: Optional[str] = None
    remarks: Optional[str] = None
    authenticity: bool
    integrity: bool
    non_repudiation: bool
    confidentiality: bool
    availability: bool
    authorization: bool
    is_ai_generated: bool
    is_confirmed: bool
    source_document_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssetRelationCreate(BaseModel):
    """Schema for creating an asset relation."""

    source_asset_id: int
    target_asset_id: int
    relation_type: str = Field(..., max_length=50)
    protocol: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class AssetRelationResponse(BaseModel):
    """Schema for asset relation response."""

    id: int
    project_id: int
    source_asset_id: int
    target_asset_id: int
    relation_type: str
    protocol: Optional[str] = None
    description: Optional[str] = None
    source_asset_name: Optional[str] = None
    target_asset_name: Optional[str] = None

    class Config:
        from_attributes = True


class AssetGraphNode(BaseModel):
    """Schema for asset graph node."""

    id: str
    name: str
    category: str
    subcategory: Optional[str] = None


class AssetGraphEdge(BaseModel):
    """Schema for asset graph edge."""

    source: str
    target: str
    type: str
    protocol: Optional[str] = None


class AssetGraphResponse(BaseModel):
    """Schema for asset graph response."""

    nodes: List[AssetGraphNode] = Field(default_factory=list)
    edges: List[AssetGraphEdge] = Field(default_factory=list)
