from io import BufferedIOBase
from typing import IO
from discord import FFmpegPCMAudio
from utils.converters import Converters


class CustomAudio(FFmpegPCMAudio):
    def __init__(self, source: str | BufferedIOBase, timestamp: int, playstateId: int, *, executable: str = 'ffmpeg', pipe: bool = False, stderr: IO[str] | None = None, before_options: str | None = None, options: str | None = None) -> None:
        self.currentTimestamp = timestamp
        self.playstateId = playstateId
        self.url = source if type(source) is str else None
        if before_options is not None:
            if (before_options.startswith("-ss") and before_options.endswith("ms")):
                self.currentTimestamp = int(before_options[4:-2])
        super().__init__(source, executable=executable, pipe=pipe,
                         stderr=stderr, before_options=before_options, options=options)

    def read(self) -> bytes:
        self.currentTimestamp += 20
        return super().read()
