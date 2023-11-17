from discord.ui import View, button, Button
from discord import ButtonStyle, Interaction
from messages.messages import Messages
from enums.enums import ConfirmationEnum


class ValidationView(View):
    clicked: ConfirmationEnum = None

    @button(label="Yes", style=ButtonStyle.success)
    async def yes(self, interaction: Interaction, button: Button):
        await interaction.response.send_message(Messages.YesPlayLastEpisode)
        self.clicked = ConfirmationEnum.Yes
        self.stop()

    @button(label="No", style=ButtonStyle.danger)
    async def no(self, interaction: Interaction, button: Button):
        await interaction.response.send_message(Messages.NoPlayLastEpisode)
        self.clicked = ConfirmationEnum.No
        self.stop()
