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

Layer: modules.
"""

from __future__ import annotations

import json
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.cli.output import timestamp
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

PAIRS_VERSION = 1

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
        if self.account is not None:
            record["account"] = list(self.account)
        if self.rekordbox is not None:
            record["rekordbox"] = [member.to_json() for member in self.rekordbox]
        return record


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
        if not self.path.exists():
            return {}
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise self._unusable("it could not be opened") from exc
        except ValueError as exc:
            raise self._unusable("it is not JSON") from exc
        return self._recognize(raw)

    def _recognize(self, raw: Any) -> dict[str, Pair]:
        if not isinstance(raw, Mapping):
            raise self._unusable(f"the document is a {type(raw).__name__}, not a pair map")
        if raw.get("version") != PAIRS_VERSION:
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
        return Pair(
            account_id=account_id,
            rekordbox_id=rekordbox_id,
            name=str(value.get("name") or ""),
            marked=str(value.get("marked") or ""),
            synced=str(value.get("synced") or ""),
            account=tuple(account) if account is not None else None,
            rekordbox=members,
            links=MappingProxyType(dict(links)),
        )

    def _write(self, pairs: Mapping[str, Pair]) -> None:
        payload = {
            "version": PAIRS_VERSION,
            "library_id": self.cfg.library.volume_id,
            "pairs": {key: pair.to_json() for key, pair in sorted(pairs.items())},
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

    def mark(self, account_id: str, rekordbox_id: str, *, name: str) -> Pair:
        """Record the pair, or return it unchanged when it is already this pair.

        REFUSED when either identifier is paired with something else, read and
        written under one lock, so two syncs marking at once cannot each pair
        one rekordbox playlist with a different account playlist.
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
    ) -> Pair:
        """Record what a side holds now that it was written. A side passed None is kept.

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
                rekordbox=tuple(rekordbox) if rekordbox is not None else held.rekordbox,
                links=MappingProxyType(merged),
                name=held.name if name is None else str(name),
            )
            pairs[str(account_id)] = pair
            self._write(pairs)
            return pair


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
    "PAIRS_VERSION",
    "Membership",
    "Pair",
    "PairStore",
    "conflict",
    "paired",
    "paired_ids",
]
