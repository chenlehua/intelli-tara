"""Project management models."""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.document import Document
    from app.models.asset import Asset
    from app.models.threat import ThreatScenario
    from app.models.report import Report


class Project(Base, TimestampMixin):
    """Project model."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("draft", "analyzing", "paused", "completed", "archived", name="project_status"),
        default="draft",
        nullable=False,
        index=True
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Relationships
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="owned_projects",
        foreign_keys=[owner_id]
    )
    versions: Mapped[List["ProjectVersion"]] = relationship(
        "ProjectVersion",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    members: Mapped[List["ProjectMember"]] = relationship(
        "ProjectMember",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    config: Mapped[Optional["ProjectConfig"]] = relationship(
        "ProjectConfig",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan"
    )
    documents: Mapped[List["Document"]] = relationship(
        "Document",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    assets: Mapped[List["Asset"]] = relationship(
        "Asset",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    threats: Mapped[List["ThreatScenario"]] = relationship(
        "ThreatScenario",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    reports: Mapped[List["Report"]] = relationship(
        "Report",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class ProjectVersion(Base, TimestampMixin):
    """Project version model."""

    __tablename__ = "project_versions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )
    version: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("draft", "active", "archived", name="version_status"),
        default="draft",
        nullable=False
    )
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="versions")
    creator: Mapped["User"] = relationship("User")

    __table_args__ = (
        {"mysql_charset": "utf8mb4"},
    )


class ProjectMember(Base):
    """Project member association model."""

    __tablename__ = "project_members"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    role: Mapped[str] = mapped_column(
        Enum("owner", "admin", "editor", "viewer", name="member_role"),
        default="viewer",
        nullable=False
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="project_memberships")


class ProjectConfig(Base):
    """Project configuration model."""

    __tablename__ = "project_configs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    item_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    item_boundary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    functional_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    config_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="config")
