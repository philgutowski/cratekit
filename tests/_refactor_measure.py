"""``scripts/refactor_measure.py``, loaded once for the suites that read through it.

The duplication check, the import rules and the per package pins all measure
with the script's own functions, so the suite and the refactor's audit cannot
read two different things (U296). It is a script, not a package module, so it
is loaded by path, as the other scripts' suites load theirs.

Not a test module: pytest does not collect it, and it defines no tests.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load() -> ModuleType:
    name = "cratekit_refactor_measure"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / "scripts" / "refactor_measure.py")
    module = importlib.util.module_from_spec(spec)
    # Registered before it runs: its dataclasses resolve their own module by name.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


measure = _load()
