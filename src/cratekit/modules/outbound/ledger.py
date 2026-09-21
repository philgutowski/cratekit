"""What this library already wrote to a streaming account.

A year watermark is not this file. This file is the remote identifiers a
re-run must reuse so an interrupted write does not create a second playlist
or a second heart. It SURVIVES a library rollback: the remote account does
not roll back, and forgetting a remote id is how the next export duplicates.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

LEDGER_VERSION = 1


def _unusable(path, what: str) -> CratekitError:
    return refuse(
        "outbound-ledger-unusable",
        f"the outbound write ledger at {path.name} could not be read ({what}), "
        f"so treating it as empty would duplicate remote playlists and hearts "
        f"this library already wrote",
        steps=("repair or restore the outbound write ledger before exporting",),
        scope=Scope.RUN,
        origin=("outbound.ledger",),
        detail={"problem": what, "path": str(path)},
    )


def _empty() -> dict[str, Any]:
    return {"version": LEDGER_VERSION, "playlists": {}, "hearts": {}}


def _load(cfg: config.Config) -> dict[str, Any]:
    path = config.state_path("outbound_writes", cfg)
    if not path.exists():
        return _empty()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise _unusable(path, "it could not be opened") from exc
    except ValueError as exc:
        raise _unusable(path, "it is not JSON") from exc
    if not isinstance(raw, Mapping):
        raise _unusable(path, f"the document is a {type(raw).__name__}, not a map")
    version = raw.get("version")
    if version not in (None, LEDGER_VERSION):
        raise _unusable(
            path, f"it says version {version!r} and this build writes {LEDGER_VERSION}"
        )
    playlists = raw.get("playlists", {})
    hearts = raw.get("hearts", {})
    if not isinstance(playlists, Mapping) or not isinstance(hearts, Mapping):
        raise _unusable(path, "playlists and hearts must both be maps")
    return {
        "version": LEDGER_VERSION,
        "playlists": {str(key): dict(value) for key, value in playlists.items()
                      if isinstance(value, Mapping)},
        "hearts": {str(key): str(value) for key, value in hearts.items()},
    }


def _write(cfg: config.Config, document: Mapping[str, Any]) -> None:
    path = config.state_path("outbound_writes", cfg)
    payload = json.dumps(document, indent=2, sort_keys=True) + "\n"
    config.atomic_write_bytes(payload.encode("utf-8"), path)


def _locked(cfg: config.Config):
    lock = config._exclusive_lock(config.state_path("outbound_writes_lock", cfg))
    try:
        lock.__enter__()
    except config.ConfigLockUnavailable as exc:
        raise refuse(
            "outbound-ledger-unusable",
            f"the outbound write ledger could not be locked ({exc}), and "
            f"writing it unlocked duplicates a neighbour export's remote id",
            steps=("make the library state directory writable by this account",),
            scope=Scope.RUN,
            origin=("outbound.ledger",),
        ) from exc
    return lock


#: The share of a recorded playlist's tracks a crate must still carry to be
#: recognised as that playlist under a new path, as a fraction spelled in two
#: integers so the comparison never leaves whole numbers. HALF, and the argument
#: for it is what a person does to a crate between two exports: they add to it
#: freely, which costs nothing here since additions are not in the recorded set,
#: and they prune it a little. A crate that lost more than half of what was
#: written is more likely a different crate than the same one reorganised, and a
#: wrong adoption writes onto a remote playlist that belongs to something else.
SHARED_NUMERATOR = 1
SHARED_DENOMINATOR = 2


@dataclass(frozen=True, slots=True)
class Recognition:
    """What the ledger can say about a crate that has no record under its key.

    THE KEY IS A DISPLAY PATH BECAUSE THERE IS NOTHING ELSE (R-229). A rekordbox
    collection export gives a playlist a name, a place in a tree and its track
    ids, and no identifier, so a crate that is renamed or dragged into a folder
    arrives here under a key nothing was ever recorded against. Read as "never
    exported", that created a SECOND remote playlist with nothing said.

    ``adopts`` is the recorded key whose remote playlist this crate should go on
    using, or empty. It is set only when EXACTLY ONE recorded key qualifies.
    ``candidates`` carries every key that qualified, so two is reported as two
    rather than resolved by a rule nobody chose: adopting the wrong one writes
    this crate's tracks onto another crate's remote playlist.

    ``shared`` and ``recorded`` are the evidence, for the sentence a person
    reads. Both are zero for a record recognised by its name alone, which is a
    record written before this build recorded tracks at all.
    """

    adopts: str = ""
    remote_id: str = ""
    shared: int = 0
    recorded: int = 0
    candidates: tuple[str, ...] = ()

    @property
    def ambiguous(self) -> bool:
        return len(self.candidates) > 1


def _listed(record: Mapping[str, Any], field: str) -> list[str]:
    """One list valued field of a record, or empty when it is not a list."""
    value = record.get(field) or []
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _same_name(recorded_key: str, name: str) -> bool:
    """Whether a recorded display path ends in this display name.

    BY SUFFIX AND NOT BY SPLITTING, because a playlist name may itself contain
    the separator, so the last element of a split key is not reliably the name.
    """
    return bool(name) and (recorded_key == name or recorded_key.endswith("/" + name))


def recognise(
    cfg: config.Config,
    playlist_key: str,
    *,
    name: str,
    track_ids: Iterable[str],
    live_keys: Iterable[str],
) -> Recognition:
    """Whether an unrecorded crate is a recorded one under a new path.

    READ ONLY, and it decides nothing on its own. The verb shows the answer on
    its confirm gate and freezes it into the job, and ``reserve_playlist`` moves
    the record only when that frozen answer says so.

    A RECORDED KEY IS A CANDIDATE ONLY IF THE EXPORT NO LONGER CARRIES IT.
    ``live_keys`` is every playlist path in the document being exported from. A
    recorded key still among them is a living crate with its own remote
    playlist, and it is never offered however many tracks it shares: two crates
    sharing most of their tracks is an ordinary library.

    TWO RULES, BY WHAT THE RECORD CARRIES. A record holding the library tracks
    it wrote qualifies when this crate still carries at least
    ``SHARED_NUMERATOR / SHARED_DENOMINATOR`` of them, and at least one. A record
    written before this build holds none, so it qualifies on its display name
    alone, which is the crate dragged into a folder. A record that holds tracks
    never qualifies by name: a new crate reusing an old name with different
    music is a different crate.

    THE WEAKNESS IS THE DOCUMENT'S AGE, stated rather than hidden. "No longer
    carries" is judged against the export handed in, so an export older than a
    crate reads that crate's record as orphaned. That is why this is an offer on
    a gate that also shows the export's date, and never a silent move.
    """
    playlists = _load(cfg)["playlists"]
    own = playlists.get(playlist_key) or {}
    if own.get("remote_id"):
        return Recognition()
    live = frozenset(str(key) for key in live_keys)
    wanted = frozenset(str(track) for track in track_ids)
    found: list[tuple[str, str, int, int]] = []
    for key, record in playlists.items():
        remote = record.get("remote_id")
        if not remote or key == playlist_key or key in live:
            continue
        written = frozenset(_listed(record, "tracks"))
        if written:
            shared = len(written & wanted)
            if shared < 1 or shared * SHARED_DENOMINATOR < len(written) * SHARED_NUMERATOR:
                continue
            found.append((key, str(remote), shared, len(written)))
        elif _same_name(key, name):
            found.append((key, str(remote), 0, 0))
    candidates = tuple(sorted(key for key, *_rest in found))
    if len(found) != 1:
        return Recognition(candidates=candidates)
    key, remote, shared, recorded = found[0]
    return Recognition(
        adopts=key,
        remote_id=remote,
        shared=shared,
        recorded=recorded,
        candidates=candidates,
    )


def playlist_remote_id(cfg: config.Config, playlist_key: str) -> str | None:
    """The remote playlist already created for this local playlist, if any."""
    record = _load(cfg)["playlists"].get(playlist_key)
    if not record:
        return None
    remote = record.get("remote_id")
    return str(remote) if remote else None


def playlist_added(cfg: config.Config, playlist_key: str) -> frozenset[str]:
    """Remote track ids already recorded as written onto this playlist."""
    record = _load(cfg)["playlists"].get(playlist_key) or {}
    added = record.get("added") or []
    if not isinstance(added, list):
        return frozenset()
    return frozenset(str(item) for item in added)


def recorded_hearts(cfg: config.Config) -> frozenset[str]:
    """Remote track ids this library has already hearted."""
    return frozenset(_load(cfg)["hearts"])


def record_playlist(cfg: config.Config, playlist_key: str, remote_id: str) -> None:
    """Remember the remote playlist so a re-run updates it rather than creating."""
    lock = _locked(cfg)
    try:
        _record_playlist_locked(cfg, playlist_key, remote_id)
    finally:
        lock.__exit__(None, None, None)


def _record_playlist_locked(
    cfg: config.Config, playlist_key: str, remote_id: str
) -> None:
    document = _load(cfg)
    existing = document["playlists"].get(playlist_key) or {
        "remote_id": remote_id,
        "added": [],
    }
    existing["remote_id"] = remote_id
    existing.setdefault("added", [])
    document["playlists"][playlist_key] = existing
    _write(cfg, document)


@dataclass(frozen=True, slots=True)
class Reserved:
    """The remote playlist a crate writes to, and how this call came by it.

    ``adopted_from`` is the key the record was moved from BY THIS CALL, decided
    under the lock, so two drivers cannot both report the one move.
    """

    remote_id: str
    created: bool = False
    adopted_from: str = ""


def reserve_playlist(
    cfg: config.Config,
    playlist_key: str,
    create: Callable[[], str],
    *,
    adopts: str = "",
) -> Reserved:
    """The remote playlist for this crate, creating one only if none is recorded.

    ``adopts`` NAMES A RECORDED KEY THIS CRATE USED TO LIVE UNDER (R-229), which
    a person confirmed on the verb's gate. When this key has no record and that
    one does, the record MOVES here, under the lock, and no playlist is created.
    The order is this key first: under the per item shape the first item moves
    the record and every later item of the same job finds it already here. An
    ``adopts`` naming a record that is gone falls through to the create, which
    is what the job would have done had nothing been recognised.

    **THE LOCK IS TAKEN BEFORE THE CREATE, AND THAT ORDERING IS THE WHOLE POINT.**
    The caller used to read the recorded id without a lock, call
    ``create_playlist`` when there was none, and only then take the lock to
    record it. A ledger that cannot be locked or written fails at that last step,
    with a remote playlist already made and nothing remembering it. Every
    subsequent call read no record and made ANOTHER one.

    That was not hypothetical. It was driven on 2026-09-02 against a state
    directory the account could not write: one three track export produced THREE
    remote playlists on the account, one per item, and the person is left to find
    and delete two of them by hand at the provider. The per item shape the
    outbound verbs use is what turned one orphan into N, which is why the fix
    belongs here on the checking path rather than in either verb.

    Taking the lock first means an unwritable ledger refuses
    ``outbound-ledger-unusable`` BEFORE anything is created, so the account is
    untouched. A narrower window survives, where the lock is held and the write
    then fails, and it is recorded as a residual rather than claimed closed:
    closing it needs a create the provider itself can make idempotent, which no
    adapter offers.
    """
    lock = _locked(cfg)
    try:
        record = _load(cfg)["playlists"].get(playlist_key) or {}
        recorded = record.get("remote_id")
        if recorded:
            return Reserved(str(recorded))
        if adopts:
            moved = _move_locked(cfg, adopts, playlist_key)
            if moved:
                return Reserved(moved, adopted_from=adopts)
        remote_id = create()
        _record_playlist_locked(cfg, playlist_key, remote_id)
        return Reserved(remote_id, created=True)
    finally:
        lock.__exit__(None, None, None)


def _move_locked(cfg: config.Config, recorded_key: str, playlist_key: str) -> str:
    """Move one record to a new key. The remote id moved, or empty for none.

    A MOVE AND NOT A COPY. Two keys naming one remote playlist would make the
    old path, if a crate is ever created there again, write onto a playlist that
    now belongs to this one. ``formerly`` keeps the path it came from, so the
    file still says how the record got here.
    """
    document = _load(cfg)
    record = document["playlists"].get(recorded_key) or {}
    remote = record.get("remote_id")
    if not remote:
        return ""
    # WHAT WAS WRITTEN UNDER THIS KEY BEFORE A REMOTE ID WAS, which is the shape
    # ``record_playlist_track`` leaves when it runs first. Kept rather than
    # overwritten, since forgetting an added track is how it is added twice.
    stub = document["playlists"].get(playlist_key) or {}
    for field in ("added", "tracks"):
        merged = _listed(record, field)
        merged += [item for item in _listed(stub, field) if item not in merged]
        record[field] = merged
    record["formerly"] = [*_listed(record, "formerly"), recorded_key]
    del document["playlists"][recorded_key]
    document["playlists"][playlist_key] = record
    _write(cfg, document)
    return str(remote)


def record_playlist_track(
    cfg: config.Config, playlist_key: str, remote_id: str, *, local: str = ""
) -> None:
    """Remember one track written to the remote playlist, and the row it was.

    ``local`` IS THE LIBRARY IDENTITY, and it is what :func:`recognise` reads. The
    remote ids in ``added`` cannot serve: a crate under a new path is recognised
    when it is QUEUED, and a row's remote id is only known once the provider has
    been asked, per item, at drive time.
    """
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        record = document["playlists"].setdefault(
            playlist_key, {"remote_id": "", "added": []}
        )
        added = _listed(record, "added")
        if remote_id not in added:
            added.append(remote_id)
        record["added"] = added
        if local:
            tracks = _listed(record, "tracks")
            if local not in tracks:
                tracks.append(local)
            record["tracks"] = tracks
        document["playlists"][playlist_key] = record
        _write(cfg, document)
    finally:
        lock.__exit__(None, None, None)


def record_playlist_row(cfg: config.Config, playlist_key: str, local: str) -> None:
    """Remember a library row that was ALREADY on the remote playlist.

    Nothing was written to the account, so nothing joins ``added``. The row
    joins ``tracks`` anyway, and that is how a record written before this build
    comes to hold the tracks :func:`recognise` needs: its next export under the
    same key finds every row already there and records each one. It writes only
    when the row is new to the record, so a settled crate costs no writes.
    """
    if not local:
        return
    record = _load(cfg)["playlists"].get(playlist_key) or {}
    if local in _listed(record, "tracks"):
        return
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        record = document["playlists"].setdefault(
            playlist_key, {"remote_id": "", "added": []}
        )
        tracks = _listed(record, "tracks")
        if local not in tracks:
            tracks.append(local)
        record["tracks"] = tracks
        _write(cfg, document)
    finally:
        lock.__exit__(None, None, None)


def record_heart(cfg: config.Config, remote_id: str) -> None:
    """Remember one heart so a re-run does not add it again."""
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        document["hearts"][remote_id] = "hearted"
        _write(cfg, document)
    finally:
        lock.__exit__(None, None, None)
