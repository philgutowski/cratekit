"""The one register of guards that are written but not yet armed.

U6 ports the safety net BEFORE the engine it guards, on purpose: a guard that
arrives after the code it governs can only ever confirm what already shipped,
while a guard that arrives first makes the violation impossible to introduce
silently. The cost of that ordering is that some ported guards name a module
that does not exist yet.

The rule for handling that cost, and the reason this file exists:

1. A pending guard keeps its FULL ported assertion body. It is never weakened,
   never reduced to a placeholder, and the production module is never stubbed
   just to make it green. A stub would turn a real guard into a test of the stub.
2. It is gated behind a skip whose reason names the unit that unblocks it, so
   anyone reading a skipped test learns what has to land, not just that something
   is missing.
3. Every such skip is declared here, and tests/test_pending_units.py asserts the
   declared set is exactly the intended set AND that each target is genuinely
   still absent. The moment a unit lands its module, that meta-test goes red and
   the only way to make it green is to delete the entry, which arms the guard.

That third point is the whole design. Without it, a skip added for a good reason
in August is still silently skipping in December, and the safety net has a hole
nobody can see. With it, a skip is a countdown, not a hiding place.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Guards awaiting the module they govern.
#
# key   -> a stable identifier for the thing that is missing. For an import
#          target this is the dotted module path, checked with find_spec. For a
#          non-import target it is a "path:" key, checked against the filesystem.
# value -> (unit that lands it, one line saying what the guard asserts)
# ---------------------------------------------------------------------------
PENDING: dict[str, tuple[str, str]] = {
    "cratekit.core.rb_writer": (
        "U7",
        "the additive whitelist, the two-process refusal, the version pin "
        "including U2's refusal on a pin that was never recorded, the cloud "
        "canary, and the cross-process write-session lock",
    ),
    "cratekit.write.rbxml": (
        "U17",
        "the XML byte rules: CRLF-only emission, PLAYLISTS-scoped anchoring, "
        "Entries arithmetic, and the no-partial-write failure path",
    ),
    "cratekit.write.trees": (
        "U18",
        "the tree writers whose exact output bytes the golden files pin",
    ),
    "cratekit.intake.collection_xml": (
        "U37",
        "the COLLECTION TRACK emitter that must never emit a <TEMPO> element",
    ),
    "cratekit.core.snapshot": (
        "U8",
        "that the KTD21b capture set is DERIVED from the state inventory rather "
        "than hand-listed, and that it therefore includes the rekordbox "
        "database's -wal and -shm sidecars, without which a capture is a "
        "database silently missing every uncheckpointed transaction",
    ),
    "cratekit.core.restore": (
        "U32",
        "that a restore replaces exactly the derived coupled set, and that it "
        "keeps the source system's sidecar asymmetry: clear both live sidecars "
        "first, write back the -wal, never the -shm",
    ),
    "cratekit.core.review": (
        "U11",
        "that a verb declaring it adjudicates produces PERSISTED review items "
        "with stable identifiers, rather than writing a CSV for a human to hand "
        "edit, which is what fourteen files in the source system already are",
    ),
    "cratekit.core.jobs": (
        "U10",
        "that a verb declaring itself long-running QUEUES through the job engine "
        "instead of working inline, and that its handler key resolves without "
        "importing the module, which is what keeps the lazy-import stubs intact "
        "across the subprocess boundary (KTD26)",
    ),
    "cratekit.core.session": (
        "U8",
        "that every destructive verb refuses without the library lock, the "
        "backup acknowledgment, and a matching volume identity, with three "
        "distinct codes and no writes on any of the three paths (KTD24, R38). "
        "Note the case that makes the binding non-obvious: a backup restore "
        "replaces a live database and its sidecars while writing no database "
        "row, so a rule binding the gates to database WRITES alone would leave "
        "the one operation that destroys a library outside the safety spine "
        "entirely. The gates bind to destructive sessions, not to write sessions"
    ),
    "cratekit.cli.doctor": (
        "U27",
        "that a database acknowledged outside the library root is REPORTED on "
        "every run, so the snapshot that is a copy rather than an atomic commit "
        "stays visible long after the date somebody accepted it",
    ),
    "path:skills": (
        "U28",
        "the shipped operator skills the skills lint runs over",
    ),
    "cratekit.cli.exit_codes": (
        "U5",
        "that every structured refusal cause the standalone utilities raise has "
        "a reserved exit code and a remediation, which is the S4 obligation "
        "applied to this unit: a refusal with no reserved code collapses to a "
        "bare status at the process boundary and cannot be recovered downstream",
    ),
}


def _is_absent(key: str) -> bool:
    """True when the thing named by ``key`` has not landed yet.

    Import targets are probed with ``find_spec`` rather than a real import, so a
    probe can never execute module-level code and never has an import failure of
    its own to distinguish from absence.
    """
    if key.startswith("path:"):
        return not (REPO_ROOT / key[len("path:") :]).exists()
    try:
        return importlib.util.find_spec(key) is None
    except ModuleNotFoundError:
        # A parent package is missing, so the target is certainly missing too.
        return True


def requires(key: str) -> pytest.MarkDecorator:
    """Gate a ported guard on the unit that lands the thing it guards.

    Usage::

        @requires("cratekit.core.rb_writer")
        def test_creating_a_track_row_is_forbidden():
            ...

    The skip reason always names the unit, so ``pytest -rs`` reads as a work
    queue rather than as a list of mysteries.
    """
    if key not in PENDING:
        raise KeyError(
            f"{key!r} is not declared in _pending.PENDING. Add it there with the "
            f"unit that lands it, so tests/test_pending_units.py can hold it "
            f"accountable, or the skip becomes permanent by accident."
        )
    unit, what = PENDING[key]
    return pytest.mark.skipif(
        _is_absent(key),
        reason=f"{key} lands in {unit}; this guard asserts {what}",
    )
