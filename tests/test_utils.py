from pytest import mark
from pytest_mock.plugin import MockerFixture
from utils.utils import Utils
from botpackage.messages.messages import Messages
pytest_plugins = ('pytest_asyncio',)


class MockInteraction():
    def __init__(self, is_playing: bool = True, user=None, response=None, followup=None) -> None:
        self.guild = MockGuild(is_playing)
        self.user = user
        self.response = response
        self.followup = followup


class MockGuild():
    def __init__(self, is_playing) -> None:
        self.voice_client = MockVoiceClient(is_playing)


class MockVoiceClient():
    def __init__(self, is_playing: bool) -> None:
        self.source = MockSource()
        self.default = is_playing

    def is_playing(self) -> bool:
        return self.default

    def stop(self):
        return None


class MockSource():
    def __init__(self) -> None:
        self.playstateId = None
        self.currentTimestamp = None


class MockDb():
    async def updatePlaystate(*args, **kwargs):
        return None


@mark.asyncio
async def test_stopSaveAudio() -> None:
    await Utils.stopSaveAudio(MockInteraction(), MockDb(), "")


@mark.asyncio
async def test_stopSaveAudio_NotPlaying() -> None:
    await Utils.stopSaveAudio(MockInteraction(False), MockDb(), "")


@mark.asyncio
async def test_connect_SuccessSendMessage(mocker: MockerFixture):
    followup = mocker.patch("discord.Webhook")
    user = mocker.patch("discord.User")
    user.voice.channel.name = "TEST"
    user.voice.channel.connect = mocker.async_stub()
    response = mocker.patch("discord.InteractionResponse")
    response.type = None
    response.send_message = mocker.async_stub()
    followup.send = mocker.async_stub()
    mock = MockInteraction(user=user, response=response, followup=followup)
    await Utils.connect(mock)
    response.send_message.assert_awaited_with(Messages.ConnectedTo("TEST"))
    followup.send.assert_not_awaited()
    user.voice.channel.connect.assert_awaited()


@mark.asyncio
async def test_connect_SuccessSend(mocker: MockerFixture):
    followup = mocker.patch("discord.Webhook")
    user = mocker.patch("discord.User")
    user.voice.channel.name = "TEST"
    user.voice.channel.connect = mocker.async_stub()
    response = mocker.patch("discord.InteractionResponse")
    response.send_message = mocker.async_stub()
    followup.send = mocker.async_stub()
    mock = MockInteraction(user=user, response=response, followup=followup)
    await Utils.connect(mock)
    response.send_message.assert_not_awaited()
    followup.send.assert_awaited_with(Messages.ConnectedTo("TEST"))
    user.voice.channel.connect.assert_awaited()


@mark.asyncio
async def test_connect_NotConnectSend(mocker: MockerFixture):
    followup = mocker.patch("discord.Webhook")
    user = mocker.patch("discord.User")
    user.voice = None
    response = mocker.patch("discord.InteractionResponse")
    response.send_message = mocker.async_stub()
    followup.send = mocker.async_stub()
    await Utils.connect(MockInteraction(user=user, response=response, followup=followup))
    response.send_message.assert_not_awaited()
    followup.send.assert_awaited_with(Messages.NotConnected)


@mark.asyncio
async def test_connect_NotConnectSendMessage(mocker: MockerFixture):
    followup = mocker.patch("discord.Webhook")
    user = mocker.patch("discord.User")
    user.voice = None
    response = mocker.patch("discord.InteractionResponse")
    response.type = None
    response.send_message = mocker.async_stub()
    await Utils.connect(MockInteraction(user=user, response=response, followup=followup))
    response.send_message.assert_awaited_with(Messages.NotConnected)


@mark.asyncio
async def test_connect_ExceptSendMessage(mocker: MockerFixture):
    followup = mocker.patch("discord.Webhook")
    user = mocker.patch("discord.User")
    response = mocker.patch("discord.InteractionResponse")
    response.type = None
    response.send_message = mocker.async_stub()
    user.voice.channel.name = "TEST"
    user.voice.channel.connect.side_effect = Exception()
    mock = MockInteraction(user=user, response=response, followup=followup)
    await Utils.connect(mock)
    response.send_message.assert_awaited_with(Messages.ErrorConnecting)


@mark.asyncio
async def test_connect_ExceptSend(mocker: MockerFixture):
    followup = mocker.patch("discord.Webhook")
    user = mocker.patch("discord.User")
    response = mocker.patch("discord.InteractionResponse")
    response.type = "a"
    response.send_message = mocker.async_stub()
    user.voice.channel.name = "TEST"
    user.voice.channel.connect.side_effect = Exception()
    followup.send = mocker.async_stub()
    mock = MockInteraction(user=user, response=response, followup=followup)
    await Utils.connect(mock)
    followup.send.assert_awaited_with(Messages.ErrorConnecting)


@mark.asyncio
async def test_sendResponseMessage(mocker: MockerFixture):
    response = mocker.patch("discord.InteractionResponse")
    response.send_message = mocker.async_stub()
    mock = MockInteraction(response=response, is_playing=False)
    await Utils.sendResponseMessage(mock, "TEST")
    response.send_message.assert_awaited_with("TEST")
