"""Calendar service - generates and manages personalized tax calendars."""
from __future__ import annotations

import uuid
from datetime import date
from uuid import UUID

from app.domain.entities.calendar_entry import CalendarEntryEntity
from app.domain.entities.evaluation import EvaluationEntity
from app.domain.interfaces.calendar_repository import CalendarRepository


class CalendarService:
    def __init__(self, calendar_repo: CalendarRepository) -> None:
        self._repo = calendar_repo

    async def generate_calendar(
        self,
        evaluation: EvaluationEntity,
        nit_last_digit: int | None,
    ) -> list[CalendarEntryEntity]:
        entries: list[CalendarEntryEntity] = []

        for result in evaluation.results:
            if result.result != "applies":
                continue

            # Generate calendar entries based on the result's calendar_entries
            for cal_data in result.calendar_entries:
                entry = CalendarEntryEntity(
                    id=uuid.uuid4(),
                    evaluation_id=evaluation.id,
                    user_id=evaluation.user_id,
                    tenant_id=evaluation.tenant_id,
                    obligation_type_id=result.obligation_type_id,
                    title=cal_data.get("title", f"{result.obligation_name}"),
                    description=cal_data.get("description"),
                    due_date=date.fromisoformat(cal_data["due_date"])
                    if isinstance(cal_data.get("due_date"), str)
                    else cal_data.get("due_date", date.today()),
                    periodicity=cal_data.get("periodicity", result.periodicity or "anual"),
                )
                entries.append(entry)

        if entries:
            await self._repo.create_entries(entries)

        return entries

    async def list_calendar(
        self, user_id: UUID, tenant_id: UUID
    ) -> list[CalendarEntryEntity]:
        return await self._repo.list_by_user(user_id, tenant_id)

    async def mark_completed(
        self, entry_id: UUID, tenant_id: UUID
    ) -> CalendarEntryEntity | None:
        return await self._repo.mark_completed(entry_id, tenant_id)
