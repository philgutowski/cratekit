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
from pathlib import Path
from typing import Any

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
                "calibrate again over a folder holding both vocal and "
                "instrumental tracks, which rewrites it",
                f"or delete {path}, after which My Tags use the default cut of "
                f"{DEFAULT_VOCAL_THRESHOLD} and the routing passes file nothing "
                f"under the vocal sub-playlist until a calibration is written",
            ),
            origin=_ORIGIN,
            detail={"calibration": str(path), "kind": type(exc).__name__},
        ) from exc
    return {**record, "threshold": threshold}


def _prefix_rules(cfg: config.Config) -> list[locations.PrefixRule]:
    return [
        locations.PrefixRule(source, target)
        for source, target in cfg.resolved_prefix_map()
    ]


def _file_for(
    row: trees.ContentRow, *, root: Path, prefix_map: list[locations.PrefixRule]
) -> Path | None:
    resolved = locations.resolve_recorded_path(
        locations.location_to_path(row.recorded),
        root=root,
        prefix_map=prefix_map,
    )
    if resolved.path is None:
        return None
    path = Path(resolved.path)
    return path if path.is_file() else None


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
    cut = vocal_cut(cfg)
    root = Path(cfg.library.root)
    prefix_map = _prefix_rules(cfg)
    items: list[dict[str, Any]] = []
    active = 0
    unresolved = 0
    for row in routing_pass.content_rows(db):
        if row.deleted:
            continue
        active += 1
        path = _file_for(row, root=root, prefix_map=prefix_map)
        if path is None:
            unresolved += 1
            continue
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
            "active": active,
            "unresolved": unresolved,
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
        plan = plan_mytags(cfg, db)
        if not writing:
            return ctx.envelope(data=plan, outcome=Outcome.OK)
        with session.assert_gates(
            cfg,
            workflow=WORKFLOW,
            analysis_roots=analysis_store.watch_roots(cfg),
        ):
            capture = snapshot.capture(cfg, db=db)
            snapshot.assert_verified(capture)
            try:
                counts = apply_mytags(cfg, db, plan)
                rb_writer.commit_guarded(db)
            except BaseException:
                _rollback_quietly(db)
                raise
        plan["totals"]["written"] = counts["written"]
        plan["totals"]["already"] = counts["already"]
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    finally:
        rb_writer.close_db(db)
