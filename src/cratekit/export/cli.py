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

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs
from cratekit.core.cause import Outcome, refuse
from cratekit.modules.outbound import account, artifacts, shell, source
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


def summary(cfg: config.Config, job_id: str) -> dict[str, list[str]]:
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
    """
    added: list[str] = []
    already: list[str] = []
    unmatched: list[str] = []
    for report in artifacts.committed(cfg, job_id):
        added.extend(str(item) for item in report.get("added") or ())
        already.extend(str(item) for item in report.get("already") or ())
        # THE IDENTITY, NOT THE ROW. An unmatched entry is a mapping carrying the
        # library identity, the title and the artist, because a person reading
        # the ARTIFACT needs a name to recognise. Stringifying the mapping here
        # put a Python dict repr in a JSON envelope, which is a value nothing
        # downstream can key on. Measured by the first drive of this summary.
        unmatched.extend(_identity(item) for item in report.get("unmatched") or ())
    return {"added": added, "already": already, "unmatched": unmatched}


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
    parser.set_defaults(_handler=export_playlist)


def confirm_digest(
    playlist_key: str, export_path: str, tracks: list[str] | tuple[str, ...]
) -> str:
    """The identity the confirm decision is recorded against.

    ONE FUNCTION RATHER THAN TWO CALL SITES SPELLING A DICT, because the enqueue
    path builds it from a freshly resolved playlist and the resume path builds it
    from the frozen payload, and the whole point is that those two produce the
    same string. Two literals would be two chances to disagree, and the symptom
    would be a confirmed job that refuses its own resume for ever.
    """
    return digest_of(
        {
            "kind": "export.playlist",
            "playlist": playlist_key,
            "export": export_path,
            # THE TRACK SET, not just the file it came from. A path names where
            # the answer was read; only this names what will be written.
            "tracks": list(tracks),
        }
    )


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
            ctx, spec, ctx.args.job, digest=confirm_digest, summary=summary
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
    resolved = source.resolve(source.read_library(exported), playlist)

    option = ctx.gate.require(spec, digest=confirm_digest(resolved.key, str(exported), resolved.track_ids))
    if option == "abort":
        # THE DECLARED SHAPE, and nothing about the playlist. See
        # ``shell.declined``: this verb declares ``job_state/1`` and the payload
        # that named the playlist carried none of that surface's four fields.
        return ctx.envelope(data=shell.declined(), outcome=Outcome.NO_OP)
    cfg = shell.load_config("export.cli")
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
            warnings=shell.queue_warnings(resolved, noun="track"),
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
    tracks = source.local_tracks(library, (track_id,))
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
    )
    report = outbound_export.apply(cfg, remote, planned)
    return {
        "track": track_id,
        "playlist_key": report.playlist_key,
        "remote_id": report.remote_id,
        "created": report.created,
        "added": list(report.added),
        "already": list(report.already),
        "unmatched": [
            {"identity": row.identity, "title": row.title, "artist": row.artist}
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
    file, and in this build it always refuses; the queued envelope already warned
    the person that it would.
    """
    payload = dict(job.payload or {})
    report = run_export_item(payload, str(item.item_id), cfg, account.resolve(cfg))
    return artifacts.produced(cfg, job, item, report)


__all__ = [
    "build",
    "confirm_digest",
    "export_argv",
    "export_playlist",
    "handle",
    "run_export_item",
    "summary",
]
