"""``crate adopt scan``: queue the census over an existing library.

WHY THIS IS A MODULE OF ITS OWN, AND WHY ITS SIBLING IS NOT BESIDE IT. The two
adoption verbs are not in the same position and never were. ``adopt.apply``
writes the database, is destructive, and declares two gates; ``adopt.scan``
declares none, writes nothing, and reads. They shared one ``module=`` string in
the registry, and the marker test that expires a ``planned_in`` keys on that
string, so the half that is ready was held back by the half that is not, for no
reason of its own. Splitting them costs one file.

WHAT IT ACTUALLY DOES, AND WHY THAT IS QUEUEING RATHER THAN SCANNING. A census
walks a whole collection and stats every file in it. That is long work by any
definition, and conformance 5 says long work is queued rather than run inline,
for the reason the source system taught: a sweep that runs inline in the shell
has no record, no resume, and no way to answer "what is it doing" from anywhere
except the terminal it was started in. So this verb freezes the configuration
the run will use (KTD9), queues one job under its own handler key, and reports
the job. The engine that drives it is :mod:`cratekit.core.jobs`, which landed in
U10.

THERE IS NO TREE ARGUMENT, AND THAT IS THE R19 ANSWER RATHER THAN A GAP. A
taxonomy declares exactly one routing tree, by stable identifier, and adoption
files tracks into the tree the active taxonomy declares. A flag naming a tree
would be a second opinion about a value the template already holds, and the only
thing a user could put in it is either that identifier or a mistake.

WHAT IT MUST NOT IMPORT, AND WHY IT IS A LAYERING TRAP RATHER THAN A RULE. A
command-line shell wants ``registry.Entry`` for its builder signature, and
importing it from here would be a modules-layer file reaching into the CLI layer,
which the layering guard refuses (KTD23). The legal shape is the one
``cratekit.acquire.match_cli`` uses: name :mod:`cratekit.cli.output` alone, which
is foundation-ranked because the output contract is reserved globally before any
verb ships (KTD25), and leave the builder's parameters unannotated. The types are
real at runtime; they are simply not this layer's to name.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, taxonomy
from cratekit.core.cause import Cause, CratekitError, Remediation
from cratekit.core.exit_codes import Remedy


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause.

    The remedy token is carried straight through from the configuration error
    that raised it, so "no config at all" and "config written by a newer build"
    keep their different answers all the way to the CLI. Flattening them here
    would put this module back in the business of writing instructions, which is
    what D2 removes from every layer but the outermost.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("adopt.scan_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb's arguments. The parameters are unannotated on purpose.

    ``entry`` is a ``cratekit.cli.registry.Entry`` and naming that type here
    would be this layer importing the one above it. See the module docstring.
    """
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help=(
            "continue the census already queued under this identifier rather "
            "than queueing a new one; this is how a resume re-invokes the verb"
        ),
    )
    parser.set_defaults(_handler=scan)


def adopt_scan_argv(job) -> list[str]:
    """The command line that continues one queued census.

    THE CONTRACT EVERY LONG-RUNNING VERB OWES, and the reason it is a function
    rather than a string in the registry: the payload is frozen at queue time
    (KTD9), so only the verb that queued it knows how to turn it back into an
    invocation. ``cratekit.cli.jobs.argv_for`` looks this up by handler key and
    imports nothing until the key is known to be real.

    It names the JOB rather than re-stating the request, which is what stops a
    resume from queueing a second record for one piece of work. ``job`` is a
    ``cratekit.core.jobs.Job`` and is unannotated for the layering reason the
    module docstring gives.
    """
    return ["adopt", "scan", "--job", job.job_id]


def _reported(store, job) -> dict:
    """One job as the ``job_state`` payload, which is what this verb emits."""
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def scan(ctx) -> Envelope:
    """Queue one census, or reconcile the one already queued, and report it.

    The handler key comes off the entry rather than being spelled again here, so
    the job the queue holds and the verb the registry declares cannot name two
    different things.

    WHAT THIS SHELL DOES NOT YET DO, said here rather than discovered by somebody
    watching a job sit still. It queues the census and reports it. The WORKER
    that walks a real collection is not in this unit and cannot be: turning a
    rekordbox library into :class:`cratekit.adopt.scan.CollectionRow` values needs
    a collection reader that has not landed, and the engine underneath
    (:func:`cratekit.adopt.scan.scan_rows`) deliberately takes its rows from a
    caller so that it is testable without a database at all. Recorded in the
    residual titled "adoption's tag write takes no destructive session and no
    library lock" rather than left as a surprise.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            # RECONCILE FIRST. A resume arrives after something stopped, and a
            # claim left behind by a driver that died is the state the queue
            # cannot see for itself.
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"tree": taxonomy.default_taxonomy().tree.id},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))
