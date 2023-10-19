import discord
from vault.vault import Vault
from discord import app_commands
from database.db import Database
import asqlite
from sqlalchemy.ext.asyncio import create_async_engine

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

@tree.command(name="testdb",description="add podcast url to subscription")
async def add(interaction:discord.Interaction):

    async with asqlite.connect("list.sqlite") as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''CREATE TABLE list
                                 (user, url)''')
            await cursor.execute("INSERT INTO list VALUES ('13245','TT')")
            
            await conn.commit()

@tree.command(name="readdb")
async def read(interaction:discord.Interaction):
    async with asqlite.connect("list.sqlite") as conn:
        async with conn.cursor() as cursor:
            res = await cursor.execute("SELECT url FROM list")
            row = await res.fetchall()
            await interaction.response.send_message(row[0]['url'])

@client.event
async def on_ready():
    await tree.sync()
    await db.init()

client.run(vault.get_discord_token())