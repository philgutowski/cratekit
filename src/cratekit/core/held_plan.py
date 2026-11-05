"""A run's plan, held between the commands that answer its gates (U209).

WHY THIS EXISTS. An explicit gate is answered by a separate act, so a verb
with two of them runs three times: once to show the first gate, once after
each answer. Each run planned again from the top, and the gates' digest
comparison was the only thing that noticed a list moving. Sitting 54 measured
what that costs on the playlist pair sync over 101 playlists: the plan was 2,500
to 4,200 provider calls, and every answer paid it again. So the command that
plans holds its plan here under its run, and every later command of the run
reads it back instead of planning.

**THE CODEC IS CLOSED.** A plan is a graph of dataclasses. It is written as
tagged JSON, and read back only through the classes the caller names in a
``registry``, by name, never imported by name and never unpickled, so a held
file can build nothing the verb did not list. This module names no feature
package, which the layering forbids; the registry is the caller's.

**A PLAN IS HELD ONLY WHEN IT READS BACK EQUAL TO ITSELF.** ``hold`` encodes,
decodes, and compares, so a class with a field the codec cannot carry is
caught at the moment it is held rather than when a later command reads a
plan that is not the one shown. A value of a type the codec does not know
refuses the hold the same way.

**WHAT IS READ BACK IS CHECKED, AND EVERY FAILURE IS A REASON, NEVER A
GUESS.** :func:`load` answers the plan, or None and why: no file, a file of
another version, kind or run, one that does not decode, or one whose plan
digests other than the digest held beside it. The caller compares that
digest with the offers its run recorded and plans again on any reason, so a
plan that cannot be held costs a plan, never a write the person did not see.

Layer: core.
"""

from __future__ import annotations

import dataclasses
import json
import time
from collections.abc import Callable, Mapping
from datetime import datetime, timedelta
from pathlib import Path
from types import MappingProxyType
from typing import Any

from cratekit.cli.output import timestamp
from cratekit.core import config

#: The declared state directory, a sibling of the run records.
STATE_KEY = "held_plans"

#: The held document's own schema version.
VERSION = 1

#: How long a held plan whose run never finished is kept. A run answered
#: within it reads its plan back; one answered after it plans again.
KEEP = timedelta(days=30)

#: The key a tagged value carries, and its value's key.
TAG = "$"
VALUE = "v"
NAME = "n"


class Unheld(ValueError):
    """A value the codec cannot carry, or a document it cannot read back."""


def _sort_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def encode(value: Any, registry: Mapping[str, type]) -> Any:
    """``value`` as tagged JSON, its dataclasses named by ``registry``."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, datetime):
        return {TAG: "datetime", VALUE: value.isoformat()}
    if isinstance(value, tuple):
        return {TAG: "tuple", VALUE: [encode(one, registry) for one in value]}
    if isinstance(value, list):
        return [encode(one, registry) for one in value]
    if isinstance(value, (frozenset, set)):
        items = sorted((encode(one, registry) for one in value), key=_sort_key)
        return {TAG: "frozenset" if isinstance(value, frozenset) else "set", VALUE: items}
    if isinstance(value, (dict, MappingProxyType)):
        return {
            TAG: "dict",
            VALUE: [[encode(key, registry), encode(one, registry)] for key, one in value.items()],
        }
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        kind = type(value)
        name = kind.__name__
        if registry.get(name) is not kind:
            raise Unheld(f"{kind.__module__}.{name} is not a class this plan may hold")
        fields = dataclasses.fields(value)
        unset = [one.name for one in fields if not one.init]
        if unset:
            raise Unheld(f"{name} carries {unset}, which its constructor does not take")
        return {
            TAG: "dataclass",
            NAME: name,
            VALUE: {one.name: encode(getattr(value, one.name), registry) for one in fields},
        }
    raise Unheld(f"a {type(value).__name__} is not a value a held plan can carry")


def decode(value: Any, registry: Mapping[str, type]) -> Any:
    """The value :func:`encode` wrote, built through ``registry`` and nothing else."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, list):
        return [decode(one, registry) for one in value]
    if not isinstance(value, dict) or TAG not in value:
        raise Unheld(f"{type(value).__name__} is not a value a held plan writes")
    tag = value[TAG]
    inner = value.get(VALUE)
    try:
        if tag == "datetime":
            return datetime.fromisoformat(inner)
        if tag == "tuple":
            return tuple(decode(one, registry) for one in inner)
        if tag == "frozenset":
            return frozenset(decode(one, registry) for one in inner)
        if tag == "set":
            return {decode(one, registry) for one in inner}
        if tag == "dict":
            return {decode(key, registry): decode(one, registry) for key, one in inner}
        if tag == "dataclass":
            kind = registry.get(str(value.get(NAME)))
            if kind is None:
                raise Unheld(f"{value.get(NAME)!r} is not a class this plan may hold")
            return kind(**{str(key): decode(one, registry) for key, one in inner.items()})
    except Unheld:
        raise
    except (TypeError, ValueError, AttributeError) as exc:
        raise Unheld(f"a {tag} did not read back ({type(exc).__name__}: {exc})") from None
    raise Unheld(f"{tag!r} is not a tag a held plan writes")


def path(run_id: str) -> Path:
    """One run's held plan. The identifier is generated, so it needs no escaping."""
    return config.state_path(STATE_KEY) / f"{run_id}.json"


def hold(
    run_id: str,
    kind: str,
    plan: Any,
    *,
    registry: Mapping[str, type],
    digest: str,
    extra: Mapping[str, Any] | None = None,
) -> str:
    """Hold ``plan`` for ``run_id``, and answer why not, or the empty string when held.

    ``digest`` is the plan's digest as its gates offer it, and ``extra`` is
    plain JSON the verb reads back beside the plan. A plan that does not read
    back equal to itself is not held. A held plan older than :data:`KEEP` is
    pruned here, the one moment this directory is written.
    """
    try:
        encoded = encode(plan, registry)
        if decode(encoded, registry) != plan:
            return "the plan did not read back equal to itself, so it was not held"
        document = {
            "version": VERSION,
            "kind": kind,
            "run_id": run_id,
            "digest": digest,
            "held": timestamp(),
            "extra": dict(extra or {}),
            "plan": encoded,
        }
        payload = json.dumps(document, sort_keys=True, allow_nan=False).encode() + b"\n"
    except (Unheld, ValueError, TypeError) as exc:
        return f"the plan could not be held ({exc})"
    try:
        config.atomic_write_bytes(payload, path(run_id))
    except OSError as exc:
        return f"the plan could not be written ({type(exc).__name__}: {exc})"
    prune(keep=run_id)
    return ""


def load(
    run_id: str,
    kind: str,
    *,
    registry: Mapping[str, type],
    digest_of: Callable[[Any], str],
) -> tuple[Any, str, dict[str, Any], str]:
    """The plan held for ``run_id``, its digest, its extra, and why not when there is none.

    Answers ``(plan, digest, extra, "")`` or ``(None, "", {}, why)``. The
    digest is checked against ``digest_of(plan)`` here; comparing it with the
    run's offers is the caller's, which knows its gates.
    """
    where = path(run_id)
    try:
        age = time.time() - where.stat().st_mtime
        raw = json.loads(where.read_text())
    except FileNotFoundError:
        return None, "", {}, "no plan is held for this run"
    except (OSError, ValueError) as exc:
        return None, "", {}, f"the held plan could not be read ({type(exc).__name__}: {exc})"
    if age > KEEP.total_seconds():
        # OLDER THAN IT IS KEPT is no plan, whether or not a prune reached it.
        return None, "", {}, f"the held plan is older than {KEEP.days} days"
    if not isinstance(raw, dict):
        return None, "", {}, "the held plan is not a JSON object"
    for key, wanted in (("version", VERSION), ("kind", kind), ("run_id", run_id)):
        if raw.get(key) != wanted:
            return None, "", {}, f"the held plan's {key} is {raw.get(key)!r}, not {wanted!r}"
    try:
        plan = decode(raw.get("plan"), registry)
    except Unheld as exc:
        return None, "", {}, f"the held plan did not read back ({exc})"
    held = str(raw.get("digest") or "")
    try:
        actual = digest_of(plan)
    except Exception as exc:  # noqa: BLE001 - a plan that cannot digest is no plan
        return None, "", {}, f"the held plan could not be digested ({type(exc).__name__}: {exc})"
    if actual != held:
        return None, "", {}, "the held plan does not digest as it did when it was held"
    extra = raw.get("extra")
    return plan, held, dict(extra) if isinstance(extra, dict) else {}, ""


def release(run_id: str) -> None:
    """Let go of a run's held plan, once the run has written or stopped."""
    try:
        path(run_id).unlink(missing_ok=True)
    except OSError:
        pass


def prune(*, keep: str = "", now: float | None = None) -> int:
    """Remove held plans older than :data:`KEEP`, except ``keep``'s. Returns how many."""
    directory = config.state_path(STATE_KEY)
    cutoff = (time.time() if now is None else now) - KEEP.total_seconds()
    removed = 0
    try:
        found = sorted(directory.glob("*.json"))
    except OSError:
        return 0
    for one in found:
        if one.stem == keep:
            continue
        try:
            if one.stat().st_mtime < cutoff:
                one.unlink()
                removed += 1
        except OSError:
            continue
    return removed


__all__ = [
    "KEEP",
    "STATE_KEY",
    "Unheld",
    "VERSION",
    "decode",
    "encode",
    "hold",
    "load",
    "path",
    "prune",
    "release",
]
