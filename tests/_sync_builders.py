"""Helpers shared by the sync, session and routing tests of one slice (U312).

A test module asserts here through ``exited``; this module is not rewritten by
pytest, so the message carries the code itself.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode


def exited(result: tuple[int, dict], expected: ExitCode = ExitCode.OK) -> dict:
    """The envelope of a drive that exited ``expected``, OK unless told otherwise."""
    code, envelope = result
    assert code == int(expected), f"exited {code}, expected {int(expected)}: {envelope!r}"
    return envelope
