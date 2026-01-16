"""Report management models."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.project import Project, ProjectVersion
    from app.models.user import User


class Report(Base, TimestampMixin):
    """Report model."""

    __tablename__ = "reports"

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
    report_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    report_version: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("generating", "completed", "failed", name="report_status"),
        default="generating",
        nullable=False
    )
    storage_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    generated_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    author: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    reviewer: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    approver: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="reports")
    version: Mapped[Optional["ProjectVersion"]] = relationship("ProjectVersion")
    generator: Mapped["User"] = relationship("User")
