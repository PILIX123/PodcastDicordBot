import discord
from vault.vault import Vault
from discord import app_commands
from database.db import Database
from rssreader.reader import Reader
from utils.customAudio import CustomAudio
from utils.utils import Utils

vault = Vault()
db = Database()
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

@tree.command(name="connect",description="connect to voice chat")
async def connect(interaction:discord.Interaction):
    await Utils.connect(interaction)

@tree.command(name="stop")
async def stop(interaction:discord.Interaction):
    await interaction.response.defer()
    await Utils.stopSaveAudio(interaction,db)
    await interaction.followup.send("audio stopped and timestamp saved")

@tree.command(name="disconnect",description="disconnects from channel")
async def disconnect(interaction:discord.Interaction):
    await interaction.response.defer()
    if(interaction.guild.voice_client is not None):
        await Utils.stopSaveAudio(interaction,db)
        await interaction.guild.voice_client.disconnect()
        await interaction.followup.send("Disconnected")
    else:
        await interaction.response.send("Not currently connected to a voice channel.")

@tree.command(name="add_podcast")
async def add(interaction:discord.Interaction,url:str):
    await interaction.response.defer(thinking=True)
    success = await db.add(db.asyncSession,interaction.user.id,url)
    if success:
        await interaction.followup.send("Podcast added")
    else:
        await interaction.followup.send("Podcast wasn't added")


@tree.command(name="play")
async def play(interaction:discord.Interaction,name:str,episode_number:None|int=None,timestamp:None|str=None):
    if interaction.guild.voice_client is None:
        await Utils.connect(interaction)
    title,url,lastTimeStamp = await db.getFromTitle(interaction.user.id,name)
    reader = Reader(url)
    num = len(reader.podcast.items)-episode_number if episode_number is not None else 0
    options = (None if lastTimeStamp is None else f"-ss {lastTimeStamp}ms") if timestamp is None else f"-ss {timestamp}"
    source = CustomAudio(reader.getEpisode(num),title,before_options=options)
    interaction.guild.voice_client.play(source)
    await interaction.followup.send(f"Playing {title}")        

@client.event
async def on_ready():
    await tree.sync()
    await db.init()

client.run(vault.get_discord_token())