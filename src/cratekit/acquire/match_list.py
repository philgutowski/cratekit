"""The one internal shape every list becomes, and its three readers (U305).

Split from :mod:`cratekit.acquire.match`, which re-exports every public name.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, replace
from typing import Any

from cratekit.acquire.match_identity import (
    _DASH,
    _ORDINAL,
    Recorded,
    Why,
    _credits_in,
    _equivalent_versions,
    _head_of,
    _spellings_of,
    every_question_identity,
    fold,
    key_token,
    listed_title,
    question_identity,
    split_ambiguous,
    split_title,
    title_identity,
    version_identity,
)

# ---------------------------------------------------------------------------
# The one internal shape (R13)
# ---------------------------------------------------------------------------

#: The three list origins this unit reads. Values are stable identifiers that
#: travel in a list document, so they are never display names (R19).
TIDAL = "tidal"
SPOTIFY = "spotify"
TEXT = "text"


@dataclass(frozen=True, slots=True)
class Wanted(Recorded):
    """One track an external list asks for, in the shape everything downstream reads.

    ``ref`` is the source's own identifier and is PROVENANCE, never identity.
    Keying anything on it would make the same record from two services two
    different questions, and a person would answer both.
    """

    artist: str
    title: str
    version: str = ""
    key: str | None = None
    isrc: str | None = None
    origin: str = TEXT
    ref: str = ""
    #: The title as the source spelled it, version and all. Carried because the
    #: tombstone identity hashes a library row's Title column verbatim. Empty only
    #: for a ``Wanted`` built by hand, where :attr:`listed` composes the fallback.
    spelled: str = ""
    #: The other (title, version) reading of a bare one word dash tail, else
    #: ``None``. See :func:`split_ambiguous` and :attr:`readings`.
    other_reading: tuple[str, str] | None = None
    #: Whether the row billed more than one artist, a credit the title does not
    #: show. Read only by :attr:`uncredited_spellings`.
    several_artists: bool = False

    def folded_row(self) -> dict[str, str]:
        """The three fields the exact test compares, so one line in two lists is one question."""
        return {
            "artist": fold(self.artist),
            "title": title_identity(self.title),
            "version": self.version_key,
        }

    @property
    def key_key(self) -> str:
        return key_token(self.key)

    @property
    def listed(self) -> str:
        """The title this track is addressed by, which is the one it arrived as.

        The deletion pass hashes a library row's Title column verbatim, so a split
        and recomposed title misses tombstones silently. Composing from
        :attr:`title`, which has lost its credits, is the hand built fallback only.
        """
        return self.spelled or listed_title(self.title, self.version)

    @property
    def identity(self) -> dict[str, str]:
        """THE TOMBSTONE identity (R36), which is U24's and not this module's."""
        return version_identity(artist=self.artist, title=self.listed)

    @property
    def readings(self) -> tuple[Wanted, ...]:
        """This listing, and the other way its title reads. Conservative first.

        The second entry keeps the same spelled string. It decides only what is
        offered with a question (:func:`_other_reading_the_library_holds`); no
        identifier and no address is derived from it.
        """
        if self.other_reading is None:
            return (self,)
        title, version = self.other_reading
        return (
            self,
            replace(self, title=title, version=version, other_reading=None),
        )

    @property
    def addresses(self) -> tuple[str, ...]:
        """Every title string a library row could carry for this exact version.

        Composed from the spelling's own head (:func:`_head_of`) and only for the
        reading the list spelled, as :func:`_spellings_of` does, since an over
        eager suppression is the cost :func:`tombstone_fold` rejects. Composition
        also requires the head to keep every credit the listing spelled; otherwise
        the listing is addressed only by what it said, a reported miss at worst.
        """
        found: list[str] = []
        spelled = self.listed
        head = _head_of(spelled, self.version) or self.title
        composed: tuple[str, ...] = ()
        if _credits_in(head) == _credits_in(spelled):
            composed = tuple(
                built
                for text in _equivalent_versions(self.version)
                for built in _spellings_of(head, text)
            )
        for spelling in (spelled, *composed):
            if spelling not in found:
                found.append(spelling)
        return tuple(found)

    @property
    def suppression_spellings(self) -> tuple[dict[str, str], ...]:
        """Every identity one version of this recording could have been recorded under.

        A recorder writes one identity; a consulter that misses re-acquires a
        deleted track silently, so it asks under every spelling of the same
        version (:attr:`addresses`). No spelling crosses a version boundary or drops
        a credit, so KTD16 holds.
        """
        seen: list[dict[str, str]] = []
        for title in self.addresses:
            built = version_identity(artist=self.artist, title=title)
            if built not in seen:
                seen.append(built)
        return tuple(seen)

    @property
    def uncredited_spellings(self) -> tuple[dict[str, str], ...]:
        """The identities to ask the companion kind under, which is often none.

        A provider row spelling ``Sun Path`` cannot compose the guest of a deleted
        ``Sun Path (feat. Mira) (Nightwave Remix)``, so the deletion pass records a
        companion under :data:`UNCREDITED_KIND` with credits out. Only a listing
        seen to credit nobody asks, else a deletion of one credited recording would
        withhold another: not a hand built ``Wanted`` (no :attr:`spelled`), and not
        a row billing several artists. A plain deletion writes no companion.
        """
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
            return ()
        return self.suppression_spellings

    def question(self, why: Why) -> dict[str, str]:
        """The review item identity, which is this module's (:func:`question_identity`).

        Separate from :attr:`identity`: a tombstone outlives every list, a question
        is one thing somebody was asked. ``why`` names the question; every value is
        read off the list line, never the library.
        """
        return question_identity(self.artist, self.title, self.version, self.key, why)

    def questions(self) -> tuple[dict[str, str], ...]:
        """Every identity this line can have been asked under, to retire once owned."""
        return every_question_identity(self.artist, self.title, self.version, self.key)


def _field(row: object, name: str, default: Any = None) -> Any:
    """Read ``name`` from a mapping or from an object attribute.

    Both, so documents and live provider objects share one reader rather than a
    second normalization step.
    """
    if isinstance(row, Mapping):
        value = row.get(name, default)
    else:
        value = getattr(row, name, default)
    return default if value is None else value


def row_isrc(row: object) -> Any:
    """The ISRC a provider row carries, as the row spelled it, or None.

    From the row, else its ``external_ids``. Public, so the label genre gate finds
    it in the same places this reader does.
    """
    external = _field(row, "external_ids", {})
    return _field(row, "isrc") or (_field(external, "isrc") if external else None)


def _first_named(entries: object) -> str:
    """The first non-empty name in a list of artists, whatever they are made of.

    A bare string is a list of one, never split on a comma, since a comma is legal
    inside one artist's name and guessing risks a wrong join.
    """
    if isinstance(entries, str):
        return entries.strip()
    if not isinstance(entries, (list, tuple)):
        return ""
    for entry in entries:
        if isinstance(entry, str) and entry.strip():
            return entry.strip()
        name = _field(entry, "name", "")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return ""


def _bills_several(row: object) -> bool:
    """Whether a provider row names more than one artist, counted as :func:`_first_named` reads."""
    for field_name in ("artist", "artists"):
        entries = _field(row, field_name)
        if not isinstance(entries, (list, tuple)):
            continue
        named = [entry for entry in entries if _first_named([entry])]
        if len(named) > 1:
            return True
    return False


def _artist_of(row: object) -> str:
    """The primary artist, from whichever of the four shapes a provider used.

    A list under ``artist`` reads as a list under ``artists`` does, and a bare
    string as a list of one, since an artist read as empty matches nothing or
    gives two recordings one identity.
    """
    single = _field(row, "artist")
    if isinstance(single, str) and single.strip():
        return single.strip()
    if isinstance(single, (list, tuple)):
        return _first_named(single) or _first_named(_field(row, "artists", ()))
    if single is not None:
        name = _field(single, "name", "")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return _first_named(_field(row, "artists", ()))


def read_tidal_tracks(rows: Iterable[object]) -> tuple[Wanted, ...]:
    """Provider playlist rows, where the version is its own field.

    The other readers carry it inside the title; all three fold to one version
    token, so all three ask one question.
    """
    return tuple(
        _from_row(row, origin=TIDAL, position=position)
        for position, row in enumerate(rows, start=1)
    )


def read_spotify_items(items: Iterable[object]) -> tuple[Wanted, ...]:
    """Public playlist items, each wrapping its track; a bare track is accepted too.

    So the choice of endpoint stays out of this module's contract.
    """
    found: list[Wanted] = []
    for position, item in enumerate(items, start=1):
        inner = _field(item, "track")
        found.append(
            _from_row(
                inner if inner is not None else item, origin=SPOTIFY, position=position
            )
        )
    return tuple(found)


def read_text_lines(text: str, *, allow_empty: bool = False) -> tuple[Wanted, ...]:
    """Pasted "Artist - Title" lines. Blank lines and ``#`` comments are skipped.

    A line with no separator is refused, being far more often a bad paste than a
    record by nobody. A list with no track line is refused, since it would read as
    every track owned; ``allow_empty`` is for a document declaring an empty array.
    """
    found: list[Wanted] = []
    for number, raw in enumerate(str(text).splitlines(), start=1):
        line = _ORDINAL.sub("", raw).strip()
        if not line or line.startswith("#"):
            continue
        found.append(_line(line, raw=raw, number=number))
    if not found and not allow_empty:
        raise UnreadableList(
            "this list holds no track lines at all; a blank list and a list whose "
            "every track is owned produce the same empty result and the same "
            "exit status, so it is refused rather than reported clean"
        )
    return tuple(found)


def read_text_rows(rows: Iterable[object], *, allow_empty: bool = True) -> tuple[Wanted, ...]:
    """A list document's ``tracks`` array, where each entry is one line.

    Read entry by entry, so line numbers stay true and an entry holding a line
    break is refused rather than becoming two tracks. Blank and ``#`` rows are
    skipped, so a document and the pasted list it came from read the same.
    """
    found: list[Wanted] = []
    for position, raw in enumerate(rows, start=1):
        text = str(raw)
        if "\n" in text or "\r" in text:
            raise UnreadableList(
                f"track {position} carries a line break, so one entry in the "
                f"array would become two tracks and the list would be longer "
                f"than it declares",
                line=position,
            )
        line = _ORDINAL.sub("", text).strip()
        if not line or line.startswith("#"):
            continue
        found.append(_line(line, raw=text, number=position))
    if not found and not allow_empty:
        raise UnreadableList("this list holds no track lines at all")
    return tuple(found)


def _line(line: str, *, raw: str, number: int) -> Wanted:
    artist, separator, title = line.partition(_DASH)
    if not separator or not artist.strip() or not title.strip():
        raise UnreadableList(
            f"line {number} is not an 'Artist - Title' line: {raw.strip()!r}",
            line=number,
        )
    return _from_row(
        {"artist": artist, "title": title}, origin=TEXT, position=number
    )


#: Origin to the reader that speaks it, so a new source is one entry plus one reader.
READERS: Mapping[str, Callable[[Iterable[object]], tuple[Wanted, ...]]] = {
    TIDAL: read_tidal_tracks,
    SPOTIFY: read_spotify_items,
}


def _from_row(row: object, *, origin: str, position: int) -> Wanted:
    """One row, positively recognized or refused.

    Both an artist and a title are required: either half alone is not unique to a
    recording, so it matches unrelated files and gives two rows one identifier.
    """
    raw_title = _raw_title(row)
    declared = str(_field(row, "version", "")).strip()
    title, embedded = split_title(raw_title)
    isrc = row_isrc(row)
    artist = _artist_of(row)
    if not artist or not title:
        absent = "artist" if title else "title"
        raise UnreadableList(
            f"track {position} names no {absent}, and the half that is left is "
            f"not unique to the recording it means: it matches any file in the "
            f"library agreeing on that half, and two rows differing only in the "
            f"missing one are a single identifier",
            line=position,
        )
    return Wanted(
        artist=artist,
        title=title,
        version=declared or embedded,
        key=(str(_field(row, "key", "")).strip() or None),
        isrc=(str(isrc).strip() or None) if isrc else None,
        origin=origin,
        ref=str(_field(row, "id", "")).strip(),
        # The row's own title with its version in it, composed here from the raw
        # title when the version was declared apart, so a featured credit survives
        # into every address; the matching title has lost its credits.
        spelled=listed_title(raw_title, declared) if declared else raw_title,
        # A declared version leaves nothing ambiguous.
        other_reading=None if declared else split_ambiguous(raw_title),
        several_artists=_bills_several(row),
    )


def _raw_title(row: object) -> str:
    """The title one provider row spells, its version and brackets still in it."""
    return str(_field(row, "title", "") or _field(row, "name", "")).strip()


def listed_names(row: object) -> tuple[str, str, str]:
    """The provider id, the artist and the unsplit title of a row (U213).

    For naming a row :func:`read_row` refused, so one track is set aside rather
    than every playlist refused over it.
    """
    return str(_field(row, "id", "")).strip(), _artist_of(row), _raw_title(row)


def read_row(row: object, *, origin: str, position: int) -> Wanted:
    """One provider shaped row as a ``Wanted``, for a reader outside this module.

    The recognition identifier reads its hits here, so a recognised track and the
    same track pasted fold to one identity. Raises :class:`UnreadableList` for a
    row naming no artist or no title.
    """
    return _from_row(row, origin=origin, position=position)


class UnreadableList(ValueError):
    """A pasted tracklist carries a line this reader will not guess at.

    A plain exception, since this module sits below the failure vocabulary; the
    verb converts it.
    """

    def __init__(self, message: str, *, line: int | None = None) -> None:
        super().__init__(message)
        self.line = line
