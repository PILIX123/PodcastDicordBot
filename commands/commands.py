from discord import Interaction
from utils.utils import Utils
from messages.messages import Messages
from rssreader.reader import Reader
from pyPodcastParser.Podcast import Podcast
from requests import get
from models.podcasts import Podcast as PodcastDto
from models.subscription import Subscriptions
from enums.enums import CommandEnum
from messages.descriptions import Description
from utils.converters import Converters
from models.episode import Episode
from models.playstate import Playstate
from utils.customAudio import CustomAudio
from database.db import Database

async def connect(interaction:Interaction):
    await Utils.connect(interaction)

async def stop(interaction:Interaction,db:Database,session):
    await interaction.response.defer(thinking=True)
    if (interaction.guild.voice_client is not None):
        await Utils.stopSaveAudio(interaction, db,session)
        await interaction.followup.send(Messages.AudioSaved)
        return
    await interaction.followup.send(Messages.NotConnected)

async def disconnect(interaction:Interaction,db:Database,session):
    await interaction.response.defer(thinking=True)
    if (interaction.guild.voice_client is not None):
        await Utils.stopSaveAudio(interaction, db, session)
        await interaction.guild.voice_client.disconnect()
        await interaction.followup.send(Messages.Disconnected)
    else:
        await interaction.followup.send(Messages.NotConnected)

async def subscribe(interaction:Interaction,url:str,db:Database,session):
    await interaction.response.defer(thinking=True)
    url = "https://" + \
        url if not \
        (url.startswith("https://") or url.startswith("http://")) \
        else url

    p = Podcast(get(url).content)
    reader = Reader(p)
    user = await db.getUser(session, interaction.user.id)
    podcast = await db.getPodcastFromTitle(session, reader.podcast.title)
    if (user is None):
        user = await db.addUser(session, interaction.user.id)

    if podcast is None:
        podcast = await db.addPodcast(session, PodcastDto(url=url, title=reader.podcast.title))

    subscription = await db.addSubscription(session, Subscriptions(userId=user.id, podcastId=podcast.id))

    if subscription:
        await interaction.followup.send(Messages.PodcastAdded)
    else:
        await interaction.followup.send(Messages.PodcastNotAdded)

async def list(interaction:Interaction,db:Database,session):
    await interaction.response.defer(thinking=True)
    user = await db.getUser(session, interaction.user.id)

    if user is None:
        await interaction.followup.send(Messages.UserNotFound)
        return

    ids = [s.id for s in user.subscriptions]
    podcasts = await db.getPodcastBulk(session, ids)
    names = [f"- {p.title}" for p in podcasts]
    nameL = """  
""".join(names)
    t= f"""You are subscribed to:  
{nameL}"""
    await interaction.followup.send(f"""You are subscribed to:  
{nameL}""")

async def unsubscribe(interaction:Interaction,name:str,db:Database,session):
    await interaction.response.defer(thinking=True)
    user = await db.getUser(session, interaction.user.id)

    podcast = await db.getPodcastFromTitle(session, name)
    subscription = await db.getSubscriptionUser(session, user.id, podcast.id)
    await db.deleteSubscription(session, subscription)
    await interaction.followup.send(f"Unsubscribed from {name}")

async def help(interaction:Interaction,command:CommandEnum):
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

async def play(interaction:Interaction,name:str,episode_number: int | None, timestamp: str |None,db:Database,session):
    await interaction.response.defer(thinking=True)
    podcast = await db.getPodcastFromTitle(session, name)
    user = await db.getUser(session, interaction.user.id)
    episode = None
    playstate = None
    timestampms = None
    # TODO add stop audio before starting again
    # TODO /ff to skip 30 sec ahead and /bw to rewind 15 sec
    # TODO:
    # Une commande fast-forward et back-ward
    # add completed to playstate, ask user to replay
    # add error handling
    # mark completed

    if timestamp is not None:
        if len(timestamp.split(":")) != 3:
            await interaction.followup.send(Messages.FormatError)
            return
        timestampms = Converters.hourStrToMs(timestamp)

    if user is None:
        await interaction.followup.send(Messages.UserNotFound)
        return
    if podcast is None:
        await interaction.followup.send(Messages.PodcastNotFound)
        return

    subscription = await db.getSubscriptionUser(session, user.id, podcast.id)
    if subscription is None:
        await interaction.followup.send(Messages.SubscriptionNotFound)
        return
    
    reader = Reader(Podcast(get(podcast.url).content))

    if episode_number is None:
        episode_number = len(reader.podcast.items)

    if podcast.id == user.lastPodcastId:
        #TODO: Add button to confirm 
        episode = await db.getEpisode(session, user.lastEpisodeId)
    if episode is None:
        episode = await db.getEpisodePodcastNumber(session, podcast.id, episode_number)
    if episode is not None:
        playstate = await db.getPlaystateUserEpisode(session, user.id, episode.id)

    reverseNumber = len(reader.podcast.items)-episode_number

    if episode is None:
        episodeDto = Episode(episodeNumber=episode_number,
                             podcastId=podcast.id,
                             title=reader.getEpisodeTitle(reverseNumber))
        episode = await db.addEpisode(session, episodeDto)

    user.lastEpisodeId = episode.id
    user.lastPodcastId = podcast.id
    await db.updateUser(session, user)
    if playstate is None:
        playstate = await db.addPlaystate(session, Playstate(episodeId=episode.id, timestamp=(0 if timestampms is None else timestampms),userId=user.id))

    if interaction.guild.voice_client is None:
        #Not tested because this function is tested and works
        await Utils.connect(interaction) #pragma: no coverage

    acutalTimestamp = playstate.timestamp if timestampms is None else timestampms
    options = f"-ss {acutalTimestamp}ms"
    source = CustomAudio(reader.getEpisodeUrl(
        reverseNumber), acutalTimestamp, playstate.id, before_options=options)

    interaction.guild.voice_client.play(source)
    episodeNumberName = episode.title if str(
        episode.episodeNumber) in episode.title else f"{episode.episodeNumber}: {episode.title}"
    await interaction.followup.send(f"Playing {name}  \nEpisode {episodeNumberName}")
