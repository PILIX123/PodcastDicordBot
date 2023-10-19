from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from model.list import Base
class Database():
    async def init(self) -> None:
        engine = create_async_engine("sqlite+aiosqlite:///list.sqlite")
        session = async_sessionmaker(bind=engine, expire_on_commit=False)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
