from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID


class ThresholdRepository(ABC):
    @abstractmethod
    async def get_thresholds_map(self, fiscal_year_id: UUID) -> dict[str, Decimal]:
        """Returns a dict mapping threshold code -> value_cop."""
        ...

    @abstractmethod
    async def get_threshold_detail(
        self, fiscal_year_id: UUID, code: str
    ) -> dict | None:
        """Returns full threshold details including UVT value and legal reference."""
        ...
