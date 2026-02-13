from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class ProfileCreateRequest(BaseModel):
    fiscal_year_id: str
    persona_type: str
    regime: str
    is_iva_responsable: bool
    ingresos_brutos_cop: Decimal
    economic_activity_ciiu: str | None = None
    economic_activities: list[str] = []
    patrimonio_bruto_cop: Decimal | None = None
    has_employees: bool = False
    employee_count: int = 0
    city: str | None = None
    department: str | None = None
    has_rut: bool = False
    has_comercio_registration: bool = False
    nit_last_digit: int | None = None
    consignaciones_cop: Decimal | None = None
    compras_consumos_cop: Decimal | None = None
    additional_data: dict = {}


class ProfileUpdateRequest(BaseModel):
    persona_type: str | None = None
    regime: str | None = None
    is_iva_responsable: bool | None = None
    ingresos_brutos_cop: Decimal | None = None
    economic_activity_ciiu: str | None = None
    economic_activities: list[str] | None = None
    patrimonio_bruto_cop: Decimal | None = None
    has_employees: bool | None = None
    employee_count: int | None = None
    city: str | None = None
    department: str | None = None
    has_rut: bool | None = None
    has_comercio_registration: bool | None = None
    nit_last_digit: int | None = None
    consignaciones_cop: Decimal | None = None
    compras_consumos_cop: Decimal | None = None
    additional_data: dict | None = None


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    fiscal_year_id: str
    persona_type: str
    regime: str
    is_iva_responsable: bool
    ingresos_brutos_cop: float
    economic_activity_ciiu: str | None = None
    patrimonio_bruto_cop: float | None = None
    has_employees: bool
    employee_count: int
    city: str | None = None
    department: str | None = None
    has_rut: bool
    has_comercio_registration: bool
    nit_last_digit: int | None = None
    consignaciones_cop: float | None = None
    compras_consumos_cop: float | None = None

    model_config = {"from_attributes": True}
