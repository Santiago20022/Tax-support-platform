from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID


@dataclass
class TaxProfileEntity:
    id: UUID
    user_id: UUID
    tenant_id: UUID
    fiscal_year_id: UUID
    persona_type: str
    regime: str
    is_iva_responsable: bool
    ingresos_brutos_cop: Decimal
    has_employees: bool = False
    employee_count: int = 0
    economic_activity_ciiu: str | None = None
    economic_activities: list = field(default_factory=list)
    patrimonio_bruto_cop: Decimal | None = None
    city: str | None = None
    department: str | None = None
    has_rut: bool = False
    has_comercio_registration: bool = False
    nit_last_digit: int | None = None
    consignaciones_cop: Decimal | None = None
    compras_consumos_cop: Decimal | None = None
    additional_data: dict = field(default_factory=dict)

    def get_field_value(self, field_name: str) -> object:
        """Get a profile field value by name, supporting nested additional_data."""
        if hasattr(self, field_name):
            return getattr(self, field_name)
        return self.additional_data.get(field_name)

    def to_snapshot(self) -> dict:
        """Create an immutable snapshot of the profile for evaluation records."""
        return {
            "persona_type": self.persona_type,
            "regime": self.regime,
            "is_iva_responsable": self.is_iva_responsable,
            "ingresos_brutos_cop": float(self.ingresos_brutos_cop),
            "patrimonio_bruto_cop": float(self.patrimonio_bruto_cop) if self.patrimonio_bruto_cop else None,
            "has_employees": self.has_employees,
            "employee_count": self.employee_count,
            "economic_activity_ciiu": self.economic_activity_ciiu,
            "economic_activities": self.economic_activities,
            "city": self.city,
            "department": self.department,
            "has_rut": self.has_rut,
            "has_comercio_registration": self.has_comercio_registration,
            "nit_last_digit": self.nit_last_digit,
            "consignaciones_cop": float(self.consignaciones_cop) if self.consignaciones_cop else None,
            "compras_consumos_cop": float(self.compras_consumos_cop) if self.compras_consumos_cop else None,
            "additional_data": self.additional_data,
        }
