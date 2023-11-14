from discord import FFmpegPCMAudio
from pytest import MonkeyPatch
from botmodules.utils.customAudio import CustomAudio


def test_CustomAudio(monkeypatch: MonkeyPatch) -> None:
    def mockInit(*args, **kwargs):
        return None
    monkeypatch.setattr(FFmpegPCMAudio, "__init__", mockInit)

    customAudio = CustomAudio("", 0, 0)
    assert customAudio.currentTimestamp == 0
    assert customAudio.playstateId == 0


def test_CustomAudio_beforeOptionMS(monkeypatch: MonkeyPatch) -> None:
    def mockInit(*args, **kwargs):
        return None
    monkeypatch.setattr(FFmpegPCMAudio, "__init__", mockInit)

    customAudio = CustomAudio("", 0, 0, before_options="-ss 1245ms")
    assert customAudio.currentTimestamp == 1245
    assert customAudio.playstateId == 0


def test_CustomAudio_read(monkeypatch: MonkeyPatch) -> None:
    def mockRead(*args, **kwargs):
        return None
    monkeypatch.setattr(FFmpegPCMAudio, "read", mockRead)

    customAudio = CustomAudio("", 0, 0)
    customAudio.read()
    assert customAudio.playstateId == 0
    assert customAudio.currentTimestamp == 20
