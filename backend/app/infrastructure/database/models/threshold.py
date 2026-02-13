from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class Threshold(Base):
    __tablename__ = "thresholds"
    __table_args__ = (
        UniqueConstraint("fiscal_year_id", "code", name="uq_thresholds_fy_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fiscal_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("fiscal_years.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    value_uvt: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    value_cop: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    legal_reference: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    fiscal_year: Mapped["FiscalYear"] = relationship(back_populates="thresholds")  # noqa: F821
