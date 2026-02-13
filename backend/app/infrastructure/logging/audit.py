from __future__ import annotations

import uuid
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.audit_log import AuditLog


async def write_audit_log(
    db: AsyncSession,
    action: str,
    entity_type: str,
    entity_id: UUID | None = None,
    tenant_id: UUID | None = None,
    user_id: UUID | None = None,
    payload: dict | None = None,
    ip_address: str | None = None,
) -> None:
    log_entry = AuditLog(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        payload=payload,
        ip_address=ip_address,
    )
    db.add(log_entry)
