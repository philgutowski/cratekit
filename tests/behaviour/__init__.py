"""Behaviour scenarios: what `crate` prints and writes, captured for comparison (U297).

`scripts/behaviour_compare.py capture` runs the files in this directory as a
pytest run of their own and records what each scenario did, and `compare`
reads two such captures. The files are not named ``test_*.py``, so the suite
does not collect them: they are run when a branch has to show it prints and
writes what its base does, and at no other time.

ONE FILE PER PACKAGE, named for the package whose verbs it drives, so two
cards never edit the same one. A scenario is a test function that takes the
``stage`` fixture and drives commands through it:

    def test_a_tag_is_written(stage, machine, silence):
        ...
        stage.crate("tag", "remap")

Its fixtures are the suite's own, imported from the test module that defines
them, never new builders. Assert what the scenario depends on, an exit code
or a job id, so a scenario whose setup broke fails the capture instead of
recording a refusal as if it were the behaviour.

This module is the stage's parts: the pinned clock, the counted ids and the
``Stage`` that runs a command and keeps what it did. ``conftest.py`` beside it
holds the fixtures that put them around every scenario.
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
import uuid
from dataclasses import dataclass, field
from pathlib import Path

#: The one instant every scenario runs at. Late enough that the fixtures'
#: recorded dates, a pin validated in August 2026 among them, are in its past.
INSTANT = datetime_module.datetime(2026, 11, 21, 12, 0, 0, tzinfo=datetime_module.timezone.utc)

#: The modules whose own names for the clock and the id sources are re-pointed.
#: The standard library's modules are patched at their own attributes, which
#: covers every later import and every ``module.name`` call; these are the
#: packages that may already hold ``from datetime import datetime`` by then.
SWEPT = ("cratekit", "tests", "pyrekordbox")

_REAL_DATETIME = datetime_module.datetime
_REAL_DATE = datetime_module.date


class _Pinned(type):
    """Makes a pinned class stand for the real one in ``isinstance`` and ``issubclass``.

    No instance of a pinned class ever exists: its constructor returns the
    real type's. So a check against the pinned name has to accept those, or
    code holding the pinned name would stop recognising every date it meets.
    """

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
        if tz is None:
            return INSTANT.astimezone().replace(tzinfo=None)
        return INSTANT.astimezone(tz)

    @classmethod
    def utcnow(cls):
        return INSTANT.replace(tzinfo=None)

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
        return INSTANT.astimezone().date()


class Counted:
    """Ids from a counted sequence, so the nth id a scenario mints is always the same.

    A sequence and not a constant, because ids must stay distinct. It makes
    the ids depend on the order they are minted in, so a change that mints one
    more id, or mints two in the other order, shows as a difference in every
    id after it; that is read as a difference to explain, not as noise.
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

    ``patch`` is a ``pytest.MonkeyPatch``, so everything set here is put back
    when it is undone; the shared ``random`` generator is seeded, and what is
    returned puts its state back. What is pinned is what Python code reads:
    ``datetime`` and ``date``; ``time.time`` and ``time.time_ns``; the two
    clocks a duration is measured on, ``time.monotonic`` and
    ``time.perf_counter``, which stand still, so every measured duration is
    zero and a wait that would have timed out never does, which the capture's
    own timeout ends; ``uuid.uuid4``, ``secrets.token_hex`` and
    ``secrets.token_bytes``, the last being where the rekordbox binding draws
    a new row's id; and the stamps the binding puts on a row it writes
    (``pin_binding_stamps``). What the operating system gives is not pinned
    here: a file's times are set by ``Stage.settle`` between commands, and the
    process id and each file's inode are the capture's own, which ``compare``
    knows by name.
    """
    counted = Counted()
    stamp = INSTANT.timestamp()
    pairs = (
        (datetime_module, "datetime", PinnedDatetime),
        (datetime_module, "date", PinnedDate),
        (time, "time", lambda: stamp),
        (time, "time_ns", lambda: int(stamp) * 1_000_000_000),
        (time, "monotonic", lambda: 0.0),
        (time, "monotonic_ns", lambda: 0),
        (time, "perf_counter", lambda: 0.0),
        (time, "perf_counter_ns", lambda: 0),
        (uuid, "uuid4", counted.uuid4),
        (secrets, "token_hex", counted.token_hex),
        (secrets, "token_bytes", counted.token_bytes),
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
    for module, name, replacement in pairs:
        patch.setattr(module, name, replacement)
    pin_binding_stamps(patch)
    state = random.getstate()
    random.seed(0)
    return lambda: random.setstate(state)


def pin_binding_stamps(patch) -> None:
    """Make the rekordbox binding stamp a row with the pinned instant.

    The binding's tables declare ``default=datetime.now`` and
    ``onupdate=datetime.now`` on every row's two stamps, and that is the real
    class's method, bound when the binding was imported, which no patch of a
    name reaches. So each such default is re-pointed where the schema holds
    it, on the binding's own shared declaration, for the life of the patch.
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


def unpin() -> None:
    """Put the real clock classes back in any module that imported a pinned one.

    A module first imported while the clock was pinned took the pinned class
    as its own ``datetime``, and undoing the patch does not reach it, since
    the patch never set it. Left there it would hold every later test in this
    process at the scenario's instant.
    """
    real = {id(PinnedDatetime): _REAL_DATETIME, id(PinnedDate): _REAL_DATE}
    for module in list(sys.modules.values()):
        if module is None or module is sys.modules[__name__]:
            continue
        for name, value in list(getattr(module, "__dict__", {}).items()):
            replacement = real.get(id(value))
            if replacement is not None:
                setattr(module, name, replacement)


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
        """Give everything under the scenario's directory the pinned instant as its times.

        The clock is pinned and the file system's is not, so a file one
        command wrote would carry the real time into the next command that
        reads it: a gate reports how long a run has stood open by its record's
        last write. Between commands every file and directory is therefore
        set to the instant the commands themselves believe it is.
        """
        stamp = INSTANT.timestamp()
        for current, directories, files in os.walk(self.root):
            for name in (*directories, *files):
                os.utime(os.path.join(current, name), (stamp, stamp), follow_symlinks=False)

    def crate(self, *argv: str) -> Ran:
        """Run one `crate` command through the real dispatcher and keep what it did.

        In this process, as the suite drives a verb, so the suite's fakes
        stand where a provider or a program would. Both streams are also
        redirected, because argparse prints a help screen to the process's own
        standard output whatever the dispatcher was handed.
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

    The product records both, in a session's holder, in a lock file and in
    the job queue, and both differ between two captures whatever the tree
    does. They are written into the capture so `compare` can read one
    capture's against the other's instead of calling each a difference. The
    start is spelled as ``core.session.process_started`` spells it.
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
