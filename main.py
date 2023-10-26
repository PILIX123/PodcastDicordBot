import discord
from vault.vault import Vault
from discord import app_commands
from database.db import Database
from rssreader.reader import Reader

vault = Vault()
db = Database()
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

@tree.command(name="connect",description="connect to voice chat")
async def connect(interaction:discord.Interaction):
    in_voice = interaction.user.voice
    if in_voice:
        channel = interaction.user.voice.channel
        await interaction.response.send_message(f"I connected to {channel.name}")
        try:
            await channel.connect()
        except Exception as e:
            print(f"Error connecting to voice channel: {e}")
            await interaction.response.send_message("Error connecting to voice channel.")
    else:
        await interaction.response.send_message("cant connect no voice")

@tree.command(name="disconnect",description="disconnects from channel")
async def disconnect(interaction:discord.Interaction):
    if(interaction.guild.voice_client is not None):
        if(interaction.guild.voice_client.is_playing()):
            interaction.guild.voice_client.stop()
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("test")
    else:
        await interaction.response.send_message("Not currently connected to a voice channel.")

@tree.command(name="add_podcast")
async def add(interaction:discord.Interaction,url:str):
    await interaction.response.defer(thinking=True)
    success = await db.add(db.asyncSession,interaction.user.id,url)
    if success:
        await interaction.followup.send("Podcast added")
    else:
        await interaction.followup.send("Podcast wasn't added")


@tree.command(name="play")
async def play(interaction:discord.Interaction,name:str):
    await interaction.response.defer(thinking=True)
    title,url = await db.getFromTitle(interaction.user.id,name)
    reader = Reader(url)
    source = discord.FFmpegPCMAudio(reader.getLatestEpisode())
    if interaction.guild.voice_client is not None:
        interaction.guild.voice_client.play(source)
        await interaction.followup.send(f"Playing {title}")
    else:
        await interaction.followup.send("Connect me to a voice channel first")

@client.event
async def on_ready():
    await tree.sync()
    await db.init()

client.run(vault.get_discord_token())