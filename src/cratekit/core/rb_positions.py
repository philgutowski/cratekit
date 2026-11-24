"""Every playlist this product writes stays numbered 1 to N (U958).

Part of :mod:`cratekit.core.rb_writer`, which re-exports every name here; read them there. A
name of the writer outside this file, and every seam a test patches, is read through
``rb_writer`` at call time so a patch on the writer bites here too (U300).

rekordbox shows a playlist's live rows at positions 1 to N whatever their stored
``TrackNo``, and its Remove from Playlist takes out the row whose ``TrackNo``
equals the selected row's shown position (sitting 107, A218). So a playlist whose
live rows are not numbered 1 to N loses the wrong track to a removal by hand.

**THE RULE, ONE PLACE**, :func:`contiguous_positions`: per playlist, the live rows
in the order rekordbox shows them (live ``TrackNo``, ties by row id, as every
reader here orders them) numbered 1 to N, and every row marked removed that holds
a number moved to 0, below every place a live row can hold. Only a row whose
number changes is written.

**WHERE IT RUNS**: :func:`remove_memberships` records each playlist it marked a
row in on the write handle's session (:func:`record_touched`), and
:func:`commit_guarded` closes their gaps just before the binding's commit
(:func:`close_gaps`), from SQL, each moved live row stamped as U955 stamps a
renumbered row and each marked row moving its number alone, proven from SQL
before the commit. So every verb that removes a membership inherits it,
and the repair verb (``write.numbers``) is the same rule over playlists it
records itself, with nothing removed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from cratekit.core import rb_removal
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.rb_call_time import writer as _writer
from cratekit.core.rb_removal import (
    TIME_STAMP_COLUMN,
    USN_STAMP_COLUMN,
    RenumberingStamp,
    stamp_time,
)
from cratekit.core.rb_tables import (
    LOCAL_UPDATE_COUNT,
    MEMBERSHIP_TABLE,
    PLAYLIST_REFERENCE_COLUMN,
    TRACK_NUMBER_COLUMN,
)

#: Where a write handle's session holds the playlists whose gaps its commit closes.
TOUCHED_KEY = "cratekit.u958.touched"

#: Set once the session's commit and rollback clear :data:`TOUCHED_KEY`.
_LISTENING_KEY = "cratekit.u958.listening"

#: Where a marked row is put, below every place a live row holds.
MARKED_PLACE = 0

#: How many identifiers one ``IN`` clause binds, well under SQLite's limit.
_CHUNK = 400


@dataclass(frozen=True, slots=True)
class Numbering:
    """One playlist's live numbers, as the doctor and the repair show them."""

    playlist: str
    #: Live rows.
    rows: int
    #: The lowest and highest live ``TrackNo``, None for an empty playlist.
    lowest: int | None
    highest: int | None
    #: Marked rows holding a number other than :data:`MARKED_PLACE`.
    marked_placed: int
    #: Whether the live rows read 1 to N, each once.
    contiguous: bool


def _grouped(
    rows: Iterable[tuple[str, str, int | None, bool | None]],
) -> dict[str, list[tuple[str, int | None, bool | None]]]:
    by: dict[str, list[tuple[str, int | None, bool | None]]] = {}
    for key, playlist, number, live in rows:
        by.setdefault(str(playlist), []).append(
            (str(key), None if number is None else int(number), live)
        )
    return by


def unplaceable(rows: Iterable[tuple[str, str, int | None, bool | None]]) -> dict[str, list[str]]:
    """The playlists the rule cannot number, each with the rows that say why. PURE.

    A row whose marker cannot be read (``live`` None), or a live row with no
    ``TrackNo``, leaves its playlist's order unsayable, so the playlist is
    refused whole, as :func:`removal_renumbering` refuses.
    """
    found: dict[str, list[str]] = {}
    for playlist, held in _grouped(rows).items():
        bad = sorted(key for key, number, live in held if live is None or (live and number is None))
        if bad:
            found[playlist] = bad
    return found


def contiguous_positions(
    rows: Iterable[tuple[str, str, int | None, bool | None]],
) -> dict[str, tuple[str, int, int]]:
    """Which membership rows the rule moves, and to what. PURE (U958).

    ``rows`` holds ``(membership id, playlist id, TrackNo, live)``; returns
    ``{membership id: (playlist id, TrackNo now, TrackNo after)}`` for rows that
    move. Per playlist the live rows, ordered by ``TrackNo`` then row id, take 1
    to N; a marked row holding a number other than 0 takes 0. A playlist
    :func:`unplaceable` names is left whole: the caller refuses it.
    """
    grouped = _grouped(rows)
    held_back = set(unplaceable(
        (key, playlist, number, live)
        for playlist, held in grouped.items()
        for key, number, live in held
    ))
    moved: dict[str, tuple[str, int, int]] = {}
    for playlist, held in sorted(grouped.items()):
        if playlist in held_back:
            continue
        live = sorted(
            ((number, key) for key, number, alive in held if alive),
            key=lambda one: (int(one[0]), one[1]),
        )
        for place, (number, key) in enumerate(live, start=1):
            if int(number) != place:
                moved[key] = (playlist, int(number), place)
        for key, number, alive in held:
            if not alive and number is not None and number != MARKED_PLACE:
                moved[key] = (playlist, number, MARKED_PLACE)
    return moved


def numbering(rows: Iterable[tuple[str, str, int | None, bool | None]]) -> dict[str, Numbering]:
    """Each playlist's live numbers, read off ``rows``. PURE.

    A playlist with a row :func:`unplaceable` names reads not contiguous.
    """
    grouped = _grouped(rows)
    held_back = set(unplaceable(
        (key, playlist, number, live)
        for playlist, held in grouped.items()
        for key, number, live in held
    ))
    found: dict[str, Numbering] = {}
    for playlist, held in grouped.items():
        numbers = sorted(int(number) for _key, number, live in held if live and number is not None)
        found[playlist] = Numbering(
            playlist=playlist,
            rows=sum(1 for _key, _number, live in held if live),
            lowest=numbers[0] if numbers else None,
            highest=numbers[-1] if numbers else None,
            marked_placed=sum(
                1
                for _key, number, live in held
                if live is False and number is not None and number != MARKED_PLACE
            ),
            contiguous=playlist not in held_back and numbers == list(range(1, len(numbers) + 1)),
        )
    return found


def _live(marker: Any) -> bool | None:
    """A membership marker read as live (True), marked (False) or unreadable (None)."""
    if marker is None:
        return None
    return not bool(marker)


def membership_rows(
    db: Any, playlist_ids: Iterable[str] | None = None
) -> list[tuple[str, str, int | None, bool | None]]:
    """``(membership id, playlist id, TrackNo, live)`` from SQL, for ``playlist_ids`` or every playlist.

    Reads nothing else and writes nothing. No object mapper in between, so a
    flushed write is seen as SQL holds it.
    """
    from sqlalchemy import bindparam, text

    marker = _writer().SOFT_DELETE_COLUMN
    select = (
        f'SELECT "ID", "{PLAYLIST_REFERENCE_COLUMN}", "{TRACK_NUMBER_COLUMN}", "{marker}" '
        f'FROM "{MEMBERSHIP_TABLE}"'
    )
    session = db.session
    if playlist_ids is None:
        found = session.execute(text(select)).fetchall()
    else:
        wanted = sorted({str(one) for one in playlist_ids})
        found = []
        statement = text(f'{select} WHERE "{PLAYLIST_REFERENCE_COLUMN}" IN :ids').bindparams(
            bindparam("ids", expanding=True)
        )
        for at in range(0, len(wanted), _CHUNK):
            found.extend(session.execute(statement, {"ids": wanted[at : at + _CHUNK]}).fetchall())
    return [
        (str(row[0]), str(row[1]), None if row[2] is None else int(row[2]), _live(row[3]))
        for row in found
    ]


def record_touched(db: Any, playlist_id: Any) -> None:
    """Record that this handle's next commit closes ``playlist_id``'s gaps (U958).

    Held on the write handle's session and CLEARED BY ITS COMMIT AND BY ANY
    ROLLBACK, so a refused or abandoned write leaves nothing for a later commit
    on the handle to renumber.
    """
    session = getattr(db, "session", None)
    info = getattr(session, "info", None)
    if not isinstance(info, dict):
        raise _writer()._unavailable(
            "whitelist-violation",
            "the write handle carries no session to record the playlist a removal "
            "touched on, so its numbers could not be closed up; nothing was written",
            detail={"playlist_id": str(playlist_id)},
        )
    if not info.get(_LISTENING_KEY):
        from sqlalchemy import event

        event.listen(session, "after_commit", _forget)
        event.listen(session, "after_rollback", _forget)
        info[_LISTENING_KEY] = True
    info.setdefault(TOUCHED_KEY, set()).add(str(playlist_id))


def _forget(session: Any) -> None:
    session.info.pop(TOUCHED_KEY, None)


def touched(db: Any) -> frozenset[str]:
    """The playlists this handle's next commit closes the gaps of."""
    info = getattr(getattr(db, "session", None), "info", None)
    held = info.get(TOUCHED_KEY) if isinstance(info, dict) else None
    return frozenset(held or ())


@dataclass(frozen=True)
class GapReading:
    """Every membership row of some playlists, whole, read from SQL, by membership id."""

    columns: tuple[str, ...]
    rows: Mapping[str, tuple]
    counter: int | None


def gap_reading(db: Any, playlist_ids: Iterable[str]) -> GapReading:
    """Every column of every membership row of ``playlist_ids``, and ``localUpdateCount``, from SQL."""
    from sqlalchemy import bindparam, text

    wanted = sorted({str(one) for one in playlist_ids})
    session = db.session
    statement = text(
        f'SELECT * FROM "{MEMBERSHIP_TABLE}" WHERE "{PLAYLIST_REFERENCE_COLUMN}" IN :ids'
    ).bindparams(bindparam("ids", expanding=True))
    columns: tuple[str, ...] = ()
    rows: dict[str, tuple] = {}
    for at in range(0, max(len(wanted), 1), _CHUNK):
        result = session.execute(statement, {"ids": wanted[at : at + _CHUNK]})
        columns = tuple(result.keys())
        key = columns.index("ID")
        for row in result:
            rows[str(row[key])] = tuple(row)
    counter = session.execute(
        text("SELECT int_1 FROM agentRegistry WHERE registry_id = :id"),
        {"id": LOCAL_UPDATE_COUNT},
    ).scalar()
    return GapReading(columns, rows, None if counter is None else int(counter))


def gap_violations(
    before: GapReading,
    after: GapReading,
    *,
    planned: Mapping[str, tuple[str, int, int]],
    stamp: RenumberingStamp | None,
) -> list[str]:
    """Every difference between two readings the planned closing up does not explain. PURE.

    No row is added or disappears; a planned live row moved ``TrackNo`` to its
    planned number and ``rb_local_usn`` and ``updated_at`` to ``stamp``'s and
    nothing else; a planned marked row moved ``TrackNo`` ALONE, since its
    ``updated_at`` is the moment it was removed, which ``sync pair`` reads; every
    other row is unchanged; and the live rows of every playlist read 1 to N with
    no marked row on a live place. ``stamp`` is None when no live row moves.
    """
    marker = _writer().SOFT_DELETE_COLUMN
    violations: list[str] = []
    for key in sorted(set(before.rows) ^ set(after.rows)):
        violations.append(f"the {MEMBERSHIP_TABLE} row {key!r} was added or disappeared")
    if not after.columns:
        return violations
    cols = after.columns
    number_at = cols.index(TRACK_NUMBER_COLUMN)
    playlist_at = cols.index(PLAYLIST_REFERENCE_COLUMN)
    marker_at = cols.index(marker)
    stamps = {
        cols.index(name): value
        for name, value in (
            (USN_STAMP_COLUMN, None if stamp is None else stamp.counter),
            (TIME_STAMP_COLUMN, None if stamp is None else stamp.at),
        )
        if name in cols
    }
    for key in sorted(set(before.rows) & set(after.rows)):
        old, new = before.rows[key], after.rows[key]
        if key not in planned:
            if old != new:
                violations.append(
                    f"the {MEMBERSHIP_TABLE} row {key!r} changed, and the closing up "
                    f"planned no move of it"
                )
            continue
        _playlist, was, wanted = planned[key]
        if new[number_at] != wanted:
            violations.append(
                f"the {MEMBERSHIP_TABLE} row {key!r} was to move from {was} to "
                f"{wanted} and holds {new[number_at]}"
            )
        if _live(old[marker_at]) is False:
            # A marked row: its number alone, its removal's own stamps kept.
            if any(o != n for at, (o, n) in enumerate(zip(old, new)) if at != number_at):
                violations.append(
                    f"the marked {MEMBERSHIP_TABLE} row {key!r} changed in a column "
                    f"other than {TRACK_NUMBER_COLUMN}, and a marked row moves that alone"
                )
            continue
        for at, value in stamps.items():
            if new[at] != value:
                violations.append(
                    f"the {MEMBERSHIP_TABLE} row {key!r} was to be stamped "
                    f"{cols[at]} {value!r} and holds {new[at]!r}"
                )
        moving = {number_at, *stamps}
        if any(o != n for at, (o, n) in enumerate(zip(old, new)) if at not in moving):
            violations.append(
                f"the {MEMBERSHIP_TABLE} row {key!r} changed in a column other than "
                f"{TRACK_NUMBER_COLUMN}, {USN_STAMP_COLUMN} and "
                f"{TIME_STAMP_COLUMN}"
            )
    for playlist, read in sorted(
        numbering(
            (key, row[playlist_at], row[number_at], _live(row[marker_at]))
            for key, row in after.rows.items()
        ).items()
    ):
        if not read.contiguous or read.marked_placed:
            violations.append(
                f"the playlist {playlist!r} does not read 1 to N after the closing up: "
                f"{read.rows} live row(s) from {read.lowest} to {read.highest}, "
                f"{read.marked_placed} marked row(s) on a place"
            )
    return violations


def _stamp(db: Any) -> RenumberingStamp:
    """The stamp for this commit's moved rows, the count the commit leaves (U955).

    With no change buffered the binding's commit would leave the count where it
    is, so the closing up counts as one change: the count is moved on by one in
    SQL and the held registry rows are expired for the binding to read it again.
    """
    from sqlalchemy import text

    rb_writer = _writer()
    reaching = rb_writer.counter_at_commit(db)
    current = int(db.get_local_usn())
    if reaching == current:
        reaching = current + 1
        db.session.execute(
            text("UPDATE agentRegistry SET int_1 = :n WHERE registry_id = :id"),
            {"n": reaching, "id": LOCAL_UPDATE_COUNT},
        )
        for held in list(db.session.identity_map.values()):
            if rb_writer._table_of(held) == "agentRegistry":
                db.session.expire(held)
    return RenumberingStamp(reaching, stamp_time(rb_removal._now()))


def _park_marked(db: Any, moves: Mapping[str, tuple[str, int, int]]) -> None:
    """Put each marked row at its planned place, ``TrackNo`` alone (U958 review B1).

    Its ``updated_at`` is the moment it was removed, which ``sync pair`` reads
    against the account's own changes, so neither stamp moves. A row that is
    no longer marked, or no longer at its planned number, refuses and rolls back.
    """
    from sqlalchemy import text

    statement = text(
        f'UPDATE "{MEMBERSHIP_TABLE}" SET "{TRACK_NUMBER_COLUMN}" = :after '
        f'WHERE "ID" = :key AND "{TRACK_NUMBER_COLUMN}" = :before '
        f'AND "{_writer().SOFT_DELETE_COLUMN}" = 1'
    )
    session = db.session
    for key, (_playlist, before, after) in sorted(moves.items()):
        if session.execute(statement, {"after": after, "key": key, "before": before}).rowcount != 1:
            db.rollback()
            raise _writer()._unavailable(
                "whitelist-violation",
                f"the marked playlist membership {key!r} no longer holds the place {before} "
                f"the closing up planned to move it from, so nothing was committed",
                detail={"membership_id": key, "planned": before},
            )
    for held in list(session.identity_map.values()):
        if _writer()._table_of(held) == MEMBERSHIP_TABLE and str(getattr(held, "ID", "")) in moves:
            session.expire(held)


def close_gaps(db: Any) -> dict[str, tuple[str, int, int]]:
    """Number every recorded playlist's live rows 1 to N, inside the open transaction (U958).

    Called by :func:`commit_guarded` after the whitelist and before the
    binding's commit. Flushes, reads the recorded playlists from SQL, plans by
    :func:`contiguous_positions`, writes the live rows through
    :func:`renumber_memberships` with the stamp and the marked rows' ``TrackNo``
    alone (:func:`_park_marked`), and proves it from SQL by
    :func:`gap_violations`. A row this same commit also wrote through the binding
    (a row added or marked here) is stamped again by the binding's commit with
    its own count, as every row the binding writes is. REFUSED, ROLLED BACK: a
    recorded playlist :func:`unplaceable` names, or a write the plan does not
    explain. Returns what moved.
    """
    rb_writer = _writer()
    info = getattr(getattr(db, "session", None), "info", None)
    recorded = info.pop(TOUCHED_KEY, None) if isinstance(info, dict) else None
    if not recorded:
        return {}
    db.session.flush()
    rows = membership_rows(db, recorded)
    held = unplaceable(rows)
    if held:
        db.rollback()
        raise refuse(
            "soft-delete-marker-unreadable",
            f"{len(held)} playlist(s) this write touched hold a membership row whose "
            f"removal marker or place cannot be read, so the order its tracks show in "
            f"cannot be said and their numbers were not closed up; nothing was written",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("rb_writer",),
            detail={"playlists": {key: value[:20] for key, value in sorted(held.items())}},
        )
    planned = contiguous_positions(rows)
    if not planned:
        return {}
    marked = {key for key, _playlist, _number, live in rows if live is False}
    live_moves = {key: move for key, move in planned.items() if key not in marked}
    before = gap_reading(db, recorded)
    stamp = _stamp(db) if live_moves else None
    if stamp is not None:
        rb_writer.renumber_memberships(db, live_moves, stamp=stamp)
    _park_marked(db, {key: move for key, move in planned.items() if key in marked})
    violations = gap_violations(before, gap_reading(db, recorded), planned=planned, stamp=stamp)
    if violations:
        db.rollback()
        raise rb_writer._unavailable(
            "whitelist-violation",
            "closing up the numbers of the playlists this write touched reached rows it "
            "did not plan, or did not make a move it planned, read from SQL before the "
            "commit:\n  - " + "\n  - ".join(violations[:20]),
            detail={"violations": violations},
        )
    return planned
