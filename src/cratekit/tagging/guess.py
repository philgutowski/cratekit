"""Guess a genre for each staged file no catalogue tagged (U172).

Files the catalogues had no hit for landed with no genre, so no tree placed
them, though most sit beside tracks that say what they are.

TWO SIGNALS, AS PHILLIP ANSWERED ON 2026-11-01, each a weighted vote: the
artist's other tracks, in the library and the folder, :data:`ARTIST_WEIGHT`
each, ``tag suggest``'s weight; and each account playlist of the pass holding
the file, ONE voice of :data:`PLAYLIST_WEIGHT` shared out by its other members'
genres, so a long playlist does not drown the artist's own tracks. A track by
the same artist votes once, as the artist's. The votes are weighed by
:func:`cratekit.tagging.suggest.weigh`, so only a declared genre is guessed.

EVERY GUESS IS WRITTEN, whatever its band (2026-11-01); a tie is written as the
tied genre the artist weighs most, then the first by name, and says ``split``.
A file nothing votes for keeps no genre and is named. FILL IF EMPTY, and an
unreadable genre is never blank. A library or pass that could not be read
gives no votes and the plan records which.

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
from cratekit.tagging.tag import relative as relative_to

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


@dataclass(frozen=True, slots=True)
class Staged:
    """One audio file under the folder, as read before the guess. ``genre`` is
    its first genre value; ``readable`` False when it could not be read at all."""

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
    """One playlist's voice for one candidate, shared out by its other members'
    genres, the candidate and its artist's tracks left out."""
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


def band_of(weight: Fraction, total: Fraction) -> str:
    """``tag suggest``'s band for a share, compared exactly. Pure.

    :func:`cratekit.tagging.suggest.band_of`'s two conditions, read exactly: a
    playlist's share makes the votes Fractions, and a float compare puts an exact
    eighty percent one band low, so the bound is read as the decimal it is.
    """
    if total <= 0 or weight <= 0:
        return suggest.NONE
    share = Fraction(weight) / Fraction(total)
    for name, least, votes in suggest._BOUNDS:
        if share >= Fraction(str(least)) and total >= votes:
            return name
    return suggest.LOW


def off_taxonomy(declared: taxonomy.Taxonomy, word: str) -> bool:
    """Whether a word on a file is one this taxonomy has no place of its own for,
    ``tag folder``'s own test (R-650)."""
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
        relative = relative_to(one.path, root)
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
        if band in suggest.BANDS:
            band = band_of(votes[genre], sum(votes.values()))
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
    """Each live row's genre by its artist key, from the binding's own rows: the
    row's, not the file's, so no library of file reads is paid for one pass."""
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
    """Write each guess onto its file through the one genre writer, and read it
    back; a file that does not take it is ``unwritten`` with why. A report writes
    nothing."""
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
    "band_of",
    "library_by_artist",
    "off_taxonomy",
    "plan",
    "read_folder",
    "read_member",
    "write",
]
