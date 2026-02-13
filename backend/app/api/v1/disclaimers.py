from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, get_current_user
from app.infrastructure.database.models.disclaimer import DisclaimerAcceptance, DisclaimerVersion
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/disclaimers", tags=["disclaimers"])


class DisclaimerCurrentResponse(BaseModel):
    id: str
    version: int
    content_es: str
    content_en: str | None = None


class DisclaimerAcceptRequest(BaseModel):
    disclaimer_version_id: str


class DisclaimerAcceptResponse(BaseModel):
    accepted: bool
    accepted_at: str


@router.get("/current", response_model=DisclaimerCurrentResponse)
async def get_current_disclaimer(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DisclaimerVersion).where(DisclaimerVersion.is_current.is_(True))
    )
    disclaimer = result.scalar_one_or_none()
    if not disclaimer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active disclaimer found",
        )
    return DisclaimerCurrentResponse(
        id=str(disclaimer.id),
        version=disclaimer.version,
        content_es=disclaimer.content_es,
        content_en=disclaimer.content_en,
    )


@router.post("/accept", response_model=DisclaimerAcceptResponse, status_code=status.HTTP_201_CREATED)
async def accept_disclaimer(
    request_body: DisclaimerAcceptRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    acceptance = DisclaimerAcceptance(
        id=uuid.uuid4(),
        user_id=user.user_id,
        disclaimer_version_id=uuid.UUID(request_body.disclaimer_version_id),
        accepted_at=datetime.now(timezone.utc),
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(acceptance)
    return DisclaimerAcceptResponse(
        accepted=True,
        accepted_at=acceptance.accepted_at.isoformat(),
    )
