from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, get_current_user
from app.api.v1.schemas.calendar import CalendarEntryResponse, CalendarMarkCompleteRequest
from app.application.calendar_service import CalendarService
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.pg_calendar_repo import PgCalendarRepository

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("", response_model=list[CalendarEntryResponse])
async def list_calendar(
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    service = CalendarService(PgCalendarRepository(db))
    entries = await service.list_calendar(user.user_id, user.tenant_id)
    return [
        CalendarEntryResponse(
            id=str(e.id),
            obligation_type_id=str(e.obligation_type_id),
            title=e.title,
            description=e.description,
            due_date=e.due_date.isoformat(),
            periodicity=e.periodicity,
            is_completed=e.is_completed,
            completed_at=e.completed_at.isoformat() if e.completed_at else None,
        )
        for e in entries
    ]


@router.patch("/{entry_id}", response_model=CalendarEntryResponse)
async def mark_completed(
    entry_id: str,
    request: CalendarMarkCompleteRequest,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    service = CalendarService(PgCalendarRepository(db))
    entry = await service.mark_completed(UUID(entry_id), user.tenant_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar entry not found",
        )
    return CalendarEntryResponse(
        id=str(entry.id),
        obligation_type_id=str(entry.obligation_type_id),
        title=entry.title,
        description=entry.description,
        due_date=entry.due_date.isoformat(),
        periodicity=entry.periodicity,
        is_completed=entry.is_completed,
        completed_at=entry.completed_at.isoformat() if entry.completed_at else None,
    )
