"""What this library already wrote to a streaming account.

The remote identifiers a re-run must reuse so an interrupted write never makes a
second playlist or heart. It SURVIVES a library rollback: the account does not
roll back. One locked JSON document, each map carried through every write:
``playlists`` and ``hearts``; ``labels`` (R-835) with their year playlists and
``dated`` ones (U123); ``sets`` and ``set_folders`` (R-837, U142), a root
folder's NAME to its identifier; ``kind_folders`` (U131); ``mirrors`` (U147)
with each playlist's ``agreed`` snapshot (U201), ``mirror_links`` and
``mirror_misses`` (R-1031). :func:`product_made` says which playlists the
product made (R-836), the only ones that may lose a track.

The reservations live in :mod:`.ledger_reserve` and the settlement in
:mod:`.ledger_settle`, both named here so every caller and patch reads this module.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
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


def _refused(cfg: config.Config, what: str) -> CratekitError:
    """:func:`_unusable` for the ledger of ``cfg``."""
    return _unusable(config.state_path("outbound_writes", cfg), what)


#: Every map the document holds, in the order an empty one is made.
_MAPS = (
    "playlists", "hearts", "labels", "sets", "set_folders", "kind_folders", "mirrors",
    "mirror_links", "mirror_misses",
)


def _empty() -> dict[str, Any]:
    return {"version": LEDGER_VERSION, **{name: {} for name in _MAPS}}


def _load(cfg: config.Config) -> dict[str, Any]:
    path = config.state_path("outbound_writes", cfg)
    raw = config.read_json_map(path, lambda why: _unusable(path, why))
    return _empty() if raw is None else _parsed(path, raw)


def _maps(value: Any) -> bool:
    """Whether ``value`` is a map of maps."""
    return isinstance(value, Mapping) and all(isinstance(one, Mapping) for one in value.values())


def _parsed(path, raw: Mapping[str, Any]) -> dict[str, Any]:
    """The document as read, or the refusal a malformed one earns.

    An unreadable playlist record or miss is dropped, costing one more request;
    a label, set, kind folder or mirror is REFUSED, since one dropped is made twice.
    """
    version = raw.get("version")
    if version not in (None, LEDGER_VERSION):
        raise _unusable(
            path, f"it says version {version!r} and this build writes {LEDGER_VERSION}"
        )
    playlists = raw.get("playlists", {})
    hearts = raw.get("hearts", {})
    labels = raw.get("labels", {})
    if not isinstance(playlists, Mapping) or not isinstance(hearts, Mapping):
        raise _unusable(path, "playlists and hearts must both be maps")
    if not _maps(labels):
        raise _unusable(path, "labels must be a map of label records")
    sets = raw.get("sets", {})
    set_folders = raw.get("set_folders", {})
    if not _maps(sets):
        raise _unusable(path, "sets must be a map of set playlist records")
    if not isinstance(set_folders, Mapping):
        raise _unusable(path, "set_folders must be a map of folder name to folder")
    kind_folders = raw.get("kind_folders", {})
    if not _maps(kind_folders):
        raise _unusable(path, "kind_folders must be a map of kind folder records")
    mirrors = raw.get("mirrors", {})
    if not _maps(mirrors) or not all(
        isinstance(value.get("playlists", {}), Mapping) for value in mirrors.values()
    ):
        raise _unusable(path, "mirrors must be a map of mirrored folder records")
    links = raw.get("mirror_links", {})
    if not isinstance(links, Mapping):
        raise _unusable(path, "mirror_links must be a map of content row to account track")
    misses = raw.get("mirror_misses", {})
    if not isinstance(misses, Mapping):
        raise _unusable(path, "mirror_misses must be a map of content row to its miss")
    # A MISS GIVES WAY only to a link read below, never to a raw entry with no
    # account track, which would forget the miss and link nothing.
    linked = {
        str(content_id)
        for content_id, value in links.items()
        if isinstance(value, Mapping) and value.get("remote")
    }
    return {
        "version": LEDGER_VERSION,
        "playlists": {str(key): dict(value) for key, value in playlists.items()
                      if isinstance(value, Mapping)},
        "hearts": {str(key): str(value) for key, value in hearts.items()},
        "labels": {str(key): _label_document(path, value) for key, value in labels.items()},
        "sets": {
            str(key): {
                "remote_id": str(value.get("remote_id") or ""),
                "year": str(value.get("year") or ""),
                "added": _listed(value, "added"),
                "refused": _listed(value, "refused"),
            }
            for key, value in sets.items()
        },
        "set_folders": {str(name): str(folder) for name, folder in set_folders.items() if folder},
        "kind_folders": {
            str(kind): {
                "folder_id": str(value["folder_id"]), "created": value.get("created") is True
            }
            for kind, value in kind_folders.items()
            if value.get("folder_id")
        },
        "mirrors": {str(name): _mirror_document(value) for name, value in mirrors.items()},
        "mirror_links": {
            str(content_id): {"remote": str(value["remote"]), "isrc": str(value.get("isrc") or "")}
            for content_id, value in links.items()
            if isinstance(value, Mapping) and value.get("remote")
        },
        "mirror_misses": {
            str(content_id): {
                "reason": str(value.get("reason") or ""),
                "under": [str(one) for one in value["under"]],
            }
            for content_id, value in misses.items()
            if isinstance(value, Mapping)
            and isinstance(value.get("under"), list)
            and str(content_id) not in linked
        },
    }


def _label_document(path, raw: Mapping[str, Any]) -> dict[str, Any]:
    """One label's record as written, or the refusal a malformed one earns."""
    years = raw.get("years", {})
    if not _maps(years):
        raise _unusable(path, "a label record's years must be a map of year records")
    return {
        "name": str(raw.get("name") or ""),
        "folder_id": str(raw.get("folder_id") or ""),
        "years": {
            str(year): {
                "remote_id": str(record.get("remote_id") or ""),
                "name": str(record.get("name") or ""),
                "added": _listed(record, "added"),
                "refused": _listed(record, "refused"),
                "pruned": _listed(record, "pruned"),
                # Absent before R-836 and kept absent, so a gate can say the
                # record predates the field rather than call it adopted.
                **({"created": record["created"]} if isinstance(record.get("created"), bool) else {}),
            }
            for year, record in years.items()
        },
        # Only a created dated playlist is written (U123), so anything but a
        # name to an identifier is dropped rather than read as made here.
        **(
            {"dated": {str(name): str(pid) for name, pid in dated.items() if name and pid}}
            if isinstance(dated := raw.get("dated"), Mapping)
            else {}
        ),
    }


def _mirror_document(value: Mapping[str, Any]) -> dict[str, Any]:
    """One mirrored folder's record as written (U147)."""
    return {
        "folder_id": str(value.get("folder_id") or ""),
        "created": value.get("created") is True,
        "playlists": {
            str(title): {
                "remote_id": str(record.get("remote_id") or ""),
                "refused": _listed(record, "refused"),
                # Absent is a playlist never agreed, not one agreed empty (U201).
                **(
                    {"agreed": _listed(record, "agreed")}
                    if isinstance(record.get("agreed"), list)
                    else {}
                ),
            }
            for title, record in (value.get("playlists") or {}).items()
            if isinstance(record, Mapping) and record.get("remote_id")
        },
        # The library's own placements (U236), kept only where a track is listed.
        **(
            {"placed": placed}
            if (placed := _placements(value.get("placed")))
            else {}
        ),
    }


def _write(cfg: config.Config, document: Mapping[str, Any]) -> None:
    path = config.state_path("outbound_writes", cfg)
    payload = json.dumps(document, indent=2, sort_keys=True) + "\n"
    config.atomic_write_bytes(payload.encode("utf-8"), path)


def _locked(cfg: config.Config):
    lock = config.exclusive_lock(config.state_path("outbound_writes_lock", cfg))
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


@contextmanager
def _open(cfg: config.Config) -> Iterator[dict[str, Any]]:
    """The document read under the lock, held for the block. Every write is made in one."""
    lock = _locked(cfg)
    try:
        yield _load(cfg)
    finally:
        lock.__exit__(None, None, None)


def _listed(record: Mapping[str, Any], field: str) -> list[str]:
    """One list valued field of a record, or empty when it is not a list."""
    value = record.get(field) or []
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _rows(record: Mapping[str, Any]) -> dict[str, str]:
    """A record's library row to remote track map, or empty when it has none."""
    rows = record.get("rows")
    if not isinstance(rows, Mapping):
        return {}
    return {str(key): str(value) for key, value in rows.items()}


def _placements(value: Any) -> dict[str, dict[str, str]]:
    """A mirrored folder's placements, title to track to its membership's time (U236).

    A placement that cannot be read is dropped, and a title holding none.
    """
    if not isinstance(value, Mapping):
        return {}
    found: dict[str, dict[str, str]] = {}
    for title, tracks in value.items():
        if not isinstance(tracks, Mapping):
            continue
        listed = {
            str(track): str(at)
            for track, at in tracks.items()
            if str(track) and isinstance(at, str) and at
        }
        if listed:
            found[str(title)] = dict(sorted(listed.items()))
    return found


def _later(candidate: str, recorded: str) -> bool:
    """Whether one ISO date is after another, an unreadable recorded one losing."""
    try:
        new = datetime.fromisoformat(candidate)
    except ValueError:
        return False
    try:
        return new > datetime.fromisoformat(recorded)
    except ValueError:
        return True


def _ids(records: Iterable[Mapping[str, Any]]) -> frozenset[str]:
    """The remote identifier of every record that has one."""
    return frozenset(str(record.get("remote_id")) for record in records if record.get("remote_id"))


def _years(document: Mapping[str, Any]) -> Iterator[dict[str, Any]]:
    """Every label's year records."""
    for record in document["labels"].values():
        yield from (record.get("years") or {}).values()


def _mirrored(document: Mapping[str, Any]) -> Iterator[dict[str, Any]]:
    """Every mirrored playlist's record."""
    for record in document["mirrors"].values():
        yield from (record.get("playlists") or {}).values()


# ── Exported playlists and hearts ─────────────────────────────────────────────


def playlist_remote_id(cfg: config.Config, playlist_key: str) -> str | None:
    """The remote playlist already created for this local playlist, if any."""
    record = _load(cfg)["playlists"].get(playlist_key)
    if not record:
        return None
    remote = record.get("remote_id")
    return str(remote) if remote else None


def playlist_added(cfg: config.Config, playlist_key: str) -> frozenset[str]:
    """Remote track ids already recorded as written onto this playlist."""
    return frozenset(_listed(_load(cfg)["playlists"].get(playlist_key) or {}, "added"))


def recorded_hearts(cfg: config.Config) -> frozenset[str]:
    """Remote track ids this library has already hearted."""
    return frozenset(_load(cfg)["hearts"])


def exported_playlist_ids(cfg: config.Config) -> frozenset[str]:
    """Every remote playlist an export recorded, read once (U131)."""
    return _ids(_load(cfg)["playlists"].values())


@dataclass(frozen=True, slots=True)
class ExportedPlaylist:
    """One exported playlist's record, read once for a prune plan."""

    key: str
    remote_id: str
    added: frozenset[str] = frozenset()
    pruned: frozenset[str] = frozenset()
    #: The ISO date of the newest collection export it was written from.
    written: str = ""
    #: Library row to the remote track it was matched to.
    rows: Mapping[str, str] = field(default_factory=dict)


def exported_playlist(cfg: config.Config, playlist_key: str) -> ExportedPlaylist | None:
    """The record an export wrote under this key, or ``None``. Read only."""
    record = _load(cfg)["playlists"].get(playlist_key) or {}
    remote = str(record.get("remote_id") or "")
    if not remote:
        return None
    return ExportedPlaylist(
        key=playlist_key, remote_id=remote, added=frozenset(_listed(record, "added")),
        pruned=frozenset(_listed(record, "pruned")), written=str(record.get("written") or ""),
        rows=_rows(record),
    )


def older_than(given: str, recorded: str) -> bool:
    """Whether an export dated ``given``, empty when unreadable, is older than the recorded date."""
    if not recorded:
        return False
    return not given or _later(recorded, given)


# ── A label's folder of year playlists (R-835) and its dated playlists (U123) ───


@dataclass(frozen=True, slots=True)
class LabelYear:
    """One year playlist this library built for a label, as recorded."""

    year: str
    remote_id: str
    #: The title it was created or adopted under, never one a mark wrote since.
    name: str
    added: frozenset[str] = frozenset()
    #: Tracks the provider would not add, never asked again.
    refused: frozenset[str] = frozenset()
    #: Tracks a prune took off (R-836), never added back by a build.
    pruned: frozenset[str] = frozenset()
    #: Created here, or adopted, or None for a record older than the field.
    created: bool | None = None


@dataclass(frozen=True, slots=True)
class LabelShape:
    """What this library has built on the account for one label."""

    label_id: str
    name: str = ""
    folder_id: str = ""
    years: Mapping[str, LabelYear] = field(default_factory=dict)
    #: U123. Each dated playlist the dated plan created, name to identifier.
    dated: Mapping[str, str] = field(default_factory=dict)


def label_shape(cfg: config.Config, label_id: str) -> LabelShape:
    """The folder and year playlists recorded for one label. Read only."""
    record = _load(cfg)["labels"].get(label_id)
    if not record:
        return LabelShape(label_id=label_id)
    return LabelShape(
        label_id=label_id,
        name=str(record.get("name") or ""),
        folder_id=str(record.get("folder_id") or ""),
        years={
            year: LabelYear(
                year=year, remote_id=str(entry.get("remote_id") or ""),
                name=str(entry.get("name") or ""), added=frozenset(_listed(entry, "added")),
                refused=frozenset(_listed(entry, "refused")),
                pruned=frozenset(_listed(entry, "pruned")),
                created=entry["created"] if isinstance(entry.get("created"), bool) else None,
            )
            for year, entry in (record.get("years") or {}).items()
            if entry.get("remote_id")
        },
        dated=dict(record.get("dated") or {}),
    )


def label_playlist_ids(cfg: config.Config) -> frozenset[str]:
    """Every year playlist this library built for any label, never swept as intake."""
    return _ids(_years(_load(cfg)))


def label_dated_ids(cfg: config.Config) -> frozenset[str]:
    """Every dated playlist made for any label (U123), never one ``sync pair`` keeps."""
    return frozenset(
        str(remote_id) for record in _load(cfg)["labels"].values()
        for remote_id in (record.get("dated") or {}).values() if remote_id
    )


# ── Set playlists, and the root folders they and the filing use (R-837, U142) ───


@dataclass(frozen=True, slots=True)
class SetPlaylist:
    """One playlist this library made on the account from a set's tracklist."""

    name: str
    remote_id: str
    #: The year it was made in, which names the folder it is archived in.
    year: str
    added: frozenset[str] = frozenset()
    #: Tracks the provider would not add, never asked again.
    refused: frozenset[str] = frozenset()


def set_playlist(cfg: config.Config, name: str) -> SetPlaylist | None:
    """The set playlist recorded under this name, or ``None``. Read only."""
    record = _load(cfg)["sets"].get(name)
    if not record or not record.get("remote_id"):
        return None
    return SetPlaylist(
        name=name, remote_id=str(record["remote_id"]), year=str(record.get("year") or ""),
        added=frozenset(_listed(record, "added")), refused=frozenset(_listed(record, "refused")),
    )


def set_playlist_names(cfg: config.Config) -> tuple[str, ...]:
    """The name of every set playlist recorded with an identifier, sorted. Read only."""
    sets = _load(cfg)["sets"]
    return tuple(sorted(str(name) for name, one in sets.items() if one and one.get("remote_id")))


def set_playlist_ids(cfg: config.Config) -> frozenset[str]:
    """Every set playlist this library made, which swept as intake would download the set twice."""
    return _ids(_load(cfg)["sets"].values())


def set_folders(cfg: config.Config) -> dict[str, str]:
    """Every root folder recorded, its name to its identifier (U144). Read only."""
    return {str(name): str(one) for name, one in _load(cfg)["set_folders"].items() if one}


def set_folder(cfg: config.Config, name: str) -> str:
    """The root folder recorded under its name, ``Downloaded Sets 2026`` or ``2026``, or ``""``."""
    return str(_load(cfg)["set_folders"].get(name) or "")


@dataclass(frozen=True, slots=True)
class KindFolder:
    """The root folder recorded for one kind of playlist (U131), or none."""

    folder_id: str = ""
    #: True only when this product created the folder. One adopted by its name
    #: may be a person's, and nothing is ever moved out of a person's folder.
    created: bool = False


def kind_folder(cfg: config.Config, kind: str) -> KindFolder:
    """The root folder recorded for ``kind``, ``Mine`` or ``Exports``. Read only."""
    record = _load(cfg)["kind_folders"].get(kind) or {}
    return KindFolder(
        folder_id=str(record.get("folder_id") or ""), created=record.get("created") is True
    )


# ── The account mirrors of the genre tree and the Favorites folder (U147) ─────


@dataclass(frozen=True, slots=True)
class MirrorPlaylist:
    """One playlist the product made inside a mirrored folder, as recorded."""

    name: str
    remote_id: str
    #: Tracks the provider would not add, never asked again.
    refused: frozenset[str] = frozenset()
    #: The snapshot (U201): the account tracks both sides held when the mirror
    #: last finished this playlist, or ``None`` for one never agreed.
    agreed: frozenset[str] | None = None


@dataclass(frozen=True, slots=True)
class MirrorFolder:
    """One mirrored root folder, and every playlist the product made in it."""

    name: str
    folder_id: str = ""
    #: True only when this product created the folder; one adopted by its name
    #: may be a person's. Said on the gate, never a reason to remove anything.
    created: bool = False
    playlists: Mapping[str, MirrorPlaylist] = field(default_factory=dict)
    #: The library's own placements (U236), by account title: each track an
    #: account edit placed in rekordbox that the account does not hold yet, to
    #: that membership's time, which the edit rule reads as no person's change.
    placed: Mapping[str, Mapping[str, str]] = field(default_factory=dict)


def mirror_folders(cfg: config.Config) -> dict[str, MirrorFolder]:
    """Every mirrored folder recorded, by its name. Read only."""
    return {
        name: MirrorFolder(
            name=name,
            folder_id=str(record.get("folder_id") or ""),
            created=record.get("created") is True,
            playlists={
                title: MirrorPlaylist(
                    name=title, remote_id=str(entry["remote_id"]),
                    refused=frozenset(_listed(entry, "refused")),
                    agreed=(
                        frozenset(_listed(entry, "agreed"))
                        if isinstance(entry.get("agreed"), list)
                        else None
                    ),
                )
                for title, entry in (record.get("playlists") or {}).items()
            },
            placed=_placements(record.get("placed")),
        )
        for name, record in _load(cfg)["mirrors"].items()
    }


def mirror_playlist_ids(cfg: config.Config) -> frozenset[str]:
    """Every mirrored playlist the product made, for the intake sweep to leave alone."""
    return _ids(_mirrored(_load(cfg)))


def recorded_folder_ids(cfg: config.Config) -> frozenset[str]:
    """Every account root folder this ledger keeps, which ``sync pair`` never adopts (U198)."""
    document = _load(cfg)
    found = {str(record.get("folder_id") or "") for record in document["labels"].values()}
    found |= {str(folder_id or "") for folder_id in document["set_folders"].values()}
    found |= {
        str((record or {}).get("folder_id") or "") for record in document["kind_folders"].values()
    }
    found |= {str(record.get("folder_id") or "") for record in document["mirrors"].values()}
    return frozenset(one for one in found if one)


def mirror_links(cfg: config.Config) -> dict[str, tuple[str, str]]:
    """Each content row a mirror matched, to ``(account track, ISRC matched under)``."""
    return {
        content_id: (str(value["remote"]), str(value.get("isrc") or ""))
        for content_id, value in _load(cfg)["mirror_links"].items()
    }


def mirror_misses(cfg: config.Config) -> dict[str, tuple[str, tuple[str, ...]]]:
    """Each content row the mirror could not match, to ``(reason, what it was asked under)``."""
    return {
        content_id: (str(value["reason"]), tuple(value["under"]))
        for content_id, value in _load(cfg)["mirror_misses"].items()
    }


# ── What the product made (R-836) ─────────────────────────────────────────────


def product_made(cfg: config.Config, playlist_id: str) -> bool:
    """Whether this product created the remote playlist, by the ledger alone.

    THE QUESTION A REMOVAL ASKS FIRST: yes for an exported, set, mirrored or
    dated playlist's record, and a label year's only when written ``created``.
    ADOPTED ANYWHERE WINS over any other record of the same playlist.
    """
    wanted = str(playlist_id or "")
    if not wanted:
        return False
    return _made_in(_load(cfg), wanted)


def product_made_among(cfg: config.Config, playlist_ids) -> frozenset[str]:
    """Those of ``playlist_ids`` this product created, :func:`product_made` with one read."""
    document = _load(cfg)
    return frozenset(
        str(one) for one in playlist_ids if str(one or "") and _made_in(document, str(one))
    )


def _made_in(document: dict, wanted: str) -> bool:
    """:func:`product_made`'s rule over a ledger already read."""
    made = False
    for record in document["labels"].values():
        for entry in (record.get("years") or {}).values():
            if str(entry.get("remote_id") or "") == wanted:
                if entry.get("created") is not True:
                    return False
                made = True
        if wanted in (record.get("dated") or {}).values():
            made = True
    if made:
        return True
    for record in (*document["playlists"].values(), *document["sets"].values()):
        if str(record.get("remote_id") or "") == wanted:
            return True
    # U147. A mirrored playlist is only ever created, never adopted.
    return any(str(entry.get("remote_id") or "") == wanted for entry in _mirrored(document))


from cratekit.modules.outbound.ledger_reserve import (  # noqa: E402, F401
    GROWN_DENOMINATOR,
    GROWN_NUMERATOR,
    SHARED_DENOMINATOR,
    SHARED_NUMERATOR,
    Recognition,
    Reserved,
    _still_carries,
    recognise,
    record_playlist,
    rename_set_playlist,
    reserve_kind_folder,
    reserve_label_dated,
    reserve_label_folder,
    reserve_label_year,
    reserve_mirror_folder,
    reserve_mirror_playlist,
    reserve_playlist,
    reserve_set_folder,
    reserve_set_playlist,
)
from cratekit.modules.outbound.ledger_settle import (  # noqa: E402, F401
    forget_label_dated,
    forget_mirror_playlist,
    record_heart,
    record_label_pruned,
    record_label_tracks,
    record_mirror_agreed,
    record_mirror_links,
    record_mirror_misses,
    record_mirror_refused,
    record_playlist_pruned,
    record_playlist_row,
    record_playlist_track,
    record_playlist_tracks,
    record_set_tracks,
    settle_mirror_tracks,
)
