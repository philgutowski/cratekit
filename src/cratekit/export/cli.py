"""``crate export playlist``: confirm, then queue the outbound write, then run it.

Builders take an untyped ``entry`` so this file does not import the CLI
registry (KTD23). Long-running work queues a job, and since U51 this shell also
DRIVES one: ``handle`` below is the per item worker behind the ``export.playlist``
handler key, and it is the first caller in ``src`` of
``cratekit.modules.outbound.export``'s ``plan`` and ``apply``.

**TWO MODULES HERE ARE CALLED ``export`` AND THEY ARE ALIASED FOR IT.**
``outbound_export`` writes the remote playlist; ``source`` reads the local one
out of a rekordbox collection export. This file is a third thing called export.
The aliases are not decoration: one symbol meaning two things in two modules is
the defect ``docs/METHOD.md`` says to hunt once the suite is green, and this file
is where three of them meet.

**WHAT AN ITEM IS, AND WHY IT IS NOT THE PLAYLIST.** One item is one track. A job
whose single item is the whole playlist would redo every track when one write
failed, which throws away the engine's resume guarantee, and it could never be
empty however empty the playlist was, which throws away the zero item rule. The
cost of the per item shape is that the collection document is read once per item;
``modules.outbound.source`` memoizes it per process for exactly that reason.

**THE CONFIRM DIGEST COVERS THE EXPORT DOCUMENT, NOT JUST THE NAME.** R34 makes
this gate answerable only by a separate act recorded against a run, so the
decision is taken in one invocation and read in another. Digesting only the
playlist name would let a decision recorded against one collection document
authorise a queue built from a different one, with a different track set, written
to somebody's streaming account. Digesting what the person TYPED is the opposite
failure: the resumed child rebuilds its command line from the frozen payload, so
a relative path typed once would never match again and the job would meet
``DecisionStale`` on every respawn. So the digest is taken over the RESOLVED
playlist key and the ABSOLUTE export path, which both invocations and the resume
all produce identically.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs
from cratekit.core.cause import Outcome, refuse
from cratekit.modules.outbound import account, artifacts, ledger, shell, source
from cratekit.modules.outbound import export as outbound_export

#: The two payload keys both outbound verbs freeze, spelled once in
#: :mod:`cratekit.modules.outbound.shell` because the shared resume branch reads
#: them to rebuild the confirm digest. A key one shell spells differently is a
#: resume that quietly does different work from the run it continues.
PLAYLIST = shell.PLAYLIST
EXPORT = shell.EXPORT

#: The remote playlist's display name, frozen so the worker never rebuilds it by
#: splitting the key. Two name builders for one remote playlist is how it comes
#: to be created under a name nobody chose.
NAME = "name"

#: The recorded ledger key this crate used to live under, frozen when the verb
#: recognised one and a person confirmed it (R-229). Empty or absent means none,
#: and a job frozen before this key existed carries none, which reads the same.
ADOPTS = "adopts"

#: The remote playlist the gate showed this write landing on, or none when it
#: showed a create. It is the one stable identifier an outbound job has, and the
#: worker finds the ledger record by it when the record has moved to the crate's
#: new path since the job was confirmed.
REMOTE = "remote_id"

#: What the confirm gate says the write will do to the account's playlists.
ACTION_CREATE = "create"
ACTION_UPDATE = "update"
ACTION_ADOPT = "adopt"


#: What an unmatched row is said to be when the account gave no reason for it.
#: The engine records the slug ``unmatched`` for that row, which is a key to
#: grep the artifacts for and not a sentence a person can act on (R-850).
#: Spelled in the shell, which the favourites sweep shares.
NO_MATCH = shell.NO_MATCH

#: The warning a finished export carries when any of its tracks went unwritten.
UNMATCHED_WARNING = "export-tracks-unmatched"


def summary(cfg: config.Config, job_id: str) -> dict[str, Any]:
    """What this job's committed artifacts say it wrote, in one summary.

    DERIVED FROM WHAT RAN, NOT FROM WHAT WAS PLANNED. The engine reports the
    tracks it could not match, and until this function existed the only place
    that report reached was a JSON file under the queue root that no verb read.
    A person exporting thirty tracks against a provider that matched one of them
    would have seen thirty of thirty items done and been told nothing, which is
    METHOD's named cost of a clean report over state the tool could not read.

    READ OFF DISK RATHER THAN ACCUMULATED, because a job driven over two sessions
    has some of its reports in this process and all of them on the filesystem,
    and the person asking what the export did means all of them.

    COUNTED PER ITEM, AND EVERY UNMATCHED TRACK LISTED (R-850). The lists above
    were in the envelope and nowhere a person reads, so a live export of eight
    tracks answered ``ok`` and ``8 of 8 settled`` over a playlist holding four.
    ``counts`` is what was written, what was already there or written before
    and what was left out, and ``unmatched_tracks`` names each one left out with its reason,
    including a row the account said nothing about, which ``reasons`` omits.
    One item writes one track, so each report adds one to exactly one count, and
    an item is one committed file whichever run settled it, so a resumed job is
    counted across both runs and nothing in it twice.
    """
    added: list[str] = []
    already: list[str] = []
    unmatched: list[str] = []
    reasons: list[str] = []
    left_out: list[dict[str, str]] = []
    for report in artifacts.committed(cfg, job_id):
        added.extend(str(item) for item in report.get("added") or ())
        already.extend(str(item) for item in report.get("already") or ())
        for item in report.get("unmatched") or ():
            # THE IDENTITY, NOT THE ROW. An unmatched entry is a mapping carrying
            # the library identity, the title and the artist, because a person
            # reading the ARTIFACT needs a name to recognise. Stringifying the
            # mapping here put a Python dict repr in a JSON envelope, which is a
            # value nothing downstream can key on. Measured by the first drive of
            # this summary. ONE ROW BUILT ONCE, and the identity list and the
            # reason sentences read off it, so the three cannot disagree.
            listed = _left_out(item)
            left_out.append(listed)
            unmatched.append(listed["identity"])
            # WHAT THE ACCOUNT SAID ABOUT A ROW IT WOULD NOT CHOOSE FOR (R-356),
            # one sentence per row and only for a row it said something about. A
            # row the provider has three releases of and a row it has never heard
            # of are both unmatched, and only the first is something a person can
            # act on. NAMED AS THE LIBRARY SHOWS THE ROW, since nobody finds a
            # track by its row number.
            if _said(item):
                reasons.append(
                    f"{listed['artist']} - {listed['title']} "
                    f"(row {listed['identity']}): {listed['reason']}"
                )
    return {
        "added": added,
        "already": already,
        "unmatched": unmatched,
        "reasons": reasons,
        "counts": {
            "written": len(added),
            "already": len(already),
            "unmatched": len(unmatched),
        },
        "unmatched_tracks": left_out,
    }


def _said(row: Any) -> str:
    """What the account said about one unmatched row, or empty when nothing."""
    said = str(row.get("reason") or "") if isinstance(row, dict) else ""
    return "" if said == "unmatched" else said


def _left_out(row: Any) -> dict[str, str]:
    """One unmatched row as the answer lists it, named as the library shows it."""
    named = row if isinstance(row, dict) else {}
    return {
        "identity": _identity(row),
        "artist": str(named.get("artist") or ""),
        "title": str(named.get("title") or ""),
        "reason": _said(row) or NO_MATCH,
    }


def concluded(outbound: Mapping[str, Any]) -> tuple[dict[str, str], ...]:
    """The warning a finished export carries when it left tracks out, or none.

    THE OUTCOME STAYS ``ok`` AND THIS IS WHAT STOPS IT BEING A BARE ONE (R-850).
    ``ok`` with a warning is what the other job verbs answer for a partial
    result: ``sync`` says ``ok`` with ``sync-source-not-queued`` when one source
    refused, and the intake jobs say ``ok`` with a ``missing`` count. The outcome
    vocabulary has no partial word. Every outcome but ``ok`` and ``no_op`` must
    carry a cause and a non zero exit, which would make a job that finished every
    item and has nothing to retry read as failed, and ``pending`` needs a human
    action with a verb that verifies it, which nothing here has. The warning is
    the line a script reading only the outcome and the warnings can key on.
    """
    tally = shell.unmatched_tally(outbound)
    if tally is None:
        return ()
    missed, total = tally
    # "WERE NOT WRITTEN", NOT "ARE NOT ON THE PLAYLIST". A track counted as
    # already there may be counted so off the ledger rather than the account
    # (R-855), so the missing set on the account can be larger than this one,
    # and only what the provider could not match is this warning's to state.
    return (
        {
            "code": UNMATCHED_WARNING,
            "message": (
                f"{missed} of the {total} track(s) in this export were not written "
                f"to the remote playlist, because the provider could not match "
                f"them; each is listed with its reason in this answer"
            ),
        },
    )


def _identity(row: Any) -> str:
    """The library identity of one unmatched row, however the report spelled it."""
    if isinstance(row, dict):
        return str(row.get("identity") or "")
    return str(row)


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument("playlist", help="stable identifier of the library playlist")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the export already queued under this identifier",
    )
    parser.add_argument(
        "--export",
        default=None,
        metavar="EXPORT",
        help=(
            "the rekordbox collection export holding the playlist to write; the "
            "live database is never read"
        ),
    )
    parser.add_argument(
        "--new-playlist",
        action="store_true",
        default=False,
        help=(
            "create a new remote playlist even when a recorded one looks like "
            "this playlist under an earlier name or folder"
        ),
    )
    parser.set_defaults(_handler=export_playlist)


def confirm_digest(
    playlist_key: str,
    export_path: str,
    tracks: list[str] | tuple[str, ...],
    *,
    adopts: str = "",
) -> str:
    """The identity the confirm decision is recorded against.

    ONE FUNCTION RATHER THAN TWO CALL SITES SPELLING A DICT, because the enqueue
    path builds it from a freshly resolved playlist and the resume path builds it
    from the frozen payload, and the whole point is that those two produce the
    same string. Two literals would be two chances to disagree, and the symptom
    would be a confirmed job that refuses its own resume for ever.

    ``adopts`` IS IN THE DIGEST, BECAUSE IT CHANGES WHERE THE TRACKS GO (R-229).
    The decision is recorded in one invocation and the queue is built in another,
    and the ledger can change between them, so a confirmation shown "updates the
    playlist recorded for X" must not authorise a queue that creates a new one,
    or the reverse. IT JOINS ONLY WHEN SET, so an export that adopts nothing
    digests exactly as it did before this key existed and a job frozen by an
    older build still resumes.
    """
    covered: dict[str, Any] = {
        "kind": "export.playlist",
        "playlist": playlist_key,
        "export": export_path,
        # THE TRACK SET, not just the file it came from. A path names where
        # the answer was read; only this names what will be written.
        "tracks": list(tracks),
    }
    if adopts:
        covered["adopts"] = adopts
    return digest_of(covered)


def _frozen_adoption(payload) -> dict[str, str]:
    """The digest's fourth input, read off a frozen payload for the resume."""
    return {"adopts": str(payload.get(ADOPTS) or "")}


def recognition_warnings(
    resolved: source.ResolvedPlaylist, found: ledger.Recognition
) -> tuple[dict[str, str], ...]:
    """What a person is told about the remote playlist, when there is something.

    AT MOST ONE, which :func:`shown_playlist` relies on. Adopting is said out
    loud because it writes onto a playlist the account already holds, and the
    way to decline it is named in the same sentence, since a wrong offer with no
    way round it would leave this crate unexportable. Ambiguity is said because
    the write then CREATES, which is the second playlist R-229 is about, and the
    person is the only one who can tell which recorded playlist was this one. A
    mismatch is said because the write lands on a playlist made from different
    music, which is what a path reused for a new crate does.
    """
    if found.adopts:
        evidence = (
            f"which was last written from {found.recorded} track(s), "
            f"{found.shared} of them among the {found.crate} this playlist holds"
            if found.recorded
            else "which was recorded under the same name before this build "
            "recorded what a playlist holds"
        )
        return (
            {
                "code": "outbound-playlist-adopted",
                "message": (
                    f"{resolved.key!r} has no recorded remote playlist, and "
                    f"{found.adopts!r} has one and is no longer in this export, "
                    f"{evidence}. This write updates that remote playlist "
                    f"{found.remote_id} rather than creating a second one. Pass "
                    f"--new-playlist to create a new one instead"
                ),
            },
        )
    if found.ambiguous:
        return (
            {
                "code": "outbound-playlist-adoption-ambiguous",
                "message": (
                    f"{resolved.key!r} has no recorded remote playlist, and "
                    f"{len(found.candidates)} recorded playlists that are no "
                    f"longer in this export could each be it: "
                    f"{', '.join(found.candidates)}. None is adopted, so this "
                    f"write creates a new remote playlist"
                ),
            },
        )
    if found.mismatched:
        elsewhere = (
            f" It looks like the playlist now at {', '.join(found.claimed_by)}, "
            f"and exporting that one first moves the remote playlist to it and "
            f"leaves this one free to get its own"
            if found.claimed_by
            else ""
        )
        return (
            {
                "code": "outbound-playlist-record-mismatch",
                "message": (
                    f"the remote playlist {found.own_remote_id} recorded for "
                    f"{resolved.key!r} was last written from a playlist that "
                    f"shared fewer than half its tracks with this one, so it may "
                    f"belong to a playlist that has since been renamed. This "
                    f"write updates it anyway.{elsewhere}"
                ),
            },
        )
    return ()


def shown_playlist(
    found: ledger.Recognition, warnings: tuple[dict[str, str], ...]
) -> dict[str, Any]:
    """What the confirm gate shows about the REMOTE playlist this write lands on.

    SHOWN EVERY TIME, for the reason ``shell.shown_export`` gives: a block that
    appeared only on an adoption would make its absence the only thing saying
    "this creates a playlist". The warning's sentence rides here as well as on
    the envelope because a refusal carries no warnings, and the gate's first
    answer IS a refusal, so on the envelope alone a person would learn of the
    adoption only after confirming it.

    A PURE FUNCTION OF ONE READING OF THE LEDGER. It takes the recognition and
    the warnings already built from it, so the gate, the envelope and the
    frozen payload cannot describe three different ledgers.
    """
    if found.own_remote_id:
        block: dict[str, Any] = {
            "action": ACTION_UPDATE,
            "remote_id": found.own_remote_id,
        }
    elif found.adopts:
        block = {
            "action": ACTION_ADOPT,
            "remote_id": found.remote_id,
            "recorded_as": found.adopts,
        }
    else:
        block = {"action": ACTION_CREATE, "remote_id": None}
    for warning in warnings:
        block["warning"] = warning["message"]
    return {"remote_playlist": block}


def export_argv(job) -> list[str]:
    """The command line that continues one queued export.

    IT CARRIES ``--run``, AND WITHOUT IT THIS JOB COULD NEVER BE DRIVEN. The
    confirm gate is ``explicit``, so R34 makes it answerable only by a separate
    act recorded against a run. The child :mod:`cratekit.core.jobs` spawns is a
    fresh process, and ``cli.run`` mints a NEW run whenever ``--run`` is absent,
    so a resume naming only the job met the gate with nothing recorded and exited
    DECISION_REQUIRED. Every respawn did the same, so a confirmed export sat in
    the queue for ever. Measured by driving this function's own output through
    the dispatcher on 2026-08-23.

    The flag goes BEFORE the verb path because ``--run`` belongs to the root
    parser: a decision belongs to the invocation rather than to the subcommand.

    IT ALSO CARRIES ``--export``, AND THE POSITIONAL IS THE RESOLVED KEY rather
    than whatever the person typed. Both are the same requirement wearing two
    hats. The resumed child recomputes the confirm digest, and the digest is
    taken over the resolved key and the absolute path, so emitting the original
    argument would produce a different digest and meet ``DecisionStale``.

    A job frozen by a build older than this one carries no gate run and resumes
    without the flag, which returns it to the refusal it was already in rather
    than crashing the driver on a missing key.
    """
    payload = job.payload or {}
    playlist = str(payload.get(PLAYLIST) or "")
    gate_run = payload.get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    argv = [*resume, "export", "playlist", playlist]
    exported = payload.get(EXPORT)
    if exported:
        argv += ["--export", str(exported)]
    return [*argv, "--job", job.job_id]


def export_playlist(ctx) -> Envelope:
    """Confirm this playlist, then queue it, or drive the job already queued."""
    spec = ctx.entry.gates[0]
    if ctx.args.job:
        return shell.resume(
            ctx,
            spec,
            ctx.args.job,
            digest=confirm_digest,
            summary=summary,
            frozen_extra=_frozen_adoption,
            concluded=concluded,
        )

    playlist = str(ctx.args.playlist or "")
    if not playlist:
        raise refuse(
            "export-playlist-unknown",
            "export playlist needs the library playlist identifier",
            steps=("pass the playlist identifier after the verb",),
            origin=("export.cli",),
        )
    # RESOLVED BEFORE THE GATE, so a person is never asked to confirm an export
    # that is about to refuse, and so the digest can name what they confirmed.
    exported = source.required_path(getattr(ctx.args, "export", None))
    library = source.read_library(exported)
    resolved = source.resolve(library, playlist)
    # THE CONFIGURATION IS LOADED BEFORE THE GATE NOW (R-227), because the age
    # the gate shows is judged against a day count the person owns. It also
    # means a configuration that cannot be read refuses before a person is asked
    # to confirm a write that could not have queued, which is the rule the
    # resolution above already follows.
    cfg = shell.load_config("export.cli")
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
    # RECOGNISED BEFORE THE GATE (R-229), so the person confirms the playlist the
    # write lands on and not only the tracks. ``--new-playlist`` takes the offer
    # off the reading rather than skipping the read, because the gate still has
    # to say whether this key has a record of its own.
    found = ledger.recognise(
        cfg,
        resolved.key,
        name=resolved.name,
        track_ids=resolved.track_ids,
        live=source.playlist_contents(library),
    )
    if getattr(ctx.args, "new_playlist", False):
        found = found.without_offer()
    said = recognition_warnings(resolved, found)

    # THE TRACKS THE DIGEST COVERS ARE SHOWN (R-693), through the gate layer,
    # beside the export's age and the remote playlist. The resume shows the
    # same tracks off the frozen payload, so one gate has one plan on either
    # screen; only the age, which the resume may not read, is the first ask's.
    option = ctx.gate.require(
        spec,
        plan={
            "digest": confirm_digest(
                resolved.key, str(exported), resolved.track_ids, adopts=found.adopts
            ),
            "items": list(resolved.track_ids),
        },
        context={
            shell.PLAYLIST: resolved.key,
            shell.EXPORT_PATH: str(exported),
            ADOPTS: found.adopts,
            **shell.shown_export(age),
            **shown_playlist(found, said),
        },
    )
    if option == "abort":
        # THE DECLARED SHAPE, and nothing about the playlist. See
        # ``shell.declined``: this verb declares ``job_state/1`` and the payload
        # that named the playlist carried none of that surface's four fields.
        return ctx.envelope(data=shell.declined(), outcome=Outcome.NO_OP)
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            # THE GATE RUN IS FROZEN so the respawned child can name the run
            # the confirmation was recorded against. See ``export_argv``.
            payload={
                PLAYLIST: resolved.key,
                NAME: resolved.name,
                EXPORT: str(exported),
                ADOPTS: found.adopts,
                REMOTE: found.own_remote_id or found.remote_id or None,
                shell.TRACKS: list(resolved.track_ids),
                jobs.GATE_RUN_KEY: ctx.run.run_id,
            },
            # ONE TRACK IS ONE ITEM. Without these the queue holds a job with
            # nothing to claim, and the driver reports an empty success over
            # work it never did.
            item_ids=resolved.track_ids,
            cfg=cfg,
        )
        return ctx.envelope(
            data=shell.reported(store, job, cfg, summary),
            warnings=(
                *shell.queue_warnings(resolved, noun="track", age=age),
                *said,
            ),
        )


def run_export_item(
    payload: dict[str, Any], track_id: str, cfg: config.Config, remote
) -> dict:
    """Write ONE library track to the remote playlist, and report what happened.

    PURE OF THE JOB ENGINE ON PURPOSE, taking the payload and an account rather
    than a job and a store. The properties that matter most about it, that a
    second run adds nothing and that an unmatched row is reported rather than
    dropped, are then drivable without a queue.

    THE PLAYLIST NAME COMES OFF THE PAYLOAD, never from splitting the key here.
    The key is a display path and the name is its last element, and rebuilding
    one from the other in a second place is how the remote playlist comes to be
    created under a name nobody chose.

    ``apply`` REUSES THE RECORDED REMOTE PLAYLIST, which is what makes the per
    item shape safe: the first item creates the remote playlist and records it,
    and every item after it reads that record rather than creating a second one.
    """
    library = source.read_library(Path(str(payload[EXPORT])))
    tracks = source.local_tracks(library, (track_id,), cfg=cfg)
    if not tracks:
        raise refuse(
            "outbound-item-absent",
            f"the export at {Path(str(payload[EXPORT])).name} no longer carries "
            f"track {track_id!r}, which this job queued, so there is nothing to "
            f"write for this item and nothing was written",
            steps=(
                "export the collection again and queue a new export rather than "
                "resuming this one",
            ),
            origin=("export", "cli"),
            detail={"track": track_id},
        )
    planned = outbound_export.plan(
        tracks,
        playlist_key=str(payload[PLAYLIST]),
        name=str(payload.get(NAME) or payload[PLAYLIST]),
        account=remote,
        adopts=str(payload.get(ADOPTS) or ""),
        expected=str(payload.get(REMOTE) or ""),
        # THE WHOLE CRATE, not this item. See ``ExportPlan.contents``.
        contents=[str(track) for track in payload.get(shell.TRACKS) or ()],
    )
    report = outbound_export.apply(cfg, remote, planned)
    return {
        "track": track_id,
        "playlist_key": report.playlist_key,
        "remote_id": report.remote_id,
        "created": report.created,
        "adopted_from": report.adopted_from,
        "added": list(report.added),
        "already": list(report.already),
        "unmatched": [
            {
                "identity": row.identity,
                "title": row.title,
                "artist": row.artist,
                "reason": row.reason,
            }
            for row in report.unmatched
        ],
    }


def handle(job, item, cfg) -> jobs.Produced:
    """Export one queued track. The per item worker behind ``export.playlist``.

    THE ITEM NAMES THE TRACK, not the payload. They differ for every job this
    shell queues, since it freezes one playlist and enqueues one item per track,
    and reading the payload instead would make every item write the same track.
    ``master/cli.py`` measured that exact defect on a four item job.

    ``cfg`` is the configuration this job was FROZEN against (KTD9), and it is
    used rather than merely accepted: the artifact root is resolved from it, so
    a queue that moved between enqueue and drive does not scatter one job's
    reports across two directories.

    THE ACCOUNT IS RESOLVED AT CALL TIME through the module attribute, so a test
    can put a stand in in front of it. It is the only route to a provider in this
    file. Since U63 it opens the provider account from the stored session, and it
    refuses with a named cause when there is none.
    """
    payload = dict(job.payload or {})
    report = run_export_item(payload, str(item.item_id), cfg, account.resolve(cfg))
    return artifacts.produced(cfg, job, item, report)


__all__ = [
    "NO_MATCH",
    "UNMATCHED_WARNING",
    "build",
    "concluded",
    "confirm_digest",
    "export_argv",
    "export_playlist",
    "handle",
    "recognition_warnings",
    "run_export_item",
    "shown_playlist",
    "summary",
]
