"""``export.set`` and ``export.archive``: a set as a playlist on the account (R-837).

The source system turns an identified set, or a tracklist somebody typed, into
a private playlist on the streaming account, and once the set has been
downloaded it prefixes that playlist ``DOWNLOADED `` and files it in a root
folder named for the year the set was processed. These two verbs are those two
steps, each behind one explicit gate.

``export set TRACKLIST`` READS THE LIST THE INTAKE VERBS READ, the text file
``intake identify`` writes or one somebody typed, or a list document, through
``match_cli.read_list``. Neither text form carries an ISRC or a provider
identifier, and the account's own match never searches by title (R-356), so a
row is decided by the first of four that applies, and the plan writes nothing
on the way:

1. the provider identifier the row carries, which only a list document has;
2. its ISRC, through the account's own match, which chooses among releases;
3. a provider candidate a person already accepted in review for the row,
   ``intake missing``'s own question, read and never offered here;
4. the catalogue's text search, listed only on ``candidates.sole_exact``'s one
   distinct exact candidate, never on a score.

Anything else is LEFT OUT AND NAMED, with its reason, on the gate screen, in the
items and in a warning, as ``export playlist`` names its own (R-850). A second
run onto the same set reuses the playlist recorded under its name and plans
nothing when every matched track is on it.

``export archive NAME --xml INTAKE`` IS THE STEP AFTER THE DOWNLOAD. The intake
file ``intake land`` wrote is the proof it landed and names the pass, on
``sync/marks.py``'s rule that a title is changed only once the importable file
is on disk. The rename is recorded in ``sync mark``'s record under that pass,
so ``sync unmark --pass`` takes it off.

Layer: modules. The builders' parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, review
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.export.cli import UNMATCHED_WARNING
from cratekit.intake import candidates
from cratekit.intake.cli import TRACKLIST_SUFFIX
from cratekit.label import catalogue
from cratekit.modules.outbound import ledger, sets, shell
from cratekit.sync import mark_record, marks
from cratekit.sync.mark_cli import pass_name_of

_SET = ("export.set",)
_ARCHIVE = ("export.archive",)

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

#: What the gate screen and the warning say when no set playlist is recorded.
NOTHING_BUILT_SAID = (
    "no set playlist was made under this name on this library, so there is "
    "nothing to archive"
)

#: The file name endings a tracklist is known by, taken off for its name.
#: ``intake identify``'s own first, so its ``.txt`` is not the one taken.
_ENDINGS = (TRACKLIST_SUFFIX, ".list.json", ".txt", ".json")


def build_set(parser, entry) -> None:
    del entry
    parser.add_argument(
        "tracklist",
        metavar="TRACKLIST",
        help="the tracklist intake identify wrote, a typed one, or a list document",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="the playlist's name on the account; defaults to the tracklist's own",
    )
    parser.set_defaults(_handler=export_set)


def build_archive(parser, entry) -> None:
    del entry
    parser.add_argument(
        "name",
        metavar="NAME",
        help="the set playlist's name, as crate export set made it",
    )
    parser.add_argument(
        "--xml",
        required=True,
        metavar="XML",
        help="the intake file crate intake land wrote for the set's download",
    )
    parser.set_defaults(_handler=export_archive)


def set_name(given: str) -> str:
    """A set playlist's name as it is made and recorded, and as it is looked up.

    A slash becomes a dash, the source system's rule, since a downloader reads
    one in a playlist name as a folder. ONE SPELLING FOR BOTH VERBS, so a name
    the archive is handed finds the record the build wrote under it.
    """
    return str(given).replace("/", "-").strip()


def name_of(path: Path) -> str:
    """The playlist name a tracklist file gives, when none is asked for.

    The file's own name with its ending off. ``intake identify``'s piece of
    the recording's digest STAYS ON: it is what tells two recordings that share
    a recorder's stem apart (``intake.cli.tracklist_name``), and the name is the
    key the set's playlist is recorded under, so taking it off would add a
    second night's set to the first night's playlist. ``--name`` chooses another.
    """
    stem = path.name
    for ending in _ENDINGS:
        if stem.lower().endswith(ending):
            stem = stem[: -len(ending)]
            break
    return set_name(stem)


def _unnamed(given: str) -> CratekitError:
    return refuse(
        "intake-list-unusable",
        f"the set playlist would be named {given!r}, which is no name, so nothing "
        f"was planned",
        steps=("pass --name with the name the playlist should carry",),
        scope=Scope.RUN,
        origin=_SET,
        detail={"name": given},
    )


class _Deferred:
    """The account, resolved the first time one of its members is asked for.

    A set whose rows need no account before its gate, a list document of
    provider identifiers or of nothing, spends no login and refuses over no
    missing credential until the write it was approved for.
    """

    def __init__(self, cfg: config.Config) -> None:
        self._cfg = cfg
        self._held = None

    def __getattr__(self, name: str) -> Any:
        if self._held is None:
            from cratekit.modules.outbound import account

            self._held = account.resolve(self._cfg)
        return getattr(self._held, name)


# ── matching ────────────────────────────────────────────────────────────────


def _searched(found: catalogue.Catalogue, one: match.Wanted) -> candidates.Answer:
    """One search answer, or the refusal ``intake missing`` gives when none came."""
    try:
        rows = tuple(found.search_tracks(one.artist, candidates.query_title(one)))
    except CratekitError:
        raise
    except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
        raise refuse(
            "unavailable-transient",
            f"the streaming provider could not answer a search for {one.artist} - "
            f"{one.listed} ({exc}), so the set could not be matched; nothing was "
            f"written",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.RUN,
            origin=_SET,
            detail={"artist": one.artist, "title": one.listed},
        ) from exc
    return candidates.read_answer(one, rows)


def _not_chosen(answer: candidates.Answer) -> str:
    """Why a search answer named no track, in words for a person."""
    if not answer.hits:
        return "the provider's search returned nothing for it"
    if candidates.shown(answer):
        return (
            f"the provider's search returned {answer.hits} hit(s) and no single "
            f"exact match, so none was chosen; crate intake missing --list over "
            f"this tracklist offers them for review when the library lacks the "
            f"track, and one accepted there is used on the next run"
        )
    return f"the provider's search returned {answer.hits} hit(s) and none resembles it"


def match_rows(
    cfg: config.Config, wanted: Sequence[match.Wanted], account
) -> tuple[sets.SetRow, ...]:
    """Each row of the set, matched to one provider track or left out with why.

    THE CATALOGUE IS RESOLVED ONLY WHEN A ROW HAS TO BE SEARCHED FOR, so a list
    document whose every row carries its identifier spends no login on it.
    """
    held: list[catalogue.Catalogue] = []
    decided: list[sets.SetRow] = []
    with review.open_store(cfg) as items:
        for position, one in enumerate(wanted, start=1):
            row = {"position": position, "artist": one.artist, "title": one.listed}
            # ONLY THE PROVIDER'S OWN IDENTIFIER, on ``listdoc``'s rule: a list
            # of another origin carries that source's identifier as provenance,
            # and handed to the account it names nothing or the wrong track.
            if one.ref and one.origin == match.TIDAL:
                decided.append(sets.SetRow(**row, remote_id=str(one.ref), how="ref"))
                continue
            said = ""
            if one.isrc:
                identity = f"set-row-{position}"
                remote = account.match_track(
                    identity=identity, isrc=one.isrc, title=one.listed, artist=one.artist
                )
                if remote:
                    decided.append(sets.SetRow(**row, remote_id=str(remote), how="isrc"))
                    continue
                said = account.unmatched_reason(identity) or (
                    f"the provider names no single track under its ISRC {one.isrc}"
                )
            answered = candidates.settled(items, one)
            if answered is not None:
                if answered.state == candidates.ACCEPTED and answered.track is not None:
                    decided.append(
                        sets.SetRow(**row, remote_id=answered.track.ref, how="accepted")
                    )
                else:
                    decided.append(sets.SetRow(**row, reason=answered.reason))
                continue
            if not held:
                held.append(catalogue.resolve(cfg))
            answer = _searched(held[0], one)
            sole = candidates.sole_exact(answer)
            if sole is not None:
                decided.append(sets.SetRow(**row, remote_id=sole.track.ref, how="search"))
                continue
            reason = _not_chosen(answer)
            decided.append(sets.SetRow(**row, reason=f"{said}; {reason}" if said else reason))
    return tuple(decided)


# ── export set ──────────────────────────────────────────────────────────────


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
    items: list[dict[str, Any]] = [
        {
            "id": planned.remote_id,
            "kind": "playlist",
            "name": planned.name,
            "action": planned.action,
            "add": len(planned.add),
        },
        *tracks,
    ]
    return {
        "digest": digest_of(planned.identity()),
        "items": items,
        "totals": {
            "count": len(tracks),
            ADD: sum(1 for item in tracks if item["action"] == ADD),
            ALREADY: sum(1 for item in tracks if item["action"] == ALREADY),
            REFUSED: sum(1 for item in tracks if item["action"] == REFUSED),
            TAKEN_OFF: sum(1 for item in tracks if item["action"] == TAKEN_OFF),
            REPEAT: sum(1 for item in tracks if item["action"] == REPEAT),
            UNMATCHED: sum(1 for item in tracks if item["action"] == UNMATCHED),
            "writes": planned.writes,
        },
        "chunk": None,
    }


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
        "removes": "nothing, ever: no track or playlist is taken away",
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


def _unmatched_warnings(planned: sets.SetPlan) -> list[dict[str, str]]:
    """The warning ``export playlist`` gives over a track it left out (R-850)."""
    if not planned.unmatched:
        return []
    return [
        {
            "code": UNMATCHED_WARNING,
            "message": (
                f"{len(planned.unmatched)} of {len(planned.rows)} track(s) of the set "
                f"were not matched and are not on the playlist: "
                + "; ".join(_left_out(planned))
            ),
        }
    ]


def _set_failed(exc: Exception, done: sets.SetApplied, planned: sets.SetPlan) -> CratekitError:
    """The failure, with what was already written named in it, on ``label playlists``'s rule."""
    wrote = (
        f"before this failed the playlist was {'created' if done.created else 'in hand'} "
        f"and {len(done.added)} track(s) added"
        if done.remote_id
        else "nothing was written before this failed"
    )
    detail = {
        "name": planned.name,
        "remote_id": done.remote_id,
        "created": done.created,
        "added": list(done.added),
    }
    again = "run crate export set again; what was written is reused, never made twice"
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{wrote}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.RUN,
            retryable=cause.retryable,
            origin=_SET,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{wrote}. The write failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.RUN,
        origin=_SET,
        detail={**detail, "kind": type(exc).__name__},
    )


def export_set(ctx) -> Envelope:
    cfg = shell.load_config("export.set_cli")
    path = Path(str(ctx.args.tracklist))
    wanted = match_cli.read_list(path)
    given = ctx.args.name if ctx.args.name is not None else name_of(path)
    name = set_name(given)
    if not name:
        raise _unnamed(str(given))
    remote = _Deferred(cfg)
    rows = match_rows(cfg, wanted, remote)
    planned = sets.plan_set(cfg, name, rows, remote, year=str(datetime.now().year))
    payload = _set_payload(planned)
    # THE PLAN ITSELF, so the screen shows every item the digest covers (R-693).
    option = ctx.gate.require(ctx.entry.gates[0], plan=payload, context=_set_shown(planned))
    warnings = _unmatched_warnings(planned)
    if option != "apply" or not planned.writes:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

    done = sets.SetApplied()
    try:
        sets.apply_set(cfg, remote, planned, done)
    except Exception as exc:
        raise _set_failed(exc, done, planned) from exc
    if done.refused:
        warnings.append(
            {
                "code": "export-set-tracks-refused",
                "message": (
                    f"the provider would not add {len(done.refused)} matched track(s) "
                    f"to {planned.name}; they are recorded and not asked for again"
                ),
            }
        )
    # WHAT WAS WRITTEN RIDES ON THE TOTALS, since ``plan/1`` admits no other key.
    totals = {
        **payload["totals"],
        "applied": {
            "remote_id": done.remote_id,
            "created": done.created,
            "added": len(done.added),
            "refused": len(done.refused),
        },
    }
    return ctx.envelope(
        data={**payload, "totals": totals}, outcome=Outcome.OK, warnings=warnings
    )


# ── export archive ──────────────────────────────────────────────────────────


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
                "name": planned.year,
                "action": planned.folder_action,
            },
            {
                "id": planned.playlist.remote_id,
                "kind": "playlist",
                "name": planned.title if planned.title is not None else "",
                "built_as": planned.playlist.name,
                "to": planned.to,
                "move": planned.move,
                "action": sets.MARK if planned.mark else "skip",
                **({"reason": planned.left} if planned.left else {}),
            },
        ]
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {
            "count": len(items),
            "writes": bool(planned is not None and planned.writes),
        },
        "chunk": None,
    }


def _archive_shown(planned: sets.ArchivePlan | None, *, name: str, pass_name: str) -> dict[str, Any]:
    if planned is None:
        return {"set playlist": name, "nothing to archive": NOTHING_BUILT_SAID}
    folder = {
        sets.CREATE: "create it",
        sets.ADOPT: "use the one already on the account under this name",
        sets.REUSE: "use the one already recorded",
    }[planned.folder_action]
    if planned.left:
        title = f"left as {planned.title!r}, since " + (
            "its name already carries the prefix"
            if planned.left == sets.ALREADY_MARKED
            else f"it was retitled since it was made as {planned.playlist.name!r}"
        )
    elif planned.move:
        title = (
            f"{planned.playlist.name} -> {planned.to}, if its title in the folder is "
            f"still {planned.playlist.name!r} once it is there"
        )
    else:
        title = f"{planned.playlist.name} -> {planned.to}"
    shown: dict[str, Any] = {
        "set playlist": planned.playlist.name,
        "pass": pass_name,
        "folder": f"{planned.year}: {folder}",
        "place": (
            "put it in the folder" if planned.move else "already in the folder, left there"
        ),
        "title": title,
        "undone by": f"crate sync unmark --pass {pass_name}",
    }
    if planned.stale_folder:
        shown["recorded folder"] = (
            f"the folder recorded for {planned.year}, {planned.stale_folder}, is no "
            f"longer on the account, so its record is replaced"
        )
    if not planned.writes:
        shown["nothing to write"] = "the playlist is already in its folder and marked"
    return shown


def _archive_failed(exc: Exception, done: sets.ArchiveApplied, unrecorded: bool) -> CratekitError:
    """The failure, with what was already written named, on ``label mark``'s rule."""
    parts = []
    if done.folder_id:
        parts.append(f"the folder was {'created' if done.folder_created else 'in hand'}")
    if done.moved:
        parts.append("the playlist was put in it")
    if done.marked:
        parts.append(
            "the playlist was renamed and the mark record could not take it, so sync "
            "unmark will not find it and its prefix is taken off by hand"
            if unrecorded
            else "the playlist was renamed and recorded for sync unmark"
        )
    said = (
        "before this failed " + ", ".join(parts)
        if parts
        else "nothing was written before this failed"
    )
    detail = {
        "folder_id": done.folder_id,
        "folder_created": done.folder_created,
        "moved": done.moved,
        "marked": done.marked,
        "unrecorded": unrecorded,
    }
    again = "run crate export archive again; what was done is not done twice"
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{said}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.SOURCE,
            retryable=cause.retryable,
            origin=_ARCHIVE,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    if unrecorded:
        return refuse(
            "sync-mark-record-unusable",
            f"{said}. The record could not be written ({type(exc).__name__}: {exc})",
            steps=("make the library's state directory writable by this account", again),
            scope=Scope.SOURCE,
            origin=_ARCHIVE,
            detail={**detail, "kind": type(exc).__name__},
        )
    return refuse(
        "internal-error",
        f"{said}. The archive failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.SOURCE,
        origin=_ARCHIVE,
        detail={**detail, "kind": type(exc).__name__},
    )


def export_archive(ctx) -> Envelope:
    cfg = shell.load_config("export.set_cli")
    xml = Path(str(ctx.args.xml))
    pass_name = pass_name_of(xml)
    # THE PROOF FIRST, before the ledger, the account or a credential.
    marks.require_output(xml)
    name = set_name(ctx.args.name)
    playlist = ledger.set_playlist(cfg, name)
    planned: sets.ArchivePlan | None = None
    remote = None
    if playlist is not None:
        from cratekit.modules.outbound import account

        remote = account.resolve(cfg)
        planned = sets.plan_archive(
            cfg, playlist, remote, year=playlist.year or str(datetime.now().year)
        )
    payload = _archive_payload(planned, name=name, pass_name=pass_name)
    option = ctx.gate.require(
        ctx.entry.gates[0],
        plan=payload,
        context=_archive_shown(planned, name=name, pass_name=pass_name),
    )
    if planned is None or remote is None:
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[{"code": "export-archive-nothing-built", "message": f"{name}: {NOTHING_BUILT_SAID}"}],
        )
    if option != "apply" or not planned.writes:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)

    record = mark_record.MarkRecord(cfg)
    # THE RECORD IS LOCKABLE BEFORE ANYTHING IS WRITTEN, as ``sync mark`` asks.
    record.ready()
    done = sets.ArchiveApplied()
    unrecorded = [False]

    def keep(before: str, to: str) -> None:
        try:
            record.record_marked(pass_name, {planned.playlist.remote_id: (before, to)})
        except (CratekitError, OSError):
            unrecorded[0] = True
            raise

    try:
        sets.apply_archive(cfg, remote, planned, done, record=keep)
    except Exception as exc:
        raise _archive_failed(exc, done, unrecorded[0]) from exc

    warnings: list[dict[str, str]] = []
    if done.left and planned.mark:
        warnings.append(
            {
                "code": "export-archive-changed-since-plan",
                "message": (
                    f"{planned.playlist.name} was "
                    + {
                        sets.ALREADY_MARKED: "already marked when it was read in the folder",
                        sets.RETITLED: "retitled by somebody when it was read in the folder",
                    }.get(
                        done.left,
                        "not yet listed in the folder it was put in; archive it again "
                        "once the account lists it",
                    )
                    + ", so it was not renamed"
                ),
            }
        )
    totals = {
        **payload["totals"],
        "applied": {
            "folder_id": done.folder_id,
            "folder_created": done.folder_created,
            "moved": done.moved,
            "marked": done.marked,
        },
    }
    wrote = done.folder_created or done.moved or done.marked
    return ctx.envelope(
        data={**payload, "totals": totals},
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
        warnings=warnings,
    )


__all__ = [
    "build_archive",
    "build_set",
    "export_archive",
    "export_set",
    "match_rows",
    "name_of",
    "set_name",
]
