"""The fetch seam: a mix at a web address, brought to this machine to be identified.

The source system's first input shape was a SoundCloud or Mixcloud address. It
ran ``yt-dlp`` into a set folder under the library and identified what landed.
Until U104 this package refused the address at the queue (R-303), so that door
was a manual download away from working.

WHAT IS PORTED AND WHAT IS NOT. The download is ported, through the engine U80
already landed: :class:`cratekit.acquire.fallback.YtDlpFetcher` is the one
spelling of a ``yt-dlp`` audio download in this package, and a second one here
would be a second argv to keep safe. WHERE IT LANDS is not ported. The source
system kept the mix in a set folder beside the music. Here a mix is INPUT and
never library material: it lands in a scratch folder under the installation
state root, is identified, and is removed when the pass ends, however it ends.

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

THIS MODULE RAISES NO REFUSAL. It raises two plain exceptions and the verb
turns them into its own vocabulary, which is how ``acquire.fallback`` and its
command line are split.

No test runs ``yt-dlp``. ``fetcher`` is looked up on this module at call time,
the suite's conftest replaces it with one that fails the test, and a test that
wants a download injects a fake.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
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

_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")


class SetFetchFailed(Exception):
    """The mix could not be brought to this machine. Never read as "nothing there"."""


class ScratchUnderLibrary(Exception):
    """The scratch root resolves inside the library, so nothing may be fetched into it."""

    def __init__(self, scratch: Path, library: Path) -> None:
        super().__init__(f"{scratch} is inside the library at {library}")
        self.scratch = scratch
        self.library = library


class SetFetcher(Protocol):
    """The seam. One mix into one empty directory, or :class:`SetFetchFailed`."""

    def fetch(self, url: str, directory: Path) -> Path: ...


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
        self._inner = fallback.YtDlpFetcher(binary, run=run, timeout=timeout)

    def fetch(self, url: str, directory: Path) -> Path:
        try:
            return self._inner.fetch(url, directory)
        except fallback.FallbackUnavailable as exc:
            raise SetFetchFailed(str(exc)) from exc


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
    return cleaned or DEFAULT_STEM


def assert_outside_library(scratch: Path, library_root: Path) -> None:
    """Refuse a scratch folder that resolves to the library or to anything in it.

    RESOLVED ON BOTH SIDES, because the state root is an environment variable
    a person can point anywhere and a symlink makes two spellings of one
    folder. A fetched mix under the library root is a file a library walk
    indexes and rekordbox can be pointed at, which is the one thing this
    module exists not to do.
    """
    here = scratch.resolve()
    library = library_root.resolve()
    if here == library or library in here.parents:
        raise ScratchUnderLibrary(here, library)


@dataclass(slots=True)
class Fetched:
    """One fetched mix, held for the length of a pass."""

    url: str
    path: Path
    #: The scratch folder, when it could not be removed. None is the ordinary end.
    leftover: str | None = None


@contextmanager
def fetched(url: str, library_root: Path, found: SetFetcher) -> Iterator[Fetched]:
    """Fetch ``url`` into its scratch folder, lend the file, and remove the folder.

    THE LANDING IS CHECKED, NOT TRUSTED. The fetcher is a seam, and a seam can
    answer with a path anywhere, so what comes back has to be a file inside the
    folder it was handed. Anything else is a failed fetch.

    ``leftover`` is set on the way out, so it is read AFTER the ``with`` block,
    and only a pass that returned can report it.
    """
    address = url.strip()
    scratch = scratch_for(address)
    assert_outside_library(scratch, library_root)
    held = Fetched(url=address, path=scratch)
    try:
        try:
            if scratch.exists():
                shutil.rmtree(scratch)
            scratch.mkdir(parents=True)
        except OSError as exc:
            raise SetFetchFailed(
                f"the scratch folder {scratch} could not be prepared "
                f"({type(exc).__name__}: {exc.strerror or exc})"
            ) from exc
        landed = Path(found.fetch(address, scratch))
        if not landed.is_file() or scratch.resolve() not in landed.resolve().parents:
            raise SetFetchFailed(
                f"the download answered with {landed}, which is not a file inside "
                f"the folder it was given"
            )
        held.path = landed
        yield held
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
        if scratch.exists():
            held.leftover = str(scratch)


__all__ = [
    "DEFAULT_STEM",
    "SCRATCH_DIGEST_CHARS",
    "SCRATCH_KEY",
    "SET_FETCH_TIMEOUT_SECONDS",
    "Fetched",
    "ScratchUnderLibrary",
    "SetFetchFailed",
    "SetFetcher",
    "YtDlpSetFetcher",
    "assert_outside_library",
    "fetched",
    "fetcher",
    "scratch_for",
    "stem_of",
]
