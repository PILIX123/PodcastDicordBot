from pyPodcastParser.Podcast import Podcast
from requests import get


class Reader:
    def __init__(self, url) -> None:
        self.podcast = Podcast(get(url).content)

    def getEpisode(self, episodeNum: int):
        return self.podcast.items[episodeNum].enclosure_url
