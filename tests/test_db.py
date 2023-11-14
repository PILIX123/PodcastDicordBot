from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from pytest import mark
from botmodules.models.base import Base
from botmodules.models.user import User
from botmodules.models.episode import Episode
from botmodules.models.subscription import Subscriptions
from botmodules.models.playstate import Playstate
from botmodules.models.podcasts import Podcast
from botmodules.database.db import Database


async def setupGet(obj):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = async_session()
    if type(obj) == list:
        session.add_all(obj)
    else:
        session.add(obj)
    await session.commit()
    await session.aclose()
    return async_session


async def setupAdd():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_session


@mark.asyncio
async def test_getUser():
    # Setup
    valid_user = User(id=1, lastPodcastId=2, lastEpisodeId=3)

    async_session = await setupGet(valid_user)
    # Exercise
    db = Database()
    user = await db.getUser(async_session, 1)

    # Verify
    assert user.id == 1
    assert user.lastEpisodeId == 3
    assert user.lastPodcastId == 2


@mark.asyncio
async def test_addUser():
    async_session = await setupAdd()
    db = Database()
    u = await db.addUser(async_session, 1)

    assert u.lastEpisodeId == None
    assert u.lastPodcastId == None
    assert u.id == 1


@mark.asyncio
async def test_updateUser():
    user = User(id=1, lastPodcastId=2, lastEpisodeId=3)
    async_session = await setupGet(user)

    user.lastPodcastId = 3
    db = Database()
    await db.updateUser(async_session, user)
    async with async_session() as session:
        u = await session.get(User, user.id)
        assert u.id == 1
        assert u.lastEpisodeId == 3
        assert u.lastPodcastId == 3


@mark.asyncio
async def test_getPodcast():
    podcast = Podcast(id=1, title="TITLE_TEST", url="http://test.test")
    async_session = await setupGet(podcast)

    db = Database()
    p = await db.getPodcast(async_session, 1)
    assert p.id == 1
    assert p.title == "TITLE_TEST"
    assert p.url == "http://test.test"


@mark.asyncio
async def test_getPodcastFromTitle():
    podcast = Podcast(id=1, title="TITLE_TEST", url="http://test.test")
    async_session = await setupGet(podcast)

    db = Database()
    p = await db.getPodcastFromTitle(async_session, "TITLE_TEST")
    assert p.id == 1
    assert p.url == "http://test.test"


@mark.asyncio
async def test_getPodcastBulk():
    podcast1 = Podcast(id=1, title="TITLE_TEST", url="http://test.test")
    podcast2 = Podcast(id=2, title="TITLE_TEST2", url="http://test.test2")
    async_session = await setupGet([podcast1, podcast2])
    db = Database()
    lp = await db.getPodcastBulk(async_session, [1, 2])
    p1 = lp[0]
    p2 = lp[1]
    assert p1.id == podcast1.id
    assert p1.title == podcast1.title
    assert p1.url == podcast1.url
    assert p2.id == podcast2.id
    assert p2.title == podcast2.title
    assert p2.url == podcast2.url


@mark.asyncio
async def test_addPodcast():
    async_session = await setupAdd()
    db = Database()
    podcast = Podcast(title="TITLE_TEST", url="http://test.test")
    p = await db.addPodcast(async_session, podcast)
    assert p.id is not None
    assert p.title == "TITLE_TEST"
    assert p.url == "http://test.test"


@mark.asyncio
async def test_getSubscription():
    user = User(id=1, lastPodcastId=2, lastEpisodeId=3)
    podcast = Podcast(id=1, title="TITLE_TEST", url="http://test.test")
    subscription = Subscriptions(id=1, userId=1, podcastId=1)

    async_session = await setupGet([user, podcast, subscription])
    db = Database()
    s = await db.getSubscription(async_session, 1)
    assert s.id == 1
    assert s.userId == 1
    assert s.podcastId == 1


@mark.asyncio
async def test_getSubscriptionUser():
    user = User(id=1, lastPodcastId=2, lastEpisodeId=3)
    podcast = Podcast(id=1, title="TITLE_TEST", url="http://test.test")
    subscription = Subscriptions(id=1, userId=1, podcastId=1)

    async_session = await setupGet([user, podcast, subscription])
    db = Database()
    s = await db.getSubscriptionUser(async_session, 1, 1)
    assert s.id == 1


@mark.asyncio
async def test_addSubscription():
    async_session = await setupAdd()
    db = Database()
    subscription = Subscriptions(userId=1, podcastId=1)
    s = await db.addSubscription(async_session, subscription)
    assert s.id is not None
    assert s.podcastId == 1
    assert s.userId == 1


@mark.asyncio
async def test_deleteSubscription():
    user = User(id=1, lastPodcastId=2, lastEpisodeId=3)
    podcast = Podcast(id=1, title="TITLE_TEST", url="http://test.test")
    subscription = Subscriptions(id=1, userId=1, podcastId=1)

    async_session = await setupGet([user, podcast, subscription])

    db = Database()
    await db.deleteSubscription(async_session, subscription)
    async with async_session() as session:
        s = await session.get(Subscriptions, 1)
        assert s is None


@mark.asyncio
async def test_getEpisode():
    episode = Episode(id=1, podcastId=2, episodeNumber=3, title="TEST_TITLE")

    async_session = await setupGet(episode)
    db = Database()
    e = await db.getEpisode(async_session, 1)
    assert e.id == 1
    assert e.podcastId == 2
    assert e.episodeNumber == 3
    assert e.title == "TEST_TITLE"


@mark.asyncio
async def test_getEpisodePodcastNumber():
    episode = Episode(id=1, podcastId=2, episodeNumber=3, title="TEST_TITLE")

    async_session = await setupGet(episode)
    db = Database()
    e = await db.getEpisodePodcastNumber(async_session, 2, 3)
    assert e.id == 1
    assert e.podcastId == 2
    assert e.episodeNumber == 3
    assert e.title == "TEST_TITLE"


@mark.asyncio
async def test_addEpisode():
    async_session = await setupAdd()
    episode = Episode(podcastId=2, episodeNumber=3, title="TEST_TITLE")
    db = Database()
    e = await db.addEpisode(async_session, episode)
    assert e.id is not None
    assert e.podcastId == 2
    assert e.episodeNumber == 3
    assert e.title == "TEST_TITLE"


@mark.asyncio
async def test_getPlaystate():
    playstate = Playstate(id=1, userId=2, episodeId=3, timestamp=123)
    async_session = await setupGet(playstate)

    db = Database()
    p = await db.getPlaystate(async_session, 1)
    assert p.id == 1
    assert p.userId == 2
    assert p.episodeId == 3
    assert p.timestamp == 123


@mark.asyncio
async def test_getPlaystateUserEpisode():
    playstate = Playstate(id=1, userId=2, episodeId=3, timestamp=123)
    async_session = await setupGet(playstate)

    db = Database()
    p = await db.getPlaystateUserEpisode(async_session, 2, 3)
    assert p.id == 1
    assert p.timestamp == 123


@mark.asyncio
async def test_addPlaystate():
    async_session = await setupAdd()
    playstate = Playstate(userId=2, episodeId=3, timestamp=123)

    db = Database()
    p = await db.addPlaystate(async_session, playstate)
    assert p.id is not None
    assert p.userId == 2
    assert p.episodeId == 3
    assert p.timestamp == 123


@mark.asyncio
async def test_updatePlaystate():
    playstate = Playstate(id=1, userId=2, episodeId=3, timestamp=123)
    async_session = await setupGet(playstate)

    db = Database()
    p = await db.updatePlaystate(async_session, 1, 1422)
    assert p.userId == 2
    assert p.episodeId == 3
    assert p.timestamp == 1422
