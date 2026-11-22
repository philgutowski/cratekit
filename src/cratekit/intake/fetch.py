"""The fetch seam: a mix at a web address, brought to this machine to be identified.

The download goes through U80's engine: :class:`cratekit.acquire.fallback.YtDlpFetcher`
is the one spelling of a ``yt-dlp`` audio download, and the mix download is that
argv with two edits rather than a second argv to keep safe. Unlike the source
system, a mix is INPUT and never library material: it lands in a scratch folder
under the installation state root, is identified, and is removed when the pass
ends, however it ends (a raise included).

THE SCRATCH FOLDER IS ONE PER ADDRESS, named by a digest of the address and
cleared before every attempt, so a killed download leaves at most one folder
and running the address again clears it. Two simultaneous passes over one
address share it and the second fails loudly in the carver; that is accepted.

THIS MODULE RAISES NO REFUSAL, only plain exceptions each naming ONE situation,
which the verb turns into its own vocabulary. They are separate types because
they are separate instructions: a timeout is worth a retry, a playlist address
never is, and an unusable scratch folder is a fact about this machine.

No test runs ``yt-dlp``: ``fetcher`` is looked up on this module at call time
and the suite's conftest replaces it.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlsplit

from cratekit.acquire import fallback
from cratekit.core import binaries, config
from cratekit.intake import recognize

#: The declared state entry the scratch folders live under.
SCRATCH_KEY = "mix_scratch"

#: Hex characters of the address's digest naming its scratch folder (64 bits).
SCRATCH_DIGEST_CHARS = 16

#: Seconds one mix download may take, four times U80's bound for one track,
#: because a mix is a two hour upload converted after it lands. Not measured.
SET_FETCH_TIMEOUT_SECONDS = 3600

#: What a tracklist is named for when the address's last segment names nothing.
DEFAULT_STEM = "mix"

#: The longest stem an address may give a tracklist. A percent encoded title
#: can pass the 255 byte file name limit, and the tracklist is written AFTER
#: the paid step, so an unbounded stem is a refusal that arrives with the bill.
STEM_MAX_CHARS = 80

#: Entries asked of an address that turns out to be a playlist: two is enough
#: to know there is more than one, and a whole set page is hours.
PLAYLIST_PROBE = 2

#: Seconds between two progress lines while a mix downloads (R-924).
FETCH_PROGRESS_SECONDS = 15.0

#: The watcher thread's name, so a test can see none outlived its fetch.
WATCHER_NAME = "mix fetch progress"

#: What a progress line is handed. JSON output hands None.
Progress = recognize.Progress

_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")

#: The page facts a set's playlist is named with (U121), as ``yt-dlp`` writes
#: them in the info document beside the download. Kept as plain text, so the
#: job payload carries words and not the whole document.
PAGE_TITLE = "title"
PAGE_UPLOADER = "uploader"
PAGE_UPLOAD_DATE = "upload_date"
PAGE_KEYS = (PAGE_TITLE, PAGE_UPLOADER, PAGE_UPLOAD_DATE)

#: What ``yt-dlp`` names the info document, next to the download, by the stem.
INFO_SUFFIX = ".info.json"


class SetFetchFailed(Exception):
    """The mix could not be brought to this machine. Never read as "nothing there".

    Says nothing about retrying: a dead address and a dead network both end
    ``yt-dlp`` non zero. Only :class:`SetFetchTimedOut` does.
    """


class SetFetchTimedOut(SetFetchFailed):
    """The download ran out its bound. The one failure known to be worth a retry."""


class SeveralRecordings(SetFetchFailed):
    """The address is a playlist of more than one recording, and one was asked for."""


class ScratchUnusable(Exception):
    """The scratch folder could not be prepared. A fact about this machine."""


class ScratchUnderLibrary(Exception):
    """The scratch root resolves inside the library, so nothing may be fetched into it."""

    def __init__(self, scratch: Path, library: Path) -> None:
        super().__init__(f"{scratch} is inside the library at {library}")
        self.scratch = scratch
        self.library = library


class SetFetcher(Protocol):
    """The seam. One mix into one empty directory, or :class:`SetFetchFailed`."""

    def fetch(self, url: str, directory: Path) -> Path: ...


class _MixDownload(fallback.YtDlpFetcher):
    """U80's download with the two edits a stranger's MIX address needs.

    ``--no-playlist`` does not stop a pure playlist address, and U80's fixed
    output name would land every entry on ONE file that looks like a whole
    mix. Numbered output makes each entry its own file, which is refused as
    more than one, and the probe bound stops the download at two entries.
    """

    def argv(self, url: str, directory: Path) -> list[str]:
        argv = super().argv(url, directory)
        template = argv.index("--output") + 1
        argv[template] = str(directory / f"{fallback.FETCH_STEM}-%(autonumber)s.%(ext)s")
        # THE PAGE IS KEPT BESIDE THE RECORDING (U121), to name the set's
        # playlist. Not an audio file, so the recording count never sees it.
        argv[1:1] = ["--playlist-end", str(PLAYLIST_PROBE), "--write-info-json"]
        return argv


class YtDlpSetFetcher:
    """The shipped fetcher: U80's ``yt-dlp`` download under a mix sized bound.
    ``run`` is ``subprocess.run`` in production and a fake in every test."""

    def __init__(
        self,
        binary: str,
        *,
        run: Callable[..., Any] = subprocess.run,
        timeout: float = SET_FETCH_TIMEOUT_SECONDS,
    ) -> None:
        self._inner = _MixDownload(binary, run=run, timeout=timeout)

    def fetch(self, url: str, directory: Path) -> Path:
        try:
            return self._inner.fetch(url, directory)
        except fallback.FallbackUnavailable as exc:
            if isinstance(exc.__cause__, subprocess.TimeoutExpired):
                raise SetFetchTimedOut(str(exc)) from exc
            landed = _recordings_in(directory)
            if len(landed) > 1:
                raise SeveralRecordings(
                    f"the address is a playlist of more than one recording "
                    f"({', '.join(landed)}), and one mix is fetched at a time"
                ) from exc
            raise SetFetchFailed(str(exc)) from exc


def _recordings_in(directory: Path) -> list[str]:
    if not directory.is_dir():
        return []
    return sorted(
        one.name
        for one in directory.iterdir()
        if one.is_file() and one.suffix.lower() == fallback.FETCH_SUFFIX
    )


def page_of(directory: Path) -> dict[str, str]:
    """The page facts the info documents in ``directory`` carry, or nothing (U121).

    READ, NEVER REQUIRED: no document, no JSON or none of the keys is an empty
    answer, and the playlist is named from the flags. Several documents are
    read in name order and the first word for each key kept.
    """
    if not directory.is_dir():
        return {}
    found: dict[str, str] = {}
    for one in sorted(directory.iterdir()):
        if not one.is_file() or not one.name.lower().endswith(INFO_SUFFIX):
            continue
        try:
            parsed = json.loads(one.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(parsed, dict):
            continue
        for key in PAGE_KEYS:
            value = parsed.get(key)
            if key not in found and isinstance(value, str) and value.strip():
                found[key] = value.strip()
    return found


def fetcher() -> SetFetcher:
    """The shipped fetcher, or :class:`binaries.BinaryNotFound` naming the fix.
    THE NETWORK SEAM, replaced by the suite so no test runs ``yt-dlp``."""
    return YtDlpSetFetcher(binaries.resolve(fallback.BINARY))


def scratch_for(url: str) -> Path:
    """The one folder this address is fetched into. Creates nothing."""
    token = hashlib.sha256(url.strip().encode("utf-8")).hexdigest()[:SCRATCH_DIGEST_CHARS]
    return config.state_path(SCRATCH_KEY) / token


def stem_of(url: str) -> str:
    """What a tracklist of this mix is named for: the address's last segment,
    reduced to letters, digits, dot, dash and underscore, because the address
    is a stranger's text and the result becomes a file name."""
    segments = [one for one in urlsplit(url.strip()).path.split("/") if one]
    cleaned = _UNSAFE.sub("-", segments[-1]).strip("-.") if segments else ""
    return cleaned[:STEM_MAX_CHARS].strip("-.") or DEFAULT_STEM


def assert_outside_library(scratch: Path, library_root: Path) -> None:
    """Refuse a scratch folder that resolves to the library or to anything in it.

    A mix under the library is a file a library walk indexes, the one thing
    this module exists not to make. RESOLVED ON BOTH SIDES, because the state
    root can point anywhere and a symlink makes two spellings of one folder.
    AND ASKED OF THE FILESYSTEM: ``resolve`` does not settle letter case on a
    case insensitive volume, so every existing ancestor is also compared with
    ``samefile``.
    """
    here = scratch.resolve()
    library = library_root.resolve()
    if here == library or library in here.parents:
        raise ScratchUnderLibrary(here, library)
    if not library.exists():
        return
    for ancestor in (here, *here.parents):
        if ancestor.exists() and ancestor.samefile(library):
            raise ScratchUnderLibrary(here, library)


@dataclass(slots=True)
class FetchedMix:
    """One fetched mix, held for the length of a pass."""

    url: str
    path: Path
    #: The scratch folder, when it could not be removed. None is the ordinary end.
    leftover: str | None = None
    #: What the page said, under :data:`PAGE_KEYS`, each only when carried (U121).
    page: dict[str, str] = field(default_factory=dict)


def megabytes(size: int) -> str:
    """A byte count the way a progress line says it."""
    return f"{size / 1_000_000:.1f} MB"


def _bytes_in(directory: Path) -> int:
    """The size of the largest file in ``directory``. Zero when unreadable.

    THE LARGEST, NOT THE SUM: fragments sit beside the growing partial and the
    converted MP3 beside its source, so a sum counts bytes twice and runs
    backwards when they go. A progress line is a hint, so a file that vanished
    between the listing and the stat is skipped rather than raised.
    """
    largest = 0
    try:
        entries = list(directory.iterdir())
    except OSError:
        return 0
    for one in entries:
        try:
            if one.is_file():
                largest = max(largest, one.stat().st_size)
        except OSError:
            continue
    return largest


@contextmanager
def _watched(directory: Path, progress: Progress | None) -> Iterator[None]:
    """Report the bytes in ``directory`` every :data:`FETCH_PROGRESS_SECONDS`.

    THE FOLDER IS WATCHED, NOT THE TOOL: ``yt-dlp``'s output is captured to
    name a failure, and every fetcher writes into the folder it was handed.
    The watcher is joined before this returns, however the block ends, so no
    line follows the fetch being reported done.
    """
    if progress is None:
        yield
        return
    stop = threading.Event()
    started = time.monotonic()

    def watch() -> None:
        while not stop.wait(FETCH_PROGRESS_SECONDS):
            elapsed = int(time.monotonic() - started)
            progress(f"fetching: {megabytes(_bytes_in(directory))} so far, {elapsed}s")

    watcher = threading.Thread(target=watch, name=WATCHER_NAME, daemon=True)
    watcher.start()
    try:
        yield
    finally:
        stop.set()
        watcher.join()


@contextmanager
def fetched(
    url: str, library_root: Path, found: SetFetcher, *, progress: Progress | None = None
) -> Iterator[FetchedMix]:
    """Fetch ``url`` into its scratch folder, lend the file, and remove the folder.

    THE LANDING IS CHECKED, NOT TRUSTED: a seam can answer with a path
    anywhere, so it must be a file inside the folder it was handed.
    ``leftover`` is set on the way out, so it is read AFTER the ``with`` block.
    ``progress`` is told the start, the bytes so far and what landed (R-924).
    """
    address = url.strip()
    scratch = scratch_for(address)
    assert_outside_library(scratch, library_root)
    held = FetchedMix(url=address, path=scratch)
    try:
        try:
            if scratch.exists():
                shutil.rmtree(scratch)
            scratch.mkdir(parents=True)
        except OSError as exc:
            raise ScratchUnusable(
                f"the scratch folder {scratch} could not be prepared "
                f"({type(exc).__name__}: {exc.strerror or exc})"
            ) from exc
        if progress is not None:
            progress(f"fetching: {address}")
        started = time.monotonic()
        with _watched(scratch, progress):
            landed = Path(found.fetch(address, scratch))
        if not landed.is_file() or scratch.resolve() not in landed.resolve().parents:
            raise SetFetchFailed(
                f"the download answered with {landed}, which is not a file inside "
                f"the folder it was given"
            )
        if progress is not None:
            elapsed = int(time.monotonic() - started)
            progress(f"fetched: {megabytes(landed.stat().st_size)} in {elapsed}s")
        held.path = landed
        held.page = page_of(scratch)
        yield held
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
        if scratch.exists():
            held.leftover = str(scratch)
