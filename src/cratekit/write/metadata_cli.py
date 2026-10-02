"""Mirror vocal file tags into library My Tags.

My Tags are not content columns. U21's per-field policy in
``write/metadata.py`` does not govern this surface. The writer is
:func:`cratekit.core.rb_writer.ensure_my_tag_value` and
:func:`cratekit.core.rb_writer.add_my_tag`, add-only and idempotent.

THE LIVE DATABASE IS NEVER THE TARGET. The open uses the configured
database path, which a test points at a disposable copy. Opening with
an explicit path is also what the R-15 audit holds every binding call
to.

THE ANALYSIS WATCH NAMES ``watch_roots``, never an empty list and never
a folder that holds no ANLZ file. A My Tag write does not intend to
touch a grid, and naming the roots the library actually uses is what
makes a side effect visible rather than a clean session over a barren
watch.

Layer: write.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cratekit.cli import output
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import (
    analysis_store,
    config,
    locations,
    rb_writer,
    session,
    snapshot,
    tags,
)
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import routing_pass, trees

_ORIGIN = ("write", "metadata_cli")

WORKFLOW = "mytags-vocals"

#: The refusal the plan, the apply and doctor's ``library.paths_resolved`` share
#: when most of the collection records a path no prefix rule maps (R-372).
#: Registered in ``core.cause.REASONS``; the spelling here is the one every
#: surface raises and every consumer branches on.
PATHS_MAJORITY_UNRESOLVED = "library-paths-majority-unresolved"

#: How many recorded prefixes the refusal names, so a person is shown "these
#: 8554 rows record this prefix" rather than a wall of paths.
_NAMED_PREFIXES = 3

#: What this verb's write is filed under in a session record's change summary.
#: The summary's key is a tree identifier everywhere else, and a My Tag category
#: is no tree, so this names the surface instead. It is only ever rendered, in
#: ``restore list`` and in the refusal a restore raises before discarding later
#: work, and nothing looks it up in the tree registry. Stable on purpose and
#: distinct from ``CATEGORY``, which is a display name a person can rename (R19).
CHANGE_KEY = "my-tags.vocals"

CATEGORY = "Vocals"
VALUE_VOX = "vox"
VALUE_MALE = "male vox"
VALUE_FEMALE = "female vox"

#: Matches ``cratekit.analysis.cli.DEFAULT_VOCAL_THRESHOLD``. Duplicated
#: because this layer may not import the analysis package.
DEFAULT_VOCAL_THRESHOLD = 12.0

STATE_KEY_VOCAL_CALIBRATION = "vocal_calibration"


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=_ORIGIN,
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def vocal_tag_values(
    voxlevel: int | None, voxgender: str | None, cut: float
) -> list[str]:
    """The My Tag values a track should carry. Empty below the with-vox cut.

    Gender is only considered for with-vox tracks, so male vox and female vox
    are always accompanied by vox.
    """
    if voxlevel is None or voxlevel < cut:
        return []
    values = [VALUE_VOX]
    if voxgender == "M":
        values.append(VALUE_MALE)
    elif voxgender == "F":
        values.append(VALUE_FEMALE)
    return values


def vocal_cut(cfg: config.Config) -> float:
    """The with-vox threshold for tagging: the fitted cut, or the default.

    A MISSING file is the default cut, because a My Tag written from the
    default is the source system's behaviour. An unreadable one refuses, and
    that refusal is :func:`load_vocal_threshold`'s, not a second copy.
    """
    threshold = load_vocal_threshold(cfg)
    return DEFAULT_VOCAL_THRESHOLD if threshold is None else threshold


def load_vocal_threshold(cfg: config.Config) -> float | None:
    """The library's fitted with-vox cut, or None when it was never calibrated.

    The threshold of :func:`load_vocal_calibration`, which is the one reader.
    """
    record = load_vocal_calibration(cfg)
    return None if record is None else record["threshold"]


def load_vocal_calibration(cfg: config.Config) -> dict[str, Any] | None:
    """The library's vocal calibration record, or None when there is none.

    THE ONE READER OF THE VOCAL CALIBRATION. The tagging verb, the routing
    passes, the rebuild and resort workers and the convergence report all come
    through here, so a corrupt file refuses the same way on every surface and
    no surface can read it more leniently than another. The record comes back
    whole, with ``threshold`` already checked and made a float, because the
    calibrate verb reports the ``method`` and ``note`` of the cut it replaces
    (U90) and a second reader for those would be a second opinion on the file.

    A MISSING file is None rather than the default cut, and the difference is
    the routing contract (R-276): the default was never fitted to this library,
    so filing a whole library under "with vox" from it would be the product
    answering for the person. None leaves the vocal dimension uncompared, and
    the engine names it. An UNREADABLE file refuses, because a corrupt
    calibration and an absent one are different states, and folding the first
    into the second files or tags from a cut nobody fitted. This mirrors
    ``energy.load_calibration``.
    """
    path = config.state_path(STATE_KEY_VOCAL_CALIBRATION, cfg)
    if not path.is_file():
        return None
    # A list, string or null payload raises TypeError at the subscript, so
    # AttributeError, which energy's tuple carries for its ``.items()`` call,
    # has no producer here. json.loads accepts NaN and Infinity, and a NaN cut
    # makes every ``voxlevel < cut`` false, which would tag every scored track
    # as vox, so a threshold that is not finite is unreadable too. A JSON
    # boolean would read as a cut of 1.0 and an integer too large for a float
    # raises OverflowError, and both are refused for the same reason.
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
        raw = record["threshold"]
        if isinstance(raw, bool):
            raise TypeError(f"threshold {raw} is a boolean, not a number")
        threshold = float(raw)
        if not math.isfinite(threshold):
            raise ValueError(f"threshold {threshold} is not a finite number")
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        raise refuse(
            "vocal-calibration-unreadable",
            f"this library's vocal calibration at {path} could not be read "
            f"({type(exc).__name__}: {exc}), so no with-vox cut can be taken from it",
            steps=(
                "calibrate again over the whole library, the library root walked "
                "recursively, which rewrites it from every scored track",
                f"or delete {path}, after which My Tags use the default cut of "
                f"{DEFAULT_VOCAL_THRESHOLD} and the routing passes file nothing "
                f"under the vocal sub-playlist until a calibration is written",
            ),
            origin=_ORIGIN,
            detail={"calibration": str(path), "kind": type(exc).__name__},
        ) from exc
    return {**record, "threshold": threshold}


def _prefix_rules(cfg: config.Config) -> list[locations.PrefixRule]:
    return list(locations.prefix_rules(cfg.resolved_prefix_map()))


@dataclass(frozen=True, slots=True)
class ResolutionTotals:
    """How the collection's active rows resolve on this machine (R-372).

    ``unresolved`` is every row the plan could not read a file for, for any of
    three reasons: no recorded path at all, which is a streaming row; a path
    under no rule; or a mapped path whose file is gone. ``unmapped`` is the
    middle one alone, the rows whose recorded path matched neither the library
    root nor any ``library.location_prefix_map`` rule, and it is the count the
    majority rule reads. THE OTHER TWO ARE NOT A PREFIX RULE'S TO FIX: a
    streaming row has nothing a rule could rewrite, and a missing file is the
    deletion pass's question. Reading the whole ``unresolved`` total as the
    prefix map's failure would refuse a library of streaming rows with a step
    that cannot help, and would refuse every fixture in this suite whose rows
    carry no path. The sitting that found R-372 measured 9937 unmapped of 9937
    unresolved, so on the library that paid for this the two readings agree.

    ``prefixes`` groups the unmapped rows by their leading components, which is
    what ``locations.leading_prefix`` exists for, so the refusal can name the
    drive rather than the rows.
    """

    active: int
    unresolved: int
    unmapped: int
    prefixes: Mapping[str, int] = field(default_factory=dict)

    @property
    def majority_unmapped(self) -> bool:
        """More than half of the active rows record a path under no rule.

        Strictly more than half, and never over an empty collection: zero rows
        is a library with nothing to resolve, not a library that resolves
        nothing.
        """
        return self.active > 0 and self.unmapped * 2 > self.active

    def as_dict(self) -> dict[str, int]:
        return {
            "active": self.active,
            "unresolved": self.unresolved,
            "unmapped": self.unmapped,
        }


@dataclass(frozen=True, slots=True)
class _Survey:
    """One walk of the collection: the totals and the rows that resolved to a file."""

    totals: ResolutionTotals
    resolved: tuple[tuple[trees.ContentRow, Path], ...]


def _survey(cfg: config.Config, db: Any) -> _Survey:
    """THE ONE WALK. The plan and doctor both read the collection through here.

    Decoded and resolved by ``trees.located``, the one decode-then-resolve step,
    rather than by a second pairing of the two calls; and counted once, in one
    place, so the plan's totals and the doctor check's verdict cannot come from
    two different readings of what a row is. A path is a file for the plan's
    purposes only when it exists as one, which is the rule the plan always had.
    """
    root = Path(cfg.library.root)
    prefix_map = _prefix_rules(cfg)
    active = 0
    unresolved = 0
    unmapped = 0
    prefixes: Counter[str] = Counter()
    resolved: list[tuple[trees.ContentRow, Path]] = []
    for row in routing_pass.content_rows(db):
        if row.deleted:
            continue
        active += 1
        try:
            _, outcome = trees.located(row.recorded, root=root, prefix_map=prefix_map)
        except locations.LocationDecodeError:
            # A location naming another host, or one that will not decode, is
            # a row this machine cannot read a file for and counts as such. It
            # is not the prefix map's failure, so it is not unmapped, and it is
            # not a defect in this walk, so it does not take the plan or the
            # doctor check down with it.
            unresolved += 1
            continue
        if outcome.resolution is locations.Resolution.UNMAPPED:
            unmapped += 1
            prefixes[outcome.prefix or "?"] += 1
        path = Path(outcome.path) if outcome.path is not None else None
        if path is None or not path.is_file():
            unresolved += 1
            continue
        resolved.append((row, path))
    return _Survey(
        ResolutionTotals(
            active=active,
            unresolved=unresolved,
            unmapped=unmapped,
            prefixes=dict(prefixes.most_common()),
        ),
        tuple(resolved),
    )


def resolution_totals(cfg: config.Config, db: Any) -> ResolutionTotals:
    """How the collection resolves, for doctor's ``library.paths_resolved``."""
    return _survey(cfg, db).totals


#: What the majority refusal says cannot be done, for the verb it was written for.
_VOCALS_BLOCKED = "nothing about its vocals can be reported or written"


def majority_unmapped_cause(
    cfg: config.Config, totals: ResolutionTotals, *, blocked: str = _VOCALS_BLOCKED
) -> Cause:
    """The refusal every surface raises when most rows record an unmapped path.

    ``blocked`` is the clause saying what cannot be done until the rule exists.
    It is the one part of the sentence that belongs to the verb raising it, so
    a second verb that plans over the collection's files says its own and
    shares the slug, the counts, the steps and the detail.

    Built through ``refuse`` so the slug is checked against the registry and the
    remedy is the reserved one. ``RUN_SETUP`` rather than ``RUN_DOCTOR``: doctor
    now says the same thing, and sending a person from the plan to a check that
    sends them back is a loop. Setup, run again with the database present, reads
    rekordbox's own recorded drive names and offers the rule.
    """
    named = list(totals.prefixes.items())[:_NAMED_PREFIXES]
    listed = ", ".join(f"{count} under {prefix}" for prefix, count in named)
    more = len(totals.prefixes) - len(named)
    if more > 0:
        listed += f", and {more} other prefix{'es' if more > 1 else ''}"
    current = [
        {"from": source, "to": target} for source, target in cfg.resolved_prefix_map()
    ]
    return refuse(
        PATHS_MAJORITY_UNRESOLVED,
        (
            f"{totals.unmapped} of {totals.active} active rows record a path "
            f"under no library.location_prefix_map rule ({listed}), so this "
            f"library cannot be read from here and {blocked} until the rule exists"
        ),
        remedy=Remedy.RUN_SETUP,
        steps=(
            "run setup again with the database present; it reads the drive "
            "rekordbox recorded the library under and where it is mounted today, "
            "and offers the rule",
            "or add library.location_prefix_map = [{ from = \"<recorded prefix>\", "
            "to = \"<where it is mounted>\" }] to the configuration by hand, with "
            "from equal to to when the folder is exactly where the rows say",
        ),
        origin=_ORIGIN,
        detail={
            **totals.as_dict(),
            "prefixes": dict(totals.prefixes),
            "prefix_map": current,
        },
    ).cause


def _refused_plan(ctx, plan: dict[str, Any], cause: Cause) -> Envelope:
    """The plan, whole, under a failed outcome that names why it may not be acted on.

    The totals stay in ``data`` because they are the evidence: a person reading
    the refusal should see the 9937 beside the 0 rather than an empty payload.
    Built through ``output.build`` because the context's envelope helper takes no
    cause, and a non success outcome without one is the envelope the validator
    rejects. No warning is attached: a warning rides a success and this is not
    one.
    """
    return output.build(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        schema=ctx.entry.output_schema or output.current_schema("plan"),
        started=ctx.started,
        outcome=Outcome.FAILED,
        code=cause.code,
        data=plan,
        cause=cause,
    )


def _open(cfg: config.Config, *, writing: bool) -> Any:
    target = rb_writer.live_db_path(cfg)
    return rb_writer.open_db(
        target,
        require_closed=writing,
        cfg=cfg,
    )


def _rollback_quietly(db: Any) -> None:
    try:
        db.session.rollback()
    except Exception:  # noqa: BLE001 - a failed cleanup must not hide its cause
        return


def plan_mytags(cfg: config.Config, db: Any) -> dict[str, Any]:
    """The plan this verb shows: which existing rows would receive which values."""
    return _plan_from(cfg, _survey(cfg, db))


def _plan_from(cfg: config.Config, survey: _Survey) -> dict[str, Any]:
    """The plan over one walk, so the verb can keep the walk's grouping beside it."""
    cut = vocal_cut(cfg)
    items: list[dict[str, Any]] = []
    for row, path in survey.resolved:
        values = vocal_tag_values(
            tags.read_vox_from_file(path),
            tags.read_voxgender_from_file(path),
            cut,
        )
        if values:
            items.append(
                {
                    "content_id": row.content_id,
                    "values": values,
                    "path": str(path),
                }
            )
    return {
        "digest": digest_of(
            {
                "kind": WORKFLOW,
                "cut": cut,
                "items": items,
            }
        ),
        "items": items,
        "totals": {
            "count": len(items),
            **survey.totals.as_dict(),
            "cut": cut,
            "written": 0,
            "already": 0,
        },
        "chunk": None,
    }


def apply_mytags(cfg: config.Config, db: Any, plan: dict[str, Any]) -> dict[str, int]:
    """Ensure the Vocals category and add missing associations. Does not commit."""
    written = 0
    already = 0
    by_value: dict[str, list[str]] = {}
    for item in plan["items"]:
        for value_name in item["values"]:
            by_value.setdefault(value_name, []).append(item["content_id"])
    for value_name, content_ids in by_value.items():
        value_row = rb_writer.ensure_my_tag_value(db, CATEGORY, value_name)
        for content_id in content_ids:
            if rb_writer.add_my_tag(db, value_row, content_id):
                written += 1
            else:
                already += 1
    return {"written": written, "already": already}


def _record_mytags_commit(record: session.SessionRecord, written: int, cfg: config.Config) -> None:
    """Record this verb's commit on its session record, when it wrote anything.

    A SECOND APPLY WRITES NOTHING AND CLAIMS NO COMMIT, for the reason
    :func:`cratekit.write.trees._record_membership_commit` gives: a restore reads
    a committed source as work it would discard. Zero is decidable because a
    value row this verb creates is only ever created on the way to an
    association. Keyed on ``CHANGE_KEY``, a stable identifier and never the
    category's display name (R19).
    """
    if written <= 0:
        return
    session.record_commit(
        record,
        CHANGE_KEY,
        session.ChangeSummary((session.TreeChange(tree=CHANGE_KEY, created=written),)),
        cfg,
    )


def build_mytags_vocals(parser, entry) -> None:
    del entry
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="write the planned My Tags (default: plan only, nothing is written)",
    )
    parser.set_defaults(_handler=mytags_vocals)


def mytags_vocals(ctx) -> Envelope:
    cfg = _load()
    writing = bool(getattr(ctx.args, "apply", False))
    db = _open(cfg, writing=writing)
    try:
        # ONE WALK, kept beside the plan rather than read back out of it, so the
        # refusal names the prefixes the walk grouped. The plan's totals carry
        # the counts alone, which is all the payload surface declares.
        survey = _survey(cfg, db)
        # A MAJORITY UNMAPPED REFUSES BEFORE THE APPLY FLAG IS READ (R-372). The
        # first real plan reported ok over 9937 rows it had skipped, and an apply
        # on it would have written nothing and reported success. Plan and apply
        # refuse alike, under one slug, with the totals still in the payload; the
        # apply flag is still required for a write, and it does not reach one.
        # The refused plan carries the totals and no items, so a run that is
        # about to be refused does not read the tags off every resolved file.
        if survey.totals.majority_unmapped:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
            return _refused_plan(ctx, empty, majority_unmapped_cause(cfg, survey.totals))
        plan = _plan_from(cfg, survey)
        if not writing:
            return ctx.envelope(data=plan, outcome=Outcome.OK)
        with session.assert_gates(
            cfg,
            workflow=WORKFLOW,
            analysis_roots=analysis_store.watch_roots(cfg),
            keep=session.Keep.RECORD,
        ) as gates, rb_writer.commit_witness(db) as witness:
            record = gates.record
            # THE RECORD IS WHAT MAKES THE CAPTURE AN UNDO (R-375). This verb
            # took a capture and opened no record, so after a real apply the
            # only trace of the write was a snapshot directory ``restore list``
            # could not show and the pruning scan did not protect. Attached
            # before it is judged, for the reason the membership writer gives.
            capture = snapshot.capture(cfg, db=db)
            session.attach_capture(record, capture.root, cfg)
            snapshot.assert_verified(capture)
            counts = {"written": 0, "already": 0}
            try:
                counts = apply_mytags(cfg, db, plan)
                rb_writer.commit_guarded(db)
            except BaseException:
                _rollback_quietly(db)
                # AN EXCEPTION IS NOT PROOF NOTHING LANDED: the binding commits
                # and THEN saves rekordbox's playlist file. The witness is the
                # engine's own answer, for the reason the membership writer gives.
                if witness.landed:
                    _record_mytags_commit(record, counts["written"], cfg)
                raise
            # RECORDED THE INSTANT THE COMMIT RETURNS.
            _record_mytags_commit(record, counts["written"], cfg)
        plan["totals"]["written"] = counts["written"]
        plan["totals"]["already"] = counts["already"]
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    finally:
        rb_writer.close_db(db)
