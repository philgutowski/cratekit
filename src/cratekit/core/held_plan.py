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

**AND THE WRITE'S STEPS, AS EACH LANDS (U210).** A write over a hundred
playlists can stop part way, on the call ceiling or anything else that parks
it. :class:`Steps` records each step of each item the moment it lands, in a
sibling file bound to the held plan's digest, so a continue of the run starts
each item at its first unfinished step under the plan and the answers already
given. Steps that cannot be read are no steps, and the reason is said: the
continue then reads every list as the plan read it, so anything already
written refuses stale rather than being written twice.

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
        raw = json.loads(where.read_text())
    except FileNotFoundError:
        return None, "", {}, "no plan is held for this run"
    except (OSError, ValueError) as exc:
        return None, "", {}, f"the held plan could not be read ({type(exc).__name__}: {exc})"
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
    """Let go of a run's held plan and its write's steps (U210), once the run has written or stopped."""
    for one in (path(run_id), steps_path(run_id)):
        try:
            one.unlink(missing_ok=True)
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
        # A RUN'S STEPS ARE ITS PLAN'S (U210), so ``keep`` keeps both.
        if one.name.split(".", 1)[0] == keep:
            continue
        try:
            if one.stat().st_mtime < cutoff:
                one.unlink()
                removed += 1
        except OSError:
            continue
    return removed


# ---------------------------------------------------------------------------
# The write's steps, recorded as each one lands (U210)
# ---------------------------------------------------------------------------

#: What a run's steps file is named by, beside its held plan.
STEPS_SUFFIX = ".steps.json"

#: The steps document's own schema version.
STEPS_VERSION = 1


def steps_path(run_id: str) -> Path:
    """One run's steps, a sibling of its held plan."""
    return config.state_path(STATE_KEY) / f"{run_id}{STEPS_SUFFIX}"


class Steps:
    """The steps one run's write has finished, by item and step (U210).

    WHY. A write over a hundred playlists can stop part way, on the call
    ceiling or anything else that parks it, and a continue of the run must
    start each item at its first unfinished step rather than plan again. So
    each step is recorded the moment it lands and before the next starts,
    written whole and atomically, and a step whose record could not be
    written stops the write: a step done and not recorded is read by the
    continue as not done, which the check before the write refuses stale
    rather than doing it twice.

    ``digest`` is the held plan's, so steps recorded against one plan are
    never read for another.
    """

    def __init__(
        self, run_id: str, digest: str, done: Mapping[str, Mapping[str, Any]] | None = None
    ) -> None:
        self.run_id = run_id
        self.digest = digest
        self.done: dict[str, dict[str, Any]] = {
            str(key): dict(value) for key, value in (done or {}).items()
        }

    def has(self, key: str, step: str) -> bool:
        return step in self.done.get(key, {})

    def get(self, key: str, step: str, default: Any = None) -> Any:
        return self.done.get(key, {}).get(step, default)

    def started(self) -> bool:
        """Whether any step of any item was recorded."""
        return any(self.done.values())

    def keys_with(self, step: str) -> list[str]:
        return sorted(key for key, value in self.done.items() if step in value)

    def mark(self, key: str, step: str, value: Any = True) -> None:
        """Record one step of one item. An ``OSError`` writing it is the caller's to refuse."""
        self.done.setdefault(str(key), {})[step] = value
        self._write()

    def begin(self) -> None:
        """Write the record before the first write, so an unwritable one refuses first."""
        self._write()

    def _write(self) -> None:
        document = {
            "version": STEPS_VERSION,
            "run_id": self.run_id,
            "digest": self.digest,
            "steps": self.done,
        }
        payload = json.dumps(document, sort_keys=True, allow_nan=False).encode() + b"\n"
        config.atomic_write_bytes(payload, steps_path(self.run_id))


def load_steps(run_id: str, digest: str) -> tuple[Steps, str]:
    """The steps recorded for ``run_id`` against the plan of ``digest``, and why none when unusable.

    No file is no step yet, and says nothing. A file that cannot be read, of
    another version or run, or recorded against another plan answers no steps
    AND the reason, which the caller says: the continue then reads every list
    as the plan read it, so anything already written refuses stale rather
    than being written again.
    """
    fresh = Steps(run_id, digest)
    where = steps_path(run_id)
    try:
        raw = json.loads(where.read_text())
    except FileNotFoundError:
        return fresh, ""
    except (OSError, ValueError) as exc:
        return fresh, f"the run's steps could not be read ({type(exc).__name__}: {exc})"
    if not isinstance(raw, dict):
        return fresh, "the run's steps are not a JSON object"
    for key, wanted in (("version", STEPS_VERSION), ("run_id", run_id), ("digest", digest)):
        if raw.get(key) != wanted:
            return fresh, f"the run's steps record {key} {raw.get(key)!r}, not {wanted!r}"
    done = raw.get("steps")
    if not isinstance(done, dict) or not all(isinstance(one, dict) for one in done.values()):
        return fresh, "the run's steps are not one record per item"
    return Steps(run_id, digest, done), ""


__all__ = [
    "KEEP",
    "STATE_KEY",
    "STEPS_SUFFIX",
    "STEPS_VERSION",
    "Steps",
    "Unheld",
    "VERSION",
    "decode",
    "encode",
    "hold",
    "load",
    "load_steps",
    "path",
    "prune",
    "release",
    "steps_path",
]
