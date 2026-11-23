"""U44: ``crate master``, the shell over the mastering engine (row 30).

``tests/modules/test_tools.py`` proves the engine; this proves the shell reaches it, refusals
arrive as refusals and a resume rebuilds the run. The stand-in encoder dispatches on its argv.
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

#: One loudnorm report answering the measure passes and the encode's own report.
LOUDNORM = json.dumps({
    "input_i": "-20.0", "input_lra": "5.0", "input_tp": "-3.0", "input_thresh": "-30.0",
    "target_offset": "0.5", "output_i": "-14.0", "output_lra": "5.0", "output_tp": "-1.0",
})


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    return root


@pytest.fixture
def configured(library):
    """A set-up machine with NO DATABASE, which is all this verb may have."""
    cfg = _config(library, library.parent / "staging")
    config.save(cfg)
    config.reset_cache()
    return cfg


def _config(library: Path, staging: Path) -> config.Config:
    return config.from_dict({
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(library), "volume_id": "F1E2-D3C4",
            "db_path": str(library / "db" / "master.db"),
        },
        "paths": {"download_staging": str(staging)},
        "profile": {"name": "full"},
    })


def _entry() -> registry.Entry:
    return next(e for e in registry.ENTRIES if e.name == "master")


def _recording(tmp_path: Path, name: str = "REC001.wav", *, seconds: int = 1) -> Path:
    """A real container, so the digest assertions are over real audio bytes."""
    require_ffmpeg()
    return _synthesize(tmp_path / name, "anullsrc=r=44100:cl=stereo", seconds)


#: ffmpeg's rendering of each lavfi source, kept so a second request copies it.
_RENDERED: dict[tuple, bytes] = {}


def _synthesize(out: Path, source: str, seconds: int, *codec: str) -> Path:
    """Render ``source`` to ``out`` once, then copy; never through ``tempfile``, which is seeded."""
    key = (out.suffix, source, seconds, codec)
    if key in _RENDERED:
        out.write_bytes(_RENDERED[key])
        return out
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", source, "-t", str(seconds), *codec, str(out)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0 and out.exists(), proc.stderr[-400:]
    _RENDERED[key] = out.read_bytes()
    return out


def _master(*parts: Path, output_dir=None, overwrite=False, runner=None):
    """``run_master`` over the payload the shell freezes for these parts."""
    recording = str(parts[0]) if len(parts) == 1 else [str(p) for p in parts]
    payload = master_cli.frozen_payload(recording, output_dir, overwrite)
    return master_cli.run_master(payload, runner=runner or _encoder())


def _refused(*parts: Path, **kwargs):
    """The cause a ``run_master`` refusal carries."""
    with pytest.raises(CratekitError) as excinfo:
        _master(*parts, **kwargs)
    return excinfo.value.cause


def _encoder(*, encode_returncode: int = 0, encode_writes: bool = True):
    """A stand-in ffmpeg and ffprobe that answers each stage on its own terms."""
    def run(command: mastering.Command) -> mastering.CommandResult:
        argv = list(command.argv)
        if argv[0].endswith("ffprobe"):
            probed = "sample_rate=44100\nsample_fmt=s16\n"
            return mastering.CommandResult(returncode=0, stdout=probed)
        if "-f" in argv and "null" in argv:
            return mastering.CommandResult(returncode=0, stderr=LOUDNORM)
        if "pcm_s24le" in argv:
            Path(argv[-1]).write_bytes(b"intermediate")
            return mastering.CommandResult(returncode=0)
        if encode_writes:
            Path(argv[-1]).write_bytes(b"x" * 64)
        return mastering.CommandResult(returncode=encode_returncode, stderr=LOUDNORM)
    return run


# ── The declared surface ──


def test_the_parser_accepts_the_whole_declared_argument_shape():
    parser = cli.build_parser([_entry()])
    argv = ["master", "/tmp/REC001.wav", "--output-dir", "/tmp/out", "--overwrite"]
    args = parser.parse_args(argv)
    # A list since the positional takes every part of a split recording.
    assert args.recording == ["/tmp/REC001.wav"]
    assert (args.output_dir, args.overwrite, args.job, args.lufs) == ("/tmp/out", True, None, None)


def test_the_entry_is_landed_declares_no_gate_and_is_absent_from_a_slim_profile(configured):
    """R1's second half: the toggle decides, so this is a property of the entry."""
    del configured
    entry = _entry()
    assert not entry.available_to(profiles.resolve("slim"))
    assert entry.available_to(profiles.resolve("full"))
    assert entry.landed and entry.gates == ()
    assert entry.long_running and entry.argv_builder == "master_argv"
    assert entry.destructive and entry.writes == frozenset({"files"})


# ── The queued half ──


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
    assert (envelope["verb"], envelope["schema"]) == ("master", "job_state/1")
    assert envelope["data"]["job_id"]


def test_an_empty_recording_and_an_unknown_job_refuse_from_the_vocabulary(configured):
    del configured
    code, envelope = _drive(["master", ""])
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "source-missing"
    code, envelope = _drive(["master", "/tmp/a.wav", "--job", "no-such-job"])
    assert code != int(ExitCode.OK)
    assert code in {int(c) for c in ExitCode}
    assert envelope["cause"]["reason"] == "job-unknown"


def test_naming_a_job_reports_it_rather_than_queueing_a_second(configured, monkeypatch):
    """Still one job after a resume, and now the resume also DOES the work."""
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


# ── The resume argv (R10) ──


class _Job:
    job_id = "job-1"

    def __init__(self, payload):
        self.payload = payload


def test_the_resume_argv_rebuilds_every_frozen_flag_and_omits_absent_ones():
    full = {"source": "/tmp/REC001.wav", "output_dir": "/tmp/out", "overwrite": True}
    argv = master_cli.master_argv(_Job(full))
    assert argv[argv.index("--output-dir") + 1] == "/tmp/out"
    assert "--overwrite" in argv
    assert argv[argv.index("--job") + 1] == "job-1"
    assert argv[0] == "master" and argv[1] == "/tmp/REC001.wav"

    argv = master_cli.master_argv(_Job({**full, "output_dir": None, "overwrite": False}))
    assert "--output-dir" not in argv and "--overwrite" not in argv
    assert argv[:2] == ["master", "/tmp/REC001.wav"]
    assert "--job" in argv

    # No --run, since the verb declares no gate, and a payload missing keys still builds.
    argv = master_cli.master_argv(_Job({"source": "/tmp/a.wav", jobs.GATE_RUN_KEY: "r-1"}))
    assert "--run" not in argv
    assert master_cli.master_argv(_Job({"source": "/tmp/a.wav"}))[:2] == ["master", "/tmp/a.wav"]


def test_an_empty_output_dir_and_an_omitted_one_freeze_identically():
    """The divergence R10 forbids, closed at the freeze rather than in two places."""
    empty = master_cli.frozen_payload("/tmp/a.wav", "", False)
    assert empty == master_cli.frozen_payload("/tmp/a.wav", None, False)
    assert "--output-dir" not in master_cli.master_argv(_Job(empty))


# ── The work half: the archive promise ──


def test_the_source_is_byte_identical_and_its_archive_verified_after_a_full_run(tmp_path):
    """R6 and R7, asserted by digest over a real container."""
    source = _recording(tmp_path)
    before = mastering.digest(source)

    reported = _master(source)

    assert mastering.digest(source) == before
    assert source.stat().st_size > 0
    assert reported["source"] == str(source)
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

    assert _refused(source).reason == "archive-holds-a-different-recording"
    assert mastering.digest(impostor) == impostor_digest, "the earlier recording was destroyed"
    assert source.exists()


# ── The work half: refusals arrive from the vocabulary ──


def test_a_recording_that_is_not_there_refuses_rather_than_raising(tmp_path):
    cause = _refused(tmp_path / "absent.wav")
    assert cause.reason == "source-missing"
    assert cause.code is ExitCode.PRECONDITION
    assert cause.code is not ExitCode.INTERNAL, "a mistyped path is not a defect in this program"
    # A container the engine does not read has a slug of its own.
    unsupported = tmp_path / "REC001.m4a"
    unsupported.write_bytes(b"not a container this reads")

    assert _refused(unsupported).reason == "source-unsupported"


def test_an_existing_master_refuses_without_overwrite_and_proceeds_with_it(tmp_path):
    source = _recording(tmp_path)
    target = mastering.output_path(source)
    target.write_bytes(b"a master somebody already kept")
    kept = target.read_bytes()

    assert _refused(source).reason == "output-exists"
    assert target.read_bytes() == kept, "a refusal that leaves a trace has already done something"
    assert _master(source, overwrite=True)["output"] == str(target)


def test_a_failing_encode_does_not_report_success(tmp_path):
    source = _recording(tmp_path)
    assert _refused(source, runner=_encoder(encode_returncode=1)).reason == "encoder-failed"


def test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success(tmp_path):
    """The defect U44 drove, and the guard that keeps it closed."""
    cause = _refused(_recording(tmp_path), runner=_encoder(encode_writes=False))
    assert cause.reason == "encoder-failed"
    assert "produced no output" in cause.message


def test_an_encode_that_writes_an_empty_file_does_not_report_success(tmp_path):
    """A zero-byte FLAC is not a master, and 1.0 is the same false saving."""
    source = _recording(tmp_path)

    def empty(command):
        result = _encoder(encode_writes=False)(command)
        argv = list(command.argv)
        if not argv[0].endswith("ffprobe") and "pcm_s24le" not in argv and "null" not in argv:
            Path(argv[-1]).write_bytes(b"")
        return result

    assert _refused(source, runner=empty).reason == "encoder-failed"


def test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding(tmp_path):
    """The branch KTD1's first argument does not cover, driven rather than argued."""
    source = _recording(tmp_path)
    before = mastering.digest(source)
    target = mastering.output_path(source)
    target.write_bytes(b"a master somebody already kept")

    assert _refused(source, overwrite=True, runner=_encoder(encode_returncode=1)).reason == (
        "encoder-failed"
    )
    assert mastering.digest(source) == before
    archived = tmp_path / mastering.ARCHIVE_DIRNAME / source.name
    assert archived.exists() and mastering.digest(archived) == before


def test_the_output_directory_is_honoured_and_never_the_source(tmp_path):
    """R2. The destination comes from the engine, and it is not the recording."""
    source = _recording(tmp_path)
    elsewhere = tmp_path / "masters"

    reported = _master(source, output_dir=str(elsewhere))

    assert Path(reported["output"]).parent == elsewhere
    assert Path(reported["output"]) != source
    assert reported["output"].endswith(mastering.OUTPUT_SUFFIX)


# ── Round two: the two archive-path zeros the author's table left ──


def test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy(tmp_path, monkeypatch):
    """Closes A1 in ``docs/mutation/u44-author.md``, and drives ``archive-verify-failed``."""
    source = _recording(tmp_path)
    before = mastering.digest(source)

    def corrupting_copy2(src, dst, **kwargs):
        Path(dst).write_bytes(Path(src).read_bytes() + b"\x00")
        return dst

    monkeypatch.setattr(mastering.shutil, "copy2", corrupting_copy2)

    cause = _refused(source)
    assert cause.reason == "archive-verify-failed"
    assert cause.code is ExitCode.PRECONDITION
    assert not (tmp_path / mastering.ARCHIVE_DIRNAME / source.name).exists(), "a bad copy stayed"
    assert mastering.digest(source) == before
    assert not mastering.output_path(source).exists(), "the run went on without an archive"


def test_an_impostor_matching_the_first_chunk_is_still_a_different_recording(tmp_path):
    """Closes A4. The digest must read the whole file, not its first chunk."""
    source = _recording(tmp_path, seconds=8)
    chunk = 1 << 20
    assert source.stat().st_size > chunk, "the fixture sits where the guard cannot matter"

    archive = tmp_path / mastering.ARCHIVE_DIRNAME
    archive.mkdir()
    impostor = archive / source.name
    impostor.write_bytes(source.read_bytes()[:chunk] + b"a different set after the first chunk")
    impostor_digest = mastering.digest(impostor)

    assert _refused(source).reason == "archive-holds-a-different-recording"
    assert mastering.digest(impostor) == impostor_digest
    assert not mastering.output_path(source).exists()


# ── U46: the queued work is actually run, read back from the item's row ──


def _queued(source: Path, *extra: str) -> str:
    code, envelope = _drive(["master", str(source), *extra])
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["job_id"]


def _items(job_id: str) -> tuple[jobs.Item, ...]:
    with jobs.open_store() as store:
        return jobs.items(store, job_id)


def test_queueing_a_recording_gives_the_driver_one_item_to_claim(configured):
    """Without this the queue holds a job with nothing in it."""
    source = configured.library.root / "REC001.wav"
    job_id = _queued(source)

    items = _items(job_id)
    assert [i.item_id for i in items] == [str(source)]
    assert items[0].state == jobs.ItemState.PENDING


def test_a_relative_recording_and_output_dir_are_frozen_absolute(configured, monkeypatch):
    """The child inherits the RESUMING process's directory, not the queueing one."""
    monkeypatch.chdir(configured.library.root)
    (configured.library.root / "out").mkdir()
    job_id = _queued(Path("REC001.wav"), "--output-dir", "out")

    with jobs.open_store() as store:
        payload = jobs.get(store, job_id).payload
    assert payload[master_cli.SOURCE] == str(configured.library.root / "REC001.wav")
    assert Path(payload[master_cli.SOURCE]).is_absolute()
    assert payload[master_cli.OUTPUT_DIR] == str(configured.library.root / "out")
    assert Path(payload[master_cli.OUTPUT_DIR]).is_absolute()


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

    assert any(master_cli.MASTER_STAGING_DIRNAME in target for target in seen), seen
    assert str(mastering.output_path(source)) not in seen, "the encode aimed at the destination"


def test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt(configured, monkeypatch):
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
    """Closes the half of R-191 that a driven job can close."""
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


def test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it(
    configured, monkeypatch
):
    """Reopening is ``job resume``'s act, and driving is this verb's."""
    source = configured.library.root / "REC001.wav"
    job_id = _queued(source)
    _drive(["master", str(source), "--job", job_id])
    assert _items(job_id)[0].state == jobs.ItemState.FAILED

    code, reported = _drive(["master", str(source), "--job", job_id])
    assert code != int(ExitCode.OK), reported
    assert reported["outcome"] == "failed", reported
    assert _items(job_id)[0].state == jobs.ItemState.FAILED

    # The reopening is refused (R-390): ``source-missing`` is permanent.
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
    def engine(command):
        ran.append("ran")
        raise AssertionError("the engine ran")

    monkeypatch.setattr(mastering, "subprocess_runner", engine)
    job_id = _queued(source)
    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code != int(ExitCode.OK)
    assert ran == [], "the destination check happened after the engine started"
    item = _items(job_id)[0]
    assert item.cause is not None and item.cause.reason == "output-exists"
    assert final.read_bytes() == b"a master somebody kept"


def test_overwrite_reaches_the_handler_and_replaces_the_previous_master(configured, monkeypatch):
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

    # Through the override the resolver reads, not a stand-in resolver.
    monkeypatch.setenv("CRATEKIT_BIN_FFMPEG", str(configured.library.root / "no-ffmpeg"))
    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code != int(ExitCode.OK)
    item = _items(job_id)[0]
    assert item.cause is not None and item.cause.reason == "encoder-missing"


def test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause(
    configured, monkeypatch
):
    """An encoder that reports success and writes nothing."""
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
    """One verb working and nineteen silent is worse than all of them silent."""
    source = configured.library.root / "REC001.wav"
    job_id = _queued(source)

    code, envelope = _drive(["job", "show", job_id])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["progress"]["worker"] == "bound"
    assert envelope["data"]["progress"]["worker_reason"] is None

    moved = sorted(handlers.HANDLERS)[0]
    reason = "no worker in this build, a declaration this test made"
    bound = {k: v for k, v in handlers.HANDLERS.items() if k != moved}
    monkeypatch.setattr(handlers, "HANDLERS", bound)
    unbound = {**handlers.HANDLERS_NOT_YET_BOUND, moved: reason}
    monkeypatch.setattr(handlers, "HANDLERS_NOT_YET_BOUND", unbound)
    with jobs.open_store() as store:
        other = jobs.enqueue(store, handler_key=moved, payload={}, cfg=configured)
    code, envelope = _drive(["job", "show", other.job_id])
    assert envelope["data"]["progress"]["worker"] == "none"
    assert envelope["data"]["progress"]["worker_reason"] == reason


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


def test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there(configured):
    """``source-missing`` promises nothing was read and nothing was written."""
    source = configured.library.root / "Sets" / "nope.wav"
    job_id = _queued(source)

    _drive(["master", str(source), "--job", job_id])

    assert not source.parent.exists(), "a staging tree was built for a missing recording"
    assert _items(job_id)[0].cause.reason == "source-missing"


def test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume(
    configured, tmp_path, monkeypatch
):
    """Drift, driven through the verb's own envelope rather than through the driver."""
    source = _recording(configured.library.root)
    job_id = _queued(source)

    config.save(_config(configured.library.root, tmp_path / "moved-staging"))
    config.reset_cache()

    monkeypatch.setattr(mastering, "subprocess_runner", _encoder())
    code, envelope = _drive(["master", str(source), "--job", job_id])

    assert code == int(ExitCode.OK), envelope
    codes = [warning["code"] for warning in envelope.get("warnings", [])]
    assert "config-drift" in codes, envelope.get("warnings")
    assert _items(job_id)[0].state == jobs.ItemState.DONE


# ── U105: a recording the player split into several files, and a loudness target ──


def _tone(directory: Path, name: str, *, seconds: int, rate: int = 44100) -> Path:
    """A real sine recording: silence measures as negative infinity, which a real encode refuses."""
    require_ffmpeg()
    sine = f"sine=frequency=220:r={rate}"
    return _synthesize(directory / name, sine, seconds, "-c:a", "pcm_s16le")


def _duration(path: Path) -> float:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr[-400:]
    return float(proc.stdout.strip())


#: The stand-in probe's whole layout for a part with no override, so parts differ by field.
PROBED = {"sample_rate": "44100", "sample_fmt": "s16", "channels": "2", "codec_name": "pcm_s16le"}


def _recorder(layouts: dict[str, dict[str, str]] | None = None):
    """The stand-in encoder, recording every command, with a per-part probe."""
    seen: list[mastering.Command] = []
    inner = _encoder()

    def run(command: mastering.Command) -> mastering.CommandResult:
        seen.append(command)
        argv = list(command.argv)
        if argv[0].endswith("ffprobe"):
            fields = {**PROBED, **(layouts or {}).get(Path(argv[-1]).name, {})}
            stdout = "".join(f"{k}={v}\n" for k, v in fields.items())
            return mastering.CommandResult(returncode=0, stdout=stdout)
        return inner(command)

    return run, seen


#: One FLAC block of 4096 samples at 44.1 kHz, the brief's "within a frame".
ONE_FRAME_SECONDS = 4096 / 44100


def test_two_parts_produce_one_master_whose_duration_is_their_sum(tmp_path):
    """The brief's first scenario, over a REAL encode rather than a stand-in."""
    first = _tone(tmp_path, "REC001.wav", seconds=2)
    second = _tone(tmp_path, "REC002.wav", seconds=3)
    digests = [mastering.digest(first), mastering.digest(second)]

    reported = master_cli.run_master(
        master_cli.frozen_payload([str(first), str(second)], None, False)
    )

    output = Path(reported["output"])
    assert output == tmp_path / "REC001_set_mastered.flac"
    joined = _duration(first) + _duration(second)
    assert _duration(output) == pytest.approx(joined, abs=ONE_FRAME_SECONDS)
    # The parts are untouched and each has its own verified archive copy.
    assert [mastering.digest(first), mastering.digest(second)] == digests
    assert reported["parts"] == [str(first), str(second)]
    assert [mastering.digest(Path(a)) for a in reported["archives"]] == digests
    # The joined intermediate is this module's and does not survive the run.
    assert not list(tmp_path.glob(".cratekit-join-*"))
    assert not (tmp_path / "REC001_set.wav").exists()


def test_the_parts_are_joined_in_the_order_given_and_never_sorted(tmp_path):
    """The brief's second scenario, measured at the join itself."""
    later = _recording(tmp_path, "REC002.wav")
    earlier = _recording(tmp_path, "REC001.wav")
    run, _ = _recorder()
    listed: list[str] = []

    def capture(command):
        if "concat" in command.argv:
            listing = Path(command.argv[command.argv.index("-i") + 1])
            listed.extend(listing.read_text().splitlines())
        return run(command)

    reported = _master(later, earlier, runner=capture)

    assert [line.split("/")[-1].rstrip("'") for line in listed] == ["REC002.wav", "REC001.wav"]
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
    one = master_cli.frozen_payload([str(source)], None, False)
    assert one == {"source": str(source), "output_dir": None, "overwrite": False}
    assert one == master_cli.frozen_payload(str(source), None, False)
    assert master_cli.master_argv(_Job(one)) == ["master", str(source), "--job", "job-1"]

    code, envelope = _drive(["master", str(source)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["warnings"] == []


def test_one_input_masters_through_the_unchanged_engine_path(tmp_path):
    """A single recording's report carries no join keys and its own archive."""
    source = _recording(tmp_path)
    run, seen = _recorder()
    payload = master_cli.frozen_payload([str(source)], None, False)
    reported = master_cli.run_master(payload, runner=run)
    assert "parts" not in reported and "archives" not in reported
    assert Path(reported["output"]).name == "REC001_mastered.flac"
    assert not any("concat" in c.argv for c in seen)


def test_the_engine_refuses_an_out_of_range_target_and_takes_the_bounds_inclusively():
    for value in (-4.0, -70.5, float("nan"), float("inf")):
        with pytest.raises(ValueError, match="target_lufs"):
            mastering.Settings(target_lufs=value)
    for value in (-70.0, -5.0, -14.0):
        assert mastering.Settings(target_lufs=value).target_lufs == value


@pytest.mark.parametrize("value", ["-4", "-71", "nan"])
def test_an_out_of_range_target_refuses_and_queues_nothing(configured, value):
    """The brief's fourth scenario, through the verb."""
    recording = str(configured.library.root / "REC001.wav")
    code, envelope = _drive(["master", recording, f"--lufs={value}"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "target-lufs-out-of-range"
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 0


def test_the_target_reaches_every_loudnorm_filter(tmp_path):
    """A frozen target that the engine never sees is a flag that does nothing."""
    source = _recording(tmp_path)
    run, seen = _recorder()
    payload = master_cli.frozen_payload([str(source)], None, False, lufs=-9.0)
    master_cli.run_master(payload, runner=run)
    filters = [c.argv[c.argv.index("-af") + 1] for c in seen if "loudnorm" in " ".join(c.argv)]
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
    rebuilt = master_cli.frozen_payload(
        args.recording, args.output_dir, args.overwrite, lufs=args.lufs
    )
    assert rebuilt == frozen
    assert args.job == "job-1"
    # A negative target parses as two tokens as well.
    args = cli.build_parser([_entry()]).parse_args(["master", "/tmp/a.wav", "--lufs", "-16"])
    assert args.lufs == -16.0 and args.recording == ["/tmp/a.wav"]


def test_parts_at_different_sample_rates_refuse_before_anything_is_written(tmp_path):
    """The brief's hazard. A stream copy would not fail, it would lie."""
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.wav")
    run, seen = _recorder({"REC002.wav": {"sample_rate": "48000"}})

    cause = _refused(first, second, runner=run)

    assert cause.reason == "source-unsupported"
    assert "48000" in cause.message
    assert not (tmp_path / mastering.ARCHIVE_DIRNAME).exists()
    assert not any("concat" in c.argv for c in seen)
    assert set(tmp_path.iterdir()) == {first, second}


@pytest.mark.parametrize("second", ["REC001.wav", "REC002.flac"], ids=["twice", "containers"])
def test_a_part_named_twice_or_in_another_container_refuses_before_any_command(tmp_path, second):
    first = _recording(tmp_path, "REC001.wav")
    other = _recording(tmp_path, second)
    run, seen = _recorder()
    assert _refused(first, other, runner=run).reason == "source-unsupported"
    assert seen == []


def test_a_missing_part_refuses_as_missing(tmp_path):
    first = _recording(tmp_path, "REC001.wav")
    assert _refused(first, tmp_path / "REC002.wav").reason == "source-missing"


def test_a_queued_split_recording_lands_as_one_master_through_the_resume(configured, monkeypatch):
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
    loudnorm = [c for c in seen if "loudnorm" in " ".join(c.argv)]
    assert all("I=-12.0:" in c.argv[c.argv.index("-af") + 1] for c in loudnorm)


def test_an_existing_joined_master_is_refused_on_the_real_destination(configured, monkeypatch):
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
    [{"channels": "1"}, {"codec_name": "pcm_s32le", "sample_fmt": "s32"}, {"sample_fmt": "s32"}],
    ids=["mono-beside-stereo", "codec", "sample-format"],
)
def test_parts_differing_in_any_copied_field_refuse(tmp_path, differs):
    """Rate alone admitted a mono part, and a 24 bit part beside a 32 bit one."""
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.wav")
    run, seen = _recorder({"REC002.wav": differs})

    assert _refused(first, second, runner=run).reason == "source-unsupported"
    assert not (tmp_path / mastering.ARCHIVE_DIRNAME).exists()
    assert not any("concat" in c.argv for c in seen)


def test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone(tmp_path):
    """Both are ``s32`` as a sample format, so the codec is the only field that separates them."""
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.wav")
    same_fmt = {"sample_fmt": "s32"}
    run, _ = _recorder({
        "REC001.wav": {**same_fmt, "codec_name": "pcm_s24le"},
        "REC002.wav": {**same_fmt, "codec_name": "pcm_s32le"},
    })
    assert "pcm_s32le" in _refused(first, second, runner=run).message


def test_a_joined_wav_is_written_as_rf64_when_it_needs_to_be(tmp_path):
    """Found by this unit's review."""
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.wav")
    run, seen = _recorder()
    _master(first, second, runner=run)
    join = next(c for c in seen if "concat" in c.argv)
    assert join.argv[join.argv.index("-rf64") + 1] == "auto"
    drift = next(c for c in seen if "pcm_s24le" in c.argv)
    assert drift.argv[drift.argv.index("-rf64") + 1] == "auto"

    # A joined FLAC, in a folder of its own, carries no WAV muxer option.
    (tmp_path / "flac").mkdir()
    first, second = tmp_path / "flac" / "REC001.flac", tmp_path / "flac" / "REC002.flac"
    first.write_bytes(b"one")
    second.write_bytes(b"two")
    run, seen = _recorder()
    _master(first, second, runner=run)
    join = next(c for c in seen if "concat" in c.argv)
    assert "-rf64" not in join.argv


def test_the_engine_refuses_an_existing_joined_master_before_archiving(tmp_path):
    """The engine's own check, not the handler's pre-check."""
    first = _recording(tmp_path, "REC001.wav")
    second = _recording(tmp_path, "REC002.wav")
    (tmp_path / "REC001_set_mastered.flac").write_bytes(b"kept")
    run, seen = _recorder()

    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.master_parts([first, second], runner=run)

    assert excinfo.value.refusal is mastering.Refusal.OUTPUT_EXISTS
    assert not (tmp_path / mastering.ARCHIVE_DIRNAME).exists()
    assert seen == []
