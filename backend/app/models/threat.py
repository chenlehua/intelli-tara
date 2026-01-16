"""Threat analysis and risk assessment models."""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.project import Project, ProjectVersion
    from app.models.asset import Asset


class ThreatScenario(Base, TimestampMixin):
    """Threat scenario model."""

    __tablename__ = "threat_scenarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    version_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("project_versions.id"),
        nullable=True
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    threat_id: Mapped[str] = mapped_column(String(50), nullable=False)
    security_attribute: Mapped[str] = mapped_column(String(50), nullable=False)
    stride_type: Mapped[str] = mapped_column(
        Enum("S", "T", "R", "I", "D", "E", name="stride_type"),
        nullable=False
    )
    threat_description: Mapped[str] = mapped_column(Text, nullable=False)
    damage_scenario: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attack_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_reference: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    wp29_mapping: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Attack feasibility parameters
    attack_vector: Mapped[Optional[str]] = mapped_column(
        Enum("Physical", "Local", "Adjacent", "Network", name="attack_vector"),
        nullable=True
    )
    attack_complexity: Mapped[Optional[str]] = mapped_column(
        Enum("High", "Low", name="attack_complexity"),
        nullable=True
    )
    privileges_required: Mapped[Optional[str]] = mapped_column(
        Enum("None", "Low", "High", name="privileges_required"),
        nullable=True
    )
    user_interaction: Mapped[Optional[str]] = mapped_column(
        Enum("Required", "None", name="user_interaction"),
        nullable=True
    )
    attack_feasibility: Mapped[Optional[str]] = mapped_column(
        Enum("High", "Medium", "Low", "Very Low", name="attack_feasibility"),
        nullable=True
    )
    attack_feasibility_value: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Impact analysis
    impact_safety: Mapped[Optional[str]] = mapped_column(
        Enum("S0", "S1", "S2", "S3", name="impact_safety"),
        nullable=True
    )
    impact_financial: Mapped[Optional[str]] = mapped_column(
        Enum("F0", "F1", "F2", "F3", name="impact_financial"),
        nullable=True
    )
    impact_operational: Mapped[Optional[str]] = mapped_column(
        Enum("O0", "O1", "O2", "O3", name="impact_operational"),
        nullable=True
    )
    impact_privacy: Mapped[Optional[str]] = mapped_column(
        Enum("P0", "P1", "P2", "P3", name="impact_privacy"),
        nullable=True
    )
    impact_level: Mapped[Optional[str]] = mapped_column(
        Enum("Negligible", "Moderate", "Major", "Severe", name="impact_level"),
        nullable=True
    )
    impact_level_value: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Risk assessment
    risk_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    risk_level_label: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Risk treatment
    treatment_decision: Mapped[Optional[str]] = mapped_column(
        Enum("Accept", "Reduce", "Avoid", "Transfer", name="treatment_decision"),
        nullable=True
    )

    # Metadata
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=True)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="threats")
    version: Mapped[Optional["ProjectVersion"]] = relationship("ProjectVersion")
    asset: Mapped["Asset"] = relationship("Asset", back_populates="threats")
    mitigations: Mapped[List["SecurityMitigation"]] = relationship(
        "SecurityMitigation",
        back_populates="threat",
        cascade="all, delete-orphan"
    )


class SecurityMitigation(Base, TimestampMixin):
    """Security mitigation model."""

    __tablename__ = "security_mitigations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    threat_id: Mapped[int] = mapped_column(
        ForeignKey("threat_scenarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    security_goal: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    security_requirement: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    wp29_control_mapping: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    implementation_status: Mapped[str] = mapped_column(
        Enum("planned", "in_progress", "implemented", "verified", name="impl_status"),
        default="planned",
        nullable=False
    )

    # Relationships
    threat: Mapped["ThreatScenario"] = relationship(
        "ThreatScenario",
        back_populates="mitigations"
    )
