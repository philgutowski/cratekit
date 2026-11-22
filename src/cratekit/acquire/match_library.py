"""The library, indexed from what is on the disk (U305).

Split from :mod:`cratekit.acquire.match`, which re-exports every public name.
"""

from __future__ import annotations

import os
import time
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType

from cratekit.acquire.match_identity import (
    Recorded,
    _sorted_words,
    credited_members,
    fold,
    isrc_token,
    key_token,
    recording_identity,
    recording_token,
    same_title,
    split_title,
)
from cratekit.core import naming, tags

#: A short curated list of slang and numeral spellings, each folded word beside
#: the folded word it stands for (card 833). ``Luv U`` against a held ``Love
#: You`` shares no word and scores under :data:`APPROXIMATE_TITLE_FLOOR`, where
#: unrelated pairs sit, so no floor can join them. Read only when two titles are
#: compared, never in a token, identity or anything written, so a pair it joins
#: is offered for review, never called owned. A word missing reads as it always
#: did; ``two`` and ``four`` are left out because, with spaces gone, ``Two Day``
#: would read as ``Today``.
_SPELLED_OUT: Mapping[str, str] = MappingProxyType(
    {
        "u": "you",
        "ur": "your",
        "luv": "love",
        "4": "for",
        "2": "to",
        "too": "to",
        "n": "and",
        "r": "are",
        "b": "be",
        "c": "see",
        "y": "why",
        "thru": "through",
        "tho": "though",
        "nite": "night",
        "tonite": "tonight",
        "2nite": "tonight",
        "2day": "today",
        "2morrow": "tomorrow",
        "4ever": "forever",
        "b4": "before",
        "cuz": "because",
        "coz": "because",
        "lil": "little",
        "gr8": "great",
        "l8r": "later",
    }
)



# ---------------------------------------------------------------------------
# The library, indexed from what is on the disk
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Owned(Recorded):
    """One audio file the library holds, and what the disk says it is."""

    path: Path
    artist: str
    title: str
    version: str
    key: str | None
    #: The file's ISRC, folded, or empty when the tag is absent or malformed.
    isrc: str = ""
    #: The folded names the artist tag credits, computed once per file for the
    #: credited list rule.
    members: frozenset[str] = field(init=False, default=frozenset())

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "members", frozenset(fold(name) for name in credited_members(self.artist))
        )

    @property
    def key_key(self) -> str:
        return key_token(self.key)


@dataclass(frozen=True, slots=True)
class LibraryIndex:
    """Ownership as membership: a caller that forgets a lookup gets nothing and
    notices, where one that forgets a filter gets a plausible answer."""

    by_recording: Mapping[str, tuple[Owned, ...]]
    #: Every file under the folded ISRC it carries. A file with no ISRC tag is
    #: in :attr:`by_recording` and not here.
    by_isrc: Mapping[str, tuple[Owned, ...]] = field(default_factory=dict)
    #: Every file under its folded title alone, for the credited list rule, so a
    #: file is indexed once however many artists it credits.
    by_title: Mapping[str, tuple[Owned, ...]] = field(default_factory=dict)
    #: The recordings beside their words sorted, built lazily on the approximate
    #: pass's first ask and kept for the index's life (U265); read it through
    #: :meth:`sorted_recordings`.
    _sorted: tuple[tuple[str, ...], tuple[str, ...]] | None = field(
        default=None, init=False, repr=False, compare=False
    )
    #: The recordings under their spelled out key (:func:`_spelled_key`), built
    #: lazily like :attr:`_sorted`; read it through :meth:`spelled_alike`.
    _spelled: Mapping[str, tuple[str, ...]] | None = field(
        default=None, init=False, repr=False, compare=False
    )

    @property
    def recordings(self) -> tuple[str, ...]:
        return tuple(self.by_recording)

    def sorted_recordings(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """The recordings, and each one's words sorted, position for position, so
        a position the scorer returns names a recording."""
        cached = self._sorted
        if cached is None:
            recordings = self.recordings
            cached = (recordings, tuple(_sorted_words(token) for token in recordings))
            object.__setattr__(self, "_sorted", cached)
        return cached

    def versions(self, recording: str) -> tuple[Owned, ...]:
        return self.by_recording.get(recording, ())

    def spelled_alike(self, recording: str) -> tuple[str, ...]:
        """The recordings by this artist whose title equals this one's spelled
        out by :data:`_SPELLED_OUT` with spaces gone, where either title holds a
        listed word (card 833), in token order.

        An exact lookup beside the discovery score, never in place of it, because
        a short slang title falls under the score's floor for a short artist.
        """
        cached = self._spelled
        if cached is None:
            grouped: dict[str, list[str]] = {}
            for token in self.by_recording:
                grouped.setdefault(_spelled_key(token), []).append(token)
            cached = {key: tuple(sorted(tokens)) for key, tokens in grouped.items()}
            object.__setattr__(self, "_spelled", cached)
        asks = _holds_spelling(recording)
        return tuple(
            token
            for token in cached.get(_spelled_key(recording), ())
            if asks or _holds_spelling(token)
        )

    def held_by_isrc(self, isrc: str) -> tuple[Owned, ...]:
        """Every file carrying this folded ISRC. Empty for an empty token, so a
        row with no ISRC, or a malformed one, asks nothing here."""
        return self.by_isrc.get(isrc, ()) if isrc else ()

    def held(self, artist: str, title: str) -> tuple[Owned, ...]:
        """Every file that is this recording, under two rules in order.

        The recording token first. Then the credited list rule: a file whose
        folded title is this title and whose artist tag credits this artist as
        one whole member, because a processed file's tag lists every credited
        artist where a provider row names one, the residual titled "The match
        engine never consults the ISRC, and a processed file's artist tag lists
        every credited artist, so a quarter of the hearts the library holds read
        missing or offered". Whole names, never substrings, and a comma is the
        only joiner, since an ampersand is more often a band's own name. Both
        rules read the title by :func:`title_identity`, so titles folding to
        nothing never answer for each other.
        """
        distinct = recording_identity(artist, title)
        exact = tuple(
            one for one in self.versions(recording_token(artist, title))
            if one.distinct == distinct
        )
        member = fold(artist)
        counted = {one.path for one in exact}
        credited = tuple(
            one for one in self.by_title.get(fold(title), ())
            if same_title(one.title, title) and member in one.members
            and one.path not in counted
        )
        return exact + credited

    def __len__(self) -> int:
        return sum(len(held) for held in self.by_recording.values())


@dataclass(frozen=True, slots=True)
class _Remembered:
    """What one clean read of a file said, and the file's stamp when it said it."""

    stamp: tuple[int, int, int, int, int]
    made_ns: int
    owned: Owned


#: The index reader's memory, one entry per file read cleanly in this process
#: (U249), so the several index builds of one sync pass do not reopen every file.
#: Every index is still a fresh walk; only an unchanged file's tags are recalled.
#:
#: An entry answers only while the path, the name template and the file's whole
#: stamp agree: size, modification time, change time, inode and device, because
#: copy tools can restore an old modification time over new bytes and a rename
#: can put a lookalike under the name. A file modified within
#: :data:`REMEMBER_WINDOW_NS` of the entry's moment is never answered from memory,
#: for volumes stamping in two second steps. Only a whole read is remembered.
#: Nothing outlives the process, and :func:`reset_cache` forgets every entry.
_REMEMBERED: dict[tuple[Path, naming.NameTemplate], _Remembered] = {}

#: Two seconds, a FAT volume's modification time step.
REMEMBER_WINDOW_NS = 2_000_000_000

#: The clock an entry's moment is read from, named so a test can hold it.
_now_ns = time.time_ns

#: The four fields the index reads from every file, through one open.
_INDEX_FIELDS = ("artist", "title", "initialkey", "isrc")


def reset_cache() -> None:
    """Forget every file the index reader remembers. A module level memory no
    test can clear is a memory that leaks one test's library into the next."""
    _REMEMBERED.clear()


def remembered() -> int:
    """How many files the index reader remembers, for a test to read."""
    return len(_REMEMBERED)


def _stamp_of(path: Path) -> tuple[int, int, int, int, int] | None:
    """The file's size, modification time, change time, inode and device, or
    None when it cannot be stat'ed, which is a file with no identity to keep."""
    try:
        seen = os.stat(path)
    except OSError:
        return None
    return (seen.st_size, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)


def _read_from_disk(path: Path, template: naming.NameTemplate) -> Owned:
    """What this file is, read once per process while it stays unchanged (U249),
    by the rules noted at :data:`_REMEMBERED`; a miss reads :func:`_read_fresh`.
    """
    made_ns = _now_ns()
    stamp = _stamp_of(path)
    key = (path, template)
    if stamp is not None:
        entry = _REMEMBERED.get(key)
        if (
            entry is not None
            and entry.stamp == stamp
            and stamp[1] <= entry.made_ns - REMEMBER_WINDOW_NS
        ):
            return entry.owned
    owned, whole = _read_fresh(path, template)
    if stamp is not None and whole:
        _REMEMBERED[key] = _Remembered(stamp=stamp, made_ns=made_ns, owned=owned)
    else:
        # A read that was not whole, or a file with no stamp, forgets what an
        # earlier whole read left: the file has been seen changing, and a stamp
        # that came back later must not bring the older answer back with it.
        _REMEMBERED.pop(key, None)
    return owned


def _read_fresh(path: Path, template: naming.NameTemplate) -> tuple[Owned, bool]:
    """What this file is, from its tags first and its filename second, and
    whether the read was whole enough to remember.

    Artist and title fall back as a pair and a present value is never discarded:
    both tags win when both are there, otherwise the name when it carries both
    halves, otherwise each field takes what it has. The key runs the other way,
    the filename's Camelot head first, since this product writes it there, then a
    head found in the title tag, then ``initialkey``. The title tag is stripped of
    its head as the stem is, since the live library writes ``KEY - BPM - `` there
    too and a head inside the token would match no provider row.
    """
    stem = path.stem
    head = naming.parse_head(stem, template=template) or {}
    body = naming.strip_heads(stem, template=template)
    artist_part, separator, title_part = body.partition(template.segment_sep)
    if not separator:
        artist_part, title_part = "", body

    # One container open for the four fields; a failed read is indexed as it
    # always was and never remembered.
    read, whole = tags.read_tags_noting(path, _INDEX_FIELDS)
    tagged_artist = str(read["artist"] or "").strip()
    spelled_tag = read["title"] or ""
    tagged_title = naming.strip_heads(spelled_tag, template=template)
    named_artist, named_title = artist_part.strip(), str(title_part).strip()
    if tagged_artist and tagged_title:
        artist, spelled = tagged_artist, tagged_title
    elif named_artist and named_title:
        artist, spelled = named_artist, named_title
    else:
        artist, spelled = tagged_artist or named_artist, tagged_title or named_title
    title, version = split_title(spelled)

    tag_head = naming.parse_head(spelled_tag, template=template) or {}
    written_key = head.get("key") or tag_head.get("key")
    key = written_key or read["initialkey"]
    return Owned(
        path=path,
        artist=artist,
        title=title,
        version=version,
        key=str(key).strip() if key else None,
        isrc=isrc_token(read["isrc"]),
    ), whole


def index_library(
    root: Path,
    *,
    template: naming.NameTemplate | None = None,
    reader: Callable[[Path, naming.NameTemplate], Owned] = _read_from_disk,
) -> LibraryIndex:
    """Walk the library's music tree and index what it holds.

    ``reader`` is injected for tests, and defaults to the real disk reader so a
    forgotten argument never looks like an empty library.
    """
    return index_paths(
        sorted(root.rglob("*")) if root.is_dir() else (), template=template, reader=reader
    )


def index_paths(
    paths: Iterable[Path],
    *,
    template: naming.NameTemplate | None = None,
    reader: Callable[[Path, naming.NameTemplate], Owned] = _read_from_disk,
) -> LibraryIndex:
    """Index exactly the files named, the way :func:`index_library` indexes a tree,
    for a caller that must not be answered from anything beside them (U113). A
    name that is not an audio file is passed over as the walk passes it.
    """
    shape = template or naming.NameTemplate()
    suffixes = {suffix.lower() for suffix in naming.AUDIO_EXTS}
    grouped: dict[str, list[Owned]] = {}
    by_isrc: dict[str, list[Owned]] = {}
    by_title: dict[str, list[Owned]] = {}
    for path in paths:
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        held = reader(path, shape)
        grouped.setdefault(held.recording, []).append(held)
        by_title.setdefault(fold(held.title), []).append(held)
        if held.isrc:
            by_isrc.setdefault(held.isrc, []).append(held)
    return LibraryIndex(
        by_recording={key: tuple(rows) for key, rows in grouped.items()},
        by_isrc={key: tuple(rows) for key, rows in by_isrc.items()},
        by_title={key: tuple(rows) for key, rows in by_title.items()},
    )


def _spelled_out(folded: str) -> str:
    """A folded name with each word of :data:`_SPELLED_OUT` spelled out and
    the spaces gone, ``luv u`` as ``loveyou``. Read in comparison only."""
    return "".join(_SPELLED_OUT.get(word, word) for word in folded.split())


def _holds_spelling(recording: str) -> bool:
    """Whether a recording token's TITLE holds a word of :data:`_SPELLED_OUT`."""
    _artist, _separator, title = recording.partition("\x1f")
    return any(word in _SPELLED_OUT for word in title.split())


def _spelled_key(recording: str) -> str:
    """A recording token with its title read by :func:`_spelled_out`, the key
    :meth:`LibraryIndex.spelled_alike` looks up; the artist is kept as it folds."""
    artist, separator, title = recording.partition("\x1f")
    return f"{artist}{separator}{_spelled_out(title)}"
