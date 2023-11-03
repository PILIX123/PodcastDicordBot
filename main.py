from discord import Intents, Interaction, Client, app_commands
from vault.vault import Vault
from database.db import Database
from rssreader.reader import Reader
from utils.customAudio import CustomAudio
from utils.utils import Utils
from utils.converters import Converters
from messages.messages import Messages
from messages.descriptions import Description
from enums.enums import CommandEnum
from pyPodcastParser.Podcast import Podcast
from requests import get
from models.episode import Episode
from models.subscription import Subscriptions
from models.playstate import Playstate
from models.podcasts import Podcast as PodcastDto

vault = Vault()
db = Database()
intents = Intents.none()
intents.guilds = True
intents.voice_states = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="connect", description="Connects to a voice channel")
async def connect(interaction: Interaction):
    await Utils.connect(interaction)


@tree.command(name="stop", description="Stops audio")
async def stop(interaction: Interaction):
    await interaction.response.defer()
    if (interaction.guild.voice_client is not None):
        await Utils.stopSaveAudio(interaction, db)
        await interaction.followup.send(Messages.AudioSaved)
    await interaction.followup.send(Messages.NotConnected)


@tree.command(name="disconnect", description="Disconnects from a voice channel")
async def disconnect(interaction: Interaction):
    await interaction.response.defer()
    if (interaction.guild.voice_client is not None):
        await Utils.stopSaveAudio(interaction, db)
        await interaction.guild.voice_client.disconnect()
        await interaction.followup.send("Disconnected")
    else:
        await interaction.response.send("Not currently connected to a voice channel.")


@tree.command(name="subscribe", description="Subscribes the user to the given RSS feed")
@app_commands.describe(url="URL pointing to the rss feed")
async def subscribe(interaction: Interaction, url: str):
    await interaction.response.defer(thinking=True)
    url = "https://" + \
        url if not \
        (url.startswith("https://") or url.startswith("http://")) \
        else url

    reader = Reader(Podcast(get(url).content))
    user = await db.getUser(interaction.user.id)
    podcast = await db.getPodcastFromTitle(reader.podcast.title)
    if (user is None):
        user = await db.addUser(interaction.user.id)

    if podcast is None:
        podcast = await db.addPodcast(PodcastDto(url=url, title=reader.podcast.title))

    subscription = await db.addSubscription(Subscriptions(userId=user.id, podcastId=podcast.id))

    if subscription:
        await interaction.followup.send("Podcast added")
    else:
        await interaction.followup.send("Podcast wasn't added")


@tree.command(name="list", description="List all podcast you are subscribed to")
async def listing(interaction: Interaction):
    await interaction.response.defer(thinking=True)
    user = await db.getUser(interaction.user.id)
    if user is None:
        await interaction.followup.send(Messages.UserNotFound)
        return

    ids = [s.id for s in user.subscriptions]
    podcasts = await db.getPodcastBulk(ids)
    names = [f"- {p.title}" for p in podcasts]
    nameL = """  
""".join(names)
    await interaction.followup.send(f"""You are subscribed to:  
{nameL}""")


@tree.command(name="unsubscribe", description="Unsubscribes the user from the RSS feed")
@app_commands.describe(name="**RESPECT CAPITALIZATION** Name of the podcast")
async def unsubscribe(interaction: Interaction, name: str):
    await interaction.response.defer(thinking=True)
    user = await db.getUser(interaction.user.id)
    podcast = await db.getPodcastFromTitle(name)
    subscription = await db.getSubscriptionUser(user.id, podcast.id)
    await db.deleteSubscription(subscription)
    await interaction.followup.send(f"Unsubscribed from {name}")


@tree.command(name="play", description="Plays the podcast with the given name.")
@app_commands.describe(name="**RESPECT CAPITALIZATION** Name of the podcast",
                       episode_number="The number of the episode wanted",
                       timestamp="**`HH:MM:SS` format only** Timestamp to start the episode at")
async def play(interaction: Interaction, name: str, episode_number: None | int = None, timestamp: None | str = None):
    await interaction.response.defer(thinking=True)
    podcast = await db.getPodcastFromTitle(name)
    user = await db.getUser(interaction.user.id)
    episode = None
    playstate = None
    timestampms = None
    # TODO add stop audio before starting again
    # TODO /ff to skip 30 sec ahead and /bw to rewind 15 sec
    # TODO:
    # Pouvoir display le nom de l'épisode avec le message de confirmation de jeu
    # Une commande fast-forward et back-ward
    # add completed to playstate, ask user to replay
    # add error handling

    if timestamp is not None:
        if len(timestamp.split(":")) != 3:
            await interaction.followup.send(Messages.FormatError)
        timestampms = Converters.hourStrToMs(timestamp)

    if user is None:
        await interaction.followup.send(Messages.UserNotFound)
        return
    if podcast is None:
        await interaction.followup.send(Messages.PodcastNotFound)
        return

    reader = Reader(Podcast(get(podcast.url).content))

    subscription = await db.getSubscriptionUser(user.id, podcast.id)
    if subscription is None:
        await interaction.followup.send(Messages.SubscriptionNotFound)
        return

    if episode_number is None:
        episode_number = len(reader.podcast.items)

    if podcast.id == user.lastPodcastId:
        episode = await db.getEpisode(user.lastEpisodeId)
    if episode is None:
        episode = await db.getEpisodePodcastNumber(podcast.id, episode_number)
    if episode is not None:
        playstate = await db.getPlaystateUserEpisode(user.id, episode.id)

    reverseNumber = len(reader.podcast.items)-episode_number

    if episode is None:
        episodeDto = Episode(episodeNumber=episode_number,
                             podcastId=podcast.id,
                             title=reader.getEpisodeTitle(reverseNumber))
        episode = await db.addEpisode(episodeDto)

    user.lastEpisodeId = episode.id
    user.lastPodcastId = podcast.id
    await db.updateUser(user)
    if playstate is None:
        playstate = await db.addPlaystate(Playstate(episodeId=episode.id, timestamp=(0 if timestampms is None else timestampms), userId=user.id))

    user.lastEpisodeId = episode.id
    user.lastPodcastId = podcast.id
    if interaction.guild.voice_client is None:
        await Utils.connect(interaction)

    acutalTimestamp = playstate.timestamp if timestampms is None else timestampms
    options = f"-ss {acutalTimestamp}ms"
    source = CustomAudio(reader.getEpisodeUrl(
        reverseNumber), acutalTimestamp, playstate.id, before_options=options)

    interaction.guild.voice_client.play(source)
    episodeNumberName = episode.title if str(
        episode.episodeNumber) in episode.title else f"{episode.episodeNumber}: {episode.title}"
    await interaction.followup.send(f"Playing {name}  \nEpisode {episodeNumberName}")


@tree.command(name="help", description="Explains the use of the commands")
@app_commands.describe(command="Name of the command you want help with")
async def help(interaction: Interaction, command: CommandEnum):
    match(command):
        case CommandEnum.Connect:
            await Utils.sendResponseMessage(interaction, Description.Connect)
        case CommandEnum.Disconnect:
            await Utils.sendResponseMessage(interaction, Description.Disconnect)
        case CommandEnum.Stop:
            await Utils.sendResponseMessage(interaction, Description.Stop)
        case CommandEnum.Subscribe:
            await Utils.sendResponseMessage(interaction, Description.Subscribe)
        case CommandEnum.Unsubscribe:
            await Utils.sendResponseMessage(interaction, Description.Unsubscribe)
        case CommandEnum.Play:
            await Utils.sendResponseMessage(interaction, Description.Play)


@client.event
async def on_ready():
    await tree.sync()
    await db.init()

client.run(vault.get_discord_token())
