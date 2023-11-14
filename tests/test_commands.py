from pytest import mark
from pytest_mock.plugin import MockerFixture
from commands import commands
from messages.messages import Messages
from messages.descriptions import Description
from enums.enums import CommandEnum
pytest_plugins = ('pytest_asyncio',)


@mark.asyncio
async def test_connect(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.connect = mocker.async_stub()
    await commands.connect("test")
    utils.connect.assert_called_once_with("test")


@mark.asyncio
async def test_stop_connected(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.stopSaveAudio = mocker.async_stub()
    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    guild = mocker.MagicMock()
    guild.voice_client = "t"

    interaction = mocker.MagicMock()
    interaction.followup = followup
    interaction.response = response
    interaction.guild = guild
    await commands.stop(interaction, "TEST_DB", "TEST_SESSION")
    utils.stopSaveAudio.assert_awaited_once_with(
        interaction, "TEST_DB", "TEST_SESSION")
    followup.send.assert_awaited_with(Messages.AudioSaved)


@mark.asyncio
async def test_stop_notConnected(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.stopSaveAudio = mocker.async_stub()
    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    guild = mocker.MagicMock()
    guild.voice_client = None

    interaction = mocker.MagicMock()
    interaction.followup = followup
    interaction.response = response
    interaction.guild = guild
    await commands.stop(interaction, "TEST_DB", "TEST_SESSION")
    utils.stopSaveAudio.assert_not_awaited()
    followup.send.assert_awaited_with(Messages.NotConnected)


@mark.asyncio
async def test_disconnect_Connected(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.stopSaveAudio = mocker.async_stub()
    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    voice_client = mocker.MagicMock()
    voice_client.disconnect = mocker.async_stub()

    guild = mocker.MagicMock()
    guild.voice_client = voice_client

    interaction = mocker.MagicMock()
    interaction.followup = followup
    interaction.response = response
    interaction.guild = guild

    await commands.disconnect(interaction, "TEST_DB", "TEST_SESSION")
    utils.stopSaveAudio.assert_awaited_once_with(
        interaction, "TEST_DB", "TEST_SESSION")
    followup.send.assert_awaited_with(Messages.Disconnected)


@mark.asyncio
async def test_disconnect_notConnected(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.stopSaveAudio = mocker.async_stub()
    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    guild = mocker.async_stub()
    guild.voice_client = None

    interaction = mocker.async_stub()
    interaction.followup = followup
    interaction.response = response
    interaction.guild = guild
    await commands.disconnect(interaction, "TEST_DB", "TEST_SESSION")
    utils.stopSaveAudio.assert_not_awaited()
    followup.send.assert_awaited_with(Messages.NotConnected)


def setupMocks(mocker):
    get = mocker.patch("commands.commands.get")

    reader = mocker.patch("commands.commands.Reader")
    podcastMock = mocker.patch("commands.commands.Podcast")
    podcastDto = mocker.patch("commands.commands.PodcastDto")
    podcastDto.return_value = "TEST_PODCAST"
    subscriptionMock = mocker.patch("commands.commands.Subscriptions")
    subscriptionMock.return_value = "TEST_SUBSCRIPTION"
    utils = mocker.patch("commands.commands.Utils")
    utils.stopSaveAudio = mocker.async_stub()

    reader.return_value.podcast.title = "TEST_TITLE"

    discordUser = mocker.MagicMock()
    discordUser.id = 123

    user = mocker.MagicMock()
    user.id = 123

    podcast = mocker.MagicMock()
    podcast.id = 1

    subscription = mocker.MagicMock()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    guild = mocker.async_stub()
    guild.voice_client = None

    interaction = mocker.MagicMock()
    interaction.followup = followup
    interaction.response = response
    interaction.guild = guild
    interaction.user = discordUser

    db = mocker.MagicMock()

    return get, followup, interaction, db


@mark.asyncio
async def test_subscribe(mocker: MockerFixture):
    user = mocker.MagicMock()
    user.id = 123

    podcast = mocker.MagicMock()
    podcast.id = 1

    subscription = mocker.MagicMock()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    get, followup, interaction, db = setupMocks(mocker)
    db.getUser = mocker.async_stub()
    db.getPodcastFromTitle = mocker.async_stub()
    db.addUser = mocker.async_stub()
    db.addPodcast = mocker.async_stub()
    db.addSubscription = mocker.async_stub()

    db.getUser.return_value = user
    db.getPodcastFromTitle.return_value = podcast
    db.addSubscription.return_value = subscription

    await commands.subscribe(interaction, "TEST_URL", db, "TEST_SESSION")
    get.assert_called_once_with("https://TEST_URL")
    db.getUser.assert_awaited_once_with("TEST_SESSION", 123)
    db.addUser.assert_not_awaited()
    db.getPodcastFromTitle.assert_awaited_once_with(
        "TEST_SESSION", "TEST_TITLE")
    db.addSubscription.assert_awaited_once_with(
        "TEST_SESSION", "TEST_SUBSCRIPTION")
    followup.send.assert_awaited_once_with(Messages.PodcastAdded)


@mark.asyncio
async def test_subscribe_userNone(mocker: MockerFixture):
    user = mocker.MagicMock()
    user.id = 123

    podcast = mocker.MagicMock()
    podcast.id = 1

    subscription = mocker.MagicMock()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    get, followup, interaction, db = setupMocks(mocker)
    db.getUser = mocker.async_stub()
    db.getPodcastFromTitle = mocker.async_stub()
    db.addUser = mocker.async_stub()
    db.addPodcast = mocker.async_stub()
    db.addSubscription = mocker.async_stub()

    db.getUser.return_value = None
    db.getPodcastFromTitle.return_value = podcast
    db.addSubscription.return_value = subscription
    db.addUser.return_value = user
    await commands.subscribe(interaction, "TEST_URL", db, "TEST_SESSION")
    get.assert_called_once_with("https://TEST_URL")
    db.getUser.assert_awaited_once_with("TEST_SESSION", 123)
    db.addUser.assert_awaited_once_with("TEST_SESSION", 123)
    db.getPodcastFromTitle.assert_awaited_once_with(
        "TEST_SESSION", "TEST_TITLE")
    db.addSubscription.assert_awaited_once_with(
        "TEST_SESSION", "TEST_SUBSCRIPTION")
    followup.send.assert_awaited_once_with(Messages.PodcastAdded)


@mark.asyncio
async def test_subscribe_podcastNone(mocker: MockerFixture):
    user = mocker.MagicMock()
    user.id = 123

    podcast = mocker.MagicMock()
    podcast.id = 1

    subscription = mocker.MagicMock()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    get, followup, interaction, db = setupMocks(mocker)
    db.getUser = mocker.async_stub()
    db.getPodcastFromTitle = mocker.async_stub()
    db.addUser = mocker.async_stub()
    db.addPodcast = mocker.async_stub()
    db.addSubscription = mocker.async_stub()

    db.getUser.return_value = user
    db.getPodcastFromTitle.return_value = None
    db.addSubscription.return_value = subscription
    db.addPodcast.return_value = podcast

    await commands.subscribe(interaction, "TEST_URL", db, "TEST_SESSION")
    get.assert_called_once_with("https://TEST_URL")
    db.getUser.assert_awaited_once_with("TEST_SESSION", 123)
    db.addUser.assert_not_awaited()
    db.getPodcastFromTitle.assert_awaited_once_with(
        "TEST_SESSION", "TEST_TITLE")
    db.addPodcast.assert_awaited_once_with("TEST_SESSION", "TEST_PODCAST")
    db.addSubscription.assert_awaited_once_with(
        "TEST_SESSION", "TEST_SUBSCRIPTION")
    followup.send.assert_awaited_once_with(Messages.PodcastAdded)


@mark.asyncio
async def test_subscribe_subscriptionNone(mocker: MockerFixture):
    user = mocker.MagicMock()
    user.id = 123

    podcast = mocker.MagicMock()
    podcast.id = 1

    subscription = mocker.MagicMock()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    get, followup, interaction, db = setupMocks(mocker)
    db.getUser = mocker.async_stub()
    db.getPodcastFromTitle = mocker.async_stub()
    db.addUser = mocker.async_stub()
    db.addPodcast = mocker.async_stub()
    db.addSubscription = mocker.async_stub()

    db.getUser.return_value = user
    db.getPodcastFromTitle.return_value = podcast
    db.addSubscription.return_value = None

    await commands.subscribe(interaction, "TEST_URL", db, "TEST_SESSION")
    get.assert_called_once_with("https://TEST_URL")
    db.getUser.assert_awaited_once_with("TEST_SESSION", 123)
    db.addUser.assert_not_awaited()
    db.getPodcastFromTitle.assert_awaited_once_with(
        "TEST_SESSION", "TEST_TITLE")
    db.addPodcast.assert_not_awaited()
    db.addSubscription.assert_awaited_once_with(
        "TEST_SESSION", "TEST_SUBSCRIPTION")
    followup.send.assert_awaited_once_with(Messages.PodcastNotAdded)


@mark.asyncio
async def test_list_userNone(mocker: MockerFixture):
    user = mocker.MagicMock()
    user.id = 123

    podcast = mocker.MagicMock()
    podcast.id = 1

    subscription = mocker.MagicMock()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    get, followup, interaction, db = setupMocks(mocker)
    db.getUser = mocker.async_stub()
    db.getPodcastFromTitle = mocker.async_stub()
    db.addUser = mocker.async_stub()
    db.addPodcast = mocker.async_stub()
    db.addSubscription = mocker.async_stub()

    db.getUser.return_value = None
    db.getPodcastFromTitle.return_value = podcast
    db.addSubscription.return_value = None
    await commands.list(interaction, db, "TEST_SESSION")
    db.getUser.assert_awaited_once_with("TEST_SESSION", 123)
    followup.send.assert_awaited_once_with(Messages.UserNotFound)


@mark.asyncio
async def test_list(mocker: MockerFixture):
    user = mocker.MagicMock()
    user.id = 123
    mockSub1 = mocker.MagicMock()
    mockSub1.id = 1
    mockSub2 = mocker.MagicMock()
    mockSub2.id = 2

    user.subscriptions = [mockSub1, mockSub2]

    podcast = mocker.MagicMock()
    podcast.id = 1
    podcast.title = "TEST1"
    podcast2 = mocker.MagicMock()
    podcast2.id = 2
    podcast2.title = "TEST2"

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    get, followup, interaction, db = setupMocks(mocker)
    db.getUser = mocker.async_stub()
    db.getPodcastFromTitle = mocker.async_stub()
    db.addUser = mocker.async_stub()
    db.addPodcast = mocker.async_stub()
    db.addSubscription = mocker.async_stub()
    db.getPodcastBulk = mocker.async_stub()

    db.getUser.return_value = user
    db.getPodcastFromTitle.return_value = podcast
    db.addSubscription.return_value = None
    db.getPodcastBulk.return_value = [podcast, podcast2]
    await commands.list(interaction, db, "TEST_SESSION")
    db.getUser.assert_awaited_once_with("TEST_SESSION", 123)
    db.getPodcastBulk.assert_awaited_once_with("TEST_SESSION", [1, 2])
    followup.send.assert_awaited_once_with(
        'You are subscribed to:  \n- TEST1  \n- TEST2')


@mark.asyncio
async def test_unsubscribe(mocker: MockerFixture):
    user = mocker.MagicMock()
    user.id = 123
    mockSub1 = mocker.MagicMock()
    mockSub1.id = 1
    mockSub2 = mocker.MagicMock()
    mockSub2.id = 2

    user.subscriptions = [mockSub1, mockSub2]

    podcast = mocker.MagicMock()
    podcast.id = 1
    podcast.title = "TEST1"
    podcast2 = mocker.MagicMock()
    podcast2.id = 2
    podcast2.title = "TEST2"

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    get, followup, interaction, db = setupMocks(mocker)
    db.getUser = mocker.async_stub()
    db.getPodcastFromTitle = mocker.async_stub()
    db.getSubscriptionUser = mocker.async_stub()
    db.deleteSubscription = mocker.async_stub()
    db.getUser.return_value = user
    db.getPodcastFromTitle.return_value = podcast
    db.getSubscriptionUser.return_value = mockSub1
    await commands.unsubscribe(interaction, "TEST1", db, "TEST_SESSION")
    followup.send.assert_awaited_once_with("Unsubscribed from TEST1")
    db.getPodcastFromTitle.assert_awaited_once_with("TEST_SESSION", "TEST1")
    db.getSubscriptionUser.assert_awaited_once_with("TEST_SESSION", 123, 1)
    db.deleteSubscription.assert_awaited_once_with("TEST_SESSION", mockSub1)


@mark.asyncio
async def test_help_connect(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.sendResponseMessage = mocker.async_stub()

    await commands.help("TEST_INTERACTION", CommandEnum.Connect)
    utils.sendResponseMessage.assert_awaited_once_with(
        "TEST_INTERACTION", Description.Connect)


@mark.asyncio
async def test_help_disconnect(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.sendResponseMessage = mocker.async_stub()

    await commands.help("TEST_INTERACTION", CommandEnum.Disconnect)
    utils.sendResponseMessage.assert_awaited_once_with(
        "TEST_INTERACTION", Description.Disconnect)


@mark.asyncio
async def test_help_stop(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.sendResponseMessage = mocker.async_stub()

    await commands.help("TEST_INTERACTION", CommandEnum.Stop)
    utils.sendResponseMessage.assert_awaited_once_with(
        "TEST_INTERACTION", Description.Stop)


@mark.asyncio
async def test_help_subscribe(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.sendResponseMessage = mocker.async_stub()

    await commands.help("TEST_INTERACTION", CommandEnum.Subscribe)
    utils.sendResponseMessage.assert_awaited_once_with(
        "TEST_INTERACTION", Description.Subscribe)


@mark.asyncio
async def test_help_unsubscribe(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.sendResponseMessage = mocker.async_stub()

    await commands.help("TEST_INTERACTION", CommandEnum.Unsubscribe)
    utils.sendResponseMessage.assert_awaited_once_with(
        "TEST_INTERACTION", Description.Unsubscribe)


@mark.asyncio
async def test_help_play(mocker: MockerFixture):
    utils = mocker.patch("commands.commands.Utils")
    utils.sendResponseMessage = mocker.async_stub()

    await commands.help("TEST_INTERACTION", CommandEnum.Play)
    utils.sendResponseMessage.assert_awaited_once_with(
        "TEST_INTERACTION", Description.Play)


@mark.asyncio
async def test_play(mocker: MockerFixture):
    get = mocker.patch("commands.commands.get")
    get.return_value.content = "TEST_CONTENT"
    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    voice_client = mocker.MagicMock()
    voice_client.play = mocker.async_stub()

    guild = mocker.MagicMock()
    guild.voice_client = voice_client

    discordUser = mocker.MagicMock()
    discordUser.id = 1

    interaction = mocker.MagicMock()
    interaction.response = response
    interaction.guild = guild
    interaction.followup = followup
    interaction.user = discordUser

    reader = mocker.patch("commands.commands.Reader")
    reader.return_value.podcast.title = "TEST_TITLE"
    reader.return_value.podcast.items = [1, 2, 3]
    reader.return_value.getEpisodeUrl = mocker.stub()
    reader.return_value.getEpisodeUrl.return_value = "http://test.test/mp3"
    reader.return_value.getEpisodeTitle.return_value = "EPISODE_TITLE"

    podcastMock = mocker.patch("commands.commands.Podcast")
    podcastMock.return_value = "PODCAST_MOCK"

    episodeMock = mocker.patch("commands.commands.Episode")
    episodeMock.return_value = "TEST_EPISODE"

    customAudio = mocker.patch("commands.commands.CustomAudio")
    customAudio.return_value = "TEST_CUSTOM_AUDIO"

    playState = mocker.patch("commands.commands.Playstate")
    playState.return_value = "TEST_PLAYSTATE"

    user = mocker.MagicMock()
    user.id = 1

    podcast = mocker.MagicMock()
    podcast.id = 1
    podcast.url = "http://test.test"

    subscription = mocker.MagicMock()
    subscription.id = 1
    subscription.userId = 1
    subscription.podcastId = 1

    episode = mocker.MagicMock()
    episode.title = "EPISODE_TITLE"
    episode.episodeNumber = 123

    playstate = mocker.MagicMock()
    playstate.id = 1
    playstate.timestamp = 0

    db = mocker.MagicMock()
    db.getPodcastFromTitle = mocker.async_stub()
    db.getPodcastFromTitle.return_value = podcast
    db.getUser = mocker.async_stub()
    db.getUser.return_value = user
    db.addEpisode = mocker.async_stub()
    db.addEpisode.return_value = episode
    db.updateUser = mocker.async_stub()
    db.getSubscriptionUser = mocker.async_stub()
    db.getSubscriptionUser.return_value = subscription
    db.getEpisodePodcastNumber = mocker.async_stub()
    db.getEpisodePodcastNumber.return_value = None
    db.addPlaystate = mocker.async_stub()
    db.addPlaystate.return_value = playstate
    await commands.play(interaction, "TEST_TITLE", None, None, db, "TEST_SESSION")
    db.getPodcastFromTitle.assert_awaited_once_with(
        "TEST_SESSION", "TEST_TITLE")
    db.getUser.assert_awaited_once_with("TEST_SESSION", 1)
    get.assert_called_once_with("http://test.test")
    podcastMock.assert_called_once_with("TEST_CONTENT")
    reader.assert_called_once_with("PODCAST_MOCK")
    db.getSubscriptionUser.assert_awaited_once_with("TEST_SESSION", 1, 1)
    db.getEpisodePodcastNumber.assert_awaited_once_with("TEST_SESSION", 1, 3)
    episodeMock.assert_called_once_with(
        episodeNumber=3, podcastId=1, title="EPISODE_TITLE")
    db.addEpisode.assert_awaited_once_with("TEST_SESSION", "TEST_EPISODE")
    db.updateUser.assert_awaited_once_with("TEST_SESSION", user)
    db.addPlaystate.assert_awaited_once_with("TEST_SESSION", "TEST_PLAYSTATE")
    customAudio.assert_called_once_with(
        "http://test.test/mp3", 0, 1, before_options="-ss 0ms")
    followup.send.assert_awaited_once_with(
        "Playing TEST_TITLE  \nEpisode 123: EPISODE_TITLE")


@mark.asyncio
async def test_play_wrongTimestamp(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    interaction = mocker.MagicMock()
    interaction.response = response
    interaction.followup = followup

    db = mocker.MagicMock()
    db.getPodcastFromTitle = mocker.async_stub()
    db.getPodcastFromTitle.return_value = None
    db.getUser = mocker.async_stub()
    db.getUser.return_value = None
    await commands.play(interaction, "TEST_NAME", None, "2:2", db, "TEST_SESSION")
    followup.send.assert_awaited_once_with(Messages.FormatError)


@mark.asyncio
async def test_play_rightTimestamp(mocker: MockerFixture):
    content = mocker.MagicMock()
    content.return_value = "TEST_CONTENT"
    get = mocker.patch("commands.commands.get")
    get.return_value.content = content
    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    voice_client = mocker.MagicMock()
    voice_client.play = mocker.async_stub()

    guild = mocker.MagicMock()
    guild.voice_client = voice_client

    discordUser = mocker.MagicMock()
    discordUser.id = 1

    interaction = mocker.MagicMock()
    interaction.response = response
    interaction.guild = guild
    interaction.followup = followup
    interaction.user = discordUser

    reader = mocker.patch("commands.commands.Reader")
    reader.return_value.podcast.title = "TEST_TITLE"
    reader.return_value.podcast.items = [1, 2, 3]
    reader.return_value.getEpisodeUrl = mocker.stub()
    reader.return_value.getEpisodeUrl.return_value = "http://test.test/mp3"
    reader.return_value.getEpisodeTitle.return_value = "EPISODE_TITLE"

    get = mocker.patch("commands.commands.get")
    podcastMock = mocker.patch("commands.commands.Podcast")
    podcastMock.return_value = "PODCAST_MOCK"

    episodeMock = mocker.patch("commands.commands.Episode")
    episodeMock.return_value = "TEST_EPISODE"

    customAudio = mocker.patch("commands.commands.CustomAudio")
    customAudio.return_value = "TEST_CUSTOM_AUDIO"

    playState = mocker.patch("commands.commands.Playstate")
    playState.return_value = "TEST_PLAYSTATE"

    user = mocker.MagicMock()
    user.id = 1

    podcast = mocker.MagicMock()
    podcast.id = 1
    podcast.url = "http://test.test"

    subscription = mocker.MagicMock()
    subscription.id = 1
    subscription.userId = 1
    subscription.podcastId = 1

    episode = mocker.MagicMock()
    episode.title = "EPISODE_TITLE"
    episode.episodeNumber = 123

    playstate = mocker.MagicMock()
    playstate.id = 1
    playstate.timestamp = 0

    db = mocker.MagicMock()
    db.getPodcastFromTitle = mocker.async_stub()
    db.getPodcastFromTitle.return_value = podcast
    db.getUser = mocker.async_stub()
    db.getUser.return_value = user
    db.addEpisode = mocker.async_stub()
    db.addEpisode.return_value = episode
    db.updateUser = mocker.async_stub()
    db.getSubscriptionUser = mocker.async_stub()
    db.getSubscriptionUser.return_value = subscription
    db.getEpisodePodcastNumber = mocker.async_stub()
    db.getEpisodePodcastNumber.return_value = None
    db.addPlaystate = mocker.async_stub()
    db.addPlaystate.return_value = playstate
    await commands.play(interaction, "TEST_NAME", None, "02:02:02", db, "TEST_SESSION")
    customAudio.assert_called_once_with(
        "http://test.test/mp3", 7322000, 1, before_options="-ss 7322000ms")


@mark.asyncio
async def test_play_noUser(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    interaction = mocker.MagicMock()
    interaction.response = response
    interaction.followup = followup

    db = mocker.MagicMock()
    db.getPodcastFromTitle = mocker.async_stub()
    db.getPodcastFromTitle.return_value = None
    db.getUser = mocker.async_stub()
    db.getUser.return_value = None
    await commands.play(interaction, "TEST_NAME", None, None, db, "TEST_SESSION")
    followup.send.assert_awaited_once_with(Messages.UserNotFound)


@mark.asyncio
async def test_play_noPodcast(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    interaction = mocker.MagicMock()
    interaction.response = response
    interaction.followup = followup

    user = mocker.MagicMock()
    user.id = 1

    db = mocker.MagicMock()
    db.getPodcastFromTitle = mocker.async_stub()
    db.getPodcastFromTitle.return_value = None
    db.getUser = mocker.async_stub()
    db.getUser.return_value = user
    await commands.play(interaction, "TEST_NAME", None, None, db, "TEST_SESSION")
    followup.send.assert_awaited_once_with(Messages.PodcastNotFound)


@mark.asyncio
async def test_play_noSubscription(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    interaction = mocker.MagicMock()
    interaction.response = response
    interaction.followup = followup

    user = mocker.MagicMock()
    user.id = 1

    podcast = mocker.MagicMock()
    podcast.id = 1
    podcast.url = "http://test.test"

    db = mocker.MagicMock()
    db.getPodcastFromTitle = mocker.async_stub()
    db.getPodcastFromTitle.return_value = podcast
    db.getUser = mocker.async_stub()
    db.getUser.return_value = user
    db.getSubscriptionUser = mocker.async_stub()
    db.getSubscriptionUser.return_value = None
    await commands.play(interaction, "TEST_NAME", None, None, db, "TEST_SESSION")
    followup.send.assert_awaited_once_with(Messages.SubscriptionNotFound)


@mark.asyncio
async def test_play_lastPodcastId(mocker: MockerFixture):
    get = mocker.patch("commands.commands.get")
    podcastMock = mocker.patch("commands.commands.Podcast")

    customAudio = mocker.patch("commands.commands.CustomAudio")
    customAudio.return_value = "TEST_CUSTOM_AUDIO"

    reader = mocker.patch("commands.commands.Reader")
    reader.return_value.podcast.title = "TEST_TITLE"
    reader.return_value.podcast.items = [1, 2, 3]
    reader.return_value.getEpisodeUrl = mocker.stub()
    reader.return_value.getEpisodeUrl.return_value = "http://test.test/mp3"
    reader.return_value.getEpisodeTitle.return_value = "EPISODE_TITLE"

    response = mocker.MagicMock()
    response.defer = mocker.async_stub()

    followup = mocker.MagicMock()
    followup.send = mocker.async_stub()

    interaction = mocker.MagicMock()
    interaction.response = response
    interaction.followup = followup

    user = mocker.MagicMock()
    user.id = 1
    user.lastPodcastId = 1
    user.lastEpisodeId = 1

    podcast = mocker.MagicMock()
    podcast.id = 1
    podcast.url = "http://test.test"

    subscription = mocker.MagicMock()
    subscription.id = 1
    subscription.userId = 1
    subscription.podcastId = 1

    episode = mocker.MagicMock()
    episode.id = 1
    episode.title = "EPISODE_TITLE"
    episode.episodeNumber = 123

    playstate = mocker.MagicMock()
    playstate.id = 1
    playstate.timestamp = 0

    db = mocker.MagicMock()
    db.getPodcastFromTitle = mocker.async_stub()
    db.getPodcastFromTitle.return_value = podcast
    db.getUser = mocker.async_stub()
    db.getUser.return_value = user
    db.getSubscriptionUser = mocker.async_stub()
    db.getSubscriptionUser.return_value = subscription
    db.getEpisode = mocker.async_stub()
    db.getEpisode.return_value = episode
    db.getPlaystateUserEpisode = mocker.async_stub()
    db.getPlaystateUserEpisode.return_value = playstate
    db.updateUser = mocker.async_stub()
    await commands.play(interaction, "TEST_NAME", None, None, db, "TEST_SESSION")
    db.getEpisode.assert_awaited_once_with("TEST_SESSION", 1)
    db.getPlaystateUserEpisode.assert_awaited_once_with("TEST_SESSION", 1, 1)
