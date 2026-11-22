"""``crate taxonomy upgrade``: the shipped classes, buckets and vocabulary tables a library's copy lacks, added (U132, U244).

Plans what the copy lacks, asks at an explicit gate, plans again and refuses
a stale answer, keeps a dated backup, writes atomically and reads the copy
back through the loader, so a copy that would not route is reported here. The
digest covers the two texts and the items, never the path, so a rehearsal on
a disposable copy matches the live plan.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import gates, output, registry
from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy, config, taxonomy, taxonomy_upgrade
from cratekit.core.cause import CratekitError, Outcome, Remedy, refuse

if TYPE_CHECKING:  # pragma: no cover
    from cratekit.cli import Context

#: The gate, explicit: the copy is the declaration every verb routes by.
APPLY_GATE = "taxonomy.upgrade.apply"

#: The notes the verb carries on its warnings channel.
UPGRADED = "taxonomy-upgraded"
HELD = "taxonomy-upgrade-held"
KEYWORD_RULE = "taxonomy-upgrade-keyword-rule"
NOTHING_TO_UPGRADE = "taxonomy-nothing-to-upgrade"

_ORIGIN = ("cli", "verbs", "taxonomy")


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    return load_config(_ORIGIN)


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
        {"kind": taxonomy_upgrade.VOCABULARY, "id": i, "change": "add"}
        for i in found.vocabularies
    ]
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
            "vocabularies": len(found.vocabularies),
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
    ] + [{"code": KEYWORD_RULE, "message": sentence} for sentence in found.keywords]


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


def write_copy(
    cfg: config.Config,
    spec: registry.GateSpec,
    run_id: str,
    path: Path,
    before: str,
    after: str,
    digest: str,
    *,
    what: str,
) -> tuple[Path, str, bytes]:
    """Keep the copy as it was, write ``after`` over it, and read it back through the loader.

    The one write for every verb that edits the copy (U194). Returns the
    backup's path, the line ending written, and the bytes the copy held. The
    backup and any restore are the exact bytes on disk, and the new copy keeps
    their line ending; bytes that no longer read as ``before`` are refused as
    stale. A copy that does not read back is restored, so no declaration every
    routing verb refuses is left, and the refusal says whether the restore took.
    """
    raw = path.read_bytes()
    if as_read(raw) != before:
        # The copy's digest, not a plan's: there is no plan of bytes that changed.
        moved_to = taxonomy.template_digest(raw.decode("utf-8", errors="replace"))
        raise gates.DecisionStale(spec, run_id, digest, moved_to)
    ending = newline(raw)
    written = after.replace("\n", ending).encode("utf-8")

    kept = backup_path(path, datetime.now())
    config.atomic_write_bytes(raw, kept)
    config.atomic_write_bytes(written, path)

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
            f"the {what} copy at {path} did not read back ({problem}), {outcome}",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"path": str(path), "backup": str(kept), "restored": failed is None},
        )
    return kept, ending, raw


def taxonomy_upgrade_verb(ctx: "Context") -> Envelope:
    """Plan what the copy lacks, ask, keep the copy as it was, write, read back."""
    cfg = _load()
    path, found = taxonomy_upgrade.planned(cfg)
    spec = _apply_gate(ctx.entry)
    data = payload(found)
    warnings = _held(found)
    if not found.writes:
        # No gate over an empty change, which trains people to answer unread.
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

    # Planned again after the answer, so a hand edit in between makes it stale.
    _, fresh = taxonomy_upgrade.planned(cfg)
    moved = payload(fresh)
    if moved["digest"] != data["digest"]:
        raise gates.DecisionStale(spec, ctx.run.run_id, data["digest"], moved["digest"])

    kept, ending, raw = write_copy(
        cfg, spec, ctx.run.run_id, path, fresh.before, fresh.after, data["digest"], what="upgraded"
    )

    added = [
        *fresh.classes,
        *fresh.buckets,
        *(f"[{taxonomy_upgrade.VOCABULARY}.{source}]" for source in fresh.vocabularies),
    ]
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
    "write_copy",
]
