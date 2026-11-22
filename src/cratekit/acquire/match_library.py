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

#: A short CURATED list of slang and numeral spellings, each folded word
#: beside the folded word it stands for (card 833, chosen by Phillip on
#: 2026-11-15). ``Luv U`` against a held ``Love You`` and ``4 U`` against
#: ``For You`` by one artist share no word and score on their letters alone,
#: 61.5 and 40.0, under :data:`APPROXIMATE_TITLE_FLOOR`, exactly where the
#: unrelated ``Get Out`` against ``Agenou`` sits, so no floor tells them apart
#: and the row read missing and downloaded a record the library holds.
#:
#: READ ONLY WHEN TWO TITLES ARE COMPARED. Nothing is ever spelled out in a
#: token, an identity, a candidate, a review item or anything written: the
#: approximate pass reads a title this way (:func:`_agree` and
#: :meth:`LibraryIndex.spelled_alike`) and nothing else does, so a pair it
#: joins is OFFERED for review, never called owned.
#:
#: DELIBERATELY SHORT, and a word missing from it reads as it always did. A
#: spelling with more than one reading takes the one a title means most
#: (``2`` is ``to``), and ``too`` is read as ``to`` so that ``Luv U 2`` is
#: ``Love You Too``; it is the one real word listed. ``two`` and ``four``
#: were measured and left out: read as ``to`` and ``for`` with the spaces
#: gone, ``Two Day`` became ``Today`` and ``Four Tune`` ``Fortune``
#: (review round one). The spaces are gone because ``2 Nite`` is
#: ``Tonight``, so a few spelled out words can still run together into an
#: unrelated title (``B Side`` and ``Beside``); that costs a question, never
#: ownership, and is the residual this card filed. Not here: ``da`` (``Da
#: Funk`` is not ``The Funk``), ``ya`` (you or yeah), and cardinals (``1``
#: for ``One``), which agree already wherever the titles share another word.
#: ``test_every_listed_spelling_offers_its_spelled_out_title`` drives each
#: entry and ``test_the_word_list_maps_no_word_to_itself_and_only_folded_words``
#: holds its form.
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
    #: THE FILE'S ISRC, FOLDED, or empty when the tag is absent or malformed.
    #: 1691 of 9868 files on the live volume carry none, and those are held by
    #: the credited list rule or by the recording token alone.
    isrc: str = ""
    #: THE FOLDED NAMES THE ARTIST TAG CREDITS, for the credited list rule.
    #: Computed once when the file is read, not on every lookup, because the
    #: index answers one membership question per row over every file under a
    #: title and the inputs never change between rows.
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
    """Ownership as MEMBERSHIP, which is the shape the source repo got right.

    Ownership being a lookup in this index, rather than a filter somebody
    applies at each call site, is what stops a caller forgetting it. A caller
    that forgets a filter gets a plausible answer; a caller that forgets a
    lookup gets nothing and notices.
    """

    by_recording: Mapping[str, tuple[Owned, ...]]
    #: Every file under the folded ISRC it carries. A file with no ISRC tag is
    #: in :attr:`by_recording` and not here.
    by_isrc: Mapping[str, tuple[Owned, ...]] = field(default_factory=dict)
    #: Every file under its folded title alone, the lookup the credited list
    #: rule reads. Membership is decided at the lookup, not here, so one file
    #: is indexed once however many artists its tag credits and ``__len__``
    #: still counts files.
    by_title: Mapping[str, tuple[Owned, ...]] = field(default_factory=dict)
    #: The recordings beside their words sorted, built the first time the
    #: approximate pass asks and kept for the life of the index (U265), so a
    #: library name is sorted once and not once for every wanted row. Built
    #: lazily because a landing or a set build that never reaches the
    #: approximate pass should not pay for it; read it through
    #: :meth:`sorted_recordings`.
    _sorted: tuple[tuple[str, ...], tuple[str, ...]] | None = field(
        default=None, init=False, repr=False, compare=False
    )
    #: The recordings under their artist and their title spelled out (see
    #: :func:`_spelled_key`), built the first time the approximate pass asks
    #: and kept for the life of the index, as :attr:`_sorted` is. Read it
    #: through :meth:`spelled_alike`.
    _spelled: Mapping[str, tuple[str, ...]] | None = field(
        default=None, init=False, repr=False, compare=False
    )

    @property
    def recordings(self) -> tuple[str, ...]:
        return tuple(self.by_recording)

    def sorted_recordings(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """The recordings, and each one's words sorted, position for position.

        The two tuples are taken together so a position the scorer returns in
        the second names the recording at the same position in the first.
        """
        cached = self._sorted
        if cached is None:
            recordings = self.recordings
            cached = (recordings, tuple(_sorted_words(token) for token in recordings))
            object.__setattr__(self, "_sorted", cached)
        return cached

    def versions(self, recording: str) -> tuple[Owned, ...]:
        return self.by_recording.get(recording, ())

    def spelled_alike(self, recording: str) -> tuple[str, ...]:
        """The recordings by this recording's artist whose title is this
        one's once each word of :data:`_SPELLED_OUT` is spelled out and the
        spaces are gone, where one of the two titles holds such a word
        (card 833), in token order.

        AN EXACT LOOKUP BESIDE THE DISCOVERY SCORE, NEVER IN PLACE OF IT. The
        score reads the artist and the title together, and a short slang
        title against its spelled out form falls under its floor for a short
        artist: ``Prince, 4 U`` against ``Prince, For You`` scores 75.0, so
        the title test never saw the pair and the row was downloaded. Read
        only when one title holds a listed word, so a pair the list does not
        join, ``OK`` against ``O.K.`` included, is found by the score alone,
        exactly as before.
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
        """Every file that IS this recording, under two rules in order.

        The recording token first, the exact text rule every caller had. Then
        THE CREDITED LIST RULE: a file whose folded title is this title and
        whose artist tag credits this artist as one whole member. In this
        library the artist tag of a processed file lists every credited
        artist, ``Malive, Tito Azevedo, MRQZ``, where the provider row names
        the primary one, ``Malive``, so the token can never agree and the
        approximate pass either offered the file or scored it under the floor.
        The finding is the residual titled "The match engine never consults the
        ISRC, and a processed file's artist tag lists every credited artist, so
        a quarter of the hearts the library holds read missing or offered",
        cited by title for the reason given under :func:`split_title`.

        Whole names, never substrings: ``Tito`` is not a member of that list.
        The two rules are unioned, token hits first, because a file tagged with
        the one artist and a file tagged with the list are both copies the
        library holds.

        A COMMA IS THE ONLY JOINER, and that is a measured limit rather than an
        oversight. Walked on the live volume on 2026-09-23, 3041 of 9868 artist
        tags carry a comma, and of the tags with no comma 105 carry an
        ampersand, 25 a feat or ft, and 12 an x or an and. The ampersand is a
        band's own name far more often than a join, ``Above & Beyond``, so
        splitting on it would invent members, and the other two are a
        population of 37 a person can answer from the review queue.

        BOTH RULES READ THE TITLE BY :func:`title_identity`. A token and a
        folded title agree for every title that folds to nothing, so a held
        ``🔥`` answered for a wanted ``💧`` by the same artist, the row was
        called owned and never downloaded. Files under the token or the title
        whose title identity differs from the row's are not this recording.
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


#: THE INDEX READER'S MEMORY, one entry per file read cleanly in this process
#: (U249). A sync pass builds one index of the whole music folder per intake
#: job and one more for ``intake missing``, and each used to open every file
#: again although nothing landed between them: (P + 1) x N opens for P
#: playlists over N files, on a volume where one walk of the live library was
#: measured at nine to twelve seconds. Every index is still a FRESH WALK of the
#: folder as it is now, so a file that is gone is absent and a new one is read;
#: only what an unchanged file's tags say is remembered.
#:
#: THE KEY IS NEVER THE PATH ALONE. An entry answers only while the path, the
#: name template it was parsed under and the file's whole stamp agree: size,
#: modification time, change time, inode and device. Size and modification
#: time are what the set builder's cache keys on; the change time is added
#: because ``rsync -a``, ``cp -p`` and ``os.utime`` put the old modification
#: time back over new bytes and none of them can set it, and the inode pair
#: because a rename can put another file of the same size and times under the
#: same name. A field too many costs a read, never a stale answer.
#:
#: THE WINDOW. A file whose modification time is not at least
#: :data:`REMEMBER_WINDOW_NS` older than the moment its entry was made is never
#: answered from memory, because a FAT volume stamps in two second steps and a
#: rewrite inside one step keeps every field above on a volume with no change
#: time of its own. The moment is taken BEFORE the stat and the read, so a
#: write that lands during or after the read either changes the stamp or falls
#: inside the window.
#:
#: ONLY A WHOLE READ IS REMEMBERED. A read that failed anywhere is answered
#: through its one open exactly as the lenient reader always answered it, and
#: remembered never, because a failed read on an external volume can be a
#: moment's I/O error and the next job must be free to read the file properly.
#: A file that cannot be stat'ed is read as before and remembered never.
#:
#: Nothing is kept across processes, so a resume in a new process walks and
#: reads as before. :func:`reset_cache` forgets every entry, and the suite
#: calls it around every test.
_REMEMBERED: dict[tuple[Path, naming.NameTemplate], _Remembered] = {}

#: Two seconds, a FAT volume's modification time step.
REMEMBER_WINDOW_NS = 2_000_000_000

#: The clock an entry's moment is read from, the wall clock a file's
#: modification time is stamped by. A name of its own so a test can hold it.
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
    """What this file is, read once per process while it stays unchanged (U249).

    The index's one reader, so every caller of :func:`index_library` and
    :func:`index_paths` gains and none changes. The rules are the note above
    :data:`_REMEMBERED`; :func:`_read_fresh` is what a miss reads.
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

    Tags first because a tag is what the file itself says; the filename second
    because the library's own naming convention carries the Camelot head and,
    for anything acquired before it was tagged, the artist and title too.
    Neither alone is enough, and an export is neither.

    THE ARTIST AND THE TITLE FALL BACK AS A PAIR, AND A PRESENT VALUE IS NEVER
    DISCARDED. Three rules in precedence order, because two of them alone each
    lose a file. Field by field, a title tag with no artist tag gave an identity
    assembled from two sources matching neither the tags nor the name. As a
    plain pair, an artist tag with no title tag and a filename carrying no
    separator threw the artist away entirely, so the file was found by no list
    naming its artist and a held track reported missing. So: both tags win when
    both are there; otherwise the NAME wins when the name carries both halves;
    otherwise each field takes whatever it has, which is the only case where the
    two sources mix and the only case where mixing beats losing a value.

    THE KEY'S PRECEDENCE RUNS THE OTHER WAY, on purpose. The Camelot head is
    written into the filename by this product, following the library's own
    convention, so for the key the NAME is the library's own statement and the
    tag is whatever some other tool last wrote. For the artist and the title
    there is no such convention and the tag is the file speaking.

    THE TITLE TAG IS STRIPPED OF ITS HEAD THE WAY THE STEM IS. The live library
    writes ``KEY - BPM - `` into the title tag as well as the filename, the live
    system's convention, and 9767 of 9868 files on the volume carry it there. A
    tag taken verbatim put the head inside every recording token, so no
    processed file could match a provider row exactly and the first live
    favourites job resolved 206 hearts as 0 owned over a library holding at
    least 96 of them. The finding is the residual titled "The index takes the
    title tag with its head on, so no processed file resolves owned and every
    heart is offered or missing", cited by title for the reason given under
    :func:`split_title`. A tag that is nothing but a head strips to empty and
    takes the branch an absent tag takes, which is the filename. The head found
    inside the tag carries the key when the stem has none, below the stem's
    head and above the ``initialkey`` tag, which is the opinion
    ``write/naming_cli.py`` already holds about the same bytes: the first draft
    read nothing off the tag's head, and the review drove a file that indexed
    with no key until a rename padded the same head into its filename, so one
    file gave two answers depending on whether ``naming apply`` had run.
    """
    stem = path.stem
    head = naming.parse_head(stem, template=template) or {}
    body = naming.strip_heads(stem, template=template)
    artist_part, separator, title_part = body.partition(template.segment_sep)
    if not separator:
        artist_part, title_part = "", body

    # ONE CONTAINER OPEN FOR THE FOUR FIELDS. Three opens per file was the shape
    # the residual titled "The index reader opens every container three times,
    # and the walk is the library" recorded, and the ISRC is not a fourth.
    # The lenient answer, and whether any part of it failed, through that one
    # open: a failed read is indexed as it always was and never remembered.
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

    ``reader`` is injected so a test can drive the grouping without synthesizing
    a valid container for every fixture. Its default is the real disk reader, so
    the production path is the one that runs unless somebody deliberately
    replaces it; a default that read nothing would make an empty library and a
    forgotten argument look identical.
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
    """Index exactly the files named, the way :func:`index_library` indexes a tree.

    For a caller that knows which files it means and must not be answered from
    anything else beside them: a landing ties its planned files to the rows that
    asked for them before they move (U113), and download staging also holds the
    partial downloads of attempts that never finished. A name that is not an
    audio file, or not a file, is passed over exactly as the walk passes it.
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
    """A recording token with its title read by :func:`_spelled_out`, what
    :meth:`LibraryIndex.spelled_alike` looks a recording up by. The artist is
    kept as it folds, so the lookup is the same artist always."""
    artist, separator, title = recording.partition("\x1f")
    return f"{artist}{separator}{_spelled_out(title)}"
