from typing import Protocol


class Podcast(Protocol):  # pragma: no cover
    def __init__(self) -> None:
        self.items: list[Items]
        super().__init__()


class Items(Protocol):  # pragma: no cover
    def __init__(self) -> None:
        self.enclosure_url: str
        super().__init__()


class Reader:
    def __init__(self, podcast: Podcast) -> None:
        self.podcast = podcast

    def getEpisode(self, episodeNum: int) -> str:
        return self.podcast.items[episodeNum].enclosure_url
