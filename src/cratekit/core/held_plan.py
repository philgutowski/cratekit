"""A run's plan, held between the commands that answer its gates (U209).

Planning again at every gate answer cost thousands of provider calls, so the
planning command holds its plan here and later commands read it back.
**THE CODEC IS CLOSED**, decoding only through the caller's ``registry``, never
by import or unpickling. **A PLAN IS HELD ONLY WHEN IT READS BACK EQUAL TO
ITSELF**, and every failed read is a reason on which the caller plans again.
:class:`Steps` records each write step as it lands (U210), and :func:`carry`
keeps one item's steps past its run (R-1372).
"""

from __future__ import annotations

import dataclasses
import hashlib
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

#: A run answered within it reads its plan back; one answered after it plans again.
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
    """Hold ``plan`` for ``run_id``, answering why not, or the empty string when held."""
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
    """The held plan as ``(plan, digest, extra, "")``, or ``(None, "", {}, why)``."""
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


# The write's steps, recorded as each one lands (U210)

#: What a run's steps file is named by, beside its held plan.
STEPS_SUFFIX = ".steps.json"

#: The steps document's own schema version.
STEPS_VERSION = 1


def steps_path(run_id: str) -> Path:
    """One run's steps, a sibling of its held plan."""
    return config.state_path(STATE_KEY) / f"{run_id}{STEPS_SUFFIX}"


class Steps:
    """The steps one run's write has finished, by item and step (U210).

    Each is recorded atomically before the next starts and an unrecordable one
    stops the write, so a continue never repeats a step. ``digest`` binds them to one plan.
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
    """The steps recorded for ``run_id`` against ``digest``, or none and why when unusable."""
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


def recorded_steps(*, now: float | None = None) -> tuple[list[Steps], list[str]]:
    """Every run's steps still kept, and why any could not be read (U225).

    An unreadable record is NAMED in the second list, never read as no write.
    """
    directory = config.state_path(STATE_KEY)
    cutoff = (time.time() if now is None else now) - KEEP.total_seconds()
    try:
        found = sorted(directory.glob(f"*{STEPS_SUFFIX}"))
    except OSError as exc:
        return [], [f"the runs' steps could not be listed ({type(exc).__name__}: {exc})"]
    records: list[Steps] = []
    problems: list[str] = []
    for one in found:
        run_id = one.name[: -len(STEPS_SUFFIX)]
        try:
            if one.stat().st_mtime < cutoff:
                continue
            raw = json.loads(one.read_text())
        except FileNotFoundError:
            continue
        except (OSError, ValueError) as exc:
            problems.append(
                f"run {run_id}'s steps could not be read ({type(exc).__name__}: {exc})"
            )
            continue
        if not isinstance(raw, dict):
            problems.append(f"run {run_id}'s steps are not a JSON object")
            continue
        wrong = [
            key
            for key, wanted in (("version", STEPS_VERSION), ("run_id", run_id))
            if raw.get(key) != wanted
        ]
        if wrong:
            problems.append(
                f"run {run_id}'s steps record {wrong[0]} {raw.get(wrong[0])!r}"
            )
            continue
        done = raw.get("steps")
        if not isinstance(done, dict) or not all(isinstance(item, dict) for item in done.values()):
            problems.append(f"run {run_id}'s steps are not one record per item")
            continue
        records.append(Steps(run_id, str(raw.get("digest") or ""), done))
    return records, problems


# One item's steps, carried past its run (R-1372)

#: The directory, beneath the held plans, that carried records are kept in.
CARRIED_DIR = "carried"

#: A carried record's own schema version.
CARRIED_VERSION = 1


def carried_dir() -> Path:
    """Where carried records are kept: beneath the held plans, out of :func:`prune`'s reach."""
    return config.state_path(STATE_KEY) / CARRIED_DIR


def carried_path(run_id: str, key: str) -> Path:
    """One run's carried record of one item. The key is the caller's, so it is hashed."""
    name = hashlib.sha256(str(key).encode()).hexdigest()[:24]
    return carried_dir() / f"{run_id}.{name}.json"


def carry(steps: Steps, key: str) -> None:
    """Keep ``steps`` for ``key`` past its run, atomically, until :func:`let_go`."""
    document = {
        "version": CARRIED_VERSION,
        "run_id": steps.run_id,
        "digest": steps.digest,
        "key": str(key),
        "steps": dict(steps.done.get(str(key), {})),
    }
    payload = json.dumps(document, sort_keys=True, allow_nan=False).encode() + b"\n"
    config.atomic_write_bytes(payload, carried_path(steps.run_id, key))


def let_go(run_id: str, key: str) -> bool:
    """Let go of one carried record, and answer whether it is gone; one never carried is."""
    try:
        carried_path(run_id, key).unlink(missing_ok=True)
    except OSError:
        return False
    return True


def carried_step(run_id: str, key: str, step: str) -> Any:
    """One step of one run's carried record of one item, or None when it has none or cannot be read (U231)."""
    try:
        raw = json.loads(carried_path(run_id, key).read_text())
    except (OSError, ValueError):
        return None
    if not isinstance(raw, dict) or raw.get("run_id") != run_id or raw.get("key") != str(key):
        return None
    steps = raw.get("steps")
    return steps.get(step) if isinstance(steps, dict) else None


def carried() -> tuple[list[Steps], list[str]]:
    """Every carried record whatever its age, and why any could not be read.

    An unreadable record is NAMED in the second list, never read as no record.
    """
    # LISTED WITH ``iterdir``, since ``glob`` answers an unlistable directory as empty.
    try:
        found = sorted(
            one for one in carried_dir().iterdir() if one.name.endswith(".json")
        )
    except FileNotFoundError:
        return [], []
    except OSError as exc:
        return [], [f"the carried steps could not be listed ({type(exc).__name__}: {exc})"]
    records: list[Steps] = []
    problems: list[str] = []
    for one in found:
        run_id = one.name.split(".", 1)[0]
        try:
            raw = json.loads(one.read_text())
        except FileNotFoundError:
            continue
        except (OSError, ValueError) as exc:
            problems.append(
                f"run {run_id}'s carried steps could not be read ({type(exc).__name__}: {exc})"
            )
            continue
        if not isinstance(raw, dict) or raw.get("version") != CARRIED_VERSION:
            problems.append(f"run {run_id}'s carried steps are not a record this version reads")
            continue
        key = raw.get("key")
        steps = raw.get("steps")
        if (
            raw.get("run_id") != run_id
            or not isinstance(key, str)
            or not key
            or carried_path(run_id, key) != one
        ):
            problems.append(f"run {run_id}'s carried steps are not where their run and item name")
            continue
        if not isinstance(steps, dict):
            problems.append(f"run {run_id}'s carried steps are not one item's record")
            continue
        records.append(Steps(run_id, str(raw.get("digest") or ""), {key: steps}))
    return records, problems


__all__ = [
    "CARRIED_DIR",
    "CARRIED_VERSION",
    "KEEP",
    "STATE_KEY",
    "STEPS_SUFFIX",
    "STEPS_VERSION",
    "Steps",
    "Unheld",
    "VERSION",
    "carried",
    "carried_dir",
    "carried_step",
    "carried_path",
    "carry",
    "decode",
    "encode",
    "hold",
    "let_go",
    "load",
    "load_steps",
    "path",
    "prune",
    "recorded_steps",
    "release",
    "steps_path",
]
