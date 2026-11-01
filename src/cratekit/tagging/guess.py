"""Guess a genre for each staged file no catalogue tagged (U172).

WHY THIS EXISTS. Sitting 47 landed 116 tracks and ``tag folder`` gave a genre
to 87. Traxsource and Bandcamp refused every search with a bot check, as they
have since sitting 32, and 27 tracks had no hit on the catalogues that still
answer. Those landed with no genre, so no tree placed them and they waited in
INBOX for a hand tag. Most of them sit beside tracks that say what they are:
the same artist's other tracks, and the playlist on the account they came from,
which the catalogues mostly did tag.

TWO SIGNALS, AS PHILLIP ANSWERED ON 2026-11-01, each a weighted vote:

* the artist's other tracks, in the library and among the folder's own files,
  :data:`ARTIST_WEIGHT` each, the weight ``tag suggest`` gives them;
* each playlist on the account the pass swept that holds the file. A playlist
  casts ONE voice of :data:`PLAYLIST_WEIGHT`, shared out by the genres its
  other members carry, rather than a vote per member, so the 98 tracks of one
  playlist do not drown the three tracks by the file's own artist. Four is two
  artist neighbours: a playlist outweighs one stray track by the artist and
  not three.

A track by the same artist votes once, as the artist's: it is left out of the
playlist's share. The rules that weigh the votes are ``tag suggest``'s
(:func:`cratekit.tagging.suggest.weigh`), so only a genre the active taxonomy
declares is guessed, a word it does not declare still counts toward the total
and lowers the band, and the bands mean what they mean there.

EVERY GUESS IS WRITTEN, whatever its band, Phillip's answer of 2026-11-01:
nothing waits on him, and a wrong guess is put right by hand later. A tie at
the top is written too, to the tied genre the artist's tracks weigh most and
then the first by name, and the item says ``split`` so a person can find it.
A file nothing votes for keeps no genre and is named.

FILL IF EMPTY, as ``tag folder``. A file that carries a genre is never changed,
and a file whose genre could not be read is never treated as blank.

WHAT COULD NOT BE READ IS SAID. A library or a pass that could not be read
gives no votes, and the plan records which, so a file left with no votes
because the library was unreadable is not reported as one nothing knows.

Layer: modules. It opens no database of its own; the verb hands it what it
read.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from fractions import Fraction
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.core import routing, tags, taxonomy
from cratekit.tagging import rows, suggest
from cratekit.tagging.tag import HAS_GENRE, audio_files

#: The name a guess is digested under and the source a written file names.
WORKFLOW = "tag-guess"

#: An artist neighbour's weight, ``tag suggest``'s own.
ARTIST_WEIGHT = suggest.ARTIST_WEIGHT

#: The whole voice of one playlist, shared out by its members' genres.
PLAYLIST_WEIGHT = 4

#: The outcomes, in the order a summary lists them. Every file lands in one.
GUESSED = "guessed"
NO_VOTES = suggest.NO_VOTES
UNWRITTEN = "unwritten"
FILE_UNREADABLE = rows.FILE_UNREADABLE
OUTCOMES: tuple[str, ...] = (GUESSED, NO_VOTES, UNWRITTEN, HAS_GENRE, FILE_UNREADABLE)

#: The outcomes of a file that needed a genre, the candidates.
CANDIDATE_OUTCOMES: tuple[str, ...] = (GUESSED, NO_VOTES, UNWRITTEN)


def artist_key(value: str) -> str:
    """The key two artist names agree on: case and spacing folded, as ``tag suggest``'s."""
    return " ".join((value or "").casefold().split())


# ---------------------------------------------------------------------------
# What the verb reads, handed in
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Staged:
    """One audio file under the folder, as read before the guess.

    ``genre`` is the file's first genre value, or empty. ``readable`` is False
    when the genre could not be read at all, which is not a blank.
    """

    path: Path
    artist: str
    title: str
    genre: str = ""
    readable: bool = True


@dataclass(frozen=True, slots=True)
class Member:
    """One other track of a playlist, as the playlist's share reads it."""

    artist: str
    genre: str
    #: The staged file it is, or None for a track the library already owned.
    path: Path | None = None


@dataclass(frozen=True, slots=True)
class Playlist:
    """One playlist on the account the pass swept, and what it holds of the folder."""

    name: str
    #: The staged files it asked for, which the guess may tag.
    files: tuple[Path, ...]
    #: The tracks it holds that the library already owned, read from their files.
    owned: tuple[Member, ...] = ()


@dataclass(frozen=True, slots=True)
class Signals:
    """What was read beside the folder, and what could not be."""

    #: Each library row's genre by its artist key, or None when unread.
    library: Mapping[str, tuple[str, ...]] | None = None
    #: Why the library could not be read, empty when it was or was not asked.
    library_unread: str = ""
    #: The playlists of the pass that hold any staged file.
    playlists: tuple[Playlist, ...] = ()
    #: The pass the playlists were read for, empty when none was named.
    pass_name: str = ""
    #: Why the pass's playlists could not be read, empty when they were.
    playlists_unread: str = ""


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Item:
    """One staged file and what the guess makes of it."""

    path: Path
    relative: str
    artist: str
    title: str
    outcome: str
    genre: str = ""
    band: str = suggest.NONE
    #: Every word's weight, heaviest first.
    votes: tuple[tuple[str, Fraction], ...] = ()
    #: The genres tied at the top when the band is a split.
    tied: tuple[str, ...] = ()
    #: How many tracks by the artist voted, from the library and from the folder.
    artist_library: int = 0
    artist_folder: int = 0
    #: The playlists whose share voted.
    playlists: tuple[str, ...] = ()
    #: Whether the genre is on the file. False for a report, and for a candidate left.
    written: bool = False
    #: Why the write failed, for an unwritten file.
    note: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "path": self.relative,
            "artist": self.artist,
            "title": self.title,
            "outcome": self.outcome,
            "genre": self.genre,
            "band": self.band,
            "votes": [[word, round(float(weight), 2)] for word, weight in self.votes],
            "tied": list(self.tied),
            "signals": {
                "artist_library": self.artist_library,
                "artist_folder": self.artist_folder,
                "playlists": list(self.playlists),
            },
            "written": self.written,
            "note": self.note,
        }


@dataclass(frozen=True, slots=True)
class GuessPlan:
    """Every staged file sorted into one outcome, and what was read beside them."""

    root: Path
    items: tuple[Item, ...]
    signals: Signals
    #: Each off taxonomy word a staged file carries, and the files carrying it.
    off_taxonomy: Mapping[str, tuple[str, ...]] = field(
        default_factory=lambda: MappingProxyType({})
    )
    report: bool = False

    @property
    def counts(self) -> dict[str, int]:
        counted = dict.fromkeys(OUTCOMES, 0)
        for item in self.items:
            counted[item.outcome] += 1
        return counted

    @property
    def guesses(self) -> tuple[Item, ...]:
        return tuple(item for item in self.items if item.outcome == GUESSED)

    @property
    def before(self) -> int:
        """The files carrying a genre before the guess."""
        return self.counts[HAS_GENRE]

    @property
    def after(self) -> int:
        """The files carrying a genre after it, or that would on a report."""
        return self.before + len(self.guesses)

    def bands(self) -> dict[str, int]:
        counted = dict.fromkeys((*suggest.BANDS, suggest.SPLIT), 0)
        for item in self.guesses:
            counted[item.band] += 1
        return counted

    def identity(self) -> dict[str, Any]:
        """What the digest is taken over: each candidate's guess and the signals read."""
        return {
            "root": str(self.root),
            "items": [
                [item.relative, item.outcome, item.genre, item.band] for item in self.items
            ],
            "library": self.signals.library is not None,
            "pass": self.signals.pass_name,
            "playlists": [one.name for one in self.signals.playlists],
            "report": self.report,
        }


def _share(
    playlist: Playlist,
    candidate: Staged,
    staged: Mapping[Path, Staged],
) -> dict[str, Fraction]:
    """One playlist's voice for one candidate, shared out by its other members' genres.

    The candidate itself and every track by its artist are left out: the
    artist's tracks vote as the artist's, once. A member with no genre gives
    nothing, and a playlist none of whose other members carries a genre has no
    voice.
    """
    own = artist_key(candidate.artist)
    words: Counter[str] = Counter()
    members = [
        Member(artist=one.artist, genre=one.genre, path=path)
        for path in playlist.files
        if path != candidate.path and (one := staged.get(path)) is not None
    ]
    for member in (*members, *playlist.owned):
        if not member.genre or (own and artist_key(member.artist) == own):
            continue
        words[member.genre] += 1
    total = sum(words.values())
    if not total:
        return {}
    return {word: Fraction(PLAYLIST_WEIGHT * count, total) for word, count in words.items()}


def _artist_votes(
    candidate: Staged,
    staged: Sequence[Staged],
    library: Mapping[str, tuple[str, ...]] | None,
) -> tuple[Counter[str], int, int]:
    """The artist's other tracks' votes, and how many came from the library and the folder."""
    own = artist_key(candidate.artist)
    votes: Counter[str] = Counter()
    if not own:
        return votes, 0, 0
    from_library = [word for word in (library or {}).get(own, ()) if word]
    from_folder = [
        one.genre
        for one in staged
        if one.path != candidate.path and one.genre and artist_key(one.artist) == own
    ]
    for word in (*from_library, *from_folder):
        votes[word] += ARTIST_WEIGHT
    return votes, len(from_library), len(from_folder)


def _broken(tied: Iterable[str], artist: Mapping[str, int]) -> str:
    """The tied genre a split is written as: the artist's heaviest, then the first by name."""
    return sorted(tied, key=lambda word: (-artist.get(word, 0), word))[0]


def off_taxonomy(declared: taxonomy.Taxonomy, word: str) -> bool:
    """Whether a word on a file is one this taxonomy has no place of its own for.

    ``tag folder``'s own test (R-650): the last tier of tagging passes the word
    through unchanged and flags it. A bucket's own display reaches that tier
    and is not flagged, since routing files it exactly.
    """
    return bool(word) and routing.suggest_tag(declared, word).off_taxonomy


def plan(
    root: Path,
    staged: Sequence[Staged],
    signals: Signals,
    declared: taxonomy.Taxonomy,
    *,
    report: bool = False,
) -> GuessPlan:
    """Sort every staged file into one outcome and guess each candidate's genre. Pure."""
    by_path = {one.path: one for one in staged}
    holding: dict[Path, list[Playlist]] = {}
    for playlist in signals.playlists:
        for path in playlist.files:
            holding.setdefault(path, []).append(playlist)
    items: list[Item] = []
    off: dict[str, list[str]] = {}
    for one in sorted(staged, key=lambda found: str(found.path)):
        relative = _relative(one.path, root)
        common = {"path": one.path, "relative": relative, "artist": one.artist, "title": one.title}
        if not one.readable:
            items.append(Item(outcome=FILE_UNREADABLE, **common))
            continue
        if one.genre:
            if off_taxonomy(declared, one.genre):
                off.setdefault(one.genre, []).append(relative)
            items.append(Item(outcome=HAS_GENRE, genre=one.genre, **common))
            continue
        artist, from_library, from_folder = _artist_votes(one, staged, signals.library)
        votes: dict[str, Fraction] = {word: Fraction(weight) for word, weight in artist.items()}
        voiced: list[str] = []
        for playlist in holding.get(one.path, ()):
            share = _share(playlist, one, by_path)
            if share:
                voiced.append(playlist.name)
            for word, weight in share.items():
                votes[word] = votes.get(word, Fraction(0)) + weight
        genre, band, tied = suggest.weigh(declared, votes)
        if band == suggest.SPLIT:
            genre = _broken(tied, artist)
        ordered = tuple(sorted(votes.items(), key=lambda entry: (-entry[1], entry[0])))
        items.append(
            Item(
                outcome=GUESSED if genre else NO_VOTES,
                genre=genre,
                band=band,
                votes=ordered,
                tied=tied if band == suggest.SPLIT else (),
                artist_library=from_library,
                artist_folder=from_folder,
                playlists=tuple(voiced),
                **common,
            )
        )
    return GuessPlan(
        root=root,
        items=tuple(items),
        signals=signals,
        off_taxonomy=MappingProxyType({word: tuple(paths) for word, paths in sorted(off.items())}),
        report=report,
    )


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


# ---------------------------------------------------------------------------
# Reading, and the write
# ---------------------------------------------------------------------------


def read_folder(root: Path) -> tuple[Staged, ...]:
    """Every audio file under ``root``, ``tag folder``'s own walk, with its artist and genre."""
    found: list[Staged] = []
    for path in audio_files(root):
        word, outcome = rows._file_word(path)
        found.append(
            Staged(
                path=path,
                artist=(tags.read_tag(path, "artist") or "").strip(),
                title=(tags.read_tag(path, "title") or path.stem).strip(),
                genre=word,
                readable=outcome != rows.FILE_UNREADABLE,
            )
        )
    return tuple(found)


def read_member(path: Path) -> Member | None:
    """A library file a playlist owned, as its share reads it, or None when unread."""
    word, outcome = rows._file_word(path)
    if outcome == rows.FILE_UNREADABLE:
        return None
    return Member(artist=(tags.read_tag(path, "artist") or "").strip(), genre=word)


def library_by_artist(content: Iterable[Any]) -> dict[str, tuple[str, ...]]:
    """Each live row's genre by its artist key, from the binding's own rows.

    A soft deleted row is not a neighbour, and a row with no genre or no artist
    gives nothing. The row's genre, not its file's: a whole library of file
    reads is not paid for one pass, and ``tag rows`` keeps the two agreeing.
    """
    from cratekit.adopt import collection
    from cratekit.write import trees

    found: dict[str, list[str]] = {}
    for row in content:
        if trees.soft_delete_marker(row):
            continue
        genre = collection.genre_of(row).strip()
        key = artist_key(str(getattr(row, "ArtistName", "") or ""))
        if genre and key:
            found.setdefault(key, []).append(genre)
    return {key: tuple(words) for key, words in found.items()}


def write(found: GuessPlan) -> GuessPlan:
    """Write each guess onto its file through the one genre writer, and read it back.

    A file that will not take its genre, or reads back another, is ``unwritten``
    with why, never reported guessed. A report writes nothing and returns the
    plan as it was.
    """
    if found.report:
        return found
    settled: list[Item] = []
    for item in found.items:
        if item.outcome != GUESSED:
            settled.append(item)
            continue
        if not tags.write_genre(item.path, item.genre):
            settled.append(
                replace(item, outcome=UNWRITTEN, note="the file would not take the genre")
            )
            continue
        back, _outcome = rows._file_word(item.path)
        if back != item.genre:
            settled.append(
                replace(
                    item,
                    outcome=UNWRITTEN,
                    note=f"the file reads back {back!r} after the write",
                )
            )
            continue
        settled.append(replace(item, written=True))
    return replace(found, items=tuple(settled))


__all__ = [
    "ARTIST_WEIGHT",
    "CANDIDATE_OUTCOMES",
    "FILE_UNREADABLE",
    "GUESSED",
    "GuessPlan",
    "Item",
    "Member",
    "NO_VOTES",
    "OUTCOMES",
    "PLAYLIST_WEIGHT",
    "Playlist",
    "Signals",
    "Staged",
    "UNWRITTEN",
    "WORKFLOW",
    "artist_key",
    "library_by_artist",
    "off_taxonomy",
    "plan",
    "read_folder",
    "read_member",
    "write",
]
