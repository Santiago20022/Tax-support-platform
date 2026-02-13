from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.obligations import ObligationTypeResponse
from app.infrastructure.database.models.obligation import ObligationType
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/obligations", tags=["obligations"])


@router.get("", response_model=list[ObligationTypeResponse])
async def list_obligations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ObligationType)
        .where(ObligationType.is_active.is_(True))
        .order_by(ObligationType.display_order)
    )
    obligations = result.scalars().all()
    return [
        ObligationTypeResponse(
            id=str(o.id),
            code=o.code,
            name=o.name,
            category=o.category,
            description=o.description,
            responsible_entity=o.responsible_entity,
            legal_base=o.legal_base,
            is_active=o.is_active,
            display_order=o.display_order,
        )
        for o in obligations
    ]


@router.get("/{code}", response_model=ObligationTypeResponse)
async def get_obligation(code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ObligationType).where(ObligationType.code == code)
    )
    obligation = result.scalar_one_or_none()
    if not obligation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Obligation '{code}' not found",
        )
    return ObligationTypeResponse(
        id=str(obligation.id),
        code=obligation.code,
        name=obligation.name,
        category=obligation.category,
        description=obligation.description,
        responsible_entity=obligation.responsible_entity,
        legal_base=obligation.legal_base,
        is_active=obligation.is_active,
        display_order=obligation.display_order,
    )
