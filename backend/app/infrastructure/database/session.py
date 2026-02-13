from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings


def _fix_database_url(url: str) -> str:
    """Convert sslmode to ssl for asyncpg compatibility."""
    return url.replace("sslmode=", "ssl=").replace("channel_binding=require", "").rstrip("&?")


engine = create_async_engine(
    _fix_database_url(settings.DATABASE_URL),
    echo=settings.DATABASE_ECHO,
    pool_size=20,
    max_overflow=10,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
