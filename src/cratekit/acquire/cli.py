"""``crate acquire download`` and ``crate acquire audit``: the two acquisition shells.

U15 landed the acquisition ENGINES and never landed a shell, so Feature
Inventory rows 6 and 7 sat uncovered while the registry declared both verbs
against a closed unit. This file is the shell half, and nothing here re-decides
what the registry already declares.

Builders take an untyped ``entry`` so this file does not import the CLI registry
(KTD23).

**Why ``acquire.download`` declares no gate, decided here rather than inherited.**
The house pattern for a destructive verb is a confirm gate against a plan digest,
and ``export.playlist`` beside it has one. The distinction that separates them is
the one ``run_backup`` and ``run_restore`` are separated on: this verb ADDS files
into the configured download staging directory and replaces nothing, deletes
nothing, and publishes nothing outward. An accidental run costs network time and
disk, both of which a person can simply delete. ``export.playlist`` is gated
because it writes to a remote service, which is an act the user cannot take back.

The provider-side cost is the real argument for a gate and it does not survive
contact with what this shell does: an unpaced run can get a credentialed account
blocked, but the pacing apparatus in :mod:`cratekit.acquire.download` is what
manages that, and the shell reaches no network at all. It freezes a path and
queues. So the gate would guard the one step in the verb that cannot cause the
harm the gate is for.

Declining it also keeps the verb out of ``tests/test_queued_resume_contract.py``'s
derived population, which is a consequence rather than a reason: an explicit gate
plus ``long_running`` plus an ``argv_builder`` obliges the resume argv to carry
``--run`` with the frozen gate run, and that machinery would exist here purely to
guard an add-only local write.

**Why the audit reads NAMES and containers rather than opening files.** R21 makes
a lossy copy carry a marker inside its name, config owns the marker text (S3),
and :func:`cratekit.acquire.match_cli.library_template` already hands that text to
the naming engine so the marked copy and its lossless twin fold to one recording.
That marker is therefore the durable on-disk fact about a file's losslessness, and
it is the one this verb audits. The alternative, opening every file to read its
codec, needs the audio stack: this verb declares no doctor check and no module
toggle, so it has to answer on a slim profile that has no such stack installed.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from cratekit.acquire.adapter import LosslessPolicy
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, naming
from cratekit.core.cause import Cause, CratekitError, Remediation
from cratekit.core.exit_codes import Remedy

# ---------------------------------------------------------------------------
# What a container can tell you about loss, and what it cannot
# ---------------------------------------------------------------------------

#: Containers that hold audio without loss.
LOSSLESS_EXTS: frozenset[str] = frozenset({".flac", ".aiff", ".aif", ".wav", ".alac"})

#: Containers that hold audio only after a lossy encode.
LOSSY_EXTS: frozenset[str] = frozenset({".mp3", ".aac", ".opus", ".ogg", ".webm"})

#: Containers the SUFFIX cannot decide, DERIVED as the remainder of the renamer's
#: own audio table rather than listed. Today that remainder is exactly ``.m4a``,
#: because ALAC and AAC ship inside the same MP4 container, so the suffix names a
#: file that may be either and only opening it answers which.
#:
#: The derivation is the point and a third literal would have defeated it. A
#: format added to ``naming.AUDIO_EXTS`` and to neither set above lands here on
#: its own and is REPORTED as unclassified, where a hand-kept list would have let
#: it fall out of the sweep silently. Unclassified is the safe default because a
#: sweep that quietly counted an unknown container as lossless would report a
#: clean library over files it never classified, which is the merge bar's "shown a
#: clean report over state the tool could not read" exactly (P4).
UNDECIDED_EXTS: frozenset[str] = frozenset(naming.AUDIO_EXTS) - LOSSLESS_EXTS - LOSSY_EXTS

#: The queue name this report scopes itself to. Named rather than a bare string
#: for the reason :mod:`cratekit.cli.review` names its own: a consumer reading an
#: unlabelled queue field has no way to tell which set it is looking at.
AUDIT_QUEUE = "acquire.lossless"


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("acquire.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


# ---------------------------------------------------------------------------
# acquire.download
# ---------------------------------------------------------------------------


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument("list", help="the list of tracks to acquire")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the acquisition already queued under this identifier",
    )
    parser.set_defaults(_handler=acquire_download)


def download_argv(job) -> list[str]:
    """The command line that continues one queued acquisition.

    No ``--run`` here, and its absence is a decision rather than an omission. The
    flag exists to carry a frozen gate run back into the respawned child, and this
    verb declares no gate, so there is nothing to carry. The module docstring says
    why it declares none.
    """
    payload = job.payload or {}
    wanted = str(payload.get("list") or "")
    return ["acquire", "download", wanted, "--job", job.job_id]


def acquire_download(ctx) -> Envelope:
    """Freeze the list and queue. The acquisition itself is the worker's.

    The path is frozen WITHOUT being read, which is the same convention
    ``tag.folder`` and ``master`` follow and it is deliberate: a read here would
    refuse on a fixture, or on a machine where the work would have run fine once
    claimed, and the queue is what owns reading the input under the frozen
    configuration.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"list": str(ctx.args.list)},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


# ---------------------------------------------------------------------------
# acquire.audit
# ---------------------------------------------------------------------------


def build_audit(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.set_defaults(_handler=acquire_audit)


def classify(suffix: str) -> str:
    """``lossless``, ``lossy``, ``undecided``, or ``other`` for one lowercase suffix.

    ``other`` is everything that is not audio at all, which a music directory
    holds plenty of. It is a fourth answer rather than a silent skip so that the
    walk below reads as a classification of every file it saw.
    """
    if suffix in LOSSLESS_EXTS:
        return "lossless"
    if suffix in LOSSY_EXTS:
        return "lossy"
    if suffix in UNDECIDED_EXTS:
        return "undecided"
    return "other"


def findings(root: Path, *, policy: LosslessPolicy, marker: str) -> tuple[dict[str, Any], ...]:
    """Every file under ``root`` that the lossless policy does not admit.

    Four kinds, and each one is a state R21 forbids rather than a preference:

    * ``lossy-under-strict``: a lossy file under the strict policy, which says a
      track that exists only lossy is reported unacquired rather than downloaded.
      The marker is irrelevant here; strict means the file should not be present.
      NOT called ``lossy-refused``, which is what it said first: that string is
      already a declared CAUSE key, raised by
      :func:`cratekit.intake.pipeline.acquire_lossy_or_refuse` for the same policy
      at acquisition time. A cause key carries a remedy and an exit code; a
      finding kind is payload data with neither, and one string meaning both is
      the "one symbol meaning two things in two modules" METHOD lists among the
      things a green suite cannot see. The suite that noticed is
      ``test_reserved_causes``, and it noticed by counting rather than by knowing.
    * ``lossy-unmarked``: a lossy file under the permissive policy without the
      marker. This is the single failure R21 exists to prevent, because the
      marker is what a later stage strips to fold a lossy copy and its lossless
      twin into one recording.
    * ``marked-lossless``: a lossless file carrying the marker, which is the same
      failure wearing the opposite hat. The marker is false, the naming engine
      strips it anyway, and two genuinely different files fold to one key.
    * ``format-undecided``: a container whose suffix cannot answer the question.
      Reported rather than assumed, because a clean report over an unclassified
      file is worse than a report that says it could not tell.
    * ``path-unreadable``: a directory under the root that could not be listed.
      Not a policy violation, and reported for the same reason as the kind above
      it: a sweep that cannot see a directory has not audited it.

    ``marker`` empty means the configuration declares no marker text, so no file
    carries one. The two marker-dependent kinds cannot be decided in that state
    and are not reported, which is the same answer ``library_template`` gives when
    it returns a template with no marker rule rather than refusing the run.

    **WHY ``os.walk`` WITH AN ERROR HOOK AND NOT ``Path.rglob``.** This was
    written with ``rglob`` first, and driven on 2026-08-28: a music directory
    holding ``open/a.mp3`` and a mode 0o000 ``locked/`` containing ``b.mp3``
    reported exactly one finding and said nothing at all about ``locked``.
    ``rglob`` swallows the ``PermissionError`` from ``scandir`` and yields what it
    could reach, so the audit's answer over a partly unreadable library is
    indistinguishable from its answer over a clean one. The producer is not
    exotic: the library root is a removable volume, and macOS puts directories
    this walk cannot enter at the root of one as a matter of course. ``os.walk``
    takes an ``onerror`` hook, which turns the silence into a row.
    """
    if not root.is_dir():
        return ()
    found: list[dict[str, Any]] = []
    unreadable: list[Path] = []

    def note(exc: OSError) -> None:
        unreadable.append(Path(exc.filename) if exc.filename else root)

    for dirpath, _dirnames, filenames in os.walk(root, onerror=note):
        here = Path(dirpath)
        for name in filenames:
            path = here / name
            kind = classify(path.suffix.lower())
            if kind == "other":
                continue
            marked = bool(marker) and marker in path.stem
            if kind == "undecided":
                found.append(_item(path, root, "format-undecided"))
            elif kind == "lossy":
                if policy is LosslessPolicy.STRICT:
                    found.append(_item(path, root, "lossy-under-strict"))
                elif marker and not marked:
                    found.append(_item(path, root, "lossy-unmarked"))
            elif marked:
                found.append(_item(path, root, "marked-lossless"))
    found += [_item(path, root, "path-unreadable") for path in unreadable]
    return tuple(sorted(found, key=lambda item: (item["id"], item["kind"])))


def _item(path: Path, root: Path, kind: str) -> dict[str, Any]:
    """One finding projected for a listing: what it is and where.

    The path is recorded RELATIVE to the library root. An absolute one would put
    somebody's real directory layout into a payload a person may well paste into
    an issue (R1), and the root is already the subject of the report.
    """
    try:
        where = str(path.relative_to(root))
    except ValueError:
        # The walk never leaves the root, so this is unreachable through
        # ``findings``. It is handled anyway because the alternative is a
        # ValueError escaping a REPORT, and a report that raises over one odd
        # path tells the user nothing about the files it had already classified.
        where = path.name
    return {
        "id": where,
        "queue": AUDIT_QUEUE,
        "kind": kind,
        "suffix": path.suffix.lower(),
    }


def acquire_audit(ctx) -> Envelope:
    """Report what the lossless policy does not admit. Writes nothing.

    ``unresolved`` and the length of ``items`` are equal here and that is a
    property of this verb rather than a coincidence worth relying on: nothing
    pages, so the walk's whole result is the page. A later flag that returns a
    subset must recompute ``unresolved`` from the walk, never from the page, for
    the reason :mod:`cratekit.cli.review` gives: reporting the page size as the
    backlog is how a person concludes they are finished.
    """
    cfg = _load()
    found = findings(
        cfg.library.root / cfg.library.music_dir,
        policy=LosslessPolicy(cfg.acquisition.lossless_policy),
        marker=(cfg.naming.lossy_marker or "").strip(),
    )
    return ctx.envelope(
        data={
            "queue": AUDIT_QUEUE,
            "items": list(found),
            "unresolved": len(found),
        }
    )


__all__ = [
    "AUDIT_QUEUE",
    "LOSSLESS_EXTS",
    "LOSSY_EXTS",
    "UNDECIDED_EXTS",
    "acquire_audit",
    "acquire_download",
    "build",
    "build_audit",
    "classify",
    "download_argv",
    "findings",
]
