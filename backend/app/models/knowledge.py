"""Knowledge base models."""

from typing import Optional

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class KbWp29Threat(Base):
    """WP29 threat knowledge base model."""

    __tablename__ = "kb_wp29_threats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    subcategory: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    threat_description_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    threat_description_zh: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mitigation_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mitigation_zh: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class KbAttackPattern(Base):
    """Attack pattern knowledge base model."""

    __tablename__ = "kb_attack_patterns"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pattern_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    prerequisites: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attack_steps: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mitigations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    related_cwe: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    related_capec: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)


class KbSecurityRequirement(Base):
    """Security requirement template knowledge base model."""

    __tablename__ = "kb_security_requirements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    requirement_template: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    related_stride: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    related_wp29: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
