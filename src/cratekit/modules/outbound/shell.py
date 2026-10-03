"""What the two outbound verbs share, so a rule has one owner rather than two.

``crate export playlist`` and ``crate sync favorites`` differ in what they write
and in what an item is. They do NOT differ in how a queued job is resumed, how a
frozen configuration is loaded, or in what a person is warned about before they
confirm, and until this module existed each of those was written out twice.

**THE RESUME BRANCH IS THE ONE THAT MATTERED.** It carries the R-225 fix: a job
that half failed must exit with its own cause rather than through a normal
envelope, because a person whose export wrote nothing must not be told it
finished. Two copies of a fix is one copy that gets updated, and the predicate
itself is now ``jobs.raise_for_state``, the one mapping every shell calls. It is
also what added the parked job, which leaves as ``JobBlocked`` (R-290).
``master/cli.py`` had the unfixed shape when this module was written and calls
the same mapping now.

**WHAT IS DELIBERATELY NOT HERE.** ``confirm_digest`` stays one function per
shell, because the two verbs digest different key sets and a single digest
builder would have to branch on which verb called it. Each shell's ``summary``
stays its own, because the export engine reports an unmatched row as a mapping
and the hearts engine reports it as a string, and one function over both would
reintroduce the shape branch. Both are passed in rather than merged.

``ctx`` is untyped here for the reason every builder in this package takes an
untyped ``entry`` (KTD23): this is modules-ranked and ``cratekit.cli`` is above
it, so naming that type would be reaching upward.

Layer: modules.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping

from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound import account
from cratekit.modules.outbound.source import ExportAge, ResolvedPlaylist

#: The two payload keys both verbs freeze, spelled once. A key one shell reads
#: and the other spells differently is a resume that quietly does different work
#: from the run it continues, and the confirm digest is taken over both of them.
PLAYLIST = "playlist"
EXPORT = "export"

#: The resolved track identifiers this job will write, frozen so the confirm
#: digest can cover them.
#:
#: WITHOUT THIS THE DIGEST NAMED A FILE PATH RATHER THAN A WRITE SET. A person
#: confirmed an export of one crate, and if the document at that path was
#: regenerated before the approved invocation ran, a different set of tracks was
#: written to their streaming account under a decision that never described it.
#: A content hash of the document would also close it and is worse: it moves
#: whenever rekordbox re-exports anything, so an unrelated edit would force a
#: person to confirm again. The track set is what the write actually is.
TRACKS = "tracks"

#: The fact under which a gate screen names the export document's path (R-693).
#: NOT ``EXPORT``: :func:`shown_export` already shows a block under ``export``
#: with the document's name and age, and the resume, which may not read the
#: document, names the frozen path beside it rather than in its place.
EXPORT_PATH = "export path"

#: What an unmatched row is said to be when the account gave no reason for it,
#: spelled once for both verbs so the export and the sweep name the same
#: provider answer in the same words (R-850, R-856).
NO_MATCH = "the provider returned no track for it"


def unmatched_tally(outbound: Mapping[str, Any]) -> tuple[int, int] | None:
    """How many rows a finished job left unmatched, and of how many, or none.

    THE ARITHMETIC BOTH ``concluded`` HOOKS SHARE, so neither verb can count the
    same condition differently: ``None`` when the summary does not count or
    matched everything, otherwise the unmatched count and the sum of every
    count the summary carries. A bool is not a count, though Python calls it an
    int, so one is read as absent rather than as one.
    """
    counts = outbound.get("counts")
    if not isinstance(counts, Mapping):
        return None
    missed = counts.get("unmatched")
    if not _whole(missed) or missed <= 0:
        return None
    return missed, sum(n for n in counts.values() if _whole(n))


def _whole(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def load_config(origin: str) -> config.Config:
    """The current configuration, or the refusal a person can act on.

    ``origin`` names the shell for the cause, which is the only thing that
    differed between the two copies this replaces.

    THE SAME BODY EXISTS IN ``master/cli.py`` AND ``backup/cli.py`` and is NOT
    consolidated with them here. Those are other units' files and the shared home
    for all four would be ``core.config``, which is a wider change than this unit
    owns. R-232, rather than silently left at four copies.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=(origin,),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def reported(
    store,
    job,
    cfg: config.Config,
    summary: Callable[[config.Config, str], Mapping[str, Any]],
) -> dict[str, Any]:
    """One queued job, flattened for the envelope, with what it actually wrote.

    ``summary`` is a parameter rather than a branch because the two verbs report
    different sets: added, already and unmatched for an export; hearted, already
    and unmatched for a sweep.
    """
    # UNDER ``progress``, NOT BESIDE IT. The registry declares both verbs as
    # ``job_state/1`` and ``cli.output`` closes that surface with
    # ``additionalProperties: false``, so a top level ``outbound`` key is an
    # UNDECLARED FIELD and a consumer generated from the committed schema rejects
    # every envelope these two verbs emit. Nothing in the suite noticed, because
    # the schema fingerprint hashes the DECLARED fields rather than an emitted
    # payload. ``progress`` is declared ``object`` with no inner constraint,
    # which is where a per verb detail belongs.
    #
    # A ``job_state/2`` bump would be the wrong lever: ``_PAYLOAD_FIELDS`` has no
    # optional entries, so declaring ``outbound`` would make it REQUIRED of
    # ``master``, ``backup.run`` and every other job_state verb, none of which
    # has one.
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": {
            **jobs.progress(store, job.job_id),
            "outbound": dict(summary(cfg, job.job_id)),
        },
    }


#: The four things :func:`shown_export` can say about an export's date, spelled once.
#: WORDS RATHER THAN A BOOLEAN, because only one of the four means recent and the
#: human renderer prints a missing boolean as "none", which reads as "not stale".
AGE_STALE = "stale"
AGE_WITHIN_LIMIT = "within-limit"
AGE_FUTURE_DATED = "future-dated"
AGE_UNKNOWN = "unknown"


def freshness(age: ExportAge) -> str:
    """Which of the four an age is. The two that cannot be judged are asked FIRST."""
    if not age.known:
        return AGE_UNKNOWN
    if age.future_dated:
        return AGE_FUTURE_DATED
    return AGE_STALE if age.stale else AGE_WITHIN_LIMIT


def _local_date(moment) -> str:
    """The date as the person's own machine spells it.

    LOCAL, NOT UTC, on the one surface where it matters. A person compares this
    with their memory of when they exported and with the date Finder shows, and
    an evening export west of Greenwich is the next day in UTC.
    """
    return moment.astimezone().date().isoformat()


def _spelled(age: ExportAge) -> str | None:
    """The age in days and hours, so "past seven days" never reads as seven.

    Staleness is judged on the duration and whole days are floored, so an export
    seven days and five hours old printed as "7 day(s) ago, which is past the 7
    day(s)" allowed. The hours are what make that sentence true.
    """
    elapsed = age.age
    if elapsed is None:
        return None
    hours = elapsed.seconds // 3600
    return f"{elapsed.days} days {hours} hours"


def shown_export(age: ExportAge) -> dict[str, Any]:
    """What the confirm gate shows about the document the write is read from.

    NAMED FOR WHAT IT SHOWS. ``intake.candidates.shown`` is already a public
    function about something else, and one symbol meaning two things in two
    modules is a defect ``docs/METHOD.md`` says to hunt once a suite is green.

    SHOWN EVERY TIME, fresh or not (R-227). A plan that named the date only when
    it was old would make a missing line mean "recent", and the person deciding
    is the only one who knows whether their library moved since that date.

    THE WARNING'S SENTENCE RIDES HERE AS WELL AS ON THE ENVELOPE. A refusal
    carries no warnings, so on the envelope alone the advice to export again
    reached a person only after they had confirmed and the write was queued,
    which is the one moment it is no use. ``warning`` is absent when there is
    nothing to warn of, and ``freshness`` is always present, so the absence is
    never the only thing saying the date is fine.

    IT IS A DISPLAY VALUE AND IS NOT IN THE CONFIRM DIGEST, deliberately. The
    digest covers the track set, which is what the write is. An age in the
    digest would stale every recorded decision at midnight.
    """
    export: dict[str, Any] = {
        "file": age.path.name,
        "written": (
            age.written.astimezone().replace(microsecond=0).isoformat()
            if age.written is not None
            else None
        ),
        "age": _spelled(age),
        "age_days": age.age_days,
        "stale_after_days": age.limit_days,
        "freshness": freshness(age),
    }
    for warning in age_warnings(age):
        export["warning"] = warning["message"]
    return {"export": export}


def age_warnings(age: ExportAge) -> tuple[dict[str, str], ...]:
    """The sentence a person reads when the export is old, or its age unreadable.

    A WARNING AND NEVER A REFUSAL. Somebody who has not touched their library in
    a month has a month old export that is exactly right, and only they know
    that. The date is called "last written" rather than "exported" because it is
    the file's modification time, which is all a rekordbox export offers.

    AT MOST ONE, which :func:`shown_export` relies on to carry it as a single sentence.
    """
    written = age.written
    if written is None:
        return (
            {
                "code": "outbound-export-age-unknown",
                "message": (
                    f"the date {age.path.name} was last written could not be "
                    f"read, so nothing here can say whether it still describes "
                    f"the library"
                ),
            },
        )
    if age.future_dated:
        return (
            {
                "code": "outbound-export-age-unknown",
                "message": (
                    f"{age.path.name} is dated {_local_date(written)}, which is "
                    f"in the future, so its age cannot be judged and nothing "
                    f"here can say whether it still describes the library. "
                    f"Export the collection again if it may have moved"
                ),
            },
        )
    if age.stale:
        return (
            {
                "code": "outbound-export-stale",
                "message": (
                    f"{age.path.name} was last written on "
                    f"{_local_date(written)}, {_spelled(age)} ago, which is "
                    f"past the {age.limit_days} days "
                    f"outbound.export_stale_days allows. Anything the library "
                    f"gained or lost since then is not in this write. Export "
                    f"the collection again if it has moved"
                ),
            },
        )
    return ()


def queue_warnings(
    resolved: ResolvedPlaylist, *, noun: str, age: ExportAge
) -> tuple[dict[str, str], ...]:
    """What the person should know at the moment they are asked to confirm.

    ``age`` IS REQUIRED, never defaulted. Three shells queue an outbound write,
    and a default would let the next one leave the export's age out with nothing
    failing, which is R-227 coming back through a new caller.

    THE UNBOUND PROVIDER WARNING IS HERE RATHER THAN AT THE REFUSAL, and that is
    the honest half of deferring the refusal to the worker. Deferring is right
    for an input that can appear between queueing and running, which is the case
    ``master`` argues for a recording that may exist later. A missing adapter
    cannot appear later without a new build, so a person who is only told at
    drive time was told at the one moment they could do nothing with it.

    The dangling and repeated rows are reported rather than dropped for the
    reason ``source.resolve`` collects them: somebody whose export is short a
    track needs to know which one, and a count alone is not something to act on.
    """
    warnings: list[dict[str, str]] = [*age_warnings(age)]
    if not account.bound():
        warnings.append(
            {
                "code": "outbound-account-unbound",
                "message": (
                    "this build has no streaming provider adapter, so this job "
                    "will queue and then fail at the provider seam"
                ),
            }
        )
    if resolved.dangling:
        warnings.append(
            {
                "code": "playlist-track-missing",
                "message": (
                    f"{len(resolved.dangling)} {noun}(s) this playlist names are "
                    f"not in the export's collection and are not queued: "
                    f"{', '.join(resolved.dangling)}"
                ),
            }
        )
    if resolved.repeated:
        warnings.append(
            {
                "code": "playlist-track-repeated",
                "message": (
                    f"{len(resolved.repeated)} {noun}(s) appear more than once in "
                    f"this playlist and are queued once: "
                    f"{', '.join(resolved.repeated)}"
                ),
            }
        )
    return tuple(warnings)


def declined(job_id: str = "") -> dict[str, Any]:
    """The payload for a confirmation somebody answered with abort.

    IT IS THE DECLARED ``job_state`` SHAPE, not a bespoke summary. Both verbs
    emitted ``{"job_id": ..., "summary": {"queued": False}}``, which carries none
    of the four fields ``cli.output`` requires of that surface and two it forbids,
    so a consumer generated from the committed schema rejected the envelope. The
    outcome is already ``no-op``, so the summary field said nothing the envelope
    did not.

    ``cratekit.adopt.apply_cli`` set this convention on main and its version
    passes ``job_id: None``, which fails the same validator for a different
    reason. That verb is another unit's file, so the corrected shape lands here
    and the divergence is R-234 rather than something reached across.
    """
    return {"job_id": job_id, "state": "declined", "cause": None, "progress": {}}


def resume(
    ctx,
    spec,
    job_id: str,
    *,
    digest: Callable[..., str],
    summary: Callable[[config.Config, str], Mapping[str, Any]],
    standing: tuple[dict[str, str], ...] = (),
    frozen_extra: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None = None,
    concluded: Callable[[Mapping[str, Any]], tuple[dict[str, str], ...]] | None = None,
):
    """Answer the gate from the frozen payload, then drive the job's items.

    ``standing`` IS WHAT IS TRUE OF EVERY PASS OF THE CALLING VERB, as against
    the warnings a run produces. ``sync.favorites`` carries one (R-424): the
    sweep writes nothing in the library, and the default renderer prints a
    verb's warnings and nothing of its payload, so a standing sentence is the
    only way that fact reaches a person who did not ask for json. A verb with
    nothing standing to say passes nothing and reports exactly what it did.

    THIS BRANCH READS NOTHING FROM THE EXPORT DOCUMENT. The job's items are
    already in the queue and its identity is already frozen, so re-deriving here
    would make a resume refuse over a file the person has since moved, and would
    let a regenerated document silently change what a confirmed job does.

    THE DIGEST COMES OFF THE PAYLOAD for the same reason and for one more: the
    child ``jobs.spawn`` starts rebuilds its command line from that payload, so
    the two sides of the comparison have to be built from the same values or the
    job meets ``DecisionStale`` on every respawn.

    ``frozen_extra`` IS FOR A SHELL WHOSE DIGEST COVERS MORE THAN THE THREE
    SHARED KEYS. It is handed the frozen payload and returns keyword arguments
    for ``digest``, so what one verb adds to its digest is read off the payload
    here, where the payload is, and the other verb's digest is untouched.

    ``concluded`` IS WHAT A FINISHED RUN SAYS, as against ``standing``. It is
    handed the job's own summary, the one the envelope carries, after the job
    is driven, and returns warnings for what that summary shows (R-850). Handed
    the summary rather than reading the artifacts itself, so the warning and
    the counts beside it are one reading of the disk and cannot disagree.

    RECONCILE BEFORE DRIVING. A resume arrives after something stopped, and a
    claim left behind by a driver that died is state the queue cannot see for
    itself.

    IT RAISES ON A FAILED JOB RATHER THAN REPORTING ONE. That is R-225: a resume
    branch that returns a normal envelope for a job that half failed exits OK, so
    a person whose work did not happen is told it finished. U50 fixed it for
    ``backup.run`` by re-raising the job's own cause, and since R-290 that fix
    has one owner for every queued verb, ``jobs.raise_for_state``, which also
    refuses a PARKED job the copied predicate could not see.
    """
    with jobs.open_store() as store:
        queued = jobs.get(store, job_id)
        payload = queued.payload or {}
        playlist = str(payload.get(PLAYLIST) or "")
        exported = str(payload.get(EXPORT) or "")
        tracks = [str(track) for track in payload.get(TRACKS) or ()]
        extra = dict(frozen_extra(payload)) if frozen_extra is not None else {}
        # THE FROZEN PLAN IS SHOWN THROUGH THE GATE LAYER (R-693): every
        # track the digest covers, with the playlist, the export path and any
        # extra the digest was taken over in front of them. Nothing here is
        # read from the export document, for the reason above.
        option = ctx.gate.require(
            spec,
            plan={"digest": digest(playlist, exported, tracks, **extra), "items": tracks},
            context={PLAYLIST: playlist, EXPORT_PATH: exported, **extra},
        )
        if option == "abort":
            return ctx.envelope(data=declined(queued.job_id), outcome=Outcome.NO_OP)
        frozen = jobs.frozen_config(queued)
        job = jobs.reconcile(store, job_id)
        warnings: tuple[dict[str, str], ...] = ()
        if job.is_open():
            # A JOB WITH NO ITEMS DRIVES STRAIGHT TO SUCCEEDED, by design:
            # ``core.jobs`` treats attempting nothing as a genuine no-op so an
            # up-to-date source does not look broken. Neither verb can queue one
            # now, but a job frozen by a build BEFORE this one carries no items
            # at all, and driving it would report a clean success over an export
            # that never happened. ``backup/cli.py`` refuses the same shape for
            # the same reason.
            if not jobs.items(store, job.job_id):
                raise refuse(
                    "internal-error",
                    f"job {job.job_id} has no items to run, so driving it would "
                    f"report a success over work it never did. It was queued by "
                    f"a build that did not record what its items were",
                    remedy=Remedy.REPORT_DEFECT,
                    origin=("outbound", "shell"),
                    detail={"job_id": job.job_id},
                )
            _, warnings = ctx.run_job(store, job)
            job = jobs.get(store, job.job_id)
        # ANY CLOSED JOB CARRYING A CAUSE, not FAILED alone. A run stopped with
        # a signal is CANCELLED rather than FAILED, and it carries the cause
        # ``jobs.cancel`` builds, so the narrower predicate reported an
        # interrupted export through a normal envelope and exited OK: driven on
        # 2026-09-02 as exit 0 over a job with 0 of 3 items done and one track
        # already on the remote playlist. SUCCEEDED carries no cause, so it is
        # unaffected. ``backup/cli.py`` already uses this predicate.
        jobs.raise_for_state(job)
        data = reported(store, job, frozen, summary)
        said = concluded(data["progress"]["outbound"]) if concluded is not None else ()
        return ctx.envelope(
            data=data,
            # THE STANDING ONES FIRST, because they are true whether or not the
            # run produced any of its own, and a person scanning a long report
            # should not have to reach the end to learn what the verb cannot do.
            warnings=(*standing, *warnings, *said),
        )


__all__ = [
    "EXPORT",
    "EXPORT_PATH",
    "NO_MATCH",
    "PLAYLIST",
    "TRACKS",
    "age_warnings",
    "freshness",
    "load_config",
    "queue_warnings",
    "reported",
    "resume",
    "shown_export",
    "unmatched_tally",
]
