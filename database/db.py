import asqlite

class Database():
    async def init(self) -> None:
        #asqlite.create_pool("list.sqlite")
        async with asqlite.connect("list.sqlite") as conn:
            async with conn.cursor() as cursor:
                if((await (await cursor.execute("SELECT name FROM sqlite_master WHERE name='list'")).fetchone())["name"] is not None):
                    return
                await cursor.execute('''CREATE TABLE list
                                 (user, url)''')


