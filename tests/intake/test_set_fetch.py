"""U104: a mix URL is fetched through a seam, identified, and removed (R-303).

No test here runs ``yt-dlp``. The conftest replaces ``fetch.fetcher`` with one
that fails the test, every test below that wants a download injects a fake, and
the shipped fetcher is only ever built over a fake ``run``.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.acquire import fallback
from cratekit.core import binaries, config, jobs
from cratekit.core.cause import Outcome
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import fetch
from tests.cli_drive import drive
from tests.intake import test_workers as workers
from tests.intake.test_recognition import miss
from tests.intake.test_workers import items_of, job_of, recording, resume_argv, three_tracks

# The three fixtures the worker tests already build a configured, recognition
# ready machine with. Bound by assignment so the names are this module's own.
cfg = workers.cfg
library = workers.library
recognised = workers.recognised

URL = "https://soundcloud.example/somebody/friday-night-mix"


class FakeFetcher:
    """Lands a few bytes where it is told to and remembers what it was asked."""

    def __init__(self, *, fail: str | None = None, land_at: Path | None = None) -> None:
        self.fail = fail
        self.land_at = land_at
        self.asked: list[tuple[str, Path]] = []
        self.seen_inside: list[str] = []

    def fetch(self, url: str, directory: Path) -> Path:
        self.asked.append((url, directory))
        self.seen_inside = sorted(one.name for one in directory.iterdir())
        if self.fail is not None:
            # A download that died part way leaves its partial behind.
            (directory / "fetched.mp3.part").write_bytes(b"half")
            raise fetch.SetFetchFailed(self.fail)
        landed = self.land_at if self.land_at is not None else directory / "fetched.mp3"
        landed.write_bytes(b"ID3 a fetched mix")
        return landed


@pytest.fixture
def fetcher(monkeypatch) -> FakeFetcher:
    fake = FakeFetcher()
    monkeypatch.setattr(fetch, "fetcher", lambda: fake)
    return fake


def scratch_root() -> Path:
    return config.state_path(fetch.SCRATCH_KEY)


def nothing_left() -> bool:
    root = scratch_root()
    return not root.exists() or not any(root.iterdir())


# ---------------------------------------------------------------------------
# The brief's four scenarios
# ---------------------------------------------------------------------------


def test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file(
    cfg, library, recognised, fetcher
):
    three_tracks(recognised)
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.OK), envelope
    job_id = envelope["data"]["job_id"]
    assert len(items_of(job_id)) == 3
    assert envelope["data"]["progress"]["calls"] == 3
    assert envelope["warnings"] == []
    assert [url for url, _ in fetcher.asked] == [URL]
    # What was identified is what was fetched: every chunk was carved from it.
    assert len(recognised.requests) == 3
    # The job freezes the ADDRESS, because the file is gone, and the resume
    # argv is rebuilt from it.
    assert job_of(job_id).payload[intake_cli.SOURCE] == URL
    assert resume_argv(job_id) == ["intake", "set", URL, "--job", job_id]
    assert nothing_left()


def test_a_missing_yt_dlp_refuses_a_url_with_the_install_hint(
    cfg, library, recognised, monkeypatch
):
    three_tracks(recognised)

    def absent():
        raise binaries.BinaryNotFound(
            "yt-dlp was not found (checked PATH).",
            binary="yt-dlp",
            remedy=binaries.Remedy.INSTALL_BINARY,
            hint=binaries.InstallHint(binaries.PackageManager.HOMEBREW, ("yt-dlp",)),
        )

    monkeypatch.setattr(fetch, "fetcher", absent)
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "yt-dlp-missing"
    assert cause["remediation"]["remedy"] == "install-binary"
    assert "install yt-dlp with homebrew" in " ".join(cause["remediation"]["steps"])
    assert "Fetching a mix runs it" in cause["message"]
    assert cause["detail"]["source"] == URL
    assert recognised.requests == []
    assert nothing_left()


def test_a_fetch_failure_refuses_and_leaves_no_scratch_file(
    cfg, library, recognised, monkeypatch
):
    three_tracks(recognised)
    fake = FakeFetcher(fail="the download failed with exit status 1 (HTTP Error 404)")
    monkeypatch.setattr(fetch, "fetcher", lambda: fake)
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "unavailable-transient"
    assert cause["retryable"] is True
    assert "HTTP Error 404" in cause["message"]
    assert URL in cause["message"]
    assert recognised.requests == []
    # The partial the fake left is gone with its folder.
    assert len(fake.asked) == 1
    assert nothing_left()
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_local_path_never_consults_the_fetch_seam(cfg, library, recognised):
    """The conftest's refusing fetcher is in force, so reaching the seam fails."""
    three_tracks(recognised)
    path = recording(library)
    code, envelope = drive(["intake", "set", str(path)])
    assert code == int(ExitCode.OK), envelope
    job_id = envelope["data"]["job_id"]
    assert job_of(job_id).payload[intake_cli.SOURCE] == str(path)
    assert path.is_file()
    assert not scratch_root().exists()


def test_a_path_that_names_nothing_is_still_refused_before_the_gate(cfg, library, recognised):
    code, envelope = drive(["intake", "set", str(library / "absent.mp3")])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "is not a file on this machine" in envelope["cause"]["message"]


# ---------------------------------------------------------------------------
# Order, and the hazard
# ---------------------------------------------------------------------------


def test_the_gate_refuses_before_anything_is_fetched(cfg, library, fetcher):
    """No recognition keys. A download is minutes and the gate is free."""
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-recognition-unready"
    assert fetcher.asked == []
    assert not scratch_root().exists()


def test_a_scratch_root_inside_the_library_refuses_before_anything_is_fetched(
    cfg, library, recognised, fetcher, monkeypatch
):
    three_tracks(recognised)
    inside = library / "Music" / "state"
    inside.mkdir(parents=True)
    monkeypatch.setattr(fetch, "scratch_for", lambda url: inside / "mix_scratch" / "abc")
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "intake-list-unusable"
    assert "never written under the library" in cause["message"]
    assert config.ENV_STATE_DIR in " ".join(cause["remediation"]["steps"])
    assert fetcher.asked == []
    assert recognised.requests == []
    assert not (inside / "mix_scratch").exists()


@pytest.mark.parametrize("where", ["the-root-itself", "deep-inside"])
def test_the_library_guard_reads_resolved_paths(tmp_path, where):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    link = tmp_path / "elsewhere"
    link.symlink_to(root, target_is_directory=True)
    scratch = link if where == "the-root-itself" else link / "Music" / "a" / "b"
    with pytest.raises(fetch.ScratchUnderLibrary):
        fetch.assert_outside_library(scratch, root)
    # A sibling whose name only STARTS with the library's is outside it.
    fetch.assert_outside_library(tmp_path / "library-state" / "x", root)


def test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch(
    cfg, library, recognised, monkeypatch
):
    three_tracks(recognised)
    stray = library / "Music" / "stray.mp3"
    fake = FakeFetcher(land_at=stray)
    monkeypatch.setattr(fetch, "fetcher", lambda: fake)
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "unavailable-transient"
    assert "not a file inside" in envelope["cause"]["message"]
    assert recognised.requests == []
    assert nothing_left()


def test_the_scratch_folder_is_cleared_before_every_attempt(cfg, library, recognised, fetcher):
    three_tracks(recognised)
    stale = fetch.scratch_for(URL)
    stale.mkdir(parents=True)
    (stale / "fetched.mp3").write_bytes(b"what a killed process left")
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.OK), envelope
    assert fetcher.seen_inside == []


def test_identification_that_raises_still_removes_the_fetched_mix(
    cfg, library, recognised, fetcher
):
    recognised.answers[:] = [ConnectionError("down"), ConnectionError("down"), miss()]
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "intake-recognition-failed"
    # Named for the address, not for the file it was fetched into.
    assert URL in cause["message"]
    assert "fetched.mp3" not in cause["message"]
    assert cause["detail"]["source"] == URL
    assert len(fetcher.asked) == 1
    assert nothing_left()


def test_a_mix_nobody_recognised_is_an_honest_zero_that_names_the_address(
    cfg, library, recognised, fetcher
):
    recognised.answers[:] = [miss(), miss(), miss()]
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == str(Outcome.NO_OP)
    assert envelope["data"]["state"] == "nothing-identified"
    assert envelope["data"]["progress"]["source"] == URL
    assert envelope["data"]["progress"]["calls"] == 3
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()
    assert nothing_left()


def test_a_resume_of_a_url_job_fetches_nothing(cfg, library, recognised, fetcher):
    three_tracks(recognised)
    code, envelope = drive(["intake", "set", URL])
    job_id = envelope["data"]["job_id"]
    assert len(fetcher.asked) == 1
    code, envelope = drive(resume_argv(job_id))
    assert len(fetcher.asked) == 1
    assert nothing_left()


def test_a_scratch_folder_that_cannot_be_removed_is_said_on_the_envelope(
    cfg, library, recognised, fetcher, monkeypatch
):
    three_tracks(recognised)
    monkeypatch.setattr(fetch.shutil, "rmtree", lambda *a, **k: None)
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.OK), envelope
    note = next(w for w in envelope["warnings"] if w["code"] == intake_cli.MIX_SCRATCH_LEFT)
    assert str(fetch.scratch_for(URL)) in note["message"]


def test_the_scratch_entry_is_declared_under_the_installation_root():
    entry = config.state_file(fetch.SCRATCH_KEY)
    assert entry.root is config.StateRoot.INSTALLATION
    assert entry.snapshot is config.SnapshotRole.NEVER_RESTORED
    assert entry.medium is config.Medium.DIRECTORY
    assert fetch.scratch_for(URL).parent == config.installation_state_dir() / "mix_scratch"
    # One folder per address, and a stray space is not a second address.
    assert fetch.scratch_for(URL) == fetch.scratch_for(f"  {URL} ")
    assert fetch.scratch_for(URL) != fetch.scratch_for(URL + "-two")


# ---------------------------------------------------------------------------
# intake identify takes the address the same way
# ---------------------------------------------------------------------------


def test_identify_over_a_url_writes_a_tracklist_named_for_the_address(
    cfg, library, recognised, fetcher, tmp_path
):
    three_tracks(recognised)
    out = tmp_path / "lists"
    code, envelope = drive(["intake", "identify", URL, "--out", str(out)])
    assert code == int(ExitCode.OK), envelope
    written = sorted(out.iterdir())
    assert len(written) == 1
    assert written[0].name.startswith("friday-night-mix-")
    assert written[0].name.endswith(intake_cli.TRACKLIST_SUFFIX)
    assert "Aurora Bloom - Sun Path" in written[0].read_text()
    assert len(envelope["data"]["missing"]) == 3
    assert nothing_left()


def test_identify_over_a_url_refuses_an_absent_library_before_anything_is_fetched(
    cfg, library, recognised, fetcher
):
    three_tracks(recognised)
    (library / "Music").rmdir()
    code, envelope = drive(["intake", "identify", URL])
    assert envelope["cause"]["reason"] == "library-volume-unmounted"
    assert envelope["cause"]["detail"]["source"] == URL
    assert fetcher.asked == []


@pytest.mark.parametrize(
    ("url", "stem"),
    [
        (URL, "friday-night-mix"),
        ("https://example.invalid/a/b/?x=1", "b"),
        ("https://example.invalid/", fetch.DEFAULT_STEM),
        ("https://example.invalid/../../%2e%2e/etc passwd", "etc-passwd"),
        ("https://example.invalid/mix/..", fetch.DEFAULT_STEM),
        ("https://example.invalid/...", fetch.DEFAULT_STEM),
    ],
)
def test_a_tracklist_stem_is_the_last_segment_reduced_to_a_safe_name(url, stem):
    got = fetch.stem_of(url)
    assert got == stem
    assert "/" not in got and not got.startswith(".")


# ---------------------------------------------------------------------------
# The shipped fetcher, over a fake run
# ---------------------------------------------------------------------------


def test_the_shipped_fetcher_runs_u80s_download_under_a_mix_sized_bound(tmp_path):
    calls: list[tuple[list[str], dict]] = []

    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        (tmp_path / f"{fallback.FETCH_STEM}{fallback.FETCH_SUFFIX}").write_bytes(b"ID3")
        return SimpleNamespace(returncode=0, stderr="")

    landed = fetch.YtDlpSetFetcher("/opt/bin/yt-dlp", run=run).fetch(URL, tmp_path)
    assert landed == tmp_path / "fetched.mp3"
    argv, kwargs = calls[0]
    assert argv[0] == "/opt/bin/yt-dlp"
    # The address can never be read as an option.
    assert argv[-2:] == ["--", URL]
    assert "--no-playlist" in argv
    assert kwargs["timeout"] == fetch.SET_FETCH_TIMEOUT_SECONDS == 3600
    assert fetch.SET_FETCH_TIMEOUT_SECONDS > fallback.FETCH_TIMEOUT_SECONDS


@pytest.mark.parametrize(
    ("run", "said"),
    [
        (lambda argv, **k: SimpleNamespace(returncode=1, stderr="ERROR: 404\n"), "exit status 1"),
        (lambda argv, **k: SimpleNamespace(returncode=0, stderr=""), "left 0 .mp3 file(s)"),
    ],
)
def test_the_shipped_fetcher_says_every_failure_in_this_seams_own_exception(tmp_path, run, said):
    with pytest.raises(fetch.SetFetchFailed, match=said.replace("(", r"\(").replace(")", r"\)")):
        fetch.YtDlpSetFetcher("/opt/bin/yt-dlp", run=run).fetch(URL, tmp_path)


def test_the_shipped_fetcher_says_a_timeout_in_this_seams_own_exception(tmp_path):
    def run(argv, **kwargs):
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])

    with pytest.raises(fetch.SetFetchFailed, match="did not finish within 5 seconds"):
        fetch.YtDlpSetFetcher("/opt/bin/yt-dlp", run=run, timeout=5).fetch(URL, tmp_path)


def test_the_suite_cannot_reach_the_shipped_fetcher():
    with pytest.raises(AssertionError, match="shipped mix fetcher"):
        fetch.fetcher()
