from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest
from models.base import Base
from models.user import User
from sqlalchemy import select
from models.episode import Episode
from models.subscription import Subscriptions
from models.playstate import Playstate
from models.podcasts import Podcast
from database.db import Database


async def setupGet(obj):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = async_session()
    session.add(obj)
    await session.commit()
    return async_session, session


async def setupAdd():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_session, async_session()


@pytest.mark.asyncio
async def test_get_user():
    # Setup
    valid_user = User(id=1, lastPodcastId=2, lastEpisodeId=3)

    async_session, session = await setupGet(valid_user)
    # Exercise
    db = Database()
    user = await db.getUser(async_session, 1)

    # Verify
    assert user.id == 1
    assert user.lastEpisodeId == 3
    assert user.lastPodcastId == 2

    # Teardown
    await session.rollback()
    await session.close()


@pytest.mark.asyncio
async def test_addUser():
    async_session, session = await setupAdd()
    db = Database()
    u = await db.addUser(async_session, 1)

    assert u.lastEpisodeId == None
    assert u.lastPodcastId == None
    assert u.id == 1
    session.close()
