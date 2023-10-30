from database.db import Database
from discord import Interaction


class Utils():
    async def stopSaveAudio(interaction: Interaction, db: Database):
        if (interaction.guild.voice_client.is_playing()):
            await db.updateEpisode(
                interaction.user.id,
                interaction.guild.voice_client.source.name,
                interaction.guild.voice_client.source.episode,
                interaction.guild.voice_client.source.currentTimestamp)
            interaction.guild.voice_client.stop()

    async def connect(interaction: Interaction):
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
            await interaction.response.send_message("Cannot connect you are not connected to a voice channel")
