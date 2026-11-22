"""``export.set`` and ``export.archive``: a set as a playlist on the account (R-837).

``export set TRACKLIST`` makes a set a private account playlist, rows matched
by :mod:`cratekit.export.set_match` and the rest LEFT OUT AND NAMED (R-850); a
second run reuses the playlist recorded under its name. ``export archive NAME
--xml INTAKE`` files it in its year's folder once the intake file proves the
download, held as taken in ``sync mark``'s record (U242). With no tracklist or
name each backfills behind one gate (U129); ``--rename`` is ``set_rename``.

The verbs' registered home and every caller's import path. Layer: modules.
The builders' parameters are unannotated so this file does not import the CLI
registry (KTD23).
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.cli.output import Envelope
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.export.cli import UNMATCHED_WARNING
from cratekit.export.set_archive import (  # noqa: F401 - the verbs' public names
    NOTHING_BUILT_SAID,
    ArchivePlanned,
    apply_archive,
    plan_archive,
    plan_archive_named,
)
from cratekit.export.set_common import (
    _ARCHIVE,
    _SET,
    NOTHING_WRITTEN,
    REMOVES_NOTHING,
    _Deferred,
    _inspiration_folder,
    _names_for_job,
    _unnamed,
    failed,
    plan_payload,
    set_name,
    warning,
    with_applied,
)
from cratekit.export.set_match import match_rows
from cratekit.export.set_rename import (  # noqa: F401 - the verbs' public names
    RENAME_GATE,
    RENAME_UNRESOLVED,
    RenamePlanned,
    _export_set_rename,
    _standing_mark,
    apply_rename,
    plan_rename,
)
from cratekit.intake.cli import TRACKLIST_SUFFIX
from cratekit.modules.outbound import ledger, sets, shell

#: What a row is in the plan, one word each.
ADD = "add"
ALREADY = "already"
UNMATCHED = "unmatched"
#: Matched, and the provider would not add it when it was asked before.
REFUSED = "refused"
#: Matched, recorded as written, and no longer on the playlist: a person took
#: it off, and it is not put back.
TAKEN_OFF = "taken-off"
#: The same track as an earlier row of the set, asked for once.
REPEAT = "repeat"

_ROW_WHY = {
    REFUSED: "the provider would not add it when it was asked before, so it is not asked again",
    TAKEN_OFF: "it was written before and is no longer on the playlist, so it is not put back",
    REPEAT: "an earlier row of the set is the same track",
}

#: The file name endings a tracklist is known by, taken off for its name.
#: ``intake identify``'s own first, so its ``.txt`` is not the one taken.
_ENDINGS = (TRACKLIST_SUFFIX, ".list.json", ".txt", ".json")


def build_set(parser, entry) -> None:
    del entry
    parser.add_argument(
        "tracklist",
        nargs="?",
        metavar="TRACKLIST",
        help=(
            "the tracklist intake identify wrote, a typed one, or a list document; "
            "omit it to backfill over INSPIRATION playlists that have no account playlist"
        ),
    )
    parser.add_argument(
        "--name", help="the playlist's name on the account; defaults to the tracklist's own"
    )
    parser.add_argument(
        "--rename",
        metavar="JOB",
        help=(
            "rename the set job's account playlist to the name its INSPIRATION "
            "playlist carries now, and record the new name"
        ),
    )
    parser.set_defaults(_handler=export_set)


def build_archive(parser, entry) -> None:
    del entry
    parser.add_argument(
        "name",
        nargs="?",
        metavar="NAME",
        help=(
            "the set playlist's name, as crate export set made it; omit it to "
            "archive every recorded set whose download is proven"
        ),
    )
    said = "the intake file crate intake land wrote for the set's download"
    parser.add_argument("--xml", metavar="XML", help=said)
    parser.set_defaults(_handler=export_archive)


def name_of(path: Path) -> str:
    """The playlist name a tracklist file gives, when none is asked for: its name, ending off.

    ``intake identify``'s digest piece STAYS ON, telling two nights' recordings of
    one stem apart, since the name is the key the playlist is recorded under.
    """
    stem = path.name
    ending = next((one for one in _ENDINGS if stem.lower().endswith(one)), "")
    return set_name(stem[: len(stem) - len(ending)])



def _row_items(planned: sets.SetPlan) -> list[dict[str, Any]]:
    """One item per tracklist row, in its order, each saying what becomes of it."""
    owed = set(planned.add)
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    for row in planned.rows:
        if not row.matched:
            action = UNMATCHED
        elif row.remote_id in seen:
            action = REPEAT
        elif row.remote_id in owed:
            action = ADD
        elif row.remote_id in planned.refused:
            action = REFUSED
        elif row.remote_id in planned.on_playlist:
            action = ALREADY
        else:
            action = TAKEN_OFF
        seen.add(row.remote_id)
        why = row.reason or _ROW_WHY.get(action, "")
        items.append(
            {
                "id": row.remote_id,
                "kind": "track",
                "position": row.position,
                "artist": row.artist,
                "title": row.title,
                "action": action,
                **({"how": row.how} if row.how else {}),
                **({"why": why} if why else {}),
            }
        )
    return items


def _set_payload(planned: sets.SetPlan) -> dict[str, Any]:
    tracks = _row_items(planned)
    playlist = {
        "id": planned.remote_id,
        "kind": "playlist",
        "name": planned.name,
        "action": planned.action,
        "add": len(planned.add),
    }
    counted = Counter(item["action"] for item in tracks)
    totals = {
        "count": len(tracks),
        **{one: counted[one] for one in (ADD, ALREADY, REFUSED, TAKEN_OFF, REPEAT, UNMATCHED)},
        "writes": planned.writes,
    }
    return plan_payload(planned.identity(), [playlist, *tracks], totals)


def _left_out(planned: sets.SetPlan) -> list[str]:
    return [f"{row.artist} - {row.title}: {row.reason}" for row in planned.unmatched]


def _set_shown(planned: sets.SetPlan) -> dict[str, Any]:
    playlist = {
        sets.CREATE: "create it private",
        sets.REUSE: "use the one already made for this set",
    }[planned.action]
    shown: dict[str, Any] = {
        "playlist": f"{planned.name}: {playlist}",
        "tracks": (
            f"{len(planned.add)} to add, of {sum(1 for row in planned.rows if row.matched)} "
            f"matched in a tracklist of {len(planned.rows)}"
        ),
        "left out": _left_out(planned),
        "removes": REMOVES_NOTHING,
    }
    if planned.refused or planned.taken_off:
        shown["not asked again"] = (
            f"{len(planned.refused)} matched track(s) the provider would not add "
            f"before, and {len(planned.taken_off)} written before and since taken "
            f"off the playlist"
        )
    if not planned.writes:
        shown["nothing to write"] = (
            "nothing in the set was matched"
            if planned.action == sets.CREATE
            else "every matched track is on the playlist or is not asked for again"
        )
    return shown


def unmatched_warnings(planned: sets.SetPlan) -> list[dict[str, str]]:
    """The warning ``export playlist`` gives over a track it left out (R-850)."""
    if not planned.unmatched:
        return []
    return [
        warning(
            UNMATCHED_WARNING,
            f"{len(planned.unmatched)} of {len(planned.rows)} track(s) of the set "
            f"were not matched and are not on the playlist: " + "; ".join(_left_out(planned)),
        )
    ]


def _set_failed(exc: Exception, done: sets.SetApplied, planned: sets.SetPlan) -> CratekitError:
    """The failure, with what was already written named in it, on ``label playlists``'s rule."""
    made = "created" if done.created else "in hand"
    wrote = (
        f"before this failed the playlist was {made} and {len(done.added)} track(s) added"
        if done.remote_id
        else NOTHING_WRITTEN
    )
    detail = {
        "name": planned.name,
        "remote_id": done.remote_id,
        "created": done.created,
        "added": list(done.added),
    }
    again = "run crate export set again; what was written is reused, never made twice"
    return failed(exc, wrote, again, origin=_SET, detail=detail) or refuse(
        "internal-error",
        f"{wrote}. The write failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        origin=_SET,
        detail={**detail, "kind": type(exc).__name__},
    )


@dataclass
class SetPlanned:
    """One set's account playlist, planned: the gate's payload and what an apply needs."""

    name: str
    payload: dict[str, Any]
    planned: sets.SetPlan
    remote: Any

    @property
    def shown(self) -> dict[str, Any]:
        return _set_shown(self.planned)

    @property
    def writes(self) -> bool:
        return self.planned.writes


def plan_from_wanted(
    cfg, name: str, wanted: Sequence[match.Wanted], *, year: str | None = None
) -> SetPlanned:
    """Plan the account playlist for a set's rows under ``name``, its playlist name already.

    An all unmatched set still returns its plan, writing nothing, so the caller can say why.
    """
    name = set_name(name)
    if not name:
        raise _unnamed(str(name))
    remote = _Deferred(cfg)
    rows = match_rows(cfg, wanted, remote)
    planned = sets.plan_set(cfg, name, rows, remote, year=year or str(datetime.now().year))
    return SetPlanned(name=name, payload=_set_payload(planned), planned=planned, remote=remote)


def apply_planned(cfg, built: SetPlanned) -> tuple[dict[str, Any], list[dict[str, str]], bool]:
    """Write what the plan names after the gate said apply. Returns payload, warnings, wrote."""
    planned = built.planned
    warnings = unmatched_warnings(planned)
    if not planned.writes:
        return built.payload, warnings, False
    done = sets.SetApplied()
    try:
        sets.apply_set(cfg, built.remote, planned, done)
    except Exception as exc:
        raise _set_failed(exc, done, planned) from exc
    if done.refused:
        said = (
            f"the provider would not add {len(done.refused)} matched track(s) "
            f"to {planned.name}; they are recorded and not asked for again"
        )
        warnings.append(warning("export-set-tracks-refused", said))
    applied = {
        "remote_id": done.remote_id,
        "created": done.created,
        "added": len(done.added),
        "refused": len(done.refused),
    }
    return with_applied(built.payload, applied), warnings, True


def _settled(ctx, data, warnings, wrote: bool) -> Envelope:
    outcome = Outcome.OK if wrote else Outcome.NO_OP
    return ctx.envelope(data=data, outcome=outcome, warnings=warnings)


def export_set(ctx) -> Envelope:
    cfg = shell.load_config("export.set_cli")
    if ctx.args.rename is not None:
        return _export_set_rename(ctx, cfg)
    if ctx.args.tracklist is None:
        return _export_set_backfill(ctx, cfg)
    path = Path(str(ctx.args.tracklist))
    wanted = match_cli.read_list(path)
    given = ctx.args.name if ctx.args.name is not None else name_of(path)
    name = set_name(given)
    if not name:
        raise _unnamed(str(given))
    built = plan_from_wanted(cfg, name, wanted)
    # THE PLAN ITSELF, so the screen shows every item the digest covers (R-693).
    option = ctx.gate.require(ctx.entry.gates[0], plan=built.payload, context=built.shown)
    if option != "apply" or not built.writes:
        return _settled(ctx, built.payload, unmatched_warnings(built.planned), False)
    return _settled(ctx, *apply_planned(cfg, built))



def export_archive(ctx) -> Envelope:
    cfg = shell.load_config("export.set_cli")
    if ctx.args.name is None:
        return _export_archive_backfill(ctx, cfg)
    if ctx.args.xml is None:
        raise refuse(
            "intake-list-unusable",
            "crate export archive needs the intake file that proves the set "
            "landed, pass --xml INTAKE, or omit the name to archive every "
            "recorded set whose download is proven",
            steps=("pass --xml with the intake file crate intake land wrote",),
            origin=_ARCHIVE,
        )
    archived = plan_archive(cfg, ctx.args.name, Path(str(ctx.args.xml)))
    option = ctx.gate.require(ctx.entry.gates[0], plan=archived.payload, context=archived.shown)
    if archived.planned is None or archived.remote is None:
        nothing = warning("export-archive-nothing-built", f"{archived.name}: {NOTHING_BUILT_SAID}")
        return ctx.envelope(data=archived.payload, outcome=Outcome.NO_OP, warnings=[nothing])
    if option != "apply" or not archived.planned.writes:
        return ctx.envelope(data=archived.payload, outcome=Outcome.NO_OP)
    return _settled(ctx, *apply_archive(cfg, archived))



def _inspiration_playlists(
    cfg, *, read_only: bool = False, declared=None, one_read=None
) -> list[tuple[str, str]]:
    """Live playlists under the declared INSPIRATION folder: (name, playlist_id)."""
    with _inspiration_folder(
        cfg, read_only=read_only, declared=declared, one_read=one_read
    ) as found:
        return inspiration_playlists_on(*found)


def inspiration_playlists_on(db, folder_id: str) -> list[tuple[str, str]]:
    """Live playlists directly under the INSPIRATION folder ``folder_id``, on ``db``.

    One rule for the archive's proof (U142) and organize's parity step (U144).
    """
    from cratekit.core import rb_writer

    if not folder_id:
        return []
    # Bound under a local name so the add-only scan over this file does not
    # read the writer's removal predicate as a removal this verb performs.
    gone = rb_writer.node_removed
    rows = [row for row in db.get_playlist(ParentID=folder_id) if not rb_writer.is_folder(row)]
    named = ((set_name(str(getattr(row, "Name", "") or "")), row) for row in rows if not gone(row))
    found = [(name, str(row.ID)) for name, row in named if name]
    return sorted(found, key=lambda one: one[0].lower())


def inspiration_names(cfg, *, one_read=None) -> frozenset[str] | None:
    """Every set name an INSPIRATION playlist carries, or None when none is declared.

    For ``crate organize`` (U142), whose proof a set downloaded it is. ``one_read``
    is the report's one read handle (U267).
    """
    from cratekit.core import active_taxonomy

    declared = active_taxonomy.load(cfg)
    if declared.inspiration is None:
        return None
    return frozenset(
        name
        for name, _pid in _inspiration_playlists(
            cfg, read_only=True, declared=declared, one_read=one_read
        )
    )


def _job_for_inspiration_name(cfg, name: str):
    """The succeeded set job whose frozen or recorded playlist name is ``name``, or None."""
    from cratekit.core import jobs, session
    from cratekit.intake import set_playlist

    wanted = set_name(name)
    with jobs.open_store() as store:
        for job in jobs.list_jobs(store):
            if (
                job.handler_key == set_playlist.SET_KEY
                and job.state is jobs.JobState.SUCCEEDED
                and wanted in _names_for_job(job)
            ):
                return job
    # Session records from a landing name the playlist and the job.
    records, _unreadable = session.scan_log(cfg)
    for record in records:
        kept = record.detail.get(set_playlist.RECORD_KEY)
        if not isinstance(kept, dict) or set_name(str(kept.get("name") or "")) != wanted:
            continue
        if not (job_id := str(kept.get("job") or "")):
            continue
        with jobs.open_store() as store:
            try:
                return set_playlist.set_job_or_refuse(store, job_id)
            except Exception:
                continue
    return None


def _wanted_from_job(cfg, job) -> tuple[match.Wanted, ...]:
    """The set's rows as Wanted, from the job's committed reports."""
    from cratekit.core import jobs
    from cratekit.intake import cli as intake_cli
    from cratekit.intake import set_playlist

    del cfg
    with jobs.open_store() as store:
        held = set_playlist.set_job_or_refuse(store, job.job_id)
        raw = set_playlist.reports_of(store, held)
    tracks = (report.get("track") if isinstance(report, dict) else None for report in raw)
    return tuple(intake_cli.thawed(track) for track in tracks if isinstance(track, dict))


@dataclass(frozen=True)
class _Backfill:
    """How a backfill names what it did: in a failure, in its totals, in its detail."""

    did: str
    listed_as: str
    detail_key: str
    origin: tuple[str, ...]
    again: str


_SET_BACKFILL = _Backfill(
    "made",
    "playlists",
    "applied",
    _SET,
    "the playlists named above are on the account; resume or "
    "run crate export set again for the rest",
)
_ARCHIVE_BACKFILL = _Backfill(
    "archived",
    "archived",
    "archived",
    _ARCHIVE,
    "the playlists named above are already archived on the account; "
    "resume or run crate export archive again for the rest",
)


def _gate_then_apply_each(ctx, cfg, payload, shown, warnings, planned, apply, said: _Backfill):
    """A backfill's one gate, then each plan that writes applied in order.

    A failure after some landed names them (U129).
    """
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=shown)
    if option != "apply" or not payload["totals"]["writes"]:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)
    done: list[str] = []
    try:
        for one in planned:
            if not one.writes:
                continue
            _data, more, wrote = apply(cfg, one)
            warnings.extend(more)
            if wrote:
                done.append(one.name)
    except Exception as exc:
        if not done:
            raise
        before = f"before this failed the backfill already {said.did} {', '.join(done)}"
        detail = {said.detail_key: list(done)}
        again = said.again
        carried = failed(exc, before, again, origin=said.origin, detail=detail, credential=True)
        raise carried or refuse(
            "internal-error",
            f"{before}. {type(exc).__name__}: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            steps=(again,),
            scope=Scope.RUN,
            origin=said.origin,
            detail={**detail, "kind": type(exc).__name__},
        ) from exc
    return _settled(ctx, with_applied(payload, {said.listed_as: done}), warnings, bool(done))


def _export_set_backfill(ctx, cfg) -> Envelope:
    """List INSPIRATION playlists with no account playlist, plan each, one gate."""
    held = set(ledger.set_playlist_names(cfg))
    missing = [name for name, _pid in _inspiration_playlists(cfg) if name not in held]
    if not missing:
        payload = plan_payload(
            {"kind": "export-set-backfill", "names": []}, [], {"count": 0, "writes": False}
        )
        shown = {
            "inspiration without account playlist": ["none"],
            "already on the account": sorted(held),
            "removes": REMOVES_NOTHING,
            "nothing to write": (
                "every INSPIRATION playlist already has an account playlist, or "
                "there is no INSPIRATION playlist yet"
            ),
        }
        ctx.gate.require(ctx.entry.gates[0], plan=payload, context=shown)
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    # Each set planned from its job's reports, so the gate shows the writes.
    planned: list[SetPlanned] = []
    warnings: list[dict[str, str]] = []
    for name in missing:
        job = _job_for_inspiration_name(cfg, name)
        wanted = _wanted_from_job(cfg, job) if job is not None else ()
        if job is None:
            said = (
                f"{name}: no succeeded set job names this INSPIRATION "
                f"playlist, so its account playlist is not planned here"
            )
            warnings.append(warning("export-set-backfill-no-job", said))
        elif not wanted:
            said = f"{name}: the set job carries no tracks to match"
            warnings.append(warning("export-set-backfill-no-tracks", said))
        else:
            planned.append(plan_from_wanted(cfg, name, wanted))
    items = [item for one in planned for item in one.payload["items"]]
    writes = any(one.writes for one in planned)
    payload = plan_payload(
        {"kind": "export-set-backfill", "sets": [one.planned.identity() for one in planned]},
        items,
        {"count": len(items), "sets": len(planned), "writes": writes},
    )
    shown = {
        "inspiration without account playlist": [one.name for one in planned],
        "left for a later sitting": [one["message"] for one in warnings],
        "removes": REMOVES_NOTHING,
    }
    if not writes:
        shown["nothing to write"] = (
            "every listed set has nothing matched to add, or is already on the account"
        )
    return _gate_then_apply_each(
        ctx, cfg, payload, shown, warnings, planned, apply_planned, _SET_BACKFILL
    )


def _proof_for_set(cfg, name: str) -> Path | None:
    """The latest intake file whose stem is the set's name, organize's own rule."""
    from cratekit.organize.account import intake_by_pass

    return intake_by_pass(cfg).get(set_name(name))


def _export_archive_backfill(ctx, cfg) -> Envelope:
    """Archive every recorded set whose download is proven, behind one gate."""
    planned: list[ArchivePlanned] = []
    listed: list[dict[str, Any]] = []
    waiting: list[str] = []
    warnings: list[dict[str, str]] = []
    for name in ledger.set_playlist_names(cfg):
        xml = _proof_for_set(cfg, name)
        if xml is None:
            why = "no intake file proves its download"
            listed.append(
                {"id": name, "kind": "set", "name": name, "action": "waiting", "why": why}
            )
            waiting.append(name)
            continue
        try:
            archived = plan_archive(cfg, name, xml)
        except CratekitError as exc:
            # Soft skip per set, as a landing's _plan_set_archive does. A
            # CredentialError (not a CratekitError) still refuses the verb.
            said = f"{name}: {exc.cause.message}"
            warnings.append(warning("export-archive-backfill-refused", said))
            continue
        planned.append(archived)
        listed.extend(archived.payload["items"])
    identity = {
        "kind": "export-archive-backfill",
        "sets": [one.payload["digest"] for one in planned],
        "waiting": waiting,
    }
    writes = any(one.writes for one in planned)
    payload = plan_payload(
        identity, listed, {"count": len(listed), "sets": len(planned), "writes": writes}
    )
    shown = {
        "to archive": [one.name for one in planned if one.writes] or ["none"],
        "already filed": [one.name for one in planned if not one.writes],
        "waiting on a landing": waiting,
    }
    return _gate_then_apply_each(
        ctx, cfg, payload, shown, warnings, planned, apply_archive, _ARCHIVE_BACKFILL
    )


__all__ = [
    "ArchivePlanned", "RenamePlanned", "SetPlanned", "apply_archive", "apply_planned",
    "apply_rename", "build_archive", "build_set", "export_archive", "export_set",
    "inspiration_names", "inspiration_playlists_on", "match_rows", "name_of", "plan_archive",
    "plan_archive_named", "plan_from_wanted", "plan_rename", "set_name", "unmatched_warnings",
]
