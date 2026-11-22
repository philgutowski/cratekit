"""The ledger's settlement: what was written to a reserved playlist, as it lands.

Each write is recorded once the provider answered, under the lock, so a refusal
part way leaves every landed write recorded. ``_write`` is looked up on
:mod:`.ledger` at call time, and ``_open`` reads its globals there, so a test
that patches them reaches here.
"""

from __future__ import annotations

from collections.abc import Iterable
from types import MappingProxyType
from typing import Any, Mapping

from cratekit.core import config
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound.ledger import _listed, _open, _placements, _refused, _rows


def _extend(entry: dict[str, Any], **values: Iterable[str]) -> None:
    """Add each value not yet held to the entry's list of that name, in order."""
    for key, more in values.items():
        held = _listed(entry, key)
        held += [str(one) for one in more if str(one) not in held]
        entry[key] = held


def _found(cfg: config.Config, entry: Any, what: str, done: str = "written") -> dict[str, Any]:
    """``entry``, or the refusal for a record the write that just landed should be on."""
    if not entry:
        raise _refused(cfg, f"it holds no {what}, whose tracks were just {done}")
    return entry


def _playlist(document: dict[str, Any], playlist_key: str) -> dict[str, Any]:
    """An exported playlist's record, a stub with no remote id when there is none."""
    return document["playlists"].setdefault(playlist_key, {"remote_id": "", "added": []})


def record_playlist_track(
    cfg: config.Config, playlist_key: str, remote_id: str, *, identity: str = ""
) -> None:
    """Remember one track added to the remote playlist, and the row it came from.

    ``identity`` lets ``export prune`` tell a row that left from one whose match
    drifted (R-836).
    """
    with _open(cfg) as document:
        record = _playlist(document, playlist_key)
        added = _listed(record, "added")
        if remote_id not in added:
            added.append(remote_id)
        record["added"] = added
        if identity:
            record["rows"] = {**_rows(record), str(identity): str(remote_id)}
        ledger._write(cfg, document)


def record_playlist_tracks(
    cfg: config.Config, playlist_key: str, *, landed: Mapping[str, str],
    rows: Mapping[str, str] = MappingProxyType({}),
) -> None:
    """After one batch's answer, ONE lock and ONE write for the batch (U270).

    ``landed`` is row to remote track for each row the answer held, recorded as
    added; ``rows`` names rows for tracks ALREADY added, on
    :func:`record_playlist_row`'s rule. NOTHING IS RECORDED BEFORE THE ANSWER
    (R-1543): a read cannot tell a landed track from one a person added.
    """
    with _open(cfg) as document:
        record = _playlist(document, playlist_key)
        added = _listed(record, "added")
        known = _rows(record)
        before = (list(added), dict(known))
        for row, track in landed.items():
            if str(track) not in added:
                added.append(str(track))
            known[str(row)] = str(track)
        for row, track in rows.items():
            if str(track) in added:
                known[str(row)] = str(track)
        if (added, known) != before:
            record["added"] = added
            if known:
                record["rows"] = known
            ledger._write(cfg, document)


def record_playlist_row(
    cfg: config.Config, playlist_key: str, identity: str, remote_id: str
) -> None:
    """Remember which library row a track ALREADY WRITTEN here was matched from.

    Only a track recorded as added, so one a person added is never claimed.
    """
    with _open(cfg) as document:
        record = document["playlists"].get(playlist_key)
        if not record or str(remote_id) not in _listed(record, "added"):
            return
        rows = _rows(record)
        if rows.get(str(identity)) == str(remote_id):
            return
        record["rows"] = {**rows, str(identity): str(remote_id)}
        ledger._write(cfg, document)


def record_heart(cfg: config.Config, remote_id: str) -> None:
    """Remember one heart so a re-run does not add it again."""
    with _open(cfg) as document:
        document["hearts"][remote_id] = "hearted"
        ledger._write(cfg, document)


def _year(document: dict[str, Any], label_id: str, year: str) -> dict[str, Any] | None:
    return (document["labels"].get(label_id) or {}).get("years", {}).get(year)


def record_label_tracks(
    cfg: config.Config, label_id: str, year: str, *, added: Iterable[str] = (),
    refused: Iterable[str] = (),
) -> None:
    """Remember tracks written to one year playlist, and ones the provider refused."""
    with _open(cfg) as document:
        entry = _found(cfg, _year(document, label_id, year), f"playlist for {label_id} {year}")
        _extend(entry, added=added, refused=refused)
        ledger._write(cfg, document)


def record_set_tracks(
    cfg: config.Config, name: str, *, added: Iterable[str] = (), refused: Iterable[str] = ()
) -> None:
    """Remember tracks written to one set playlist, and ones the provider refused."""
    with _open(cfg) as document:
        entry = _found(cfg, document["sets"].get(name), f"set playlist named {name!r}")
        _extend(entry, added=added, refused=refused)
        ledger._write(cfg, document)


def forget_label_dated(cfg: config.Config, label_id: str, remote_id: str) -> None:
    """Drop a dated playlist's entry once ``label heard`` removed the playlist."""
    with _open(cfg) as document:
        record = document["labels"].get(label_id)
        held = record.get("dated") if record is not None else None
        if not held:
            return
        kept = {name: pid for name, pid in held.items() if pid != str(remote_id)}
        if kept == held:
            return
        record["dated"] = kept
        ledger._write(cfg, document)


# ── What a prune took off (R-836) ─────────────────────────────────────────────


def _moved_to_pruned(entry: dict[str, Any], taken: Iterable[str]) -> None:
    """Move each taken identifier off ``added`` and onto ``pruned``, in place."""
    gone = [str(one) for one in taken]
    entry["added"] = [one for one in _listed(entry, "added") if one not in gone]
    _extend(entry, pruned=gone)


def record_label_pruned(
    cfg: config.Config, label_id: str, year: str, taken: Iterable[str]
) -> None:
    """Remember tracks a prune took off one year playlist, as they land."""
    with _open(cfg) as document:
        entry = _year(document, label_id, year)
        entry = _found(cfg, entry, f"playlist for {label_id} {year}", "taken off")
        _moved_to_pruned(entry, taken)
        ledger._write(cfg, document)


def record_playlist_pruned(cfg: config.Config, playlist_key: str, taken: Iterable[str]) -> None:
    """Remember tracks a prune took off one exported playlist, so one put back is exported again."""
    with _open(cfg) as document:
        entry = document["playlists"].get(playlist_key)
        entry = _found(cfg, entry, f"exported playlist under {playlist_key!r}", "taken off")
        _moved_to_pruned(entry, taken)
        gone = {str(one) for one in taken}
        if _rows(entry):
            entry["rows"] = {key: value for key, value in _rows(entry).items() if value not in gone}
        ledger._write(cfg, document)


# ── The account mirrors (U147, U201, U236, R-1031) ────────────────────────────


def _mirrored(document: dict[str, Any], folder: str) -> dict[str, Any]:
    """The mirrored playlists recorded in one folder, or an empty map."""
    return (document["mirrors"].get(folder) or {}).get("playlists") or {}


def record_mirror_links(cfg: config.Config, links: Mapping[str, tuple[str, str]]) -> None:
    """Remember rows matched to account tracks, so a refresh does not match them again."""
    if not links:
        return
    with _open(cfg) as document:
        for content_id, (remote, isrc) in links.items():
            if remote:
                linked = document["mirror_links"]
                linked[str(content_id)] = {"remote": str(remote), "isrc": str(isrc)}
                document["mirror_misses"].pop(str(content_id), None)
        ledger._write(cfg, document)


def record_mirror_misses(
    cfg: config.Config, misses: Mapping[str, tuple[str, Iterable[str]]]
) -> None:
    """Remember rows the mirror could not match, so a refresh does not ask again (R-1031).

    A linked row is never recorded as a miss, so a link is never overwritten.
    """
    if not misses:
        return
    with _open(cfg) as document:
        for content_id, (reason, under) in misses.items():
            if str(content_id) in document["mirror_links"]:
                continue
            document["mirror_misses"][str(content_id)] = {
                "reason": str(reason), "under": [str(one) for one in under]
            }
        ledger._write(cfg, document)


def forget_mirror_playlist(cfg: config.Config, folder: str, name: str, remote_id: str) -> None:
    """Drop one mirrored playlist's record once the account no longer holds it (U150).

    Only THAT playlist's, by title and identifier both. One already gone is no error.
    """
    with _open(cfg) as document:
        playlists = _mirrored(document, folder)
        entry = playlists.get(name)
        if not entry or str(entry.get("remote_id") or "") != str(remote_id):
            return
        del playlists[name]
        ledger._write(cfg, document)


def record_mirror_refused(
    cfg: config.Config, folder: str, name: str, refused: Iterable[str]
) -> None:
    """Remember tracks the provider would not add to one mirrored playlist."""
    wanted = [str(one) for one in refused]
    if not wanted:
        return
    with _open(cfg) as document:
        entry = _mirrored(document, folder).get(name)
        entry = _found(cfg, entry, f"mirrored playlist {name!r} in {folder!r}")
        _extend(entry, refused=wanted)
        ledger._write(cfg, document)


def record_mirror_agreed(
    cfg: config.Config, folder: str, agreed: Mapping[str, tuple[str, Iterable[str], Iterable[str]]]
) -> None:
    """Record each mirrored playlist's snapshot, title to ``(remote id, after, held)`` (U201).

    ``after`` is what it holds once mirrored; tracks ``held`` covers keep the
    word recorded NOW, so one settled since the plan is never written back over.
    Only on THAT playlist's record, by title and identifier both.
    """
    from cratekit.modules.outbound import mirror_edits

    if not agreed:
        return
    with _open(cfg) as document:
        playlists = _mirrored(document, folder)
        wrote = False
        for name, (remote_id, after, held) in agreed.items():
            entry = playlists.get(name)
            if not entry or str(entry.get("remote_id") or "") != str(remote_id):
                continue
            base = _listed(entry, "agreed") if isinstance(entry.get("agreed"), list) else None
            tracks = mirror_edits.agreed_after(base, after, held)
            entry["agreed"] = sorted({str(one) for one in tracks if str(one)})
            # And its placements (U236): one whose track the account now holds
            # here, with no hold on it, is the snapshot's word now, and is dropped.
            record = document["mirrors"][folder]
            _place(record, name, mirror_edits.placed_after(
                _placements(record.get("placed")).get(name, {}), after, held
            ))
            wrote = True
        if wrote:
            ledger._write(cfg, document)


def _place(record: dict[str, Any], title: str, tracks: Mapping[str, str]) -> None:
    """Set one title's placements on a mirrored folder's record, none dropping the title."""
    placed = _placements(record.get("placed"))
    kept = _placements({title: dict(tracks)}).get(str(title), {})
    if kept:
        placed[str(title)] = kept
    else:
        placed.pop(str(title), None)
    if placed:
        record["placed"] = placed
    else:
        record.pop("placed", None)


def settle_mirror_tracks(
    cfg: config.Config, settled: Iterable[tuple[str, str, str, bool]],
    placed: Iterable[tuple[str, str, str, str]] = (),
) -> None:
    """Agree tracks the library took an account edit for, ``(folder, title, track, on)`` (U201).

    A playlist never agreed stays so. ``placed`` is each ``(folder, title,
    track, time)`` placed in rekordbox that the account does not hold (U236); a
    settled track loses its placement before the new ones are added.
    """
    wanted = list(settled)
    placements = list(placed)
    if not wanted and not placements:
        return
    with _open(cfg) as document:
        wrote = False
        for folder, name, track, on in wanted:
            record = document["mirrors"].get(folder)
            if record is not None:
                before = _placements(record.get("placed")).get(str(name), {})
                if str(track) in before:
                    kept = {one: at for one, at in before.items() if one != str(track)}
                    _place(record, name, kept)
                    wrote = True
            entry = ((record or {}).get("playlists") or {}).get(name)
            if not entry or not isinstance(entry.get("agreed"), list):
                continue
            held = set(_listed(entry, "agreed"))
            held = held | {str(track)} if on else held - {str(track)}
            entry["agreed"] = sorted(held)
            wrote = True
        for folder, name, track, at in placements:
            record = document["mirrors"].get(folder)
            if record is None or not str(track) or not str(at):
                continue
            _place(
                record, name,
                {**_placements(record.get("placed")).get(str(name), {}), str(track): str(at)},
            )
            wrote = True
        if wrote:
            ledger._write(cfg, document)
