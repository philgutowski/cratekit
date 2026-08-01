#!/usr/bin/env python3
"""Regenerate the committed schema lock and the representative envelopes.

The lock file is what turns "remember to bump the schema version" into something
a build can check. The source system's record on remembering is perfect and
negative: exactly one of its twenty-one state files carries a version, and the
plan preview, the job records, the calibrations, and the label registries all
changed shape more than once with no version to tell a reader which shape they
are holding.

So the rule is mechanical instead: every payload surface's structure is hashed
and the hash is committed. Change the structure without bumping the major and
``tests/test_cli_contract.py`` fails, naming the surface and telling you to bump.

Run this ONLY when you meant to change a schema::

    python scripts/dump_schemas.py

Then read the diff. A hash that moved with no major bump beside it is the thing
the test is about to reject.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from cratekit.cli import output  # noqa: E402
from cratekit.core.cause import Cause, Outcome, Remediation  # noqa: E402
from cratekit.core.exit_codes import ExitCode, Remedy  # noqa: E402

SCHEMA_DIR = REPO_ROOT / "tests" / "schemas"
GOLDEN_DIR = SCHEMA_DIR / "golden"

#: One representative payload per surface. They are the shape a consumer should
#: expect to be able to read, so they carry a populated example rather than an
#: empty one wherever the surface has a repeating element.
EXAMPLES: dict[str, dict] = {
    "plan": {
        "digest": "0123456789abcdef",
        "items": [{"id": "item-1", "change": "add"}],
        "totals": {"add": 1, "remove": 0},
        "chunk": None,
    },
    "match": {
        "matched": [{"id": "t-1", "source": "s-1"}],
        "needs_review": [{"id": "t-2", "source": "s-2", "why": "version-differs"}],
        "missing": [{"source": "s-3"}],
    },
    "review_set": {
        "queue": "duplicates",
        "items": [{"id": "rv-1", "kind": "duplicate", "verdict": None}],
        "unresolved": 1,
    },
    "job_state": {
        "job_id": "job-1",
        "state": "queued",
        "cause": None,
        "progress": {"done": 0, "total": 12},
    },
    "diagnostic": {
        "checks": [
            {
                "key": "library.mounted",
                "title": "library volume",
                "status": "ok",
                "detail": "",
                "remedy": None,
            }
        ],
        "summary": {"ok": 1, "failed": 0},
    },
}


def golden_envelope(name: str) -> dict:
    """One envelope per surface, at a representative but not trivial state."""
    started = "2026-01-01T00:00:00+00:00"
    if name == "job_state":
        # The one failure example, so a golden exists for the half of the
        # envelope that only appears when something went wrong.
        cause = Cause(
            reason="auth-failed",
            message="the provider rejected the stored credential",
            remediation=Remediation(remedy=Remedy.AUTHENTICATE_PROVIDER),
            origin=("adapter", "download", "job", "cli"),
        )
        return output.build(
            verb="job.show",
            run_id="2026-01-01T00:00:00Z-0000",
            schema=output.current_schema(name),
            started=started,
            ended=started,
            outcome=Outcome.FAILED,
            code=ExitCode.UPSTREAM_AUTH,
            data=EXAMPLES[name],
            cause=cause,
        ).to_json()
    return output.build(
        verb="profile.show",
        run_id="2026-01-01T00:00:00Z-0000",
        schema=output.current_schema(name),
        started=started,
        ended=started,
        data=EXAMPLES[name],
    ).to_json()


def main() -> int:
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

    lock = {}
    for name in output.schema_names():
        identifier = output.current_schema(name)
        lock[identifier] = output.schema_fingerprint(name)
        major = identifier.split("/")[1]
        (SCHEMA_DIR / f"{name}.v{major}.json").write_text(
            json.dumps(output.schema_document(name), indent=2, sort_keys=True) + "\n"
        )
        (GOLDEN_DIR / f"{name}.v{major}.json").write_text(
            json.dumps(golden_envelope(name), indent=2, sort_keys=True) + "\n"
        )

    existing = {}
    lock_path = SCHEMA_DIR / "lock.json"
    if lock_path.is_file():
        existing = json.loads(lock_path.read_text())
    # Retired majors stay in the lock forever, so no version is silently dropped
    # and a consumer holding an old envelope can still find out what it was.
    merged = {**existing, **lock}
    lock_path.write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n")
    print(f"wrote {lock_path.relative_to(REPO_ROOT)} with {len(merged)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
