from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from models.base import Base
from models.user import User
from models.episode import Episode
from models.podcasts import Podcast
from models.subscription import Subcriptions
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
            return result.scalar_one_or_none()

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

    async def addPodcast(self, url: str, title: str) -> Podcast:
        async with self.asyncSession() as session:
            async with session.begin():
                p = Podcast(url=url, title=title)
                session.add(p)
                await session.flush()
                return p

    async def getSubscriptionUser(self, userId: int, podcastId: int) -> Subcriptions | None:
        async with self.asyncSession() as session:
            stmt = select(Subcriptions).where(Subcriptions.userId == userId).where(
                Subcriptions.podcastId == podcastId)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def getSubscription(self, subscriptionId: int) -> Subcriptions:
        async with self.asyncSession() as session:
            stmt = select(Subcriptions).where(
                Subcriptions.id == subscriptionId)
            result = await session.execute(stmt)
            return result.scalar_one()

    async def addSubscription(self, userId: int, podcastId: int) -> Subcriptions:
        async with self.asyncSession() as session:
            async with session.begin():
                s = Subcriptions(userId=userId, podcastId=podcastId)
                session.add(s)
                await session.flush()
                return s

    async def deleteSubscription(self, subscription: Subcriptions):
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

    # async def add(self, sessionmaker: async_sessionmaker[AsyncSession], userId: int, url: str) -> bool:
    #     async with sessionmaker() as session:
    #         stmt = select(User).where(User.user_id == userId)
    #         result = await session.execute(stmt)
    #         user = result.scalars().one_or_none()
    #         if (user is not None):
    #             await session.execute(self.__addPodcast(userId, url))
    #         else:
    #             self.__addUserPodcast(session, userId, url)
    #         try:
    #             await session.commit()
    #             return True
    #         except IntegrityError:
    #             await session.rollback()
    #             return False

    # async def getFromTitle(self, userId: int, title: str) -> tuple[str, str, int]:
    #     async with self.asyncSession() as session:
    #         stmt = select(Podcast) \
    #             .where(Podcast.userId == userId) \
    #             .where(Podcast.title == title)

    #         result = await session.execute(stmt)
    #         pod = result.scalar()
    #         return (pod.title, pod.url, pod.lastEpisode)

    # async def updatePodcast(self, userId: int, timestamp: int, title: str):
    #     async with self.asyncSession() as session:
    #         stmt = select(Podcast) \
    #             .where(Podcast.userId == userId) \
    #             .where(Podcast.title == title)

    #         result = await session.execute(stmt)
    #         pod = result.scalar_one()
    #         pod.latestTimeStamp = timestamp
    #         await session.commit()

    # async def createEpisode(self, userId: int, title: str, timestamp: int):
    #     async with self.asyncSession() as session:
    #         stmt = select(Podcast) \
    #             .where(Podcast.userId == userId) \
    #             .where(Podcast.title == title)

    #         result = await session.execute(stmt)
    #         pod = result.scalar_one()

    #         session.add(Episode(podcastId=pod.id,
    #                     episodeNumber=1, timeStamp=timestamp))

    # async def updateEpisode(self, userId: int, title: str, episodeNum: int, timestamp: int):
    #     async with self.asyncSession() as session:
    #         stmt = select(Podcast)\
    #             .where(Podcast.title == title).where(Podcast.userId == userId)\
    #             # .where(Episode.episodeNumber == episodeNum)

    #         result = await session.execute(stmt)
    #         tt = result.scalars().all()
    #         test = result.scalar()
    #         0

    # def __addUserPodcast(self, session: AsyncSession, userId: int, url: str):
    #     url = "https://" + \
    #         url if not \
    #         (url.startswith("https://") or url.startswith("http://")) \
    #         else url
    #     reader = Reader(url)

    #     session.add(
    #         User(
    #             user_id=userId,
    #             podcasts=[
    #                 Podcast(title=reader.podcast.title,
    #                         url=url)
    #             ])
    #     )

    # def __addPodcast(self, userId: int, url: str) -> Insert:
    #     url = "https://" + \
    #         url if not \
    #         (url.startswith("https://") or url.startswith("http://")) \
    #         else url
    #     reader = Reader(url)
    #     stmt = insert(Podcast).values(userId=userId,
    #                                   url=url,
    #                                   title=reader.podcast.title
    #                                   ).on_conflict_do_nothing(index_where=['title'])
    #     return stmt
