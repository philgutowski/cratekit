"""Cratekit: acquisition and curation for rekordbox DJs.

This package intentionally does almost nothing at import time. Importing
``cratekit`` must not read configuration, touch a filesystem path, open a
database, or import a feature module. Two reasons:

1. ``crate --help`` has to work on a slim install with every heavy extra
   absent (KTD7). If importing the package pulled in the analysis module, help
   would crash on a machine that never enabled analysis.
2. Layering (KTD23) depends downward only. The package root is the lowest
   layer there is, so it may not name a module, a verb, or a taxonomy literal.

Version lives here rather than being read from installed metadata so that a
source checkout without an install still reports something coherent.
"""

__version__ = "0.6.0"

__all__ = ["__version__"]
