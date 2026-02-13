from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.tax_profile import TaxProfileEntity


class ProfileRepository(ABC):
    @abstractmethod
    async def create(self, profile: TaxProfileEntity) -> TaxProfileEntity:
        ...

    @abstractmethod
    async def get_by_id(self, profile_id: UUID, tenant_id: UUID) -> TaxProfileEntity | None:
        ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID, tenant_id: UUID) -> list[TaxProfileEntity]:
        ...

    @abstractmethod
    async def update(self, profile: TaxProfileEntity) -> TaxProfileEntity:
        ...

    @abstractmethod
    async def delete(self, profile_id: UUID, tenant_id: UUID) -> bool:
        ...
