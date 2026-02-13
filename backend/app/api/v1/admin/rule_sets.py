from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, require_admin
from app.application.admin_service import AdminService
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.pg_rule_repo import PgRuleRepository

router = APIRouter(prefix="/admin/rule-sets", tags=["admin"])


class RuleSetCreateRequest(BaseModel):
    fiscal_year_id: str
    version: int = 1


@router.get("")
async def list_rule_sets(
    db: AsyncSession = Depends(get_db),
    admin: CurrentUser = Depends(require_admin),
):
    service = AdminService(db, PgRuleRepository(db))
    return await service.list_rule_sets()


@router.post("", status_code=201)
async def create_rule_set(
    request: RuleSetCreateRequest,
    db: AsyncSession = Depends(get_db),
    admin: CurrentUser = Depends(require_admin),
):
    service = AdminService(db, PgRuleRepository(db))
    return await service.create_rule_set(
        fiscal_year_id=UUID(request.fiscal_year_id),
        version=request.version,
    )


@router.post("/{rule_set_id}/publish")
async def publish_rule_set(
    rule_set_id: str,
    db: AsyncSession = Depends(get_db),
    admin: CurrentUser = Depends(require_admin),
):
    service = AdminService(db, PgRuleRepository(db))
    return await service.publish_rule_set(UUID(rule_set_id))
