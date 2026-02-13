from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class EvaluationResultEntity:
    obligation_type_id: UUID
    obligation_code: str
    obligation_name: str
    result: str  # applies / does_not_apply / needs_more_info / conditional
    periodicity: str | None = None
    responsible_entity: str | None = None
    triggered_rule_id: UUID | None = None
    conditions_evaluated: list[dict] = field(default_factory=list)
    explanation_es: str = ""
    legal_references: list[str] = field(default_factory=list)
    calendar_entries: list[dict] = field(default_factory=list)


@dataclass
class EvaluationEntity:
    id: UUID
    user_id: UUID
    tenant_id: UUID
    tax_profile_id: UUID
    rule_set_id: UUID
    fiscal_year_id: UUID
    status: str
    evaluated_at: datetime
    profile_snapshot: dict
    results: list[EvaluationResultEntity] = field(default_factory=list)

    def summary(self) -> dict:
        total = len(self.results)
        applies = sum(1 for r in self.results if r.result == "applies")
        does_not_apply = sum(1 for r in self.results if r.result == "does_not_apply")
        conditional = sum(1 for r in self.results if r.result == "conditional")
        needs_more_info = sum(1 for r in self.results if r.result == "needs_more_info")
        return {
            "total_obligations_evaluated": total,
            "applies": applies,
            "does_not_apply": does_not_apply,
            "conditional": conditional,
            "needs_more_info": needs_more_info,
        }
