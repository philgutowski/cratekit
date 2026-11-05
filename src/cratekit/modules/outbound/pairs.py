"""The playlist pairs: which account playlist stays the same list as which rekordbox one.

U130. A PAIR is one of the author's own account playlists and one rekordbox
playlist, marked to be kept the same list on both sides by ``crate sync pair``.
This module is the record of every pair and of what each side held when its
last sync finished, which is the base ``sync/pair_merge.py`` merges against.

**BY IDENTIFIER, BOTH SIDES, NEVER BY NAME (R-906).** The account's playlist
identifier is the key, and the rekordbox playlist identifier is held beside it.
A playlist renamed on either side is still the same pair, and two playlists
sharing a name are never mistaken for one. One account playlist pairs with one
rekordbox playlist and the reverse: :meth:`PairStore.mark` refuses an
identifier already paired with something else.

**A MARK IS WRITTEN WHEN THE FIRST SYNC IS APPROVED, A SNAPSHOT WHEN THE WHOLE
PAIR WAS WRITTEN.** The two are separate on purpose. A first sync that is
approved and then fails part way leaves the pair marked with no snapshot, so
the next sync is still a first one, which adds only. Both sides' snapshots are
recorded together and only after both were written and read back from a whole
listing, because a snapshot of one side taken while the other still owes it a
change would read that change as never having happened.

**IT IS ALSO THE ACCOUNT'S PERMISSION TO TAKE A TRACK OFF.** The account seam
removes tracks only from a playlist the outbound ledger says the product made
(R-836), and the author's own playlists were not. :func:`paired` is the second
question that removal asks: a playlist the author marked here is one whose
removals the author asked to have applied, by the rule U130 decided on
2026-10-10, and nothing else is.

**WHAT A SYNC OF EVERY PAIR RECORDS BESIDE THE PAIRS (U198).** The account
root folders it made or adopted, by name; every rekordbox row the account had
no track for, with the ISRC it was asked under and the answer; and the
playlists a made pair left behind when its other side was deleted, so nothing
makes that side again. A write of the pairs alone reads them again under its
lock and keeps them.

**AND THE OTHER WAY, AND THE DATES (U202).** A pair whose rekordbox side the
product made for an account playlist is reserved the same way, under the lock
before the playlist is made (:meth:`PairStore.reserve_made_rekordbox`), and
is ``made`` like U198's. A snapshot also records when the account says each
track it held was added (``Pair.account_added``), so a track taken out and put
back on the account between two syncs can be told from one held all along
(R-990). The document stays version 2: a copy that does not know the dates
drops them on its next write, and the sync after reads every track as held
all along, which is the rule before U202, never a loss.

**AND WHAT AN ADOPTED FOLDER HELD (U216).** A root folder adopted by its name
records the account playlists it held at that moment (``MadeFolder.held``), so
no sync brings them to rekordbox; a folder the product created records that it
held nothing. Still version 2: a record without ``held`` is a folder adopted
before U216, and a sync reads it by time, every unknown as held, so a copy
that drops the field on its next write costs a playlist named rather than one
made twice.

**AND WHAT A TWIN HOLDS FOR THE AUTHOR'S CHOICE (U221).** Decided by
Phillip on 2026-11-05: the account tracks a custom playlist twin was made
without are never queued for download on their own. ``crate sync twins``
records them on the twin's pair (``Pair.on_hold``), ``crate sync pair`` names
them and queues none, and ``crate sync release`` empties one twin's hold, or
every twin's, so the next sync queues them (:meth:`PairStore.release_hold`).
A landing's twin records an empty hold. A twin with no hold recorded was
paired before U221, and a sync reads it by time, every track the account
listed before the pair was marked held. Still version 2: a copy that drops the
field on its next write leaves a twin that is read by time, which holds the
same tracks, never one that queues them.

Layer: modules.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.cli.output import timestamp
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

#: 2 since U198, which records made pairs, their folders, the remembered
#: misses and the released playlists. A copy built before it refuses the
#: document rather than rewriting it without them, which would forget a
#: released playlist and make it again. Version 1 is still read.
PAIRS_VERSION = 2
READ_VERSIONS = (1, 2)

_ORIGIN = ("outbound", "pairs")


@dataclass(frozen=True, slots=True)
class Membership:
    """One rekordbox membership as a snapshot holds it: the track and its row."""

    content_id: str
    row_id: str

    def to_json(self) -> list[str]:
        return [self.content_id, self.row_id]


@dataclass(frozen=True, slots=True)
class Pair:
    """One pair and what each side held when its last sync finished.

    ``account`` and ``rekordbox`` are None for a side no sync has recorded,
    which is every side of a pair that was marked and never written. ``links``
    maps a remote track identifier to the rekordbox content row it was matched
    with, so a later sync does not match the same track twice.
    """

    account_id: str
    rekordbox_id: str
    name: str
    marked: str
    synced: str = ""
    account: tuple[str, ...] | None = None
    rekordbox: tuple[Membership, ...] | None = None
    links: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))
    #: Whether the product made the rekordbox side as the account playlist's
    #: custom playlist twin (U149), so a sync unpairs it, rather than leaving
    #: it out, once the account playlist is gone.
    twin: bool = False
    #: Whether the product made the account side for a rekordbox playlist a
    #: sync of every pair found (U198), so a sync unpairs it, rather than
    #: leaving it out, once either side is gone. ``folder`` is the account
    #: root folder it was made in.
    made: bool = False
    folder: str = ""
    #: U202. When the account says each track the account side held at the
    #: last whole sync was added there, ISO 8601 text by remote identifier,
    #: for the tracks it dated. A later date on a track the base held is that
    #: track taken out and put back on the account since (R-990).
    account_added: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))
    #: U221. The account tracks a twin was made without, held for the author's
    #: choice and never queued, remote identifier to the words a person reads.
    #: Empty for a twin holding nothing, a landing's or one released. None when
    #: the pair recorded no hold: no twin, a twin paired before U221, or one
    #: made from a short listing, which ``sync pair`` reads by time.
    on_hold: Mapping[str, str] | None = None

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
    #: U216. The account playlists the folder held when a sync adopted it, which no
    #: sync brings to rekordbox. Empty for a folder this product created, which held
    #: nothing. None for a folder recorded before U216, whose record does not say.
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

    @contextmanager
    def _locked(self) -> Iterator[None]:
        lock = config._exclusive_lock(self.lock_path)
        try:
            lock.__enter__()
        except config.ConfigLockUnavailable as exc:
            raise refuse(
                "sync-pair-store-unusable",
                f"the playlist pairs could not be locked ({exc}), and recording a "
                f"snapshot unlocked discards whatever a second sync is recording "
                f"at the same time",
                steps=("make the library's state directory writable by this account",),
                scope=Scope.RUN,
                origin=_ORIGIN,
                detail={"lock": str(self.lock_path)},
            ) from exc
        try:
            yield
        finally:
            lock.__exit__(None, None, None)

    def _load(self) -> dict[str, Pair]:
        return self._document().pairs

    def _document(self) -> Document:
        if not self.path.exists():
            return Document()
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise self._unusable("it could not be opened") from exc
        except ValueError as exc:
            raise self._unusable("it is not JSON") from exc
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
            if held is not None and (
                not isinstance(held, list) or not all(isinstance(one, str) and one for one in held)
            ):
                raise self._unusable(f"what the folder {name!r} held is not playlist ids")
            found[str(name)] = MadeFolder(
                str(name),
                str(value["folder_id"]),
                value.get("created") is True,
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
            if not isinstance(ids, list) or not all(isinstance(one, str) and one for one in ids):
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
        found: dict[str, Pair] = {}
        for key, value in records.items():
            found[str(key)] = self._pair(str(key), value)
        return found

    def _pair(self, account_id: str, value: Any) -> Pair:
        if not account_id or not isinstance(value, Mapping):
            raise self._unusable(f"the pair {account_id!r} is not an object")
        rekordbox_id = value.get("rekordbox_id")
        if not isinstance(rekordbox_id, str) or not rekordbox_id:
            raise self._unusable(f"the pair {account_id!r} names no rekordbox playlist")
        account = value.get("account")
        if account is not None and not (
            isinstance(account, list) and all(isinstance(one, str) and one for one in account)
        ):
            raise self._unusable(f"the pair {account_id!r} has an account side that is not ids")
        rekordbox = value.get("rekordbox")
        members: tuple[Membership, ...] | None = None
        if rekordbox is not None:
            if not isinstance(rekordbox, list) or not all(
                isinstance(one, list)
                and len(one) == 2
                and all(isinstance(part, str) and part for part in one)
                for one in rekordbox
            ):
                raise self._unusable(
                    f"the pair {account_id!r} has a rekordbox side that is not memberships"
                )
            members = tuple(Membership(one[0], one[1]) for one in rekordbox)
        links = value.get("links") or {}
        if not isinstance(links, Mapping) or not all(
            isinstance(k, str) and k and isinstance(v, str) and v for k, v in links.items()
        ):
            raise self._unusable(f"the pair {account_id!r} has links that are not ids")
        twin = value.get("twin", False)
        if not isinstance(twin, bool):
            raise self._unusable(f"the pair {account_id!r} says twin as something not true or false")
        made = value.get("made", False)
        if not isinstance(made, bool):
            raise self._unusable(f"the pair {account_id!r} says made as something not true or false")
        folder = value.get("folder", "")
        if not isinstance(folder, str):
            raise self._unusable(f"the pair {account_id!r} names a folder that is not a name")
        added = value.get("account_added") or {}
        if not isinstance(added, Mapping) or not all(
            isinstance(k, str) and k and isinstance(v, str) and v for k, v in added.items()
        ):
            raise self._unusable(f"the pair {account_id!r} has added dates that are not dates")
        on_hold = value.get("on_hold")
        if on_hold is not None and not (
            isinstance(on_hold, Mapping)
            and all(isinstance(k, str) and k and isinstance(v, str) for k, v in on_hold.items())
        ):
            raise self._unusable(f"the pair {account_id!r} holds tracks that are not ids")
        return Pair(
            account_id=account_id,
            rekordbox_id=rekordbox_id,
            name=str(value.get("name") or ""),
            marked=str(value.get("marked") or ""),
            synced=str(value.get("synced") or ""),
            account=tuple(account) if account is not None else None,
            rekordbox=members,
            links=MappingProxyType(dict(links)),
            twin=twin,
            made=made,
            folder=folder,
            account_added=MappingProxyType(dict(added)),
            on_hold=None if on_hold is None else MappingProxyType(dict(on_hold)),
        )

    def _write(self, pairs: Mapping[str, Pair], document: Document | None = None) -> None:
        """Write the pairs, and the rest of the document as it was read or as given.

        THE REST IS READ AGAIN HERE when no document is given, under the
        caller's lock, so a write of the pairs alone never drops the folders,
        the misses or the released playlists another sync recorded.
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
                content_id: {"isrc": one.isrc, "reason": one.reason}
                for content_id, one in sorted(rest.misses.items())
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
        self,
        account_id: str,
        rekordbox_id: str,
        *,
        name: str,
        twin: bool = False,
        on_hold: Mapping[str, str] | None = None,
    ) -> Pair:
        """Record the pair, or return it unchanged when it is already this pair.

        REFUSED when either identifier is paired with something else, read and
        written under one lock, so two syncs marking at once cannot each pair
        one rekordbox playlist with a different account playlist. ``twin`` says
        the product made the rekordbox side as a custom playlist twin (U149),
        and ``on_hold`` the tracks it was made without, held for the author's
        choice (U221); a pair already marked keeps the hold it has.
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
                account_id=account_id,
                rekordbox_id=rekordbox_id,
                name=str(name),
                marked=timestamp(),
                twin=bool(twin),
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
        self,
        account_id: str,
        *,
        account: Sequence[str] | None = None,
        rekordbox: Sequence[Membership] | None = None,
        links: Mapping[str, str] | None = None,
        name: str | None = None,
        account_added: Mapping[str, str] | None = None,
    ) -> Pair:
        """Record what a side holds now that it was written. A side passed None is kept.

        ``account_added`` replaces the added dates held, and is recorded only
        beside an account side, since a date is about the base it was read
        with (U202).

        ``links`` is MERGED into the links held, never replacing them: a link
        is what one sync learned about one track, and a later sync that did not
        need to ask about that track has learned nothing that undoes it. The
        time of the sync moves only when a side is recorded.
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
            )
            pairs[str(account_id)] = pair
            self._write(pairs)
            return pair


    def unmark(self, account_id: str, rekordbox_id: str) -> Pair | None:
        """Forget one pair, and answer what it was, or None when it is not this pair.

        U149. Only a pair still holding ``rekordbox_id`` is forgotten, read and
        written under one lock, so a pair marked again since the caller read it
        is left as it is. Neither side's playlist is touched: an unpaired
        playlist is still the list it was, in rekordbox and on the account.
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

        Read and written under one lock. Only a twin still paired with the
        rekordbox playlist named is released, so one unpaired or paired again
        since the plan keeps what it holds. A twin holding nothing already is
        passed over. Answers each pair released, as it was before.
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
        self,
        name: str,
        create: Callable[[], str],
        *,
        adopt: str = "",
        stale: str = "",
        held: Iterable[str] | None = None,
    ) -> tuple[str, bool]:
        """The account root folder for ``name``, made only if none is recorded. ``(id, created)``.

        The ledger's reserve shape: the lock is taken before the create, so an
        unwritable document refuses before anything exists on the account;
        ``adopt`` is the one root folder of the name the plan found and a
        person was shown, and ``stale`` a recorded folder read as gone.
        ``held`` is what the plan listed in the folder it adopts, recorded in
        the same write (U216), and None records an adoption whose plan did not
        say, which a sync reads by time; a folder this call creates held nothing.
        """
        with self._locked():
            document = self._document()
            recorded = document.folders.get(name)
            if recorded is not None and recorded.folder_id != stale:
                return recorded.folder_id, False
            if adopt:
                folder_id, created = adopt, False
                before = (
                    None if held is None else frozenset(str(one) for one in held if str(one))
                )
            else:
                folder_id, created = str(create()), True
                before = frozenset()
            document.folders[name] = MadeFolder(name, folder_id, created, before)
            self._write(document.pairs, document)
            return folder_id, created

    def reserve_made(
        self, rekordbox_id: str, *, name: str, folder: str, create: Callable[[], str]
    ) -> tuple[str, bool]:
        """The account playlist made for one rekordbox playlist, and its pair. ``(id, created)``.

        MADE AND MARKED IN ONE WRITE, under one lock taken before the create:
        an unwritable document refuses before the playlist exists, and a
        rekordbox playlist a pair already holds answers that pair's account
        playlist, so two syncs never make two.
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
            document.pairs[account_id] = Pair(
                account_id=account_id,
                rekordbox_id=rekordbox_id,
                name=str(name),
                marked=timestamp(),
                made=True,
                folder=str(folder),
            )
            self._write(document.pairs, document)
            return account_id, True

    def reserve_made_rekordbox(
        self, account_id: str, *, name: str, folder: str, create: Callable[[], str]
    ) -> tuple[str, bool]:
        """The rekordbox playlist made for one account playlist, and its pair. ``(id, created)``.

        U202, :meth:`reserve_made` the other way round. The lock is taken
        before ``create`` runs, so an unwritable document refuses before the
        playlist exists, and the pair is marked as the product's in the write
        straight after it. An account playlist a pair already holds answers
        that pair's rekordbox playlist, so two syncs never make two.
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
            document.pairs[account_id] = Pair(
                account_id=account_id,
                rekordbox_id=rekordbox_id,
                name=str(name),
                marked=timestamp(),
                made=True,
                folder=str(folder),
            )
            self._write(document.pairs, document)
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

        ``side`` is the side that is GONE. The other side's playlist is left
        where it is and recorded as released, so a sync of every pair never
        makes its partner again. Answers the pair forgotten, or None when it is
        not this pair any more.
        """
        if side not in (ACCOUNT_SIDE, REKORDBOX_SIDE):
            raise ValueError(f"no such side: {side!r}")
        with self._locked():
            document = self._document()
            held = document.pairs.get(str(account_id))
            if held is None or held.rekordbox_id != str(rekordbox_id):
                return None
            del document.pairs[str(account_id)]
            if side == ACCOUNT_SIDE:
                document.released = replace(
                    document.released,
                    rekordbox=document.released.rekordbox | {held.rekordbox_id},
                )
            else:
                document.released = replace(
                    document.released, account=document.released.account | {held.account_id}
                )
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
            "account_id": account_id,
            "rekordbox_id": rekordbox_id,
            "paired_account": held.account_id,
            "paired_rekordbox": held.rekordbox_id,
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
    "ACCOUNT_SIDE",
    "PAIRS_VERSION",
    "REKORDBOX_SIDE",
    "Document",
    "MadeFolder",
    "Membership",
    "Miss",
    "Pair",
    "PairStore",
    "Released",
    "conflict",
    "paired",
    "paired_ids",
]
