from discord import Interaction
from messages.messages import Messages
from database.db import Database


class Utils():
    async def stopSaveAudio(interaction: Interaction, db: Database, session):
        if (interaction.guild.voice_client.is_playing()):
            await db.updatePlaystate(session, interaction.guild.voice_client.source.playstateId, interaction.guild.voice_client.source.currentTimestamp)
            interaction.guild.voice_client.stop()

    async def connect(interaction: Interaction):
        in_voice = interaction.user.voice
        if in_voice:
            channel = interaction.user.voice.channel
            if interaction.response.type is None:
                await interaction.response.send_message(Messages.ConnectedTo(channel.name))
            else:
                await interaction.edit_original_response(content=Messages.ConnectedTo(channel.name))
                # await interaction.followup.send(Messages.ConnectedTo(channel.name))
            try:
                await channel.connect()
                return
            except Exception as e:
                if interaction.response.type is None:
                    await interaction.response.send_message(Messages.ErrorConnecting)
                    return
                await interaction.edit_original_response(content=Messages.ErrorConnecting)
                return

        if interaction.response.type is None:
            await interaction.response.send_message(Messages.NotConnected)
            return
        await interaction.edit_original_response(content=Messages.NotConnected)

    async def sendResponseMessage(interaction: Interaction, msg: str):
        await interaction.response.send_message(msg)
