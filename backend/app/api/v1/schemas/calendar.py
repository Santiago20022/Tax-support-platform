from __future__ import annotations

from pydantic import BaseModel


class CalendarEntryResponse(BaseModel):
    id: str
    obligation_type_id: str
    title: str
    description: str | None = None
    due_date: str
    periodicity: str
    is_completed: bool
    completed_at: str | None = None


class CalendarMarkCompleteRequest(BaseModel):
    is_completed: bool = True
