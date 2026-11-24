"""One harness for "this lookup imports nothing", shared by the suites that claim it.

A clean interpreter, since in this process every feature module is cached:
a real ``importlib.import_module`` in ``registry.by_handler_key`` once killed
zero tests that way.
"""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_probe(body: str) -> dict:
    """Run ``body`` in a fresh interpreter and return the ``{walked, leaked}`` it printed.

    ``body`` snapshots ``sys.modules`` around EACH lookup, not the loop, which
    would count the package initializer.
    """
    finished = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(body)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert finished.returncode == 0, finished.stderr
    return json.loads(finished.stdout.strip().splitlines()[-1])


def assert_no_leak(result: dict, *, what: str) -> None:
    """No leak, and a non-zero ``walked`` counted from the loop, so a skipped walk fails."""
    assert result["walked"] > 0, (
        f"the probe walked nothing, so it measured nothing about {what}"
    )
    assert result["leaked"] == {}, (
        f"{what} imported a cratekit module: {result['leaked']}. The supervisor "
        f"answers this question before it spawns anything, so a lookup that "
        f"imports pulls the feature module into its own process"
    )
