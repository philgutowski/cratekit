"""``sync.mark``: a landed sync pass marks the playlists it finished, behind one gate.

R-358's production half. A pass resolves each account playlist and acquires
nothing, ``intake missing --run`` lists what it found missing, ``acquire
download`` fetches that, and ``intake land`` writes one intake file. Only then
does an importable file exist, which is what ``sync/marks.py`` makes a rename
wait for. This verb is handed that file and is the one caller of
:func:`cratekit.sync.playlists.mark_swept`.

THE FILE NAMES THE PASS. ``intake missing --run`` names its list after the run,
``<run without colons>_synced``, and tells the person to land with that as
``--pass``, so the intake file is ``<name>_inboxed.xml`` while the batch folder
and playlist carry the date and the source (U110). Nothing here is told a run
identifier. The name is read off the intake file, and the pass's jobs are the
ones whose own run spells that name, which is a comparison in the direction the
name was built and never an attempt to put the colons back.

ONLY A FINISHED PLAYLIST IS MARKED, AND THE JOB'S OWN REPORTS SAY WHAT FINISHED
MEANS. Each playlist of the pass has one intake job, and that job committed one
report per track: owned, suppressed, offered or missing. Every track the pass
did not find, the offered and the missing, is resolved against the library
again NOW, by the view ``acquire match`` uses. A playlist is planned only when
its job SUCCEEDED and every such track is LANDED, the intake file names the
file, OWNED, the library holds it and the file does not name it, or SUPPRESSED,
somebody has since deleted it on purpose and the pass itself never owed a
suppressed track. One track outstanding leaves the playlist alone with the
track named.

NOT THE MANIFEST, which the brief named and ``/code-review`` showed cannot
carry the decision. The manifest beside the pass's list is derived from these
reports and drops two kinds of track on the way: one the pass OFFERED for
review, which is never listed for download, and one it handed on to the text
list because the provider gave it no id. A playlist holding either would have
had no row owed and been marked DOWNLOADED over a track that is not in the
library. A manifest can also be another pass's, and a pass whose every missing
track was handed on has none at all. The reports are per playlist, are written
once and are what the manifest was made from, so they are read instead and the
verb takes no manifest.

A FILE OF NO PASS IS A PLAN OF NOTHING, NOT A REFUSAL, on the precedent
``intake land`` set for an empty folder: no playlist job on this library spells
the file's name, so there is nothing this verb could ever rename from it. That
is decided before the account is listed or a credential is asked for, the empty
plan is still gated, and the run ends NO_OP under a warning that says why.

THE PLAN IS SHOWN BEFORE ANYTHING IS RENAMED, and what runs after the answer is
the engine's own recheck against a second listing, so a playlist retitled or
removed since the plan is skipped and said, never forced.

A FAILURE PART WAY NAMES WHAT WAS MARKED. Each rename is its own write to the
account. A refusal the account raised keeps its reason, anything else is this
build's own defect and says so, and either way the message and detail carry the
playlists already renamed, which stay renamed.

A DATABASE NATIVE INTAKE TREE WRITES NO INTAKE FILE (R-777), so there the
pass is named with ``--pass`` instead of ``--xml``. The pass's jobs are found
by that name exactly as by the file's, and every track the pass did not find is
resolved against the library the same way; with no file to say which landing
brought a track, each one the library holds is counted owned. The proof the
engine waits for is :class:`cratekit.sync.marks.NativeLanding`, made only after
the medium reads native, and the medium is read again before the first rename.
``--pass`` on a tree still on the bridge is refused naming ``--xml``, because
there the intake file is the proof and a pass named without it is unproven.

EVERY RENAME THAT LANDS IS RECORDED (R-838), under the pass, with the title
before and the title written, on the failure path as well. That record is what
``sync unmark`` reads to put a mistaken mark back, and the only thing it trusts
to say which pass wrote a prefix.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs, locations
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.intake import cli as intake_cli
from cratekit.intake import ingest, land_cli, landing, missing_cli, native
from cratekit.sync import cli as sync_cli
from cratekit.sync import mark_record, marks, playlists, sources
from cratekit.write import rbxml

_ORIGIN = ("sync.mark",)

#: What a planned item carries, and what the apply turns it into.
MARK = "mark"
MARKED = "marked"
SKIP = "skip"

#: Why a playlist of the pass is not planned, one word each.
ALREADY_MARKED = "already-marked"
NOT_LISTED = "not-listed"
JOB_UNFINISHED = "job-unfinished"
#: The pass's own word for the label batch's ` LIBRARY` debris, read through
#: the enum so the two verbs cannot spell it two ways (R-361). A job for one
#: reaches the pass only from before the rule or by hand, and the source
#: system's throwaway is never renamed under it.
LABEL_DEBRIS = str(playlists.Excluded.LABEL_DEBRIS)
REPORTS_UNREADABLE = "reports-unreadable"
ROWS_OUTSTANDING = "rows-outstanding"
#: Why a planned playlist was not renamed after all: the engine's recheck.
CHANGED_SINCE = "changed-since-plan"

#: The reasons that say the pass did not complete a playlist, so naming one
#: with ``--playlist`` is refused rather than shown as a skip (U174). The other
#: reasons are about the account or the name, not the pass, and stay skips.
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})

#: The gate screen's line naming a plan narrowed by ``--playlist``.
ONLY_SAID = "only the playlists named"

#: What the gate screen and the warning say about a file of no pass.
NO_PASS_SAID = (
    "no playlist job a sync pass queued on this library belongs to this file, so "
    "there is nothing to rename from it"
)

#: The three ways a track the pass did not find is no longer owed.
LANDED = "landed"
OWNED = "owned"
SUPPRESSED = "suppressed"

#: The report states that say the pass did not find the track in the library.
#: ``owned`` and ``suppressed`` are the other two, and neither was ever owed.
_NOT_FOUND = frozenset({"missing", "offered"})


def build_mark(parser, entry) -> None:
    del entry
    proof = parser.add_mutually_exclusive_group(required=True)
    proof.add_argument(
        "--xml",
        metavar="XML",
        help="the intake file crate intake land wrote for the sync pass",
    )
    proof.add_argument(
        "--pass",
        dest="pass_name",
        metavar="NAME",
        help=(
            "the sync pass to mark, by the name it was landed with, on a database "
            "native intake tree, which writes no intake file"
        ),
    )
    parser.add_argument(
        "--playlist",
        action="append",
        default=[],
        metavar="ID",
        help=(
            "mark only this playlist of the pass, by its account identifier; "
            "repeatable. A playlist the pass did not complete is refused by name"
        ),
    )
    parser.set_defaults(_handler=sync_mark)


def _blocked(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "sync-marks-blocked",
        message,
        steps=steps,
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail=detail,
    )


@dataclass
class _Playlist:
    """One playlist of the pass, and whether the landed file finishes it."""

    identity: str
    name: str
    job: jobs.Job
    wanted: tuple[match.Wanted, ...] = ()
    settled: dict[str, int] = field(
        default_factory=lambda: {LANDED: 0, OWNED: 0, SUPPRESSED: 0}
    )
    outstanding: list[dict[str, str]] = field(default_factory=list)
    reason: str | None = None
    why: str = ""

    @property
    def planned(self) -> bool:
        return self.reason is None


def _pass_name(xml: Path) -> str:
    """The name the pass's list and intake file share, read off the file.

    NOT THE BATCH'S since U110, which is named for the date and the source; a
    landing names only its intake file for the pass.
    """
    # RETIRED OR NOT (R-501). ``intake imported`` renames the file once the
    # import is proven, and a person who proved it before marking passes that
    # name. It is the same file and it names the same pass.
    written = land_cli.unretired_name(xml.name)
    if not written.endswith(land_cli.INTAKE_SUFFIX) or written == land_cli.INTAKE_SUFFIX:
        raise _blocked(
            f"{xml.name} is not named as an intake file, so it does not say which "
            f"sync pass it landed and nothing can be marked from it",
            f"pass the file ending in {land_cli.INTAKE_SUFFIX} that crate intake land wrote",
            path=str(xml),
        )
    return written[: -len(land_cli.INTAKE_SUFFIX)]


#: The pass name rule, public for ``label mark`` (R-835), so the two verbs that
#: read a pass off an intake file read it one way.
pass_name_of = _pass_name


def _comparable(path: str | Path) -> str:
    """A path as both sides spell it, THROUGH THE FILESYSTEM and then the form.

    Resolved first, which is what ``landing._file_labels`` does for the same
    question, because a library root reached through a link spells every landed
    file one way in the intake file and another in the index.
    """
    return locations.norm_for_compare(str(Path(path).resolve()))


def _locations(xml: Path) -> frozenset[str]:
    """Every local file the intake file names, comparable to a path off the disk."""
    try:
        content = xml.read_bytes()
    except OSError as exc:
        raise _blocked(
            f"{xml.name} could not be read ({exc.strerror or exc}), so what it landed "
            f"is unknown and nothing was marked",
            "write the importable file, then mark the remote side",
            path=str(xml),
        ) from exc
    named: set[str] = set()
    for track in rbxml.collection_tracks(content):
        recorded = rbxml.attributes(content, track).get("Location") or ""
        if not recorded:
            continue
        try:
            named.add(_comparable(locations.location_to_path(recorded)))
        except locations.LocationDecodeError:
            # A location on another host is not a file this landing put here,
            # so it is nothing a track could have landed as. Passed over, and
            # never a traceback out of a verb whose failures are refusals.
            continue
    if not named:
        raise _blocked(
            f"{xml.name} names no track on this machine, so it is not an intake file "
            f"a landing wrote and nothing was marked",
            f"pass the file ending in {land_cli.INTAKE_SUFFIX} that crate intake land wrote",
            path=str(xml),
        )
    return frozenset(named)


def _native_proof(cfg: config.Config, name: str) -> marks.NativeLanding:
    """The native proof for a pass named on the command line, or the refusal.

    THE MEDIUM IS ``ingest.intake_medium`` AND NO COPY OF IT (R-770), the one
    switch every verb that writes the intake tree reads.
    """
    if not landing.plain_name(name):
        raise _blocked(
            f"{name!r} is not a pass name a landing could have been given, so it names "
            f"no pass and nothing was marked",
            "pass the name crate intake missing --run told the landing to use as --pass",
            pass_name=name,
        )
    medium = ingest.intake_medium(cfg)
    if medium.declared is None:
        # AN UNREACHABLE ROOT DECIDES NOTHING, so it is not called the bridge.
        raise _blocked(
            f"the library root {cfg.library.root} could not be reached, so whether the "
            f"intake tree is database native cannot be read and nothing was marked",
            "mount the library volume, then run crate sync mark again",
            pass_name=name,
        )
    if not medium.native:
        raise _blocked(
            f"the intake tree is on the xml bridge, so the landing of {name!r} wrote an "
            f"intake file and that file is what proves the pass landed; nothing was marked",
            f"pass the file ending in {land_cli.INTAKE_SUFFIX} that crate intake land "
            f"wrote as --xml",
            pass_name=name,
        )
    landings = native.landings_of_pass(cfg, name)
    if not landings:
        raise _blocked(
            f"no landing of {name!r} into the database native intake tree committed, so "
            f"nothing proves the pass landed and nothing was marked",
            "land the pass with crate intake land --pass and the name crate intake missing "
            "--run gave, then mark it by that same name",
            pass_name=name,
        )
    return marks.NativeLanding(
        tree_id=medium.declared.intake.id, pass_name=name, landings=landings
    )


def native_passes(cfg: config.Config) -> tuple[str, ...]:
    """The passes a database native landing committed, for a caller that marks every pass.

    ``crate organize`` finds a pass on the bridge by its intake file and here by
    its native landing's record (R-915, U174). NONE ON A TREE READ AS THE
    BRIDGE, where the intake file is the proof and a pass named without it is
    refused by :func:`_native_proof`, so a record left from before a revert is
    not planned as a refusal on every run. A root that cannot be reached is not
    read as the bridge: its passes are returned, and each one's plan refuses
    with that reason, rather than the step vanishing.
    """
    medium = ingest.intake_medium(cfg)
    if medium.declared is not None and not medium.native:
        return ()
    return native.landed_passes(cfg)


def _pass_jobs(store, cfg: config.Config, name: str, handler_key: str) -> list[jobs.Job]:
    """The playlist jobs of the pass the intake file is named after, oldest first."""
    return sorted(
        (
            job
            for job in playlists.source_jobs(store, cfg, handler_key=handler_key)
            if missing_cli.in_pass(job, name)
        ),
        key=lambda job: (job.created, job.job_id),
    )


def _spelled(wanted: match.Wanted) -> str:
    return f"{wanted.artist} - {wanted.title}" + (f" ({wanted.version})" if wanted.version else "")


_WHY = {
    NOT_LISTED: "the account no longer lists it, so there is no name to prefix",
    ALREADY_MARKED: "its name already carries the prefix",
    LABEL_DEBRIS: (
        "its name is the source system's label run debris, which a sync never "
        "offers and never renames"
    ),
    JOB_UNFINISHED: "its intake job did not succeed, so its tracks were never all resolved",
}


def _decided(store, sweep: playlists.Sweep, found: list[jobs.Job]) -> list[_Playlist]:
    """Every playlist of the pass, with the cheap reasons decided and the rest's
    unfound tracks read off their reports. Nothing here walks the library."""
    listed = sweep.names()
    latest: dict[str, jobs.Job] = {}
    for job in found:
        identity = playlists.playlist_of(job)
        if identity:
            latest[identity] = job
    decided: list[_Playlist] = []
    for identity, job in latest.items():
        entry = _Playlist(identity=identity, name=listed.get(identity, ""), job=job)
        decided.append(entry)
        if not entry.name:
            entry.reason = NOT_LISTED
        elif playlists.is_swept_name(entry.name):
            entry.reason = ALREADY_MARKED
        elif playlists.is_library_debris(entry.name):
            entry.reason = LABEL_DEBRIS
        elif job.state is not jobs.JobState.SUCCEEDED:
            entry.reason = JOB_UNFINISHED
        if entry.reason is not None:
            entry.why = _WHY[entry.reason]
            continue
        try:
            reports = missing_cli.job_reports(store, job)
        except CratekitError as exc:
            # UNREAD IS NOT NOTHING OWED. A playlist whose reports cannot be
            # read is one this run cannot say is finished, so it is left alone.
            entry.reason = REPORTS_UNREADABLE
            entry.why = exc.cause.message
            continue
        entry.wanted = tuple(
            intake_cli.thawed(report["track"])
            for report in reports
            if report["state"] in _NOT_FOUND
        )
    return decided


def _settle(decided: list[_Playlist], named: frozenset[str], cfg: config.Config) -> None:
    """Resolve every track the pass did not find, against the library as it is now.

    THE LIBRARY IS WALKED ONLY WHEN SOMETHING ASKS. A second run over a pass
    that is wholly marked, or a pass whose every track was owned, has nothing
    to resolve, and the walk is every file on the music volume.

    THE VIEW IS ``acquire match``'s OWN, tombstones included, so a track is
    owned here by the rule that called it missing. A track that is close and not
    exact is OUTSTANDING, since whether that file is the record is a person's
    to say. The review store is NOT consulted, so a track somebody has since
    accepted through review still holds its playlist back, which is recorded as
    a residual and errs on the side of not renaming.
    """
    asking = [entry for entry in decided if entry.planned and entry.wanted]
    if not asking:
        return
    index, suppresses, identify = match_cli.library_view(cfg)
    for entry in asking:
        for wanted in entry.wanted:
            found = match.resolve_one(
                wanted, index, suppresses=suppresses, suppression_id=identify
            )
            if found.state is match.MatchState.MATCHED:
                held = {_comparable(path) for path in found.paths}
                entry.settled[LANDED if held & named else OWNED] += 1
            elif found.state is match.MatchState.SUPPRESSED:
                entry.settled[SUPPRESSED] += 1
            else:
                entry.outstanding.append(
                    {
                        "id": wanted.ref,
                        "track": _spelled(wanted),
                        "why": f"{found.state}, {found.why}",
                    }
                )
        if entry.outstanding:
            entry.reason = ROWS_OUTSTANDING
            entry.why = (
                f"{len(entry.outstanding)} track(s) the pass did not find are still not "
                f"in the library: "
                + "; ".join(f"{row['track']} ({row['why']})" for row in entry.outstanding)
            )


def _item(entry: _Playlist) -> dict[str, Any]:
    base: dict[str, Any] = {"id": entry.identity, "name": entry.name, "job_id": entry.job.job_id}
    if entry.planned:
        return {**base, "action": MARK, "to": playlists.SWEPT_PREFIX + entry.name, **entry.settled}
    return {
        **base,
        "action": SKIP,
        "reason": entry.reason,
        "why": entry.why,
        "outstanding": list(entry.outstanding),
    }


def _payload(
    decided: list[_Playlist],
    *,
    proof: Path | marks.NativeLanding,
    seen,
    named: tuple[str, ...] = (),
) -> dict[str, Any]:
    items = [_item(entry) for entry in decided]
    planned = sorted((item["id"], item["to"]) for item in items if item["action"] == MARK)
    if isinstance(proof, marks.NativeLanding):
        # NO FILE TO FINGERPRINT. The pass and the tree it landed on are what
        # the person was shown, and the marks themselves, which a track
        # landing since the plan moves.
        identity: dict[str, Any] = {
            "kind": "sync-mark",
            "pass": proof.pass_name,
            "tree": proof.tree_id,
            # THE LANDINGS THAT PROVE IT, so a second landing of the pass since
            # the plan is another plan, as a rewritten intake file is.
            "landings": list(proof.landings),
            "marks": planned,
        }
    else:
        identity = {
            "kind": "sync-mark",
            "xml": str(proof),
            # THE ONE STAT ``marks.require_output`` TOOK. A file rewritten since
            # the person was shown the plan is another landing, and its size
            # and time move with it.
            "xml_size": seen.st_size,
            "xml_mtime_ns": seen.st_mtime_ns,
            "marks": planned,
        }
    if named:
        # A NARROWED PLAN IS ANOTHER QUESTION (U174), so an answer to the
        # screen that named one playlist never carries out the whole pass's.
        # Left out when nothing is named, so the whole pass's digest is as it was.
        identity["only"] = sorted(named)
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {
            "count": len(items),
            MARK: sum(1 for item in items if item["action"] == MARK),
            SKIP: sum(1 for item in items if item["action"] == SKIP),
        },
        "chunk": None,
    }


def _shown(
    payload: dict[str, Any],
    *,
    proof: Path | marks.NativeLanding,
    named: tuple[str, ...] = (),
) -> dict[str, Any]:
    """What the gate screen puts in front of the person, one line per fact."""
    said = (
        {"pass": f"{proof.pass_name}, landed on the database native {proof.tree_id!r} tree"}
        if isinstance(proof, marks.NativeLanding)
        else {"intake file": str(proof)}
    )
    shown: dict[str, Any] = {
        **said,
        "renamed on the account": [
            f"{item['name']} -> {item['to']}"
            + (f" (sync unmark put this title back {item['put_back']})" if "put_back" in item else "")
            for item in payload["items"]
            if item["action"] == MARK
        ],
        "left alone": [
            f"{item['name'] or item['id']}: {item['why']}"
            for item in payload["items"]
            if item["action"] == SKIP
        ],
    }
    if named:
        shown[ONLY_SAID] = list(named)
    if not payload["items"]:
        shown["nothing to rename"] = NO_PASS_SAID
    return shown


def _failed_part_way(
    exc: Exception,
    landed: list[str],
    names: dict[str, str],
    planned: list[str],
    unrecorded: CratekitError | None = None,
) -> CratekitError:
    """The failure, with what was already marked named in it.

    A REFUSAL THE ACCOUNT RAISED KEEPS ITS REASON AND ITS REMEDY. The adapter
    turns its provider's failures into causes itself, so anything else arriving
    here is this build's own defect, and calling that a provider outage would
    send a person to retry against a bug.

    ``unrecorded`` is the mark record's own refusal when it could not take what
    landed. It is SAID beside the account's failure and never replaces it, so
    the reason, the remedy and what is still unmarked all survive.
    """
    marked = [names.get(identity, identity) for identity in landed]
    said = (
        f"{len(marked)} playlist(s) were marked before this failed and stay marked: "
        + ", ".join(marked)
        if marked
        else "no playlist was marked before this failed"
    )
    if unrecorded is not None:
        said += (
            f". The record crate sync unmark reads could not take them "
            f"({unrecorded.cause.message})"
        )
    detail = {
        "marked": list(landed),
        "unmarked": [identity for identity in planned if identity not in landed],
        "unrecorded": unrecorded is not None,
    }
    again = "run crate sync mark again; a marked playlist is skipped by its name"
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{said}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.SOURCE,
            retryable=cause.retryable,
            origin=_ORIGIN,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{said}. The mark step failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail={**detail, "kind": type(exc).__name__},
    )


def _remember(
    cfg: config.Config, name: str, landed: list[str], names: dict[str, str]
) -> CratekitError | None:
    """Record every rename that landed, under the pass, for ``sync unmark`` (R-838).

    ON THE FAILURE PATH TOO, since what landed before a refusal is on the
    account and is exactly what a person may want put back. RETURNS the refusal
    rather than raising it, so a caller already holding the account's failure
    can say both. The refusal names what was renamed, because those renames
    stand whether or not the record took them.
    """
    try:
        mark_record.MarkRecord(cfg).record_marked(
            name,
            {
                identity: (names[identity], playlists.SWEPT_PREFIX + names[identity])
                for identity in landed
            },
        )
    except (CratekitError, OSError) as exc:
        message = exc.cause.message if isinstance(exc, CratekitError) else str(exc)
        renamed = ", ".join(names.get(identity, identity) for identity in landed)
        failure = refuse(
            "sync-mark-record-unusable",
            f"{len(landed)} playlist(s) were renamed and stay renamed, {renamed}, and "
            f"the record crate sync unmark reads could not take them ({message})",
            steps=("repair the mark record; sync unmark cannot put these back until then",),
            scope=Scope.RUN,
            origin=_ORIGIN,
            detail={"marked": list(landed)},
            inner=exc.cause if isinstance(exc, CratekitError) else None,
        )
        failure.__cause__ = exc
        return failure
    return None


@dataclass
class PassPlan:
    """One intake file's pass, planned: what the gate is asked over and what applies.

    PUBLIC FOR ``crate organize`` (U112), which plans every landed pass through
    :func:`plan_pass` and applies an approved one through :func:`apply_pass`,
    so a pass is marked there by exactly this verb's body.
    """

    xml: Path | None
    name: str
    payload: dict[str, Any]
    decided: list[_Playlist] = field(default_factory=list)
    sweep: Any = None
    catalogue_found: Any = None
    #: What the engine waits for before a rename: the intake file, or on a
    #: database native intake tree the :class:`marks.NativeLanding` (R-777).
    native: marks.NativeLanding | None = None
    #: The playlists ``--playlist`` narrowed the plan to, or empty for the
    #: whole pass (U174).
    named: tuple[str, ...] = ()

    @property
    def proof(self) -> Path | marks.NativeLanding:
        return self.native if self.native is not None else self.xml

    @property
    def said(self) -> str:
        """The pass as a person names it, the file's name or the pass's."""
        return self.xml.name if self.xml is not None else self.name

    @property
    def of_a_pass(self) -> bool:
        """Whether any playlist job a sync pass queued belongs to the file."""
        return self.sweep is not None

    @property
    def planned(self) -> list[str]:
        return [entry.identity for entry in self.decided if entry.planned]


def plan_pass(
    cfg: config.Config,
    xml: Path | None = None,
    *,
    pass_name: str | None = None,
    listing=None,
    playlists_named: Sequence[str] = (),
) -> PassPlan:
    """Plan the marks one intake file's pass earns, reading the account only when it has one.

    ``listing`` IS FOR A CALLER PLANNING MANY PASSES (U112): a callable
    answering ``(catalogue, sweep)``, asked only for a file a pass owns, so
    one listing of the account serves every pass rather than one listing
    each. Absent, this pass lists the account itself, as the verb does.

    ``playlists_named`` NARROWS AND NEVER WIDENS (U174), ``sync unmark``'s
    rule: only those playlists of the pass are planned, shown and covered by
    the digest. One that is not the pass's is refused before the account is
    listed, since the pass's jobs alone say which playlists it holds, and one
    the pass did not complete is refused by name with its reason, rather than
    shown as a skip the person asked to be marked.
    """
    named = tuple(dict.fromkeys(str(one) for one in playlists_named))
    # THE FILE FIRST, before the account is listed or a credential is asked
    # for, by the same single read the engine makes again before it renames.
    # With no file, the native proof first, for the same reason (R-777).
    native: marks.NativeLanding | None = None
    if (xml is None) == (pass_name is None):
        raise _blocked(
            "a mark names its pass by exactly one of the intake file and the pass name, "
            "and this was given both or neither; nothing was marked",
            "pass --xml on an intake tree on the bridge, or --pass on a database native one",
        )
    if xml is not None:
        seen = marks.require_output(xml)
        name = _pass_name(xml)
        located = _locations(xml)
    else:
        native = _native_proof(cfg, pass_name)
        seen = None
        name = native.pass_name
        located = frozenset()
    proof: Path | marks.NativeLanding = native if native is not None else xml

    spec = next(one for one in sources.SPECS if one.source_id == playlists.SOURCE_ID)
    handler_key = str(spec.handler_key)
    with jobs.open_store() as store:
        found = _pass_jobs(store, cfg, name, handler_key)
    _refuse_strangers(named, found, name)
    if not found:
        # BEFORE THE LISTING AND THE CREDENTIAL. Neither can change the answer,
        # and a person with no session stored is owed "this file is no pass's"
        # rather than "log in" followed by it.
        return PassPlan(
            xml=xml,
            name=name,
            payload=_payload([], proof=proof, seen=seen, named=named),
            native=native,
            named=named,
        )

    if listing is None:
        catalogue_found, sweep = listed(cfg)
    else:
        catalogue_found, sweep = listing()
    with jobs.open_store() as store:
        decided = _decided(store, sweep, found)
    if named:
        # BEFORE THE LIBRARY IS WALKED, so naming one playlist settles that one.
        decided = [entry for entry in decided if entry.identity in named]
    _settle(decided, located, cfg)
    _refuse_unfinished(named, decided, name)

    # THE RECORD BEFORE THE GATE (R-838). One that cannot be read or locked
    # refuses now, while nothing is on the account, and not after renames it
    # then could not take. A playlist this pass marked and ``sync unmark`` put
    # back is planned again like any other, and the screen says so.
    put_back = {
        entry.playlist_id: entry.unmarked
        for entry in mark_record.MarkRecord(cfg).ready()
        if entry.pass_name == name and entry.unmarked
    }
    payload = _payload(decided, proof=proof, seen=seen, named=named)
    for item in payload["items"]:
        if item["action"] == MARK and item["id"] in put_back:
            item["put_back"] = put_back[item["id"]]
    return PassPlan(
        xml=xml,
        name=name,
        payload=payload,
        decided=decided,
        sweep=sweep,
        catalogue_found=catalogue_found,
        native=native,
        named=named,
    )


def _refuse_strangers(named: tuple[str, ...], found: list[jobs.Job], name: str) -> None:
    """Refuse a named playlist that is not one of the pass's, by its jobs alone."""
    if not named:
        return
    held = {playlists.playlist_of(job) for job in found}
    strangers = [identity for identity in named if identity not in held]
    if strangers:
        raise _blocked(
            f"pass {name} holds no playlist {', '.join(strangers)}, so it cannot "
            f"mark it; nothing was marked",
            "name only playlists of this pass, by the account identifier its plan "
            "shows, or leave --playlist out to mark the whole pass",
            not_of_pass=strangers,
            pass_name=name,
        )


def _refuse_unfinished(named: tuple[str, ...], decided: list[_Playlist], name: str) -> None:
    """Refuse a named playlist the pass did not complete, naming it and why."""
    if not named:
        return
    unfinished = [entry for entry in decided if entry.reason in UNFINISHED]
    if unfinished:
        raise _blocked(
            f"pass {name} did not complete "
            + "; ".join(f"{entry.name or entry.identity} ({entry.why})" for entry in unfinished)
            + ", so it is not marked; nothing was marked",
            "finish the playlist first, the remedy its reason names, then mark it again",
            not_complete=[entry.identity for entry in unfinished],
            reasons={entry.identity: entry.reason for entry in unfinished},
            pass_name=name,
        )


def listed(cfg: config.Config) -> tuple[Any, Any]:
    """The catalogue and the account's playlists as a mark reads them, listed once."""
    from cratekit.label import catalogue

    spec = next(one for one in sources.SPECS if one.source_id == playlists.SOURCE_ID)
    catalogue_found = catalogue.resolve(cfg)
    with jobs.open_store() as store:
        sweep = playlists.marking_sweep(
            store, cfg, catalogue_found, handler_key=str(spec.handler_key)
        )
    return catalogue_found, sweep


def shown(planned: PassPlan) -> dict[str, Any]:
    """The gate screen's facts for one planned pass."""
    return _shown(planned.payload, proof=planned.proof, named=planned.named)


def apply_pass(cfg: config.Config, planned: PassPlan) -> tuple[dict[str, Any], list[dict[str, str]], list[str]]:
    """Rename what the plan marks and record it, after the gate said apply.

    Returns the payload as applied, its warnings and the identifiers renamed.
    Raises naming what was marked when the account or the record fails.
    """
    from cratekit.modules.outbound import account

    if planned.native is not None:
        # THE MEDIUM AGAIN, before the first rename. A tree reverted to the
        # bridge since the plan has an intake file to wait for, and the native
        # proof would stand in for a file that should exist.
        if _native_proof(cfg, planned.name) != planned.native:
            raise _blocked(
                f"the intake tree or the landings of {planned.name!r} changed since the "
                f"plan was shown, so the answer does not cover them and nothing was marked",
                "run crate sync mark again and answer the new plan",
                pass_name=planned.name,
            )
    remote = account.resolve(cfg)
    landed: list[str] = []
    sweep = planned.sweep
    try:
        playlists.mark_swept(
            sweep,
            planned.catalogue_found,
            remote,
            local_output=planned.proof,
            applied=landed,
            only=frozenset(planned.planned),
        )
    except Exception as exc:
        unrecorded = _remember(cfg, planned.name, landed, sweep.names())
        raise _failed_part_way(exc, landed, sweep.names(), planned.planned, unrecorded) from exc
    unrecorded = _remember(cfg, planned.name, landed, sweep.names())
    if unrecorded is not None:
        raise unrecorded

    items: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    for item in planned.payload["items"]:
        if item["action"] != MARK:
            items.append(item)
        elif item["id"] in landed:
            items.append({**item, "action": MARKED})
        else:
            items.append(
                {
                    **item,
                    "action": SKIP,
                    "reason": CHANGED_SINCE,
                    "why": (
                        "the account lists it under another name, or not at all, "
                        "since the plan was shown, so it was not renamed"
                    ),
                }
            )
            warnings.append(
                {
                    "code": "sync-mark-changed-since-plan",
                    "message": f"{item['name']} changed on the account since the plan "
                    f"was shown and was not renamed",
                }
            )
    totals = {
        "count": len(items),
        MARKED: len(landed),
        SKIP: sum(1 for item in items if item["action"] == SKIP),
    }
    return {**planned.payload, "items": items, "totals": totals}, warnings, landed


def sync_mark(ctx) -> Envelope:
    cfg = sync_cli._load()
    xml = Path(ctx.args.xml) if ctx.args.xml is not None else None
    planned = plan_pass(
        cfg,
        xml,
        pass_name=ctx.args.pass_name,
        playlists_named=list(getattr(ctx.args, "playlist", None) or ()),
    )
    option = ctx.gate.require(
        ctx.entry.gates[0], digest=planned.payload["digest"], context=shown(planned)
    )
    if not planned.of_a_pass:
        return ctx.envelope(
            data=planned.payload,
            outcome=Outcome.NO_OP,
            warnings=[
                {"code": "sync-mark-no-pass", "message": f"{planned.said}: {NO_PASS_SAID}"}
            ],
        )
    if option != "apply" or not planned.planned:
        return ctx.envelope(data=planned.payload, outcome=Outcome.NO_OP)

    data, warnings, landed = apply_pass(cfg, planned)
    return ctx.envelope(
        data=data,
        outcome=Outcome.OK if landed else Outcome.NO_OP,
        warnings=warnings,
    )


__all__ = [
    "PassPlan",
    "apply_pass",
    "build_mark",
    "listed",
    "native_passes",
    "plan_pass",
    "shown",
    "sync_mark",
]
