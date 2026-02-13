from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass
class ObligationTypeEntity:
    id: UUID
    code: str
    name: str
    category: str
    description: str
    responsible_entity: str
    legal_base: str | None = None
    is_active: bool = True
    display_order: int = 0
