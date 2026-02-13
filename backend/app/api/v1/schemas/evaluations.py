from __future__ import annotations

from pydantic import BaseModel


class EvaluationCreateRequest(BaseModel):
    tax_profile_id: str


class ConditionEvaluatedResponse(BaseModel):
    field: str
    operator: str
    profile_value: object = None
    threshold_code: str | None = None
    threshold_value: object = None
    passes: bool
    description: str | None = None


class ObligationResponse(BaseModel):
    code: str
    name: str
    category: str | None = None
    responsible_entity: str | None = None


class CalendarEntryBriefResponse(BaseModel):
    title: str
    due_date: str
    periodicity: str


class EvaluationResultResponse(BaseModel):
    obligation: ObligationResponse
    result: str
    periodicity: str | None = None
    explanation: str
    legal_references: list[str] = []
    conditions_evaluated: list[dict] = []
    calendar_entries: list[CalendarEntryBriefResponse] = []


class EvaluationSummaryResponse(BaseModel):
    total_obligations_evaluated: int
    applies: int
    does_not_apply: int
    conditional: int
    needs_more_info: int


class DisclaimerResponse(BaseModel):
    version: int = 1
    text: str
    is_informational_only: bool = True


class EvaluationResponse(BaseModel):
    id: str
    fiscal_year: int | None = None
    rule_set_version: int | None = None
    evaluated_at: str
    profile_summary: dict = {}
    results: list[EvaluationResultResponse] = []
    summary: EvaluationSummaryResponse | None = None
    disclaimer: DisclaimerResponse | None = None


class EvaluationListItemResponse(BaseModel):
    id: str
    fiscal_year_id: str
    status: str
    evaluated_at: str
    summary: EvaluationSummaryResponse | None = None
