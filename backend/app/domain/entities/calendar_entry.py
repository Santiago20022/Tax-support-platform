from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass
class CalendarEntryEntity:
    id: UUID
    evaluation_id: UUID
    user_id: UUID
    tenant_id: UUID
    obligation_type_id: UUID
    title: str
    due_date: date
    periodicity: str
    description: str | None = None
    is_completed: bool = False
    completed_at: datetime | None = None
