"""U16: three-state matching, and the one internal shape every intake becomes.

R11 in one sentence: an external list resolves each track to matched, needs
review, or missing, and a version difference is never silently treated as
matched. The system this replaces has two comma separated files, owned and
missing, and no representation for the middle state at all, so a remix, an
extended cut, a live take, and a clean edit all landed in "owned" and the user
found out at the gig.

FOUR PROPERTIES, and each one answers a specific way that failed.

1. **Ownership is on-disk truth.** The index is built by walking the library's
   own music tree, reading each file's tags and falling back to its filename.
   Never an export. An export is a snapshot of what rekordbox believed at the
   moment somebody pressed a button, and the source system read a stale one and
   reported an owned track unowned, then went and acquired it again.

2. **A fuzzy or substring hit is a DISCOVERY heuristic and never an identity.**
   Every approximate hit resolves to needs review with the difference named. The
   scoring here can be as generous as it likes precisely because a generous
   score costs one question rather than one wrong join.

3. **A version is part of the identity.** ``recording_token`` folds the artist
   and title; ``version_token`` folds the qualifier separately. Two records that
   agree on the recording and disagree on the version are a QUESTION, and the
   question carries what differs, so a person answers "is your extended mix the
   record this list means" rather than "here are two strings".

4. **One internal shape.** Three readers, one ``Wanted``. A list that arrived as
   a provider playlist, as a public Spotify playlist, or as pasted text produces
   the same match result and, more importantly, the same review item identity,
   so a question answered against one source is not asked again when the same
   list arrives through another. Acquisition is source-agnostic once matched
   (R13), and this module is where "once matched" is made true.

**WHERE THE FETCH IS NOT.** Nothing here opens a socket. The readers take rows
that somebody already has: a provider client's track objects, a public playlist
API's items, or lines a person pasted. R13's URL fetching belongs to the intake
verbs, which own provider sessions and pagination; putting it here would make
this module untestable without an account and would give the product two places
that page a playlist.

**THE SUPPRESSED STATE, and why it is not a fourth array.** R36 says an
acquisition source skips a tombstoned version and REPORTS the suppression rather
than omitting it silently. R11 says the match is exactly three states, and the
``match`` payload surface has been closed at three arrays since U5 reserved it.
Those are not in conflict once the two questions are told apart: matched, needs
review, and missing describe the MATCH, and suppression describes what
acquisition may do with the result. A suppressed version is therefore reported
on its own channel by the verb, is in none of the three arrays, and so is
skipped by anything that reads ``missing`` to decide what to go and get. Putting
it in ``missing`` would count it missing, which is what the brief forbids by
name; dropping it would be the silent omission R36 forbids by name.

**ORDER: on-disk truth first, then suppression.** A version the library actually
holds is matched even if a tombstone stands over it, because property 1 says the
disk wins and a tombstone over a held file is a stale record rather than a fact
about the library. The verb reports that disagreement instead of hiding it. Only
a version the library does NOT hold is checked against the tombstones, which is
exactly the case R36 is about: something is about to be acquired.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from cratekit.core import naming, tags

# ---------------------------------------------------------------------------
# The states, and the reasons
# ---------------------------------------------------------------------------


class MatchState(StrEnum):
    """R11's three states, plus what suppression is.

    The three payload values are spelled exactly as the ``match`` surface's
    field names, so the payload is DERIVED from this enum rather than written a
    second time. A fourth state added here without a payload decision fails
    ``PAYLOAD_STATES`` below rather than silently widening the envelope.
    """

    MATCHED = "matched"
    NEEDS_REVIEW = "needs_review"
    MISSING = "missing"
    #: Not one of R11's three. See the module docstring: this describes what
    #: acquisition may do, not how the match resolved.
    SUPPRESSED = "suppressed"


#: The three states the ``match`` payload carries, in the order it carries them.
#: A consumer of the payload derives its keys from here; nothing spells them
#: twice.
PAYLOAD_STATES: tuple[MatchState, ...] = (
    MatchState.MATCHED,
    MatchState.NEEDS_REVIEW,
    MatchState.MISSING,
)


class Why(StrEnum):
    """Why a track landed where it did. Stable slugs, never sentences.

    A reason is read by the next stage and by a person, so it is an identifier
    (R19). The sentence a person sees is rendered from it, and rewording that
    sentence must not change what a decision was recorded against.
    """

    #: The library holds this exact version.
    EXACT = "exact"
    #: A person already said one of the owned versions is this record.
    VERDICT_ACCEPTED = "verdict-accepted"
    #: A person already said none of them is.
    VERDICT_REJECTED = "verdict-rejected"
    #: The recording is owned, the version is not. R11's whole point.
    VERSION_DIFFERS = "version-differs"
    #: Only a scored, approximate hit on the recording. Discovery, never identity.
    TITLE_APPROXIMATE = "title-approximate"
    #: Same Camelot number, different letter: the relative major or minor. It
    #: looks like agreement to anything comparing wheel positions, which is why
    #: it gets a slug of its own rather than folding into the one below.
    KEY_RELATIVE = "key-relative"
    #: The two keys disagree outright.
    KEY_DIFFERS = "key-differs"
    #: Nothing in the library resembles it.
    NOT_IN_LIBRARY = "not-in-library"
    #: A tombstone stands over this exact version (R36).
    TOMBSTONED = "tombstoned"
    #: A recorded verdict names a candidate the library no longer offers. The
    #: decision cannot be applied and this tool will not clear somebody's
    #: verdict for them, so the track is presented again with the item named.
    CANDIDATE_GONE = "candidate-gone"
    #: An acceptance that names no candidate while several are on offer. "One of
    #: these is the record" does not say which, and guessing is the silent join
    #: this whole unit exists to prevent.
    VERDICT_UNSPECIFIC = "verdict-unspecific"


#: The kind a version-match question is offered under. An identifier, normalized
#: by the queue on the way in, and the same one every producer of this question
#: must use or two spellings become two items for one candidate.
QUESTION_KIND = "version-match"

#: The kind a tombstone is recorded under. DECLARED HERE because this module
#: owns the version identity that both the tombstone and the question address,
#: and a deletion pass that spells the kind or the identity differently records
#: a suppression this module can never find. The pending register carries that
#: obligation against the unit that writes tombstones.
TOMBSTONE_KIND = "version"

#: The score at or above which an approximate recording hit is worth SHOWING a
#: person. Deliberately generous: everything above it becomes a question and
#: nothing above it becomes a match, so the cost of a low floor is noise in the
#: queue and the cost of a high one is a track reported missing that the library
#: already holds under a slightly different spelling.
APPROXIMATE_FLOOR = 82

#: How many approximate recordings are offered for one wanted track. A person
#: choosing between five candidates is choosing; a person choosing between forty
#: is scrolling.
APPROXIMATE_LIMIT = 5


# ---------------------------------------------------------------------------
# Folding: one spelling per value, so one candidate is one decision
# ---------------------------------------------------------------------------

_MARKS = re.compile(r"[^\w\s]", re.UNICODE)
_RUNS = re.compile(r"\s+")

#: Trailing bracketed groups that name a PERFORMER rather than a version. They
#: come off the title because two listings of one record disagree constantly
#: about whether the guest is in the title or in the artist field, and they are
#: not folded into the version because a guest vocalist is not an edit.
_CREDIT_PREFIXES: tuple[str, ...] = ("feat ", "feat. ", "ft ", "ft. ", "featuring ", "with ")

#: Version qualifiers that mean "no qualifier at all". A record listed as the
#: original mix and the same record listed with nothing are one version, and
#: treating them as two asks a person to confirm a track against itself.
#: Deliberately short. "Album version" is NOT here: on plenty of releases it is
#: a genuinely different cut from the single, and folding it would silently join
#: two versions, which is the exact defect this unit exists to remove.
_NULL_VERSIONS: frozenset[str] = frozenset({"original", "original mix", "original version"})

#: A leading list ordinal in pasted text: "1. ", "12) ", "03 - " is NOT included
#: because a leading number followed by a dash is indistinguishable from an
#: artist whose name is a number.
_ORDINAL = re.compile(r"^\s*\d{1,3}\s*[.)]\s+")

#: One trailing bracketed group. Applied repeatedly, right to left, so
#: "Title (feat. X) (Someone Remix)" yields the remix as the version and drops
#: the credit.
_TRAILING_GROUP = re.compile(r"\s*[(\[]([^()\[\]]*)[)\]]\s*$")


def fold(text: object) -> str:
    """One canonical spelling of a value, for hashing and for comparison.

    Case, accents, and punctuation come off; word boundaries stay. That last
    part is the line: folding punctuation to NOTHING would make "Re Mix" and
    "Remix" the same token and would make two different titles collide, and a
    collision here silently merges two candidates onto one decision, which is
    the failure that cannot be noticed afterwards.
    """
    decomposed = unicodedata.normalize("NFKD", str(text))
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return _RUNS.sub(" ", _MARKS.sub(" ", stripped.casefold())).strip()


def split_version(title: str) -> tuple[str, str]:
    """Split a listing's title into (title, version qualifier).

    Only TRAILING bracketed groups are read. A dash-introduced qualifier is
    deliberately not parsed: titles contain dashes, and a parser that guessed
    would split "Sun - Rise" into a title and a version and then ask a person
    about a record that does not exist.
    """
    remaining = str(title).strip()
    qualifiers: list[str] = []
    while True:
        found = _TRAILING_GROUP.search(remaining)
        if found is None:
            break
        inside = found.group(1).strip()
        remaining = remaining[: found.start()].strip()
        folded = fold(inside)
        if any(folded.startswith(fold(prefix)) for prefix in _CREDIT_PREFIXES):
            continue
        if inside:
            qualifiers.append(inside)
    return remaining, " ".join(reversed(qualifiers))


def recording_token(artist: str, title: str) -> str:
    """The folded identity of a RECORDING, version excluded.

    Artist and title are joined through a separator that folding can never
    produce, so an artist whose name ends in the first word of a title cannot
    collide with a different split of the same characters.
    """
    return f"{fold(artist)}\x1f{fold(title)}"


def version_token(version: str) -> str:
    """The folded identity of a VERSION, with the no-op qualifiers folded away."""
    folded = fold(version)
    return "" if folded in _NULL_VERSIONS else folded


def version_identity(artist: str, title: str, version: str) -> dict[str, str]:
    """What addresses one exact version of one recording, everywhere.

    ONE function rather than one per consumer, because the review item asking
    about a version and the tombstone suppressing it must resolve to the same
    thing. Two spellings of this mapping means a deletion recorded under one and
    consulted under the other suppresses nothing, and nobody finds out until a
    deleted version comes back.

    The values are plain text and are already folded, which matters one layer
    up: the queue hashes an identity and distinguishes ``7`` from ``"7"``, so a
    producer handing it raw values of mixed types manufactures two items for one
    candidate.
    """
    return {
        "recording": recording_token(artist, title),
        "version": version_token(version),
    }


def _digest(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# The one internal shape (R13)
# ---------------------------------------------------------------------------

#: The three list origins this unit reads. Values are stable identifiers that
#: travel in a list document, so they are never display names (R19).
TIDAL = "tidal"
SPOTIFY = "spotify"
TEXT = "text"


@dataclass(frozen=True, slots=True)
class Wanted:
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

    @property
    def recording(self) -> str:
        return recording_token(self.artist, self.title)

    @property
    def version_key(self) -> str:
        return version_token(self.version)

    @property
    def identity(self) -> dict[str, str]:
        return version_identity(self.artist, self.title, self.version)


def _field(row: object, name: str, default: Any = None) -> Any:
    """Read ``name`` from a mapping or from an object attribute.

    Both, because the same reader has to serve a list document that was written
    to disk and a provider client's live track objects. Supporting only the
    first would make the intake verbs convert every object before calling this,
    which is a second normalization step and therefore a second place for the
    shapes to disagree.
    """
    if isinstance(row, Mapping):
        value = row.get(name, default)
    else:
        value = getattr(row, name, default)
    return default if value is None else value


def _artist_of(row: object) -> str:
    """The primary artist, from whichever of the three shapes a provider used."""
    single = _field(row, "artist")
    if isinstance(single, str) and single.strip():
        return single.strip()
    if single is not None and not isinstance(single, (list, tuple)):
        name = _field(single, "name", "")
        if isinstance(name, str) and name.strip():
            return name.strip()
    listed = _field(row, "artists", ())
    if isinstance(listed, (list, tuple)):
        for entry in listed:
            if isinstance(entry, str) and entry.strip():
                return entry.strip()
            name = _field(entry, "name", "")
            if isinstance(name, str) and name.strip():
                return name.strip()
    return ""


def read_tidal_tracks(rows: Iterable[object]) -> tuple[Wanted, ...]:
    """Provider playlist rows, where the version is its OWN field.

    This is the shape that makes the three readers worth having. The provider
    carries "Someone Remix" beside the title; the public playlist API below
    carries it inside the title; pasted text carries it inside the title too.
    All three fold to one version token, so all three ask one question.
    """
    return tuple(_from_row(row, origin=TIDAL) for row in rows)


def read_spotify_items(items: Iterable[object]) -> tuple[Wanted, ...]:
    """Public playlist items, each of which wraps the track it holds.

    A row that is already a track is accepted too. The wrapper is what the
    playlist endpoint returns and the bare track is what the tracks endpoint
    returns, and refusing one of them would put the choice of endpoint into this
    module's contract.
    """
    found: list[Wanted] = []
    for item in items:
        inner = _field(item, "track")
        found.append(_from_row(inner if inner is not None else item, origin=SPOTIFY))
    return tuple(found)


def read_text_lines(text: str) -> tuple[Wanted, ...]:
    """Pasted "Artist - Title" lines. Blank lines and ``#`` comments are skipped.

    A line that carries no separator is REFUSED rather than read as a title with
    no artist. A tracklist with one malformed line is far more often a tracklist
    somebody pasted wrong than a record by nobody, and reading it as anonymous
    would put a track in the queue that no source can ever match.
    """
    found: list[Wanted] = []
    for number, raw in enumerate(str(text).splitlines(), start=1):
        line = _ORDINAL.sub("", raw).strip()
        if not line or line.startswith("#"):
            continue
        artist, separator, title = line.partition(" - ")
        if not separator or not artist.strip() or not title.strip():
            raise UnreadableList(
                f"line {number} is not an 'Artist - Title' line: {raw.strip()!r}",
                line=number,
            )
        found.append(_from_row({"artist": artist, "title": title}, origin=TEXT))
    return tuple(found)


#: Origin to the reader that speaks it. A list document names its origin and the
#: reader is looked up here, so adding a fourth source is one entry plus one
#: reader rather than a branch somebody has to find.
READERS: Mapping[str, Callable[[Iterable[object]], tuple[Wanted, ...]]] = {
    TIDAL: read_tidal_tracks,
    SPOTIFY: read_spotify_items,
}


def _from_row(row: object, *, origin: str) -> Wanted:
    raw_title = str(_field(row, "title", "") or _field(row, "name", "")).strip()
    declared = str(_field(row, "version", "")).strip()
    title, embedded = split_version(raw_title)
    external = _field(row, "external_ids", {})
    isrc = _field(row, "isrc") or (_field(external, "isrc") if external else None)
    return Wanted(
        artist=_artist_of(row),
        title=title,
        version=declared or embedded,
        key=(str(_field(row, "key", "")).strip() or None),
        isrc=(str(isrc).strip() or None) if isrc else None,
        origin=origin,
        ref=str(_field(row, "id", "")).strip(),
    )


class UnreadableList(ValueError):
    """A pasted tracklist carries a line this reader will not guess at.

    A plain exception rather than a structured cause, because this module sits
    below the layer that owns the failure vocabulary. The verb converts it, in
    the one place that is allowed to know what a remediation looks like.
    """

    def __init__(self, message: str, *, line: int | None = None) -> None:
        super().__init__(message)
        self.line = line


# ---------------------------------------------------------------------------
# The library, indexed from what is on the disk
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Owned:
    """One audio file the library holds, and what the disk says it is."""

    path: Path
    artist: str
    title: str
    version: str
    key: str | None

    @property
    def recording(self) -> str:
        return recording_token(self.artist, self.title)

    @property
    def version_key(self) -> str:
        return version_token(self.version)


@dataclass(frozen=True, slots=True)
class LibraryIndex:
    """Ownership as MEMBERSHIP, which is the shape the source repo got right.

    Ownership being a lookup in this index, rather than a filter somebody
    applies at each call site, is what stops a caller forgetting it. A caller
    that forgets a filter gets a plausible answer; a caller that forgets a
    lookup gets nothing and notices.
    """

    by_recording: Mapping[str, tuple[Owned, ...]]

    @property
    def recordings(self) -> tuple[str, ...]:
        return tuple(self.by_recording)

    def versions(self, recording: str) -> tuple[Owned, ...]:
        return self.by_recording.get(recording, ())

    def __len__(self) -> int:
        return sum(len(held) for held in self.by_recording.values())


def _read_from_disk(path: Path, template: naming.NameTemplate) -> Owned:
    """What this file is, from its tags first and its filename second.

    Tags first because a tag is what the file itself says; the filename second
    because the library's own naming convention carries the Camelot head and,
    for anything acquired before it was tagged, the artist and title too.
    Neither alone is enough, and an export is neither.
    """
    stem = path.stem
    head = naming.parse_head(stem, template=template) or {}
    body = naming.strip_heads(stem, template=template)
    artist_part, separator, title_part = body.partition(template.segment_sep)
    if not separator:
        artist_part, title_part = "", body

    artist = str(tags.read_tag(path, "artist") or artist_part).strip()
    tagged_title = tags.read_tag(path, "title")
    title, version = split_version(str(tagged_title or title_part))

    written_key = head.get("key")
    key = written_key or tags.read_tag(path, "initialkey")
    return Owned(
        path=path,
        artist=artist,
        title=title,
        version=version,
        key=str(key).strip() if key else None,
    )


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
    shape = template or naming.NameTemplate()
    suffixes = {suffix.lower() for suffix in naming.AUDIO_EXTS}
    grouped: dict[str, list[Owned]] = {}
    if root.is_dir():
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            held = reader(path, shape)
            grouped.setdefault(held.recording, []).append(held)
    return LibraryIndex(by_recording={key: tuple(rows) for key, rows in grouped.items()})


# ---------------------------------------------------------------------------
# Keys: the relative major and minor trap
# ---------------------------------------------------------------------------


def key_disagreement(wanted: str | None, owned: str | None) -> Why | None:
    """How two Camelot codes disagree, or None when there is nothing to say.

    ABSENCE IS NOT DISAGREEMENT. A listing with no key and a library file with
    one agree about everything they both have an opinion on, and reporting that
    as a conflict would put most of a real playlist in the queue.

    The relative case gets its own answer because it is the one that looks like
    agreement: 8A and 8B share a wheel position and share every note, so a check
    comparing wheel numbers calls them the same key, and the two are a minor and
    a major recording of the same material. Picking one silently is what the
    plan's own scenario forbids.
    """
    if not wanted or not owned:
        return None
    left = naming.parse_camelot(wanted)
    right = naming.parse_camelot(owned)
    if left is None or right is None:
        return None
    if left == right:
        return None
    return Why.KEY_RELATIVE if left[0] == right[0] else Why.KEY_DIFFERS


# ---------------------------------------------------------------------------
# One resolved track
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Candidate:
    """One owned VERSION offered as the answer to a version question.

    ADDRESSED BY THE VERSION, NOT BY THE FILE. Two files that are the same
    version, a lossless copy and a marked lossy one, are one answer to "is the
    record you want the one I hold as this version", so they are one candidate
    carrying two paths. Addressing by path instead would ask the same question
    twice and would orphan the decision the first time somebody renames a file.

    The artist and title travel with it because an approximate hit offers
    candidates from a DIFFERENT recording, and a person shown only a version
    qualifier cannot tell which record they are being asked about.
    """

    candidate_id: str
    artist: str
    title: str
    version: str
    key: str | None
    difference: Why
    paths: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.candidate_id,
            "artist": self.artist,
            "title": self.title,
            "version": self.version,
            "key": self.key,
            "difference": str(self.difference),
            "paths": list(self.paths),
        }


@dataclass(frozen=True, slots=True)
class TrackMatch:
    """One wanted track, the state it resolved to, and why.

    ``match_id`` is derived from the recording and the version and from nothing
    else, which is what makes the same list from three sources produce the same
    rows. The provider's own reference travels under ``wanted`` as provenance.
    """

    wanted: Wanted
    state: MatchState
    why: Why
    candidates: tuple[Candidate, ...] = ()
    paths: tuple[str, ...] = ()
    item_id: str | None = None
    suppression_id: str | None = None

    @property
    def match_id(self) -> str:
        return f"mt_{_digest(self.wanted.recording, self.wanted.version_key)}"

    @property
    def identity(self) -> dict[str, str]:
        return self.wanted.identity

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.match_id,
            "state": str(self.state),
            "why": str(self.why),
            "artist": self.wanted.artist,
            "title": self.wanted.title,
            "version": self.wanted.version,
            "key": self.wanted.key,
            "candidates": [candidate.to_json() for candidate in self.candidates],
            "paths": list(self.paths),
            "review_item": self.item_id,
            "suppression": self.suppression_id,
            # PROVENANCE, and the only key that may differ between the same list
            # read from two services. Everything above it is derived from the
            # recording, which is what "identical match results" means.
            "source": {"origin": self.wanted.origin, "ref": self.wanted.ref},
        }


@dataclass(frozen=True, slots=True)
class MatchResult:
    """Every track in one list, resolved.

    The payload is DERIVED from ``PAYLOAD_STATES`` rather than assembled by
    hand, so the three arrays cannot fall out of step with the states, and a
    fourth state cannot arrive in the envelope without a decision.
    """

    matches: tuple[TrackMatch, ...]

    def __len__(self) -> int:
        return len(self.matches)

    def of(self, state: MatchState) -> tuple[TrackMatch, ...]:
        return tuple(found for found in self.matches if found.state is state)

    @property
    def suppressed(self) -> tuple[TrackMatch, ...]:
        return self.of(MatchState.SUPPRESSED)

    def payload(self) -> dict[str, list[dict[str, Any]]]:
        return {
            str(state): [found.to_json() for found in self.of(state)]
            for state in PAYLOAD_STATES
        }


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------


def _candidates_for(wanted: Wanted, owned: Sequence[Owned]) -> tuple[Candidate, ...]:
    """Group owned files into one candidate per version, naming what differs.

    GROUPED BY RECORDING AND VERSION, not by version alone. An approximate pass
    offers files from several different recordings, and two of them with no
    version qualifier would collapse onto one candidate carrying both sets of
    paths, so a person accepting one of them would be accepting the other too.
    """
    grouped: dict[tuple[str, str], list[Owned]] = {}
    for held in owned:
        grouped.setdefault((held.recording, held.version_key), []).append(held)
    built: list[Candidate] = []
    for recording, version_key in sorted(grouped):
        rows = grouped[(recording, version_key)]
        first = rows[0]
        if recording != wanted.recording:
            difference = Why.TITLE_APPROXIMATE
        elif version_key != wanted.version_key:
            difference = Why.VERSION_DIFFERS
        else:
            difference = key_disagreement(wanted.key, first.key) or Why.EXACT
        built.append(
            Candidate(
                candidate_id=f"cd_{_digest(recording, version_key)}",
                artist=first.artist,
                title=first.title,
                version=first.version,
                key=first.key,
                difference=difference,
                paths=tuple(str(row.path) for row in rows),
            )
        )
    return tuple(built)


def _approximate(wanted: Wanted, index: LibraryIndex) -> tuple[Owned, ...]:
    """Recordings that merely RESEMBLE the wanted one. Discovery, never identity.

    Scored on the folded recording token, so the artist and the title are both
    in the comparison: a title alone matches every cover version and every
    unrelated record that happens to share a common word.

    The scorer is imported here rather than at module scope because the parser
    imports every landed verb's module on every invocation, ``crate --help``
    included, and this is the only function in the unit that needs it. A cheap
    help screen is a property U5 states about the dispatcher, and paying for a
    scoring library to print one would take it away.
    """
    if not index.by_recording:
        return ()
    from rapidfuzz import fuzz, process

    found = process.extract(
        wanted.recording,
        index.recordings,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=APPROXIMATE_FLOOR,
        limit=APPROXIMATE_LIMIT,
    )
    return tuple(held for token, _score, _position in found for held in index.versions(token))


def resolve_one(
    wanted: Wanted,
    index: LibraryIndex,
    *,
    suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str],
) -> TrackMatch:
    """Resolve one wanted track against the library and the tombstones.

    ``suppresses`` HAS NO DEFAULT, deliberately. A default of "nothing is
    suppressed" is the permissive answer, and a caller that forgot to pass the
    tombstone store would re-acquire exactly what somebody deleted on purpose
    while every test stayed green. The same argument the soft-delete marker
    already lost once in this repository.
    """
    owned = index.versions(wanted.recording)
    exact = [held for held in owned if held.version_key == wanted.version_key]

    if exact:
        disagreement = key_disagreement(wanted.key, exact[0].key)
        if disagreement is None:
            return TrackMatch(
                wanted=wanted,
                state=MatchState.MATCHED,
                why=Why.EXACT,
                paths=tuple(str(held.path) for held in exact),
            )
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=disagreement,
            candidates=_candidates_for(wanted, exact),
        )

    identity = wanted.identity
    if suppresses(TOMBSTONE_KIND, identity):
        return TrackMatch(
            wanted=wanted,
            state=MatchState.SUPPRESSED,
            why=Why.TOMBSTONED,
            suppression_id=suppression_id(TOMBSTONE_KIND, identity),
        )

    if owned:
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=Why.VERSION_DIFFERS,
            candidates=_candidates_for(wanted, owned),
        )

    near = _approximate(wanted, index)
    if near:
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=Why.TITLE_APPROXIMATE,
            candidates=_candidates_for(wanted, near),
        )

    return TrackMatch(wanted=wanted, state=MatchState.MISSING, why=Why.NOT_IN_LIBRARY)


def resolve_all(
    wanted: Sequence[Wanted],
    index: LibraryIndex,
    *,
    suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str],
) -> MatchResult:
    """Resolve a whole list, preserving its order inside each state."""
    return MatchResult(
        matches=tuple(
            resolve_one(
                one, index, suppresses=suppresses, suppression_id=suppression_id
            )
            for one in wanted
        )
    )


def apply_verdict(
    found: TrackMatch,
    *,
    accepted: bool | None,
    option: str | None,
    item_id: str,
) -> TrackMatch:
    """Fold a recorded decision into a track that would otherwise need review.

    THREE ANSWERS, NOT TWO. ``accepted`` is None for an item nobody has decided
    AND for an item carrying a verdict this build cannot read, and both of those
    leave the track where it is: still a question, still answerable. A verdict
    the reader does not recognize must never freeze an item out of every route,
    because the route out of a wrong decision is to clear it and a frozen item
    cannot be reached to clear.

    A decision naming a candidate the library no longer offers is NOT applied.
    Ownership is on-disk truth, so reporting a track matched on the strength of
    a verdict about a file that is gone would be reporting ownership of nothing.
    The track comes back as a question naming the item, because clearing
    somebody's verdict is their act and not this tool's.

    AN ACCEPTANCE THAT NAMES NO CANDIDATE is applied only when there is exactly
    one to name. The queue allows a verdict with no option, so with several
    candidates on offer "accepted" says the library has the record and does not
    say which version, and taking all of them would report the library holding
    three copies of one record on the strength of one unspecific yes.
    """
    if accepted is None:
        return TrackMatch(
            wanted=found.wanted,
            state=found.state,
            why=found.why,
            candidates=found.candidates,
            paths=found.paths,
            item_id=item_id,
        )
    if not accepted:
        return TrackMatch(
            wanted=found.wanted,
            state=MatchState.MISSING,
            why=Why.VERDICT_REJECTED,
            candidates=found.candidates,
            item_id=item_id,
        )
    if option is None:
        chosen = list(found.candidates) if len(found.candidates) == 1 else []
        unresolved = Why.VERDICT_UNSPECIFIC
    else:
        chosen = [c for c in found.candidates if c.candidate_id == option]
        unresolved = Why.CANDIDATE_GONE
    if not chosen:
        return TrackMatch(
            wanted=found.wanted,
            state=MatchState.NEEDS_REVIEW,
            why=unresolved,
            candidates=found.candidates,
            item_id=item_id,
        )
    return TrackMatch(
        wanted=found.wanted,
        state=MatchState.MATCHED,
        why=Why.VERDICT_ACCEPTED,
        candidates=tuple(chosen),
        paths=tuple(path for candidate in chosen for path in candidate.paths),
        item_id=item_id,
    )


__all__ = [
    "APPROXIMATE_FLOOR",
    "APPROXIMATE_LIMIT",
    "PAYLOAD_STATES",
    "QUESTION_KIND",
    "READERS",
    "SPOTIFY",
    "TEXT",
    "TIDAL",
    "TOMBSTONE_KIND",
    "Candidate",
    "LibraryIndex",
    "MatchResult",
    "MatchState",
    "Owned",
    "TrackMatch",
    "UnreadableList",
    "Wanted",
    "Why",
    "apply_verdict",
    "fold",
    "index_library",
    "key_disagreement",
    "read_spotify_items",
    "read_text_lines",
    "read_tidal_tracks",
    "recording_token",
    "resolve_all",
    "resolve_one",
    "split_version",
    "version_identity",
    "version_token",
]
