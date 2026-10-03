"""What this library already wrote to a streaming account.

A year watermark is not this file. This file is the remote identifiers a
re-run must reuse so an interrupted write does not create a second playlist
or a second heart. It SURVIVES a library rollback: the remote account does
not roll back, and forgetting a remote id is how the next export duplicates.

SINCE R-835 IT ALSO HOLDS EACH LABEL'S SHAPE ON THE ACCOUNT, under ``labels``:
the folder a label's year playlists live in, and per year the playlist, the
title it was given and the tracks written to it. Every reader and writer here
carries the map through, so an export that writes this file never drops it.

SINCE R-837 IT HOLDS EACH SET PLAYLIST TOO, under ``sets``, keyed by the
playlist's name: the playlist an identified set or a typed tracklist became,
the year it was made in and the tracks written to it. ``set_folders`` maps a
year to the root folder its archived set playlists are filed in. Both are
carried through the way ``labels`` is, for the same reason.

SINCE R-836 IT SAYS WHICH PLAYLISTS THE PRODUCT MADE, because that is the one
kind of playlist a track may be taken off. :func:`product_made` is the answer,
and a track taken off moves from ``added`` to ``pruned`` on its record, so a
resume takes nothing off twice and a second prune plans nothing.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass, field
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
    return {
        "version": LEDGER_VERSION,
        "playlists": {},
        "hearts": {},
        "labels": {},
        "sets": {},
        "set_folders": {},
    }


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
    labels = raw.get("labels", {})
    if not isinstance(playlists, Mapping) or not isinstance(hearts, Mapping):
        raise _unusable(path, "playlists and hearts must both be maps")
    if not isinstance(labels, Mapping) or not all(
        isinstance(value, Mapping) for value in labels.values()
    ):
        # REFUSED, NOT SKIPPED, unlike a playlist record above. A label entry
        # dropped here is a folder and its year playlists forgotten, and the
        # next build would make all of them a second time.
        raise _unusable(path, "labels must be a map of label records")
    sets = raw.get("sets", {})
    set_folders = raw.get("set_folders", {})
    if not isinstance(sets, Mapping) or not all(
        isinstance(value, Mapping) for value in sets.values()
    ):
        # REFUSED for the label map's reason: a set record dropped here is a
        # playlist forgotten, and the next run onto the set makes a second one.
        raise _unusable(path, "sets must be a map of set playlist records")
    if not isinstance(set_folders, Mapping):
        raise _unusable(path, "set_folders must be a map of year to folder")
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
        "set_folders": {
            str(year): str(folder) for year, folder in set_folders.items() if folder
        },
    }


def _label_document(path, raw: Mapping[str, Any]) -> dict[str, Any]:
    """One label's record as written, or the refusal a malformed one earns."""
    years = raw.get("years", {})
    if not isinstance(years, Mapping) or not all(
        isinstance(value, Mapping) for value in years.values()
    ):
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
                # WRITTEN TRUE OR FALSE SINCE R-836, and absent before it. Absent
                # is kept absent, so a gate can say the record predates the field
                # rather than call the playlist adopted. Only true is made here.
                **({"created": record["created"]} if isinstance(record.get("created"), bool) else {}),
            }
            for year, record in years.items()
        },
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
#: integers so the comparison never leaves whole numbers. HALF, measured against
#: WHAT THE CRATE HELD AT ITS LAST EXPORT and not against everything ever
#: written, because the recorded set is replaced on every export rather than
#: grown. A crate that lost more than half of what it held is more likely a
#: different crate than the same one reorganised, and a wrong adoption writes
#: onto a remote playlist that belongs to something else.
SHARED_NUMERATOR = 1
SHARED_DENOMINATOR = 2

#: The other side of the same question: how much of the CRATE the shared tracks
#: must be. A QUARTER. Without it a three thousand track crate that happens to
#: contain a deleted eight track crate's music scores eight of eight and is
#: offered that crate's remote playlist. People add to a crate freely, so this
#: is looser than the bound above, and a crate that more than quadrupled
#: between two exports is read as a bigger crate rather than the same one.
GROWN_NUMERATOR = 1
GROWN_DENOMINATOR = 4


@dataclass(frozen=True, slots=True)
class Recognition:
    """What the ledger can say about the remote playlist a crate will write to.

    THE KEY IS A DISPLAY PATH BECAUSE THERE IS NOTHING ELSE (R-229). A rekordbox
    collection export gives a playlist a name, a place in a tree and its track
    ids, and no identifier, so a crate that is renamed or dragged into a folder
    arrives here under a key nothing was ever recorded against. Read as "never
    exported", that created a SECOND remote playlist with nothing said.

    ONE READ OF THE LEDGER ANSWERS EVERYTHING THE GATE SHOWS, which is why
    ``own_remote_id`` is carried here rather than asked for again: two reads can
    straddle a neighbour's write and describe two different ledgers in one plan.

    ``adopts`` is the recorded key whose remote playlist this crate should go on
    using, or empty. It is set only when EXACTLY ONE recorded key qualifies.
    ``candidates`` carries every key that qualified, so two is reported as two
    rather than resolved by a rule nobody chose: adopting the wrong one writes
    this crate's tracks onto another crate's remote playlist.

    ``shared``, ``recorded`` and ``crate`` are the evidence, for the sentence a
    person reads. The first two are zero for a record recognised by its name
    alone, which is a record written before this build recorded tracks at all.

    ``mismatched`` says this crate HAS a record under its own key and no longer
    carries half of what that record was written from, which is what a path
    somebody reused for a different crate looks like. ``claimed_by`` names the
    unrecorded playlists in the same export that do carry it.
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

        NOT CALLED ``declined``. ``shell.declined`` is the payload for a confirm
        somebody answered with abort, and the export shell calls both, so one
        word for two things in one file is the defect METHOD says to hunt.
        """
        return Recognition(
            own_remote_id=self.own_remote_id,
            crate=self.crate,
            mismatched=self.mismatched,
            claimed_by=self.claimed_by,
        )


def _listed(record: Mapping[str, Any], field: str) -> list[str]:
    """One list valued field of a record, or empty when it is not a list."""
    value = record.get(field) or []
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _legacy(record: Mapping[str, Any]) -> bool:
    """Whether a build that recorded no crate contents wrote this record.

    THE FIELD'S ABSENCE, NOT ITS EMPTINESS. A record this build wrote always
    carries the list, so an empty one means "this build recorded nothing to
    recognise by", which is no evidence, and is never promoted to the name rule.
    """
    return not isinstance(record.get("tracks"), list)


def _same_name(recorded_key: str, name: str) -> bool:
    """Whether a recorded display path ends in this display name.

    BY SUFFIX AND NOT BY SPLITTING, because a playlist name may itself contain
    the separator, so the last element of a split key is not reliably the name.
    """
    return bool(name) and (recorded_key == name or recorded_key.endswith("/" + name))


def _still_carries(written: frozenset[str], crate: frozenset[str]) -> bool:
    """Whether ``crate`` still holds enough of what a record was written from."""
    shared = len(written & crate)
    return shared >= 1 and shared * SHARED_DENOMINATOR >= len(written) * SHARED_NUMERATOR


def _grown_within(written: frozenset[str], crate: frozenset[str]) -> bool:
    """Whether the shared tracks are enough of the crate, not only of the record."""
    return len(written & crate) * GROWN_DENOMINATOR >= len(crate) * GROWN_NUMERATOR


def recognise(
    cfg: config.Config,
    playlist_key: str,
    *,
    name: str,
    track_ids: Iterable[str],
    live: Mapping[str, Iterable[str]],
) -> Recognition:
    """Which recorded remote playlist this crate writes to, as far as can be told.

    READ ONLY, and it decides nothing on its own. The verb shows the answer on
    its confirm gate and freezes it into the job, and ``reserve_playlist`` moves
    a record only when that frozen answer says so.

    ``live`` IS EVERY PLAYLIST PATH IN THE DOCUMENT BEING EXPORTED FROM, WITH ITS
    TRACKS. A recorded key still among them is a living crate with its own
    remote playlist, and it is never offered however many tracks it shares: two
    crates sharing most of their tracks is an ordinary library. THE EXCEPTION IS
    A DISPLACED RECORD, a live key whose crate no longer carries half of what the
    record was written from. That is a path reused for a different crate, which a
    yearly rotation does on purpose, and its record is free for the crate that
    was renamed away from it.

    TWO RULES, BY WHAT THE RECORD CARRIES. A record holding the crate contents
    of its last export qualifies when this crate still carries at least
    ``SHARED_NUMERATOR / SHARED_DENOMINATOR`` of them, and they are at least
    ``GROWN_NUMERATOR / GROWN_DENOMINATOR`` of this crate. A record written
    before this build holds none, so it qualifies on its display name alone and
    only while its own path is gone, which is the crate dragged into a folder. A
    record that holds tracks never qualifies by name: a new crate reusing an old
    name with different music is a different crate.

    THE WEAKNESS IS THE DOCUMENT'S AGE, stated rather than hidden. "No longer
    carries" is judged against the export handed in, so an export older than a
    crate reads that crate's record as orphaned. That is why this is an offer on
    a gate that also shows the export's date, and never a silent move.
    """
    playlists = _load(cfg)["playlists"]
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
            own_remote_id=str(own["remote_id"]),
            crate=len(wanted),
            mismatched=mismatched,
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
        adopts=key,
        remote_id=remote,
        shared=shared,
        recorded=recorded,
        crate=len(wanted),
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

    ``key`` IS WHERE THE RECORD LIVES NOW, which is the caller's own key except
    for a job confirmed before its record moved. Everything the caller goes on
    to record is recorded there. ``adopted_from`` is the key the record was
    moved from BY THIS CALL, decided under the lock, so two drivers cannot both
    report the one move. ``added`` rides along because the caller asks for it
    next, and a second parse of the whole file per item is what it would cost.
    """

    remote_id: str
    created: bool = False
    adopted_from: str = ""
    key: str = ""
    added: frozenset[str] = frozenset()
    #: Library row to remote track, for the same reason ``added`` rides along:
    #: the caller asks next whether a row is already recorded (R-836).
    rows: Mapping[str, str] = field(default_factory=dict)


def _moved_on(what: str, **detail: str) -> CratekitError:
    return refuse(
        "outbound-record-moved",
        f"{what}, so writing now would either create a remote playlist nobody "
        f"confirmed or write onto one that has since been given to another "
        f"playlist. Nothing was written for this item",
        steps=(
            "queue the export again, so its plan is built against what the "
            "ledger holds now",
        ),
        scope=Scope.RUN,
        origin=("outbound.ledger",),
        detail=dict(detail),
    )


def reserve_playlist(
    cfg: config.Config,
    playlist_key: str,
    create: Callable[[], str],
    *,
    adopts: str = "",
    expected: str = "",
    contents: Iterable[str] = (),
    written: str = "",
) -> Reserved:
    """The remote playlist for this crate, creating one only if none is recorded.

    ``adopts`` NAMES A RECORDED KEY THIS CRATE USED TO LIVE UNDER (R-229), which
    a person confirmed on the verb's gate. When this key has no record and that
    one does, the record MOVES here, under the lock, and no playlist is created.
    The order is this key first: under the per item shape the first item moves
    the record and every later item of the same job finds it already here. WHEN
    NEITHER HOLDS ONE IT REFUSES, because the person confirmed an update and a
    create is a different write. Two crates can be offered one orphaned record
    before either is driven, and the second to run is that case.

    ``expected`` IS THE REMOTE PLAYLIST THE JOB WAS CONFIRMED TO UPDATE, and it
    is the one stable identifier this file has. A job queued under a key whose
    record has since moved to the crate's new path finds the record BY THAT ID
    and goes on writing there, rather than reading its own key as never
    exported and creating. A record nothing holds any more refuses. A job frozen
    before this build carries none and is looked up by key alone, as it was.

    ``contents`` IS WHAT THE CRATE HOLDS NOW, every library row of it, and it
    REPLACES what was recorded. Replaced rather than grown, so a crate whose
    music rotates is still measured against what it last held, and written
    whole here rather than row by row, so an interrupted first export cannot
    leave one row standing as the crate. Not written through a forwarded key:
    that job describes the crate as it was.

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
    held = [str(item) for item in contents]
    lock = _locked(cfg)
    try:
        document = _load(cfg)
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
                key
                for key, record in playlists.items()
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
    finally:
        lock.__exit__(None, None, None)


def _note_written(
    document: dict[str, Any], playlist_key: str, expected: str, written: str
) -> bool:
    """Carry the export's date onto the record it writes to, kept at its latest.

    ``written`` is the ISO date of the collection export the write was made
    from (R-836). ``export prune`` refuses to read an export older than the
    record's, since every track added since would read as gone. The record is
    found by key, or by the confirmed remote playlist when it has moved. A
    date that is not newer than the recorded one changes nothing. True when
    the document changed, so the caller writes it.
    """
    if not written:
        return False
    playlists = document["playlists"]
    record = playlists.get(playlist_key)
    if expected and str((record or {}).get("remote_id") or "") != expected:
        # THE JOB WRITES WHERE IT WAS CONFIRMED TO, which is the record holding
        # ``expected``, so the date goes there too and not on this key's own.
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


def _later(candidate: str, recorded: str) -> bool:
    """Whether one ISO date is after another, an unreadable recorded one losing."""
    from datetime import datetime

    try:
        new = datetime.fromisoformat(candidate)
    except ValueError:
        return False
    try:
        return new > datetime.fromisoformat(recorded)
    except ValueError:
        return True


def _settled(
    cfg: config.Config,
    document: dict[str, Any],
    key: str,
    held: Iterable[str],
    *,
    created: bool = False,
    adopted_from: str = "",
    dirty: bool = False,
) -> Reserved:
    """Record the crate's contents if they moved, write once, and answer."""
    record = document["playlists"][key]
    contents = list(held)
    if contents and record.get("tracks") != contents:
        record["tracks"] = contents
        dirty = True
    if dirty or adopted_from:
        _write(cfg, document)
    return Reserved(
        remote_id=str(record["remote_id"]),
        created=created,
        adopted_from=adopted_from,
        key=key,
        added=frozenset(_listed(record, "added")),
        rows=_rows(record),
    )


def _move(document: dict[str, Any], recorded_key: str, playlist_key: str) -> None:
    """Move one record to a new key, in the document. The caller writes it.

    A MOVE AND NOT A COPY. Two keys naming one remote playlist would make the
    old path, if a crate is ever created there again, write onto a playlist that
    now belongs to this one. ``formerly`` keeps the path it came from, so the
    file still says how the record got here.
    """
    playlists = document["playlists"]
    record = playlists.pop(recorded_key)
    # WHAT WAS WRITTEN UNDER THIS KEY BEFORE A REMOTE ID WAS, which is the shape
    # ``record_playlist_track`` leaves when it runs first. Kept rather than
    # overwritten, since forgetting an added track is how it is added twice.
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


def record_playlist_track(
    cfg: config.Config, playlist_key: str, remote_id: str, *, identity: str = ""
) -> None:
    """Remember one track added to the remote playlist, and the row it came from.

    ``identity`` is the library row the track was matched from, kept under
    ``rows`` so ``export prune`` can tell a row that left the library playlist
    from a row whose match drifted to another remote track (R-836).
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
        if identity:
            record["rows"] = {**_rows(record), str(identity): str(remote_id)}
        document["playlists"][playlist_key] = record
        _write(cfg, document)
    finally:
        lock.__exit__(None, None, None)


def _rows(record: Mapping[str, Any]) -> dict[str, str]:
    """A record's library row to remote track map, or empty when it has none."""
    rows = record.get("rows")
    if not isinstance(rows, Mapping):
        return {}
    return {str(key): str(value) for key, value in rows.items()}


def record_playlist_row(
    cfg: config.Config, playlist_key: str, identity: str, remote_id: str
) -> None:
    """Remember which library row a track ALREADY WRITTEN here was matched from.

    Only for a track the record already holds as added: one a person put on
    the playlist is never claimed as this product's by being matched again.
    Writes nothing when the record already says so.
    """
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        record = document["playlists"].get(playlist_key)
        if not record or str(remote_id) not in _listed(record, "added"):
            return
        rows = _rows(record)
        if rows.get(str(identity)) == str(remote_id):
            return
        record["rows"] = {**rows, str(identity): str(remote_id)}
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


# ═══════════════════════════════════════════════════════════════════════════
# A label's folder of year playlists (R-835)
# ═══════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class LabelYear:
    """One year playlist this library built for a label, as recorded."""

    year: str
    remote_id: str
    #: The title it was created or adopted under, never the prefixed one a
    #: mark wrote since: the mark record keeps that.
    name: str
    added: frozenset[str] = frozenset()
    #: Tracks the provider was asked for and would not add. Not asked again,
    #: so a second build over an unchanged catalogue plans nothing.
    refused: frozenset[str] = frozenset()
    #: Tracks a prune took off (R-836). Not added again by a build either, or
    #: the build would put back what the prune just took away.
    pruned: frozenset[str] = frozenset()
    #: Whether this product created the playlist, True, or adopted one the
    #: account already held, False. None for a record written before this
    #: build said either. Only a created one may lose a track.
    created: bool | None = None


@dataclass(frozen=True, slots=True)
class LabelShape:
    """What this library has built on the account for one label."""

    label_id: str
    name: str = ""
    folder_id: str = ""
    years: Mapping[str, LabelYear] = field(default_factory=dict)


def _shape_of(label_id: str, record: Mapping[str, Any] | None) -> LabelShape:
    if not record:
        return LabelShape(label_id=label_id)
    return LabelShape(
        label_id=label_id,
        name=str(record.get("name") or ""),
        folder_id=str(record.get("folder_id") or ""),
        years={
            year: LabelYear(
                year=year,
                remote_id=str(entry.get("remote_id") or ""),
                name=str(entry.get("name") or ""),
                added=frozenset(_listed(entry, "added")),
                refused=frozenset(_listed(entry, "refused")),
                pruned=frozenset(_listed(entry, "pruned")),
                created=entry["created"] if isinstance(entry.get("created"), bool) else None,
            )
            for year, entry in (record.get("years") or {}).items()
            if entry.get("remote_id")
        },
    )


def label_shape(cfg: config.Config, label_id: str) -> LabelShape:
    """The folder and year playlists recorded for one label. Read only."""
    return _shape_of(label_id, _load(cfg)["labels"].get(label_id))


def label_playlist_ids(cfg: config.Config) -> frozenset[str]:
    """Every year playlist this library built for any label.

    For the playlist sweep, which must never read one as intake: a year
    playlist is a label's catalogue, and swept it would list every release of
    the label as missing from the library.
    """
    return frozenset(
        str(entry.get("remote_id"))
        for record in _load(cfg)["labels"].values()
        for entry in (record.get("years") or {}).values()
        if entry.get("remote_id")
    )


def _label_entry(document: dict[str, Any], label_id: str, name: str) -> dict[str, Any]:
    record = document["labels"].setdefault(
        label_id, {"name": name, "folder_id": "", "years": {}}
    )
    if name:
        record["name"] = name
    record.setdefault("years", {})
    return record


def reserve_label_folder(
    cfg: config.Config,
    label_id: str,
    name: str,
    create: Callable[[], str],
    *,
    adopt: str = "",
    stale: str = "",
) -> tuple[str, bool]:
    """The label's folder, creating one only if none is recorded. ``(id, created)``.

    THE LOCK IS TAKEN BEFORE THE CREATE, on ``reserve_playlist``'s argument: an
    unwritable ledger refuses before anything exists on the account, rather
    than after a folder nothing remembers.

    ``adopt`` is a folder already on the account under the label's name, which
    the plan found and a person was shown. It is recorded and nothing is made.
    ``stale`` is a recorded folder the plan read as gone from the account, so
    the record of it is replaced rather than reused.
    """
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        record = _label_entry(document, label_id, name)
        recorded = str(record.get("folder_id") or "")
        if recorded and recorded != stale:
            return recorded, False
        if adopt:
            record["folder_id"] = adopt
            _write(cfg, document)
            return adopt, False
        folder_id = create()
        record["folder_id"] = folder_id
        _write(cfg, document)
        return folder_id, True
    finally:
        lock.__exit__(None, None, None)


def reserve_label_year(
    cfg: config.Config,
    label_id: str,
    year: str,
    name: str,
    create: Callable[[], str],
    *,
    adopt: str = "",
) -> tuple[str, bool]:
    """One year's playlist, creating it only if none is recorded. ``(id, created)``.

    The same shape as :func:`reserve_label_folder` and for its reason. A year
    already recorded is never created again, so a build killed after the
    create and before the move resumes by moving the playlist it made.

    ``created`` IS WRITTEN WITH THE RECORD (R-836), true for a playlist this
    call made and false for one adopted from the account, because a prune may
    take a track off the first and never off the second.
    """
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        record = _label_entry(document, label_id, "")
        years = record["years"]
        recorded = str((years.get(year) or {}).get("remote_id") or "")
        if recorded:
            return recorded, False
        remote_id = adopt or create()
        years[year] = {
            "remote_id": remote_id,
            "name": name,
            "added": [],
            "refused": [],
            "pruned": [],
            "created": not adopt,
        }
        _write(cfg, document)
        return remote_id, not adopt
    finally:
        lock.__exit__(None, None, None)


def record_label_tracks(
    cfg: config.Config,
    label_id: str,
    year: str,
    *,
    added: Iterable[str] = (),
    refused: Iterable[str] = (),
) -> None:
    """Remember tracks written to one year playlist, and ones the provider refused."""
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        entry = (document["labels"].get(label_id) or {}).get("years", {}).get(year)
        if not entry:
            raise _unusable(
                config.state_path("outbound_writes", cfg),
                f"it holds no playlist for {label_id} {year}, whose tracks were just written",
            )
        for key, values in (("added", added), ("refused", refused)):
            held = _listed(entry, key)
            held += [str(one) for one in values if str(one) not in held]
            entry[key] = held
        _write(cfg, document)
    finally:
        lock.__exit__(None, None, None)


# ═══════════════════════════════════════════════════════════════════════════
# A set playlist, and the year folders it is archived in (R-837)
# ═══════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class SetPlaylist:
    """One playlist this library made on the account from a set's tracklist."""

    name: str
    remote_id: str
    #: The year it was made in, which names the folder it is archived in.
    year: str
    added: frozenset[str] = frozenset()
    #: Tracks the provider was asked for and would not add, not asked again.
    refused: frozenset[str] = frozenset()


def set_playlist(cfg: config.Config, name: str) -> SetPlaylist | None:
    """The set playlist recorded under this name, or ``None``. Read only."""
    record = _load(cfg)["sets"].get(name)
    if not record or not record.get("remote_id"):
        return None
    return SetPlaylist(
        name=name,
        remote_id=str(record["remote_id"]),
        year=str(record.get("year") or ""),
        added=frozenset(_listed(record, "added")),
        refused=frozenset(_listed(record, "refused")),
    )


def set_playlist_names(cfg: config.Config) -> tuple[str, ...]:
    """The name of every set playlist recorded with an identifier, sorted. Read only.

    For ``crate organize`` (U112), which looks each one up through
    :func:`set_playlist` so a set is read one way wherever it is read.
    """
    return tuple(
        sorted(
            str(name)
            for name, record in _load(cfg)["sets"].items()
            if record and record.get("remote_id")
        )
    )


def set_playlist_ids(cfg: config.Config) -> frozenset[str]:
    """Every set playlist this library made, for the playlist sweep to leave alone.

    A set playlist is the set's own record on the account and its tracks are
    fetched from the tracklist it was made from, so swept as intake it would be
    a second download of the same set.
    """
    return frozenset(
        str(record.get("remote_id"))
        for record in _load(cfg)["sets"].values()
        if record.get("remote_id")
    )


def set_folder(cfg: config.Config, year: str) -> str:
    """The root folder recorded for this year's set playlists, or ``""``."""
    return str(_load(cfg)["set_folders"].get(year) or "")


def reserve_set_playlist(
    cfg: config.Config, name: str, year: str, create: Callable[[], str]
) -> tuple[str, bool]:
    """The set's playlist, creating it only if none is recorded. ``(id, created)``.

    THE LOCK IS TAKEN BEFORE THE CREATE, on ``reserve_playlist``'s argument: an
    unwritable ledger refuses before anything exists on the account.
    """
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        recorded = str((document["sets"].get(name) or {}).get("remote_id") or "")
        if recorded:
            return recorded, False
        remote_id = create()
        document["sets"][name] = {
            "remote_id": remote_id,
            "year": year,
            "added": [],
            "refused": [],
        }
        _write(cfg, document)
        return remote_id, True
    finally:
        lock.__exit__(None, None, None)


def record_set_tracks(
    cfg: config.Config,
    name: str,
    *,
    added: Iterable[str] = (),
    refused: Iterable[str] = (),
) -> None:
    """Remember tracks written to one set playlist, and ones the provider refused."""
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        entry = document["sets"].get(name)
        if not entry:
            raise _unusable(
                config.state_path("outbound_writes", cfg),
                f"it holds no set playlist named {name!r}, whose tracks were just written",
            )
        for key, values in (("added", added), ("refused", refused)):
            held = _listed(entry, key)
            held += [str(one) for one in values if str(one) not in held]
            entry[key] = held
        _write(cfg, document)
    finally:
        lock.__exit__(None, None, None)


def reserve_set_folder(
    cfg: config.Config,
    year: str,
    create: Callable[[], str],
    *,
    adopt: str = "",
    stale: str = "",
) -> tuple[str, bool]:
    """The year's archive folder, creating one only if none is recorded.

    The shape of :func:`reserve_label_folder` and for its reason. ``adopt`` is
    one root folder already named as the year, which the plan found and a
    person was shown; ``stale`` is a recorded folder the plan read as gone.
    """
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        recorded = str(document["set_folders"].get(year) or "")
        if recorded and recorded != stale:
            return recorded, False
        if adopt:
            document["set_folders"][year] = adopt
            _write(cfg, document)
            return adopt, False
        folder_id = create()
        document["set_folders"][year] = folder_id
        _write(cfg, document)
        return folder_id, True
    finally:
        lock.__exit__(None, None, None)


# ═══════════════════════════════════════════════════════════════════════════
# What the product made, and what a prune took off it (R-836)
# ═══════════════════════════════════════════════════════════════════════════


def product_made(cfg: config.Config, playlist_id: str) -> bool:
    """Whether this product created the remote playlist, by the ledger alone.

    THE ONE QUESTION A REMOVAL ASKS FIRST, and the answer is no unless a record
    says yes. Three records can:

    * an exported playlist's, since ``reserve_playlist`` records only a
      playlist it created, and an adoption (R-229) moves a record the product
      already held rather than taking in one it did not make;
    * a set playlist's, since ``reserve_set_playlist`` only creates;
    * a label year's, only when it was written ``created``. A year adopted by
      its name under the folder was made by the source system or a person.

    ADOPTED ANYWHERE WINS. A playlist a label record holds as adopted is not
    made here, whatever another record says about the same identifier.
    """
    wanted = str(playlist_id or "")
    if not wanted:
        return False
    return _made_in(_load(cfg), wanted)


def product_made_among(cfg: config.Config, playlist_ids) -> frozenset[str]:
    """Those of ``playlist_ids`` this product created, the ledger read once.

    :func:`product_made`'s rule over each, for ``crate organize`` (U112), which
    asks it of every playlist on the account and would otherwise read and parse
    the ledger once per playlist.
    """
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
    if made:
        return True
    for record in (*document["playlists"].values(), *document["sets"].values()):
        if str(record.get("remote_id") or "") == wanted:
            return True
    return False


@dataclass(frozen=True, slots=True)
class ExportedPlaylist:
    """One exported playlist's record, read once for a prune plan."""

    key: str
    remote_id: str
    added: frozenset[str] = frozenset()
    pruned: frozenset[str] = frozenset()
    #: The ISO date of the newest collection export this playlist was written
    #: from, or empty for a record written before this build kept one.
    written: str = ""
    #: Library row to the remote track it was matched to, for the tracks this
    #: build wrote or matched again. A track written before has no row here.
    rows: Mapping[str, str] = field(default_factory=dict)


def exported_playlist(cfg: config.Config, playlist_key: str) -> ExportedPlaylist | None:
    """The record an export wrote under this key, or ``None``. Read only."""
    record = _load(cfg)["playlists"].get(playlist_key) or {}
    remote = str(record.get("remote_id") or "")
    if not remote:
        return None
    return ExportedPlaylist(
        key=playlist_key,
        remote_id=remote,
        added=frozenset(_listed(record, "added")),
        pruned=frozenset(_listed(record, "pruned")),
        written=str(record.get("written") or ""),
        rows=_rows(record),
    )


def older_than(given: str, recorded: str) -> bool:
    """Whether an export dated ``given`` is older than the recorded date.

    An export whose date could not be read, ``given`` empty, is older than any
    recorded date, since it cannot be shown to be newer. No recorded date is
    nothing to be older than.
    """
    if not recorded:
        return False
    return not given or _later(recorded, given)


def _moved_to_pruned(entry: dict[str, Any], taken: Iterable[str]) -> None:
    """Move each taken identifier off ``added`` and onto ``pruned``, in place."""
    gone = [str(one) for one in taken]
    entry["added"] = [one for one in _listed(entry, "added") if one not in gone]
    held = _listed(entry, "pruned")
    held += [one for one in gone if one not in held]
    entry["pruned"] = held


def record_label_pruned(
    cfg: config.Config, label_id: str, year: str, taken: Iterable[str]
) -> None:
    """Remember tracks a prune took off one year playlist, as they land."""
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        entry = (document["labels"].get(label_id) or {}).get("years", {}).get(year)
        if not entry:
            raise _unusable(
                config.state_path("outbound_writes", cfg),
                f"it holds no playlist for {label_id} {year}, whose tracks were just taken off",
            )
        _moved_to_pruned(entry, taken)
        _write(cfg, document)
    finally:
        lock.__exit__(None, None, None)


def record_playlist_pruned(cfg: config.Config, playlist_key: str, taken: Iterable[str]) -> None:
    """Remember tracks a prune took off one exported playlist, as they land.

    Off ``added``, so a track put back in the library playlist is exported
    again by the next ``export playlist`` rather than skipped as written.
    """
    lock = _locked(cfg)
    try:
        document = _load(cfg)
        entry = document["playlists"].get(playlist_key)
        if not entry:
            raise _unusable(
                config.state_path("outbound_writes", cfg),
                f"it holds no exported playlist under {playlist_key!r}, whose "
                f"tracks were just taken off",
            )
        _moved_to_pruned(entry, taken)
        gone = {str(one) for one in taken}
        if _rows(entry):
            entry["rows"] = {key: value for key, value in _rows(entry).items() if value not in gone}
        _write(cfg, document)
    finally:
        lock.__exit__(None, None, None)
