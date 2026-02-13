from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class ObligationType(Base):
    __tablename__ = "obligation_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    responsible_entity: Mapped[str] = mapped_column(String(255), nullable=False)
    legal_base: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    periodicities: Mapped[list["ObligationPeriodicity"]] = relationship(
        back_populates="obligation_type"
    )


class ObligationPeriodicity(Base):
    __tablename__ = "obligation_periodicities"
    __table_args__ = (
        UniqueConstraint(
            "obligation_type_id", "fiscal_year_id", name="uq_obligation_periodicity"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    obligation_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("obligation_types.id"), nullable=False
    )
    fiscal_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("fiscal_years.id"), nullable=False
    )
    frequency: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    nit_schedule: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    obligation_type: Mapped["ObligationType"] = relationship(back_populates="periodicities")
    fiscal_year: Mapped["FiscalYear"] = relationship()  # noqa: F821
