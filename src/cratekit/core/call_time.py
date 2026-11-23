"""The write path's patched modules, read at call time (U329).

A part split from ``rb_writer`` or ``session`` reads every seam a test
patches through its module, never through its own globals, or the patch
silently stops reaching the part (the solutions entry on part splits). Each
accessor imports its module inside the function, since that module imports
the parts that call it. One home for the accessor every part once copied.
"""

from __future__ import annotations

from types import ModuleType


def rb_writer() -> ModuleType:
    """``rb_writer`` at call time: its seams are patched there, and it imports its parts."""
    from cratekit.core import rb_writer

    return rb_writer


def session() -> ModuleType:
    """``session`` at call time: its seams are patched there, and it imports its parts."""
    from cratekit.core import session

    return session
