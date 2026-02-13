from __future__ import annotations

import uuid
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.calendar_entry import CalendarEntryEntity
from app.domain.interfaces.calendar_repository import CalendarRepository
from app.infrastructure.database.models.calendar_entry import CalendarEntry


class PgCalendarRepository(CalendarRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_entries(self, entries: list[CalendarEntryEntity]) -> list[CalendarEntryEntity]:
        for entry in entries:
            db_entry = CalendarEntry(
                id=entry.id or uuid.uuid4(),
                evaluation_id=entry.evaluation_id,
                user_id=entry.user_id,
                tenant_id=entry.tenant_id,
                obligation_type_id=entry.obligation_type_id,
                title=entry.title,
                description=entry.description,
                due_date=entry.due_date,
                periodicity=entry.periodicity,
                is_completed=False,
            )
            self._db.add(db_entry)
        await self._db.flush()
        return entries

    async def list_by_user(self, user_id: UUID, tenant_id: UUID) -> list[CalendarEntryEntity]:
        result = await self._db.execute(
            select(CalendarEntry)
            .where(
                CalendarEntry.user_id == user_id,
                CalendarEntry.tenant_id == tenant_id,
            )
            .order_by(CalendarEntry.due_date)
        )
        return [self._to_entity(e) for e in result.scalars().all()]

    async def mark_completed(self, entry_id: UUID, tenant_id: UUID) -> CalendarEntryEntity | None:
        result = await self._db.execute(
            select(CalendarEntry).where(
                CalendarEntry.id == entry_id,
                CalendarEntry.tenant_id == tenant_id,
            )
        )
        db_entry = result.scalar_one_or_none()
        if not db_entry:
            return None
        db_entry.is_completed = True
        db_entry.completed_at = datetime.now(timezone.utc)
        await self._db.flush()
        return self._to_entity(db_entry)

    @staticmethod
    def _to_entity(db: CalendarEntry) -> CalendarEntryEntity:
        return CalendarEntryEntity(
            id=db.id,
            evaluation_id=db.evaluation_id,
            user_id=db.user_id,
            tenant_id=db.tenant_id,
            obligation_type_id=db.obligation_type_id,
            title=db.title,
            description=db.description,
            due_date=db.due_date,
            periodicity=db.periodicity,
            is_completed=db.is_completed,
            completed_at=db.completed_at,
        )
