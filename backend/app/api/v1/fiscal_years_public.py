from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.fiscal_year import FiscalYear
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/fiscal-years", tags=["fiscal-years"])


@router.get("")
async def list_active_fiscal_years(
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint: returns active fiscal years for profile creation."""
    result = await db.execute(
        select(FiscalYear)
        .where(FiscalYear.status == "active")
        .order_by(FiscalYear.year.desc())
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
