import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from adapters.orm_engines.models import Base


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def engine():
    db_url = "postgresql+asyncpg://root:abfkrf2003@localhost:5432/TestUserManagement"
    engine = create_async_engine(db_url)
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def session(engine, create):
    async with AsyncSession(engine) as async_session:
        yield async_session
