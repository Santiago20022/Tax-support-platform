from __future__ import annotations

import uuid
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.tax_profile import TaxProfileEntity
from app.domain.interfaces.profile_repository import ProfileRepository
from app.infrastructure.database.models.tax_profile import TaxProfile


class PgProfileRepository(ProfileRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(self, profile: TaxProfileEntity) -> TaxProfileEntity:
        db_profile = TaxProfile(
            id=profile.id or uuid.uuid4(),
            user_id=profile.user_id,
            tenant_id=profile.tenant_id,
            fiscal_year_id=profile.fiscal_year_id,
            persona_type=profile.persona_type,
            regime=profile.regime,
            is_iva_responsable=profile.is_iva_responsable,
            economic_activity_ciiu=profile.economic_activity_ciiu,
            economic_activities=profile.economic_activities,
            ingresos_brutos_cop=profile.ingresos_brutos_cop,
            patrimonio_bruto_cop=profile.patrimonio_bruto_cop,
            has_employees=profile.has_employees,
            employee_count=profile.employee_count,
            city=profile.city,
            department=profile.department,
            has_rut=profile.has_rut,
            has_comercio_registration=profile.has_comercio_registration,
            nit_last_digit=profile.nit_last_digit,
            consignaciones_cop=profile.consignaciones_cop,
            compras_consumos_cop=profile.compras_consumos_cop,
            additional_data=profile.additional_data,
        )
        self._db.add(db_profile)
        await self._db.flush()
        return self._to_entity(db_profile)

    async def get_by_id(self, profile_id: UUID, tenant_id: UUID) -> TaxProfileEntity | None:
        result = await self._db.execute(
            select(TaxProfile).where(
                TaxProfile.id == profile_id,
                TaxProfile.tenant_id == tenant_id,
            )
        )
        db_profile = result.scalar_one_or_none()
        return self._to_entity(db_profile) if db_profile else None

    async def list_by_user(self, user_id: UUID, tenant_id: UUID) -> list[TaxProfileEntity]:
        result = await self._db.execute(
            select(TaxProfile).where(
                TaxProfile.user_id == user_id,
                TaxProfile.tenant_id == tenant_id,
            ).order_by(TaxProfile.created_at.desc())
        )
        return [self._to_entity(row) for row in result.scalars().all()]

    async def update(self, profile: TaxProfileEntity) -> TaxProfileEntity:
        result = await self._db.execute(
            select(TaxProfile).where(TaxProfile.id == profile.id)
        )
        db_profile = result.scalar_one_or_none()
        if not db_profile:
            raise ValueError(f"Profile {profile.id} not found")

        db_profile.persona_type = profile.persona_type
        db_profile.regime = profile.regime
        db_profile.is_iva_responsable = profile.is_iva_responsable
        db_profile.economic_activity_ciiu = profile.economic_activity_ciiu
        db_profile.economic_activities = profile.economic_activities
        db_profile.ingresos_brutos_cop = profile.ingresos_brutos_cop
        db_profile.patrimonio_bruto_cop = profile.patrimonio_bruto_cop
        db_profile.has_employees = profile.has_employees
        db_profile.employee_count = profile.employee_count
        db_profile.city = profile.city
        db_profile.department = profile.department
        db_profile.has_rut = profile.has_rut
        db_profile.has_comercio_registration = profile.has_comercio_registration
        db_profile.nit_last_digit = profile.nit_last_digit
        db_profile.consignaciones_cop = profile.consignaciones_cop
        db_profile.compras_consumos_cop = profile.compras_consumos_cop
        db_profile.additional_data = profile.additional_data
        await self._db.flush()
        return self._to_entity(db_profile)

    async def delete(self, profile_id: UUID, tenant_id: UUID) -> bool:
        result = await self._db.execute(
            delete(TaxProfile).where(
                TaxProfile.id == profile_id,
                TaxProfile.tenant_id == tenant_id,
            )
        )
        return result.rowcount > 0

    @staticmethod
    def _to_entity(db: TaxProfile) -> TaxProfileEntity:
        return TaxProfileEntity(
            id=db.id,
            user_id=db.user_id,
            tenant_id=db.tenant_id,
            fiscal_year_id=db.fiscal_year_id,
            persona_type=db.persona_type,
            regime=db.regime,
            is_iva_responsable=db.is_iva_responsable,
            economic_activity_ciiu=db.economic_activity_ciiu,
            economic_activities=db.economic_activities or [],
            ingresos_brutos_cop=db.ingresos_brutos_cop,
            patrimonio_bruto_cop=db.patrimonio_bruto_cop,
            has_employees=db.has_employees,
            employee_count=db.employee_count,
            city=db.city,
            department=db.department,
            has_rut=db.has_rut,
            has_comercio_registration=db.has_comercio_registration,
            nit_last_digit=db.nit_last_digit,
            consignaciones_cop=db.consignaciones_cop,
            compras_consumos_cop=db.compras_consumos_cop,
            additional_data=db.additional_data or {},
        )
