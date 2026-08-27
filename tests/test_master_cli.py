"""U44: ``crate master``, the shell over the mastering engine (row 30).

WHAT THIS FILE IS FOR, since ``tests/modules/test_tools.py`` already drives the
engine. Two different claims. That file proves the ENGINE keeps its promise when
called directly. This one proves the SHELL reaches the engine in a way that keeps
it: that the archive still happens on the path a person actually travels, that
the engine's refusals arrive as refusals rather than as internal defects, and that
a resume rebuilds the same run rather than a default version of it.

THE STAND-IN ENCODER DISPATCHES ON ITS ARGV, and that is load bearing rather than
tidy. A stand-in that answers every invocation the same way cannot reach the
encode stage at all: with no loudness JSON on stderr the measure pass returns an
empty measurement and ``apply_filter`` refuses for the missing values long before
an encode command is built. A drive that "does not reproduce" for that reason is a
harness failure wearing an absent defect's clothes. ``_fake_rclone`` in
``tests/test_restore_cli.py`` is the shape this follows.
"""

from __future__ import annotations

import io
import json
import subprocess
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output, registry
from cratekit.core import config, jobs, profiles
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.master import cli as master_cli
from cratekit.modules.tools import mastering
from tests._containers import require_ffmpeg

#: One loudnorm report, carrying both halves. The measure passes read the
#: ``input_*`` keys and the encode's own report supplies the ``output_*`` ones,
#: so a single block answers every stage that parses stderr.
LOUDNORM = json.dumps(
    {
        "input_i": "-20.0",
        "input_lra": "5.0",
        "input_tp": "-3.0",
        "input_thresh": "-30.0",
        "target_offset": "0.5",
        "output_i": "-14.0",
        "output_lra": "5.0",
        "output_tp": "-1.0",
    }
)


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    return root


@pytest.fixture
def configured(library):
    """A set-up machine with NO DATABASE, which is all this verb may have.

    Deliberately not the conformance suite's fixture, for the reason the set
    builder's suite gives for the same choice: that one builds a disposable
    rekordbox database because the destructive verbs it drives will not admit a
    machine without one, and copying it here would imply this verb needs
    something it never opens. Mastering touches audio files and a job store.
    """
    cfg = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(library),
                "volume_id": "F1E2-D3C4",
                "db_path": str(library / "db" / "master.db"),
            },
            "paths": {"download_staging": str(library.parent / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(cfg)
    config.reset_cache()
    return cfg


def _entry() -> registry.Entry:
    return next(e for e in registry.ENTRIES if e.name == "master")


def _recording(tmp_path: Path, name: str = "REC001.wav") -> Path:
    """A real container, so the digest assertions are over real audio bytes."""
    require_ffmpeg()
    out = tmp_path / name
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-t", "1", str(out)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0 and out.exists(), proc.stderr[-400:]
    return out


def _encoder(*, encode_returncode: int = 0, encode_writes: bool = True):
    """A stand-in ffmpeg and ffprobe that answers each stage on its own terms.

    Only the final encode invocation varies between arms. Every other stage
    answers as a working toolchain would, which is what lets a drive reach the
    encode at all.
    """
    def run(command: mastering.Command) -> mastering.CommandResult:
        argv = list(command.argv)
        if argv[0].endswith("ffprobe"):
            return mastering.CommandResult(
                returncode=0, stdout="sample_rate=44100\nsample_fmt=s16\n"
            )
        if "-f" in argv and "null" in argv:
            return mastering.CommandResult(returncode=0, stderr=LOUDNORM)
        if "pcm_s24le" in argv:
            Path(argv[-1]).write_bytes(b"intermediate")
            return mastering.CommandResult(returncode=0)
        if encode_writes:
            Path(argv[-1]).write_bytes(b"x" * 64)
        return mastering.CommandResult(returncode=encode_returncode, stderr=LOUDNORM)
    return run


# ---------------------------------------------------------------------------
# The declared surface
# ---------------------------------------------------------------------------


def test_the_parser_accepts_the_whole_declared_argument_shape():
    parser = cli.build_parser([_entry()])
    args = parser.parse_args(
        ["master", "/tmp/REC001.wav", "--output-dir", "/tmp/out", "--overwrite"]
    )
    assert args.recording == "/tmp/REC001.wav"
    assert args.output_dir == "/tmp/out"
    assert args.overwrite is True
    assert args.job is None


def test_the_verb_is_absent_from_a_slim_profile(configured):
    """R1's second half. The toggle decides, so this is a property of the entry."""
    del configured
    assert not _entry().available_to(profiles.resolve("slim"))
    assert _entry().available_to(profiles.resolve("full"))


def test_the_entry_is_landed_and_declares_no_gate():
    """Both halves matter and they are different claims.

    Landed is what puts the verb into the conformance population. Declaring no
    gate is what keeps it OUT of the queued-resume contract's derived population,
    and asserting it as a property rather than by name means the day somebody adds
    a gate this guard stops being true rather than staying quietly correct.
    """
    entry = _entry()
    assert entry.landed
    assert entry.gates == ()
    assert entry.long_running and entry.argv_builder == "master_argv"
    assert entry.destructive and entry.writes == frozenset({"files"})


# ---------------------------------------------------------------------------
# The queued half
# ---------------------------------------------------------------------------


def _drive(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    assert out.getvalue().strip(), f"the verb printed nothing to standard output: {err.getvalue()}"
    document = json.loads(out.getvalue())
    assert output.envelope_problems(document) == [], document
    return code, document


def test_queueing_exits_ok_with_no_ffmpeg_and_no_recording(configured):
    """R3. Queueing needs neither, which is what makes the split worth having."""
    code, envelope = _drive(["master", str(configured.library.root / "nope.wav")])
    assert code == int(ExitCode.OK), envelope
    assert envelope["verb"] == "master"
    assert envelope["data"]["job_id"]
    assert envelope["schema"] == "job_state/1"


def test_an_empty_recording_refuses_from_the_vocabulary(configured):
    del configured
    code, envelope = _drive(["master", ""])
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "source-missing"


def test_naming_a_job_reports_it_rather_than_queueing_a_second(configured):
    code, first = _drive(["master", str(configured.library.root / "a.wav")])
    assert code == int(ExitCode.OK)
    job_id = first["data"]["job_id"]

    code, again = _drive(["master", str(configured.library.root / "a.wav"), "--job", job_id])
    assert code == int(ExitCode.OK), again
    assert again["data"]["job_id"] == job_id
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 1


def test_an_unknown_job_refuses_rather_than_raising(configured):
    del configured
    code, envelope = _drive(["master", "/tmp/a.wav", "--job", "no-such-job"])
    assert code != int(ExitCode.OK)
    assert code in {int(c) for c in ExitCode}
    assert envelope["cause"]["reason"] == "job-unknown"


# ---------------------------------------------------------------------------
# The resume argv (R10)
# ---------------------------------------------------------------------------


class _Job:
    job_id = "job-1"

    def __init__(self, payload):
        self.payload = payload


def test_the_resume_argv_rebuilds_every_frozen_flag():
    argv = master_cli.master_argv(
        _Job({"source": "/tmp/REC001.wav", "output_dir": "/tmp/out", "overwrite": True})
    )
    assert argv[argv.index("--output-dir") + 1] == "/tmp/out"
    assert "--overwrite" in argv
    assert argv[argv.index("--job") + 1] == "job-1"
    assert argv[0] == "master" and argv[1] == "/tmp/REC001.wav"


def test_the_resume_argv_omits_flags_the_payload_does_not_hold():
    argv = master_cli.master_argv(
        _Job({"source": "/tmp/REC001.wav", "output_dir": None, "overwrite": False})
    )
    assert "--output-dir" not in argv
    assert "--overwrite" not in argv
    assert argv[:2] == ["master", "/tmp/REC001.wav"]
    assert "--job" in argv


def test_the_resume_argv_carries_no_run_flag():
    """The verb declares no gate, so there is no run for --run to name."""
    argv = master_cli.master_argv(_Job({"source": "/tmp/a.wav", jobs.GATE_RUN_KEY: "r-1"}))
    assert "--run" not in argv


def test_an_empty_output_dir_and_an_omitted_one_freeze_identically():
    """The divergence R10 forbids, closed at the freeze rather than in two places.

    An empty string reaches ``output_path`` as ``Path(".")`` and lands the master
    in the working directory, while the argv builder drops a falsy flag and the
    respawned child writes beside the source. One invocation, two destinations.
    """
    assert master_cli.frozen_payload("/tmp/a.wav", "", False) == master_cli.frozen_payload(
        "/tmp/a.wav", None, False
    )
    assert "--output-dir" not in master_cli.master_argv(
        _Job(master_cli.frozen_payload("/tmp/a.wav", "", False))
    )


def test_a_payload_missing_this_builds_keys_still_builds_a_command_line():
    argv = master_cli.master_argv(_Job({"source": "/tmp/a.wav"}))
    assert argv[:2] == ["master", "/tmp/a.wav"]


# ---------------------------------------------------------------------------
# The work half: the archive promise
# ---------------------------------------------------------------------------


def test_the_source_is_byte_identical_after_a_full_run(tmp_path):
    """R6, asserted by digest rather than by mtime, over a real container."""
    source = _recording(tmp_path)
    before = mastering.digest(source)

    reported = master_cli.run_master(
        master_cli.frozen_payload(str(source), None, False), runner=_encoder()
    )

    assert mastering.digest(source) == before
    assert source.stat().st_size > 0
    assert reported["source"] == str(source)


def test_the_archive_is_taken_and_verified_against_the_source(tmp_path):
    """R7. The copy is the fallback the rest of the run depends on."""
    source = _recording(tmp_path)
    before = mastering.digest(source)

    reported = master_cli.run_master(
        master_cli.frozen_payload(str(source), None, False), runner=_encoder()
    )

    archived = Path(reported["archived_to"])
    assert archived.parent.name == mastering.ARCHIVE_DIRNAME
    assert mastering.digest(archived) == before


def test_an_archive_holding_different_audio_refuses_and_keeps_both(tmp_path):
    source = _recording(tmp_path)
    archive = tmp_path / mastering.ARCHIVE_DIRNAME
    archive.mkdir()
    impostor = archive / source.name
    impostor.write_bytes(b"a different recording with the same name")
    impostor_digest = mastering.digest(impostor)

    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload(str(source), None, False), runner=_encoder()
        )

    assert excinfo.value.cause.reason == "archive-holds-a-different-recording"
    assert mastering.digest(impostor) == impostor_digest, "the earlier recording was destroyed"
    assert source.exists()


# ---------------------------------------------------------------------------
# The work half: refusals arrive from the vocabulary
# ---------------------------------------------------------------------------


def test_a_recording_that_is_not_there_refuses_rather_than_raising(tmp_path):
    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload(str(tmp_path / "absent.wav"), None, False),
            runner=_encoder(),
        )
    cause = excinfo.value.cause
    assert cause.reason == "source-missing"
    assert cause.code is ExitCode.PRECONDITION
    assert cause.code is not ExitCode.INTERNAL, "a mistyped path is not a defect in this program"


def test_a_container_the_engine_does_not_read_refuses_under_its_own_slug(tmp_path):
    """A different slug from the missing case, and the difference is the sentence.

    A person told the file is absent goes looking for a file sitting in front of
    them.
    """
    unsupported = tmp_path / "REC001.m4a"
    unsupported.write_bytes(b"not a container this reads")

    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload(str(unsupported), None, False), runner=_encoder()
        )
    assert excinfo.value.cause.reason == "source-unsupported"


def test_an_existing_master_refuses_without_overwrite_and_proceeds_with_it(tmp_path):
    source = _recording(tmp_path)
    target = mastering.output_path(source)
    target.write_bytes(b"a master somebody already kept")
    kept = target.read_bytes()

    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload(str(source), None, False), runner=_encoder()
        )
    assert excinfo.value.cause.reason == "output-exists"
    assert target.read_bytes() == kept, "a refusal that leaves a trace has already done something"

    reported = master_cli.run_master(
        master_cli.frozen_payload(str(source), None, True), runner=_encoder()
    )
    assert reported["output"] == str(target)


def test_a_failing_encode_does_not_report_success(tmp_path):
    source = _recording(tmp_path)
    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload(str(source), None, False),
            runner=_encoder(encode_returncode=1),
        )
    assert excinfo.value.cause.reason == "encoder-failed"


def test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success(tmp_path):
    """The defect U44 drove, and the guard that keeps it closed.

    Before the fix this returned a report whose ``output`` named a file that was
    not there, whose ``output_bytes`` was 0, and whose ``size_reduction`` was
    therefore 1.0: a master that saved one hundred percent of the source's bytes.
    The zero exit status is a CLAIM about the output, and nothing read the output.
    """
    source = _recording(tmp_path)
    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload(str(source), None, False),
            runner=_encoder(encode_writes=False),
        )
    assert excinfo.value.cause.reason == "encoder-failed"
    assert "produced no output" in excinfo.value.cause.message


def test_an_encode_that_writes_an_empty_file_does_not_report_success(tmp_path):
    """A zero-byte FLAC is not a master, and 1.0 is the same false saving.

    Separate from the branch above because the two are different states of the
    filesystem and only one of them is caught by an existence check.
    """
    source = _recording(tmp_path)

    def empty(command):
        result = _encoder(encode_writes=False)(command)
        argv = list(command.argv)
        if not argv[0].endswith("ffprobe") and "pcm_s24le" not in argv and "null" not in argv:
            Path(argv[-1]).write_bytes(b"")
        return result

    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload(str(source), None, False), runner=empty
        )
    assert excinfo.value.cause.reason == "encoder-failed"


def test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding(tmp_path):
    """The branch KTD1's first argument does not cover, driven rather than argued.

    ``archive_source`` archives the SOURCE only and the encode writes straight to
    the destination, so the previous master is gone before the failure. The test
    asserts BOTH halves: no success is reported, and the source and its archive
    are still intact, which is what the refusal's own message promises.
    """
    source = _recording(tmp_path)
    before = mastering.digest(source)
    target = mastering.output_path(source)
    target.write_bytes(b"a master somebody already kept")

    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload(str(source), None, True),
            runner=_encoder(encode_returncode=1),
        )

    assert excinfo.value.cause.reason == "encoder-failed"
    assert mastering.digest(source) == before
    archived = tmp_path / mastering.ARCHIVE_DIRNAME / source.name
    assert archived.exists() and mastering.digest(archived) == before


def test_the_output_directory_is_honoured_and_never_the_source(tmp_path):
    """R2. The destination comes from the engine, and it is not the recording."""
    source = _recording(tmp_path)
    elsewhere = tmp_path / "masters"

    reported = master_cli.run_master(
        master_cli.frozen_payload(str(source), str(elsewhere), False), runner=_encoder()
    )

    assert Path(reported["output"]).parent == elsewhere
    assert Path(reported["output"]) != source
    assert reported["output"].endswith(mastering.OUTPUT_SUFFIX)
