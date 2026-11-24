"""The ``repair.numbers`` verb: every playlist under this product's nodes numbered 1 to N (U958).

rekordbox's Remove from Playlist takes out the row numbered as the selected
row's shown position, so a playlist whose live rows are not 1 to N loses the
wrong track to a removal by hand. The order is ``repair rows``'s: the backup
acknowledgment before the plan and the gate (R-733), the plan on a read handle
closed before the gate, the gate asked even over an empty plan, and only
``apply`` over a plan that writes opens the database to write, where the plan
is taken again and a moved digest refuses ``decision-stale``. The gate takes no
inline answer (R34). Layer: write; it names :mod:`cratekit.cli.output` and
nothing else from the command-line layer.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, confirm_gate, load_config
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session
from cratekit.core.cause import Outcome
from cratekit.write import numbers

#: The explicit gate a write is asked behind.
CONFIRM_GATE = "repair.numbers.confirm"

#: Every playlist in scope already reads 1 to N.
NOTHING_TO_WRITE = "numbers-nothing-to-write"

#: What the apply wrote and read back.
NUMBERS_WRITTEN = "numbers-written"

#: Playlists in scope whose order cannot be read, never written.
NUMBERS_HELD = "numbers-held"

_ORIGIN = ("write", "numbers_cli")


def build(parser, entry) -> None:
    """Declare the verb: the product's playlists, and any named with ``--playlist``."""
    del entry
    parser.add_argument(
        "--playlist",
        action="append",
        default=[],
        metavar="NAME",
        help=(
            "also number this playlist, named as rekordbox shows it, every live "
            "playlist of the name; may be given more than once"
        ),
    )
    parser.set_defaults(_handler=repair_numbers)


def _payload(plan: numbers.NumbersPlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    return {
        "digest": plan.digest,
        "items": [item.to_json() for item in plan.items],
        "totals": {**numbers.summary(plan), "written": 0, "read_back": 0},
        "chunk": None,
    }


def _facts(plan: numbers.NumbersPlan) -> dict[str, Any]:
    """What the gate puts in front of the items."""
    facts: dict[str, Any] = {
        "playlists read": plan.scanned,
        "playlists to number 1 to N": len(plan.items),
        "rows that move": sum(len(one.moves) for one in plan.items),
        "what moves": (
            "each live row's TrackNo, to its place in the order rekordbox shows now, "
            "and each removed row's to 0; no track joins or leaves a playlist"
        ),
    }
    if plan.named:
        facts["playlists named"] = list(plan.named)
    if plan.held:
        facts["held back, their order cannot be read"] = [one.path for one in plan.held]
    return facts


def _notes(plan: numbers.NumbersPlan) -> list[dict[str, str]]:
    if not plan.held:
        return []
    return [
        {
            "code": NUMBERS_HELD,
            "message": (
                f"{len(plan.held)} playlist(s) hold a row whose removal marker or "
                f"place cannot be read, so their order cannot be said and they were "
                f"not planned: " + ", ".join(repr(one.path) for one in plan.held[:5])
            ),
        }
    ]


def _plan(cfg: config.Config, named: list[str]) -> numbers.NumbersPlan:
    """The plan over the library as it stands, through a handle opened to read and closed."""
    declared = active_taxonomy.load(cfg)
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return numbers.plan(db, declared, named=named)
    finally:
        rb_writer.close_db(db)


def _write(cfg: config.Config, plan: numbers.NumbersPlan) -> numbers.Written:
    """Apply the plan through a handle of this function's own, opened to write."""
    declared = active_taxonomy.load(cfg)
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return numbers.apply(
            cfg, db, plan, declared=declared, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def repair_numbers(ctx) -> Envelope:
    """Plan every playlist in scope that is not 1 to N, ask, then number them and read them back."""
    cfg = load_config(("write.numbers_cli",))
    spec = confirm_gate(ctx.entry, CONFIRM_GATE, origin=_ORIGIN)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg, list(getattr(ctx.args, "playlist", None) or []))
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_notes(plan))
    if not plan.writes:
        nothing = {
            "code": NOTHING_TO_WRITE,
            "message": (
                f"all {plan.scanned} playlist(s) read already number their live rows "
                f"1 to N, so nothing was written"
            ),
        }
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[nothing, *_notes(plan)])

    written = _write(cfg, plan)
    numbers.assert_read_back(written)
    data["totals"] = {**data["totals"], "written": written.moved, "read_back": written.playlists}
    done = {
        "code": NUMBERS_WRITTEN,
        "message": (
            f"{written.playlists} playlist(s) now number their live rows 1 to N, "
            f"{written.moved} row(s) moved, read back from the database; no track "
            f"joined or left a playlist; undo with a restore of session {written.session_id}"
        ),
    }
    return ctx.envelope(data=data, warnings=[done, *_notes(plan)])


__all__ = [
    "CONFIRM_GATE", "NOTHING_TO_WRITE", "NUMBERS_HELD", "NUMBERS_WRITTEN", "build",
    "repair_numbers",
]
