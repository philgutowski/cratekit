"""Helpers shared by the sync, session and routing tests of one slice (U312).

pytest does not rewrite this module's asserts, so each message carries the code.
"""

from __future__ import annotations

import functools
import tempfile
from pathlib import Path

from cratekit.core.exit_codes import ExitCode
from tests._containers import synth_container


def exited(result: tuple[int, dict], expected: ExitCode = ExitCode.OK) -> dict:
    """The envelope of a drive that exited ``expected``, OK unless told otherwise."""
    code, envelope = result
    assert code == int(expected), f"exited {code}, expected {int(expected)}: {envelope!r}"
    return envelope


def failed(result: tuple[int, dict]) -> dict:
    """The envelope of a drive that did not exit OK."""
    code, envelope = result
    assert code != int(ExitCode.OK), f"exited OK: {envelope!r}"
    return envelope


@functools.cache
def silent_flac() -> bytes:
    """One second of silence from the one synthesizer, made once per process and copied."""
    with tempfile.TemporaryDirectory() as folder:
        return synth_container(Path(folder), ".flac").read_bytes()
