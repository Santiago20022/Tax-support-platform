from __future__ import annotations

import uuid
from decimal import Decimal
from uuid import UUID

from app.domain.entities.tax_profile import TaxProfileEntity
from app.domain.interfaces.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, profile_repo: ProfileRepository) -> None:
        self._repo = profile_repo

    async def create_profile(
        self,
        user_id: UUID,
        tenant_id: UUID,
        fiscal_year_id: UUID,
        data: dict,
    ) -> TaxProfileEntity:
        profile = TaxProfileEntity(
            id=uuid.uuid4(),
            user_id=user_id,
            tenant_id=tenant_id,
            fiscal_year_id=fiscal_year_id,
            persona_type=data["persona_type"],
            regime=data["regime"],
            is_iva_responsable=data["is_iva_responsable"],
            ingresos_brutos_cop=Decimal(str(data["ingresos_brutos_cop"])),
            economic_activity_ciiu=data.get("economic_activity_ciiu"),
            economic_activities=data.get("economic_activities", []),
            patrimonio_bruto_cop=Decimal(str(data["patrimonio_bruto_cop"])) if data.get("patrimonio_bruto_cop") else None,
            has_employees=data.get("has_employees", False),
            employee_count=data.get("employee_count", 0),
            city=data.get("city"),
            department=data.get("department"),
            has_rut=data.get("has_rut", False),
            has_comercio_registration=data.get("has_comercio_registration", False),
            nit_last_digit=data.get("nit_last_digit"),
            consignaciones_cop=Decimal(str(data["consignaciones_cop"])) if data.get("consignaciones_cop") else None,
            compras_consumos_cop=Decimal(str(data["compras_consumos_cop"])) if data.get("compras_consumos_cop") else None,
            additional_data=data.get("additional_data", {}),
        )
        return await self._repo.create(profile)

    async def get_profile(self, profile_id: UUID, tenant_id: UUID) -> TaxProfileEntity | None:
        return await self._repo.get_by_id(profile_id, tenant_id)

    async def list_profiles(self, user_id: UUID, tenant_id: UUID) -> list[TaxProfileEntity]:
        return await self._repo.list_by_user(user_id, tenant_id)

    async def update_profile(
        self,
        profile_id: UUID,
        tenant_id: UUID,
        data: dict,
    ) -> TaxProfileEntity:
        existing = await self._repo.get_by_id(profile_id, tenant_id)
        if not existing:
            raise ValueError("Profile not found")

        for field, value in data.items():
            if hasattr(existing, field) and value is not None:
                if field in ("ingresos_brutos_cop", "patrimonio_bruto_cop", "consignaciones_cop", "compras_consumos_cop"):
                    value = Decimal(str(value))
                setattr(existing, field, value)

        return await self._repo.update(existing)

    async def delete_profile(self, profile_id: UUID, tenant_id: UUID) -> bool:
        return await self._repo.delete(profile_id, tenant_id)
