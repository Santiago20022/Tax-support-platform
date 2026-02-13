from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.threshold_repository import ThresholdRepository
from app.infrastructure.database.models.threshold import Threshold


class PgThresholdRepository(ThresholdRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_thresholds_map(self, fiscal_year_id: UUID) -> dict[str, Decimal]:
        result = await self._db.execute(
            select(Threshold).where(Threshold.fiscal_year_id == fiscal_year_id)
        )
        thresholds = result.scalars().all()
        return {t.code: t.value_cop for t in thresholds if t.value_cop is not None}

    async def get_threshold_detail(self, fiscal_year_id: UUID, code: str) -> dict | None:
        result = await self._db.execute(
            select(Threshold).where(
                Threshold.fiscal_year_id == fiscal_year_id,
                Threshold.code == code,
            )
        )
        t = result.scalar_one_or_none()
        if not t:
            return None
        return {
            "code": t.code,
            "label": t.label,
            "value_uvt": float(t.value_uvt) if t.value_uvt else None,
            "value_cop": float(t.value_cop) if t.value_cop else None,
            "description": t.description,
            "legal_reference": t.legal_reference,
        }
