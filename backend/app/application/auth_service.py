from __future__ import annotations

import uuid
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.auth.jwt_provider import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.infrastructure.database.models.tenant import Tenant
from app.infrastructure.database.models.user import User


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def register(
        self,
        email: str,
        password: str,
        full_name: str,
        tenant_slug: str | None = None,
    ) -> dict:
        # Get or create default tenant
        if tenant_slug:
            result = await self._db.execute(
                select(Tenant).where(Tenant.slug == tenant_slug)
            )
            tenant = result.scalar_one_or_none()
            if not tenant:
                raise ValueError(f"Tenant '{tenant_slug}' not found")
        else:
            result = await self._db.execute(
                select(Tenant).where(Tenant.slug == "default")
            )
            tenant = result.scalar_one_or_none()
            if not tenant:
                tenant = Tenant(
                    id=uuid.uuid4(),
                    name="Default",
                    slug="default",
                    is_active=True,
                )
                self._db.add(tenant)
                await self._db.flush()

        # Check if user exists
        existing = await self._db.execute(
            select(User).where(
                User.tenant_id == tenant.id,
                User.email == email,
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError("User with this email already exists")

        user = User(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            role="user",
            is_active=True,
        )
        self._db.add(user)
        await self._db.flush()

        access_token = create_access_token(user.id, tenant.id, user.role)
        refresh_token = create_refresh_token(user.id, tenant.id)

        return {
            "user_id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "tenant_id": str(tenant.id),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def login(self, email: str, password: str, tenant_slug: str | None = None) -> dict:
        query = select(User).join(Tenant)
        if tenant_slug:
            query = query.where(Tenant.slug == tenant_slug, User.email == email)
        else:
            query = query.where(User.email == email)

        result = await self._db.execute(query)
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Account is disabled")

        user.last_login_at = datetime.now(timezone.utc)
        await self._db.flush()

        access_token = create_access_token(user.id, user.tenant_id, user.role)
        refresh_token = create_refresh_token(user.id, user.tenant_id)

        return {
            "user_id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "tenant_id": str(user.tenant_id),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh(self, refresh_token_str: str) -> dict:
        payload = decode_token(refresh_token_str)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        user_id = UUID(payload["sub"])
        tenant_id = UUID(payload["tenant_id"])

        result = await self._db.execute(
            select(User).where(User.id == user_id, User.is_active.is_(True))
        )
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError("User not found")

        access_token = create_access_token(user.id, tenant_id, user.role)
        new_refresh = create_refresh_token(user.id, tenant_id)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh,
            "token_type": "bearer",
        }
