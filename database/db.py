from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import lazyload
from models.base import Base
from models.user import User
from models.episode import Episode
from models.podcasts import Podcast
from models.subscription import Subscriptions
from models.playstate import Playstate


class Database():
    async def init(self) -> None:
        engine = create_async_engine(
            "sqlite+aiosqlite:///list.sqlite", echo=True)
        self.asyncSession = async_sessionmaker(engine, expire_on_commit=False)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def getUser(self, userId: int) -> User | None:
        async with self.asyncSession() as session:
            stmt = select(User).where(User.id == userId)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is not None:
                await user.awaitable_attrs.subscriptions
                await user.awaitable_attrs.playstates
            return user

    async def addUser(self, userId: int) -> User:
        async with self.asyncSession() as session:
            async with session.begin():
                u = User(id=userId)
                session.add(u)
                await session.flush()
                return u

    async def getPodcast(self, podcastId: int) -> Podcast | None:
        async with self.asyncSession() as session:
            stmt = select(Podcast).where(Podcast.id == podcastId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getPodcastFromTitle(self, title: str) -> Podcast | None:
        async with self.asyncSession() as session:
            stmt = select(Podcast).where(Podcast.title == title)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getPodcastBulk(self, ids: list[int]) -> list[Podcast]:
        async with self.asyncSession() as session:
            stmt = select(Podcast).filter(Podcast.id.in_(ids))
            result = await session.execute(stmt)
            return result.scalars()

    async def addPodcast(self, url: str, title: str) -> Podcast:
        async with self.asyncSession() as session:
            async with session.begin():
                p = Podcast(url=url, title=title)
                session.add(p)
                await session.flush()
                return p

    async def getSubscriptionUser(self, userId: int, podcastId: int) -> Subscriptions | None:
        async with self.asyncSession() as session:
            stmt = select(Subscriptions).where(Subscriptions.userId == userId).where(
                Subscriptions.podcastId == podcastId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getSubscription(self, subscriptionId: int) -> Subscriptions:
        async with self.asyncSession() as session:
            stmt = select(Subscriptions).where(
                Subscriptions.id == subscriptionId)
            result = await session.execute(stmt)
            return result.scalar_one()

    async def addSubscription(self, userId: int, podcastId: int) -> Subscriptions:
        async with self.asyncSession() as session:
            async with session.begin():
                s = Subscriptions(userId=userId, podcastId=podcastId)
                session.add(s)
                await session.flush()
                return s

    async def deleteSubscription(self, subscription: Subscriptions):
        async with self.asyncSession() as session:
            await session.delete(subscription)
            await session.commit()

    async def getEpisode(self, episodeId: int) -> Episode | None:
        async with self.asyncSession() as session:
            stmt = select(Episode).where(Episode.id == episodeId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getEpisodePodcastNumber(self, podcastId: int, episodeNumber: int) -> Episode | None:
        async with self.asyncSession() as session:
            stmt = select(Episode).where(Episode.podcastId == podcastId).where(
                Episode.episodeNumber == episodeNumber)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def addEpisode(self, episodeNumber: int, podcastId: int) -> Episode:
        async with self.asyncSession() as session:
            async with session.begin():
                e = Episode(podcastId=podcastId, episodeNumber=episodeNumber)
                session.add(e)
                await session.flush()
                return e

    async def getPlaystate(self, playstateId: int) -> Playstate | None:
        async with self.asyncSession() as session:
            stmt = select(Playstate).where(Playstate.id == playstateId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getPlaystateUserEpisode(self, userId: int, episodeId: int) -> Playstate | None:
        async with self.asyncSession() as session:
            stmt = select(Playstate).where(Playstate.userId == userId).where(
                Playstate.episodeId == episodeId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def addPlaystate(self, episodeId: int, timestamp: int, userId: int) -> Playstate:
        async with self.asyncSession() as session:
            async with session.begin():
                p = Playstate(userId=userId, episodeId=episodeId,
                              timestamp=timestamp)
                session.add(p)
                await session.flush()
                return p

    async def updatePlaystate(self, playstateId: int, timestamp: int) -> Playstate:
        async with self.asyncSession() as session:
            stmt = select(Playstate).where(Playstate.id == playstateId)
            result = await session.execute(stmt)
            playstate = result.scalar_one()
            playstate.timestamp = timestamp
            await session.commit()
            return playstate
