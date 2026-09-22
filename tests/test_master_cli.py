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
from cratekit.cli import handlers, output, registry
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


def _recording(tmp_path: Path, name: str = "REC001.wav", *, seconds: int = 1) -> Path:
    """A real container, so the digest assertions are over real audio bytes."""
    require_ffmpeg()
    out = tmp_path / name
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-t", str(seconds), str(out)],
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
    # A LIST SINCE U105, which widened the positional to take every part of a
    # split recording. One path is a list of one.
    assert args.recording == ["/tmp/REC001.wav"]
    assert args.output_dir == "/tmp/out"
    assert args.overwrite is True
    assert args.job is None
    assert args.lufs is None


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


def test_naming_a_job_reports_it_rather_than_queueing_a_second(configured, monkeypatch):
    """Still one job after a resume, and now the resume also DOES the work.

    Rewritten for U46 rather than left alone. Before the handler binding a resume
    reconciled and reported, so any recording worked; now it claims the item and
    masters it, so this needs a real one and a stand-in encoder. The claim the test
    was written for, that naming a job continues it instead of queueing a second,
    is unchanged and is still what the last assertion measures.
    """
    source = _recording(configured.library.root)
    monkeypatch.setattr(mastering, "subprocess_runner", _encoder())
    code, first = _drive(["master", str(source)])
    assert code == int(ExitCode.OK)
    job_id = first["data"]["job_id"]

    code, again = _drive(["master", str(source), "--job", job_id])
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


# ---------------------------------------------------------------------------
# Round two: the two archive-path zeros the author's table left
# ---------------------------------------------------------------------------


def test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy(tmp_path, monkeypatch):
    """Closes A1 in ``docs/mutation/u44-author.md``, and drives ``archive-verify-failed``.

    With the post-copy digest comparison dropped, a copy that does not match the
    source is reported as the safety copy the rest of the run depends on. No
    filesystem here corrupts a write on demand, so the copy itself is stood in
    for: a ``copy2`` that writes the source and then one byte more.
    """
    source = _recording(tmp_path)
    before = mastering.digest(source)

    def corrupting_copy2(src, dst, **kwargs):
        Path(dst).write_bytes(Path(src).read_bytes() + b"\x00")
        return dst

    monkeypatch.setattr(mastering.shutil, "copy2", corrupting_copy2)

    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload(str(source), None, False), runner=_encoder()
        )

    cause = excinfo.value.cause
    assert cause.reason == "archive-verify-failed"
    assert cause.code is ExitCode.PRECONDITION
    assert not (tmp_path / mastering.ARCHIVE_DIRNAME / source.name).exists(), (
        "a copy that failed verification was left where a later run would trust it"
    )
    assert mastering.digest(source) == before
    assert not mastering.output_path(source).exists(), "the run proceeded without a verified archive"


def test_an_impostor_matching_the_first_chunk_is_still_a_different_recording(tmp_path):
    """Closes A4. The digest must read the whole file, not its first chunk.

    THE PREMISE IS ASSERTED, per the fixture-position lesson: the source has to
    be longer than one digest chunk, or an impostor identical up to that chunk is
    identical full stop and the row it exists to kill cannot matter.
    """
    source = _recording(tmp_path, seconds=8)
    chunk = 1 << 20
    assert source.stat().st_size > chunk, "the fixture sits where the guard cannot matter"

    archive = tmp_path / mastering.ARCHIVE_DIRNAME
    archive.mkdir()
    impostor = archive / source.name
    impostor.write_bytes(source.read_bytes()[:chunk] + b"a different set after the first chunk")
    impostor_digest = mastering.digest(impostor)

    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload(str(source), None, False), runner=_encoder()
        )

    assert excinfo.value.cause.reason == "archive-holds-a-different-recording"
    assert mastering.digest(impostor) == impostor_digest
    assert not mastering.output_path(source).exists()


# ---------------------------------------------------------------------------
# U46: the queued work is actually run
#
# Everything above this line drives ``run_master`` directly, which is the engine
# side. These drive the QUEUE: enqueue through the real dispatcher, then re-enter
# the verb with ``--job`` the way the child a resume spawns does, and read the
# item's row back from the store rather than inferring it from an exit status.
# ---------------------------------------------------------------------------


def _queued(source: Path, *extra: str) -> str:
    code, envelope = _drive(["master", str(source), *extra])
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["job_id"]


def _items(job_id: str) -> tuple[jobs.Item, ...]:
    with jobs.open_store() as store:
        return jobs.items(store, job_id)


def test_queueing_a_recording_gives_the_driver_one_item_to_claim(configured):
    """Without this the queue holds a job with nothing in it, and drive succeeds
    over work it never did."""
    source = configured.library.root / "REC001.wav"
    job_id = _queued(source)

    items = _items(job_id)
    assert [i.item_id for i in items] == [str(source)]
    assert items[0].state == jobs.ItemState.PENDING


def test_a_relative_recording_is_frozen_absolute_so_the_child_masters_the_same_file(
    configured, tmp_path, monkeypatch
):
    """The child inherits the RESUMING process's directory, not the queueing one."""
    monkeypatch.chdir(configured.library.root)
    job_id = _queued(Path("REC001.wav"))

    with jobs.open_store() as store:
        payload = jobs.get(store, job_id).payload
    assert payload[master_cli.SOURCE] == str(configured.library.root / "REC001.wav")
    assert Path(payload[master_cli.SOURCE]).is_absolute()


def test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch(
    configured, monkeypatch
):
    """The whole point of U46. Read from the store, not from the exit code."""
    source = _recording(configured.library.root)
    job_id = _queued(source)
    monkeypatch.setattr(mastering, "subprocess_runner", _encoder())

    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code == int(ExitCode.OK), envelope
    item = _items(job_id)[0]
    assert item.state == jobs.ItemState.DONE
    assert item.artifact == str(mastering.output_path(source))
    assert Path(item.artifact).is_file()
    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.SUCCEEDED


def test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place(
    configured, monkeypatch
):
    """The staging directory is why a killed encode does not poison the resume."""
    source = _recording(configured.library.root)
    job_id = _queued(source)
    seen: list[str] = []

    encoder = _encoder()

    def watching(command):
        seen.append(str(command.argv[-1]))
        return encoder(command)

    monkeypatch.setattr(mastering, "subprocess_runner", watching)
    _drive(["master", str(source), "--job", job_id])

    staging = master_cli.MASTER_STAGING_DIRNAME
    assert any(staging in target for target in seen), seen
    assert not any(
        target == str(mastering.output_path(source)) for target in seen
    ), "the encoder was pointed straight at the destination"


def test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt(
    configured, monkeypatch
):
    """The failure that made a killed master job permanently unresumable."""
    source = _recording(configured.library.root)
    job_id = _queued(source)
    final = mastering.output_path(source)
    stale = final.parent / master_cli.MASTER_STAGING_DIRNAME / job_id / "0"
    stale.mkdir(parents=True)
    (stale / final.name).write_bytes(b"half an encode")

    monkeypatch.setattr(mastering, "subprocess_runner", _encoder())
    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code == int(ExitCode.OK), envelope
    assert _items(job_id)[0].state == jobs.ItemState.DONE


def test_a_missing_recording_reports_the_engines_own_cause_on_the_item(configured):
    """Closes the half of R-191 that a driven job can close.

    The item carries ``source-missing``. The JOB carries the engine's partial
    failure cause, and the envelope carries ``no-evidence``, because a one-item
    job whose item failed is a TOTAL failure and the driver refuses to report an
    empty success. All three are asserted rather than one, because a reader who
    knows only the envelope would look for the slug in the wrong place.
    """
    source = configured.library.root / "nope.wav"
    job_id = _queued(source)

    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "no-evidence"
    item = _items(job_id)[0]
    assert item.state == jobs.ItemState.FAILED
    assert item.cause is not None and item.cause.reason == "source-missing"
    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.FAILED


def test_a_failed_job_stays_resumable_and_the_second_attempt_redoes_that_item(
    configured, monkeypatch
):
    """Reopening is ``job resume``'s act, and driving is this verb's.

    The two halves are asserted separately because the split is easy to read the
    wrong way round. Re-entering the verb on a job the engine has already recorded
    as failed does not re-drive it, a terminal job is not re-driven and
    ``jobs.drive`` refuses one outright, and it REFUSES with the job's own cause
    rather than reporting it (R-225: this asserted ``ExitCode.OK`` over the failed
    job until that closed here). What reopens it is ``crate job resume``, which calls
    ``jobs.retry`` and then spawns the child that arrives here. This drives
    ``retry`` directly rather than the spawning verb, because the child that verb
    starts is detached and the item's row is what this measures.
    """
    source = configured.library.root / "REC001.wav"
    job_id = _queued(source)
    _drive(["master", str(source), "--job", job_id])
    assert _items(job_id)[0].state == jobs.ItemState.FAILED

    code, reported = _drive(["master", str(source), "--job", job_id])
    assert code != int(ExitCode.OK), reported
    assert reported["outcome"] == "failed", reported
    assert _items(job_id)[0].state == jobs.ItemState.FAILED

    # THE REOPENING IS REFUSED (R-390). The item failed as ``source-missing``,
    # which the mastering module records as permanent, and ``jobs.retry`` reads
    # that flag before it re-arms anything. The recording arriving later is a
    # repair the person made, and the path for that is a fresh job, which is
    # what the refusal's steps say. The residual over whether a missing source
    # is honestly permanent is filed beside R-390 in the ledger.
    _recording(configured.library.root)
    monkeypatch.setattr(mastering, "subprocess_runner", _encoder())
    with jobs.open_store() as store:
        with pytest.raises(CratekitError) as excinfo:
            jobs.retry(store, job_id)
    assert excinfo.value.cause.reason == "job-not-retryable"
    assert excinfo.value.cause.inner is not None
    assert excinfo.value.cause.inner.reason == "source-missing"
    assert _items(job_id)[0].state == jobs.ItemState.FAILED

    fresh = _queued(source)
    assert fresh != job_id
    code, envelope = _drive(["master", str(source), "--job", fresh])
    assert code == int(ExitCode.OK), envelope
    assert _items(fresh)[0].state == jobs.ItemState.DONE


def test_an_existing_master_is_refused_before_the_engine_runs(configured, monkeypatch):
    """The check the handler had to take over, because the encode now stages."""
    source = _recording(configured.library.root)
    final = mastering.output_path(source)
    final.write_bytes(b"a master somebody kept")

    ran: list[str] = []
    monkeypatch.setattr(
        mastering, "subprocess_runner", lambda command: ran.append("ran") or (_ for _ in ()).throw(AssertionError("the engine ran"))
    )
    job_id = _queued(source)
    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code != int(ExitCode.OK)
    assert ran == [], "the destination check happened after the engine started"
    item = _items(job_id)[0]
    assert item.cause is not None and item.cause.reason == "output-exists"
    assert final.read_bytes() == b"a master somebody kept"


def test_overwrite_reaches_the_handler_and_replaces_the_previous_master(
    configured, monkeypatch
):
    source = _recording(configured.library.root)
    final = mastering.output_path(source)
    final.write_bytes(b"the previous master")
    monkeypatch.setattr(mastering, "subprocess_runner", _encoder())

    job_id = _queued(source, "--overwrite")
    code, envelope = _drive(["master", str(source), "--overwrite", "--job", job_id])

    assert code == int(ExitCode.OK), envelope
    assert final.read_bytes() != b"the previous master"


def test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect(
    configured, monkeypatch
):
    """R-192's drive. Cheap once something calls this path at all."""
    source = _recording(configured.library.root)
    job_id = _queued(source)

    # Through the OVERRIDE the resolver actually reads, rather than by replacing
    # the resolver. A stand-in that raises would prove this test can raise.
    monkeypatch.setenv("CRATEKIT_BIN_FFMPEG", str(configured.library.root / "no-ffmpeg"))
    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code != int(ExitCode.OK)
    item = _items(job_id)[0]
    assert item.cause is not None and item.cause.reason == "encoder-missing"


def test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause(
    configured, monkeypatch
):
    """An encoder that reports success and writes nothing.

    THE CAUSE IS ASSERTED, not just the failure, and that is what this test is for.
    The handler carried its own "the reported file is not there" check until this
    was driven; the check killed zero tests because the engine refuses first, and
    an unreachable branch is a finding rather than a guard. What a person actually
    sees is ``encoder-failed`` with the engine's remediation, and this is what says
    so.
    """
    source = _recording(configured.library.root)
    job_id = _queued(source)
    monkeypatch.setattr(mastering, "subprocess_runner", _encoder(encode_writes=False))

    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code != int(ExitCode.OK)
    assert not mastering.output_path(source).exists()
    item = _items(job_id)[0]
    assert item.cause is not None and item.cause.reason == "encoder-failed"
    assert "FileNotFoundError" not in item.cause.message


def test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver(
    configured, monkeypatch
):
    source = configured.library.root / "REC001.wav"
    job_id = _queued(source)

    def exploding(job, item, cfg):
        raise RuntimeError("something nobody declared")

    monkeypatch.setattr(handlers, "resolve", lambda key: exploding)
    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code != int(ExitCode.OK)
    item = _items(job_id)[0]
    assert item.state == jobs.ItemState.FAILED
    assert item.cause is not None and item.cause.reason == "internal-error"


def test_a_job_show_says_when_a_queued_verb_has_no_worker(configured, monkeypatch):
    """One verb working and nineteen silent is worse than all of them silent.

    THE UNBOUND SUBJECT IS DERIVED, never named. It was ``rebuild`` until U53
    bound that key, and a name here expires silently every time a unit binds one:
    the assertion would then be reading a bound verb's answer and comparing it to
    the unbound wording.

    AND SINCE U61 IT IS MADE UNBOUND HERE, because R-203 closed: every queued
    verb now has a worker, and the one declaration left in the unbound table is
    ``job.resume``, which is never queued. The property is ``job show`` reading
    the table, which is the same whichever key the table names, so one bound key
    is moved across for this test and the reading is asserted over it.
    """
    source = configured.library.root / "REC001.wav"
    job_id = _queued(source)

    code, envelope = _drive(["job", "show", job_id])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["progress"]["worker"] == "bound"
    assert envelope["data"]["progress"]["worker_reason"] is None

    moved = sorted(handlers.HANDLERS)[0]
    reason = "no worker in this build, a declaration this test made"
    monkeypatch.setattr(
        handlers, "HANDLERS", {k: v for k, v in handlers.HANDLERS.items() if k != moved}
    )
    monkeypatch.setattr(
        handlers,
        "HANDLERS_NOT_YET_BOUND",
        {**handlers.HANDLERS_NOT_YET_BOUND, moved: reason},
    )
    with jobs.open_store() as store:
        other = jobs.enqueue(store, handler_key=moved, payload={}, cfg=configured)
    code, envelope = _drive(["job", "show", other.job_id])
    assert envelope["data"]["progress"]["worker"] == "none"
    assert envelope["data"]["progress"]["worker_reason"] == reason


def test_a_relative_output_dir_is_frozen_absolute_too(configured, tmp_path, monkeypatch):
    """The directory needs it as much as the recording does.

    ``master_argv`` rebuilds ``--output-dir`` from the payload verbatim, and the
    child inherits the RESUMING process's working directory, so a relative one
    sends the master somewhere the person did not ask for and reports success.
    """
    monkeypatch.chdir(configured.library.root)
    (configured.library.root / "out").mkdir()
    job_id = _queued(Path("REC001.wav"), "--output-dir", "out")

    with jobs.open_store() as store:
        payload = jobs.get(store, job_id).payload
    assert payload[master_cli.OUTPUT_DIR] == str(configured.library.root / "out")
    assert Path(payload[master_cli.OUTPUT_DIR]).is_absolute()


def test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere(
    configured, tmp_path, monkeypatch
):
    """The drive, not just the freeze. Queue from one directory, resume from another."""
    source = _recording(configured.library.root)
    monkeypatch.chdir(configured.library.root)
    job_id = _queued(Path(source.name))

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    monkeypatch.setattr(mastering, "subprocess_runner", _encoder())
    code, envelope = _drive(["master", source.name, "--job", job_id])

    assert code == int(ExitCode.OK), envelope
    item = _items(job_id)[0]
    assert item.state == jobs.ItemState.DONE
    assert item.artifact == str(mastering.output_path(source))
    assert Path(item.artifact).is_file()


def test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there(
    configured
):
    """``source-missing`` promises nothing was read and nothing was written."""
    source = configured.library.root / "Sets" / "nope.wav"
    job_id = _queued(source)

    _drive(["master", str(source), "--job", job_id])

    assert not source.parent.exists(), (
        "a staging tree was built beside a destination for a recording that "
        "does not exist, which falsifies the refusal's own remediation"
    )
    assert _items(job_id)[0].cause.reason == "source-missing"


def test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume(
    configured, tmp_path, monkeypatch
):
    """Drift, driven through the verb's own envelope rather than through the driver.

    The two halves are each covered elsewhere. What nothing measured until this is
    the wiring between them: a resume that dropped its warnings would report a run
    against a configuration the person had already changed, silently.
    """
    source = _recording(configured.library.root)
    job_id = _queued(source)

    moved = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(configured.library.root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(configured.library.root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "moved-staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(moved)
    config.reset_cache()

    monkeypatch.setattr(mastering, "subprocess_runner", _encoder())
    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code == int(ExitCode.OK), envelope
    codes = [warning["code"] for warning in envelope.get("warnings", [])]
    assert "config-drift" in codes, envelope.get("warnings")
    assert _items(job_id)[0].state == jobs.ItemState.DONE


# ---------------------------------------------------------------------------
# U105: a recording the player split into several files, and a loudness target
# ---------------------------------------------------------------------------


def _tone(directory: Path, name: str, *, seconds: int, rate: int = 44100) -> Path:
    """A real sine recording. Silence measures as negative infinity and a real
    encode then refuses for the missing measurement, so the joined-duration proof
    needs a signal."""
    require_ffmpeg()
    out = directory / name
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", f"sine=frequency=220:r={rate}",
         "-t", str(seconds), "-c:a", "pcm_s16le", str(out)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0 and out.exists(), proc.stderr[-400:]
    return out


def _duration(path: Path) -> float:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr[-400:]
    return float(proc.stdout.strip())


#: What the stand-in probe reports for a part it has no override for: the whole
#: layout ``probe_source`` reads, so a part differing in one field differs in
#: that field alone.
PROBED = {"sample_rate": "44100", "sample_fmt": "s16", "channels": "2", "codec_name": "pcm_s16le"}


def _recorder(layouts: dict[str, dict[str, str]] | None = None):
    """The stand-in encoder, recording every command, with a per-part probe.

    ``layouts`` maps a file NAME to the probe fields that differ from
    ``PROBED`` for it, which is how a split recording at mixed rates, channel
    counts or codecs is produced without encoding one.
    """
    seen: list[mastering.Command] = []
    inner = _encoder()

    def run(command: mastering.Command) -> mastering.CommandResult:
        seen.append(command)
        argv = list(command.argv)
        if argv[0].endswith("ffprobe"):
            fields = {**PROBED, **(layouts or {}).get(Path(argv[-1]).name, {})}
            return mastering.CommandResult(
                returncode=0, stdout="".join(f"{k}={v}\n" for k, v in fields.items())
            )
        return inner(command)

    return run, seen


#: One FLAC frame at 44.1 kHz, the tolerance the brief's "within a frame" names.
#: FLAC encodes in blocks of 4096 samples at compression level 8, so a length
#: that differs by less than one block is the same length for this purpose.
ONE_FRAME_SECONDS = 4096 / 44100


def test_two_parts_produce_one_master_whose_duration_is_their_sum(tmp_path):
    """The brief's first scenario, over a REAL encode rather than a stand-in.

    A stand-in cannot prove a duration, and the failure this exists for is a join
    that drops or repeats a part, which only the audio shows.
    """
    first = _tone(tmp_path, "REC001.wav", seconds=2)
    second = _tone(tmp_path, "REC002.wav", seconds=3)
    digests = [mastering.digest(first), mastering.digest(second)]

    reported = master_cli.run_master(
        master_cli.frozen_payload([str(first), str(second)], None, False)
    )

    output = Path(reported["output"])
    assert output == tmp_path / "REC001_set_mastered.flac"
    assert _duration(output) == pytest.approx(
        _duration(first) + _duration(second), abs=ONE_FRAME_SECONDS
    )
    # The parts are untouched and each has its own verified archive copy.
    assert [mastering.digest(first), mastering.digest(second)] == digests
    assert reported["parts"] == [str(first), str(second)]
    assert [mastering.digest(Path(a)) for a in reported["archives"]] == digests
    # The joined intermediate is this module's and does not survive the run.
    assert not list(tmp_path.glob(".cratekit-join-*"))
    assert not (tmp_path / "REC001_set.wav").exists()


def test_the_parts_are_joined_in_the_order_given_and_never_sorted(tmp_path):
    """The brief's second scenario, measured at the join itself.

    Named so a sort would reverse them: the second part is given first.
    """
    later = _recording(tmp_path, "REC002.wav")
    earlier = _recording(tmp_path, "REC001.wav")
    run, _ = _recorder()
    listed: list[str] = []

    def capture(command):
        if "concat" in command.argv:
            listing = Path(command.argv[command.argv.index("-i") + 1])
            listed.extend(listing.read_text().splitlines())
        return run(command)

    reported = master_cli.run_master(
        master_cli.frozen_payload([str(later), str(earlier)], None, False),
        runner=capture,
    )

    assert [line.split("/")[-1].rstrip("'") for line in listed] == [
        "REC002.wav", "REC001.wav"
    ]
    assert reported["parts"] == [str(later), str(earlier)]
    assert Path(reported["output"]).name == "REC002_set_mastered.flac"


def test_the_order_printed_is_the_order_given(configured):
    """The plan says the order back before anything is read or written."""
    root = configured.library.root
    parts = [root / "REC003.wav", root / "REC001.wav", root / "REC002.wav"]
    code, envelope = _drive(["master", *map(str, parts)])

    assert code == int(ExitCode.OK), envelope
    warning = next(w for w in envelope["warnings"] if w["code"] == "join-order")
    positions = [warning["message"].index(str(p)) for p in parts]
    assert positions == sorted(positions), warning["message"]
    assert "1. " + str(parts[0]) in warning["message"]
    # And the order printed is the order frozen, which is the one the run uses.
    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
    assert job.payload[master_cli.PARTS] == [str(p) for p in parts]
    assert [i.item_id for i in _items(job.job_id)] == [str(parts[0])]


def test_one_input_freezes_queues_and_resumes_exactly_as_before(configured):
    """The brief's third scenario. No new key, no new flag, no notice."""
    source = configured.library.root / "REC001.wav"
    assert master_cli.frozen_payload([str(source)], None, False) == {
        "source": str(source),
        "output_dir": None,
        "overwrite": False,
    }
    assert master_cli.frozen_payload([str(source)], None, False) == (
        master_cli.frozen_payload(str(source), None, False)
    )
    assert master_cli.master_argv(
        _Job(master_cli.frozen_payload([str(source)], None, False))
    ) == ["master", str(source), "--job", "job-1"]

    code, envelope = _drive(["master", str(source)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["warnings"] == []


def test_one_input_masters_through_the_unchanged_engine_path(tmp_path):
    """A single recording's report carries no join keys and its own archive."""
    source = _recording(tmp_path)
    run, seen = _recorder()
    reported = master_cli.run_master(
        master_cli.frozen_payload([str(source)], None, False), runner=run
    )
    assert "parts" not in reported and "archives" not in reported
    assert Path(reported["output"]).name == "REC001_mastered.flac"
    assert not any("concat" in c.argv for c in seen)


@pytest.mark.parametrize("value", [-4.0, -70.5, float("nan"), float("inf")])
def test_an_out_of_range_target_is_refused_by_the_engine(value):
    with pytest.raises(ValueError, match="target_lufs"):
        mastering.Settings(target_lufs=value)


@pytest.mark.parametrize("value", [-70.0, -5.0, -14.0])
def test_the_range_bounds_are_inclusive(value):
    assert mastering.Settings(target_lufs=value).target_lufs == value


@pytest.mark.parametrize("value", ["-4", "-71", "nan"])
def test_an_out_of_range_target_refuses_and_queues_nothing(configured, value):
    """The brief's fourth scenario, through the verb."""
    code, envelope = _drive(
        ["master", str(configured.library.root / "REC001.wav"), f"--lufs={value}"]
    )
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "target-lufs-out-of-range"
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 0


def test_the_target_reaches_every_loudnorm_filter(tmp_path):
    """A frozen target that the engine never sees is a flag that does nothing."""
    source = _recording(tmp_path)
    run, seen = _recorder()
    master_cli.run_master(
        master_cli.frozen_payload([str(source)], None, False, lufs=-9.0), runner=run
    )
    filters = [
        c.argv[c.argv.index("-af") + 1] for c in seen if "loudnorm" in " ".join(c.argv)
    ]
    assert len(filters) == 3, filters
    assert all("I=-9.0:" in f for f in filters), filters


def test_a_split_recording_and_its_target_survive_the_resume_argv(configured):
    """R10 for the two new keys: the argv rebuilds the payload it came from."""
    root = configured.library.root
    frozen = master_cli.frozen_payload(
        [str(root / "B.wav"), str(root / "A.wav")], str(root / "out"), True, lufs=-16.0
    )
    argv = master_cli.master_argv(_Job(frozen))
    args = cli.build_parser([_entry()]).parse_args(argv)
    assert master_cli.frozen_payload(
        args.recording, args.output_dir, args.overwrite, lufs=args.lufs
    ) == frozen
    assert args.job == "job-1"


def test_a_negative_target_parses_as_two_tokens_as_well():
    args = cli.build_parser([_entry()]).parse_args(["master", "/tmp/a.wav", "--lufs", "-16"])
    assert args.lufs == -16.0 and args.recording == ["/tmp/a.wav"]


def test_parts_at_different_sample_rates_refuse_before_anything_is_written(tmp_path):
    """The brief's hazard. A stream copy would not fail, it would lie."""
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.wav")
    run, seen = _recorder({"REC002.wav": {"sample_rate": "48000"}})

    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload([str(first), str(second)], None, False), runner=run
        )

    assert excinfo.value.cause.reason == "source-unsupported"
    assert "48000" in excinfo.value.cause.message
    assert not (tmp_path / mastering.ARCHIVE_DIRNAME).exists()
    assert not any("concat" in c.argv for c in seen)
    assert set(tmp_path.iterdir()) == {first, second}


def test_a_part_named_twice_refuses(tmp_path):
    part = _recording(tmp_path)
    run, seen = _recorder()
    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload([str(part), str(part)], None, False), runner=run
        )
    assert excinfo.value.cause.reason == "source-unsupported"
    assert seen == []


def test_parts_in_different_containers_refuse(tmp_path):
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.flac")
    run, seen = _recorder()
    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload([str(first), str(second)], None, False), runner=run
        )
    assert excinfo.value.cause.reason == "source-unsupported"
    assert seen == []


def test_a_missing_part_refuses_as_missing(tmp_path):
    first = _recording(tmp_path, "REC001.wav")
    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload([str(first), str(tmp_path / "REC002.wav")], None, False),
            runner=_encoder(),
        )
    assert excinfo.value.cause.reason == "source-missing"


def test_a_queued_split_recording_lands_as_one_master_through_the_resume(
    configured, monkeypatch
):
    """The whole path a person travels: queue two parts, resume, one master."""
    root = configured.library.root
    first = _recording(root, "REC001.wav")
    second = _recording(root, "REC002.wav")
    run, seen = _recorder()
    monkeypatch.setattr(mastering, "subprocess_runner", run)

    job_id = _queued(first, str(second), "--lufs", "-12")
    code, envelope = _drive(["master", str(first), str(second), "--lufs=-12", "--job", job_id])

    assert code == int(ExitCode.OK), envelope
    assert (root / "REC001_set_mastered.flac").is_file()
    assert not (root / "REC001_mastered.flac").exists()
    assert (root / mastering.ARCHIVE_DIRNAME / "REC002.wav").is_file()
    assert any("concat" in c.argv for c in seen)
    assert all(
        "I=-12.0:" in c.argv[c.argv.index("-af") + 1]
        for c in seen
        if "loudnorm" in " ".join(c.argv)
    )


def test_an_existing_joined_master_is_refused_on_the_real_destination(
    configured, monkeypatch
):
    """The pre-check before staging names the JOINED master, not part one's."""
    root = configured.library.root
    first = _recording(root, "REC001.wav")
    second = _recording(root, "REC002.wav")
    kept = root / "REC001_set_mastered.flac"
    kept.write_bytes(b"a master somebody kept")
    run, seen = _recorder()
    monkeypatch.setattr(mastering, "subprocess_runner", run)

    job_id = _queued(first, str(second))
    code, envelope = _drive(["master", str(first), str(second), "--job", job_id])

    assert code != int(ExitCode.OK)
    assert _items(job_id)[0].cause.reason == "output-exists"
    assert kept.read_bytes() == b"a master somebody kept"
    assert seen == []


@pytest.mark.parametrize(
    "differs",
    [
        {"channels": "1"},
        {"codec_name": "pcm_s32le", "sample_fmt": "s32"},
        {"sample_fmt": "s32"},
    ],
    ids=["mono-beside-stereo", "codec", "sample-format"],
)
def test_parts_differing_in_any_copied_field_refuse(tmp_path, differs):
    """Found by this unit's review: rate alone admitted a mono part and a 24 bit
    part beside a 32 bit one, both copied across unconverted."""
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.wav")
    run, seen = _recorder({"REC002.wav": differs})

    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload([str(first), str(second)], None, False), runner=run
        )

    assert excinfo.value.cause.reason == "source-unsupported"
    assert not (tmp_path / mastering.ARCHIVE_DIRNAME).exists()
    assert not any("concat" in c.argv for c in seen)


def test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone(tmp_path):
    """Both are ``s32`` as a sample format, so the codec is the only field that
    separates them. Pinned alone so the codec comparison cannot hide behind the
    sample format one."""
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.wav")
    same_fmt = {"sample_fmt": "s32"}
    run, _ = _recorder(
        {"REC001.wav": {**same_fmt, "codec_name": "pcm_s24le"},
         "REC002.wav": {**same_fmt, "codec_name": "pcm_s32le"}}
    )
    with pytest.raises(CratekitError) as excinfo:
        master_cli.run_master(
            master_cli.frozen_payload([str(first), str(second)], None, False), runner=run
        )
    assert "pcm_s32le" in excinfo.value.cause.message


def test_a_joined_wav_is_written_as_rf64_when_it_needs_to_be(tmp_path):
    """Found by this unit's review. A plain WAV header's length wraps at 4 GiB,
    and a split recording is split because it is long."""
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.wav")
    run, seen = _recorder()
    master_cli.run_master(
        master_cli.frozen_payload([str(first), str(second)], None, False), runner=run
    )
    join = next(c for c in seen if "concat" in c.argv)
    assert join.argv[join.argv.index("-rf64") + 1] == "auto"
    drift = next(c for c in seen if "pcm_s24le" in c.argv)
    assert drift.argv[drift.argv.index("-rf64") + 1] == "auto"


def test_a_joined_flac_carries_no_wav_muxer_option(tmp_path):
    first = tmp_path / "REC001.flac"
    second = tmp_path / "REC002.flac"
    first.write_bytes(b"one")
    second.write_bytes(b"two")
    run, seen = _recorder()
    master_cli.run_master(
        master_cli.frozen_payload([str(first), str(second)], None, False), runner=run
    )
    join = next(c for c in seen if "concat" in c.argv)
    assert "-rf64" not in join.argv


def test_the_engine_refuses_an_existing_joined_master_before_archiving(tmp_path):
    """The engine's own check, not the handler's pre-check. ``master`` would
    also refuse the same destination, but only after every part was archived
    and the whole set joined, which is minutes of writes for a refusal that was
    decidable by reading."""
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.wav")
    (tmp_path / "REC001_set_mastered.flac").write_bytes(b"kept")
    run, seen = _recorder()

    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.master_parts([first, second], runner=run)

    assert excinfo.value.refusal is mastering.Refusal.OUTPUT_EXISTS
    assert not (tmp_path / mastering.ARCHIVE_DIRNAME).exists()
    assert seen == []
