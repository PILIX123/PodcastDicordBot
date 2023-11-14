from botmodules.rssreader.reader import Reader


class PodcastMock():
    def __init__(self) -> None:
        self.items = [ItemMock("test_url1", "title1"), ItemMock(
            "test_url2", "title2"), ItemMock("test_url3", "title3")]


class ItemMock():
    def __init__(self, url, title) -> None:
        self.enclosure_url = url
        self.title = title


def test_reader() -> None:
    reader = Reader(PodcastMock())
    assert len(reader.podcast.items) == 3


def test_reader_getEpisodeUrl() -> None:
    reader = Reader(PodcastMock())
    assert reader.getEpisodeUrl(0) == "test_url1"


def test_reader_getEpisodeTitle() -> None:
    reader = Reader(PodcastMock())
    assert reader.getEpisodeTitle(1) == "title2"
