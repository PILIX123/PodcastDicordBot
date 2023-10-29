from pyPodcastParser.Podcast import Podcast
import requests

class Reader:
    def __init__(self,url) -> None:
        self.podcast = Podcast(requests.get(url).content)

    def getEpisode(self,episodeNum:int):
        return self.podcast.items[episodeNum].enclosure_url