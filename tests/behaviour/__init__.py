"""Behaviour scenarios: what `crate` prints and writes, captured for comparison (U297).

`scripts/behaviour_compare.py capture` runs these files as a pytest run of their
own and `compare` reads two captures; not named ``test_*.py``, the suite never
collects them.

One file per package, so two cards never edit the same one; a second suite's
``machine`` lives in a file named for the package and the verb, as
``tagging_rows.py`` does (U298). A scenario takes the ``stage`` fixture and
drives commands through it, ``stage.crate("tag", "remap")``. Its fixtures are
the suite's own, imported, never new builders. Assert what the scenario
depends on, an exit code or a job id, so broken setup fails the capture
instead of recording a refusal as the behaviour.

This module holds the pinned clock, the counted ids and the ``Stage``;
``conftest.py`` puts them around every scenario.
"""

from __future__ import annotations

import contextlib
import datetime as datetime_module
import hashlib
import io
import json
import os
import random
import secrets
import sys
import time
import types
import uuid
from dataclasses import dataclass, field
from pathlib import Path

#: The one instant every scenario runs at. Late enough that the fixtures'
#: recorded dates, a pin validated in August 2026 among them, are in its past.
INSTANT = datetime_module.datetime(2026, 11, 21, 12, 0, 0, tzinfo=datetime_module.timezone.utc)

#: The packages whose own names for the clock and the id sources are re-pointed,
#: since they may already hold ``from datetime import datetime``.
SWEPT = ("cratekit", "tests", "pyrekordbox")

_REAL_DATETIME = datetime_module.datetime
_REAL_DATE = datetime_module.date

#: Whether the pins are on. Every pinned name asks each call and answers as the
#: real one when they are off, so a reference that outlives the scenario is real.
_PINS = {"on": False}


class _Pinned(type):
    """Makes a pinned class stand for the real one in ``isinstance`` and ``issubclass``,
    since its constructor returns the real type's instances."""

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, cls._real)

    def __subclasscheck__(cls, subclass) -> bool:
        return issubclass(subclass, cls._real)


class PinnedDatetime(_REAL_DATETIME, metaclass=_Pinned):
    """``datetime`` with ``now``, ``utcnow`` and ``today`` answering one instant."""

    _real = _REAL_DATETIME

    def __new__(cls, *args, **kwargs):
        return _REAL_DATETIME(*args, **kwargs)

    @classmethod
    def now(cls, tz=None):
        if not _PINS["on"]:
            return _REAL_DATETIME.now(tz)
        if tz is None:
            return INSTANT.astimezone().replace(tzinfo=None)
        return INSTANT.astimezone(tz)

    @classmethod
    def utcnow(cls):
        return cls.now(datetime_module.timezone.utc).replace(tzinfo=None)

    @classmethod
    def today(cls):
        return cls.now()


class PinnedDate(_REAL_DATE, metaclass=_Pinned):
    """``date`` with ``today`` answering the pinned instant's day."""

    _real = _REAL_DATE

    def __new__(cls, *args, **kwargs):
        return _REAL_DATE(*args, **kwargs)

    @classmethod
    def today(cls):
        return PinnedDatetime.now().date()


class Counted:
    """Ids from a counted sequence, so the nth id a scenario mints is always the same.

    A sequence keeps ids distinct; one more id minted, or two in another order,
    shows as a difference in every id after it, to be explained, not ignored.
    """

    def __init__(self) -> None:
        self.count = 0

    def _next(self, kind: str) -> bytes:
        self.count += 1
        return hashlib.sha256(f"{kind} {self.count}".encode()).digest()

    def token_bytes(self, nbytes=None) -> bytes:
        wanted = 32 if nbytes is None else nbytes
        block = b""
        while len(block) < wanted:
            block += self._next("token")
        return block[:wanted]

    def token_hex(self, nbytes=None) -> str:
        return self.token_bytes(nbytes).hex()

    def uuid4(self) -> uuid.UUID:
        return uuid.UUID(bytes=self._next("uuid")[:16], version=4)


def pin(patch):
    """Hold the clock at ``INSTANT`` and draw ids from a fresh count, through ``patch``.

    The returned callable takes the pins off again, the ``random`` seed
    included. The monotonic clocks stand still, so a wait never times out. File
    times are set by ``Stage.settle``; the process id and inodes are the
    capture's own, which ``compare`` knows by name.
    """
    if _PINS["on"]:
        raise RuntimeError("the pins are already on, and one scenario runs at a time")
    counted = Counted()
    stamp = INSTANT.timestamp()

    def held(real, pinned):
        """``pinned`` while the pins are on, and ``real`` itself once they are off."""

        def answer(*args, **kwargs):
            return pinned(*args, **kwargs) if _PINS["on"] else real(*args, **kwargs)

        return answer

    pairs = (
        (datetime_module, "datetime", PinnedDatetime),
        (datetime_module, "date", PinnedDate),
        (time, "time", held(time.time, lambda: stamp)),
        (time, "time_ns", held(time.time_ns, lambda: int(stamp) * 1_000_000_000)),
        (time, "monotonic", held(time.monotonic, lambda: 0.0)),
        (time, "monotonic_ns", held(time.monotonic_ns, lambda: 0)),
        (time, "perf_counter", held(time.perf_counter, lambda: 0.0)),
        (time, "perf_counter_ns", held(time.perf_counter_ns, lambda: 0)),
        (uuid, "uuid4", held(uuid.uuid4, counted.uuid4)),
        (secrets, "token_hex", held(secrets.token_hex, counted.token_hex)),
        (secrets, "token_bytes", held(secrets.token_bytes, counted.token_bytes)),
    )
    pinned = {id(getattr(module, name)): replacement for module, name, replacement in pairs}
    for module_name, module in list(sys.modules.items()):
        if module is None or module_name.split(".")[0] not in SWEPT:
            continue
        if module_name == __name__:
            continue  # this module's own names for the real classes stay real
        for name, value in list(vars(module).items()):
            replacement = pinned.get(id(value))
            if replacement is not None:
                patch.setattr(module, name, replacement)
    real = {id(replacement): getattr(module, name) for module, name, replacement in pairs}
    for module, name, replacement in pairs:
        patch.setattr(module, name, replacement)
    pin_binding_stamps(patch)
    state = random.getstate()
    random.seed(0)
    _PINS["on"] = True

    def unpin() -> None:
        """Turn the pins off, then put the real name back wherever a pinned one is
        held, since a module imported under the pins took a pinned name as its own."""
        _PINS["on"] = False
        random.setstate(state)
        held = real.keys()
        for module in list(sys.modules.values()):
            if not isinstance(module, types.ModuleType) or module.__name__ == __name__:
                continue
            # Most modules hold no pinned name, and asking that of the ids at
            # once is a fifth of the cost of the loop below (U336).
            if held.isdisjoint(map(id, list(vars(module).values()))):
                continue
            for name, value in list(vars(module).items()):
                original = real.get(id(value))
                if original is not None:
                    setattr(module, name, original)

    return unpin


def pin_binding_stamps(patch) -> None:
    """Make the rekordbox binding stamp a row with the pinned instant.

    The binding's ``default=datetime.now`` and ``onupdate=datetime.now`` were
    bound at import, so each is re-pointed on the shared declaration.
    """
    try:
        from pyrekordbox.db6 import tables
    except ImportError:
        return
    for table in tables.Base.metadata.tables.values():
        for column in table.columns:
            for default in (column.default, column.onupdate):
                if default is not None and getattr(default, "is_callable", False):
                    if getattr(default.arg, "__name__", "") == "now":
                        patch.setattr(default, "arg", lambda _context: PinnedDatetime.now())
                        # PinnedDatetime.now is the real clock once the pins are
                        # off, so this is right even before the patch is undone.


@dataclass(frozen=True)
class Ran:
    """One command as it ended."""

    code: int
    stdout: str
    stderr: str

    @property
    def envelope(self) -> dict:
        """The JSON envelope a command run with ``--output json`` printed."""
        return json.loads(self.stdout)


@dataclass
class Stage:
    """Where a scenario runs its commands, and the record of what each did."""

    name: str
    root: Path
    refuse_outside: object
    commands: list[dict] = field(default_factory=list)

    def settle(self) -> None:
        """Give everything under the scenario's directory the pinned instant as its
        times, so a file one command wrote carries no real time into the next."""
        stamp = INSTANT.timestamp()
        for current, directories, files in os.walk(self.root):
            for name in (*directories, *files):
                os.utime(os.path.join(current, name), (stamp, stamp), follow_symlinks=False)

    def crate(self, *argv: str) -> Ran:
        """Run one `crate` command through the real dispatcher and keep what it did.

        In this process, so the suite's fakes stand in; both streams are
        redirected, since argparse prints help to the process's own stdout.
        """
        from cratekit import cli

        self.refuse_outside()
        self.settle()
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.run([str(one) for one in argv], stdout=out, stderr=err)
        ran = Ran(code=int(code), stdout=out.getvalue(), stderr=err.getvalue())
        self.commands.append(
            {
                "argv": [str(one) for one in argv],
                "exit": ran.code,
                "stdout": ran.stdout,
                "stderr": ran.stderr,
            }
        )
        return ran

    def json(self, *argv: str) -> Ran:
        """The same command asking for the JSON envelope, which a scenario reads ids from."""
        return self.crate("--output", "json", *argv)

    def decide(self, run_id: str, gate: str, option: str) -> Ran:
        """The second of a gate's two acts: the decision, recorded against the run."""
        return self.crate("run", "decide", run_id, gate, option, "--actor", "a-person")


def scenario_name(path: Path, function: str) -> str:
    """A scenario's name in a capture: its file's package, then its function."""
    return f"{path.stem}/{function.removeprefix('test_')}"


def process_identity() -> list[str]:
    """The words this process is known by in what it writes: its id and when it started.

    Both differ between captures whatever the tree does, so `compare` reads
    across them; the start is spelled as ``core.session.process_started`` does.
    """
    import psutil

    return [str(os.getpid()), f"{psutil.Process(os.getpid()).create_time():.3f}"]


def environment_under(root: Path) -> dict[str, str]:
    """Every variable naming a path under ``root``, by name."""
    prefix = str(root)
    return {
        name: value
        for name, value in os.environ.items()
        if value == prefix or value.startswith(prefix + os.sep)
    }
