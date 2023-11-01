from rssreader.reader import Reader


class PodcastMock():
    def __init__(self) -> None:
        self.items = [ItemMock("test_url1"), ItemMock(
            "test_url2"), ItemMock("test_url3")]


class ItemMock():
    def __init__(self, url) -> None:
        self.enclosure_url = url


def test_reader() -> None:
    reader = Reader(PodcastMock())
    assert len(reader.podcast.items) == 3


def test_reader_getEpisode() -> None:
    reader = Reader(PodcastMock())
    assert reader.getEpisode(0) == "test_url1"
