import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from adapters.orm_engines.models import Base
from core.settings import TestSettings


@pytest.fixture(scope="module")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def engine(settings):
    db_url = settings.get_db_url
    engine = create_async_engine(db_url)
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="module")
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="module")
async def session(engine, create):
    async with AsyncSession(engine) as async_session:
        yield async_session


@pytest.fixture(scope="module")
def settings():
    return TestSettings()
