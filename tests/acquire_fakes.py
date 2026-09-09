"""A fake acquisition adapter the worker's suite owns, and the audio it lands.

The acquisition worker constructs its adapter through ``cratekit.acquire.build``
by the name the frozen configuration holds, so the fake is REGISTERED under a
name rather than patched over the call: a test that replaced ``build`` would be
a test of nothing this unit added. Registering it drives ``load`` and ``build``
for real, and every network touch in the suite lands here instead.

What the fake lands is REAL AUDIO by container, because the worker checks the
landed file's codec through mutagen and a file of junk bytes reads as
unreadable, which is a different answer from lossy. ``wav_bytes`` is a valid
RIFF WAVE the standard library writes, which mutagen reads as lossless;
``mp3_bytes`` is four valid MPEG-1 layer III frame headers, which it reads as
lossy. Both were measured through ``vendored.codec_of`` before this was written.

Not a test module: pytest does not collect it.
"""

from __future__ import annotations

import io
import json
import wave
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar

from cratekit.acquire.adapter import AdapterSettings, BaseAdapter, Offer, TrackRequest, TrackSource

#: The name the fake is registered under, and what a frozen configuration names.
FAKE_ADAPTER = "fake"

#: The registry declaration a test installs with ``monkeypatch.setitem``.
FAKE_DECLARATION = "tests.acquire_fakes:FakeAdapter"


def wav_bytes(frames: int = 800) -> bytes:
    """A valid mono 16 bit RIFF WAVE of silence. Mutagen: ``WAVE``, lossless."""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(8000)
        handle.writeframes(b"\x00\x00" * frames)
    return buffer.getvalue()


def mp3_bytes(frames: int = 4) -> bytes:
    """Valid MPEG-1 layer III frames, 128 kbps at 44.1 kHz. Mutagen: ``MP3``, lossy."""
    frame = b"\xff\xfb\x90\x00" + b"\x00" * 413
    return frame * frames


def tidal_list(rows: list[tuple[str, str, str]], *, isrc: str | None = None) -> str:
    """A provider list document: ``(id, artist, title)`` per row, as JSON text."""
    tracks: list[dict[str, Any]] = []
    for ref, artist, title in rows:
        row: dict[str, Any] = {"id": ref, "title": title, "artists": [{"name": artist}]}
        if isrc:
            row["isrc"] = isrc
        tracks.append(row)
    return json.dumps({"list": 1, "origin": "tidal", "tracks": tracks})


def text_list(lines: list[str]) -> str:
    return "\n".join(lines) + "\n"


@dataclass
class Landing:
    """What the fake does for one key. ``kind`` names the audio it lands."""

    #: ``lossless`` lands a WAVE, ``lossy`` an MP3, ``unreadable`` junk under a
    #: lossless suffix.
    kind: str = "lossless"
    #: What the OFFER says, which the fake may make a lie about the file.
    offer_lossless: bool = True
    #: Raised from ``offer`` instead of answering.
    offer_raises: BaseException | None = None
    #: Raised from ``fetch`` instead of landing. Raised on EVERY attempt unless
    #: ``fetch_raises_times`` bounds it, so a rate limit can be made to clear.
    fetch_raises: BaseException | None = None
    fetch_raises_times: int | None = None
    #: SKIP RATHER THAN WRITE when a file is already at the landing name, which
    #: is what the wrapped tool does: it reports a skip as a successful call
    #: carrying a path, the shape the vendoring notes are written about. A fake
    #: that always writes overwrites whatever a killed attempt left behind, and
    #: a test over stale staging then passes whether or not anything cleared it.
    skips_when_present: bool = False


@dataclass
class Script:
    """Per test state, held on the adapter CLASS because ``build`` constructs
    the instance and a test cannot hand it anything else."""

    landings: dict[str, Landing] = field(default_factory=dict)
    authenticate_raises: BaseException | None = None
    #: Every request ``offer`` saw, in order, so a test can assert what the
    #: worker asked for and how many times.
    offered: list[TrackRequest] = field(default_factory=list)
    #: Every request ``fetch`` saw, in order.
    fetched: list[TrackRequest] = field(default_factory=list)
    #: Every settings object an adapter was constructed with.
    constructed: list[AdapterSettings] = field(default_factory=list)


def _audio(kind: str) -> tuple[str, bytes]:
    if kind == "lossless":
        return ".wav", wav_bytes()
    if kind == "lossy":
        return ".mp3", mp3_bytes()
    if kind == "unreadable":
        return ".flac", b"not a flac stream at all"
    raise ValueError(f"no such landing kind: {kind!r}")


class FakeSource:
    """The I/O half, answering from the script and touching no network."""

    def __init__(self, settings: AdapterSettings, script: Script) -> None:
        self._settings = settings
        self._script = script

    def _landing(self, request: TrackRequest) -> Landing:
        try:
            return self._script.landings[request.key]
        except KeyError:
            raise LookupError(f"no such track: {request.key}") from None

    def authenticate(self) -> None:
        if self._script.authenticate_raises is not None:
            raise self._script.authenticate_raises

    def offer(self, request: TrackRequest) -> Offer:
        self._script.offered.append(request)
        landing = self._landing(request)
        if landing.offer_raises is not None:
            raise landing.offer_raises
        return Offer(lossless=landing.offer_lossless, detail="scripted")

    def fetch(self, request: TrackRequest, destination: Path) -> Path:
        self._script.fetched.append(request)
        landing = self._landing(request)
        if landing.fetch_raises is not None:
            if landing.fetch_raises_times is None:
                raise landing.fetch_raises
            if landing.fetch_raises_times > 0:
                landing.fetch_raises_times -= 1
                raise landing.fetch_raises
        suffix, payload = _audio(landing.kind)
        destination.mkdir(parents=True, exist_ok=True)
        path = destination / f"{request.key}{suffix}"
        if landing.skips_when_present and path.exists():
            return path
        path.write_bytes(payload)
        return path


class FakeAdapter(BaseAdapter):
    """Registered under ``FAKE_ADAPTER`` for the length of one test."""

    name = FAKE_ADAPTER
    script: ClassVar[Script] = Script()

    def __init__(self, settings: AdapterSettings, *, source: TrackSource | None = None) -> None:
        super().__init__(settings, source=source)
        type(self).script.constructed.append(settings)

    def _source(self, scope: object) -> TrackSource:
        return FakeSource(self.settings, type(self).script)


__all__ = [
    "FAKE_ADAPTER",
    "FAKE_DECLARATION",
    "FakeAdapter",
    "FakeSource",
    "Landing",
    "Script",
    "mp3_bytes",
    "text_list",
    "tidal_list",
    "wav_bytes",
]
