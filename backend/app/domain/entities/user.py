from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class UserEntity:
    id: UUID
    tenant_id: UUID
    email: str
    full_name: str
    role: str = "user"
    is_active: bool = True
    last_login_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)

    def is_admin(self) -> bool:
        return self.role in ("admin", "super_admin")

    def is_super_admin(self) -> bool:
        return self.role == "super_admin"
