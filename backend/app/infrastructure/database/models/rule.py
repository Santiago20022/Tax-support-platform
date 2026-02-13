from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class RuleSet(Base):
    __tablename__ = "rule_sets"
    __table_args__ = (
        UniqueConstraint("fiscal_year_id", "version", name="uq_ruleset_fy_version"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fiscal_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("fiscal_years.id"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    changelog: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    fiscal_year: Mapped["FiscalYear"] = relationship(back_populates="rule_sets")  # noqa: F821
    rules: Mapped[list["Rule"]] = relationship(back_populates="rule_set")


class Rule(Base):
    __tablename__ = "rules"
    __table_args__ = (
        Index("ix_rules_ruleset_obligation_priority", "rule_set_id", "obligation_type_id", "priority"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_set_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rule_sets.id"), nullable=False
    )
    obligation_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("obligation_types.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    logic_operator: Mapped[str] = mapped_column(String(5), nullable=False, default="AND")
    priority: Mapped[int] = mapped_column(Integer, default=0)
    result_if_true: Mapped[str] = mapped_column(String(30), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    rule_set: Mapped["RuleSet"] = relationship(back_populates="rules")
    obligation_type: Mapped["ObligationType"] = relationship()  # noqa: F821
    conditions: Mapped[list["RuleCondition"]] = relationship(back_populates="rule")


class RuleCondition(Base):
    __tablename__ = "rule_conditions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rules.id"), nullable=False
    )
    field: Mapped[str] = mapped_column(String(100), nullable=False)
    operator: Mapped[str] = mapped_column(String(20), nullable=False)
    value_type: Mapped[str] = mapped_column(String(20), nullable=False)
    value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    value_secondary: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    rule: Mapped["Rule"] = relationship(back_populates="conditions")
