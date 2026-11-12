"""Suggest a genre for a row with none, from the library and the catalogue (U114).

WHY THIS EXISTS. 621 active rows of one library carried no genre on the row or
the file, so adoption left every one of them in INBOX. Setting them by hand in
rekordbox measured about 25 seconds a track before any listening, four and a
half hours for the lot. Most of them sit beside tracks that already say what
they are: the same artist's other tracks, the same folder's.

THE CANDIDATES ARE ROWS WITH NO GENRE ON THE ROW AND NONE ON THE FILE. A row
whose file carries a genre is counted ``file-has-genre`` and left to ``tag
rows``, which makes a row agree with its file. A row that already carries a
genre is counted and never offered: changing a genre a row carries is not this
module's job. A file whose genre could not be learned is counted under the
census's own names and never offered, because nothing says it is blank.

THREE SIGNALS, IN ORDER OF STRENGTH, each a weighted vote for a genre:

* the catalogue lookup ``tag folder`` makes, the record shops and then the
  general catalogue by ISRC, asked again once on a miss, since a third of a
  label download misses the first time. Opt in, because it is paced network
  work over every candidate. Weight :data:`CATALOGUE_WEIGHT`;
* the artist's other tracks in the library, weight :data:`ARTIST_WEIGHT` each;
* the folder's other tracks, weight :data:`FOLDER_WEIGHT` each. A label folder
  spans genres, so the folder is the weakest vote.

A neighbour votes once, at the higher of its weights, so a track by the same
artist in the same folder is not counted twice.

ONLY A GENRE THE ACTIVE TAXONOMY DECLARES IS SUGGESTED, which here means a word
adoption routes and the taxonomy names by an exact declaration, see
:func:`suggestable`. A neighbour's word that is not one still counts toward the
total, so it lowers the agreement, and is never itself suggested. A catalogue
answer outside the taxonomy is recorded as evidence and is no vote at all.

A CONFIDENCE BAND says how far the votes agree, see :func:`band_of`. A tie at
the top between declared genres is ``split``: every tied genre is offered and
none is the default, so the row is written only when a person picks one.

THE CATALOGUE'S ANSWERS ARE KEPT, in the library's state directory, for
:data:`CATALOGUE_DAYS` days. The gate is answered between two invocations and
each rebuilds the plan, so without them the run that applies would ask every
catalogue again, and an answer that moved would refuse the plan as stale. A
lookup that could not be read is kept for the day only and asked again on a
later one. Three rows in a row whose catalogues could not be read stop the
walk asking them at all.

Layer: modules. It opens no database of its own and names no verb.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field, replace
from datetime import date
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.adopt import collection
from cratekit.adopt import scan as adopt_scan
from cratekit.cli.output import digest_of
from cratekit.core import config, locations, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.tagging import rows, searchers
from cratekit.tagging.tag import PublishedGenre, Searcher, SearchHit
from cratekit.write import metadata, trees

#: The name a plan digests under and a session record carries.
WORKFLOW = "tag-suggest"

#: The weights of the three signals.
CATALOGUE_WEIGHT = 6
ARTIST_WEIGHT = 2
FOLDER_WEIGHT = 1

#: The bands, strongest first, and the bounds that give them. A band is the
#: share of the weighted votes the suggested genre holds, over at least so
#: many votes. Measured on a copy of one library, 2026-10-07: neighbours alone
#: gave at least 80 percent over six or more votes for 60 of 621 rows.
HIGH = "high"
MEDIUM = "medium"
LOW = "low"
BANDS: tuple[str, ...] = (HIGH, MEDIUM, LOW)
_BOUNDS: tuple[tuple[str, float, int], ...] = ((HIGH, 0.8, 6), (MEDIUM, 0.6, 3))

#: A tie at the top, and no vote at all. Neither has a default genre.
SPLIT = "split"
NONE = "none"

#: The outcomes, in the order a summary lists them. Every live row lands in
#: exactly one, and the counts are zero filled.
WRITE = "write"
HELD_OUT = "held-out"
BELOW_BAND = "below-band"
TIED = "tied"
NO_VOTES = "no-votes"
GENRE_UNKNOWN = "genre-unknown"
ROW_HAS_GENRE = "row-has-genre"
FILE_HAS_GENRE = "file-has-genre"

OUTCOMES: tuple[str, ...] = (
    WRITE,
    HELD_OUT,
    BELOW_BAND,
    TIED,
    NO_VOTES,
    GENRE_UNKNOWN,
    ROW_HAS_GENRE,
    FILE_HAS_GENRE,
    *rows.UNREAD,
)

#: The outcomes of a candidate that is offered and not written. Each is listed
#: in the plan as an item with the outcome as its reason.
LEFT: tuple[str, ...] = (HELD_OUT, BELOW_BAND, TIED, NO_VOTES, GENRE_UNKNOWN)

#: What an item whose row is not written says it does.
LEAVE = "leave"

#: What the catalogue said about one row, as an item carries it.
MATCHED = "matched"
DECLINED = "declined"
UNREAD = "unread"

#: How long a catalogue answer is reused, in days.
CATALOGUE_DAYS = 7

#: The state entry the catalogue's answers are kept in, under the library's state.
CATALOGUE_STATE = "tag_suggest_catalogue"

#: How many lookups are kept between saves, so a run stopped part way loses
#: at most this many paced lookups.
_SAVE_EVERY = 20

#: How many rows in a row the catalogues could not be read for before the walk
#: stops asking them. A catalogue refusing this client is not asked another
#: few hundred times, which is how an account gets rate limited for good.
STOP_AFTER_UNREAD = 3

_ORIGIN = ("tagging", "suggest")

#: Given one row's artist, title and ISRC, what the catalogue said. The shipped
#: one is :func:`catalogue_lookup`; a suite hands in its own.
Lookup = Callable[[str, str, str], "Asked"]


@dataclass(frozen=True, slots=True)
class Asked:
    """What the catalogue said about one row.

    ``said`` is :data:`MATCHED`, :data:`DECLINED` or :data:`UNREAD`. ``genre`` is
    the taxonomy's tag for a match and empty otherwise. ``off_taxonomy`` says
    the genre is the catalogue's own word passed through, which is never a vote.

    ``passed_over`` names the catalogues left unread because they were not asked
    at all, Discogs with no token recorded (U244). Such a row is UNREAD, since
    whether that catalogue knows it is unknown, and it is not a refusal of this
    client, so it never counts toward :data:`STOP_AFTER_UNREAD`.
    """

    said: str
    genre: str = ""
    source: str = ""
    source_genre: str = ""
    off_taxonomy: bool = False
    note: str = ""
    passed_over: tuple[str, ...] = ()

    def to_json(self) -> dict[str, Any]:
        return {
            "said": self.said,
            "genre": self.genre,
            "source": self.source,
            "source_genre": self.source_genre,
            "off_taxonomy": self.off_taxonomy,
            "note": self.note,
            "passed_over": list(self.passed_over),
        }


@dataclass(frozen=True, slots=True)
class Item:
    """One candidate row, what the evidence suggests, and what the plan does.

    ``genre`` is what a write puts on the file and the row, empty on a row left
    for want of a default. ``options`` is every tied genre on a split, and the
    suggested genre alone otherwise. ``votes`` is the weight each word got, the
    undeclared ones included, largest first. ``chosen`` says the genre shown is
    the one a person named with ``--set`` rather than the suggestion; the row
    can still be left, for a genre the library has no lookup row for.
    """

    content_id: str
    path: str
    artist: str
    title: str
    genre: str
    band: str
    options: tuple[str, ...]
    votes: tuple[tuple[str, int], ...]
    catalogue: Asked | None
    action: str
    reason: str = ""
    genre_id: str = ""
    chosen: bool = False

    def digested(self) -> dict[str, Any]:
        """What the digest covers: every vote, the answer, and what is written."""
        return {
            "content_id": self.content_id,
            "genre": self.genre,
            "band": self.band,
            "options": list(self.options),
            "votes": [[word, weight] for word, weight in self.votes],
            "catalogue": self.catalogue.to_json() if self.catalogue else None,
            "action": self.action,
            "reason": self.reason,
            "genre_id": self.genre_id,
            "chosen": self.chosen,
        }

    def to_json(self) -> dict[str, Any]:
        """The item as the gate shows it, with the file and the track's name."""
        return {**self.digested(), "path": self.path, "artist": self.artist, "title": self.title}


@dataclass(frozen=True, slots=True)
class SuggestPlan:
    """Every candidate, the count of every outcome, and the row write itself."""

    items: tuple[Item, ...]
    counts: Mapping[str, int]
    changes: metadata.Plan
    band: str
    catalogue: bool
    #: Identifiers given to ``--leave`` or ``--set`` that name no candidate.
    #: Shown and digested, because a mistyped identifier is a row the person
    #: meant to hold or to pick and the plan does otherwise.
    unmatched: tuple[str, ...] = ()

    @property
    def writes(self) -> tuple[Item, ...]:
        return tuple(item for item in self.items if item.action == WRITE)

    @property
    def rows(self) -> int:
        """Every live row the walk counted."""
        return sum(self.counts.values())

    @property
    def unread(self) -> int:
        """Rows whose file's genre was never learned."""
        return sum(self.counts[name] for name in rows.UNREAD)

    @property
    def digest(self) -> str:
        """The fingerprint an approval is bound to.

        OVER THE ITEMS, THE COUNTS AND THE CHOICES, AND NOTHING THAT NAMES A
        COPY, for the reason :attr:`cratekit.tagging.rows.RowsPlan.digest` gives.
        """
        return digest_of(
            {
                "kind": WORKFLOW,
                "items": [item.digested() for item in self.items],
                "counts": dict(self.counts),
                "band": self.band,
                "catalogue": self.catalogue,
                "unmatched": list(self.unmatched),
            }
        )

    def groups(self) -> list[dict[str, Any]]:
        """The candidates grouped by suggested genre and band, largest first.

        A split row is grouped under every tied genre joined, since it has no
        one genre to be grouped under.
        """
        seen = Counter(
            (item.genre or " or ".join(item.options), item.band, item.action)
            for item in self.items
        )
        ordered = sorted(seen.items(), key=lambda entry: (-entry[1], entry[0]))
        return [
            {"genre": genre, "band": band, "action": action, "rows": count}
            for (genre, band, action), count in ordered
        ]


# ---------------------------------------------------------------------------
# The rules, pure
# ---------------------------------------------------------------------------


def suggestable(declared: taxonomy.Taxonomy, genre: str) -> bool:
    """Whether a genre is one this module may suggest.

    ONE ADOPTION ROUTES AND THE TAXONOMY NAMES EXACTLY. Routing alone would
    accept a word a keyword tier or a catch all places, which is a word the
    library does not declare, and the goal is a genre adoption files under its
    genre folder rather than one that only happens to land somewhere.
    """
    word = (genre or "").strip()
    if not word:
        return False
    disposition, _bucket, _match = adopt_scan.classify_genre(declared, word)
    return disposition is adopt_scan.Disposition.ROUTE and declared.named_folder(word) is not None


def band_of(weight: int, total: int) -> str:
    """The band a genre holding ``weight`` of ``total`` weighted votes earns. Pure."""
    if total <= 0 or weight <= 0:
        return NONE
    share = weight / total
    for name, least, votes in _BOUNDS:
        if share >= least and total >= votes:
            return name
    return LOW


def weigh(
    declared: taxonomy.Taxonomy, votes: Mapping[str, int]
) -> tuple[str, str, tuple[str, ...]]:
    """The suggested genre, its band, and the genres offered. Pure.

    The total is every vote, the undeclared words included. The suggestion is
    the declared genre with the most weight, and a tie there is a split with no
    default.
    """
    total = sum(votes.values())
    declared_votes = {word: weight for word, weight in votes.items() if suggestable(declared, word)}
    if not declared_votes:
        return "", NONE, ()
    top = max(declared_votes.values())
    tied = tuple(sorted(word for word, weight in declared_votes.items() if weight == top))
    if len(tied) > 1:
        return "", SPLIT, tied
    return tied[0], band_of(top, total), tied


def _at_or_above(band: str, least: str) -> bool:
    """Whether ``band`` is at least ``least``. Split and none never are."""
    if band not in BANDS:
        return False
    return BANDS.index(band) <= BANDS.index(least)


# ---------------------------------------------------------------------------
# The catalogue
# ---------------------------------------------------------------------------


def _asked_from(hit: SearchHit | None) -> Asked:
    if hit is None:
        return Asked(DECLINED)
    if hit.genre:
        return Asked(
            MATCHED,
            genre=hit.genre,
            source=hit.source,
            source_genre=hit.source_genre,
            off_taxonomy=hit.off_taxonomy,
        )
    if hit.unread and not hit.source_genre:
        # A CATALOGUE THE WALK NEVER ASKED IS NOT ONE THAT REFUSED (U244). It is
        # named with the reason its record gives, so the row says how to have
        # it asked, and it is kept apart so the walk does not stop over it.
        unasked = {
            said.source: said.note
            for said in hit.answers
            if said.source in hit.unread and said.answer == searchers.NOT_ASKED
        }
        refused = [source for source in hit.unread if source not in unasked]
        if refused:
            return Asked(UNREAD, note=f"unread: {', '.join(refused)}")
        return Asked(
            UNREAD,
            note="; ".join(f"unread: {source}, {why}" for source, why in unasked.items()),
            passed_over=tuple(unasked),
        )
    return Asked(DECLINED, source=hit.source, source_genre=hit.source_genre)


def catalogue_lookup(searcher: Searcher, published: PublishedGenre | None = None) -> Lookup:
    """The catalogue lookup ``tag folder`` makes, asked again once on a plain miss.

    The record shops first, then the general catalogue by ISRC when they gave no
    genre, which is :func:`cratekit.tagging.tag.tag_one`'s order. A refusal to
    read a catalogue is not raised: it is this row's answer, :data:`UNREAD`, and
    the walk goes on to the next row.
    """

    def once(artist: str, title: str, isrc: str) -> Asked:
        try:
            hit = searcher(artist, title)
            if published is not None and hit is not None and not hit.genre:
                hit = published(hit, isrc)
        except CratekitError as exc:
            return Asked(UNREAD, note=f"{exc.cause.reason}: {exc.cause.message}")
        return _asked_from(hit)

    def lookup(artist: str, title: str, isrc: str) -> Asked:
        first = once(artist, title, isrc)
        # ONLY A PLAIN MISS IS ASKED AGAIN. A word the taxonomy declined will
        # be declined again, and a catalogue that could not be read is one that
        # is refusing this client: asking it twice per row deepens the block.
        if first.said != DECLINED or first.source_genre:
            return first
        return once(artist, title, isrc)

    return lookup


def catalogue_path(cfg: config.Config) -> Path:
    return config.state_path(CATALOGUE_STATE, cfg)


def _read_kept(path: Path) -> dict[str, Any]:
    """The kept answers, or none when there is no file or it cannot be read.

    AN UNREADABLE FILE READS AS EMPTY, and that is safe in this direction only:
    what it costs is asking again, never an answer nobody gave.
    """
    try:
        found = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return found if isinstance(found, dict) else {}


def _save_kept(path: Path, kept: Mapping[str, Any]) -> None:
    payload = json.dumps(dict(sorted(kept.items())), indent=1, sort_keys=True)
    config.atomic_write_bytes(payload.encode("utf-8"), path)


def _kept_answer(entry: Any, asked_for: dict[str, str], today: date) -> Asked | None:
    """A kept answer still good for this row, or None."""
    if not isinstance(entry, dict) or entry.get("for") != asked_for:
        return None
    try:
        age = (today - date.fromisoformat(str(entry.get("on")))).days
        said = dict(entry["answer"])
        answer = Asked(
            str(said["said"]),
            genre=str(said.get("genre") or ""),
            source=str(said.get("source") or ""),
            source_genre=str(said.get("source_genre") or ""),
            off_taxonomy=bool(said.get("off_taxonomy")),
            note=str(said.get("note") or ""),
            passed_over=tuple(str(one) for one in said.get("passed_over") or ()),
        )
    except (KeyError, TypeError, ValueError):
        return None
    if not 0 <= age < CATALOGUE_DAYS:
        return None
    # AN ANSWER NOBODY COULD READ IS KEPT FOR THE DAY AND NO LONGER, so the run
    # that applies a plan made today reads the same answer the gate showed,
    # and a later day asks again.
    if answer.said == UNREAD and age != 0:
        return None
    return answer


class KeptCatalogue:
    """The catalogue lookup with its answers kept across invocations.

    A context manager so the answers asked since the last save are saved
    however the walk ends.
    """

    def __init__(
        self,
        cfg: config.Config,
        lookup: Lookup,
        *,
        today: date | None = None,
        unasked: frozenset[str] | None = None,
    ):
        """``unasked`` is the catalogues this run cannot ask, Discogs with no
        token, or None when the caller does not know. A kept answer that passed
        over a catalogue this run CAN ask is asked again, whatever its day
        (U244's review, round two): a person who recorded a token after the
        morning's run is not told for the rest of the day that none is."""
        self._path = catalogue_path(cfg)
        self._lookup = lookup
        self._unasked = unasked
        self._today = today or date.today()
        self._kept = _read_kept(self._path)
        self._unsaved = 0
        self._unread_running = 0
        self.asked = 0
        #: True once the walk stopped asking, see :data:`STOP_AFTER_UNREAD`.
        self.stopped = False

    def __enter__(self) -> KeptCatalogue:
        return self

    def __exit__(self, *exc: object) -> None:
        self.save()

    def _askable_now(self, kept: Asked) -> bool:
        """Whether a kept answer passed over a catalogue this run can ask."""
        if self._unasked is None or not kept.passed_over:
            return False
        return not set(kept.passed_over) <= self._unasked

    def save(self) -> None:
        if self._unsaved:
            _save_kept(self._path, self._kept)
            self._unsaved = 0

    def answer(self, content_id: str, artist: str, title: str, isrc: str) -> Asked:
        asked_for = {"artist": artist, "title": title, "isrc": isrc}
        kept = _kept_answer(self._kept.get(content_id), asked_for, self._today)
        if kept is not None and not self._askable_now(kept):
            return kept
        if self.stopped:
            answer = Asked(
                UNREAD,
                note=(
                    f"not asked: the catalogues could not be read for "
                    f"{STOP_AFTER_UNREAD} rows in a row"
                ),
            )
        else:
            answer = self._lookup(artist, title, isrc)
            self.asked += 1
            # A ROW LEFT UNREAD ONLY BY A CATALOGUE NOBODY ASKED neither counts
            # toward the stop nor ends a run of refusals: it says nothing about
            # whether the catalogues that were asked are refusing (U244).
            if answer.said == UNREAD and not answer.passed_over:
                self._unread_running += 1
            elif answer.said != UNREAD:
                self._unread_running = 0
            self.stopped = self._unread_running >= STOP_AFTER_UNREAD
        self._kept[content_id] = {
            "for": asked_for,
            "on": self._today.isoformat(),
            "answer": answer.to_json(),
        }
        self._unsaved += 1
        if self._unsaved >= _SAVE_EVERY:
            self.save()
        return answer


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class _Row:
    content_id: str
    artist: str
    folder: str
    genre: str
    title: str
    mapped: Any = field(repr=False, default=None)


def _artist_key(value: str) -> str:
    return " ".join(value.casefold().split())


def _folder_of(recorded: str) -> str:
    """The folder a recorded location names, as text, or empty."""
    text = recorded.strip()
    if "/" not in text:
        return ""
    return text.rsplit("/", 1)[0]


def _neighbours(live: Mapping[str, _Row]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """The rows carrying a genre, by artist and by folder."""
    by_artist: dict[str, list[str]] = {}
    by_folder: dict[str, list[str]] = {}
    for row in live.values():
        if not row.genre:
            continue
        if row.artist:
            by_artist.setdefault(_artist_key(row.artist), []).append(row.content_id)
        if row.folder:
            by_folder.setdefault(row.folder, []).append(row.content_id)
    return by_artist, by_folder


def _votes(
    row: _Row,
    live: Mapping[str, _Row],
    by_artist: Mapping[str, list[str]],
    by_folder: Mapping[str, list[str]],
    asked: Asked | None,
    declared: taxonomy.Taxonomy,
) -> dict[str, int]:
    """Every word's weight for one candidate. A neighbour votes once."""
    weights: dict[str, int] = {}
    for other in by_folder.get(row.folder, ()) if row.folder else ():
        weights[other] = FOLDER_WEIGHT
    for other in by_artist.get(_artist_key(row.artist), ()) if row.artist else ():
        weights[other] = max(weights.get(other, 0), ARTIST_WEIGHT)
    weights.pop(row.content_id, None)
    votes: Counter[str] = Counter()
    for other, weight in weights.items():
        votes[live[other].genre] += weight
    if (
        asked is not None
        and asked.said == MATCHED
        and not asked.off_taxonomy
        and suggestable(declared, asked.genre)
    ):
        votes[asked.genre] += CATALOGUE_WEIGHT
    return dict(votes)


def _ordered(votes: Mapping[str, int]) -> tuple[tuple[str, int], ...]:
    return tuple(sorted(votes.items(), key=lambda entry: (-entry[1], entry[0])))


def plan_suggestions(
    cfg: config.Config,
    db: Any,
    declared: taxonomy.Taxonomy,
    *,
    band: str = HIGH,
    leave: Iterable[str] = (),
    chosen: Mapping[str, str] | None = None,
    catalogue: KeptCatalogue | None = None,
    progress: Callable[[str], None] | None = None,
    probe: Callable[[Path], adopt_scan.Readability] = adopt_scan.probe_readability,
) -> SuggestPlan:
    """Walk the collection once and sort every live row into one outcome.

    THE WALK IS ADOPTION'S CENSUS, as :func:`cratekit.tagging.rows.plan_rows`
    walks it, so a row's file is found and probed the way adoption finds it and
    a tombstone is skipped and not counted.

    A CANDIDATE IS WRITTEN WHEN its suggestion is at or above ``band``, it is
    not held out by ``leave``, and the library has a lookup row for its genre.
    ``chosen`` names a genre a person picked for a candidate, which is written
    whatever the band, a split's included. The caller has checked each chosen
    genre is :func:`suggestable`.

    NOTHING IS PENDING ON THE HANDLE WHEN THIS RETURNS, for the reason
    :func:`cratekit.tagging.rows.plan_rows` gives.
    """
    held_out = frozenset(str(content_id) for content_id in leave)
    picks = {str(key): value for key, value in (chosen or {}).items()}
    counts = dict.fromkeys(OUTCOMES, 0)
    mapped = {str(row.ID): row for row in db.get_content()}
    live: dict[str, _Row] = {}
    for content_id, row in mapped.items():
        if trees.soft_delete_marker(row):
            continue
        live[content_id] = _Row(
            content_id=content_id,
            artist=str(getattr(row, "ArtistName", "") or "").strip(),
            folder=_folder_of(str(getattr(row, "FolderPath", "") or "")),
            genre=collection.genre_of(row).strip(),
            title=str(getattr(row, "Title", "") or "").strip(),
            mapped=row,
        )
    census = adopt_scan.scan_rows(
        collection.collection_rows(mapped.values()),
        declared,
        root=Path(cfg.library.root),
        prefix_map=locations.prefix_rules(cfg.resolved_prefix_map()),
        probe=probe,
        energy_reader=rows._no_energy,
    )
    candidates: list[tuple[_Row, str]] = []
    for track in census:
        if track.genre.strip():
            counts[ROW_HAS_GENRE] += 1
            continue
        if track.readability is not adopt_scan.Readability.READABLE or track.path is None:
            counts[rows._PROBED.get(track.readability, rows.FILE_UNREADABLE)] += 1
            continue
        word, outcome = rows._file_word(Path(track.path))
        if outcome == rows.FILE_UNREADABLE:
            counts[rows.FILE_UNREADABLE] += 1
            continue
        if word:
            counts[FILE_HAS_GENRE] += 1
            # IT VOTES WITH ITS FILE'S WORD. The row lags its file, which is
            # what ``tag rows`` repairs, and the file is the newer of the two.
            live[track.content_id].genre = word
            continue
        candidates.append((live[track.content_id], track.path))
    by_artist, by_folder = _neighbours(live)

    items: list[Item] = []
    to_write: dict[str, str] = {}
    for ordinal, (row, path) in enumerate(sorted(candidates, key=lambda c: c[0].content_id), 1):
        asked = None
        # A ROW HELD OUT OR PICKED IS NOT LOOKED UP: no answer changes it, and
        # every lookup is a paced request.
        settled_by_person = row.content_id in held_out or row.content_id in picks
        if catalogue is not None and not settled_by_person:
            isrc = tags.read_tag(Path(path), "isrc") or ""
            asked = catalogue.answer(row.content_id, row.artist, row.title, isrc.strip())
            if progress is not None and (ordinal == 1 or ordinal % 25 == 0):
                progress(f"catalogue: row {ordinal} of {len(candidates)}")
        votes = _votes(row, live, by_artist, by_folder, asked, declared)
        genre, earned, options = weigh(declared, votes)
        picked = picks.get(row.content_id)
        if row.content_id in held_out:
            reason = HELD_OUT
        elif picked:
            genre, reason = picked, ""
        elif earned == SPLIT:
            reason = TIED
        elif earned == NONE:
            reason = NO_VOTES
        elif not _at_or_above(earned, band):
            reason = BELOW_BAND
        else:
            reason = ""
        item = Item(
            content_id=row.content_id,
            path=path,
            artist=row.artist,
            title=row.title,
            genre=genre,
            band=earned,
            options=options,
            votes=_ordered(votes),
            catalogue=asked,
            action=LEAVE if reason else WRITE,
            reason=reason,
            chosen=bool(picked) and not reason,
        )
        if item.action == WRITE:
            to_write[row.content_id] = genre
        items.append(item)

    changes = metadata.plan_genre_retag(
        [live[content_id].mapped for content_id in to_write], to_write, db=db
    )
    linked = {change.content_id: str(change.new) for change in changes.changes}
    settled: list[Item] = []
    for item in items:
        if item.action == WRITE:
            genre_id = linked.get(item.content_id)
            item = (
                replace(item, action=LEAVE, reason=GENRE_UNKNOWN)
                if genre_id is None
                else replace(item, genre_id=genre_id)
            )
        counts[item.reason or WRITE] += 1
        settled.append(item)
    listed = {item.content_id for item in settled}
    return SuggestPlan(
        items=tuple(settled),
        counts=MappingProxyType(counts),
        changes=changes,
        band=band,
        catalogue=catalogue is not None,
        unmatched=tuple(sorted((held_out | set(picks)) - listed)),
    )


# ---------------------------------------------------------------------------
# The file write
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FilesWritten:
    """What the file half of an apply did, per content identifier.

    ``read_back`` holds the rows whose file now carries the genre. ``moved``
    carried a genre by the time the write reached them, ``failed`` the writer
    could not write, ``wrong`` were written and read back otherwise.
    """

    read_back: tuple[str, ...] = ()
    moved: tuple[str, ...] = ()
    failed: tuple[str, ...] = ()
    wrong: tuple[str, ...] = ()

    @property
    def clean(self) -> bool:
        return not (self.moved or self.failed or self.wrong)


def write_files(plan: SuggestPlan) -> FilesWritten:
    """Write each planned genre onto its file and read it back.

    EACH FILE IS READ AGAIN FIRST, and one that carries a genre by now is named
    and left: it was blank when the plan was approved, and what is on it since
    is somebody else's. Nothing here raises for one file, so one that cannot be
    written does not stop the rest.
    """
    read_back: list[str] = []
    moved: list[str] = []
    failed: list[str] = []
    wrong: list[str] = []
    for item in plan.writes:
        target = Path(item.path)
        word, outcome = rows._file_word(target)
        if word or outcome != rows.FILE_BLANK:
            moved.append(item.content_id)
            continue
        if not tags.write_genre(target, item.genre):
            failed.append(item.content_id)
            continue
        if rows._file_word(target)[0] != item.genre:
            wrong.append(item.content_id)
            continue
        read_back.append(item.content_id)
    return FilesWritten(tuple(read_back), tuple(moved), tuple(failed), tuple(wrong))


def rows_plan(plan: SuggestPlan, content_ids: Iterable[str]) -> rows.RowsPlan:
    """The row half of an apply, as the row verb's engine takes it.

    Only the rows named, which are the ones whose file read back, so a row is
    never written with a genre its file does not carry.
    """
    wanted = frozenset(content_ids)
    items = tuple(
        rows.Item(
            item.content_id, item.path, "", item.genre, rows.WRITE, genre_id=item.genre_id
        )
        for item in plan.writes
        if item.content_id in wanted
    )
    changes = metadata.Plan(
        owner=plan.changes.owner,
        changes=tuple(change for change in plan.changes.changes if change.content_id in wanted),
    )
    counts = MappingProxyType({rows.WRITE: len(items)})
    return rows.RowsPlan(items=items, counts=counts, changes=changes)


__all__ = [
    "ARTIST_WEIGHT",
    "BANDS",
    "BELOW_BAND",
    "CATALOGUE_DAYS",
    "CATALOGUE_STATE",
    "CATALOGUE_WEIGHT",
    "DECLINED",
    "FILE_HAS_GENRE",
    "FOLDER_WEIGHT",
    "GENRE_UNKNOWN",
    "HELD_OUT",
    "HIGH",
    "LEAVE",
    "LEFT",
    "LOW",
    "MATCHED",
    "MEDIUM",
    "NONE",
    "NO_VOTES",
    "OUTCOMES",
    "ROW_HAS_GENRE",
    "SPLIT",
    "STOP_AFTER_UNREAD",
    "TIED",
    "UNREAD",
    "WORKFLOW",
    "WRITE",
    "Asked",
    "FilesWritten",
    "Item",
    "KeptCatalogue",
    "Lookup",
    "SuggestPlan",
    "band_of",
    "catalogue_lookup",
    "catalogue_path",
    "plan_suggestions",
    "rows_plan",
    "suggestable",
    "weigh",
    "write_files",
]
