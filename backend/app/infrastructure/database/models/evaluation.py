from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False
    )
    tax_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tax_profiles.id"), nullable=False
    )
    rule_set_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rule_sets.id"), nullable=False
    )
    fiscal_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("fiscal_years.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    profile_snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    results: Mapped[list["EvaluationResult"]] = relationship(back_populates="evaluation")
    tax_profile: Mapped["TaxProfile"] = relationship()  # noqa: F821
    rule_set: Mapped["RuleSet"] = relationship()  # noqa: F821


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evaluations.id"), nullable=False
    )
    obligation_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("obligation_types.id"), nullable=False
    )
    result: Mapped[str] = mapped_column(String(30), nullable=False)
    triggered_rule_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rules.id"), nullable=True
    )
    conditions_evaluated: Mapped[dict] = mapped_column(JSONB, nullable=False)
    explanation_es: Mapped[str] = mapped_column(Text, nullable=False)
    explanation_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    legal_references: Mapped[dict] = mapped_column(JSONB, default=list)
    periodicity: Mapped[str | None] = mapped_column(String(30), nullable=True)
    responsible_entity: Mapped[str | None] = mapped_column(String(255), nullable=True)

    evaluation: Mapped["Evaluation"] = relationship(back_populates="results")
    obligation_type: Mapped["ObligationType"] = relationship()  # noqa: F821
    triggered_rule: Mapped["Rule | None"] = relationship()  # noqa: F821
