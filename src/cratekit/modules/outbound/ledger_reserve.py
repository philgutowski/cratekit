"""The ledger's reservations: which remote playlist or folder a write goes to.

A reserve answers the recorded identifier, or creates one and records it, with
the lock TAKEN BEFORE THE CREATE: an unwritable ledger refuses before anything
exists on the account, rather than leave a playlist nothing remembers, which
every later item makes again. A write failing under the held lock survives as a
residual, since closing it needs a create the provider can make idempotent.

``_load`` and ``_write`` are looked up on :mod:`.ledger` at call time, and
``_open`` reads its globals there, so a test that patches them reaches here.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Any, Mapping

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

#: The share of what a crate held at its LAST export it must still carry to be
#: recognised under a new path: HALF, in integers. A crate that lost more is
#: more likely another, and a wrong adoption writes onto its playlist.
SHARED_NUMERATOR = 1
SHARED_DENOMINATOR = 2

#: How much of the CRATE the shared tracks must be: a QUARTER, so a huge crate
#: holding a small deleted one's music is not offered its playlist.
GROWN_NUMERATOR = 1
GROWN_DENOMINATOR = 4


@dataclass(frozen=True, slots=True)
class Recognition:
    """What the ledger can say about the remote playlist a crate will write to.

    KEYED BY DISPLAY PATH, there being nothing else (R-229), so a renamed crate
    arrives under a key nothing was recorded against. One read answers all the
    gate shows. ``adopts`` is set only when EXACTLY ONE key qualifies, and
    ``candidates`` names every one, so two are reported rather than resolved.
    ``shared``, ``recorded`` and ``crate`` are the evidence, the first two zero
    for a record recognised by name. ``mismatched`` says the crate's own record
    no longer carries half of it, and ``claimed_by`` names who in the export does.
    """

    own_remote_id: str = ""
    adopts: str = ""
    remote_id: str = ""
    shared: int = 0
    recorded: int = 0
    crate: int = 0
    candidates: tuple[str, ...] = ()
    mismatched: bool = False
    claimed_by: tuple[str, ...] = ()

    @property
    def ambiguous(self) -> bool:
        return len(self.candidates) > 1

    def without_offer(self) -> "Recognition":
        """The same reading with the offer taken off, for a person who said no.

        Not ``declined``, which is the export shell's payload for an abort.
        """
        return Recognition(
            own_remote_id=self.own_remote_id, crate=self.crate, mismatched=self.mismatched,
            claimed_by=self.claimed_by,
        )


def _legacy(record: Mapping[str, Any]) -> bool:
    """Whether a build that recorded no crate contents wrote this record: the field's ABSENCE."""
    return not isinstance(record.get("tracks"), list)


def _same_name(recorded_key: str, name: str) -> bool:
    """Whether a recorded display path ends in this name, by suffix since a name may hold ``/``."""
    return bool(name) and (recorded_key == name or recorded_key.endswith("/" + name))


def _still_carries(written: frozenset[str], crate: frozenset[str]) -> bool:
    """Whether ``crate`` still holds enough of what a record was written from."""
    shared = len(written & crate)
    return shared >= 1 and shared * SHARED_DENOMINATOR >= len(written) * SHARED_NUMERATOR


def _grown_within(written: frozenset[str], crate: frozenset[str]) -> bool:
    """Whether the shared tracks are enough of the crate, not only of the record."""
    return len(written & crate) * GROWN_DENOMINATOR >= len(crate) * GROWN_NUMERATOR


def recognise(
    cfg: config.Config, playlist_key: str, *, name: str, track_ids: Iterable[str],
    live: Mapping[str, Iterable[str]],
) -> Recognition:
    """Which recorded remote playlist this crate writes to, as far as can be told.

    READ ONLY: the gate shows it and :func:`reserve_playlist` acts on that. A key
    still in ``live``, the export's paths and tracks, is a living crate never
    offered, unless it no longer carries half its record: a reused path. A
    record qualifies by the shared and grown fractions, or, kept before contents
    were, by display name alone while its own path is gone. An old export reads
    a newer record as orphaned, which is why this is an offer on a dated gate.
    """
    playlists = ledger._load(cfg)["playlists"]
    wanted = frozenset(str(track) for track in track_ids)
    living = {str(key): frozenset(str(t) for t in ids) for key, ids in live.items()}
    own = playlists.get(playlist_key) or {}
    if own.get("remote_id"):
        written = frozenset(_listed(own, "tracks"))
        mismatched = bool(written) and not _still_carries(written, wanted)
        claimed = (
            sorted(
                key
                for key, ids in living.items()
                if key != playlist_key
                and not (playlists.get(key) or {}).get("remote_id")
                and _still_carries(written, ids)
                and _grown_within(written, ids)
            )
            if mismatched
            else []
        )
        return Recognition(
            own_remote_id=str(own["remote_id"]), crate=len(wanted), mismatched=mismatched,
            claimed_by=tuple(claimed),
        )
    found: list[tuple[str, str, int, int]] = []
    for key, record in playlists.items():
        remote = record.get("remote_id")
        if not remote or key == playlist_key:
            continue
        written = frozenset(_listed(record, "tracks"))
        if key in living and (not written or _still_carries(written, living[key])):
            continue
        if written:
            if _still_carries(written, wanted) and _grown_within(written, wanted):
                found.append((key, str(remote), len(written & wanted), len(written)))
        elif _legacy(record) and _same_name(key, name):
            found.append((key, str(remote), 0, 0))
    candidates = tuple(sorted(key for key, *_rest in found))
    if len(found) != 1:
        return Recognition(crate=len(wanted), candidates=candidates)
    key, remote, shared, recorded = found[0]
    return Recognition(
        adopts=key, remote_id=remote, shared=shared, recorded=recorded, crate=len(wanted),
        candidates=candidates,
    )


# ── An exported playlist ──────────────────────────────────────────────────────


def record_playlist(cfg: config.Config, playlist_key: str, remote_id: str) -> None:
    """Remember the remote playlist so a re-run updates it rather than creating."""
    with _open(cfg) as document:
        existing = document["playlists"].get(playlist_key) or {"remote_id": remote_id, "added": []}
        existing["remote_id"] = remote_id
        existing.setdefault("added", [])
        document["playlists"][playlist_key] = existing
        ledger._write(cfg, document)


@dataclass(frozen=True, slots=True)
class Reserved:
    """The remote playlist a crate writes to, and how this call came by it.

    ``key`` is where the record lives now. ``adopted_from`` is the key THIS call
    moved it from, under the lock, so two drivers never both report one move.
    ``added`` and ``rows`` (R-836) ride along because the caller asks next.
    """

    remote_id: str
    created: bool = False
    adopted_from: str = ""
    key: str = ""
    added: frozenset[str] = frozenset()
    rows: Mapping[str, str] = field(default_factory=dict)


def _moved_on(what: str, **detail: str) -> CratekitError:
    return refuse(
        "outbound-record-moved",
        f"{what}, so writing now would either create a remote playlist nobody "
        f"confirmed or write onto one that has since been given to another "
        f"playlist. Nothing was written for this item",
        steps=("queue the export again, so its plan is built against what the ledger holds now",),
        scope=Scope.RUN,
        origin=("outbound.ledger",),
        detail=dict(detail),
    )


def reserve_playlist(
    cfg: config.Config, playlist_key: str, create: Callable[[], str], *, adopts: str = "",
    expected: str = "", contents: Iterable[str] = (), written: str = "",
) -> Reserved:
    """The remote playlist for this crate, creating one only if none is recorded.

    ``adopts`` is a confirmed key the crate used to live under (R-229): its
    record MOVES here, and with no record anywhere this REFUSES, a create being
    another write than the update confirmed. ``expected`` is the remote playlist
    the job was confirmed to update, found BY ID once its record moved, refused
    when nothing holds it. ``contents`` REPLACES the recorded crate, written
    whole and never through a forwarded key. ``written`` is the export's date.
    """
    held = [str(item) for item in contents]
    with _open(cfg) as document:
        noted = _note_written(document, playlist_key, expected, written)
        playlists = document["playlists"]
        own = str((playlists.get(playlist_key) or {}).get("remote_id") or "")
        if adopts:
            if own:
                return _settled(cfg, document, playlist_key, held, dirty=noted)
            if not (playlists.get(adopts) or {}).get("remote_id"):
                raise _moved_on(
                    f"the remote playlist recorded for {adopts!r}, which this "
                    f"job was confirmed to adopt, is no longer recorded there",
                    playlist=playlist_key,
                    adopts=adopts,
                )
            _move(document, adopts, playlist_key)
            return _settled(cfg, document, playlist_key, held, adopted_from=adopts)
        if expected and own != expected:
            holders = [
                key for key, record in playlists.items()
                if str(record.get("remote_id") or "") == expected
            ]
            if len(holders) != 1:
                raise _moved_on(
                    f"the remote playlist {expected}, which this job was "
                    f"confirmed to update, is no longer recorded for any playlist",
                    playlist=playlist_key,
                    remote_id=expected,
                )
            return _settled(cfg, document, holders[0], (), dirty=noted)
        if own:
            return _settled(cfg, document, playlist_key, held, dirty=noted)
        remote_id = create()
        record = playlists.get(playlist_key) or {"added": []}
        record["remote_id"] = remote_id
        record.setdefault("added", [])
        playlists[playlist_key] = record
        return _settled(cfg, document, playlist_key, held, created=True, dirty=True)


def _note_written(
    document: dict[str, Any], playlist_key: str, expected: str, written: str
) -> bool:
    """Carry the export's date onto the record it writes to, kept at its latest (R-836).

    ``export prune`` refuses an export older than the record's, since every
    track added since would read as gone. True when the document changed.
    """
    if not written:
        return False
    playlists = document["playlists"]
    record = playlists.get(playlist_key)
    if expected and str((record or {}).get("remote_id") or "") != expected:
        # The job writes where it was confirmed to, so the date goes there too.
        record = next(
            (one for one in playlists.values() if str(one.get("remote_id") or "") == expected),
            record,
        )
    if record is None:
        record = playlists.setdefault(playlist_key, {"added": []})
    if _later(written, str(record.get("written") or "")):
        record["written"] = written
        return True
    return False


def _settled(
    cfg: config.Config, document: dict[str, Any], key: str, held: Iterable[str], *,
    created: bool = False, adopted_from: str = "", dirty: bool = False,
) -> Reserved:
    """Record the crate's contents if they moved, write once, and answer."""
    record = document["playlists"][key]
    contents = list(held)
    if contents and record.get("tracks") != contents:
        record["tracks"] = contents
        dirty = True
    if dirty or adopted_from:
        ledger._write(cfg, document)
    return Reserved(
        remote_id=str(record["remote_id"]), created=created, adopted_from=adopted_from, key=key,
        added=frozenset(_listed(record, "added")), rows=_rows(record),
    )


def _move(document: dict[str, Any], recorded_key: str, playlist_key: str) -> None:
    """Move one record to a new key, in the document, for the caller to write.

    A MOVE, since two keys on one playlist let the old path write onto it; a
    stub under the new key is merged in, a forgotten added track being added
    twice. ``formerly`` keeps the old path.
    """
    playlists = document["playlists"]
    record = playlists.pop(recorded_key)
    stub = playlists.get(playlist_key) or {}
    merged = _listed(record, "added")
    merged += [item for item in _listed(stub, "added") if item not in merged]
    record["added"] = merged
    if _later(str(stub.get("written") or ""), str(record.get("written") or "")):
        record["written"] = stub["written"]
    if _rows(stub):
        record["rows"] = {**_rows(record), **_rows(stub)}
    record["formerly"] = [*_listed(record, "formerly"), recorded_key]
    playlists[playlist_key] = record


# ── Folders and playlists the label, set, kind and mirror steps make ──────────

#: Reads one map of records off the document, made where it is missing.
_Table = Callable[[dict[str, Any]], dict[str, Any]]


def _reserve(
    cfg: config.Config, table: _Table, key: str, create: Callable[[], str],
    record: Callable[[str], dict[str, Any]],
) -> tuple[str, bool]:
    """The playlist recorded under ``key``, or one ``create`` made and ``record`` describes."""
    with _open(cfg) as document:
        held = table(document)
        recorded = str((held.get(key) or {}).get("remote_id") or "")
        if recorded:
            return recorded, False
        remote_id = create()
        held[key] = record(remote_id)
        ledger._write(cfg, document)
        return remote_id, True


def _reserve_folder(
    cfg: config.Config, create: Callable[[], str], adopt: str, stale: str,
    entry: Callable[[dict[str, Any]], str], keep: Callable[[dict[str, Any], str, bool], None],
) -> tuple[str, bool]:
    """A root folder, made only if none is recorded. ``(id, created)``.

    ``entry`` reads the recorded folder and ``keep`` records one. ``adopt`` is
    one already on the account that a person was shown; ``stale`` a recorded
    one the plan read as gone.
    """
    with _open(cfg) as document:
        recorded = entry(document)
        if recorded and recorded != stale:
            return recorded, False
        folder_id, created = (adopt, False) if adopt else (create(), True)
        keep(document, folder_id, created)
        ledger._write(cfg, document)
        return folder_id, created


def _label_entry(document: dict[str, Any], label_id: str, name: str) -> dict[str, Any]:
    record = document["labels"].setdefault(
        label_id, {"name": name, "folder_id": "", "years": {}}
    )
    if name:
        record["name"] = name
    record.setdefault("years", {})
    return record


def reserve_label_folder(
    cfg: config.Config, label_id: str, name: str, create: Callable[[], str], *,
    adopt: str = "", stale: str = "",
) -> tuple[str, bool]:
    """The label's folder, creating one only if none is recorded. ``(id, created)``."""
    return _reserve_folder(
        cfg, create, adopt, stale,
        lambda document: str(_label_entry(document, label_id, name).get("folder_id") or ""),
        lambda document, folder_id, _: document["labels"][label_id].update(folder_id=folder_id),
    )


def reserve_label_year(
    cfg: config.Config, label_id: str, year: str, name: str, create: Callable[[], str], *,
    adopt: str = "",
) -> tuple[str, bool]:
    """One year's playlist, creating it only if none is recorded. ``(id, created)``.

    ``created`` is written with the record (R-836), false for one adopted, since
    a prune may take a track off the first and never off the second.
    """
    remote_id, made = _reserve(
        cfg,
        lambda document: _label_entry(document, label_id, "")["years"],
        year,
        lambda: adopt or create(),
        lambda remote_id: {
            "remote_id": remote_id,
            "name": name,
            "added": [],
            "refused": [],
            "pruned": [],
            "created": not adopt,
        },
    )
    return remote_id, made and not adopt


def reserve_label_dated(
    cfg: config.Config, label_id: str, name: str, create: Callable[[], str]
) -> str:
    """Create one dated playlist, recorded as made here so ``label heard`` may remove it (U123).

    ALWAYS CREATES: the plan asks only when the folder holds none by the name.
    """
    with _open(cfg) as document:
        record = _label_entry(document, label_id, "")
        remote_id = create()
        record.setdefault("dated", {})[str(name)] = str(remote_id)
        ledger._write(cfg, document)
        return remote_id


def reserve_set_playlist(
    cfg: config.Config, name: str, year: str, create: Callable[[], str]
) -> tuple[str, bool]:
    """The set's playlist, creating it only if none is recorded. ``(id, created)``."""
    return _reserve(
        cfg,
        lambda document: document["sets"],
        name,
        create,
        lambda remote_id: {"remote_id": remote_id, "year": year, "added": [], "refused": []},
    )


def rename_set_playlist(cfg: config.Config, old: str, new: str, remote_id: str) -> bool:
    """Move a set playlist's record from ``old`` to ``new``, once its title is ``new`` (U140).

    Left behind, the next backfill reads the set as having none and makes a
    twin. THE IDENTIFIER MUST AGREE under both names. Answers whether it moved.
    """
    with _open(cfg) as document:
        sets = document["sets"]
        held = str((sets.get(new) or {}).get("remote_id") or "")
        if held == remote_id:
            return False
        if held:
            raise _refused(
                cfg,
                f"it already holds the set playlist {held} under {new!r}, so "
                f"{remote_id} cannot take that name",
            )
        recorded = str((sets.get(old) or {}).get("remote_id") or "")
        if recorded != remote_id:
            raise _refused(
                cfg,
                f"it records {recorded or 'no playlist'} under {old!r}, not "
                f"{remote_id}, which was just renamed",
            )
        sets[new] = sets.pop(old)
        ledger._write(cfg, document)
        return True


def reserve_set_folder(
    cfg: config.Config, name: str, create: Callable[[], str], *, adopt: str = "", stale: str = ""
) -> tuple[str, bool]:
    """The root folder recorded under ``name``, as :func:`.ledger.set_folder` reads it."""
    return _reserve_folder(
        cfg, create, adopt, stale,
        lambda document: str(document["set_folders"].get(name) or ""),
        lambda document, folder_id, _: document["set_folders"].update({name: folder_id}),
    )


def reserve_kind_folder(
    cfg: config.Config, kind: str, create: Callable[[], str], *, adopt: str = "", stale: str = ""
) -> tuple[str, bool]:
    """The kind's root folder (U131), recorded by its identifier so a rename keeps it."""
    return _reserve_folder(
        cfg, create, adopt, stale,
        lambda document: str((document["kind_folders"].get(kind) or {}).get("folder_id") or ""),
        lambda document, folder_id, created: document["kind_folders"].update(
            {kind: {"folder_id": folder_id, "created": created}}
        ),
    )


def _mirror_entry(document: dict[str, Any], name: str) -> dict[str, Any]:
    record = document["mirrors"].setdefault(
        name, {"folder_id": "", "created": False, "playlists": {}}
    )
    record.setdefault("playlists", {})
    return record


def reserve_mirror_folder(
    cfg: config.Config, name: str, create: Callable[[], str], *, adopt: str = "", stale: str = ""
) -> tuple[str, bool]:
    """The mirrored folder (U147), creating one only if none is recorded."""
    return _reserve_folder(
        cfg, create, adopt, stale,
        lambda document: str(_mirror_entry(document, name).get("folder_id") or ""),
        lambda document, folder_id, created: document["mirrors"][name].update(
            folder_id=folder_id, created=created
        ),
    )


def reserve_mirror_playlist(
    cfg: config.Config, folder: str, name: str, create: Callable[[], str]
) -> tuple[str, bool]:
    """One mirrored playlist, ALWAYS CREATED and never adopted, so it may lose a track (R-836)."""
    return _reserve(
        cfg,
        lambda document: _mirror_entry(document, folder)["playlists"],
        name,
        create,
        lambda remote_id: {"remote_id": remote_id, "refused": []},
    )


# AT THE FOOT, AFTER EVERY DEFINITION: ``ledger`` re-exports this module's
# names at its own foot, so whichever of the two is imported first finds the
# other's names already bound.
from cratekit.modules.outbound import ledger  # noqa: E402
from cratekit.modules.outbound.ledger import _later, _listed, _open, _refused, _rows  # noqa: E402
