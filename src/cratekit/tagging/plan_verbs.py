"""What ``tag rows``, ``remap``, ``suggest``, ``backlog`` and ``guess`` each copied (U306).

Each verb keeps its own messages, gate lookup and origin. Layer: modules. It
names :mod:`cratekit.cli.output` and nothing else from the command-line layer,
for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import config, rb_writer
from cratekit.core.cause import CratekitError, Outcome
from cratekit.tagging import published, searchers, suggest
from cratekit.write import metadata_cli

#: How many words, paths or identifiers a sentence names. The detail carries all.
NAMED = 5


def named(values: Sequence[str]) -> str:
    """The first few of ``values`` as a clause, and how many more there are."""
    shown = ", ".join(values[:NAMED])
    more = len(values) - NAMED
    return shown + (f" and {more} more" if more > 0 else "")


def warning(code: str, message: str) -> dict[str, str]:
    """One entry on an envelope's warnings channel."""
    return {"code": code, "message": message}


def counted(counts: Mapping[str, int], names: Sequence[str]) -> str:
    """Each named outcome that happened, with its count."""
    return ", ".join(f"{counts[name]} {name}" for name in names if counts[name])


@contextmanager
def reading(cfg: config.Config, blocked: str) -> Iterator[Any]:
    """A handle opened to read, ``require_closed`` off so rekordbox may be open,
    closed on the way out. A library mostly under no prefix rule refuses first
    (R-372), through the vocal tag verb's own path survey."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        totals = metadata_cli.resolution_totals(cfg, db)
        if totals.majority_unmapped:
            raise CratekitError(
                metadata_cli.majority_unmapped_cause(cfg, totals, blocked=blocked)
            )
        yield db
    finally:
        rb_writer.close_db(db)


def kept(cfg: config.Config, declared) -> suggest.KeptCatalogue:
    """The catalogue lookup ``tag suggest --catalogue`` asks, answers kept, naming
    what this run cannot ask (U244)."""
    return suggest.KeptCatalogue(
        cfg,
        suggest.catalogue_lookup(
            searchers.for_taxonomy(declared), published.for_suggestions(declared)
        ),
        unasked=frozenset({searchers.DISCOGS} if searchers.for_discogs().token is None else ()),
    )


def payload(plan, **totals: Any) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    return {
        "digest": plan.digest,
        "items": [item.to_json() for item in plan.items],
        "totals": {"count": len(plan.items), **totals, "written": 0, "read_back": 0},
        "chunk": None,
    }


def applied(
    ctx,
    plan,
    data: dict[str, Any],
    advisories: Callable[[Any], list[dict[str, str]]],
    *,
    nothing: Callable[[Any], dict[str, str]],
    apply: Callable[[], Any],
    said: Callable[[Any], dict[str, str]],
) -> Envelope:
    """What a gate answered ``apply`` ends in: a no op over a plan that writes
    nothing, else the write, its counts and what it did ahead of the advisories."""
    if not plan.writes:
        return ctx.envelope(
            data=data, outcome=Outcome.NO_OP, warnings=[nothing(plan), *advisories(plan)]
        )
    written = apply()
    data["totals"] = {**data["totals"], "written": written.written, "read_back": written.read_back}
    return ctx.envelope(data=data, warnings=[said(written), *advisories(plan)])


__all__ = ["NAMED", "applied", "counted", "kept", "named", "payload", "reading", "warning"]
