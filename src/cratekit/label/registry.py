"""The curated favourite-label list. Identity is not the display name.

Installation scoped intent (``label_intent``, D4); per label watermarks live
elsewhere. No record is keyed on a display name (D5), so a rename leaves the
identifier, and every watermark keyed on it, alone.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass, field, replace
from typing import Any
from urllib.parse import urlsplit

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.taxonomy import KIND_NAME

REGISTRY_VERSION = 1
DEFAULT_TRACK_LIMIT = 400

_SLUG = re.compile(r"[^a-z0-9]+")

#: German letters whose source system spelling is two letters, not the base
#: letter NFKD would leave. ``Schön`` is ``schoen`` there, never ``schon``.
_TRANSLITERATE = str.maketrans(
    {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ẞ": "Ss"}
)


def _fold(text: str) -> str:
    """The fold alone, every run outside ``[a-z0-9]`` to one hyphen.

    Of a name as typed, it is the identifier that name got before R-381, asked only
    to recognise an entry written under it.
    """
    return _SLUG.sub("-", text.lower()).strip("-")


def slug(name: str) -> str:
    """Stable identifier derived from a name at creation time, never later.

    Transliterated before it folds (R-381): the umlauts and ``ß`` first, on the
    NFC form so ``ö`` is one code point, then NFKD with combining marks dropped,
    so ``Voll Schön`` is ``voll-schoen`` as the source system had it.
    """
    composed = unicodedata.normalize("NFC", name).translate(_TRANSLITERATE)
    stripped = "".join(
        char
        for char in unicodedata.normalize("NFKD", composed)
        if not unicodedata.combining(char)
    )
    folded = _fold(stripped)
    if not folded:
        raise _refused(
            "label-name-invalid",
            "a favourite label needs a name that yields an identifier; "
            "an empty or punctuation-only name would collapse every such "
            "entry onto one record",
            "give the label a name with a letter or a digit",
        )
    return folded


#: The one identifier seed shape (R-351), ASCII digits only, as the adapter reads it.
_ID_SEED = re.compile(r"id:[0-9]+")


def _refused(reason: str, message: str, *steps: str, **kwargs: Any) -> CratekitError:
    """A refusal raised by this module, its steps given in order, one item by default."""
    kwargs.setdefault("scope", Scope.ITEM)
    return refuse(reason, message, steps=steps, origin=("label.registry",), **kwargs)


def _field_invalid(message: str, step: str, detail: dict[str, Any]) -> CratekitError:
    return _refused("label-name-invalid", message, step, detail=detail)


def check_seed(seed: str) -> str:
    """A seed the registry can store, stripped, or a refusal.

    An ``id:`` seed that is not digits is refused rather than stored as a name,
    which would be searched for as an act and match nobody on every sweep.
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


def check_kind(kind: str) -> str:
    """A label's kind, folded, or a refusal for a value that could never be one.

    The shape only: which kinds exist is the library's taxonomy's to say, checked
    by the verb that sets one (R-798).
    """
    folded = kind.strip().lower() if isinstance(kind, str) else ""
    if not KIND_NAME.fullmatch(folded):
        raise _field_invalid(
            f"a label's kind is a single word such as dance or rnb, not {kind!r}",
            "pass --kind with one of the kinds the library's taxonomy names, or any",
            {"kind": kind},
        )
    return folded


#: The longest genre a label may carry, short enough that a pasted paragraph is refused.
GENRE_MAX = 64


def check_genre(genre: str) -> str:
    """A label's genre, stripped and composed, or a refusal for a value that could never be one.

    The shape only, as for a kind (U178). Kept as typed, since it is the word
    written onto every file of the label. One line with a letter or a digit.
    """
    text = unicodedata.normalize("NFC", genre.strip()) if isinstance(genre, str) else ""
    if (
        not text
        or len(text) > GENRE_MAX
        or not any(char.isalnum() for char in text)
        or any(unicodedata.category(char).startswith("C") for char in text)
    ):
        raise _field_invalid(
            f"a label's genre is one line of at most {GENRE_MAX} characters with a "
            f"letter or a digit in it, such as Rominimal, not {genre!r}",
            "pass --genre with the genre every track of this label should carry",
            {"genre": genre},
        )
    return text


#: A Bandcamp seller account as the registry keeps it: the name in its address,
#: ``pulsromania`` for ``pulsromania.bandcamp.com``, or the whole host of a seller
#: on its own domain, dot separated as a host name is.
_ACCOUNT = re.compile(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)*")

#: The suffix of a seller account's own address, as a purchase's seller is read.
_ACCOUNT_HOST = ".bandcamp.com"


def bandcamp_account(account: str) -> str:
    """The seller account ``account`` names, as a purchase's seller is read (U177).

    ``PulsRomania``, ``pulsromania.bandcamp.com`` and its https address are all
    ``pulsromania``; a seller on its own domain keeps the whole host. Anything
    else is refused, since it would match no purchase.
    """
    text = account.strip().lower() if isinstance(account, str) else ""
    if "/" in text:
        host = urlsplit(text if "://" in text else f"https://{text}").hostname or ""
    else:
        host = text
    if host.endswith(_ACCOUNT_HOST):
        host = host[: -len(_ACCOUNT_HOST)]
    if not host or not _ACCOUNT.fullmatch(host):
        raise _field_invalid(
            f"a label's Bandcamp account is the name in the address of its "
            f"releases, such as pulsromania for pulsromania.bandcamp.com, not "
            f"{account!r}",
            "pass --bandcamp with the account name, or the address of the label's page",
            {"bandcamp": account},
        )
    return host


def _checked_seeds(seed_artists: Sequence[str]) -> tuple[str, ...]:
    return tuple(check_seed(seed) for seed in seed_artists)


def _checked(
    match: str | None, seeds: tuple[str, ...] | None, track_limit: int | None,
    offer: int | None, kind: str | None, genre: str | None, bandcamp: str | None,
    cleared: Mapping[str, bool],
) -> tuple[dict[str, Any], str | None]:
    """Check every given field before a lock is taken: the changes, and the account as stored.

    The changes are what ``replace`` takes: a None field keeps what is held, and a
    field ``cleared`` flags is the way back to None.
    """
    if track_limit is not None:
        check_track_limit(track_limit)
    if offer is not None:
        check_offer(offer)
    given = {
        "match": match,
        "seed_artists": seeds,
        "track_limit": track_limit,
        "offer": offer,
        "kind": check_kind(kind) if kind is not None else None,
        "genre": check_genre(genre) if genre is not None else None,
        "bandcamp": bandcamp_account(bandcamp) if bandcamp is not None else None,
    }
    changes = {key: value for key, value in given.items() if value is not None}
    changes.update((key, None) for key, clear in cleared.items() if clear)
    return changes, given["bandcamp"]


def _name_key(name: str) -> str:
    """NFC then casefold. Not ``rbxml._folded``, which is NFC and never case."""
    return unicodedata.normalize("NFC", name.strip()).casefold()


def _coerce_int(value: Any) -> int | None:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def effective_limit(entry: LabelEntry, default: int = DEFAULT_TRACK_LIMIT) -> int:
    """Per-label newest-N. A last-pulled year is not an input."""
    limit = entry.track_limit
    return limit if limit is not None and limit > 0 else default


def effective_offer(entry: LabelEntry, default: int) -> int:
    """How many places one sweep of this label fills in review (R-790).

    The entry's own ``offer``, else ``default`` from ``labels.offer_per_sweep``,
    bounded by :func:`effective_limit`, the slice the increment takes after.
    """
    offer = entry.offer if entry.offer is not None and entry.offer > 0 else default
    return min(offer, effective_limit(entry))


@dataclass(frozen=True, slots=True)
class LabelEntry:
    """One followed label. ``label_id`` is the identity; ``name`` is display.

    ``seed_artists`` holds names, resolved by exact fold, or ``id:<digits>``
    identifiers, looked up with no search.
    """

    label_id: str
    name: str
    match: str | None = None
    seed_artists: tuple[str, ...] = ()
    track_limit: int | None = None
    #: This label's own window per sweep, or None for ``labels.offer_per_sweep``.
    offer: int | None = None
    #: The kind of music the genre gate passes (R-798), or None for the taxonomy's
    #: default. Folded lowercase and checked by the verb that sets it.
    kind: str | None = None
    #: The genre every file of this label is tagged with when it has none, or None
    #: (U178). Kept as typed and checked by the verb that sets it.
    genre: str | None = None
    #: The Bandcamp seller account this label's releases are sold from, or None
    #: (U177), one per label and one label per account, in :func:`bandcamp_account` form.
    bandcamp: str | None = None

    def to_json(self) -> dict[str, Any]:
        return {**asdict(self), "seed_artists": list(self.seed_artists)}


@dataclass(frozen=True, slots=True)
class Registry:
    """The intent document, keyed by ``label_id``.

    ``renamed`` is every identifier the loader moved, old to new, so a library
    scoped watermark can follow it later (:mod:`cratekit.label.marks`).
    """

    labels: dict[str, LabelEntry]
    renamed: Mapping[str, str] = field(default_factory=dict)

    def by_id(self, label_id: str) -> LabelEntry | None:
        """The entry, following an R-381 move when the old identifier is free.

        A job queued before the move froze the old identifier; a held identifier
        always wins.
        """
        found = self.labels.get(label_id)
        if found is None and label_id in self.renamed:
            found = self.labels.get(self.renamed[label_id])
        return found

    def live_renames(self) -> dict[str, str]:
        """The moves still in force, those whose old identifier nobody holds."""
        return {old: new for old, new in self.renamed.items() if old not in self.labels}

    def by_name(self, name: str) -> LabelEntry | None:
        return next(iter(self.named(name)), None)

    def named(self, name: str) -> tuple[LabelEntry, ...]:
        """Every label whose display name is ``name``, in registry order.

        ``rename`` allows two; a caller that must not guess asks this (R-1476).
        """
        wanted = _name_key(name)
        return tuple(entry for entry in self.labels.values() if _name_key(entry.name) == wanted)

    def claimants(self, account: str) -> tuple[LabelEntry, ...]:
        """Every label naming ``account`` as its Bandcamp seller, in registry order.

        Two can only be a hand edited file, and a caller reads two as no label (U177).
        """
        try:
            wanted = bandcamp_account(account)
        except CratekitError:
            return ()
        return tuple(entry for entry in self.labels.values() if entry.bandcamp == wanted)

    def by_bandcamp(self, account: str) -> LabelEntry | None:
        """The one label sold from ``account``, or None for none or for two."""
        found = self.claimants(account)
        return found[0] if len(found) == 1 else None

    def of_genre(self, genre: str) -> tuple[LabelEntry, ...]:
        """Every label whose genre is ``genre``, in registry order (U341).

        Matched NFC then casefold, as a name is, so the group a person typed
        one way is the group set another.
        """
        wanted = _name_key(genre)
        return tuple(
            entry for entry in self.labels.values()
            if entry.genre is not None and _name_key(entry.genre) == wanted
        )

    def genres(self) -> tuple[str, ...]:
        """Each genre the labels carry once, as its first label spells it, in registry order."""
        held: dict[str, str] = {}
        for entry in self.labels.values():
            if entry.genre is not None:
                held.setdefault(_name_key(entry.genre), entry.genre)
        return tuple(held.values())

    def resolve(self, name_or_id: str) -> LabelEntry | None:
        found = self.by_id(name_or_id) or self.by_name(name_or_id)
        if found is not None or not name_or_id.strip():
            return found
        return self.by_id(slug(name_or_id))


def _entry_from(label_id: str, raw: Mapping[str, Any]) -> LabelEntry:
    seeds, match = raw.get("seed_artists"), raw.get("match")
    kind, genre = raw.get("kind"), raw.get("genre")
    return LabelEntry(
        bandcamp=_stored_account(raw.get("bandcamp")),
        label_id=str(raw.get("label_id") or label_id),
        name=str(raw.get("name") or label_id),
        match=str(match) if match else None,
        seed_artists=tuple(str(item) for item in seeds) if isinstance(seeds, list) else (),
        track_limit=_coerce_int(raw.get("track_limit")),
        offer=_coerce_int(raw.get("offer")),
        kind=kind.strip().lower() or None if isinstance(kind, str) else None,
        genre=genre.strip() or None if isinstance(genre, str) else None,
    )


def _stored_account(value: Any) -> str | None:
    """A stored account in purchase form, or None for none or a malformed one.

    A malformed one is no account rather than a crash, as ``recognize`` degrades
    every field it cannot read.
    """
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return bandcamp_account(value)
    except CratekitError:
        return None


def recognize(raw: Any) -> Registry:
    """Load a document. Malformed input degrades to empty rather than crashing."""
    records = raw.get("labels") if isinstance(raw, Mapping) else None
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

    Only an identifier exactly the old fold of its own name moves; a slug is
    stable once created.
    """
    try:
        new = slug(entry.name)
    except CratekitError:
        return None
    if new == entry.label_id or entry.label_id != _fold(entry.name):
        return None
    return new


def migrate(held: Registry) -> tuple[Registry, dict[str, str]]:
    """Re-key every entry the old fold produced, and say which moved.

    A new identifier already taken, now or by an earlier move in this pass, is
    not a move: the entry keeps its old one, so no record merges.
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

    ``added`` is False when already held, under ``held_name``. ``refused`` is why
    a name could not become an entry, and then ``label_id`` is empty.
    """

    name: str
    label_id: str
    added: bool
    held_name: str | None = None
    refused: str | None = None


#: The ``--bandcamp`` word that clears a label's account, as for ``--kind`` and
#: ``--genre``. Matched as typed, so an account named that is set by its address.
CLEAR_BANDCAMP = "default"


def _claim(current: Mapping[str, LabelEntry], label_id: str, account: str | None) -> None:
    """Refuse ``account`` when a label other than ``label_id`` already names it (U177).

    Checked inside the lock against the entries as they stand, so two concurrent
    sets of one account cannot both land.
    """
    if account is None:
        return
    for other in current.values():
        if other.label_id != label_id and other.bandcamp == account:
            raise _refused(
                "label-name-invalid",
                f"the Bandcamp account {account} is already the seller of the label "
                f"{other.name} ({other.label_id}), and one account names one label, "
                f"so nothing was changed",
                f"clear it there first with crate label registry set "
                f"{other.label_id} --bandcamp {CLEAR_BANDCAMP}, or name another account",
                detail={"bandcamp": account, "held_by": other.label_id},
            )


class RegistryStore:
    """Locked read-modify-write over the installation-scoped intent file."""

    def __init__(self, *, path=None, lock_path=None) -> None:
        self.path = path if path is not None else config.state_path("label_intent")
        self.lock_path = (
            lock_path if lock_path is not None else config.state_path("label_intent_lock")
        )

    def _unusable(self, what: str) -> CratekitError:
        return _refused(
            "label-intent-unusable",
            f"the favourite-label list at {self.path.name} could not be read "
            f"({what}), so which labels to follow is unknown; treating it as "
            f"empty would drop the curated list on the next save",
            "repair or restore the favourite-label list before editing it",
            scope=Scope.RUN,
            detail={"problem": what, "path": str(self.path)},
        )

    def load(self) -> Registry:
        """The registry, with every R-381 move made and written under the lock.

        If the move cannot be written, the document is returned as stored, never an
        unwritten view naming identifiers the file does not hold.
        """
        held = self._read()
        if not migrate(held)[1]:
            return held
        try:
            return self.update(lambda current: False)
        except (CratekitError, OSError):
            return held

    def _read(self) -> Registry:
        found, raw = config.read_json(self.path, self._unusable)
        if not found:
            return empty()
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
            # Only when something moved. A move whose old identifier a new label holds is
            # dropped, so it can never hand that label's watermark over.
            payload["renamed"] = renamed
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2) + "\n").encode("utf-8"),
            self.path,
        )

    def update(self, mutator: Callable[[dict[str, LabelEntry]], bool | None]) -> Registry:
        """Locked read, modify, write. A mutator returning ``False`` writes nothing.

        A rewrite is not free: ``recognize`` drops a record it cannot read.
        """
        lock = config.exclusive_lock(self.lock_path)
        try:
            lock.__enter__()
        except config.ConfigLockUnavailable as exc:
            raise _refused(
                "label-intent-unusable",
                f"the favourite-label list could not be locked ({exc}), and "
                f"writing it unlocked discards whatever a second edit is "
                f"recording at the same time",
                "make the installation state directory writable by this account",
                scope=Scope.RUN,
                detail={"lock": str(self.lock_path)},
            ) from exc
        try:
            # The R-381 move is made inside the lock and written even when the mutator opts out.
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
        kind: str | None = None,
        clear_kind: bool = False,
        genre: str | None = None,
        clear_genre: bool = False,
        bandcamp: str | None = None,
        clear_bandcamp: bool = False,
    ) -> str:
        """Add or update by identifier. Re-adding keeps the same ``label_id``.

        Every field is checked before the lock, so a refused one writes nothing.
        """
        new_id = slug(name)
        seeds = _checked_seeds(seed_artists)
        changes, bandcamp = _checked(
            match, seeds or None, track_limit, offer, kind, genre, bandcamp,
            {"kind": clear_kind, "genre": clear_genre, "bandcamp": clear_bandcamp},
        )
        written: list[str] = []

        def mutate(current: dict[str, LabelEntry]) -> None:
            # An entry the migration left under its old identifier is this label, not
            # the one holding the new slug.
            legacy = current.get(_fold(name))
            label_id = (
                legacy.label_id
                if legacy is not None and _name_key(legacy.name) == _name_key(name)
                else new_id
            )
            written.append(label_id)
            held = current.get(label_id) or LabelEntry(label_id=label_id, name=name)
            _claim(current, label_id, bandcamp)
            current[label_id] = replace(held, name=name, **changes)

        self.update(mutate)
        return written[-1]

    def adopt(self, names: Sequence[str]) -> tuple[Adopted, ...]:
        """Add each name the registry does not already hold, under one lock.

        Not :meth:`add`, which overwrites a display name. A name is present when it
        resolves as every verb resolves one, against the registry inside the lock,
        this batch included, so two spellings add once. A name yielding no
        identifier is refused alone.
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
                        Adopted(name=name, label_id=held.label_id, added=False, held_name=held.name)
                    )
                    continue
                current[label_id] = LabelEntry(label_id=label_id, name=name)
                results.append(Adopted(name=name, label_id=label_id, added=True))
            # Nothing added, nothing written, so a second run leaves the file as it was.
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
        kind: str | None = None,
        clear_kind: bool = False,
        genre: str | None = None,
        clear_genre: bool = False,
        bandcamp: str | None = None,
        clear_bandcamp: bool = False,
    ) -> LabelEntry:
        """Change the given fields of a held entry and keep every other one.

        Resolved inside the lock, so a concurrent remove is a refusal, and a name
        resolving nothing refuses rather than creating an entry.
        """
        seeds = _checked_seeds(seed_artists) if seed_artists is not None else None
        changes, bandcamp = _checked(
            match, seeds, track_limit, offer, kind, genre, bandcamp,
            {"kind": clear_kind, "genre": clear_genre, "bandcamp": clear_bandcamp},
        )
        edited: list[LabelEntry] = []

        def mutate(current: dict[str, LabelEntry]) -> None:
            existing = Registry(labels=current).resolve(name_or_id)
            if existing is None:
                raise _refused(
                    "label-unknown",
                    f"no favourite label is named {name_or_id!r}",
                    "list the registry and take the identifier from it",
                    detail={"name": name_or_id},
                )
            _claim(current, existing.label_id, bandcamp)
            entry = replace(existing, **changes)
            current[existing.label_id] = entry
            edited.append(entry)

        self.update(mutate)
        return edited[0]

    def rename(self, label_id: str, new_name: str) -> LabelEntry:
        """Change the display name. The identifier, and its watermarks, stay."""

        def mutate(current: dict[str, LabelEntry]) -> None:
            existing = current.get(label_id)
            if existing is None:
                raise _refused(
                    "label-unknown",
                    f"no favourite label has the identifier {label_id!r}",
                    "list the registry and take the identifier from it",
                    detail={"label_id": label_id},
                )
            current[label_id] = replace(existing, name=new_name)

        return self.update(mutate).by_id(label_id)

    def remove(self, name_or_id: str) -> bool:
        entry = self.load().resolve(name_or_id)
        if entry is None:
            return False
        self.update(lambda current: current.pop(entry.label_id, None) and None)
        return True
