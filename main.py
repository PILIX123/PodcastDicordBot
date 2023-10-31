import discord
from vault.vault import Vault
from discord import app_commands
from database.db import Database
from rssreader.reader import Reader
from utils.customAudio import CustomAudio
from utils.utils import Utils
from utils.converters import Converters
from messages.messages import Messages


vault = Vault()
db = Database()
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)


@tree.command(name="connect", description="connect to voice chat")
async def connect(interaction: discord.Interaction):
    await Utils.connect(interaction)


@tree.command(name="stop")
async def stop(interaction: discord.Interaction):
    await interaction.response.defer()
    if (interaction.guild.voice_client is not None):
        await Utils.stopSaveAudio(interaction, db)
        await interaction.followup.send("audio stopped and timestamp saved")
    await interaction.followup.send(Messages.NotConnected)


@tree.command(name="disconnect", description="disconnects from channel")
async def disconnect(interaction: discord.Interaction):
    await interaction.response.defer()
    if (interaction.guild.voice_client is not None):
        await Utils.stopSaveAudio(interaction, db)
        await interaction.guild.voice_client.disconnect()
        await interaction.followup.send("Disconnected")
    else:
        await interaction.response.send("Not currently connected to a voice channel.")


@tree.command(name="subscribe")
async def subscribe(interaction: discord.Interaction, url: str):
    await interaction.response.defer(thinking=True)
    url = "https://" + \
        url if not \
        (url.startswith("https://") or url.startswith("http://")) \
        else url

    reader = Reader(url)
    user = await db.getUser(interaction.user.id)
    podcast = await db.getPodcastFromTitle(reader.podcast.title)
    if (user is None):
        user = await db.addUser(interaction.user.id)

    if podcast is None:
        podcast = await db.addPodcast(url, reader.podcast.title)

    subscription = await db.addSubscription(user.id, podcast.id)

    if subscription:
        await interaction.followup.send("Podcast added")
    else:
        await interaction.followup.send("Podcast wasn't added")


@tree.command(name="unsubscribe")
async def unsubscribe(interaction: discord.Interaction, title: str):
    await interaction.response.defer(thinking=True)
    user = await db.getUser(interaction.user.id)
    podcast = await db.getPodcastFromTitle(title)
    subscription = await db.getSubscriptionUser(user.id, podcast.id)
    await db.deleteSubscription(subscription)
    await interaction.followup.send(f"Unsubscribed from {title}")


@tree.command(name="play")
async def play(interaction: discord.Interaction, name: str, episode_number: None | int = None, timestamp: None | str = None):
    await interaction.response.defer(thinking=True)
    podcast = await db.getPodcastFromTitle(name)
    user = await db.getUser(interaction.user.id)
    episode = None
    playstate = None
    timestampms = None

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

    reader = Reader(podcast.url)

    subscription = await db.getSubscriptionUser(user.id, podcast.id)
    if subscription is None:
        await interaction.followup.send(Messages.SubscriptionNotFound)
        return

    if episode_number is None:
        episode_number = len(reader.podcast.items)
    if episode_number is not None:
        episode = await db.getEpisodePodcastNumber(podcast.id, episode_number)
    if episode is not None:
        playstate = await db.getPlaystateUserEpisode(user.id, episode.id)

    if episode is None:
        episode = await db.addEpisode(episode_number, podcast.id)

    if playstate is None:
        playstate = await db.addPlaystate(episode.id, (0 if timestampms is None else timestampms), user.id)

    if interaction.guild.voice_client is None:
        await Utils.connect(interaction)

    acutalTimestamp = playstate.timestamp if timestampms is None else timestampms
    options = f"-ss {acutalTimestamp}ms"
    reverseNumber = len(reader.podcast.items)-episode.episodeNumber
    source = CustomAudio(reader.getEpisode(
        reverseNumber), acutalTimestamp, playstate.id, before_options=options)

    interaction.guild.voice_client.play(source)
    await interaction.followup.send(f"Playing {name}")


@client.event
async def on_ready():
    await tree.sync()
    await db.init()

client.run(vault.get_discord_token())
