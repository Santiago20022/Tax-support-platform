from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class TaxProfile(Base):
    __tablename__ = "tax_profiles"
    __table_args__ = (
        UniqueConstraint("user_id", "fiscal_year_id", name="uq_profile_user_fy"),
        Index("ix_tax_profiles_tenant", "tenant_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False
    )
    fiscal_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("fiscal_years.id"), nullable=False
    )
    persona_type: Mapped[str] = mapped_column(String(30), nullable=False)
    regime: Mapped[str] = mapped_column(String(30), nullable=False)
    is_iva_responsable: Mapped[bool] = mapped_column(Boolean, nullable=False)
    economic_activity_ciiu: Mapped[str | None] = mapped_column(String(10), nullable=True)
    economic_activities: Mapped[dict] = mapped_column(JSONB, default=list)
    ingresos_brutos_cop: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    patrimonio_bruto_cop: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    has_employees: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    employee_count: Mapped[int] = mapped_column(Integer, default=0)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    has_rut: Mapped[bool] = mapped_column(Boolean, default=False)
    has_comercio_registration: Mapped[bool] = mapped_column(Boolean, default=False)
    nit_last_digit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    consignaciones_cop: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    compras_consumos_cop: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    additional_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="tax_profiles")  # noqa: F821
    tenant: Mapped["Tenant"] = relationship()  # noqa: F821
    fiscal_year: Mapped["FiscalYear"] = relationship()  # noqa: F821
