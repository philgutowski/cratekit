"""The three modules U300 split into parts, so a scan of one reads all of it.

U300 split ``core/rb_writer.py``, ``core/session.py`` and ``core/restore.py``
into parts each re-exports (``docs/DEVELOPING.md``, "The guarded writer, the
session and the restore, in parts"). A guard reading a module's own file, its
``inspect.getsource`` or its exact dotted name missed a forbidden shape in a
part (R-1890), so every such guard reads through here.

Parts are found by the glob of the module's file name, U300's convention.
``tests/test_split_modules.py`` derives them three other ways, from the table
in ``docs/DEVELOPING.md``, the import graph and the call time accessor; a part
off the convention that escapes all three is a recorded residual. The glob
also matches ``rb_dates.py``, the writer's too, so it is read: stricter,
never weaker.
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
