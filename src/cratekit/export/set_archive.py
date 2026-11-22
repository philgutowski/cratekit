"""``export archive``: a set playlist filed in its year's folder and held as taken.

Planned and applied here for the verb, ``crate organize`` (U112) and a set
landing (U129), all through :mod:`cratekit.export.set_cli`. Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Any

from cratekit.cli.output import timestamp
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.export.set_common import (
    _ARCHIVE,
    before_failing,
    failed,
    plan_payload,
    set_name,
    warning,
    with_applied,
)
from cratekit.modules.outbound import ledger, sets
from cratekit.sync import mark_record, marks
from cratekit.sync.mark_cli import pass_name_of

#: What the gate screen and the warning say when no set playlist is recorded.
NOTHING_BUILT_SAID = (
    "no set playlist was made under this name on this library, so there is "
    "nothing to archive"
)


def _archive_payload(planned: sets.ArchivePlan | None, *, name: str, pass_name: str) -> dict[str, Any]:
    if planned is None:
        identity: dict[str, Any] = {"kind": "export-archive", "name": name}
        items: list[dict[str, Any]] = []
    else:
        identity = {**planned.identity(), "pass": pass_name}
        items = [
            {
                "id": planned.folder_id,
                "kind": "folder",
                "name": planned.folder_name,
                "action": planned.folder_action,
            },
            {
                "id": planned.playlist.remote_id,
                "kind": "playlist",
                "name": planned.title if planned.title is not None else "",
                "built_as": planned.playlist.name,
                "move": planned.move,
                "action": sets.MARK if planned.mark else "skip",
                **({"reason": planned.left} if planned.left else {}),
            },
        ]
    writes = bool(planned is not None and planned.writes)
    return plan_payload(identity, items, {"count": len(items), "writes": writes})


def _archive_shown(planned: sets.ArchivePlan | None, *, name: str, pass_name: str) -> dict[str, Any]:
    if planned is None:
        return {"set playlist": name, "nothing to archive": NOTHING_BUILT_SAID}
    folder = {
        sets.CREATE: "create it",
        sets.ADOPT: "use the one already on the account under this name",
        sets.REUSE: "use the one already recorded",
    }[planned.folder_action]
    if planned.left:
        title = "not marked, since " + (
            "Cratekit already holds it as taken"
            if planned.left == sets.ALREADY_MARKED
            else f"it was retitled since it was made as {planned.playlist.name!r}"
        )
    elif planned.move:
        title = (
            f"recorded as taken, its title left as it is, if its title in the folder is "
            f"still {planned.playlist.name!r} once it is there"
        )
    else:
        title = "recorded as taken, its title left as it is"
    shown: dict[str, Any] = {
        "set playlist": planned.playlist.name,
        "pass": pass_name,
        "folder": f"{planned.folder_name}: {folder}",
        "place": "put it in the folder" if planned.move else "already in the folder, left there",
        "mark": title,
        "undone by": f"crate sync unmark --pass {pass_name}",
    }
    if planned.stale_folder and planned.writes:
        shown["recorded folder"] = (
            f"the folder recorded for {planned.folder_name}, {planned.stale_folder}, is no "
            f"longer on the account, so its record is replaced"
        )
    if not planned.writes:
        # NOTHING IS WRITTEN, the ledger included (U142): an adoption alone is
        # no write, so a stale record is not said to be replaced either.
        shown["nothing to write"] = (
            "the playlist is already in its folder, its title left as a person set it"
            if planned.left == sets.RETITLED
            else "the playlist is already in its folder and held as taken"
        )
    return shown


def _done(done: sets.ArchiveApplied) -> dict[str, Any]:
    """What an archive apply did, as its totals and its failures name it."""
    return {key: getattr(done, key) for key in ("folder_id", "folder_created", "moved", "marked")}


def _archive_failed(exc: Exception, done: sets.ArchiveApplied, unrecorded: bool) -> CratekitError:
    """The failure, with what was already written named, on ``label mark``'s rule."""
    parts = []
    if done.folder_id:
        parts.append(f"the folder was {'created' if done.folder_created else 'in hand'}")
    if done.moved:
        parts.append("the playlist was put in it")
    if unrecorded:
        parts.append("the mark record could not hold the playlist as taken")
    elif done.marked:
        parts.append("the playlist was recorded as taken")
    said = before_failing(parts, ", ")
    detail = {**_done(done), "unrecorded": unrecorded}
    again = "run crate export archive again; what was done is not done twice"
    kind = {**detail, "kind": type(exc).__name__}
    carried = failed(exc, said, again, scope=Scope.SOURCE, origin=_ARCHIVE, detail=detail)
    if carried is not None:
        return carried
    if unrecorded:
        return refuse(
            "sync-mark-record-unusable",
            f"{said}. The record could not be written ({type(exc).__name__}: {exc})",
            steps=("make the library's state directory writable by this account", again),
            scope=Scope.SOURCE,
            origin=_ARCHIVE,
            detail=kind,
        )
    return refuse(
        "internal-error",
        f"{said}. The archive failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.SOURCE,
        origin=_ARCHIVE,
        detail=kind,
    )


@dataclass
class ArchivePlanned:
    """One set's archive, planned: the gate's payload and what an apply needs."""

    name: str
    pass_name: str
    xml: Path
    payload: dict[str, Any]
    planned: sets.ArchivePlan | None = None
    remote: Any = None

    @property
    def shown(self) -> dict[str, Any]:
        return _archive_shown(self.planned, name=self.name, pass_name=self.pass_name)

    @property
    def writes(self) -> bool:
        return self.planned is not None and self.remote is not None and self.planned.writes


def plan_archive_named(
    cfg, name: str, *, pass_name: str, year: str | None = None
) -> ArchivePlanned:
    """Plan one set's archive by name, once the caller has the download's proof."""
    name = set_name(name)
    playlist = ledger.set_playlist(cfg, name)
    planned: sets.ArchivePlan | None = None
    remote = None
    if playlist is not None:
        from cratekit.modules.outbound import account

        remote = account.resolve(cfg)
        planned = sets.plan_archive(
            cfg, playlist, remote, year=playlist.year or year or str(datetime.now().year)
        )
    payload = _archive_payload(planned, name=name, pass_name=pass_name)
    return ArchivePlanned(name, pass_name, Path(), payload, planned=planned, remote=remote)


def plan_archive(cfg, name: str, xml: Path) -> ArchivePlanned:
    """Plan one set's archive from the intake file that proves its download."""
    pass_name = pass_name_of(xml)
    # THE PROOF FIRST, before the ledger, the account or a credential.
    marks.require_output(xml)
    return replace(plan_archive_named(cfg, name, pass_name=pass_name), xml=xml)


#: Why a playlist the plan would mark was not, by what the folder showed.
_LEFT_SAID = {
    sets.ALREADY_MARKED: "already taken when it was read in the folder",
    sets.RETITLED: "retitled by somebody when it was read in the folder",
}


def apply_archive(cfg, archived: ArchivePlanned) -> tuple[dict[str, Any], list[dict[str, str]], bool]:
    """File, move and mark what the plan names, after the gate said apply.

    Returns the payload, its warnings and whether it wrote; raises naming what was written.
    """
    planned = archived.planned
    if planned is None or archived.remote is None:
        raise refuse(
            "internal-error",
            f"{archived.name} has no recorded set playlist to archive, so there is "
            f"nothing an apply could write",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.SOURCE,
            origin=_ARCHIVE,
            detail={"name": archived.name},
        )
    record = mark_record.MarkRecord(cfg)
    # THE RECORD IS LOCKABLE BEFORE ANYTHING IS WRITTEN, as ``sync mark`` asks.
    record.ready()
    done = sets.ArchiveApplied()
    unrecorded = [False]

    def keep(title: str) -> None:
        # HELD AS TAKEN, NO TITLE CHANGES (U242): what ``sync unmark --pass``
        # lets go, and what the INSPIRATION step reads a set by.
        try:
            record.take(
                [
                    mark_record.Taken(
                        playlist_id=planned.playlist.remote_id,
                        name=title,
                        by=archived.pass_name,
                        how=mark_record.BY_SET,
                        at=timestamp(),
                    )
                ]
            )
        except (CratekitError, OSError):
            unrecorded[0] = True
            raise

    try:
        sets.apply_archive(cfg, archived.remote, planned, done, record=keep)
    except Exception as exc:
        raise _archive_failed(exc, done, unrecorded[0]) from exc
    warnings: list[dict[str, str]] = []
    if done.left and planned.mark:
        why = _LEFT_SAID.get(
            done.left,
            "not yet listed in the folder it was put in; archive it again "
            "once the account lists it",
        )
        said = f"{planned.playlist.name} was {why}, so it was not recorded as taken"
        warnings.append(warning("export-archive-changed-since-plan", said))
    wrote = bool(done.folder_created or done.moved or done.marked)
    return with_applied(archived.payload, _done(done)), warnings, wrote
