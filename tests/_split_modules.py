"""The three modules U300 split into parts, so a scan of one reads all of it.

U300 split ``core/rb_writer.py``, ``core/session.py`` and ``core/restore.py``
into parts each module re-exports (``docs/DEVELOPING.md``, "The guarded writer,
the session and the restore, in parts"). A guard that reads a module's own
file, its ``inspect.getsource``, or an import of its exact dotted name reads
the module and not the code that moved to its parts, so a forbidden shape
written in a part passed it (R-1890). Every such guard reads its module
through here instead.

The parts are found by the glob of the module's file name, the convention
U300 named them by and ``tests/test_restore.py`` already reads them with, so a
part added later is read without an edit here. A glob is only as good as the
convention, so ``tests/test_split_modules.py`` derives the parts two other
ways, from the module table in ``docs/DEVELOPING.md`` and from the call time
accessor each part holds back to its module, and fails on one the glob misses.
The glob also matches ``rb_dates.py``, which predates U300 and is the writer's
too (it installs the date bound the writer opens with), so it is read here as
well: a scan that reads one file more is stricter, never weaker.
"""

from __future__ import annotations

from pathlib import Path

CORE = Path(__file__).resolve().parent.parent / "src" / "cratekit" / "core"
PACKAGE = "cratekit.core"

#: Each split module's dotted name, and the glob its file and parts match.
SPLIT_MODULES: dict[str, str] = {
    f"{PACKAGE}.rb_writer": "rb_*.py",
    f"{PACKAGE}.session": "session*.py",
    f"{PACKAGE}.restore": "restore*.py",
}


def files_of(module: str) -> list[Path]:
    """The module's own file first, then each part, sorted by name."""
    own = CORE / f"{module.rsplit('.', 1)[-1]}.py"
    parts = sorted(path for path in CORE.glob(SPLIT_MODULES[module]) if path != own)
    return [own, *parts]


def source_of(module: str) -> str:
    """The module and its parts as one text, each file on its own lines."""
    return "\n".join(path.read_text(encoding="utf-8") for path in files_of(module))


def names_of(module: str) -> tuple[str, ...]:
    """The dotted names of the module and each of its parts."""
    return tuple(f"{PACKAGE}.{path.stem}" for path in files_of(module))


def relative_paths_of(module: str) -> tuple[str, ...]:
    """The module's and its parts' paths under the package root, ``core/x.py``."""
    return tuple(f"core/{path.name}" for path in files_of(module))
