from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from alembic.config import Config
from alembic import command
from httpx2 import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings
from app.dependency import get_session
from main import app

test_settings = settings
test_settings.DB_NAME = "test_delivery"

test_engine = create_async_engine(
    test_settings.database_url,
)

test_session_factory = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_session_factory() as session:
        yield session


@pytest_asyncio.fixture()
async def client(clean_database):
    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        yield client
    app.dependency_overrides.pop(get_session, None)


@pytest.fixture(scope="session")
def database_schema():
    config = Config("alembic.ini")
    config.attributes["database_url"] = test_settings.database_url
    command.upgrade(config, "head")


@pytest_asyncio.fixture
async def clean_database(database_schema):
    async with test_session_factory() as session:
        await session.execute(text("TRUNCATE TABLE parcels;"))
        await session.commit()
