"""The playlist pairs: which account playlist stays the same list as which rekordbox one.

U130. A PAIR is one of the author's account playlists and one rekordbox
playlist, kept the same list by ``crate sync pair``; this is the record of each
and of what each side held at its last sync, the base ``sync/pair_merge.py``
merges against. BY IDENTIFIER, BOTH SIDES, NEVER BY NAME (R-906), one to one.

A MARK IS WRITTEN WHEN THE FIRST SYNC IS APPROVED, A SNAPSHOT ONLY ONCE BOTH
SIDES WERE WRITTEN AND READ BACK WHOLE, so a first sync failing part way is
still a first one, which adds only. :func:`paired` is the account's second
question before a removal: a marked playlist's removals were asked for.

Beside the pairs (U198): the root folders a sync made or adopted, with what an
adopted one held (U216); the rows the account had no track for; and the
playlists a made pair left behind, so nothing makes their partner again. A pair
also holds the account's added dates (U202), a twin's hold (U221) and the
readings an order waits on (U231, U234). Still version 2: a copy that drops a
field it does not know costs a pair read by time, never a playlist made twice.

Layer: modules.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.cli.output import timestamp
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

#: 2 since U198. A copy built before it refuses the document rather than
#: rewriting it without what U198 records, which would make a released
#: playlist again. Version 1 is still read.
PAIRS_VERSION = 2
READ_VERSIONS = (1, 2)

_ORIGIN = ("outbound", "pairs")


def _ids(value: Any) -> bool:
    """Whether ``value`` is a list of identifiers, none empty."""
    return isinstance(value, list) and all(isinstance(one, str) and one for one in value)


def _moment(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _id_map(value: Any, *, words: bool = False) -> bool:
    """Whether ``value`` maps identifiers to text, empty text only when ``words``."""
    return isinstance(value, Mapping) and all(
        isinstance(k, str) and k and isinstance(v, str) and (words or v) for k, v in value.items()
    )


@dataclass(frozen=True, slots=True)
class Membership:
    """One rekordbox membership as a snapshot holds it: the track and its row."""

    content_id: str
    row_id: str

    def to_json(self) -> list[str]:
        return [self.content_id, self.row_id]


@dataclass(frozen=True, slots=True)
class StopReading:
    """The account's order as plans read it after one run's order stopped part way (U234).

    ``order`` was first read at ``at``; ``settled`` says a plan at least the
    agreement window later read the same order, so the provider no longer
    moves it. ``after`` is a later order differing from a settled one, first
    read at ``after_at``, the person's reorder once it settles in turn.
    """

    run: str
    order: tuple[str, ...]
    at: str
    settled: bool = False
    after: tuple[str, ...] | None = None
    after_at: str = ""

    def to_json(self) -> dict[str, Any]:
        record: dict[str, Any] = {
            "run": self.run, "order": list(self.order), "at": self.at, "settled": self.settled
        }
        if self.after is not None:
            record["after"] = {"order": list(self.after), "at": self.after_at}
        return record


@dataclass(frozen=True, slots=True)
class Pair:
    """One pair and what each side held when its last sync finished.

    ``account`` and ``rekordbox`` are None for a side no sync has recorded.
    ``links`` maps a remote track to the content row it was matched with, so a
    later sync does not match the same track twice.
    """

    account_id: str
    rekordbox_id: str
    name: str
    marked: str
    synced: str = ""
    account: tuple[str, ...] | None = None
    rekordbox: tuple[Membership, ...] | None = None
    links: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))
    #: The product made the rekordbox side as a custom playlist twin (U149), so
    #: a sync unpairs it once the account playlist is gone.
    twin: bool = False
    #: The product made the account side in root folder ``folder`` (U198), so a
    #: sync unpairs it once either side is gone.
    made: bool = False
    folder: str = ""
    #: U202. When the account says each track of the last whole sync's account
    #: side was added, by remote identifier. A later date on a track the base
    #: held is that track taken out and put back since (R-990).
    account_added: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))
    #: U221. The account tracks a twin was made without, never queued, remote
    #: identifier to the words a person reads. Empty for a twin holding
    #: nothing; None when no hold was recorded, which ``sync pair`` reads by time.
    on_hold: Mapping[str, str] | None = None
    #: U231. The account playlist's order as read after a pending order's moves
    #: last served it, and when, which a later reading must agree with before
    #: anything moves. Cleared once the snapshot moves.
    seen: tuple[str, ...] | None = None
    seen_at: str = ""
    #: U234. The order as plans read it after a write on this pair stopped part
    #: way, so a person's later order is told from the provider's partial
    #: state. Cleared once the snapshot moves.
    stop_seen: StopReading | None = None

    @property
    def first(self) -> bool:
        """Whether no side of this pair has a snapshot yet."""
        return self.account is None and self.rekordbox is None

    def to_json(self) -> dict[str, Any]:
        record: dict[str, Any] = {
            "rekordbox_id": self.rekordbox_id,
            "name": self.name,
            "marked": self.marked,
            "synced": self.synced,
            "links": dict(sorted(self.links.items())),
        }
        if self.twin:
            record["twin"] = True
        if self.made:
            record["made"] = True
            record["folder"] = self.folder
        if self.account is not None:
            record["account"] = list(self.account)
        if self.account_added:
            record["account_added"] = dict(sorted(self.account_added.items()))
        if self.rekordbox is not None:
            record["rekordbox"] = [member.to_json() for member in self.rekordbox]
        if self.on_hold is not None:
            record["on_hold"] = dict(sorted(self.on_hold.items()))
        if self.seen is not None:
            record["seen"] = {"order": list(self.seen), "at": self.seen_at}
        if self.stop_seen is not None:
            record["stop_seen"] = self.stop_seen.to_json()
        return record


#: The two sides a released playlist is recorded under.
ACCOUNT_SIDE = "account"
REKORDBOX_SIDE = "rekordbox"


@dataclass(frozen=True, slots=True)
class MadeFolder:
    """One account root folder a sync of every pair made or adopted (U198)."""

    name: str
    folder_id: str
    #: True only when this product created it; one adopted by its name may be a person's.
    created: bool = False
    #: U216. The account playlists an adopted folder held, which no sync brings
    #: to rekordbox. Empty for one created here; None for one recorded before.
    held: frozenset[str] | None = None


@dataclass(frozen=True, slots=True)
class Miss:
    """What the account said of one rekordbox row it had no track for, and under which ISRC."""

    isrc: str
    reason: str


@dataclass(frozen=True, slots=True)
class Released:
    """Playlists left behind when a made pair lost its other side (U198)."""

    #: Account playlists whose rekordbox playlist was deleted.
    account: frozenset[str] = frozenset()
    #: Rekordbox playlists whose account playlist was deleted.
    rekordbox: frozenset[str] = frozenset()


@dataclass
class Document:
    """The whole pairs document as read: the pairs and what U198 records beside them."""

    pairs: dict[str, Pair] = field(default_factory=dict)
    folders: dict[str, MadeFolder] = field(default_factory=dict)
    misses: dict[str, Miss] = field(default_factory=dict)
    released: Released = field(default_factory=Released)


class PairStore:
    """The locked document of every pair for one library."""

    def __init__(self, cfg: config.Config) -> None:
        self.cfg = cfg
        self.path: Path = config.state_path("playlist_pairs", cfg)
        self.lock_path: Path = config.state_path("playlist_pairs_lock", cfg)

    def _unusable(self, what: str) -> CratekitError:
        return refuse(
            "sync-pair-store-unusable",
            f"the playlist pairs at {self.path.name} could not be read ({what}), so "
            f"what each pair held at its last sync is unknown; reading it as empty "
            f"would make every pair's next sync a first one and would mark a pair "
            f"twice",
            steps=("repair or restore the playlist pairs document before syncing a pair",),
            scope=Scope.RUN,
            origin=_ORIGIN,
            detail={"problem": what, "path": str(self.path)},
        )

    def _locked(self):
        return config.held(
            self.lock_path,
            lambda exc: refuse(
                "sync-pair-store-unusable",
                f"the playlist pairs could not be locked ({exc}), and recording a "
                f"snapshot unlocked discards whatever a second sync is recording "
                f"at the same time",
                steps=("make the library's state directory writable by this account",),
                scope=Scope.RUN,
                origin=_ORIGIN,
                detail={"lock": str(self.lock_path)},
            ),
        )

    def _load(self) -> dict[str, Pair]:
        return self._document().pairs

    def _document(self) -> Document:
        found, raw = config.read_json(self.path, self._unusable)
        if not found:
            return Document()
        pairs = self._recognize(raw)
        return Document(
            pairs=pairs,
            folders=self._folders(raw.get("folders", {})),
            misses=self._misses(raw.get("misses", {})),
            released=self._released(raw.get("released", {})),
        )

    def _folders(self, raw: Any) -> dict[str, MadeFolder]:
        if not isinstance(raw, Mapping):
            raise self._unusable("its folders are not a map")
        found: dict[str, MadeFolder] = {}
        for name, value in raw.items():
            if (
                not isinstance(value, Mapping)
                or not isinstance(value.get("folder_id"), str)
                or not value.get("folder_id")
                or not isinstance(value.get("created", False), bool)
            ):
                raise self._unusable(f"the folder {name!r} is not a recorded folder")
            held = value.get("held")
            if held is not None and not _ids(held):
                raise self._unusable(f"what the folder {name!r} held is not playlist ids")
            found[str(name)] = MadeFolder(
                str(name), str(value["folder_id"]), value.get("created") is True,
                None if held is None else frozenset(held),
            )
        return found

    def _misses(self, raw: Any) -> dict[str, Miss]:
        if not isinstance(raw, Mapping):
            raise self._unusable("its misses are not a map")
        found: dict[str, Miss] = {}
        for content_id, value in raw.items():
            if (
                not isinstance(value, Mapping)
                or not isinstance(value.get("isrc"), str)
                or not isinstance(value.get("reason"), str)
            ):
                raise self._unusable(f"the miss of row {content_id!r} is not a recorded miss")
            found[str(content_id)] = Miss(str(value["isrc"]), str(value["reason"]))
        return found

    def _released(self, raw: Any) -> Released:
        if not isinstance(raw, Mapping):
            raise self._unusable("its released playlists are not a map")
        sides: dict[str, frozenset[str]] = {}
        for side in (ACCOUNT_SIDE, REKORDBOX_SIDE):
            ids = raw.get(side, [])
            if not _ids(ids):
                raise self._unusable(f"its released {side} playlists are not ids")
            sides[side] = frozenset(ids)
        return Released(account=sides[ACCOUNT_SIDE], rekordbox=sides[REKORDBOX_SIDE])

    def _recognize(self, raw: Any) -> dict[str, Pair]:
        if not isinstance(raw, Mapping):
            raise self._unusable(f"the document is a {type(raw).__name__}, not a pair map")
        if raw.get("version") not in READ_VERSIONS:
            raise self._unusable(
                f"it says version {raw.get('version')!r} and this build writes {PAIRS_VERSION}"
            )
        if raw.get("library_id") != self.cfg.library.volume_id:
            raise self._unusable(
                f"it was recorded against library {raw.get('library_id')!r} and this "
                f"library is {self.cfg.library.volume_id}"
            )
        records = raw.get("pairs")
        if not isinstance(records, Mapping):
            raise self._unusable("it has no pairs map")
        return {str(key): self._pair(str(key), value) for key, value in records.items()}

    def _pair(self, account_id: str, value: Any) -> Pair:
        def refused(what: str) -> CratekitError:
            return self._unusable(f"the pair {account_id!r} {what}")

        if not account_id or not isinstance(value, Mapping):
            raise refused("is not an object")
        rekordbox_id = value.get("rekordbox_id")
        if not isinstance(rekordbox_id, str) or not rekordbox_id:
            raise refused("names no rekordbox playlist")
        account = value.get("account")
        if account is not None and not _ids(account):
            raise refused("has an account side that is not ids")
        rekordbox = value.get("rekordbox")
        members: tuple[Membership, ...] | None = None
        if rekordbox is not None:
            if not isinstance(rekordbox, list) or not all(
                _ids(one) and len(one) == 2 for one in rekordbox
            ):
                raise refused("has a rekordbox side that is not memberships")
            members = tuple(Membership(one[0], one[1]) for one in rekordbox)
        links = value.get("links") or {}
        if not _id_map(links):
            raise refused("has links that are not ids")
        for flag in ("twin", "made"):
            if not isinstance(value.get(flag, False), bool):
                raise refused(f"says {flag} as something not true or false")
        folder = value.get("folder", "")
        if not isinstance(folder, str):
            raise refused("names a folder that is not a name")
        added = value.get("account_added") or {}
        if not _id_map(added):
            raise refused("has added dates that are not dates")
        on_hold = value.get("on_hold")
        if on_hold is not None and not (_id_map(on_hold, words=True)):
            raise refused("holds tracks that are not ids")
        seen = value.get("seen")
        if seen is not None and not (
            isinstance(seen, Mapping) and _ids(seen.get("order")) and _moment(seen.get("at"))
        ):
            raise refused("holds a reading that is not an order")
        stop_seen = value.get("stop_seen")
        if stop_seen is not None:
            stop_seen = self._stop_reading(account_id, stop_seen)
        return Pair(
            account_id=account_id,
            rekordbox_id=rekordbox_id,
            name=str(value.get("name") or ""),
            marked=str(value.get("marked") or ""),
            synced=str(value.get("synced") or ""),
            account=tuple(account) if account is not None else None,
            rekordbox=members,
            links=MappingProxyType(dict(links)),
            twin=value.get("twin", False),
            made=value.get("made", False),
            folder=folder,
            account_added=MappingProxyType(dict(added)),
            on_hold=None if on_hold is None else MappingProxyType(dict(on_hold)),
            seen=None if seen is None else tuple(seen["order"]),
            seen_at="" if seen is None else seen["at"],
            stop_seen=stop_seen,
        )

    def _stop_reading(self, account_id: str, value: Any) -> StopReading:
        """A pair's reading after a stopped order, read back whole or refused (U234)."""
        after = value.get("after") if isinstance(value, Mapping) else None
        if not (
            isinstance(value, Mapping)
            and _ids(value.get("order"))
            and _moment(value.get("at"))
            and _moment(value.get("run"))
            and isinstance(value.get("settled"), bool)
            and (
                after is None
                or isinstance(after, Mapping) and _ids(after.get("order"))
                and _moment(after.get("at"))
            )
        ):
            raise self._unusable(
                f"the pair {account_id!r} holds a reading after a stop that is not an order"
            )
        return StopReading(
            run=value["run"], order=tuple(value["order"]), at=value["at"], settled=value["settled"],
            after=None if after is None else tuple(after["order"]),
            after_at="" if after is None else after["at"],
        )

    def _write(self, pairs: Mapping[str, Pair], document: Document | None = None) -> None:
        """Write the pairs, and the rest of the document as it was read or as given.

        The rest is READ AGAIN HERE when none is given, under the caller's lock,
        so a write of the pairs alone never drops what another sync recorded.
        """
        rest = document if document is not None else self._document()
        payload: dict[str, Any] = {
            "version": PAIRS_VERSION,
            "library_id": self.cfg.library.volume_id,
            "pairs": {key: pair.to_json() for key, pair in sorted(pairs.items())},
        }
        if rest.folders:
            payload["folders"] = {
                name: {
                    "folder_id": one.folder_id,
                    "created": one.created,
                    **({"held": sorted(one.held)} if one.held is not None else {}),
                }
                for name, one in sorted(rest.folders.items())
            }
        if rest.misses:
            payload["misses"] = {
                row: {"isrc": miss.isrc, "reason": miss.reason}
                for row, miss in sorted(rest.misses.items())
            }
        if rest.released.account or rest.released.rekordbox:
            payload["released"] = {
                ACCOUNT_SIDE: sorted(rest.released.account),
                REKORDBOX_SIDE: sorted(rest.released.rekordbox),
            }
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            self.path,
        )

    def all(self) -> dict[str, Pair]:
        """Every pair, by account playlist identifier."""
        return self._load()

    def get(self, account_id: str) -> Pair | None:
        return self._load().get(str(account_id))

    def mark(
        self, account_id: str, rekordbox_id: str, *, name: str, twin: bool = False,
        on_hold: Mapping[str, str] | None = None,
    ) -> Pair:
        """Record the pair, or return it unchanged when it is already this pair.

        REFUSED when either identifier is paired with something else, read and
        written under one lock, so two syncs marking at once cannot pair one
        playlist twice. ``twin`` says the product made the rekordbox side
        (U149), and ``on_hold`` the tracks it was made without (U221); a pair
        already marked keeps the hold it has.
        """
        account_id = str(account_id)
        rekordbox_id = str(rekordbox_id)
        with self._locked():
            pairs = self._load()
            held = pairs.get(account_id)
            if held is not None:
                if held.rekordbox_id != rekordbox_id:
                    raise conflict(account_id, rekordbox_id, held)
                return held
            for other in pairs.values():
                if other.rekordbox_id == rekordbox_id:
                    raise conflict(account_id, rekordbox_id, other)
            pair = Pair(
                account_id=account_id, rekordbox_id=rekordbox_id, name=str(name),
                marked=timestamp(), twin=bool(twin),
                on_hold=(
                    None
                    if on_hold is None
                    else MappingProxyType({str(k): str(v) for k, v in on_hold.items() if k})
                ),
            )
            pairs[account_id] = pair
            self._write(pairs)
            return pair

    def record(
        self, account_id: str, *, account: Sequence[str] | None = None,
        rekordbox: Sequence[Membership] | None = None, links: Mapping[str, str] | None = None,
        name: str | None = None, account_added: Mapping[str, str] | None = None,
    ) -> Pair:
        """Record what a side holds now that it was written. A side passed None is kept.

        ``account_added`` replaces the dates held, and only beside an account
        side, since a date is about the base it was read with (U202). ``links``
        is MERGED, never replacing: a later sync that did not ask about a track
        learned nothing that undoes its link. The time moves only with a side.
        """
        with self._locked():
            pairs = self._load()
            held = pairs.get(str(account_id))
            if held is None:
                raise self._unusable(f"the pair {account_id!r} is not marked")
            merged = dict(held.links)
            merged.update({str(k): str(v) for k, v in (links or {}).items() if k and v})
            moved = account is not None or rekordbox is not None
            pair = replace(
                held,
                synced=timestamp() if moved else held.synced,
                account=tuple(account) if account is not None else held.account,
                account_added=(
                    MappingProxyType({str(k): str(v) for k, v in account_added.items() if k and v})
                    if account is not None and account_added is not None
                    else held.account_added
                ),
                rekordbox=tuple(rekordbox) if rekordbox is not None else held.rekordbox,
                links=MappingProxyType(merged),
                name=held.name if name is None else str(name),
                # A SNAPSHOT THAT MOVED IS LATER THAN ANY READING HELD, for a
                # pending order (U231) or after a stopped one (U234).
                seen=None if moved else held.seen,
                seen_at="" if moved else held.seen_at,
                stop_seen=None if moved else held.stop_seen,
            )
            pairs[str(account_id)] = pair
            self._write(pairs)
            return pair

    def _replace(self, account_id: str, **changes: Any) -> Pair | None:
        """Change one marked pair under the lock, or keep nothing when none is marked."""
        with self._locked():
            pairs = self._load()
            held = pairs.get(str(account_id))
            if held is None:
                return None
            pair = replace(held, **changes)
            pairs[str(account_id)] = pair
            self._write(pairs)
            return pair

    def see(self, account_id: str, order: Sequence[str], *, at: str) -> Pair | None:
        """Keep one reading of a pending order's account playlist, read at ``at`` (U231).

        Replaces any reading held. Answers the pair, or None when none is marked.
        """
        return self._replace(account_id, seen=tuple(str(one) for one in order), seen_at=str(at))

    def see_stop(self, account_id: str, reading: StopReading) -> Pair | None:
        """Keep the readings of a playlist a stopped order left (U234), as :meth:`see`."""
        return self._replace(account_id, stop_seen=reading)

    def unmark(self, account_id: str, rekordbox_id: str) -> Pair | None:
        """Forget one pair, and answer what it was, or None when it is not this pair.

        U149. Only a pair still holding ``rekordbox_id``, under one lock, so one
        marked again since the caller read it is kept. Neither playlist is
        touched: an unpaired playlist is still the list it was.
        """
        with self._locked():
            pairs = self._load()
            held = pairs.get(str(account_id))
            if held is None or held.rekordbox_id != str(rekordbox_id):
                return None
            del pairs[str(account_id)]
            self._write(pairs)
            return held

    def release_hold(self, wanted: Mapping[str, str]) -> dict[str, Pair]:
        """Empty the hold of each twin named, account id to the rekordbox id the plan read (U221).

        Under one lock, and only a twin still paired with that rekordbox
        playlist and holding something. Answers each pair released, as it was.
        """
        with self._locked():
            pairs = self._load()
            released: dict[str, Pair] = {}
            for account_id, rekordbox_id in wanted.items():
                held = pairs.get(str(account_id))
                if (
                    held is None
                    or not held.twin
                    or held.rekordbox_id != str(rekordbox_id)
                    or (held.on_hold is not None and not held.on_hold)
                ):
                    continue
                pairs[held.account_id] = replace(held, on_hold=MappingProxyType({}))
                released[held.account_id] = held
            if released:
                self._write(pairs)
            return released

    # ── U198: what a sync of every pair makes, remembers and lets go ────────

    def folders(self) -> dict[str, MadeFolder]:
        """Every account root folder a sync of every pair made or adopted, by name."""
        return self._document().folders

    def misses(self) -> dict[str, Miss]:
        """Every rekordbox row the account was asked about and had no track for."""
        return self._document().misses

    def released(self) -> Released:
        """Every playlist whose other side was deleted, so nothing makes it again."""
        return self._document().released

    def reserve_folder(
        self, name: str, create: Callable[[], str], *, adopt: str = "", stale: str = "",
        held: Iterable[str] | None = None,
    ) -> tuple[str, bool]:
        """The account root folder for ``name``, made only if none is recorded. ``(id, created)``.

        The ledger's reserve shape: the lock is taken before the create,
        ``adopt`` is the one root folder of the name the plan found, and
        ``stale`` a recorded folder read as gone. ``held`` is what the plan
        listed in the folder it adopts (U216), None when it did not say.
        """
        with self._locked():
            document = self._document()
            recorded = document.folders.get(name)
            if recorded is not None and recorded.folder_id != stale:
                return recorded.folder_id, False
            if adopt:
                folder_id, created = adopt, False
                before = None if held is None else frozenset(str(one) for one in held if str(one))
            else:
                folder_id, created = str(create()), True
                before = frozenset()
            document.folders[name] = MadeFolder(name, folder_id, created, before)
            self._write(document.pairs, document)
            return folder_id, created

    def _made(
        self, document: Document, account_id: str, rekordbox_id: str, name: str, folder: str
    ) -> None:
        """Mark a pair the product made one side of, and write it."""
        document.pairs[account_id] = Pair(
            account_id=account_id, rekordbox_id=rekordbox_id, name=str(name), marked=timestamp(),
            made=True, folder=str(folder),
        )
        self._write(document.pairs, document)

    def reserve_made(
        self, rekordbox_id: str, *, name: str, folder: str, create: Callable[[], str]
    ) -> tuple[str, bool]:
        """The account playlist made for one rekordbox playlist, and its pair. ``(id, created)``.

        MADE AND MARKED IN ONE WRITE, under one lock taken before the create,
        and a rekordbox playlist already paired answers its account playlist,
        so two syncs never make two.
        """
        rekordbox_id = str(rekordbox_id)
        with self._locked():
            document = self._document()
            for pair in document.pairs.values():
                if pair.rekordbox_id == rekordbox_id:
                    return pair.account_id, False
            account_id = str(create())
            if account_id in document.pairs:
                raise conflict(account_id, rekordbox_id, document.pairs[account_id])
            self._made(document, account_id, rekordbox_id, name, folder)
            return account_id, True

    def reserve_made_rekordbox(
        self, account_id: str, *, name: str, folder: str, create: Callable[[], str]
    ) -> tuple[str, bool]:
        """The rekordbox playlist made for one account playlist, and its pair. ``(id, created)``.

        U202, :meth:`reserve_made` the other way round.
        """
        account_id = str(account_id)
        with self._locked():
            document = self._document()
            held = document.pairs.get(account_id)
            if held is not None:
                return held.rekordbox_id, False
            rekordbox_id = str(create())
            for pair in document.pairs.values():
                if pair.rekordbox_id == rekordbox_id:
                    raise conflict(account_id, rekordbox_id, pair)
            self._made(document, account_id, rekordbox_id, name, folder)
            return rekordbox_id, True

    def remember(self, misses: Mapping[str, Miss], *, forget: Iterable[str] = ()) -> None:
        """Remember rows the account had no track for, and forget rows matched since (R-988)."""
        gone = {str(one) for one in forget}
        if not misses and not gone:
            return
        with self._locked():
            document = self._document()
            for content_id in gone:
                document.misses.pop(content_id, None)
            document.misses.update({str(k): v for k, v in misses.items()})
            self._write(document.pairs, document)

    def release(self, account_id: str, rekordbox_id: str, *, side: str) -> Pair | None:
        """Unpair a made pair one of whose sides is gone, and remember the side left.

        ``side`` is the side that is GONE. The other side's playlist is kept and
        recorded as released, so nothing makes its partner again. Answers the
        pair forgotten, or None when it is not this pair any more.
        """
        if side not in (ACCOUNT_SIDE, REKORDBOX_SIDE):
            raise ValueError(f"no such side: {side!r}")
        with self._locked():
            document = self._document()
            held = document.pairs.get(str(account_id))
            if held is None or held.rekordbox_id != str(rekordbox_id):
                return None
            del document.pairs[str(account_id)]
            gone = document.released
            if side == ACCOUNT_SIDE:
                document.released = replace(gone, rekordbox=gone.rekordbox | {held.rekordbox_id})
            else:
                document.released = replace(gone, account=gone.account | {held.account_id})
            self._write(document.pairs, document)
            return held


def conflict(account_id: str, rekordbox_id: str, held: Pair) -> CratekitError:
    """The refusal for an identifier already paired with something else."""
    return refuse(
        "sync-pair-conflict",
        f"the account playlist {held.account_id} ({held.name or 'unnamed'}) is "
        f"already paired with the rekordbox playlist {held.rekordbox_id}, so the "
        f"account playlist {account_id} and the rekordbox playlist {rekordbox_id} "
        f"were not paired; one playlist stays the same list as one other",
        steps=(
            "sync the existing pair with crate sync pair "
            f"{held.account_id}, or pick playlists neither of which is paired",
        ),
        origin=_ORIGIN,
        detail={
            "account_id": account_id, "rekordbox_id": rekordbox_id,
            "paired_account": held.account_id, "paired_rekordbox": held.rekordbox_id,
        },
    )


def paired(cfg: config.Config | None, playlist_id: str) -> bool:
    """Whether the author marked this account playlist as one side of a pair.

    The account seam's second question before a removal, after
    ``ledger.product_made``. No configuration, or no identifier, is no.
    """
    wanted = str(playlist_id or "")
    if cfg is None or not wanted:
        return False
    return wanted in PairStore(cfg).all()


def paired_ids(cfg: config.Config) -> frozenset[str]:
    """Every paired account playlist, for the playlists sweep to leave alone."""
    return frozenset(PairStore(cfg).all())


__all__ = [
    "ACCOUNT_SIDE", "PAIRS_VERSION", "REKORDBOX_SIDE", "Document", "MadeFolder", "Membership",
    "Miss", "Pair", "PairStore", "Released", "StopReading", "conflict", "paired", "paired_ids",
]
