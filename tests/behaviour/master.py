"""Mastering's scenarios: the commands planned for the encoder, and its refusals (U311).

`crate master` is queued and then run, on the mastering suite's own machine
with no database and a real recording the suite makes with ffmpeg. The encode
runs through the seam the suite drives it through, ``mastering.subprocess_runner``
answered by ``_recorder``, the stand in that answers each stage on its own
terms and keeps every command it was handed; those commands are written into
the scenario's directory after the run, so the capture holds what would have
been asked of ffmpeg and ffprobe, argument by argument.

The refusals are the encoder named through ``CRATEKIT_BIN_FFMPEG`` at a
program that is not there, which ``core.binaries`` reads before PATH, and a
master already at the destination without ``--overwrite``.
"""

from __future__ import annotations

import os
import random
import tempfile
from pathlib import Path

from cratekit.core.exit_codes import ExitCode
from cratekit.modules.tools import mastering
from tests.test_master_cli import _recorder, _recording
from tests.test_master_cli import configured as configured  # noqa: PLC0414
from tests.test_master_cli import library as library  # noqa: PLC0414

OK = int(ExitCode.OK)


def _pin_temporary_names(monkeypatch) -> None:
    """Draw the names ``tempfile`` makes from a seeded sequence, for the life of the scenario.

    A split recording is joined in a directory ``tempfile.mkdtemp`` names, and
    that name is in every command after the join. The standard library draws
    it from a generator of its own, seeded by the system and not the one the
    stage pins, so it is pinned here, as ``sync.py`` pins a staged file's time:
    a sequence seeded once, which ``tempfile`` keeps as its module's one name
    source and reuses only in the process that seeded it.
    """
    names = tempfile._RandomNameSequence()
    names._rng = random.Random(0)
    names._rng_pid = os.getpid()
    monkeypatch.setattr(tempfile, "_name_sequence", names)


def _write_commands(seen, path: Path) -> None:
    """Every command the stand in was handed, one per line, for the capture to hold."""
    path.write_text("".join(" ".join(command.argv) + "\n" for command in seen))


def test_a_recording_is_mastered_through_the_queue(stage, configured, monkeypatch, tmp_path):
    """One recording at the default target, then a split one at its own target and directory."""
    _pin_temporary_names(monkeypatch)
    root = configured.library.root
    source = _recording(root)
    run, seen = _recorder()
    monkeypatch.setattr(mastering, "subprocess_runner", run)

    queued = stage.json("master", source)
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]
    done = stage.crate("master", source, "--job", job_id)
    assert done.code == OK, done.stderr
    assert stage.json("master", source, "--job", job_id).code == OK
    assert mastering.output_path(source).is_file()

    first = _recording(root, "REC002.wav")
    second = _recording(root, "REC003.wav")
    out = tmp_path / "masters"
    split = ("master", first, second, "--lufs=-12", "--output-dir", out)
    queued = stage.crate(*split)
    assert queued.code == OK, queued.stderr
    queued = stage.json(*split)
    assert queued.code == OK, queued.stdout
    done = stage.json(*split, "--job", queued.envelope["data"]["job_id"])
    assert done.code == OK, done.stdout
    _write_commands(seen, tmp_path / "encoder-commands.txt")
    assert any("concat" in command.argv for command in seen)


def test_mastering_refuses_without_its_encoder(stage, configured, monkeypatch, tmp_path):
    """The encoder named at a program that is not there: the item fails by that name."""
    source = _recording(configured.library.root)
    queued = stage.json("master", source)
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]

    monkeypatch.setenv("CRATEKIT_BIN_FFMPEG", str(configured.library.root / "no-ffmpeg"))
    refused = stage.json("master", source, "--job", job_id)
    assert refused.code != OK, refused.stdout
    stage.crate("master", source, "--job", job_id)
    assert not mastering.output_path(source).exists()


def test_mastering_refuses_over_an_existing_master(stage, configured, monkeypatch, tmp_path):
    """A master already at the destination is refused before the encoder runs, and replaced under overwrite."""
    source = _recording(configured.library.root)
    final = mastering.output_path(source)
    final.write_bytes(b"a master somebody kept")
    run, seen = _recorder()
    monkeypatch.setattr(mastering, "subprocess_runner", run)

    queued = stage.json("master", source)
    assert queued.code == OK, queued.stdout
    refused = stage.json("master", source, "--job", queued.envelope["data"]["job_id"])
    assert refused.code != OK, refused.stdout
    assert seen == []
    assert final.read_bytes() == b"a master somebody kept"

    replacing = stage.json("master", source, "--overwrite")
    assert replacing.code == OK, replacing.stdout
    job_id = replacing.envelope["data"]["job_id"]
    replaced = stage.crate("master", source, "--overwrite", "--job", job_id)
    assert replaced.code == OK, replaced.stderr
    _write_commands(seen, tmp_path / "encoder-commands.txt")
    assert final.read_bytes() != b"a master somebody kept"


def test_mastering_refuses_outside_its_loudness_range_and_without_its_probe(
    stage, configured, monkeypatch, tmp_path
):
    """A target loudness ffmpeg would refuse, and the probe named at a program that is not there."""
    source = _recording(configured.library.root)
    stage.json("master", source, "--lufs=-3")
    stage.crate("master", source, "--lufs=-3")
    queued = stage.json("master", source)
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]

    monkeypatch.setenv("CRATEKIT_BIN_FFPROBE", str(configured.library.root / "no-ffprobe"))
    refused = stage.json("master", source, "--job", job_id)
    assert refused.code != OK, refused.stdout
    stage.crate("master", source, "--job", job_id)
    assert not mastering.output_path(source).exists()
