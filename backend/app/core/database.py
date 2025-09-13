from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

DATABASE_URL = (
    str(settings.DATABASE_URL).replace("postgresql://", "postgresql+asyncpg://")
    if settings.DATABASE_URL
    else None
)

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. Please set it in the environment or .env file"
    )

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session