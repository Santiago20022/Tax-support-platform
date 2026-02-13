"""Admin service - manage fiscal years, thresholds, and rule sets."""
from __future__ import annotations

import uuid
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.rule import RuleSetEntity
from app.domain.interfaces.rule_repository import RuleRepository
from app.infrastructure.database.models.fiscal_year import FiscalYear
from app.infrastructure.database.models.threshold import Threshold


class AdminService:
    def __init__(self, db: AsyncSession, rule_repo: RuleRepository) -> None:
        self._db = db
        self._rule_repo = rule_repo

    # --- Fiscal Years ---

    async def list_fiscal_years(self) -> list[dict]:
        result = await self._db.execute(
            select(FiscalYear).order_by(FiscalYear.year.desc())
        )
        return [
            {
                "id": str(fy.id),
                "year": fy.year,
                "status": fy.status,
                "uvt_value": float(fy.uvt_value),
                "notes": fy.notes,
            }
            for fy in result.scalars().all()
        ]

    async def create_fiscal_year(self, year: int, uvt_value: Decimal, notes: str | None = None) -> dict:
        fy = FiscalYear(
            id=uuid.uuid4(),
            year=year,
            status="draft",
            uvt_value=uvt_value,
            notes=notes,
        )
        self._db.add(fy)
        await self._db.flush()
        return {
            "id": str(fy.id),
            "year": fy.year,
            "status": fy.status,
            "uvt_value": float(fy.uvt_value),
        }

    # --- Thresholds ---

    async def list_thresholds(self, fiscal_year_id: UUID) -> list[dict]:
        result = await self._db.execute(
            select(Threshold).where(Threshold.fiscal_year_id == fiscal_year_id)
        )
        return [
            {
                "id": str(t.id),
                "code": t.code,
                "label": t.label,
                "value_uvt": float(t.value_uvt) if t.value_uvt else None,
                "value_cop": float(t.value_cop) if t.value_cop else None,
                "description": t.description,
                "legal_reference": t.legal_reference,
            }
            for t in result.scalars().all()
        ]

    async def create_or_update_threshold(
        self,
        fiscal_year_id: UUID,
        code: str,
        label: str,
        value_uvt: Decimal | None = None,
        value_cop: Decimal | None = None,
        description: str | None = None,
        legal_reference: str | None = None,
    ) -> dict:
        result = await self._db.execute(
            select(Threshold).where(
                Threshold.fiscal_year_id == fiscal_year_id,
                Threshold.code == code,
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.label = label
            existing.value_uvt = value_uvt
            existing.value_cop = value_cop
            existing.description = description
            existing.legal_reference = legal_reference
            await self._db.flush()
            t = existing
        else:
            t = Threshold(
                id=uuid.uuid4(),
                fiscal_year_id=fiscal_year_id,
                code=code,
                label=label,
                value_uvt=value_uvt,
                value_cop=value_cop,
                description=description,
                legal_reference=legal_reference,
            )
            self._db.add(t)
            await self._db.flush()

        return {
            "id": str(t.id),
            "code": t.code,
            "label": t.label,
            "value_uvt": float(t.value_uvt) if t.value_uvt else None,
            "value_cop": float(t.value_cop) if t.value_cop else None,
        }

    # --- Rule Sets ---

    async def list_rule_sets(self) -> list[dict]:
        from app.infrastructure.database.models.rule import RuleSet

        result = await self._db.execute(
            select(RuleSet).order_by(RuleSet.created_at.desc())
        )
        return [
            {
                "id": str(rs.id),
                "fiscal_year_id": str(rs.fiscal_year_id),
                "version": rs.version,
                "status": rs.status,
                "published_at": rs.published_at.isoformat() if rs.published_at else None,
            }
            for rs in result.scalars().all()
        ]

    async def create_rule_set(self, fiscal_year_id: UUID, version: int) -> dict:
        rule_set = RuleSetEntity(
            id=uuid.uuid4(),
            fiscal_year_id=fiscal_year_id,
            version=version,
            status="draft",
        )
        created = await self._rule_repo.create_rule_set(rule_set)
        return {
            "id": str(created.id),
            "fiscal_year_id": str(created.fiscal_year_id),
            "version": created.version,
            "status": created.status,
        }

    async def publish_rule_set(self, rule_set_id: UUID) -> dict:
        published = await self._rule_repo.publish_rule_set(rule_set_id)
        return {
            "id": str(published.id),
            "status": published.status,
        }
