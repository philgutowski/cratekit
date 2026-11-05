"""A label's listing, kept across runs (U217).

``TidalCatalogue.artist_for`` builds a label's roster from four kinds of
provider answer: a name searched for an exact artist, an identifier read as an
artist, an album search that finds the artists credited beside the label, and
one artist's paged listing of one release method. A label the size of Defected
is about 1,800 of them. Held only in memory, a run stopped by the call ceiling
or the breaker dropped every one, so each continue read the whole listing again
from the start, and a second ask of the same label a minute later paid it all
again. This store keeps each answer per label, so a continue asks only what the
stopped run did not finish and a second ask asks nothing.

AN ANSWER IS KEPT FOR R-1091'S AGE AND NO LONGER, :data:`kept_reads.KEPT_FOR`,
read from that module at call time so the two stores have one number. A label
that put out a release after its listing was read shows that release once the
listing is that old, and the screen says how old the listing it answered from
is, so a person knows the question was not read that minute.

WHAT IS KEPT is what the roster and every reader of a listed release take off
it and nothing else: for a release its identifier, title, year, release date,
the copyright line, the artist's name and the identifiers of the artists it
credits. It is read back as a :class:`KeptRelease`, which those readers accept
as they accept the provider's own object. A read that failed is not an answer
and is never kept, nor is a listing the client could not page or does not
expose, nor an answer about an artist with no identifier to key it by.

THE DOCUMENT NAMES WHAT IT WAS ASKED FOR, the label's name, its match and its
seed artists. Discovery's answers depend on the match, and the roster on the
seeds, so a registry entry that changed any of them reads the store as empty
and the next write replaces it.

WRITTEN AS IT GOES. :meth:`KeptListing.flush` writes the document whole and
atomically, every :data:`FLUSH_EVERY` new answers and on the way out of the
roster, a ceiling or breaker park included, so a stopped listing loses at most
the answers since its last flush and only when the process itself is killed.
A write the filesystem refuses is recorded as ``unkept`` and said, never
raised in place of the listing.

A STORE THAT CANNOT BE READ REFUSES, ``label-listing-kept-unusable``, on the
rule every state document here keeps; deleting it is safe, since it holds
provider answers only.

WHERE IT LIVES. Beside R-1091's release reads, under the installation state
entry ``label_crawl_cache``, one document per label.

Layer: modules.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.label import kept_reads
from cratekit.label.catalogue import artist_name

#: Answers asked now between two writes of the document. Fifty is under a
#: minute of calls at the default pace.
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
    if isinstance(held, bool):
        return None
    if isinstance(held, (int, str)):
        return held
    return None


def release_row(release: Any) -> dict[str, Any]:
    """One provider release as the document stores it."""
    date = getattr(release, "release_date", None)
    copyright_line = getattr(release, "copyright", None) or getattr(release, "label", None) or ""
    credited = []
    for one in getattr(release, "artists", None) or ():
        identity = str(getattr(one, "id", "") or "")
        if identity:
            credited.append(identity)
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
    """What one listing made of its store, for the screen.

    ``reused`` answers came from an earlier run and ``asked`` were asked of the
    provider now; ``stale`` of those were asked because their kept answer was
    too old, and ``changed`` says the store was set aside because the label's
    entry is not the one it was kept for.
    """

    reused: int
    asked: int
    stale: int
    changed: bool
    oldest: datetime | None
    unkept: str
    path: str

    @property
    def age(self) -> str:
        if self.oldest is None:
            return ""
        return kept_reads.age_text(_now() - self.oldest)

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


def _instant(raw: Any) -> datetime | None:
    if not isinstance(raw, str):
        return None
    try:
        moment = datetime.fromisoformat(raw)
    except ValueError:
        return None
    return moment if moment.tzinfo is not None else None


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


class KeptListing:
    """One label's kept listing answers, and what this run made of them."""

    def __init__(
        self,
        label_id: str,
        asked: Mapping[str, Any],
        held: Mapping[str, Mapping[str, Answer]],
        *,
        path: Path,
        changed: bool = False,
    ) -> None:
        self.label_id = label_id
        self.asked_for = dict(asked)
        self.path = path
        self._held: dict[str, dict[str, Answer]] = {
            section: dict(held.get(section, {})) for section in _SECTIONS
        }
        self.changed = changed
        self._unwritten = 0
        self._since = 0
        #: Answers this run asked, read back without counting as reused.
        self._asked_now: set[tuple[str, str]] = set()
        self._reused: set[tuple[str, str]] = set()
        self._stale: set[tuple[str, str]] = set()
        #: Provider answers this run asked for the listing, kept or not. A
        #: listing of many pages is one answer, so this is not a call count;
        #: the gate's spend line is. Zero means no call was made.
        self.asked = 0
        self.oldest: datetime | None = None
        self.unkept = ""

    @classmethod
    def load(cls, entry: Any) -> KeptListing:
        """The label's kept listing, an empty one when none fits, or the refusal."""
        label_id = str(entry.label_id)
        asked = asked_for(entry)
        path = path_for(label_id)
        if not path.exists():
            return cls(label_id, asked, {}, path=path)
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise _unusable(path, "it could not be opened") from exc
        except ValueError as exc:
            raise _unusable(path, "it is not JSON") from exc
        if not isinstance(raw, Mapping):
            raise _unusable(path, f"the document is a {type(raw).__name__}, not a map")
        version = raw.get("version")
        if version != VERSION:
            raise _unusable(
                path, f"it says version {version!r} and this build writes {VERSION}"
            )
        if raw.get("label_id") != label_id:
            raise _unusable(
                path, f"it names the label {raw.get('label_id')!r}, not {label_id!r}"
            )
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
                read_at = _instant(value.get("read_at"))
                if read_at is None:
                    raise _unusable(path, f"the {section} answer {key!r} carries no instant")
                if not _valid(section, value.get("value")):
                    raise _unusable(path, f"the {section} answer {key!r} is malformed")
                held[section][str(key)] = Answer(read_at=read_at, value=value["value"])
        if dict(raw["asked_for"]) != asked:
            # A DIFFERENT QUESTION, NOT A BROKEN DOCUMENT. The registry entry
            # changed since the listing was kept, so nothing in it answers this
            # one and the next write replaces it.
            return cls(label_id, asked, {}, path=path, changed=True)
        return cls(label_id, asked, held, path=path)

    # ── reading ───────────────────────────────────────────────────────────

    def _fresh(self, section: str, key: str) -> Answer | None:
        held = self._held[section].get(key)
        if held is None:
            return None
        if (section, key) in self._asked_now:
            return held
        # AN ANSWER FROM THE FUTURE IS NOT FRESH. A clock set back would
        # otherwise keep it for as long as the clock is wrong.
        if not _young(held):
            self._stale.add((section, key))
            return None
        self._reused.add((section, key))
        if self.oldest is None or held.read_at < self.oldest:
            self.oldest = held.read_at
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
        if held is None:
            return None
        return held.value["found"], held.value["name"]

    def searched(self, query: str) -> tuple[str, ...] | None:
        """The artist identifiers an album search credited, or ``None`` unkept."""
        held = self._fresh(SEARCHED, query)
        return None if held is None else tuple(held.value)

    def has_listing(self, artist_id: str, method: str) -> bool:
        """Whether a fresh listing is held, counting nothing."""
        key = _listing_key(artist_id, method)
        held = self._held[LISTED].get(key)
        if held is None:
            return False
        return (LISTED, key) in self._asked_now or _young(held)

    def listed(self, artist_id: str, method: str) -> list[KeptRelease] | None:
        """One artist's listing of one release method, or ``None`` unkept."""
        held = self._fresh(LISTED, _listing_key(artist_id, method))
        return None if held is None else [_release(one) for one in held.value]

    # ── keeping ───────────────────────────────────────────────────────────

    def asked_unkept(self) -> None:
        """Count a provider call whose answer cannot be kept, so the screen is true."""
        self.asked += 1

    def _keep(self, section: str, key: str, value: Any) -> None:
        self._held[section][key] = Answer(read_at=_now(), value=value)
        self._asked_now.add((section, key))
        self.asked += 1
        self._unwritten += 1
        self._since += 1
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
        self._keep(
            LISTED, _listing_key(artist_id, method), [release_row(one) for one in releases]
        )

    def flush(self) -> None:
        """Write every answer held, whole and atomically, if any is unwritten.

        A WRITE THE FILESYSTEM REFUSES IS SAID, NEVER RAISED, on R-1091's rule:
        the store saves provider calls and holds nothing else, so a refused
        write costs the next run its calls and never this run its listing.
        """
        self._since = 0
        if not self._unwritten:
            return
        document: dict[str, Any] = {
            "version": VERSION,
            "label_id": self.label_id,
            "asked_for": self.asked_for,
        }
        for section in _SECTIONS:
            document[section] = {
                key: {"read_at": held.read_at.isoformat(), "value": held.value}
                for key, held in sorted(self._held[section].items())
            }
        try:
            config.atomic_write_bytes(
                (json.dumps(document, indent=1, sort_keys=True) + "\n").encode("utf-8"),
                self.path,
            )
        except OSError as exc:
            self.unkept = f"{type(exc).__name__}: {exc}"
            return
        self._unwritten = 0
        self.unkept = ""

    def summary(self) -> Summary:
        return Summary(
            reused=self.reused,
            asked=self.asked,
            stale=self.stale,
            changed=self.changed,
            oldest=self.oldest,
            unkept=self.unkept,
            path=str(self.path),
        )


def _young(held: Answer) -> bool:
    return timedelta(0) <= _now() - held.read_at < kept_for()


def _listing_key(artist_id: str, method: str) -> str:
    return f"{artist_id} {method}"


__all__ = [
    "FLUSH_EVERY",
    "UNUSABLE",
    "KeptArtist",
    "KeptListing",
    "KeptRelease",
    "Summary",
    "asked_for",
    "path_for",
    "release_row",
]
