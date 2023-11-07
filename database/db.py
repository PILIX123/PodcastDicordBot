from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from models.user import User
from models.episode import Episode
from models.podcasts import Podcast
from models.subscription import Subscriptions
from models.playstate import Playstate
from models.base import Base


class Database():
    async def getUser(self, async_session: async_sessionmaker[AsyncSession], userId: int) -> User | None:
        async with async_session() as session:
            stmt = select(User).where(User.id == userId)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is not None:
                await user.awaitable_attrs.subscriptions
                await user.awaitable_attrs.playstates
            return user

    async def addUser(self, async_session: async_sessionmaker[AsyncSession], userId: int) -> User:
        async with async_session() as session:
            async with session.begin():
                u = User(id=userId)
                session.add(u)
                await session.flush()
                return u

    async def updateUser(self, async_session: async_sessionmaker[AsyncSession], user: User) -> None:
        async with async_session() as session:
            async with session.begin():
                session.add(user)
                await session.commit()

    async def getPodcast(self, async_session: async_sessionmaker[AsyncSession], podcastId: int) -> Podcast | None:
        async with async_session() as session:
            stmt = select(Podcast).where(Podcast.id == podcastId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getPodcastFromTitle(self, async_session, title: str) -> Podcast | None:
        async with async_session() as session:
            stmt = select(Podcast).where(Podcast.title == title)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getPodcastBulk(self, async_session: async_sessionmaker[AsyncSession], ids: list[int]) -> list[Podcast]:
        async with async_session() as session:
            stmt = select(Podcast).filter(Podcast.id.in_(ids))
            result = await session.execute(stmt)
            return result.scalars().all()

    async def addPodcast(self, async_session: async_sessionmaker[AsyncSession], podcast: Podcast) -> Podcast:
        async with async_session() as session:
            async with session.begin():
                p = podcast
                session.add(p)
                await session.flush()
                return p

    async def getSubscriptionUser(self, async_session, userId: int, podcastId: int) -> Subscriptions | None:
        async with async_session() as session:
            stmt = select(Subscriptions).where(Subscriptions.userId == userId).where(
                Subscriptions.podcastId == podcastId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getSubscription(self, async_session: async_sessionmaker[AsyncSession], subscriptionId: int) -> Subscriptions:
        async with async_session() as session:
            stmt = select(Subscriptions).where(
                Subscriptions.id == subscriptionId)
            result = await session.execute(stmt)
            return result.scalar_one()

    async def addSubscription(self, async_session: async_sessionmaker[AsyncSession], subscription: Subscriptions) -> Subscriptions:
        async with async_session() as session:
            async with session.begin():
                s = subscription
                session.add(s)
                await session.flush()
                return s

    async def deleteSubscription(self, async_session: async_sessionmaker[AsyncSession], subscription: Subscriptions):
        async with async_session() as session:
            await session.delete(subscription)
            await session.commit()

    async def getEpisode(self, async_session, episodeId: int) -> Episode | None:
        async with async_session() as session:
            stmt = select(Episode).where(Episode.id == episodeId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getEpisodePodcastNumber(self, async_session: async_sessionmaker[AsyncSession], podcastId: int, episodeNumber: int) -> Episode | None:
        async with async_session() as session:
            stmt = select(Episode).where(Episode.podcastId == podcastId).where(
                Episode.episodeNumber == episodeNumber)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def addEpisode(self, async_session: async_sessionmaker[AsyncSession], episode: Episode) -> Episode:
        async with async_session() as session:
            async with session.begin():
                e = episode
                session.add(e)
                await session.flush()
                return e

    async def getPlaystate(self, async_session: async_sessionmaker[AsyncSession], playstateId: int) -> Playstate | None:
        async with async_session() as session:
            stmt = select(Playstate).where(Playstate.id == playstateId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getPlaystateUserEpisode(self, async_session: async_sessionmaker[AsyncSession], userId: int, episodeId: int) -> Playstate | None:
        async with async_session() as session:
            stmt = select(Playstate).where(Playstate.userId == userId).where(
                Playstate.episodeId == episodeId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def addPlaystate(self, async_session: async_sessionmaker[AsyncSession], playstate: Playstate) -> Playstate:
        async with async_session() as session:
            async with session.begin():
                p = playstate
                session.add(p)
                await session.flush()
                return p

    async def updatePlaystate(self, async_session: async_sessionmaker[AsyncSession], playstateId: int, timestamp: int) -> Playstate:
        async with async_session() as session:
            stmt = select(Playstate).where(Playstate.id == playstateId)
            result = await session.execute(stmt)
            playstate = result.scalar_one()
            playstate.timestamp = timestamp
            await session.commit()
            return playstate
