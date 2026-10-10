"""``crate taxonomy upgrade``: the shipped classes and buckets a library's copy lacks, added (U132).

Setup copies the shipped template beside the database once, and nothing the
shipped template gains afterwards reaches the library on its own. This verb
plans what the copy lacks through ``core.taxonomy_upgrade``, shows each entry
it adds and each it holds at an explicit gate, and writes the copy with them
added, keeping the copy as it was in a dated file beside it.

THE ORDER IS THE PROFILE VERB'S, with a backup: the plan from the copy as it
stands, the gate over the digested plan, the plan taken again and refused as
stale when its digest moved, the copy as it was written beside it under the
date, the new copy written atomically, and the copy read back through the one
loader every verb reads it with, so a copy that would not route is reported
here and not by the next verb.

THE DIGEST COVERS THE TWO TEXTS AND THE ITEMS, never the path, so a rehearsal
on a disposable copy of the same file matches the live plan.

Layer: cli.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import gates, output, registry
from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, config, taxonomy, taxonomy_upgrade
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Remedy, refuse

if TYPE_CHECKING:  # pragma: no cover
    from cratekit.cli import Context

#: The gate, explicit: the copy is the declaration every verb routes by.
APPLY_GATE = "taxonomy.upgrade.apply"

#: The notes the verb carries on its warnings channel.
UPGRADED = "taxonomy-upgraded"
HELD = "taxonomy-upgrade-held"
NOTHING_TO_UPGRADE = "taxonomy-nothing-to-upgrade"

_ORIGIN = ("cli", "verbs", "taxonomy")


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
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


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.set_defaults(_handler=taxonomy_upgrade_verb)


def _apply_gate(entry: registry.Entry) -> registry.GateSpec:
    for spec in entry.gates:
        if spec.name == APPLY_GATE:
            return spec
    raise RuntimeError(f"registry entry {entry.name!r} declares no gate {APPLY_GATE!r}")


def items(found: taxonomy_upgrade.Plan) -> list[dict[str, Any]]:
    """Each change the plan makes and each entry it holds, in the order they are tried."""
    out: list[dict[str, Any]] = []
    if found.to_version != found.from_version:
        out.append(
            {
                "kind": "schema_version",
                "id": str(found.to_version),
                "change": "raise",
                "from": found.from_version,
            }
        )
    out += [{"kind": taxonomy_upgrade.SUB_CLASS, "id": i, "change": "add"} for i in found.classes]
    out += [{"kind": taxonomy_upgrade.BUCKET, "id": i, "change": "add"} for i in found.buckets]
    out += [
        {"kind": one.kind, "id": one.id, "change": "held", "reasons": list(one.reasons)}
        for one in found.held
    ]
    return out


def payload(found: taxonomy_upgrade.Plan) -> dict[str, Any]:
    """The ``plan/1`` payload: the items, their totals, and the digest over both texts."""
    listed = items(found)
    digest = output.digest_of(
        {
            "before": taxonomy.template_digest(found.before),
            "after": taxonomy.template_digest(found.after),
            "items": listed,
        }
    )
    return {
        "digest": digest,
        "items": listed,
        "totals": {
            "from_version": found.from_version,
            "to_version": found.to_version,
            "shipped_version": found.shipped_version,
            "classes": len(found.classes),
            "buckets": len(found.buckets),
            "held": len(found.held),
        },
        "chunk": None,
    }


def _held(found: taxonomy_upgrade.Plan) -> list[dict[str, str]]:
    return [
        {
            "code": HELD,
            "message": (
                f"{one.kind} {one.id} from the shipped {found.template!r} template was not "
                f"added: {'; '.join(one.reasons)}; then run {taxonomy_upgrade.VERB} again"
            ),
        }
        for one in found.held
    ]


def backup_path(path: Path, now: datetime) -> Path:
    """A dated name beside the copy that no earlier backup holds."""
    stamp = now.strftime("%Y-%m-%dT%H%M%S")
    candidate = path.with_name(f"{path.name}.{stamp}.bak")
    count = 1
    while candidate.exists():
        candidate = path.with_name(f"{path.name}.{stamp}.{count}.bak")
        count += 1
    return candidate


def as_read(raw: bytes) -> str | None:
    """``raw`` as the loader reads it, line endings folded to LF, or None when not UTF-8."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    return text.replace("\r\n", "\n").replace("\r", "\n")


def newline(raw: bytes) -> str:
    """The copy's line ending: CRLF when every line ends in one, LF otherwise."""
    lines = raw.count(b"\n")
    crlf = raw.count(b"\r\n")
    return "\r\n" if lines and crlf == lines and raw.count(b"\r") == crlf else "\n"


def _read_back(cfg: config.Config, path: Path, written: bytes) -> str | None:
    """Why the copy at ``path`` is not the one written, or None when it is and it loads.

    A copy that is not UTF-8 reaches the loader, which refuses it by cause.
    """
    try:
        if path.read_bytes() != written:
            return "the bytes on disk are not the bytes written"
        active_taxonomy.load(cfg)
    except CratekitError as exc:
        return exc.cause.message
    except OSError as exc:
        return str(exc)
    return None


def _restore(path: Path, raw: bytes) -> str | None:
    """Put ``raw`` back at ``path`` and read it back; why it did not take, or None."""
    try:
        config.atomic_write_bytes(raw, path)
        if path.read_bytes() != raw:
            return "the bytes on disk after it are not the copy as it was"
    except OSError as exc:
        return str(exc)
    return None


def taxonomy_upgrade_verb(ctx: "Context") -> Envelope:
    """Plan what the copy lacks, ask, keep the copy as it was, write, read back."""
    cfg = _load()
    path, found = taxonomy_upgrade.planned(cfg)
    spec = _apply_gate(ctx.entry)
    data = payload(found)
    warnings = _held(found)
    if not found.writes:
        # Nothing to decide, the profile verb's rule: a gate that asks about an
        # empty change trains people to answer without reading.
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                *warnings,
                {
                    "code": NOTHING_TO_UPGRADE,
                    "message": (
                        f"the copy at {path} states schema_version {found.from_version} "
                        f"and nothing the shipped {found.template!r} template declares "
                        f"can be added to it"
                        + (", past what is held above" if found.held else "")
                    ),
                },
            ],
        )
    context = {
        "template": found.template,
        "copy": str(path),
        "from_version": found.from_version,
        "to_version": found.to_version,
    }
    if ctx.gate.require(spec, plan=data, context=context) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)

    # TAKEN AGAIN AFTER THE ANSWER. A copy edited by hand between the screen
    # and the answer is another plan, and an answer given to the first one is
    # refused as stale rather than written over the edit.
    _, fresh = taxonomy_upgrade.planned(cfg)
    moved = payload(fresh)
    if moved["digest"] != data["digest"]:
        raise gates.DecisionStale(spec, ctx.run.run_id, data["digest"], moved["digest"])

    # THE BYTES ON DISK ARE WHAT IS KEPT AND PUT BACK. The planner reads the
    # copy as text, which folds CRLF to LF, so the copy is read again as bytes:
    # the backup and any restore are those bytes exactly, and the upgraded copy
    # keeps their line ending. Bytes that no longer read as the planned text
    # are an edit made after the second plan, refused as stale like one made
    # before it.
    raw = path.read_bytes()
    if as_read(raw) != fresh.before:
        # The copy's digest, not a plan's: there is no plan of bytes that changed.
        moved_to = taxonomy.template_digest(raw.decode("utf-8", errors="replace"))
        raise gates.DecisionStale(spec, ctx.run.run_id, data["digest"], moved_to)
    ending = newline(raw)
    written = fresh.after.replace("\n", ending).encode("utf-8")

    kept = backup_path(path, datetime.now())
    config.atomic_write_bytes(raw, kept)
    config.atomic_write_bytes(written, path)

    # READ BACK THROUGH THE LOADER every verb reads the copy with, so what was
    # written is what routes. A copy that does not read back is replaced by the
    # one it replaced, from the bytes this verb holds, so the library is never
    # left with a declaration every routing verb refuses. That restore is read
    # back too, and the refusal says whether it took: a disk that fills or a
    # volume that drops after the write can fail it, and then the person needs
    # the backup's path more than anything else this verb says.
    problem = _read_back(cfg, path, written)
    if problem is not None:
        failed = _restore(path, raw)
        if failed is None:
            outcome = f"so the copy as it was has been put back; it is also kept at {kept}"
        else:
            outcome = (
                f"and putting the copy as it was back failed too ({failed}), so {path} may "
                f"hold the text that did not read back; the copy as it was is kept at "
                f"{kept}, copy it over {path} by hand"
            )
        raise refuse(
            "internal-error",
            f"the upgraded copy at {path} did not read back ({problem}), {outcome}",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"path": str(path), "backup": str(kept), "restored": failed is None},
        )

    added = [*fresh.classes, *fresh.buckets]
    return ctx.envelope(
        data=data,
        warnings=[
            *warnings,
            {
                "code": UPGRADED,
                "message": (
                    f"the copy at {path} now states schema_version {fresh.to_version}"
                    + (f" and declares {', '.join(added)}" if added else "")
                    + f"; nothing it already declared was changed, and the copy as it "
                    f"was is at {kept}"
                    + (
                        "; its mixed line endings were written as LF, and the copy as it "
                        "was keeps its own"
                        if ending == "\n" and b"\r" in raw
                        else ""
                    )
                ),
            },
        ],
    )


__all__ = [
    "APPLY_GATE",
    "HELD",
    "NOTHING_TO_UPGRADE",
    "UPGRADED",
    "as_read",
    "backup_path",
    "build",
    "items",
    "newline",
    "payload",
    "taxonomy_upgrade_verb",
]
