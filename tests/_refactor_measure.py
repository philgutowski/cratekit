"""``scripts/refactor_measure.py``, loaded once by path for the suites that read through it (U296).

So the suite and the refactor's audit measure with the same functions.
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
