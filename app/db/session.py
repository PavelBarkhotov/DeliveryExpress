from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings


engine = create_async_engine(
    settings.database_url,
)

session_factory = async_sessionmaker(engine)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session





