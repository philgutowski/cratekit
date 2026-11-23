"""``session`` read at call time, the one accessor its parts share (U329).

A part split from ``session`` reads every seam a test patches through the
module, never through its own globals, or the patch silently stops reaching
the part (the solutions entry on part splits). The accessor imports the
module inside the function, since ``session`` imports the parts that call it.
"""

from __future__ import annotations

from types import ModuleType


def session() -> ModuleType:
    """``session`` at call time: its seams are patched there, and it imports its parts."""
    from cratekit.core import session

    return session
