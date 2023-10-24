from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, create_async_pool_from_url
from sqlalchemy import select, insert
from model.list import Base, PodcastList
class Database():
    async def init(self) -> None:
        engine = create_async_engine("sqlite+aiosqlite:///list.sqlite",echo=True)
        self.asyncSession = async_sessionmaker(engine,expire_on_commit=False)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def add(self,sessionmaker:async_sessionmaker[AsyncSession],userId:int,url:str) -> None:
        async with sessionmaker() as session:
            stmt = select(PodcastList).where(PodcastList.user_id==userId)
            result = await session.execute(stmt)
            podcast = result.scalars().one_or_none()
            if(podcast is not None):
                urls = set(podcast.urls.split("||"))
                urls.add(url)
                podcast.urls = "||".join(urls)
            else:
                insertStmt = insert(PodcastList).values(user_id=userId,urls=url)
                await session.execute(insertStmt)
            await session.commit()
