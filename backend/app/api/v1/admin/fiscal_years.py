from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, require_admin
from app.application.admin_service import AdminService
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.pg_rule_repo import PgRuleRepository

router = APIRouter(prefix="/admin/fiscal-years", tags=["admin"])


class FiscalYearCreateRequest(BaseModel):
    year: int
    uvt_value: Decimal
    notes: str | None = None


class ThresholdCreateRequest(BaseModel):
    code: str
    label: str
    value_uvt: Decimal | None = None
    value_cop: Decimal | None = None
    description: str | None = None
    legal_reference: str | None = None


@router.get("")
async def list_fiscal_years(
    db: AsyncSession = Depends(get_db),
    admin: CurrentUser = Depends(require_admin),
):
    service = AdminService(db, PgRuleRepository(db))
    return await service.list_fiscal_years()


@router.post("", status_code=201)
async def create_fiscal_year(
    request: FiscalYearCreateRequest,
    db: AsyncSession = Depends(get_db),
    admin: CurrentUser = Depends(require_admin),
):
    service = AdminService(db, PgRuleRepository(db))
    return await service.create_fiscal_year(
        year=request.year,
        uvt_value=request.uvt_value,
        notes=request.notes,
    )


@router.get("/{fiscal_year_id}/thresholds")
async def list_thresholds(
    fiscal_year_id: str,
    db: AsyncSession = Depends(get_db),
    admin: CurrentUser = Depends(require_admin),
):
    service = AdminService(db, PgRuleRepository(db))
    return await service.list_thresholds(UUID(fiscal_year_id))


@router.post("/{fiscal_year_id}/thresholds", status_code=201)
async def create_threshold(
    fiscal_year_id: str,
    request: ThresholdCreateRequest,
    db: AsyncSession = Depends(get_db),
    admin: CurrentUser = Depends(require_admin),
):
    service = AdminService(db, PgRuleRepository(db))
    return await service.create_or_update_threshold(
        fiscal_year_id=UUID(fiscal_year_id),
        code=request.code,
        label=request.label,
        value_uvt=request.value_uvt,
        value_cop=request.value_cop,
        description=request.description,
        legal_reference=request.legal_reference,
    )
