from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class FiscalYearEntity:
    id: UUID
    year: int
    status: str
    uvt_value: Decimal
    notes: str | None = None

    def is_active(self) -> bool:
        return self.status == "active"

    def cop_from_uvt(self, uvt_amount: Decimal) -> Decimal:
        """Convert UVT amount to COP using this fiscal year's UVT value."""
        return uvt_amount * self.uvt_value
