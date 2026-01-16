"""Threat-related Pydantic schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ThreatBase(BaseModel):
    """Base threat schema."""

    threat_id: str = Field(..., max_length=50)
    security_attribute: str = Field(..., max_length=50)
    stride_type: str = Field(..., pattern="^[STRIDE]$")
    threat_description: str
    damage_scenario: Optional[str] = None
    attack_path: Optional[str] = None


class ThreatCreate(ThreatBase):
    """Schema for creating a threat."""

    asset_id: int
    source_reference: Optional[str] = None
    wp29_mapping: Optional[str] = None

    # Attack feasibility
    attack_vector: Optional[str] = None
    attack_complexity: Optional[str] = None
    privileges_required: Optional[str] = None
    user_interaction: Optional[str] = None

    # Impact
    impact_safety: Optional[str] = None
    impact_financial: Optional[str] = None
    impact_operational: Optional[str] = None
    impact_privacy: Optional[str] = None


class ThreatUpdate(BaseModel):
    """Schema for updating a threat."""

    threat_id: Optional[str] = Field(None, max_length=50)
    security_attribute: Optional[str] = Field(None, max_length=50)
    stride_type: Optional[str] = Field(None, pattern="^[STRIDE]$")
    threat_description: Optional[str] = None
    damage_scenario: Optional[str] = None
    attack_path: Optional[str] = None
    source_reference: Optional[str] = None
    wp29_mapping: Optional[str] = None

    # Attack feasibility
    attack_vector: Optional[str] = None
    attack_complexity: Optional[str] = None
    privileges_required: Optional[str] = None
    user_interaction: Optional[str] = None

    # Impact
    impact_safety: Optional[str] = None
    impact_financial: Optional[str] = None
    impact_operational: Optional[str] = None
    impact_privacy: Optional[str] = None

    # Treatment
    treatment_decision: Optional[str] = None
    is_confirmed: Optional[bool] = None


class MitigationCreate(BaseModel):
    """Schema for creating a security mitigation."""

    security_goal: Optional[str] = None
    security_requirement: Optional[str] = None
    wp29_control_mapping: Optional[str] = None
    implementation_status: str = "planned"


class MitigationUpdate(BaseModel):
    """Schema for updating a security mitigation."""

    security_goal: Optional[str] = None
    security_requirement: Optional[str] = None
    wp29_control_mapping: Optional[str] = None
    implementation_status: Optional[str] = None


class MitigationResponse(BaseModel):
    """Schema for mitigation response."""

    id: int
    threat_id: int
    security_goal: Optional[str] = None
    security_requirement: Optional[str] = None
    wp29_control_mapping: Optional[str] = None
    implementation_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ThreatResponse(BaseModel):
    """Schema for threat response."""

    id: int
    project_id: int
    version_id: Optional[int] = None
    asset_id: int
    asset_name: Optional[str] = None
    threat_id: str
    security_attribute: str
    stride_type: str
    threat_description: str
    damage_scenario: Optional[str] = None
    attack_path: Optional[str] = None
    source_reference: Optional[str] = None
    wp29_mapping: Optional[str] = None

    # Attack feasibility
    attack_vector: Optional[str] = None
    attack_complexity: Optional[str] = None
    privileges_required: Optional[str] = None
    user_interaction: Optional[str] = None
    attack_feasibility: Optional[str] = None
    attack_feasibility_value: Optional[int] = None

    # Impact
    impact_safety: Optional[str] = None
    impact_financial: Optional[str] = None
    impact_operational: Optional[str] = None
    impact_privacy: Optional[str] = None
    impact_level: Optional[str] = None
    impact_level_value: Optional[int] = None

    # Risk
    risk_level: Optional[int] = None
    risk_level_label: Optional[str] = None

    # Treatment
    treatment_decision: Optional[str] = None

    # Metadata
    is_ai_generated: bool
    is_confirmed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Mitigations
    mitigations: List[MitigationResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class RiskMatrixResponse(BaseModel):
    """Schema for risk matrix response."""

    matrix: List[List[int]] = Field(default_factory=list)
    threat_counts: dict = Field(default_factory=dict)
    total_threats: int = 0
    high_risk_count: int = 0
