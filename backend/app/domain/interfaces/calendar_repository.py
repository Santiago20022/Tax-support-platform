from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.calendar_entry import CalendarEntryEntity


class CalendarRepository(ABC):
    @abstractmethod
    async def create_entries(self, entries: list[CalendarEntryEntity]) -> list[CalendarEntryEntity]:
        ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID, tenant_id: UUID) -> list[CalendarEntryEntity]:
        ...

    @abstractmethod
    async def mark_completed(self, entry_id: UUID, tenant_id: UUID) -> CalendarEntryEntity | None:
        ...
