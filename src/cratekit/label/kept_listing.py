"""A label's listing, kept across runs (U217).

``TidalCatalogue.artist_for`` builds a label's roster from four kinds of
provider answer: an exact artist name search, an artist identifier read, an
album search crediting artists beside the label, and one artist's paged
listing of one release method. This store keeps each answer per label, so a
continue asks only what a stopped run did not finish.

An answer is kept for :data:`kept_reads.KEPT_FOR`, read at call time so the two
stores have one number. A failed read is never kept. THE DOCUMENT NAMES WHAT IT
WAS ASKED FOR, the label's name, match and seeds, so a changed entry reads it
as empty. It is written as it goes, every :data:`FLUSH_EVERY` answers and on
the way out, a refused write said as ``unkept``. One that cannot be read
refuses, ``label-listing-kept-unusable``; deleting it is safe.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.label import kept_reads
from cratekit.label.catalogue import artist_name

#: Answers asked now between two writes of the document.
FLUSH_EVERY = 50

#: The document's version. Any other refuses rather than being read.
VERSION = 1

#: The file inside the label's own directory of the crawl cache.
FILE_NAME = "listing.json"

UNUSABLE = "label-listing-kept-unusable"

_ORIGIN = ("label.listing",)

#: The four kinds of answer, as the document's sections name them.
NAMED = "named"
IDENTIFIED = "identified"
SEARCHED = "searched"
LISTED = "listed"
_SECTIONS = (NAMED, IDENTIFIED, SEARCHED, LISTED)


def path_for(label_id: str) -> Path:
    return config.state_path("label_crawl_cache") / label_id / FILE_NAME


def _now() -> datetime:
    """R-1091's clock, so a suite ages both stores with one assignment."""
    return kept_reads.clock()


def kept_for() -> timedelta:
    return kept_reads.KEPT_FOR


@dataclass(frozen=True, slots=True)
class KeptArtist:
    """An artist a kept release credits, as the credited artist walk reads it."""

    id: str


@dataclass(frozen=True, slots=True)
class KeptRelease:
    """One listed release as the store keeps it: what every reader takes off it."""

    id: str
    title: str
    year: int | str | None
    release_date: str | None
    copyright: str
    artist: str
    artists: tuple[KeptArtist, ...] = ()

    @property
    def name(self) -> str:
        """The provider names an album ``name``; the sweep reads either."""
        return self.title


def _year(release: Any) -> int | str | None:
    held = getattr(release, "year", None)
    return held if isinstance(held, (int, str)) and not isinstance(held, bool) else None


def release_row(release: Any) -> dict[str, Any]:
    """One provider release as the document stores it."""
    date = getattr(release, "release_date", None)
    copyright_line = getattr(release, "copyright", None) or getattr(release, "label", None) or ""
    credited = [
        identity
        for one in getattr(release, "artists", None) or ()
        if (identity := str(getattr(one, "id", "") or ""))
    ]
    return {
        "id": str(getattr(release, "id", "") or ""),
        "title": str(getattr(release, "title", "") or getattr(release, "name", "") or ""),
        "year": _year(release),
        "release_date": None if date is None else str(date),
        "copyright": str(copyright_line),
        "artist": artist_name(release),
        "artists": credited,
    }


@dataclass(frozen=True, slots=True)
class Answer:
    """One kept answer and when the provider gave it."""

    read_at: datetime
    value: Any


@dataclass(frozen=True, slots=True)
class Summary:
    """What one listing made of its store, for the screen: answers ``reused`` from
    an earlier run, ``asked`` now, ``stale`` of those asked as too old, and
    whether the store was set aside as ``changed``."""

    reused: int
    asked: int
    stale: int
    changed: bool
    oldest: datetime | None
    unkept: str
    path: str

    @property
    def age(self) -> str:
        return "" if self.oldest is None else kept_reads.age_text(_now() - self.oldest)

    def said(self) -> str:
        """One sentence a person reads: where the listing came from, and why."""
        life = kept_reads.kept_for_said()
        if self.reused and not self.asked:
            text = (
                f"the label's listing was answered from the one kept by an earlier "
                f"run, {self.age} old, with no listing call to the provider; it is read again once "
                f"it is {life} old, or after {self.path} is deleted"
            )
        elif self.reused:
            text = (
                f"the label's listing continued from an earlier run: {self.reused} "
                f"answer(s) kept, the oldest {self.age} old, and {self.asked} asked "
                f"of the provider now"
            )
        elif self.changed:
            text = (
                "the label's listing was read from the provider, since the label's "
                "name, match or seed artists changed after its listing was kept"
            )
        elif self.stale:
            text = (
                f"the label's listing was read from the provider, since the one kept "
                f"was older than {life}"
            )
        else:
            text = "the label's listing was read from the provider, since none was kept"
        if self.unkept:
            text += (
                f"; what was read could not be kept ({self.unkept}), so the next "
                f"run reads it again"
            )
        return text


def _unusable(path: Path, what: str) -> CratekitError:
    return refuse(
        UNUSABLE,
        f"the listing kept for this label at {path.name} could not be read "
        f"({what}), so what the label's listing already holds is unknown; nothing "
        f"was asked of the provider and nothing was written",
        steps=(
            f"delete {path} to list the label again from the start; it holds "
            f"provider answers only and nothing else is lost",
        ),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"problem": what, "path": str(path)},
    )


def _strings(raw: Any) -> bool:
    return isinstance(raw, list) and all(isinstance(one, str) for one in raw)


def _valid_release(raw: Any) -> bool:
    if not isinstance(raw, Mapping):
        return False
    year = raw.get("year")
    date = raw.get("release_date")
    return (
        isinstance(raw.get("id"), str)
        and isinstance(raw.get("title"), str)
        and (year is None or (isinstance(year, (int, str)) and not isinstance(year, bool)))
        and (date is None or isinstance(date, str))
        and isinstance(raw.get("copyright"), str)
        and isinstance(raw.get("artist"), str)
        and _strings(raw.get("artists"))
    )


def _valid(section: str, value: Any) -> bool:
    if section == NAMED:
        return (
            isinstance(value, Mapping)
            and _strings(value.get("ids"))
            and _strings(value.get("names"))
            and len(value["ids"]) == len(value["names"])
            and len(value["ids"]) <= 1
        )
    if section == IDENTIFIED:
        return (
            isinstance(value, Mapping)
            and isinstance(value.get("found"), bool)
            and isinstance(value.get("name"), str)
        )
    if section == SEARCHED:
        return _strings(value)
    return isinstance(value, list) and all(_valid_release(one) for one in value)


def _release(raw: Mapping[str, Any]) -> KeptRelease:
    return KeptRelease(
        id=raw["id"],
        title=raw["title"],
        year=raw["year"],
        release_date=raw["release_date"],
        copyright=raw["copyright"],
        artist=raw["artist"],
        artists=tuple(KeptArtist(id=one) for one in raw["artists"]),
    )


def asked_for(entry: Any) -> dict[str, Any]:
    """What a label's listing is an answer to: its name, its match and its seeds."""
    return {
        "name": str(entry.name),
        "match": str(entry.match or ""),
        "seeds": [str(seed) for seed in entry.seed_artists],
    }


class KeptListing(kept_reads._Store):
    """One label's kept listing answers, and what this run made of them."""

    version = VERSION

    def __init__(
        self,
        label_id: str,
        asked: Mapping[str, Any],
        held: Mapping[str, Mapping[str, Answer]],
        *,
        path: Path,
        changed: bool = False,
    ) -> None:
        super().__init__(label_id, path)
        self.asked_for = dict(asked)
        self._held: dict[str, dict[str, Answer]] = {
            section: dict(held.get(section, {})) for section in _SECTIONS
        }
        self.changed = changed
        #: Answers this run asked, read back without counting as reused.
        self._asked_now: set[tuple[str, str]] = set()
        self._reused: set[tuple[str, str]] = set()
        self._stale: set[tuple[str, str]] = set()
        #: Provider answers this run asked, kept or not, not a call count.
        self.asked = 0

    @classmethod
    def load(cls, entry: Any) -> KeptListing:
        """The label's kept listing, an empty one when none fits, or the refusal."""
        label_id = str(entry.label_id)
        asked = asked_for(entry)
        path = path_for(label_id)
        raw = cls._document(path, label_id, _unusable)
        if raw is None:
            return cls(label_id, asked, {}, path=path)
        if not isinstance(raw.get("asked_for"), Mapping):
            raise _unusable(path, "it does not say what it was asked for")
        held: dict[str, dict[str, Answer]] = {}
        for section in _SECTIONS:
            answers = raw.get(section)
            if not isinstance(answers, Mapping):
                raise _unusable(path, f"its {section} answers are not a map")
            held[section] = {}
            for key, value in answers.items():
                if not isinstance(value, Mapping):
                    raise _unusable(path, f"the {section} answer {key!r} is not a map")
                read_at = kept_reads._instant(value.get("read_at"))
                if read_at is None:
                    raise _unusable(path, f"the {section} answer {key!r} carries no instant")
                if not _valid(section, value.get("value")):
                    raise _unusable(path, f"the {section} answer {key!r} is malformed")
                held[section][str(key)] = Answer(read_at=read_at, value=value["value"])
        if dict(raw["asked_for"]) != asked:
            # A DIFFERENT QUESTION, NOT A BROKEN DOCUMENT: the next write replaces it.
            return cls(label_id, asked, {}, path=path, changed=True)
        return cls(label_id, asked, held, path=path)

    def _fresh(self, section: str, key: str) -> Answer | None:
        held = self._held[section].get(key)
        if held is None:
            return None
        if (section, key) in self._asked_now:
            return held
        if not _young(held):
            self._stale.add((section, key))
            return None
        self._reused.add((section, key))
        self._reusing(held.read_at)
        return held

    @property
    def reused(self) -> int:
        """Answers this run took from an earlier one, each counted once."""
        return len(self._reused)

    @property
    def stale(self) -> int:
        """Kept answers this run found too old, each counted once."""
        return len(self._stale)

    def named(self, name: str) -> tuple[tuple[str, str], ...] | None:
        """The exact artist a name search found, as ``(id, name)`` pairs, or ``None`` unkept."""
        held = self._fresh(NAMED, name)
        if held is None:
            return None
        return tuple(zip(held.value["ids"], held.value["names"], strict=True))

    def identified(self, artist_id: str) -> tuple[bool, str] | None:
        """Whether the provider had the artist and its name, or ``None`` unkept."""
        held = self._fresh(IDENTIFIED, artist_id)
        return None if held is None else (held.value["found"], held.value["name"])

    def searched(self, query: str) -> tuple[str, ...] | None:
        """The artist identifiers an album search credited, or ``None`` unkept."""
        held = self._fresh(SEARCHED, query)
        return None if held is None else tuple(held.value)

    def has_listing(self, artist_id: str, method: str) -> bool:
        """Whether a fresh listing is held, counting nothing."""
        key = _listing_key(artist_id, method)
        held = self._held[LISTED].get(key)
        return held is not None and ((LISTED, key) in self._asked_now or _young(held))

    def listed(self, artist_id: str, method: str) -> list[KeptRelease] | None:
        """One artist's listing of one release method, or ``None`` unkept."""
        held = self._fresh(LISTED, _listing_key(artist_id, method))
        return None if held is None else [_release(one) for one in held.value]

    def asked_unkept(self) -> None:
        """Count a provider call whose answer cannot be kept, so the screen is true."""
        self.asked += 1

    def _keep(self, section: str, key: str, value: Any) -> None:
        self._held[section][key] = Answer(read_at=_now(), value=value)
        self._asked_now.add((section, key))
        self.asked += 1
        self._counted()
        if self._since >= FLUSH_EVERY:
            self.flush()

    def keep_named(self, name: str, found: Iterable[tuple[str, str]]) -> None:
        pairs = list(found)
        self._keep(
            NAMED, name, {"ids": [one for one, _ in pairs], "names": [two for _, two in pairs]}
        )

    def keep_identified(self, artist_id: str, *, found: bool, name: str) -> None:
        self._keep(IDENTIFIED, artist_id, {"found": found, "name": name})

    def keep_searched(self, query: str, credited: Iterable[str]) -> None:
        self._keep(SEARCHED, query, list(dict.fromkeys(credited)))

    def keep_listed(self, artist_id: str, method: str, releases: Iterable[Any]) -> None:
        self._keep(LISTED, _listing_key(artist_id, method), [release_row(one) for one in releases])

    def _sections(self) -> dict[str, Any]:
        return {
            "asked_for": self.asked_for,
            **{
                section: {
                    key: {"read_at": held.read_at.isoformat(), "value": held.value}
                    for key, held in sorted(self._held[section].items())
                }
                for section in _SECTIONS
            },
        }

    def summary(self) -> Summary:
        held = (self.reused, self.asked, self.stale, self.changed, self.oldest, self.unkept)
        return Summary(*held, path=str(self.path))


@dataclass(frozen=True, slots=True)
class Cost:
    """A fresh ask's cost, read off the kept answers (U278): ``held`` in the
    store, ``aged`` of them too old to answer and so asked again."""

    held: int
    aged: int


def cost(entry: Any) -> Cost | None:
    """The label's kept answers and how many are aged, or None when none can say;
    a floor, each answer counted one call."""
    try:
        kept = KeptListing.load(entry)
    except CratekitError:
        return None
    answers = [held for section in _SECTIONS for held in kept._held[section].values()]
    if not answers:
        return None
    return Cost(held=len(answers), aged=sum(1 for held in answers if not _young(held)))


def estimate(entry: Any) -> int | None:
    """The calls a fresh ask of the label would make, by :func:`cost`, or None."""
    return None if (found := cost(entry)) is None else found.aged


def _young(held: Answer) -> bool:
    return timedelta(0) <= _now() - held.read_at < kept_for()


def _listing_key(artist_id: str, method: str) -> str:
    return f"{artist_id} {method}"


__all__ = [
    "FLUSH_EVERY",
    "Cost",
    "UNUSABLE",
    "KeptArtist",
    "KeptListing",
    "KeptRelease",
    "Summary",
    "asked_for",
    "cost",
    "estimate",
    "path_for",
    "release_row",
]
