"""``sync.mark``: a landed sync pass records the playlists it finished as taken, behind one gate.

SINCE U242 NO TITLE CHANGES. A finished playlist is held as taken in
:mod:`cratekit.sync.mark_record`; the account is only read. "Rename" below
names the rule, not a write. This verb is the one caller of
:func:`cratekit.sync.playlists.mark_swept`, handed the intake file a landing
wrote (R-358).

THE FILE NAMES THE PASS. The pass name is read off ``<name>_inboxed.xml``,
and the pass's jobs are those whose run spells that name (U110), compared in
the direction the name was built, never by putting the colons back.

ONLY A FINISHED PLAYLIST IS MARKED, AND THE JOB'S OWN REPORTS SAY WHAT FINISHED
MEANS. Every track the pass did not find (offered or missing) is resolved
against the library NOW by ``acquire match``'s view. A playlist is planned only
when its job SUCCEEDED and every such track is LANDED (named in the file),
OWNED, or SUPPRESSED; one outstanding track leaves it alone, named.

NOT THE MANIFEST, which drops offered tracks and tracks with no provider id,
so a playlist holding either would be marked over a track not in the library.
The per playlist reports are read instead.

A FILE OF NO PASS IS A PLAN OF NOTHING, NOT A REFUSAL, decided before the
account is listed, still gated, ending NO_OP with a warning.

The plan is shown first and the engine rechecks against a second listing, so
a playlist changed since is skipped and said. A FAILURE PART WAY NAMES WHAT WAS
MARKED, keeping an account or record refusal's reason; anything else is this
build's defect.

A DATABASE NATIVE INTAKE TREE WRITES NO INTAKE FILE (R-777), so the pass is
named with ``--pass``, each held track counts owned, and the proof is a
:class:`cratekit.sync.marks.NativeLanding`, made once the medium reads native
and read again before the first mark. ``--pass`` on the bridge is refused
naming ``--xml``.

EVERY MARK IS A TAKEN ENTRY UNDER THE PASS (U242), stamped with the time
``organize --only file`` reads a year from; ``sync unmark`` lets it go.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.cli.output import Envelope, digest_of, timestamp
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
#: The label batch debris word, read through the enum so both verbs spell it one way (R-361).
LABEL_DEBRIS = str(playlists.Excluded.LABEL_DEBRIS)
REPORTS_UNREADABLE = "reports-unreadable"
ROWS_OUTSTANDING = "rows-outstanding"
#: Why a planned playlist was not renamed after all: the engine's recheck.
CHANGED_SINCE = "changed-since-plan"

#: The reasons the pass did not complete a playlist, so naming one with
#: ``--playlist`` is refused rather than skipped (U174).
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})

#: The gate screen's line naming a plan narrowed by ``--playlist``.
ONLY_SAID = "only the playlists named"

#: What the gate screen and the warning say about a file of no pass.
NO_PASS_SAID = (
    "no playlist job a sync pass queued on this library belongs to this file, so "
    "there is nothing to record from it"
)

#: The three ways a track the pass did not find is no longer owed.
LANDED = "landed"
OWNED = "owned"
SUPPRESSED = "suppressed"

#: The report states saying the pass did not find the track; the others were never owed.
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
    return marks.blocked(_ORIGIN, message, *steps, **detail)


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
    """The name the pass's list and intake file share, read off the file (not the batch's, U110)."""
    # RETIRED OR NOT (R-501); a retired intake file names the same pass.
    written = land_cli.unretired_name(xml.name)
    if not written.endswith(land_cli.INTAKE_SUFFIX) or written == land_cli.INTAKE_SUFFIX:
        raise _blocked(
            f"{xml.name} is not named as an intake file, so it does not say which "
            f"sync pass it landed and nothing can be marked from it",
            f"pass the file ending in {land_cli.INTAKE_SUFFIX} that crate intake land wrote",
            path=str(xml),
        )
    return written[: -len(land_cli.INTAKE_SUFFIX)]


#: The pass name rule, public so ``label mark`` reads a pass the same way (R-835).
pass_name_of = _pass_name


def _comparable(path: str | Path) -> str:
    """A path as both sides spell it, THROUGH THE FILESYSTEM and then the form.

    Resolved first, since a root reached through a link spells files differently
    in the intake file and the index.
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
            # Another host's location is nothing this landing put here; passed over.
            continue
    if not named:
        raise _blocked(
            f"{xml.name} names no track on this machine, so it is not an intake file "
            f"a landing wrote and nothing was marked",
            f"pass the file ending in {land_cli.INTAKE_SUFFIX} that crate intake land wrote",
            path=str(xml),
        )
    return frozenset(named)


#: Where a sync pass's name comes from, as a native proof's refusal says it.
SYNC_PASS_NAMED = "the name crate intake missing --run gave"


def _native_proof(
    cfg: config.Config,
    name: str,
    *,
    verb: str = "crate sync mark",
    named: str = SYNC_PASS_NAMED,
) -> marks.NativeLanding:
    """The native proof for a pass named on the command line, or the refusal.

    THE MEDIUM IS ``ingest.intake_medium`` AND NO COPY OF IT (R-770). ``verb``
    and ``named`` word the refusal for the caller, ``label mark --pass``
    included (R-1056).
    """
    if not landing.plain_name(name):
        raise _blocked(
            f"{name!r} is not a pass name a landing could have been given, so it names "
            f"no pass and nothing was marked",
            f"pass {named} to the landing as --pass, and mark by that same name",
            pass_name=name,
        )
    medium = ingest.intake_medium(cfg)
    if medium.declared is None:
        # AN UNREACHABLE ROOT DECIDES NOTHING, so it is not called the bridge.
        raise _blocked(
            f"the library root {cfg.library.root} could not be reached, so whether the "
            f"intake tree is database native cannot be read and nothing was marked",
            f"mount the library volume, then run {verb} again",
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
            f"land the pass with crate intake land --pass and {named}, then run {verb} "
            f"--pass with that same name",
            pass_name=name,
        )
    return marks.NativeLanding(
        tree_id=medium.declared.intake.id, pass_name=name, landings=landings
    )


#: The native proof, public so ``label mark --pass`` proves a pass the same way (R-1056).
native_proof = _native_proof


def native_passes(cfg: config.Config) -> tuple[str, ...]:
    """The passes a database native landing committed, for a caller that marks every pass.

    NONE ON A TREE READ AS THE BRIDGE, so a record left from before a revert is
    not planned as a refusal on every run (R-915, U174). A ROOT THAT CANNOT BE
    REACHED IS REFUSED, NEVER READ AS NO PASS, or a caller would show a clean
    plan over passes it could not see.
    """
    medium = ingest.intake_medium(cfg)
    if medium.declared is None:
        raise _blocked(
            f"the library root {cfg.library.root} could not be reached, so the passes "
            f"its native landings committed cannot be read and none was planned",
            "mount the library volume, then plan the marks again",
        )
    if not medium.native:
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
    NOT_LISTED: "the account no longer lists it, so there is nothing to record",
    ALREADY_MARKED: "Cratekit already holds it as taken",
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
        elif playlists.is_taken(identity, entry.name, sweep.taken):
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
            # UNREAD IS NOT NOTHING OWED. The playlist is left alone.
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

    THE LIBRARY IS WALKED ONLY WHEN SOMETHING ASKS, since the walk is every
    file on the music volume.

    THE VIEW IS ``acquire match``'s OWN, tombstones included. A close but not
    exact track is OUTSTANDING, a person's to judge. The review store is NOT
    consulted, which errs on the side of not marking.
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
        return {**base, "action": MARK, **entry.settled}
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
    planned = sorted((item["id"], item["name"]) for item in items if item["action"] == MARK)
    if isinstance(proof, marks.NativeLanding):
        # NO FILE TO FINGERPRINT, so the pass, tree and marks are the identity.
        identity: dict[str, Any] = {
            "kind": "sync-mark",
            "pass": proof.pass_name,
            "tree": proof.tree_id,
            # THE LANDINGS THAT PROVE IT, so a later landing is another plan.
            "landings": list(proof.landings),
            "marks": planned,
        }
    else:
        identity = {
            "kind": "sync-mark",
            "xml": str(proof),
            # THE ONE STAT ``marks.require_output`` TOOK, so a rewritten file is another plan.
            "xml_size": seen.st_size,
            "xml_mtime_ns": seen.st_mtime_ns,
            "marks": planned,
        }
    if named:
        # A NARROWED PLAN IS ANOTHER QUESTION (U174); left out when nothing is
        # named, so the whole pass's digest is unchanged.
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
        "recorded as taken": [
            f"{item['name']}"
            + (f" (sync unmark let it go {item['put_back']})" if "put_back" in item else "")
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
        shown["nothing to record"] = NO_PASS_SAID
    shown["on the account"] = "nothing is renamed; the record is Cratekit's own"
    return shown


def _failed_part_way(
    exc: Exception,
    landed: list[str],
    names: dict[str, str],
    planned: list[str],
) -> CratekitError:
    """The failure, naming what was already taken.

    A REFUSAL THE ACCOUNT OR THE RECORD RAISED KEEPS ITS REASON AND ITS REMEDY;
    anything else is this build's own defect, never called a provider outage.
    """
    marked = [names.get(identity, identity) for identity in landed]
    said = (
        f"{len(marked)} playlist(s) were recorded as taken before this failed and "
        f"stay taken: " + ", ".join(marked)
        if marked
        else "no playlist was recorded as taken before this failed"
    )
    detail = {
        "marked": list(landed),
        "unmarked": [identity for identity in planned if identity not in landed],
    }
    again = "run crate sync mark again; a playlist already taken is skipped"
    if isinstance(exc, OSError):
        # THE RECORD COULD NOT BE WRITTEN, which since U242 is the mark itself.
        return refuse(
            "sync-mark-record-unusable",
            f"{said}. The record could not be written ({type(exc).__name__}: {exc})",
            steps=("make the library's state directory writable by this account", again),
            scope=Scope.RUN,
            origin=_ORIGIN,
            detail={**detail, "kind": type(exc).__name__},
        )
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


@dataclass
class PassPlan:
    """One intake file's pass, planned: what the gate is asked over and what applies.

    PUBLIC FOR ``crate organize`` (U112), so it marks a pass by this verb's body.
    """

    xml: Path | None
    name: str
    payload: dict[str, Any]
    decided: list[_Playlist] = field(default_factory=list)
    sweep: Any = None
    catalogue_found: Any = None
    #: The native proof the engine waits for in place of the intake file (R-777).
    native: marks.NativeLanding | None = None
    #: The playlists ``--playlist`` narrowed to, or empty for the whole pass (U174).
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

    ``listing`` IS FOR A CALLER PLANNING MANY PASSES (U112), a callable
    answering ``(catalogue, sweep)`` so one account listing serves them all.

    ``playlists_named`` NARROWS AND NEVER WIDENS (U174). One not of the pass is
    refused before the account is listed; one the pass did not complete is
    refused by name with its reason.
    """
    named = tuple(dict.fromkeys(str(one) for one in playlists_named))
    # THE FILE FIRST (or the native proof, R-777), before the account is listed.
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
        # BEFORE THE LISTING AND THE CREDENTIAL, which cannot change the answer.
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

    # THE RECORD BEFORE THE GATE (R-838), so an unusable one refuses now. A
    # playlist since put back or let go is planned again, and the screen says so.
    record = mark_record.MarkRecord(cfg)
    put_back = {
        entry.playlist_id: entry.unmarked
        for entry in record.ready()
        if entry.pass_name == name and entry.unmarked
    }
    put_back.update(
        {
            entry.playlist_id: entry.released
            for entry in record.taken().values()
            if entry.by == name and entry.released
        }
    )
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
            "name only playlists of this pass, by their account identifiers, which "
            "crate organize --report --only marks lists under each pass, or leave "
            "--playlist out to mark the whole pass",
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
    """Record what the plan marks as taken, after the gate said apply (U242).

    Returns the payload as applied, its warnings and the identifiers taken;
    raises naming what was taken. NOTHING IS WRITTEN TO THE ACCOUNT.
    """
    if planned.native is not None:
        # THE MEDIUM AGAIN, before the first mark, in case the tree reverted.
        if _native_proof(cfg, planned.name) != planned.native:
            raise _blocked(
                f"the intake tree or the landings of {planned.name!r} changed since the "
                f"plan was shown, so the answer does not cover them and nothing was marked",
                "run crate sync mark again and answer the new plan",
                pass_name=planned.name,
            )
    record = mark_record.MarkRecord(cfg)
    # THE RECORD IS LOCKABLE BEFORE THE FIRST MARK, so one that cannot be
    # written refuses while nothing is taken yet.
    record.ready()
    landed: list[str] = []
    sweep = planned.sweep

    def take(identity: str, name: str) -> None:
        record.take(
            [
                mark_record.Taken(
                    playlist_id=identity,
                    name=name,
                    by=planned.name,
                    how=mark_record.BY_PASS,
                    at=timestamp(),
                )
            ]
        )

    try:
        playlists.mark_swept(
            sweep,
            planned.catalogue_found,
            take,
            local_output=planned.proof,
            applied=landed,
            only=frozenset(planned.planned),
        )
    except Exception as exc:
        raise _failed_part_way(exc, landed, sweep.names(), planned.planned) from exc

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
                        "since the plan was shown, so it was not recorded as taken"
                    ),
                }
            )
            warnings.append(
                {
                    "code": "sync-mark-changed-since-plan",
                    "message": f"{item['name']} changed on the account since the plan "
                    f"was shown and was not recorded as taken",
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
    "PassPlan", "apply_pass", "build_mark", "listed", "native_passes", "plan_pass", "shown",
    "sync_mark"
]
