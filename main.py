from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from discord import Intents, Interaction, Client, app_commands
from models.base import Base
from vault.vault import Vault
from database.db import Database
from commands import commands
from enums.enums import CommandEnum

vault = Vault()
intents = Intents.none()
db = Database()
intents.guilds = True
intents.voice_states = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="connect", description="Connects to a voice channel")
async def connect(interaction: Interaction):
    await commands.connect(interaction)


@tree.command(name="stop", description="Stops audio")
async def stop(interaction: Interaction):
    await commands.stop(interaction, db, sessionMaker(engine))


@tree.command(name="disconnect", description="Disconnects from a voice channel")
async def disconnect(interaction: Interaction):
    await commands.disconnect(interaction, db, sessionMaker(engine))


@tree.command(name="subscribe", description="Subscribes the user to the given RSS feed")
@app_commands.describe(url="URL pointing to the rss feed")
async def subscribe(interaction: Interaction, url: str):
    await commands.subscribe(interaction, url, db, sessionMaker(engine))


@tree.command(name="list", description="List all podcast you are subscribed to")
async def listing(interaction: Interaction):
    await commands.list(interaction, db, sessionMaker(engine))


@tree.command(name="unsubscribe", description="Unsubscribes the user from the RSS feed")
@app_commands.describe(name="**RESPECT CAPITALIZATION** Name of the podcast")
async def unsubscribe(interaction: Interaction, name: str):
    await commands.unsubscribe(interaction, name, db, sessionMaker(engine))


@tree.command(name="play", description="Plays the podcast with the given name.")
@app_commands.describe(name="**RESPECT CAPITALIZATION** Name of the podcast",
                       episode_number="The number of the episode wanted",
                       timestamp="**`HH:MM:SS` format only** Timestamp to start the episode at")
async def play(interaction: Interaction, name: str, episode_number: None | int = None, timestamp: None | str = None):
    await commands.play(interaction, name, episode_number, timestamp, db, sessionMaker(engine))


@tree.command(name="help", description="Explains the use of the commands")
@app_commands.describe(command="Name of the command you want help with")
async def help(interaction: Interaction, command: CommandEnum):
    await commands.help(interaction, command)


async def getEngine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///list.sqlite", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


def sessionMaker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@client.event
async def on_ready():
    await tree.sync()
    global engine
    engine = await getEngine()

if __name__ == "__main__":
    client.run(vault.get_discord_token())
