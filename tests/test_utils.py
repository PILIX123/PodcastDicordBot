from utils.utils import Utils
from pytest import mark
from pytest_mock.plugin import MockerFixture
from messages.messages import Messages
pytest_plugins = ('pytest_asyncio',)


class MockInteraction():
    def __init__(self, is_playing: bool = True, type: str = None, user=None, response=None, followup=None) -> None:
        self.guild = MockGuild(is_playing)
        self.type = type
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
    await Utils.stopSaveAudio(MockInteraction(), MockDb())


@mark.asyncio
async def test_stopSaveAudio_NotPlaying() -> None:
    await Utils.stopSaveAudio(MockInteraction(False), MockDb())


@mark.asyncio
async def test_connect(mocker: MockerFixture):
    followup = mocker.patch("discord.Webhook")
    user = mocker.patch("discord.User")
    user.voice = None
    response = mocker.patch("discord.InteractionResponse")
    response.send_message = mocker.async_stub()
    await Utils.connect(MockInteraction(user=user, response=response, followup=followup))
    response.send_message.assert_awaited_with(Messages.NotConnected)
