import asyncio
import uuid
from collections.abc import AsyncGenerator
from decimal import Decimal

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.infrastructure.database.base import Base
from app.infrastructure.database.models import *  # noqa: F401,F403
from app.infrastructure.database.session import get_db
from app.main import app


# Use a test database
TEST_DATABASE_URL = settings.DATABASE_URL


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


# --- Helper fixtures ---

@pytest_asyncio.fixture
async def sample_tenant(db_session: AsyncSession):
    from app.infrastructure.database.models.tenant import Tenant

    tenant = Tenant(
        id=uuid.uuid4(),
        name="Test Tenant",
        slug="test-tenant",
        is_active=True,
    )
    db_session.add(tenant)
    await db_session.flush()
    return tenant


@pytest_asyncio.fixture
async def sample_user(db_session: AsyncSession, sample_tenant):
    from app.infrastructure.database.models.user import User
    from app.infrastructure.auth.jwt_provider import hash_password

    user = User(
        id=uuid.uuid4(),
        tenant_id=sample_tenant.id,
        email="test@example.com",
        hashed_password=hash_password("testpass123"),
        full_name="Test User",
        role="user",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest_asyncio.fixture
async def auth_headers(sample_user, sample_tenant):
    from app.infrastructure.auth.jwt_provider import create_access_token

    token = create_access_token(sample_user.id, sample_tenant.id, sample_user.role)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession, sample_tenant):
    from app.infrastructure.database.models.user import User
    from app.infrastructure.auth.jwt_provider import hash_password

    user = User(
        id=uuid.uuid4(),
        tenant_id=sample_tenant.id,
        email="admin@example.com",
        hashed_password=hash_password("adminpass123"),
        full_name="Admin User",
        role="admin",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest_asyncio.fixture
async def admin_headers(admin_user, sample_tenant):
    from app.infrastructure.auth.jwt_provider import create_access_token

    token = create_access_token(admin_user.id, sample_tenant.id, admin_user.role)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def sample_fiscal_year(db_session: AsyncSession):
    from app.infrastructure.database.models.fiscal_year import FiscalYear

    fy = FiscalYear(
        id=uuid.uuid4(),
        year=2025,
        status="active",
        uvt_value=Decimal("49641"),
    )
    db_session.add(fy)
    await db_session.flush()
    return fy
