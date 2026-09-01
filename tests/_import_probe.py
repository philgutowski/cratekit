"""One harness for "this lookup imports nothing", shared by the suites that claim it.

WHY A CLEAN INTERPRETER AND NOT A ``sys.modules`` DIFFERENCE IN THIS PROCESS. By
the time a suite reaches either caller, every feature module is already cached, so
an in-process before-and-after difference is empty whatever the code does. That
version existed and a mutation table proved it: inserting a real
``importlib.import_module`` into ``registry.by_handler_key`` killed ZERO tests,
subset and promoted full suite alike. A difference is only a measurement where the
thing could have differed, and the state the supervisor is actually in is a fresh
process that has imported the registry and nothing else.

WHY IT IS HERE RATHER THAN COPIED. Two suites make the same claim about two
different lookups, ``registry.by_handler_key`` and ``handlers.is_known``. The probe
body differs by three lines; the harness around it, the subprocess, the JSON, the
vacuity guard, does not. A second hand-copied harness is one that drifts from the
first and then measures something slightly else while both stay green.

Not a test module: pytest does not collect it, and it defines no tests of its own.
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

    ``body`` is responsible for the whole measurement: it imports what the
    supervisor would import, walks a population, snapshots ``sys.modules`` around
    each individual lookup, and prints one JSON object with a ``walked`` count and a
    ``leaked`` mapping. The snapshot is PER LOOKUP rather than around the loop,
    because importing the module under test runs its package initializer and that
    is not what either caller claims anything about.
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
    """Both halves, and the vacuity guard is the half that is easy to forget.

    ``walked`` is COUNTED FROM THE LOOP rather than from the population's length,
    so a build in which every candidate was skipped reports zero here instead of a
    reassuring non-zero total.
    """
    assert result["walked"] > 0, (
        f"the probe walked nothing, so it measured nothing about {what}"
    )
    assert result["leaked"] == {}, (
        f"{what} imported a cratekit module: {result['leaked']}. The supervisor "
        f"answers this question before it spawns anything, so a lookup that "
        f"imports pulls the feature module into its own process"
    )
