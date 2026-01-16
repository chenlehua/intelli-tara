"""Asset management models."""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.project import Project, ProjectVersion
    from app.models.document import Document
    from app.models.threat import ThreatScenario


class Asset(Base, TimestampMixin):
    """Asset model."""

    __tablename__ = "assets"

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
    asset_id: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    subcategory: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_document_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("documents.id"),
        nullable=True
    )

    # Security attributes
    authenticity: Mapped[bool] = mapped_column(Boolean, default=False)
    integrity: Mapped[bool] = mapped_column(Boolean, default=False)
    non_repudiation: Mapped[bool] = mapped_column(Boolean, default=False)
    confidentiality: Mapped[bool] = mapped_column(Boolean, default=False)
    availability: Mapped[bool] = mapped_column(Boolean, default=False)
    authorization: Mapped[bool] = mapped_column(Boolean, default=False)

    # Metadata
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=True)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="assets")
    version: Mapped[Optional["ProjectVersion"]] = relationship("ProjectVersion")
    source_document: Mapped[Optional["Document"]] = relationship("Document")
    threats: Mapped[List["ThreatScenario"]] = relationship(
        "ThreatScenario",
        back_populates="asset",
        cascade="all, delete-orphan"
    )
    outgoing_relations: Mapped[List["AssetRelation"]] = relationship(
        "AssetRelation",
        foreign_keys="AssetRelation.source_asset_id",
        back_populates="source_asset",
        cascade="all, delete-orphan"
    )
    incoming_relations: Mapped[List["AssetRelation"]] = relationship(
        "AssetRelation",
        foreign_keys="AssetRelation.target_asset_id",
        back_populates="target_asset",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        {"mysql_charset": "utf8mb4"},
    )


class AssetRelation(Base):
    """Asset relation model."""

    __tablename__ = "asset_relations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )
    source_asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    target_asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    relation_type: Mapped[str] = mapped_column(String(50), nullable=False)
    protocol: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project")
    source_asset: Mapped["Asset"] = relationship(
        "Asset",
        foreign_keys=[source_asset_id],
        back_populates="outgoing_relations"
    )
    target_asset: Mapped["Asset"] = relationship(
        "Asset",
        foreign_keys=[target_asset_id],
        back_populates="incoming_relations"
    )
