"""``rb_writer`` read at call time, the one accessor its parts share (U329).

A part split from ``rb_writer`` reads every seam a test patches through the
module, never through its own globals, or the patch silently stops reaching
the part (the solutions entry on part splits). The accessor imports the
module inside the function, since ``rb_writer`` imports the parts that call it.
"""

from __future__ import annotations

from types import ModuleType


def writer() -> ModuleType:
    """``rb_writer`` at call time: its seams are patched there, and it imports its parts."""
    from cratekit.core import rb_writer

    return rb_writer
