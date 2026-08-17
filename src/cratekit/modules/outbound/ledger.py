"""What this library already wrote to a streaming account.

A year watermark is not this file. This file is the remote identifiers a
re-run must reuse so an interrupted write does not create a second playlist
or a second heart. It SURVIVES a library rollback: the remote account does
not roll back, and forgetting a remote id is how the next export duplicates.
"""

from __future__ import annotations

import json
from typing import Any, Mapping

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
        document = _load(cfg)
        existing = document["playlists"].get(playlist_key) or {
            "remote_id": remote_id,
            "added": [],
        }
        existing["remote_id"] = remote_id
        existing.setdefault("added", [])
        document["playlists"][playlist_key] = existing
        _write(cfg, document)
    finally:
        lock.__exit__(None, None, None)


def record_playlist_track(cfg: config.Config, playlist_key: str, remote_id: str) -> None:
    """Remember one track added to the remote playlist."""
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        record = document["playlists"].setdefault(
            playlist_key, {"remote_id": "", "added": []}
        )
        added = list(record.get("added") or [])
        if remote_id not in added:
            added.append(remote_id)
        record["added"] = added
        document["playlists"][playlist_key] = record
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
