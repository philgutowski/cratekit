"""U104: a mix URL is fetched through a seam, identified, and removed (R-303).

No test here runs ``yt-dlp``. The conftest replaces ``fetch.fetcher`` with one
that fails the test, every test below that wants a download injects a fake, and
the shipped fetcher is only ever built over a fake ``run``.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.acquire import fallback
from cratekit.core import binaries, config, jobs
from cratekit.core.cause import Outcome
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import acrcloud, fetch
from cratekit.intake import cli as intake_cli
from tests.cli_drive import drive
from tests.intake import test_workers as workers
from tests.intake.test_recognition import FakeCarver, miss
from tests.intake.test_workers import items_of, job_of, recording, resume_argv, three_tracks

# The three fixtures the worker tests already build a configured, recognition
# ready machine with. Bound by assignment so the names are this module's own.
cfg = workers.cfg
library = workers.library
recognised = workers.recognised

URL = "https://soundcloud.example/somebody/friday-night-mix"


class FakeFetcher:
    """Lands a few bytes where it is told to and remembers what it was asked."""

    def __init__(
        self,
        *,
        fail: str | None = None,
        land_at: Path | None = None,
        failure: type[Exception] = fetch.SetFetchFailed,
    ) -> None:
        self.fail = fail
        self.failure = failure
        self.land_at = land_at
        self.asked: list[tuple[str, Path]] = []
        self.seen_inside: list[str] = []

    def fetch(self, url: str, directory: Path) -> Path:
        self.asked.append((url, directory))
        self.seen_inside = sorted(one.name for one in directory.iterdir())
        if self.fail is not None:
            # A download that died part way leaves its partial behind.
            (directory / "fetched.mp3.part").write_bytes(b"half")
            raise self.failure(self.fail)
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
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    # NOT CALLED RETRYABLE. A dead address and a dead network both end the
    # download non zero, and nobody watches a session, so a driver that
    # trusted the flag would re-run a 404 for ever.
    assert cause["reason"] == "intake-list-unusable"
    assert cause["retryable"] is False
    assert "HTTP Error 404" in cause["message"]
    assert URL in cause["message"]
    assert "intake playlist" in " ".join(cause["remediation"]["steps"])
    assert recognised.requests == []
    # The partial the fake left is gone with its folder.
    assert len(fake.asked) == 1
    assert nothing_left()
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_download_that_timed_out_is_the_one_fetch_failure_called_retryable(
    cfg, library, recognised, monkeypatch
):
    three_tracks(recognised)
    fake = FakeFetcher(
        fail="the download did not finish within 3600 seconds", failure=fetch.SetFetchTimedOut
    )
    monkeypatch.setattr(fetch, "fetcher", lambda: fake)
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "unavailable-transient"
    assert cause["retryable"] is True
    assert cause["remediation"]["remedy"] == "retry-later"
    assert nothing_left()


def test_a_playlist_address_is_refused_as_more_than_one_recording(
    cfg, library, recognised, monkeypatch
):
    three_tracks(recognised)
    fake = FakeFetcher(
        fail="the address is a playlist of more than one recording",
        failure=fetch.SeveralRecordings,
    )
    monkeypatch.setattr(fetch, "fetcher", lambda: fake)
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "intake-list-unusable"
    assert cause["retryable"] is False
    assert "more than one recording" in cause["message"]
    assert "one recording on that page" in " ".join(cause["remediation"]["steps"])
    assert recognised.requests == []
    assert nothing_left()


def test_a_scratch_folder_that_cannot_be_made_is_a_fact_about_this_machine(
    cfg, library, recognised, fetcher
):
    three_tracks(recognised)
    # A FILE where the scratch root would go, so the folder cannot be made.
    root = scratch_root()
    root.parent.mkdir(parents=True, exist_ok=True)
    root.write_bytes(b"")
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "intake-list-unusable"
    assert cause["retryable"] is False
    assert "could not be prepared" in cause["message"]
    assert config.ENV_STATE_DIR in " ".join(cause["remediation"]["steps"])
    assert fetcher.asked == []
    assert recognised.requests == []


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


def test_the_library_guard_asks_the_filesystem_and_not_only_the_strings(tmp_path, monkeypatch):
    """Two spellings of one folder that ``resolve`` does not settle.

    Found on a case insensitive volume, where ``resolve`` leaves the letter
    case as typed, so a lower case spelling of a mixed case library is not
    textually inside it. Built here so it holds on any volume: where the other
    spelling is not already the same folder it is made one, and ``resolve`` is
    held still so only the ``samefile`` layer can answer.
    """
    root = tmp_path / "Library"
    (root / "Music" / "state").mkdir(parents=True)
    other = tmp_path / "library"
    if not other.exists():
        other.symlink_to(root, target_is_directory=True)
    monkeypatch.setattr(Path, "resolve", lambda self, strict=False: self)
    scratch = other / "Music" / "state" / "mix_scratch" / "abc"
    assert root not in scratch.parents
    with pytest.raises(fetch.ScratchUnderLibrary):
        fetch.assert_outside_library(scratch, root)
    with pytest.raises(fetch.ScratchUnderLibrary):
        fetch.assert_outside_library(other, root)
    fetch.assert_outside_library(tmp_path / "elsewhere" / "abc", root)


def test_a_library_that_is_not_there_has_nothing_to_be_inside(tmp_path):
    fetch.assert_outside_library(tmp_path / "state" / "x", tmp_path / "absent-library")


def test_a_library_that_is_not_there_is_still_refused_by_name(tmp_path):
    """An unplugged drive is the ordinary way a library root is absent, and the
    filesystem layer has nothing to ask then, so the strings alone refuse."""
    absent = tmp_path / "absent-library"
    with pytest.raises(fetch.ScratchUnderLibrary):
        fetch.assert_outside_library(absent / "state" / "mix_scratch" / "abc", absent)


def test_a_fetcher_that_answers_with_a_file_that_is_not_there_is_a_failed_fetch(
    cfg, library, recognised, monkeypatch
):
    three_tracks(recognised)

    class Ghost:
        def fetch(self, url, directory):
            return directory / "fetched.mp3"

    monkeypatch.setattr(fetch, "fetcher", lambda: Ghost())
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert "not a file inside" in envelope["cause"]["message"]
    assert recognised.requests == []
    assert nothing_left()


def test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch(
    cfg, library, recognised, monkeypatch
):
    three_tracks(recognised)
    stray = library / "Music" / "stray.mp3"
    fake = FakeFetcher(land_at=stray)
    monkeypatch.setattr(fetch, "fetcher", lambda: fake)
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert envelope["cause"]["retryable"] is False
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


def test_a_refusal_from_inside_the_identifier_names_the_address_and_not_the_scratch_file(
    cfg, library, recognised, fetcher, monkeypatch
):
    """The identifier names what it was handed, and that file is gone."""

    class Unmeasurable(FakeCarver):
        def duration(self, source):
            raise OSError("ffprobe could not read it")

    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: Unmeasurable(85.0))
    code, envelope = drive(["intake", "set", URL])
    assert code != int(ExitCode.OK), envelope
    cause = envelope["cause"]
    assert "could not be measured" in cause["message"]
    assert URL in cause["message"]
    assert "fetched.mp3" not in cause["message"]
    assert cause["detail"]["source"] == URL
    assert str(scratch_root()) not in str(cause["detail"])
    assert nothing_left()


def test_the_same_refusal_over_a_local_recording_still_names_the_file(
    cfg, library, recognised, monkeypatch
):
    class Unmeasurable(FakeCarver):
        def duration(self, source):
            raise OSError("ffprobe could not read it")

    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: Unmeasurable(85.0))
    path = recording(library)
    code, envelope = drive(["intake", "set", str(path)])
    cause = envelope["cause"]
    assert "set.mp3 could not be measured" in cause["message"]
    assert cause["detail"]["source"] == str(path)


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


def test_a_fetched_mix_with_no_digest_is_named_by_its_address_and_not_its_scratch_file(tmp_path):
    """Every fetched mix lands on a file of one name pattern, so a token taken
    from the scratch path would say nothing about which mix it was."""
    path = tmp_path / "fetched-00001.mp3"
    one = intake_cli.SetRecording(path=path, ref=URL, stem="mix", shown=URL)
    other = intake_cli.SetRecording(path=path, ref=URL + "-two", stem="mix", shown=URL)
    assert intake_cli.tracklist_name(one, "") != intake_cli.tracklist_name(other, "")
    assert intake_cli.tracklist_name(one, "ab" * 32) == intake_cli.tracklist_name(other, "ab" * 32)


@pytest.mark.parametrize(
    ("url", "stem"),
    [
        (URL, "friday-night-mix"),
        ("https://example.invalid/a/b/?x=1", "b"),
        ("https://example.invalid/", fetch.DEFAULT_STEM),
        ("https://example.invalid/../../%2e%2e/etc passwd", "etc-passwd"),
        ("https://example.invalid/mix/..", fetch.DEFAULT_STEM),
        ("https://example.invalid/...", fetch.DEFAULT_STEM),
        ("https://example.invalid/" + "%E3%81%82" * 60, ("E3-81-82-" * 9)[:80].strip("-.")),
    ],
)
def test_a_tracklist_stem_is_the_last_segment_reduced_to_a_safe_name(url, stem):
    got = fetch.stem_of(url)
    assert got == stem
    assert "/" not in got and not got.startswith(".")
    assert len(got) <= fetch.STEM_MAX_CHARS


# ---------------------------------------------------------------------------
# The shipped fetcher, over a fake run
# ---------------------------------------------------------------------------


def test_the_shipped_fetcher_runs_u80s_download_under_a_mix_sized_bound(tmp_path):
    calls: list[tuple[list[str], dict]] = []

    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        (tmp_path / "fetched-00001.mp3").write_bytes(b"ID3")
        return SimpleNamespace(returncode=0, stderr="")

    landed = fetch.YtDlpSetFetcher("/opt/bin/yt-dlp", run=run).fetch(URL, tmp_path)
    assert landed == tmp_path / "fetched-00001.mp3"
    argv, kwargs = calls[0]
    assert argv[0] == "/opt/bin/yt-dlp"
    # Each entry of a playlist address is its OWN file, and at most two are
    # asked for, so a set page can never come back as one file.
    assert argv[argv.index("--output") + 1] == str(tmp_path / "fetched-%(autonumber)s.%(ext)s")
    assert argv[argv.index("--playlist-end") + 1] == "2"
    assert argv.index("--playlist-end") < argv.index("--")
    # U121. The page is kept beside the recording, so a set's playlist can be
    # named from it, and the flag sits with the other edit ahead of the address.
    assert "--write-info-json" in argv
    assert argv.index("--write-info-json") < argv.index("--")
    # Everything else is U80's argv, unchanged.
    rest = [one for one in argv if one not in ("--playlist-end", "2", "--write-info-json")]
    theirs = fallback.YtDlpFetcher("/opt/bin/yt-dlp").argv(URL, tmp_path)
    assert [a for a, b in zip(rest, theirs, strict=True) if a != b] == [
        str(tmp_path / "fetched-%(autonumber)s.%(ext)s")
    ]
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


def test_the_shipped_fetcher_says_a_timeout_as_the_one_retryable_kind(tmp_path):
    def run(argv, **kwargs):
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])

    with pytest.raises(fetch.SetFetchTimedOut, match="did not finish within 5 seconds"):
        fetch.YtDlpSetFetcher("/opt/bin/yt-dlp", run=run, timeout=5).fetch(URL, tmp_path)


def test_the_shipped_fetcher_refuses_a_playlist_that_landed_two_recordings(tmp_path):
    def run(argv, **kwargs):
        (tmp_path / "fetched-00001.mp3").write_bytes(b"ID3")
        (tmp_path / "fetched-00002.mp3").write_bytes(b"ID3")
        return SimpleNamespace(returncode=0, stderr="")

    with pytest.raises(fetch.SeveralRecordings, match="fetched-00001.mp3, fetched-00002.mp3"):
        fetch.YtDlpSetFetcher("/opt/bin/yt-dlp", run=run).fetch(URL, tmp_path)


def test_an_ordinary_failed_download_is_neither_a_timeout_nor_a_playlist(tmp_path):
    run = lambda argv, **k: SimpleNamespace(returncode=1, stderr="ERROR: 404\n")  # noqa: E731
    with pytest.raises(fetch.SetFetchFailed) as caught:
        fetch.YtDlpSetFetcher("/opt/bin/yt-dlp", run=run).fetch(URL, tmp_path)
    assert type(caught.value) is fetch.SetFetchFailed


def test_the_suite_cannot_reach_the_shipped_fetcher():
    with pytest.raises(AssertionError, match="shipped mix fetcher"):
        fetch.fetcher()


# ---------------------------------------------------------------------------
# U121: the page the mix came from rides on the job
# ---------------------------------------------------------------------------


class PageWritingFetcher(FakeFetcher):
    """Lands the recording and the info document ``yt-dlp`` writes beside it."""

    def __init__(self, page: dict) -> None:
        super().__init__()
        self.page = page

    def fetch(self, url: str, directory: Path) -> Path:
        landed = super().fetch(url, directory)
        (directory / f"{landed.stem}{fetch.INFO_SUFFIX}").write_text(
            json.dumps(self.page), encoding="utf-8"
        )
        return landed


def test_the_page_a_mix_came_from_is_frozen_on_the_set_job(cfg, library, recognised, monkeypatch):
    """U121. The uploader, the title and the upload day name the set's permanent
    playlist later, so the job carries them; nothing else of the document does."""
    three_tracks(recognised)
    page = {
        "title": "Probe - Friday Night Mix",
        "uploader": "Probe",
        "upload_date": "20260503",
        "description": "not kept",
        "duration": 5400,
    }
    monkeypatch.setattr(fetch, "fetcher", lambda: PageWritingFetcher(page))
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.OK), envelope
    assert job_of(envelope["data"]["job_id"]).payload[intake_cli.PAGE] == {
        "title": "Probe - Friday Night Mix",
        "uploader": "Probe",
        "upload_date": "20260503",
    }
    assert nothing_left()


def test_a_fetch_that_left_no_info_document_freezes_an_empty_page(
    cfg, library, recognised, fetcher
):
    three_tracks(recognised)
    code, envelope = drive(["intake", "set", URL])
    assert code == int(ExitCode.OK), envelope
    assert job_of(envelope["data"]["job_id"]).payload[intake_cli.PAGE] == {}


def test_a_local_recording_freezes_an_empty_page(cfg, library, recognised):
    three_tracks(recognised)
    path = recording(library)
    code, envelope = drive(["intake", "set", str(path)])
    assert code == int(ExitCode.OK), envelope
    assert job_of(envelope["data"]["job_id"]).payload[intake_cli.PAGE] == {}


def test_page_of_reads_the_three_words_and_nothing_a_document_cannot_say(tmp_path):
    assert fetch.page_of(tmp_path / "absent") == {}
    assert fetch.page_of(tmp_path) == {}
    (tmp_path / "fetched.info.json").write_text("not json", encoding="utf-8")
    assert fetch.page_of(tmp_path) == {}
    (tmp_path / "fetched.info.json").write_text(
        json.dumps({"title": "  A Set ", "uploader": 7, "upload_date": "", "other": "x"}),
        encoding="utf-8",
    )
    assert fetch.page_of(tmp_path) == {"title": "A Set"}
    (tmp_path / "fetched.mp3").write_bytes(b"ID3")
    assert fetch.page_of(tmp_path) == {"title": "A Set"}
