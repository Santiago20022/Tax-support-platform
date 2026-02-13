from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.rule import RuleEntity, RuleSetEntity


class RuleRepository(ABC):
    @abstractmethod
    async def get_active_rule_set(self, fiscal_year_id: UUID) -> RuleSetEntity | None:
        ...

    @abstractmethod
    async def get_rules_for_obligation(
        self, rule_set_id: UUID, obligation_type_id: UUID
    ) -> list[RuleEntity]:
        ...

    @abstractmethod
    async def get_rule_set_by_id(self, rule_set_id: UUID) -> RuleSetEntity | None:
        ...

    @abstractmethod
    async def create_rule_set(self, rule_set: RuleSetEntity) -> RuleSetEntity:
        ...

    @abstractmethod
    async def publish_rule_set(self, rule_set_id: UUID) -> RuleSetEntity:
        ...
