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
the run will use (KTD9), queues one job under its own handler key with one item
per live collection row, and reports the job. The engine that drives it is
:mod:`cratekit.core.jobs`, which landed in U10, and :func:`handle` below is the
worker U55 landed behind it.

READING THE ROWS IS NOT SCANNING THEM, which is why this verb touches the
database before it queues anything. Deriving the items needs the row identifiers
and nothing else; deciding what is at the end of each recorded location is the
per-item work the job exists to do. So the shell opens the database, reads the
collection, and hands the walk to the queue.

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

# ``scan`` IS ALIASED because this module already defines a function of that
# name and that function is the VERB. One symbol meaning two things in one file
# is the defect ``docs/METHOD.md`` says to hunt, and here it would shadow the
# handler the parser binds. U51 aliased three modules called ``export`` for the
# same reason.
from cratekit.adopt import artifacts, collection, shell
from cratekit.adopt import scan as scan_engine
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, taxonomy
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
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


def _summary(cfg: config.Config, job_id: str) -> dict:
    """What this job's committed artifacts say the library looks like.

    DERIVED FROM WHAT RAN, never from what was queued. A scan that classified
    three rows of five and was continued tomorrow has five reports on disk and
    the person asking what their library holds means all five, which is why this
    reads the artifacts back rather than accumulating counts in memory.

    ZEROES INCLUDED, for the reason :func:`cratekit.adopt.scan.categories` gives:
    a summary listing only the categories it happened to see makes "no online
    only files in this library" and "this build does not look for them" the same
    output, and AE12 is precisely about telling those apart.
    """
    categories = {str(member): 0 for member in scan_engine.Readability}
    dispositions = {str(member): 0 for member in scan_engine.Disposition}
    for report in artifacts.committed(cfg, job_id):
        readability = str(report.get("readability") or "")
        disposition = str(report.get("disposition") or "")
        if readability in categories:
            categories[readability] += 1
        if disposition in dispositions:
            dispositions[disposition] += 1
    return {"categories": categories, "dispositions": dispositions}


def _empty(reason: str, detail: str) -> tuple[dict, tuple[dict[str, str], ...]]:
    """The payload and warning for a library with nothing to census.

    THE HONEST ZERO, and it is a different thing from a job with no items. A
    library that holds nothing is a correct outcome and the state every library
    is in before its first import; ``core.jobs`` reports a job with no items as
    SUCCEEDED by design, so a verb that queued one here would report a clean
    success over a census that never ran. Nothing is queued and the envelope says
    which zero this is.

    THE PAYLOAD SHAPE IS :func:`cratekit.adopt.shell.no_op`'s rather than this
    module's, because the three zero paths these two verbs now have would
    otherwise each be free to reintroduce R-234's null ``job_id`` separately.
    """
    return shell.no_op("no-op"), ({"code": reason, "message": detail},)


def scan(ctx) -> Envelope:
    """Queue one census over the person's own collection, and drive it on a resume.

    The handler key comes off the entry rather than being spelled again here, so
    the job the queue holds and the verb the registry declares cannot name two
    different things.

    THE READER LANDED, so this verb now reads. Everything this docstring said
    about a worker that "is not in this unit and cannot be" was true until U55 and
    is false now: :func:`cratekit.adopt.collection.read_collection` turns the
    configured database into :class:`cratekit.adopt.scan.CollectionRow` values,
    one item is queued per LIVE row, and :func:`handle` classifies one of them.

    THE ITEMS ARE DERIVED FROM THE COLLECTION AND NEVER FROM THE CENSUS. Deriving
    them from the census would stat every file in the library before the person
    is told anything, which is the work the job exists to do in the background.
    Reading the rows is cheap; probing the files is not.

    A LIBRARY OF TOMBSTONES IS NOT AN EMPTY LIBRARY, and only the collection can
    tell them apart: :func:`cratekit.adopt.scan.scan_rows` skips a deleted row, so
    both produce an empty census. The two warnings below are why the read happens
    here rather than one layer down.
    """
    cfg = _load()
    if ctx.args.job:
        return _resume(ctx, cfg)

    rows = collection.read_collection(cfg)
    live = tuple(row.content_id for row in rows if not row.deleted)
    if not live:
        payload, warnings = (
            _empty(
                "collection-all-tombstones",
                f"every one of the {len(rows)} rows in this library is a removal "
                f"rekordbox has not purged, so there is nothing to adopt",
            )
            if rows
            else _empty(
                "collection-empty",
                "this library holds no tracks, so there is nothing to census",
            )
        )
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"tree": taxonomy.default_taxonomy().tree.id},
            # ONE LIVE ROW IS ONE ITEM. Without them the queue holds a job with
            # nothing to claim and the driver reports an empty success over a
            # census it never took.
            item_ids=live,
            cfg=cfg,
        )
        return ctx.envelope(data=shell.reported(store, job))


def _resume(ctx, cfg: config.Config) -> Envelope:
    """Continue the census already queued under this identifier, and drive it.

    RECONCILE FIRST. A resume arrives after something stopped, and a claim left
    behind by a driver that died is state the queue cannot see for itself.

    IT RAISES ON A JOB THAT DID NOT FINISH rather than reporting one. That is
    R-225: ``master/cli.py``'s resume branch returns a normal envelope for a job
    that half failed and exits OK, so a person whose census did not happen is
    told it did. The predicate is ANY CLOSED JOB CARRYING A CAUSE rather than
    FAILED alone, because a run stopped with a signal is CANCELLED and carries
    the cause ``jobs.cancel`` builds; SUCCEEDED carries none, so it is unaffected.
    """
    with jobs.open_store() as store:
        job, warnings = shell.advance(
            ctx,
            store,
            jobs.get(store, ctx.args.job),
            origin=("adopt", "scan_cli"),
            nothing_to_run="report a census over a library it never read",
        )
        return ctx.envelope(
            data=shell.reported(store, job, {"census": _summary(cfg, job.job_id)}),
            warnings=warnings,
        )


def handle(job, item, cfg) -> jobs.Produced:
    """Classify ONE collection row. The per-item worker behind ``adopt.scan``.

    THE COLLECTION IS RE-READ AT DRIVE TIME AND IS NOT FROZEN.
    ``jobs.enqueue`` freezes the payload and the configuration, and neither
    carries the library. So a row soft deleted or a track removed in rekordbox
    between the queueing and the drive leaves an item naming a content identifier
    this read no longer produces, and that is refused with its own slug rather
    than raised as a ``KeyError``: an item that reported done having classified
    nothing is the clean-report-over-unreadable-state cost ``docs/METHOD.md``
    names.

    THE CONFIGURATION IS THE FROZEN ONE AND IS NOT LOADED HERE. KTD9 closes the
    recorded resume bug where a queued run re-resolved its configuration; a
    handler that loaded one is that defect wearing a new hat.

    ONE ROW RATHER THAN THE WHOLE WALK, which is what makes the engine's resume
    guarantee worth anything: a census killed at row three thousand resumes at row
    three thousand and one rather than restarting a walk that stats every file.
    """
    row = collection.indexed(cfg).get(item.item_id)
    if row is None:
        raise refuse(
            "adopt-item-absent",
            f"the collection no longer holds the row {item.item_id!r} this job "
            f"queued, so there is nothing to classify for it",
            steps=("queue a fresh census; this one was planned against a library that has moved",),
            origin=("adopt", "scan_cli"),
            detail={"content_id": item.item_id},
        )
    declared = taxonomy.default_taxonomy()
    (classified,) = scan_engine.scan_rows(
        [row],
        declared,
        root=cfg.library.root,
        prefix_map=collection.prefix_rules(cfg),
    )
    return artifacts.produced(
        cfg,
        job,
        item,
        {
            "content_id": classified.content_id,
            "recorded": classified.recorded,
            "path": classified.path,
            "readability": str(classified.readability),
            "disposition": str(classified.disposition),
            "genre": classified.genre,
            "bucket": classified.bucket,
            "match": classified.match,
        },
    )
