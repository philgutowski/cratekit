"""U81: an accepted second source candidate downloads into staging, marked lossy.

``crate acquire fallback-fetch PATH`` resolves the list exactly as ``acquire
fallback`` does, queues one job item per row whose candidate a person accepted
in review, and the worker downloads that upload into the download staging
directory, marked lossy and tagged from the ROW. A strict lossless policy
refuses each such item before anything downloads.

EVERYTHING BUT THE FETCHER IS REAL. The list reader, the library index, the
review store, the job queue and its driver, the resume argv and the tag writer
all run as shipped. The fetcher is a fake substituted where the worker looks it
up, and the shipped ``yt-dlp`` fetcher is driven through a fake runner. NO TEST
RUNS ``yt-dlp`` AND NO TEST DOWNLOADS ANYTHING.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import dataclasses
import subprocess
from pathlib import Path

import pytest

from cratekit.acquire import fallback, fallback_cli, match
from cratekit.cli import handlers, registry
from cratekit.cli import jobs as cli_jobs
from cratekit.core import binaries, config, jobs, review, tags
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import candidates
from cratekit.intake import cli as intake_cli
from tests.acquire_fakes import mp3_bytes
from tests.cli_drive import drive
from tests.test_config import valid_data

BOOT = "Aurora Bloom - Sun Path (Night Bootleg)"
BOOT_ARTIST, BOOT_TITLE = "Aurora Bloom", "Sun Path (Night Bootleg)"
TIDE = "Nova Reef - Tide"
UPLOAD = "https://soundcloud.example/2"
OTHER_UPLOAD = "https://youtube.example/4"
MARKER = "[LOSSY]"

# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


def _configure(library: Path, policy: str, marker: str | None = MARKER) -> config.Config:
    built = config.from_dict(
        valid_data(
            library,
            profile={"name": "full"},
            acquisition={"lossless_policy": policy},
            naming={"lossy_marker": marker},
        )
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def permissive(library) -> config.Config:
    return _configure(library, "allow_lossy_marked")


@pytest.fixture
def strict(library) -> config.Config:
    return _configure(library, "strict")


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    yield
    intake_cli.reset_cache()


@pytest.fixture(autouse=True)
def no_real_subprocess(monkeypatch):
    """A test that forgets to bind a fake fails loudly instead of running yt-dlp."""

    def refuse(*_a, **_k):
        raise AssertionError("the real subprocess runner was reached")

    monkeypatch.setattr(subprocess, "run", refuse)


class FakeFetcher:
    """Lands an MP3 already tagged with the UPLOAD's page title, records every call.

    The page tags are the point: a worker that kept what the upload carried
    would commit a file named and tagged for somebody's upload, not the row.
    """

    def __init__(self, *, fail: Exception | None = None, before=None, payload: bytes | None = None):
        self.calls: list[tuple[str, Path]] = []
        self.fail = fail
        self.before = before
        self.payload = mp3_bytes() if payload is None else payload

    def fetch(self, url: str, directory: Path) -> Path:
        self.calls.append((url, directory))
        if self.before is not None:
            self.before()
        if self.fail is not None:
            raise self.fail
        landed = directory / f"{fallback.FETCH_STEM}.mp3"
        landed.write_bytes(self.payload)
        tags.write_tags(landed, {"artist": "some uploader", "title": "UPLOAD PAGE TITLE"})
        return landed


def bind(monkeypatch, fake: FakeFetcher) -> FakeFetcher:
    monkeypatch.setattr(fallback_cli, "fetcher", lambda: fake)
    return fake


def tracklist(tmp_path: Path, *lines: str) -> Path:
    path = tmp_path / "unlisted.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def offered(cfg, line: str, *urls: str, handler_key: str = "acquire.fallback") -> str:
    """Offer second source candidates for one row, as ``acquire fallback`` does."""
    wanted = match.read_text_lines(line)[0]
    answer = fallback.Answer(
        hits=tuple(
            fallback.Hit(fallback.SOUNDCLOUD, url, "UPLOAD PAGE TITLE", "some uploader", 300)
            for url in urls
        )
    )
    with review.open_store(cfg) as items:
        made = fallback.propose(items, wanted, answer, handler_key=handler_key)
    return str(made.item_id)


def answered(cfg, item_id: str, verdict: review.Verdict, option: str | None = None) -> None:
    with review.open_store(cfg) as items:
        review.resolve(items, item_id, verdict, option=option, actor="suite")


def accepted(cfg, line: str = BOOT, url: str = UPLOAD) -> str:
    item_id = offered(cfg, line, url, OTHER_UPLOAD)
    answered(cfg, item_id, review.Verdict.ACCEPTED, option=url)
    return item_id


def queue(path: Path) -> tuple[int, dict]:
    return drive(["acquire", "fallback-fetch", str(path)])


def queued(path: Path) -> str:
    code, envelope = queue(path)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok", envelope
    return envelope["data"]["job_id"]


def run(job_id: str) -> tuple[int, dict]:
    with jobs.open_store() as store:
        return drive(cli_jobs.argv_for(jobs.get(store, job_id)))


def items_of(job_id: str) -> tuple[jobs.Item, ...]:
    with jobs.open_store() as store:
        return jobs.items(store, job_id)


def job_of(job_id: str) -> jobs.Job:
    with jobs.open_store() as store:
        return jobs.get(store, job_id)


def only_item(job_id: str) -> jobs.Item:
    [item] = items_of(job_id)
    return item


def staging(cfg) -> Path:
    return Path(cfg.paths.download_staging)


def marked_final(cfg) -> Path:
    return staging(cfg) / f"{BOOT_ARTIST} - {BOOT_TITLE} {MARKER}.mp3"


# ═══════════════════════════════════════════════════════════════════════════
# The binding
# ═══════════════════════════════════════════════════════════════════════════


def test_the_fetch_key_resolves_to_this_worker():
    assert handlers.resolve("acquire.fallback-fetch") is fallback_cli.handle_fetch
    assert "acquire.fallback-fetch" not in handlers.HANDLERS_NOT_YET_BOUND
    entry = registry.entry("acquire.fallback-fetch")
    assert entry.long_running and entry.argv_builder == "fetch_argv"


# ═══════════════════════════════════════════════════════════════════════════
# The brief's four scenarios
# ═══════════════════════════════════════════════════════════════════════════


def test_a_lossy_file_lands_marked(permissive, tmp_path, monkeypatch):
    """R21: a second source file is lossy, so it is committed only WITH the marker."""
    accepted(permissive)
    fake = bind(monkeypatch, FakeFetcher())
    job_id = queued(tracklist(tmp_path, BOOT))

    code, envelope = run(job_id)

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "succeeded"
    item = only_item(job_id)
    assert item.state is jobs.ItemState.DONE
    assert item.artifact == str(marked_final(permissive))
    assert marked_final(permissive).is_file()
    assert [url for url, _ in fake.calls] == [UPLOAD]
    # Downloaded into the item's own directory, and moved, not copied.
    [(_, directory)] = fake.calls
    assert directory.parent.parent.name == ".cratekit-acquire-staging"
    assert not (directory / f"{fallback.FETCH_STEM}.mp3").exists()


def test_a_strict_policy_refuses_that_item_before_anything_downloads(
    strict, tmp_path, monkeypatch
):
    accepted(strict)
    fake = bind(monkeypatch, FakeFetcher())
    job_id = queued(tracklist(tmp_path, BOOT))

    run(job_id)

    item = only_item(job_id)
    assert item.state is jobs.ItemState.FAILED
    assert item.cause is not None and item.cause.reason == "lossy-refused"
    assert item.cause.remediation.remedy == Remedy.RELAX_LOSSLESS_POLICY
    assert fake.calls == [], "a lossy download was spent under the strict policy"
    assert not any(staging(strict).glob("*.mp3"))


def test_an_existing_output_is_refused_without_a_download(permissive, tmp_path, monkeypatch):
    accepted(permissive)
    fake = bind(monkeypatch, FakeFetcher())
    job_id = queued(tracklist(tmp_path, BOOT))
    kept = marked_final(permissive)
    kept.parent.mkdir(parents=True, exist_ok=True)
    kept.write_bytes(b"a file somebody kept")

    run(job_id)

    item = only_item(job_id)
    assert item.cause is not None and item.cause.reason == "output-exists"
    assert kept.read_bytes() == b"a file somebody kept"
    assert fake.calls == [], "a download was spent on a name already taken"


def test_an_output_that_appears_during_the_download_is_refused_not_replaced(
    permissive, tmp_path, monkeypatch
):
    accepted(permissive)
    kept = marked_final(permissive)

    def somebody_writes_it():
        kept.write_bytes(b"arrived while downloading")

    bind(monkeypatch, FakeFetcher(before=somebody_writes_it))
    job_id = queued(tracklist(tmp_path, BOOT))

    run(job_id)

    item = only_item(job_id)
    assert item.cause is not None and item.cause.reason == "output-exists"
    assert kept.read_bytes() == b"arrived while downloading"


def test_artist_and_title_tags_come_from_the_row_not_the_upload_page(
    permissive, tmp_path, monkeypatch
):
    accepted(permissive)
    bind(monkeypatch, FakeFetcher())
    job_id = queued(tracklist(tmp_path, BOOT))

    run(job_id)

    final = marked_final(permissive)
    assert tags.read_tag(final, "artist") == BOOT_ARTIST
    assert tags.read_tag(final, "title") == BOOT_TITLE
    assert "UPLOAD" not in final.name


# ═══════════════════════════════════════════════════════════════════════════
# What becomes an item, and what does not
# ═══════════════════════════════════════════════════════════════════════════


def test_one_item_per_accepted_row_keyed_on_its_review_item(permissive, tmp_path, monkeypatch):
    item_id = accepted(permissive)
    job_id = queued(tracklist(tmp_path, BOOT, BOOT))
    [item] = items_of(job_id)
    assert item.item_id == item_id
    assert job_of(job_id).payload[fallback_cli.ROWS] == {
        item_id: {"artist": BOOT_ARTIST, "title": BOOT_TITLE, "url": UPLOAD}
    }
    assert job_of(job_id).payload[fallback_cli.LIST] == str(tmp_path / "unlisted.txt")


def test_nothing_accepted_queues_nothing_and_says_so(permissive, tmp_path, monkeypatch):
    offered(permissive, BOOT, UPLOAD)  # waiting, not answered
    rejected = offered(permissive, TIDE, OTHER_UPLOAD)
    answered(permissive, rejected, review.Verdict.REJECTED)

    code, envelope = queue(tracklist(tmp_path, BOOT, TIDE))

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["state"] == "nothing-accepted"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_an_acceptance_naming_no_upload_of_several_is_not_queued(permissive, tmp_path):
    item_id = offered(permissive, BOOT, UPLOAD, OTHER_UPLOAD)
    answered(permissive, item_id, review.Verdict.ACCEPTED)

    code, envelope = queue(tracklist(tmp_path, BOOT))

    assert envelope["data"]["state"] == "nothing-accepted", envelope


def test_a_row_the_library_already_holds_is_not_fetched(permissive, library, tmp_path):
    accepted(permissive, TIDE, UPLOAD)
    (library / "Music" / "Nova Reef - Tide.flac").write_bytes(b"")

    code, envelope = queue(tracklist(tmp_path, TIDE))

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "nothing-accepted"


def test_a_row_with_a_provider_route_is_not_fetched_lossy(permissive, tmp_path):
    accepted(permissive, TIDE, UPLOAD)
    wanted = match.read_text_lines(TIDE)[0]
    with review.open_store(permissive) as items:
        review.offer(
            items,
            queue=candidates.QUEUE,
            kind=candidates.KIND,
            identity=candidates.identity(wanted),
            payload={},
            options=[
                review.Option(
                    option_id="7001",
                    summary="one",
                    detail={
                        "track": intake_cli.frozen(
                            dataclasses.replace(wanted, ref="7001", origin=match.TIDAL)
                        )
                    },
                )
            ],
            handler_key="intake.missing",
        )

    code, envelope = queue(tracklist(tmp_path, TIDE))

    assert envelope["data"]["state"] == "nothing-accepted", envelope


def test_an_unmounted_library_refuses_rather_than_fetching_every_row(permissive, library, tmp_path):
    accepted(permissive)
    (library / "Music").rmdir()

    code, envelope = queue(tracklist(tmp_path, BOOT))

    assert envelope["cause"]["reason"] == "library-volume-unmounted", envelope


def test_the_accepted_upload_is_frozen_with_the_job(permissive, tmp_path, monkeypatch):
    """KTD9: an answer changed in review after queueing does not change the item."""
    item_id = accepted(permissive)
    job_id = queued(tracklist(tmp_path, BOOT))
    with review.open_store(permissive) as items:
        review.clear(items, item_id, actor="suite")
    answered(permissive, item_id, review.Verdict.ACCEPTED, option=OTHER_UPLOAD)
    fake = bind(monkeypatch, FakeFetcher())

    run(job_id)

    assert [url for url, _ in fake.calls] == [UPLOAD]


# ═══════════════════════════════════════════════════════════════════════════
# Every other refusal the worker can give
# ═══════════════════════════════════════════════════════════════════════════


def test_no_marker_text_refuses_the_item_before_a_download(library, tmp_path, monkeypatch):
    cfg = _configure(library, "allow_lossy_marked", marker="")
    accepted(cfg)
    fake = bind(monkeypatch, FakeFetcher())
    job_id = queued(tracklist(tmp_path, BOOT))

    run(job_id)

    item = only_item(job_id)
    assert item.cause is not None and item.cause.reason == "lossy-refused"
    assert fake.calls == []
    assert not any(staging(cfg).glob("*.mp3")), "a lossy file was committed unmarked"


def test_a_failed_download_is_transient_and_stays_retryable(permissive, tmp_path, monkeypatch):
    accepted(permissive)
    bind(monkeypatch, FakeFetcher(fail=fallback.FallbackUnavailable("the edge hung up")))
    job_id = queued(tracklist(tmp_path, BOOT))

    run(job_id)

    item = only_item(job_id)
    assert item.cause is not None and item.cause.reason == "unavailable-transient"
    assert item.cause.retryable is True
    assert "the edge hung up" in item.cause.message


def test_a_file_that_cannot_be_tagged_from_its_row_is_not_committed(
    permissive, tmp_path, monkeypatch
):
    accepted(permissive)
    fake = FakeFetcher(payload=b"not an mpeg stream")
    fake.fetch = lambda url, directory: _junk(directory)
    bind(monkeypatch, fake)
    job_id = queued(tracklist(tmp_path, BOOT))

    run(job_id)

    item = only_item(job_id)
    assert item.cause is not None and item.cause.reason == "unavailable-transient"
    assert not marked_final(permissive).exists()


def _junk(directory: Path) -> Path:
    landed = directory / f"{fallback.FETCH_STEM}.mp3"
    landed.write_bytes(b"not an mpeg stream")
    return landed


def test_a_missing_yt_dlp_parks_the_job_rather_than_failing_every_item(
    permissive, tmp_path, monkeypatch
):
    accepted(permissive)

    def missing():
        raise binaries.BinaryNotFound(
            "yt-dlp was not found", binary="yt-dlp", remedy=list(binaries.Remedy)[0]
        )

    monkeypatch.setattr(fallback_cli, "fetcher", missing)
    job_id = queued(tracklist(tmp_path, BOOT))

    run(job_id)

    job = job_of(job_id)
    assert job.state is jobs.JobState.BLOCKED, job
    assert job.cause is not None and job.cause.reason == "yt-dlp-missing"
    assert only_item(job_id).state is jobs.ItemState.PENDING


@pytest.mark.parametrize("url", ["file:///etc/hosts", "-o/tmp/x", "https://"])
def test_an_accepted_option_that_is_not_a_web_address_is_never_handed_to_the_tool(
    permissive, tmp_path, monkeypatch, url
):
    item_id = offered(permissive, BOOT, url)
    answered(permissive, item_id, review.Verdict.ACCEPTED, option=url)
    fake = bind(monkeypatch, FakeFetcher())
    job_id = queued(tracklist(tmp_path, BOOT))

    run(job_id)

    item = only_item(job_id)
    assert item.cause is not None and item.cause.reason == "unavailable-permanent"
    assert fake.calls == []


def test_the_stem_is_the_rows_and_carries_no_path_separator():
    assert fallback_cli.fetch_stem("A/B", "Song") == "A-B - Song"
    assert fallback_cli.fetch_stem("", "Song") == "Song"
    assert fallback_cli.fetch_stem("Artist", "x" * 300) == ("Artist - " + "x" * 300)[:120]


# ═══════════════════════════════════════════════════════════════════════════
# The shipped fetcher, through a fake runner
# ═══════════════════════════════════════════════════════════════════════════


class Runner:
    def __init__(self, *, returncode: int = 0, lands: tuple[str, ...] = ("fetched.mp3",), raises=None):
        self.returncode = returncode
        self.lands = lands
        self.raises = raises
        self.argv: list[str] | None = None

    def __call__(self, argv, **_kwargs):
        self.argv = argv
        if self.raises is not None:
            raise self.raises
        directory = Path(argv[argv.index("--output") + 1]).parent
        for name in self.lands:
            (directory / name).write_bytes(mp3_bytes())
        return subprocess.CompletedProcess(argv, self.returncode, "", "ERROR: gone\n")


def test_the_shipped_fetcher_extracts_mp3_drops_upload_metadata_and_ends_on_the_address(tmp_path):
    runner = Runner()
    landed = fallback.YtDlpFetcher("yt-dlp", run=runner).fetch(UPLOAD, tmp_path)

    assert landed == tmp_path / "fetched.mp3"
    argv = runner.argv
    assert argv is not None
    assert argv[-2:] == ["--", UPLOAD]
    assert argv[argv.index("--audio-format") + 1] == "mp3"
    assert argv[argv.index("--postprocessor-args") + 1] == "ExtractAudio:-map_metadata -1"
    assert argv[argv.index("--output") + 1] == str(tmp_path / "fetched.%(ext)s")
    assert "--no-playlist" in argv


@pytest.mark.parametrize(
    "runner",
    [
        Runner(returncode=1),
        Runner(lands=()),
        Runner(lands=("fetched.mp3", "other.mp3")),
        Runner(lands=("fetched.webm",)),
        Runner(raises=subprocess.TimeoutExpired("yt-dlp", 1)),
        Runner(raises=OSError("no such file")),
    ],
    ids=["nonzero", "nothing", "two", "not-mp3", "timeout", "unstartable"],
)
def test_the_shipped_fetcher_never_reads_a_failure_as_a_file(tmp_path, runner):
    with pytest.raises(fallback.FallbackUnavailable):
        fallback.YtDlpFetcher("yt-dlp", run=runner).fetch(UPLOAD, tmp_path)
