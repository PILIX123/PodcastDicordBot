from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Insert
from models.base import Base
from models.user import User
from models.podcasts import Podcast
from rssreader.reader import Reader
from sqlalchemy.dialects.sqlite import insert


class Database():
    async def init(self) -> None:
        engine = create_async_engine(
            "sqlite+aiosqlite:///list.sqlite", echo=True)
        self.asyncSession = async_sessionmaker(engine, expire_on_commit=False)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add(self, sessionmaker: async_sessionmaker[AsyncSession], userId: int, url: str) -> bool:
        async with sessionmaker() as session:
            stmt = select(User).where(User.user_id == userId)
            result = await session.execute(stmt)
            user = result.scalars().one_or_none()
            if (user is not None):
                await session.execute(self.__addPodcast(userId, url))
            else:
                self.__addUserPodcast(session, userId, url)
            try:
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                return False

    async def getFromTitle(self, userId: int, title: str) -> tuple[str, str, int]:
        async with self.asyncSession() as session:
            stmt = select(Podcast) \
                .where(Podcast.userId == userId) \
                .where(Podcast.title == title)

            result = await session.execute(stmt)
            pod = result.scalar()
            return (pod.title, pod.url, pod.latestTimeStamp)

    async def updatePodcast(self, userId: int, timestamp: int, title: str):
        async with self.asyncSession() as session:
            stmt = select(Podcast) \
                .where(Podcast.userId == userId) \
                .where(Podcast.title == title)

            result = await session.execute(stmt)
            pod = result.scalar_one()
            pod.latestTimeStamp = timestamp
            await session.commit()

    def __addUserPodcast(self, session: AsyncSession, userId: int, url: str):
        url = "https://" + \
            url if not url.startswith(
                "https://") or not url.startswith("http://") else url
        reader = Reader(url)

        session.add(
            User(
                user_id=userId,
                podcasts=[
                    Podcast(title=reader.podcast.title,
                            url=url,
                            author=reader.podcast.itunes_author_name)
                ])
        )

    def __addPodcast(self, userId: int, url: str) -> Insert:
        url = "https://" + \
            url if not (url.startswith("https://")
                        or url.startswith("http://")) else url
        reader = Reader(url)
        stmt = insert(Podcast).values(userId=userId,
                                      url=url,
                                      title=reader.podcast.title,
                                      author=reader.podcast.itunes_author_name).on_conflict_do_nothing(index_where=['title'])
        return stmt
