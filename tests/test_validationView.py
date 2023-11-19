from pytest import mark
from pytest_mock.plugin import MockerFixture
from customViews.validationView import ValidationView
from enums.enums import ConfirmationEnum
from messages.messages import Messages


@mark.asyncio
async def test_yes(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.send_message = mocker.async_stub()

    interaction = mocker.MagicMock()
    interaction.response = response
    vv = ValidationView()
    await vv.yes.callback(interaction=interaction)
    assert (vv.clicked is ConfirmationEnum.Yes)
    response.send_message.assert_awaited_once_with(
        Messages.YesPlayLastEpisode, ephemeral=True)


@mark.asyncio
async def test_no(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.send_message = mocker.async_stub()

    interaction = mocker.MagicMock()
    interaction.response = response
    vv = ValidationView()
    await vv.no.callback(interaction=interaction)
    assert (vv.clicked is ConfirmationEnum.No)
    response.send_message.assert_awaited_once_with(
        Messages.NoPlayLastEpisode, ephemeral=True)
