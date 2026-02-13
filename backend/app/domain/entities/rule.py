from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class RuleConditionEntity:
    id: UUID
    rule_id: UUID
    field: str
    operator: str
    value_type: str
    value: str | None = None
    value_secondary: str | None = None
    description: str | None = None


@dataclass
class RuleEntity:
    id: UUID
    rule_set_id: UUID
    obligation_type_id: UUID
    code: str
    name: str
    logic_operator: str = "AND"
    priority: int = 0
    result_if_true: str = "applies"
    is_active: bool = True
    description: str | None = None
    conditions: list[RuleConditionEntity] = field(default_factory=list)


@dataclass
class RuleSetEntity:
    id: UUID
    fiscal_year_id: UUID
    version: int = 1
    status: str = "draft"
    rules: list[RuleEntity] = field(default_factory=list)
