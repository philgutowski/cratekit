"""``export set --rename JOB``: a set's account playlist follows its INSPIRATION rename (U140).

Behind its own gate it retitles the account playlist by identifier, moves the
ledger key and refreezes the job, so a backfill makes no twin under the new name.

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.export.set_common import (
    _SET,
    REMOVES_NOTHING,
    _Deferred,
    _inspiration_folder,
    _names_for_job,
    _unnamed,
    before_failing,
    failed,
    plan_payload,
    set_name,
    with_applied,
)
from cratekit.intake.cli import PLAYLIST_NAME
from cratekit.modules.outbound import sets
from cratekit.sync import mark_record

#: The gate the rename asks at, the second one ``export.set`` declares.
RENAME_GATE = "export.set.rename"
#: Why a rename cannot be planned: no INSPIRATION playlist to follow, no
#: account playlist recorded, or one the archive marked.
RENAME_UNRESOLVED = "export-set-rename-unresolved"
#: What a rename plan does to each of its two items.
RENAME = "rename"
REFREEZE = "refreeze"
KEEP = "keep"


def _rename_unresolved(job_id: str, message: str, step: str, **detail: Any) -> CratekitError:
    return refuse(
        RENAME_UNRESOLVED,
        f"job {job_id}: {message}; nothing was written",
        steps=(step,),
        origin=_SET,
        detail={"job_id": job_id, **detail},
    )


def _inspiration_of(cfg, job_id: str) -> tuple[str, str] | None:
    """The INSPIRATION playlist a write made for this job, its id and live name, or None."""
    from cratekit.intake import set_playlist

    with _inspiration_folder(cfg) as (db, folder_id):
        if not folder_id:
            return None
        return set_playlist.recorded_playlist(cfg, db, job_id, folder_id)


def _standing_mark(cfg, remote_id: str) -> mark_record.Marked | None:
    """A legacy archive prefix still on this playlist, or None.

    ONLY ONE A PASS WROTE AND NO LATER STRIP TOOK OFF (U242).
    """
    every = mark_record.MarkRecord(cfg).all()
    for entry in mark_record.standing_prefix_marks(every):
        if entry.playlist_id != remote_id:
            continue
        superseded = any(
            other.playlist_id == remote_id
            and not other.of_the_prefix
            and not other.unmarked
            and other.marked > entry.marked
            for other in every
        )
        if not superseded:
            return entry
    return None


@dataclass
class RenamePlanned:
    """One set's rename, planned: the gate's payload and what an apply needs."""

    planned: sets.RenamePlan
    payload: dict[str, Any]

    @property
    def shown(self) -> dict[str, Any]:
        return _rename_shown(self.planned)

    @property
    def writes(self) -> bool:
        return self.planned.writes


def _rename_payload(planned: sets.RenamePlan) -> dict[str, Any]:
    items = [
        {
            "id": planned.playlist.remote_id,
            "kind": "playlist",
            "name": planned.playlist.name,
            "to": planned.to,
            "action": RENAME if planned.rename else KEEP,
        },
        {
            "id": planned.job_id,
            "kind": "job",
            "name": planned.frozen,
            "to": planned.live or planned.to,
            "action": REFREEZE if planned.refreeze else KEEP,
        },
    ]
    return plan_payload(planned.identity(), items, {"count": len(items), "writes": planned.writes})


def _rename_shown(planned: sets.RenamePlan) -> dict[str, Any]:
    old, to = planned.playlist.name, planned.to
    frozen_to = planned.live or to
    shown: dict[str, Any] = {
        "follows": f"the INSPIRATION playlist {planned.inspiration_id}, named {to!r}",
        "account playlist": (
            f"{planned.playlist.remote_id}: {old!r} -> {to!r}"
            if planned.rename
            else f"{planned.playlist.remote_id}: already {to!r}"
        ),
        "ledger entry": f"{old!r} -> {to!r}" if planned.rename else f"already {to!r}",
        "frozen name": (
            f"{repr(planned.frozen) if planned.frozen else 'none'} -> {frozen_to!r}"
            if planned.refreeze
            else f"already {frozen_to!r}"
        ),
        "removes": REMOVES_NOTHING,
    }
    if not planned.writes:
        shown["nothing to write"] = (
            "the account playlist, its ledger entry and the job already carry the "
            "INSPIRATION playlist's name"
        )
    return shown


def plan_rename(cfg, job_id: str) -> RenamePlanned:
    """Plan a set's account playlist renamed to its INSPIRATION playlist's live name.

    REFUSED BY NAME, with nothing written, with no INSPIRATION playlist, no account
    playlist or two under the job's names, or the archive's mark on it.
    """
    from cratekit.core import jobs
    from cratekit.intake import set_playlist

    with jobs.open_store() as store:
        job = set_playlist.set_job_or_refuse(store, job_id)
    found = _inspiration_of(cfg, job.job_id)
    if found is None:
        raise _rename_unresolved(
            job.job_id,
            "no INSPIRATION playlist this library made for the set is still in the "
            "folder, so there is no name for its account playlist to follow",
            f"make it with crate intake inspiration {job.job_id}, then rename",
        )
    inspiration_id, live = found
    to = set_name(live)
    if not to:
        raise _unnamed(live)
    # R-1017. The frozen name, which an earlier rename chose; then the names the
    # set's landings wrote, since a backfill made the account playlist under
    # one; then the names the job's page words spell today.
    frozen = set_playlist.frozen_name(job)
    recorded = tuple(set_name(one) for one in set_playlist.recorded_names(cfg, job.job_id))
    names = tuple(
        dict.fromkeys(
            one
            for one in (set_name(frozen) if frozen else "", *recorded, *_names_for_job(job))
            if one
        )
    )
    planned = sets.plan_rename(
        cfg, job_id=job.job_id, names=names, to=to, frozen=frozen, live=live,
        inspiration_id=inspiration_id,
    )
    if planned is None:
        raise _rename_unresolved(
            job.job_id,
            f"no account playlist is recorded for the set under {to!r} or any name "
            f"its landing recorded or its job gives "
            f"({', '.join(repr(one) for one in names) or 'none'}), so "
            f"there is nothing to rename",
            "if the set's account playlist was made under a name of its own, from a "
            "tracklist or --name, rename it on the account by hand, since this verb "
            "finds only the names the landing recorded and the job gives; if the set "
            "has none, crate export set with no tracklist makes one",
            names=list(names),
            to=to,
        )
    if planned.twin is not None:
        raise _rename_unresolved(
            job.job_id,
            f"two account playlists are recorded for the set, "
            f"{planned.playlist.remote_id} under {planned.playlist.name!r} and "
            f"{planned.twin.remote_id} "
            f"under {planned.twin.name!r}, and renaming either would leave the other "
            f"on the account with nothing recording which is the set's",
            "keep one of the two on the account, take the other and its ledger entry "
            "away by hand, then rename again",
            remote_id=planned.playlist.remote_id,
            twin=planned.twin.remote_id,
        )
    if planned.rename:
        mark = _standing_mark(cfg, planned.playlist.remote_id)
        if mark is not None:
            raise _rename_unresolved(
                job.job_id,
                f"the account playlist {planned.playlist.remote_id} was archived as "
                f"{mark.to!r} by the pass {mark.pass_name}, and renaming it would take "
                f"that mark off a title crate sync unmark expects to find",
                f"run crate sync unmark --pass {mark.pass_name!r}, rename, then archive again",
                remote_id=planned.playlist.remote_id,
                pass_name=mark.pass_name,
            )
    return RenamePlanned(planned=planned, payload=_rename_payload(planned))


def _done(done: sets.RenameApplied) -> dict[str, bool]:
    return {"renamed": done.renamed, "rekeyed": done.rekeyed, "refrozen": done.refrozen}


def _rename_failed(exc: Exception, done: sets.RenameApplied, planned: sets.RenamePlan) -> CratekitError:
    """The failure, with what was already written named, on ``_set_failed``'s rule."""
    parts = []
    if done.renamed:
        parts.append(f"the account playlist was renamed to {planned.to!r}")
    if done.rekeyed:
        parts.append("its ledger entry moved")
    said = before_failing(parts, " and ")
    detail = {"job_id": planned.job_id, "remote_id": planned.playlist.remote_id, **_done(done)}
    again = (
        f"run crate export set --rename {planned.job_id} again; what was written "
        f"is not written twice"
    )
    return failed(exc, said, again, origin=_SET, detail=detail, credential=True) or refuse(
        "internal-error",
        f"{said}. The rename failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        origin=_SET,
        detail={**detail, "kind": type(exc).__name__},
    )


def apply_rename(cfg, built: RenamePlanned) -> tuple[dict[str, Any], bool]:
    """Write what the rename plan names after the gate said apply. Returns payload, wrote."""
    from cratekit.core import jobs

    planned = built.planned
    if not planned.writes:
        return built.payload, False

    def refreeze(to: str) -> None:
        with jobs.open_store() as store:
            jobs.refreeze(store, planned.job_id, PLAYLIST_NAME, to)

    done = sets.RenameApplied()
    try:
        # DEFERRED, so a plan that only refreezes the job asks for no sign in.
        sets.apply_rename(cfg, _Deferred(cfg), planned, done, refreeze=refreeze)
    except Exception as exc:
        raise _rename_failed(exc, done, planned) from exc
    return with_applied(built.payload, _done(done)), True


def _export_set_rename(ctx, cfg) -> Envelope:
    if ctx.args.tracklist is not None or ctx.args.name is not None:
        raise refuse(
            "intake-list-unusable",
            "crate export set --rename takes the set's job and nothing else, since "
            "the new name is the INSPIRATION playlist's and the tracks are not "
            "touched, so nothing was planned",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=("drop the tracklist and --name, and pass --rename JOB alone",),
            origin=_SET,
        )
    built = plan_rename(cfg, str(ctx.args.rename))
    gate = next(spec for spec in ctx.entry.gates if spec.name == RENAME_GATE)
    option = ctx.gate.require(gate, plan=built.payload, context=built.shown)
    if option != "apply" or not built.writes:
        return ctx.envelope(data=built.payload, outcome=Outcome.NO_OP)
    data, wrote = apply_rename(cfg, built)
    return ctx.envelope(data=data, outcome=Outcome.OK if wrote else Outcome.NO_OP)
