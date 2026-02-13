from __future__ import annotations

from pydantic import BaseModel


class ObligationTypeResponse(BaseModel):
    id: str
    code: str
    name: str
    category: str
    description: str
    responsible_entity: str
    legal_base: str | None = None
    is_active: bool
    display_order: int
