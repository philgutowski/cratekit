"""One synthesizer for a real audio container, shared by every suite that needs one.

A second synthesizer would be a second opinion about what a valid file is, and
the tag suite's opinion is the one the tag reader is proven against. So there is
one, and it lives here rather than inside a test module.

WHY NOT ``from tests.test_tags import _synth``. That binding reached across test
modules for a private name, which is a coupling nothing declares, and importing a
test module runs its top-level code as a side effect of an unrelated suite. The
tag suite's top level builds a container table and a field table; none of that is
wrong, and none of it is any business of the match suite. A helper module has no
top level worth running and no tests to collect.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


def require_ffmpeg() -> str:
    binary = shutil.which("ffmpeg")
    if binary is None:
        pytest.fail(
            "ffmpeg is required to prove that a tag write leaves audio bytes "
            "unchanged. Install it (the CI workflow does this in a dedicated "
            "step). This fails rather than skips because a skipped audio-safety "
            "proof is indistinguishable from a passing one in every summary "
            "anybody reads."
        )
    return binary


def synth_container(tmp_path: Path, suffix: str) -> Path:
    """One second of silence in the given container."""
    require_ffmpeg()
    out = tmp_path / f"probe{suffix}"
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-t", "1", str(out)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0 and out.exists(), (
        f"ffmpeg could not encode {suffix}, so this container's audio-safety "
        f"proof cannot run: {proc.stderr[-400:]}"
    )
    return out


def tagged_container(tmp_path: Path, target: Path, **fields: str) -> Path:
    """A real container at ``target`` carrying ``fields`` as its tags.

    One synthesizer, one tag writer, one copy. Three tests had written this
    sequence by hand with three signatures, and the point of this module is that
    there is one opinion about what a valid file is.
    """
    from cratekit.core import tags

    probe = synth_container(tmp_path, target.suffix)
    assert tags.write_tags(probe, dict(fields))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(probe, target)
    return target


__all__ = ["require_ffmpeg", "synth_container", "tagged_container"]
