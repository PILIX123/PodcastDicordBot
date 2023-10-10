import discord
from vault.vault import Vault
from discord import app_commands



vault = Vault()
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

@client.event
async def on_ready():
    await tree.sync()

client.run(vault.get_discord_token())