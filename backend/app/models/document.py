"""Document management models."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, Enum, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.project import Project, ProjectVersion
    from app.models.user import User


class Document(Base, TimestampMixin):
    """Document model."""

    __tablename__ = "documents"

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
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(
        Enum(
            "architecture",
            "function_list",
            "communication_matrix",
            "interface_definition",
            "asset_list",
            "security_requirement",
            "security_measure",
            "other",
            name="document_category"
        ),
        default="other",
        nullable=False
    )
    parse_status: Mapped[str] = mapped_column(
        Enum("pending", "parsing", "completed", "failed", name="parse_status"),
        default="pending",
        nullable=False,
        index=True
    )
    parse_result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    parse_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="documents")
    version: Mapped[Optional["ProjectVersion"]] = relationship("ProjectVersion")
    uploader: Mapped["User"] = relationship("User")
