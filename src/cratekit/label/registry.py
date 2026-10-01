"""The curated favourite-label list. Identity is not the display name.

D4 split the source file: this document is installation-scoped intent
(``label_intent``). Per-label last-pulled years live in ``label_watermarks``.
D5 forbids keying a persisted record on a display name, so a rename changes
the name and leaves the identifier (and every watermark keyed on it) alone.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

REGISTRY_VERSION = 1
DEFAULT_TRACK_LIMIT = 400

_SLUG = re.compile(r"[^a-z0-9]+")

#: German letters whose source system spelling is two letters, not the base
#: letter NFKD would leave. ``Schön`` is ``schoen`` there, never ``schon``.
_TRANSLITERATE = str.maketrans(
    {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ẞ": "Ss"}
)


def _fold(text: str) -> str:
    """The fold alone, every run outside ``[a-z0-9]`` to one hyphen."""
    return _SLUG.sub("-", text.lower()).strip("-")


def _legacy_slug(name: str) -> str:
    """The identifier a name got before R-381, the fold with no transliteration.

    Kept for the loader and for :meth:`RegistryStore.add` only, to recognise an
    entry written under it. Nothing new is ever keyed on it.
    """
    return _fold(name)


def slug(name: str) -> str:
    """Stable identifier derived from a name at creation time, never later.

    TRANSLITERATED BEFORE IT FOLDS (R-381). The umlauts and ``ß`` first, then
    NFKD with the combining marks dropped, so ``Sueño`` is ``sueno`` and
    ``Voll Schön`` is ``voll-schoen``, the identifiers the source system used.
    The umlauts go first because NFC gives ``ö`` as one code point, so the table
    catches it before NFKD can split it into ``o`` and a mark.
    """
    composed = unicodedata.normalize("NFC", name).translate(_TRANSLITERATE)
    stripped = "".join(
        char
        for char in unicodedata.normalize("NFKD", composed)
        if not unicodedata.combining(char)
    )
    folded = _fold(stripped)
    if not folded:
        raise refuse(
            "label-name-invalid",
            "a favourite label needs a name that yields an identifier; "
            "an empty or punctuation-only name would collapse every such "
            "entry onto one record",
            steps=("give the label a name with a letter or a digit",),
            scope=Scope.ITEM,
            origin=("label.registry",),
        )
    return folded


#: The one identifier seed shape R-351 defined. ASCII digits only, so a seed
#: stored here is one the adapter's own ``^id:(\d+)$`` reads as an identifier.
_ID_SEED = re.compile(r"id:[0-9]+")


def _field_invalid(message: str, step: str, detail: dict[str, Any]) -> CratekitError:
    return refuse(
        "label-name-invalid",
        message,
        steps=(step,),
        scope=Scope.ITEM,
        origin=("label.registry",),
        detail=detail,
    )


def check_seed(seed: str) -> str:
    """A seed the registry can store, stripped, or a refusal.

    AN ``id:`` SEED THAT IS NOT DIGITS IS REFUSED, NOT STORED AS A NAME. The
    adapter reads anything that is not exactly ``id:<digits>`` as an artist
    name, so ``id:12a`` or ``ID:12`` would be searched for as an act called
    that, match nobody, and refuse the label on every sweep with nothing on the
    screen saying the seed was mistyped.
    """
    text = str(seed).strip()
    if not text:
        raise _field_invalid(
            "a seed artist needs a name or an identifier of the form id:<digits>",
            "pass each seed as an artist name or as id: followed by the provider's digits",
            {"seed": seed},
        )
    if text[:3].casefold() == "id:" and not _ID_SEED.fullmatch(text):
        raise _field_invalid(
            f"the seed {text!r} starts like a provider identifier and is not "
            f"id: followed by digits, so it would be searched for as an artist "
            f"name and match nobody",
            "write the seed as id: followed by the provider artist's digits",
            {"seed": text},
        )
    return text


def check_track_limit(limit: int) -> int:
    """A track limit of one or more, or a refusal. Zero would read as the default."""
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise _field_invalid(
            f"a track limit must be a whole number of one or more, not {limit!r}",
            "pass --track-limit with a positive number",
            {"track_limit": limit},
        )
    return limit


def check_offer(offer: int) -> int:
    """An offer of one or more, or a refusal. Zero would read as the default."""
    if isinstance(offer, bool) or not isinstance(offer, int) or offer < 1:
        raise _field_invalid(
            f"a label's offer must be a whole number of one or more, not {offer!r}",
            "pass --offer with a positive number",
            {"offer": offer},
        )
    return offer


def _checked_seeds(seed_artists: Sequence[str]) -> tuple[str, ...]:
    return tuple(check_seed(seed) for seed in seed_artists)


def _name_key(name: str) -> str:
    """NFC then casefold. Not ``rbxml._folded``, which is NFC and never case."""
    return unicodedata.normalize("NFC", name.strip()).casefold()


def _coerce_int(value: Any) -> int | None:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number


def effective_limit(entry: LabelEntry, default: int = DEFAULT_TRACK_LIMIT) -> int:
    """Per-label newest-N. A last-pulled year is not an input."""
    if entry.track_limit is not None and entry.track_limit > 0:
        return entry.track_limit
    return default


def effective_offer(entry: LabelEntry, default: int) -> int:
    """How many places one sweep of this label fills in review (R-790).

    The entry's own ``offer`` when it set one, else ``default``, which the
    caller takes from ``labels.offer_per_sweep`` in the configuration. Bounded
    by :func:`effective_limit`, because the increment slices to that number
    after the listing, and a window wider than the slice would file fewer than
    it reported and drop the rest without counting them.
    """
    offer = entry.offer if entry.offer is not None and entry.offer > 0 else default
    return min(offer, effective_limit(entry))


@dataclass(frozen=True, slots=True)
class LabelEntry:
    """One followed label. ``label_id`` is the identity; ``name`` is display.

    ``seed_artists`` holds names, or provider identifiers of the form
    ``id:<digits>``. A name is resolved by exact fold. An identifier is
    looked up with no search.
    """

    label_id: str
    name: str
    match: str | None = None
    seed_artists: tuple[str, ...] = ()
    track_limit: int | None = None
    #: This label's own window of releases per sweep, or None for the
    #: configuration's ``labels.offer_per_sweep``. See :func:`effective_offer`.
    offer: int | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "label_id": self.label_id,
            "name": self.name,
            "match": self.match,
            "seed_artists": list(self.seed_artists),
            "track_limit": self.track_limit,
            "offer": self.offer,
        }


@dataclass(frozen=True, slots=True)
class Registry:
    """The intent document, keyed by ``label_id``.

    ``renamed`` is every identifier the loader moved, old to new, kept so a
    library scoped watermark keyed on the old one can follow it later
    (:mod:`cratekit.label.marks`). The registry cannot move those itself, it is
    installation scoped and has no configuration naming a library.
    """

    labels: dict[str, LabelEntry]
    renamed: Mapping[str, str] = field(default_factory=dict)

    def by_id(self, label_id: str) -> LabelEntry | None:
        """The entry, following an R-381 move when the old identifier is free.

        A sweep job queued before the move froze the old identifier as its
        item, and refusing it ``label-unknown`` would send a person to add a
        label literally named that. A held identifier always wins, so an old one
        reused by a new label is that label's.
        """
        found = self.labels.get(label_id)
        if found is None and label_id in self.renamed:
            found = self.labels.get(self.renamed[label_id])
        return found

    def live_renames(self) -> dict[str, str]:
        """The moves still in force, those whose old identifier nobody holds."""
        return {old: new for old, new in self.renamed.items() if old not in self.labels}

    def by_name(self, name: str) -> LabelEntry | None:
        wanted = _name_key(name)
        for entry in self.labels.values():
            if _name_key(entry.name) == wanted:
                return entry
        return None

    def resolve(self, name_or_id: str) -> LabelEntry | None:
        found = self.by_id(name_or_id)
        if found is not None:
            return found
        found = self.by_name(name_or_id)
        if found is not None:
            return found
        return self.by_id(slug(name_or_id)) if name_or_id.strip() else None


def _entry_from(label_id: str, raw: Mapping[str, Any]) -> LabelEntry:
    seeds = raw.get("seed_artists")
    seed_list = tuple(str(item) for item in seeds) if isinstance(seeds, list) else ()
    name = str(raw.get("name") or label_id)
    match = raw.get("match")
    return LabelEntry(
        label_id=str(raw.get("label_id") or label_id),
        name=name,
        match=str(match) if match else None,
        seed_artists=seed_list,
        track_limit=_coerce_int(raw.get("track_limit")),
        offer=_coerce_int(raw.get("offer")),
    )


def recognize(raw: Any) -> Registry:
    """Load a document. Malformed input degrades to empty rather than crashing."""
    if not isinstance(raw, Mapping):
        return Registry(labels={})
    records = raw.get("labels")
    if not isinstance(records, Mapping):
        return Registry(labels={})
    found: dict[str, LabelEntry] = {}
    for key, value in records.items():
        if not isinstance(value, Mapping):
            continue
        entry = _entry_from(str(key), value)
        found[entry.label_id] = entry
    moved = raw.get("renamed")
    renamed = (
        {str(old): str(new) for old, new in moved.items() if isinstance(new, str)}
        if isinstance(moved, Mapping)
        else {}
    )
    return Registry(labels=found, renamed=renamed)


def _migrated_id(entry: LabelEntry) -> str | None:
    """The identifier R-381 moves this entry to, or None if it stays.

    Only an entry whose identifier is EXACTLY the old fold of its own name
    moves. A label renamed since it was created, or one added under an
    identifier the source system chose, was not produced by the old fold and is
    left alone, because a slug is stable once created.
    """
    try:
        new = slug(entry.name)
    except CratekitError:
        return None
    if new == entry.label_id or entry.label_id != _legacy_slug(entry.name):
        return None
    return new


def migrate(held: Registry) -> tuple[Registry, dict[str, str]]:
    """Re-key every entry the old fold produced, and say which moved.

    A NEW IDENTIFIER ALREADY TAKEN IS NOT A MOVE. The entry keeps its old
    identifier, so neither label loses its record or its watermarks, and the
    collision stays visible as an old style identifier rather than a merge.
    Taken means held by another entry now, or by one this pass already moved.
    """
    taken = set(held.labels)
    labels: dict[str, LabelEntry] = {}
    moved: dict[str, str] = {}
    for old, entry in held.labels.items():
        new = _migrated_id(entry)
        if new is None or new in taken:
            labels[old] = entry
            continue
        taken.add(new)
        labels[new] = replace(entry, label_id=new)
        moved[old] = new
    if not moved:
        return held, moved
    return Registry(labels=labels, renamed={**held.renamed, **moved}), moved


def empty() -> Registry:
    return Registry(labels={})


@dataclass(frozen=True, slots=True)
class Adopted:
    """What :meth:`RegistryStore.adopt` did with one offered name.

    ``added`` is False when the registry already held the label, and then
    ``held_name`` is the display name it is held under, which may be a
    different spelling of the offered one. ``refused`` carries the reason a name
    could not become an entry at all, and then ``label_id`` is empty.
    """

    name: str
    label_id: str
    added: bool
    held_name: str | None = None
    refused: str | None = None


class RegistryStore:
    """Locked read-modify-write over the installation-scoped intent file."""

    def __init__(self, *, path=None, lock_path=None) -> None:
        self.path = path if path is not None else config.state_path("label_intent")
        self.lock_path = (
            lock_path if lock_path is not None else config.state_path("label_intent_lock")
        )

    def _unusable(self, what: str) -> CratekitError:
        return refuse(
            "label-intent-unusable",
            f"the favourite-label list at {self.path.name} could not be read "
            f"({what}), so which labels to follow is unknown; treating it as "
            f"empty would drop the curated list on the next save",
            steps=("repair or restore the favourite-label list before editing it",),
            scope=Scope.RUN,
            origin=("label.registry",),
            detail={"problem": what, "path": str(self.path)},
        )

    def load(self) -> Registry:
        """The registry, with every R-381 move made and written.

        A move is written through :meth:`update`, under the lock, so a load
        racing an edit re-reads and re-plans rather than writing a stale copy.
        IF THE MOVE CANNOT BE WRITTEN, THE DOCUMENT IS RETURNED AS STORED.
        Returning the moved view unwritten would hand a caller identifiers the
        file does not hold, and a queued item frozen on one would name a label
        the next process cannot find.
        """
        held = self._read()
        if not migrate(held)[1]:
            return held
        try:
            return self.update(lambda current: False)
        except (CratekitError, OSError):
            return held

    def _read(self) -> Registry:
        if not self.path.exists():
            return empty()
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise self._unusable("it could not be opened") from exc
        except ValueError as exc:
            raise self._unusable("it is not JSON") from exc
        if isinstance(raw, Mapping) and raw.get("version") not in (None, REGISTRY_VERSION):
            raise self._unusable(
                f"it says version {raw.get('version')!r} and this build writes "
                f"{REGISTRY_VERSION}"
            )
        return recognize(raw)

    def _write(self, held: Registry) -> None:
        payload: dict[str, Any] = {
            "version": REGISTRY_VERSION,
            "labels": {key: entry.to_json() for key, entry in held.labels.items()},
        }
        renamed = held.live_renames()
        if renamed:
            # Only when something moved, so a registry R-381 never touched
            # keeps the shape it has always had. A move whose old identifier a
            # new label now holds is dropped, so it can never hand that label's
            # watermark to the label that moved.
            payload["renamed"] = renamed
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2) + "\n").encode("utf-8"),
            self.path,
        )

    def update(self, mutator: Callable[[dict[str, LabelEntry]], bool | None]) -> Registry:
        """Locked read, modify, write. A mutator returning ``False`` writes nothing.

        The opt out is for a caller that may find nothing to change. A rewrite is
        not free even when the entries are equal: ``recognize`` drops a record it
        cannot read, so saving what it loaded discards that record from the file.
        """
        lock = config._exclusive_lock(self.lock_path)
        try:
            lock.__enter__()
        except config.ConfigLockUnavailable as exc:
            raise refuse(
                "label-intent-unusable",
                f"the favourite-label list could not be locked ({exc}), and "
                f"writing it unlocked discards whatever a second edit is "
                f"recording at the same time",
                steps=("make the installation state directory writable by this account",),
                scope=Scope.RUN,
                origin=("label.registry",),
                detail={"lock": str(self.lock_path)},
            ) from exc
        try:
            # The R-381 move is made here, inside the lock, before the mutator
            # sees the entries, and it is written even when the mutator opts out.
            stored, moved = migrate(self._read())
            current = dict(stored.labels)
            changed = mutator(current)
            held = Registry(labels=current, renamed=stored.renamed)
            if changed is not False or moved:
                self._write(held)
            return held
        finally:
            lock.__exit__(None, None, None)

    def add(
        self,
        name: str,
        *,
        match: str | None = None,
        seed_artists: tuple[str, ...] | list[str] = (),
        track_limit: int | None = None,
        offer: int | None = None,
    ) -> str:
        """Add or update by identifier. Re-adding keeps the same ``label_id``.

        Every seed and the limit are checked before the lock is taken, so a
        refused field writes nothing, not even the fields beside it.
        """
        new_id = slug(name)
        seeds = _checked_seeds(seed_artists)
        if track_limit is not None:
            check_track_limit(track_limit)
        if offer is not None:
            check_offer(offer)
        written: list[str] = []

        def mutate(current: dict[str, LabelEntry]) -> None:
            # AN ENTRY THE MIGRATION LEFT UNDER ITS OLD IDENTIFIER IS THIS
            # LABEL, not the one holding the new slug. That is the collision
            # case, and keying on the new slug would overwrite the other label's
            # display name with this one's.
            legacy = current.get(_legacy_slug(name))
            label_id = (
                legacy.label_id
                if legacy is not None and _name_key(legacy.name) == _name_key(name)
                else new_id
            )
            written.append(label_id)
            existing = current.get(label_id)
            current[label_id] = LabelEntry(
                label_id=label_id,
                name=name,
                match=match if match is not None else (existing.match if existing else None),
                seed_artists=seeds if seeds else (
                    existing.seed_artists if existing else ()
                ),
                track_limit=track_limit if track_limit is not None else (
                    existing.track_limit if existing else None
                ),
                offer=offer if offer is not None else (existing.offer if existing else None),
            )

        self.update(mutate)
        return written[-1]

    def adopt(self, names: Sequence[str]) -> tuple[Adopted, ...]:
        """Add each name the registry does not already hold, under one lock.

        NOT :meth:`add`, which re-adds by identifier and overwrites the display
        name a person chose. A name is PRESENT when it resolves the way every
        other verb resolves one: by identifier, by folded display name, then by
        its slug. The fold is what R-381 made load bearing. A label carried over
        under an identifier the source system chose, which need not be what
        :func:`slug` derives from its name, would be filed a second time by a
        check on the slug alone, with watermarks nobody can see from the first.

        Resolution is against the registry AS IT STANDS INSIDE THE LOCK, entries
        this call has already added included, so two spellings of one label in
        one batch add it once, and a concurrent add is seen rather than doubled.
        A name that yields no identifier is refused on its own and the rest
        still land.
        """
        results: list[Adopted] = []

        def mutate(current: dict[str, LabelEntry]) -> bool:
            results.clear()
            for raw in names:
                name = str(raw).strip()
                try:
                    label_id = slug(name)
                except CratekitError as exc:
                    results.append(
                        Adopted(name=name, label_id="", added=False, refused=exc.cause.reason)
                    )
                    continue
                held = Registry(labels=current).resolve(name)
                if held is not None:
                    results.append(
                        Adopted(
                            name=name,
                            label_id=held.label_id,
                            added=False,
                            held_name=held.name,
                        )
                    )
                    continue
                current[label_id] = LabelEntry(label_id=label_id, name=name)
                results.append(Adopted(name=name, label_id=label_id, added=True))
            # NOTHING ADDED, NOTHING WRITTEN, so a second run leaves the file
            # byte for byte as it found it. See :meth:`update` for why a rewrite
            # of equal entries is not harmless.
            return any(result.added for result in results)

        self.update(mutate)
        return tuple(results)

    def edit(
        self,
        name_or_id: str,
        *,
        match: str | None = None,
        seed_artists: Sequence[str] | None = None,
        track_limit: int | None = None,
        offer: int | None = None,
    ) -> LabelEntry:
        """Change the given fields of a held entry and keep every other one.

        Not ``update``, which is the locked read, modify, write this calls. The
        entry is resolved INSIDE the lock, by identifier or display name, so a
        concurrent remove is a refusal rather than a resurrection. A name that
        resolves nothing refuses rather than creating an entry, which is what
        separates this from :meth:`add`.
        """
        seeds = _checked_seeds(seed_artists) if seed_artists is not None else None
        if track_limit is not None:
            check_track_limit(track_limit)
        if offer is not None:
            check_offer(offer)
        edited: list[LabelEntry] = []

        def mutate(current: dict[str, LabelEntry]) -> None:
            existing = Registry(labels=current).resolve(name_or_id)
            if existing is None:
                raise refuse(
                    "label-unknown",
                    f"no favourite label is named {name_or_id!r}",
                    steps=("list the registry and take the identifier from it",),
                    scope=Scope.ITEM,
                    origin=("label.registry",),
                    detail={"name": name_or_id},
                )
            entry = replace(
                existing,
                match=match if match is not None else existing.match,
                seed_artists=seeds if seeds is not None else existing.seed_artists,
                track_limit=track_limit if track_limit is not None else existing.track_limit,
                offer=offer if offer is not None else existing.offer,
            )
            current[existing.label_id] = entry
            edited.append(entry)

        self.update(mutate)
        return edited[0]

    def rename(self, label_id: str, new_name: str) -> LabelEntry:
        """Change the display name. The identifier, and its watermarks, stay."""

        def mutate(current: dict[str, LabelEntry]) -> None:
            existing = current.get(label_id)
            if existing is None:
                raise refuse(
                    "label-unknown",
                    f"no favourite label has the identifier {label_id!r}",
                    steps=("list the registry and take the identifier from it",),
                    scope=Scope.ITEM,
                    origin=("label.registry",),
                    detail={"label_id": label_id},
                )
            current[label_id] = replace(existing, name=new_name)

        return self.update(mutate).by_id(label_id)

    def remove(self, name_or_id: str) -> bool:
        held = self.load()
        entry = held.resolve(name_or_id)
        if entry is None:
            return False

        def mutate(current: dict[str, LabelEntry]) -> None:
            current.pop(entry.label_id, None)

        self.update(mutate)
        return True
