from pyPodcastParser.Podcast import Podcast
import requests

class Reader:
    def __init__(self,url) -> None:
        self.podcast = Podcast(requests.get(url))