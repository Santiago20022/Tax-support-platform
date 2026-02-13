from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.evaluation import EvaluationEntity


class EvaluationRepository(ABC):
    @abstractmethod
    async def create(self, evaluation: EvaluationEntity) -> EvaluationEntity:
        ...

    @abstractmethod
    async def get_by_id(self, evaluation_id: UUID, tenant_id: UUID) -> EvaluationEntity | None:
        ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID, tenant_id: UUID) -> list[EvaluationEntity]:
        ...
