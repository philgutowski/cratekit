"""Mirror vocal file tags into library My Tags.

My Tags are not content columns, so U21's per-field policy does not govern
them; the writers are :func:`cratekit.core.rb_writer.ensure_my_tag_value` and
:func:`cratekit.core.rb_writer.add_my_tag`, add-only and idempotent. The open
names the configured database path explicitly (R-15), and the analysis watch
names ``watch_roots``.

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
from cratekit.cli.output import Envelope, digest_of, load_config
from cratekit.core import analysis_store, config, locations, rb_writer, session, tags
from cratekit.core.cause import Cause, Outcome, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import routing_pass, trees

_ORIGIN = ("write", "metadata_cli")

WORKFLOW = "mytags-vocals"

#: The refusal the plan, the apply and doctor's ``library.paths_resolved`` share
#: when most of the collection records a path no prefix rule maps (R-372).
PATHS_MAJORITY_UNRESOLVED = "library-paths-majority-unresolved"

#: How many recorded prefixes the refusal names, rather than a wall of paths.
_NAMED_PREFIXES = 3

#: What this verb's write is filed under in a session record's change summary,
#: stable, unlike ``CATEGORY``, a display name a person can rename (R19).
CHANGE_KEY = "my-tags.vocals"

CATEGORY = "Vocals"
VALUE_VOX = "vox"
VALUE_MALE = "male vox"
VALUE_FEMALE = "female vox"

#: Matches ``cratekit.analysis.cli.DEFAULT_VOCAL_THRESHOLD``; this layer may not
#: import the analysis package.
DEFAULT_VOCAL_THRESHOLD = 12.0

STATE_KEY_VOCAL_CALIBRATION = "vocal_calibration"


def vocal_tag_values(voxlevel: int | None, voxgender: str | None, cut: float) -> list[str]:
    """The My Tag values a track should carry, empty below the with-vox cut.

    Gender is read only for with-vox tracks, so a gendered value always comes
    with vox.
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
    """The with-vox threshold for tagging: the fitted cut, or the default when none
    was fitted. An unreadable file refuses in :func:`load_vocal_threshold`.
    """
    threshold = load_vocal_threshold(cfg)
    return DEFAULT_VOCAL_THRESHOLD if threshold is None else threshold


def load_vocal_threshold(cfg: config.Config) -> float | None:
    """The fitted with-vox cut from :func:`load_vocal_calibration`, or None."""
    record = load_vocal_calibration(cfg)
    return None if record is None else record["threshold"]


def load_vocal_calibration(cfg: config.Config) -> dict[str, Any] | None:
    """The library's vocal calibration record, or None when there is none.

    The one reader, so a corrupt file refuses alike on every surface; the record
    comes back whole with ``threshold`` checked and a float (U90). A missing file
    is None, not the default cut, so routing leaves the vocal dimension
    uncompared (R-276). An unreadable file refuses.
    """
    path = config.state_path(STATE_KEY_VOCAL_CALIBRATION, cfg)
    if not path.is_file():
        return None
    # A non-object payload raises TypeError at the subscript. A NaN cut would
    # tag every scored track as vox, so a threshold that is not finite, a JSON
    # boolean (a cut of 1.0) and an overflowing integer are unreadable too.
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

    ``unresolved`` is every row with no readable file. ``unmapped`` is those
    under no rule alone, the only ones a prefix rule fixes, and is what the
    majority rule reads. ``prefixes`` groups them so the refusal names the drive.
    """

    active: int
    unresolved: int
    unmapped: int
    prefixes: Mapping[str, int] = field(default_factory=dict)

    @property
    def majority_unmapped(self) -> bool:
        """Strictly more than half of the active rows are unmapped; never over none."""
        return self.active > 0 and self.unmapped * 2 > self.active

    def as_dict(self) -> dict[str, int]:
        return {"active": self.active, "unresolved": self.unresolved, "unmapped": self.unmapped}


@dataclass(frozen=True, slots=True)
class _Survey:
    """One walk of the collection: the totals and the rows that resolved to a file."""

    totals: ResolutionTotals
    resolved: tuple[tuple[trees.ContentRow, Path], ...]


def _survey(cfg: config.Config, db: Any) -> _Survey:
    """The one walk of the collection, for the plan and doctor alike.

    Rows are located by ``trees.located`` and counted in one place, so the plan's
    totals and the doctor check cannot disagree. A path counts only when it
    exists as a file.
    """
    root = Path(cfg.library.root)
    prefix_map = _prefix_rules(cfg)
    active = unresolved = unmapped = 0
    prefixes: Counter[str] = Counter()
    resolved: list[tuple[trees.ContentRow, Path]] = []
    for row in routing_pass.content_rows(db):
        if row.deleted:
            continue
        active += 1
        try:
            _, outcome = trees.located(row.recorded, root=root, prefix_map=prefix_map)
        except locations.LocationDecodeError:
            # Another host or an undecodable location: unresolved, not unmapped,
            # and not a defect that ends the walk.
            unresolved += 1
            continue
        if outcome.resolution is locations.Resolution.UNMAPPED:
            unmapped += 1
            prefixes[outcome.prefix or "?"] += 1
        path = Path(outcome.path) if outcome.path is not None else None
        if path is None or not _is_a_file(path):
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


def _is_a_file(path: Path) -> bool:
    """Whether a file is there, a refusal to answer read as no.

    ``Path.is_file`` raises on an unenterable directory, a refused name, an input
    error or a null byte, and one such row must not end the walk.
    """
    try:
        return path.is_file()
    except (OSError, ValueError):
        return False


def resolution_totals(cfg: config.Config, db: Any) -> ResolutionTotals:
    """How the collection resolves, for doctor's ``library.paths_resolved``."""
    return _survey(cfg, db).totals


#: What the majority refusal says cannot be done, for the verb it was written for.
_VOCALS_BLOCKED = "nothing about its vocals can be reported or written"


def majority_unmapped_cause(
    cfg: config.Config, totals: ResolutionTotals, *, blocked: str = _VOCALS_BLOCKED
) -> Cause:
    """The refusal every surface raises when most rows record an unmapped path.

    ``blocked`` is the clause naming what cannot be done, the raising verb's
    own. ``RUN_SETUP``, since setup reads rekordbox's drive names and offers the
    rule.
    """
    named = list(totals.prefixes.items())[:_NAMED_PREFIXES]
    listed = ", ".join(f"{count} under {prefix}" for prefix, count in named)
    more = len(totals.prefixes) - len(named)
    if more > 0:
        listed += f", and {more} other prefix{'es' if more > 1 else ''}"
    current = [{"from": source, "to": target} for source, target in cfg.resolved_prefix_map()]
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
        detail={**totals.as_dict(), "prefixes": dict(totals.prefixes), "prefix_map": current},
    ).cause


def _refused_plan(ctx, plan: dict[str, Any], cause: Cause) -> Envelope:
    """The plan, whole, under a failed outcome naming why it may not be acted on.

    The totals stay as the evidence. Built through ``output.build`` because the
    context's envelope helper takes no cause; no warning, since this is no success.
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
            tags.read_vox_from_file(path), tags.read_voxgender_from_file(path), cut
        )
        if values:
            items.append({"content_id": row.content_id, "values": values, "path": str(path)})
    return {
        "digest": digest_of({"kind": WORKFLOW, "cut": cut, "items": items}),
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

    A second apply writes nothing and claims no commit. Keyed on ``CHANGE_KEY``,
    never the category's display name (R19).
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
    cfg = load_config(_ORIGIN)
    writing = bool(getattr(ctx.args, "apply", False))
    db = _open(cfg, writing=writing)
    try:
        # One walk, kept beside the plan so the refusal names its prefixes.
        survey = _survey(cfg, db)
        # A majority unmapped refuses plan and apply alike, before the apply flag
        # is read (R-372), with the totals and no items, so no tag is read.
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
            # The record is what makes the capture an undo (R-375), attached
            # before it is judged as ``trees.attached_capture`` says.
            record, capture = trees.attached_capture(gates, cfg, db)
            counts = {"written": 0, "already": 0}
            try:
                counts = apply_mytags(cfg, db, plan)
                rb_writer.commit_guarded(db)
            except BaseException:
                _rollback_quietly(db)
                # An exception is not proof nothing landed; the witness answers.
                if witness.landed:
                    _record_mytags_commit(record, counts["written"], cfg)
                raise
            # Recorded the instant the commit returns.
            _record_mytags_commit(record, counts["written"], cfg)
        plan["totals"]["written"] = counts["written"]
        plan["totals"]["already"] = counts["already"]
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    finally:
        rb_writer.close_db(db)
