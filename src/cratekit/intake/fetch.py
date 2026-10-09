"""The fetch seam: a mix at a web address, brought to this machine to be identified.

The source system's first input shape was a SoundCloud or Mixcloud address. It
ran ``yt-dlp`` into a set folder under the library and identified what landed.
Until U104 this package refused the address at the queue (R-303), so that door
was a manual download away from working.

WHAT IS PORTED AND WHAT IS NOT. The download is ported, through the engine U80
already landed: :class:`cratekit.acquire.fallback.YtDlpFetcher` is the one
spelling of a ``yt-dlp`` audio download in this package, and the mix download
is that argv with two edits rather than a second argv to keep safe. WHERE IT
LANDS is not ported. The source system kept the mix in a set folder beside the
music. Here a mix is INPUT and never library material: it lands in a scratch
folder under the installation state root, is identified, and is removed when
the pass ends, however it ends.

THE SCRATCH FOLDER IS ONE PER ADDRESS, named by a digest of the address and
cleared before every attempt. A process killed mid download leaves at most one
folder, and running the same address again, which is what a person does next,
clears it. Two passes over the SAME address at the same moment share that
folder, so the second clears the first's recording and the first fails loudly
inside the carver. That is accepted rather than locked against.

REMOVED HOWEVER THE PASS ENDS, a raise included. The recognition cache keeps
what a raised pass paid for, keyed by the recording's bytes, and whether a
second download reproduces those bytes is NOT measured here. It is recorded as
a residual rather than answered by keeping a few hundred megabytes in a folder
nobody is shown.

THIS MODULE RAISES NO REFUSAL. It raises plain exceptions, each naming ONE
situation, and the verb turns them into its own vocabulary, which is how
``acquire.fallback`` and its command line are split. They are separate types
because they are separate instructions: a download that timed out is worth
running again, a playlist address never is, and a scratch folder that cannot
be made is a fact about this machine and not about the address.

No test runs ``yt-dlp``. ``fetcher`` is looked up on this module at call time,
the suite's conftest replaces it with one that fails the test, and a test that
wants a download injects a fake.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlsplit

from cratekit.acquire import fallback
from cratekit.core import binaries, config

#: The declared state entry the scratch folders live under.
SCRATCH_KEY = "mix_scratch"

#: How much of the address's digest names its scratch folder. Sixteen hex
#: characters is sixty four bits, which no two addresses a person fetches share.
SCRATCH_DIGEST_CHARS = 16

#: Seconds one mix download may take. NOT MEASURED. U80's bound is fifteen
#: minutes for one track, and a mix is a two hour upload converted after it
#: lands, so this is four times that. The attended first address is where the
#: real number comes from.
SET_FETCH_TIMEOUT_SECONDS = 3600

#: What a tracklist is named for when the address's last segment names nothing.
DEFAULT_STEM = "mix"

#: The longest stem an address may give a tracklist. A percent encoded title
#: runs to hundreds of characters, a file name is refused past 255 bytes, and
#: the tracklist is written AFTER the paid step, so an unbounded stem is a
#: refusal that arrives with the bill. The digest beside it keeps names apart.
STEM_MAX_CHARS = 80

#: Entries asked of an address that turns out to be a playlist. TWO, because
#: two is enough to know there is more than one and a whole set page is hours.
PLAYLIST_PROBE = 2

#: Seconds between two progress lines while a mix downloads (R-924). The
#: measured first address took about seven minutes for 557 MB, so fifteen
#: seconds is a line a person sees move without a screen of them.
FETCH_PROGRESS_SECONDS = 15.0

#: The watcher thread's name, so a test can see none outlived its fetch.
WATCHER_NAME = "mix fetch progress"

#: What a progress line is handed. A no op is what JSON output gets.
Progress = Callable[[str], None]

_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")


class SetFetchFailed(Exception):
    """The mix could not be brought to this machine. Never read as "nothing there".

    WHETHER RUNNING IT AGAIN CAN HELP IS NOT KNOWN from a failed download: a
    dead address and a dead network both end ``yt-dlp`` non zero. So this says
    nothing about retrying, and only :class:`SetFetchTimedOut` does.
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

    U80 only ever hands its fetcher a single track page it found by searching.
    A person hands this one anything, and a set page or a playlist is an
    address too. ``--no-playlist`` does not stop a pure playlist address, and
    U80's fixed output name would land every entry on ONE file name, so a
    playlist of twelve recordings would come back as one file that looks like
    a whole mix. Numbering the output makes each entry its own file, which
    ``landed_in`` then refuses as more than one, and the probe bound stops the
    download at two entries instead of at the whole page.
    """

    def argv(self, url: str, directory: Path) -> list[str]:
        argv = super().argv(url, directory)
        template = argv.index("--output") + 1
        argv[template] = str(directory / f"{fallback.FETCH_STEM}-%(autonumber)s.%(ext)s")
        argv[1:1] = ["--playlist-end", str(PLAYLIST_PROBE)]
        return argv


class YtDlpSetFetcher:
    """The shipped fetcher: U80's ``yt-dlp`` download under a mix sized bound.

    ``run`` is ``subprocess.run`` in production and a fake in every test.
    """

    def __init__(
        self,
        binary: str,
        *,
        run: Callable[..., Any] = subprocess.run,
        timeout: float = SET_FETCH_TIMEOUT_SECONDS,
    ) -> None:
        self._inner = _MixDownload(binary, run=run, timeout=timeout)

    def argv(self, url: str, directory: Path) -> list[str]:
        return self._inner.argv(url, directory)

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


def fetcher() -> SetFetcher:
    """The shipped fetcher, or :class:`binaries.BinaryNotFound` naming the fix.

    THE NETWORK SEAM. The suite replaces this function, so no test ever builds
    the shipped fetcher and no test ever runs ``yt-dlp``.
    """
    return YtDlpSetFetcher(binaries.resolve(fallback.BINARY))


def scratch_for(url: str) -> Path:
    """The one folder this address is fetched into. Creates nothing."""
    token = hashlib.sha256(url.strip().encode("utf-8")).hexdigest()[:SCRATCH_DIGEST_CHARS]
    return config.state_path(SCRATCH_KEY) / token


def stem_of(url: str) -> str:
    """What a tracklist of this mix is named for: the address's last segment.

    The source system titled a set the same way. Reduced to letters, digits,
    dot, dash and underscore, because the address is a stranger's text and the
    result becomes a file name.
    """
    segments = [one for one in urlsplit(url.strip()).path.split("/") if one]
    cleaned = _UNSAFE.sub("-", segments[-1]).strip("-.") if segments else ""
    return cleaned[:STEM_MAX_CHARS].strip("-.") or DEFAULT_STEM


def assert_outside_library(scratch: Path, library_root: Path) -> None:
    """Refuse a scratch folder that resolves to the library or to anything in it.

    RESOLVED ON BOTH SIDES, because the state root is an environment variable
    a person can point anywhere and a symlink makes two spellings of one
    folder. A fetched mix under the library root is a file a library walk
    indexes and rekordbox can be pointed at, which is the one thing this
    module exists not to do.

    AND ASKED OF THE FILESYSTEM, NOT ONLY OF THE STRINGS. ``resolve`` does not
    settle letter case, and the volumes a DJ library sits on are case
    insensitive: driven on this project's own machine, a state root spelled
    in lower case under a library recorded in mixed case resolved to a path
    that is not textually inside it. So every ancestor that exists is also
    compared with ``samefile``, which asks whether two names are one folder.
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


def megabytes(size: int) -> str:
    """A byte count the way a progress line says it."""
    return f"{size / 1_000_000:.1f} MB"


def _bytes_in(directory: Path) -> int:
    """What the download has written so far, partials included. Zero when unreadable.

    A progress line is a hint and never a result, so a file that vanished
    between the listing and the stat, which a downloader renaming its partial
    does, is skipped rather than raised.
    """
    total = 0
    try:
        entries = list(directory.iterdir())
    except OSError:
        return 0
    for one in entries:
        try:
            if one.is_file():
                total += one.stat().st_size
        except OSError:
            continue
    return total


@contextmanager
def _watched(directory: Path, progress: Progress | None) -> Iterator[None]:
    """Report the bytes in ``directory`` every :data:`FETCH_PROGRESS_SECONDS`.

    THE FOLDER IS WATCHED, NOT THE TOOL. ``yt-dlp`` runs with its output
    captured, because its last line of standard error is how a failed download
    is named, and any fetcher behind the seam writes into the folder it was
    handed. So the folder's size is a progress reading every fetcher gives,
    and nothing about the download changes to give it.

    The watcher is stopped and joined before this returns, however the block
    ends, so no line is written after the fetch has been reported done.
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
    url: str,
    library_root: Path,
    found: SetFetcher,
    *,
    progress: Progress | None = None,
) -> Iterator[FetchedMix]:
    """Fetch ``url`` into its scratch folder, lend the file, and remove the folder.

    THE LANDING IS CHECKED, NOT TRUSTED. The fetcher is a seam, and a seam can
    answer with a path anywhere, so what comes back has to be a file inside the
    folder it was handed. Anything else is a failed fetch.

    ``leftover`` is set on the way out, so it is read AFTER the ``with`` block,
    and only a pass that returned can report it.

    ``progress``, when given, is told the download started, how many bytes it
    has written while it runs, and what landed (R-924). A download is minutes
    with nothing else on the screen.
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
        yield held
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
        if scratch.exists():
            held.leftover = str(scratch)


__all__ = [
    "DEFAULT_STEM",
    "FETCH_PROGRESS_SECONDS",
    "PLAYLIST_PROBE",
    "SCRATCH_DIGEST_CHARS",
    "SCRATCH_KEY",
    "SET_FETCH_TIMEOUT_SECONDS",
    "STEM_MAX_CHARS",
    "WATCHER_NAME",
    "FetchedMix",
    "Progress",
    "ScratchUnderLibrary",
    "ScratchUnusable",
    "SetFetchFailed",
    "SetFetchTimedOut",
    "SetFetcher",
    "SeveralRecordings",
    "YtDlpSetFetcher",
    "assert_outside_library",
    "fetched",
    "fetcher",
    "megabytes",
    "scratch_for",
    "stem_of",
]
