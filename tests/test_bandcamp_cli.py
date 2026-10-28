"""U176: ``crate acquire bandcamp`` plans, ``crate acquire bandcamp-fetch`` stages.

EVERYTHING BUT THE TRANSPORT IS REAL. The keychain is the suite's isolated
one, and the library index, the matcher, the job queue and its driver, the
codec probe and the record all run as shipped. The transport is
:class:`tests.bandcamp_fakes.FakeAccount`, bound where the verbs look it up.
The releases it serves are real FLAC containers, tagged, inside real archives.

D1 applies. No real person, seller or release is named.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from cratekit.acquire import bandcamp_cli
from cratekit.cli import jobs as cli_jobs
from cratekit.core import config, jobs, secrets, tags
from cratekit.core.exit_codes import ExitCode
from tests._containers import synth_container
from tests.acquire_fakes import mp3_bytes
from tests.bandcamp_fakes import COOKIE, IDENTITY, SIGNED, FakeAccount, archive, item
from tests.cli_drive import drive
from tests.test_config import valid_data

SESSION = str(secrets.Credential.BANDCAMP_SESSION)
MARKER = "[LOSSY]"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


def _configure(library: Path, policy: str = "strict") -> config.Config:
    built = config.from_dict(
        valid_data(
            library,
            acquisition={"lossless_policy": policy},
            naming={"lossy_marker": MARKER},
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
def cfg(library) -> config.Config:
    return _configure(library)


@pytest.fixture
def signed_in(cfg):
    secrets.set(SESSION, COOKIE)
    return cfg


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> bytes:
    """One second of silence as FLAC, the bytes every served track starts from."""
    return synth_container(tmp_path_factory.mktemp("flac"), ".flac").read_bytes()


def track_file(tmp_path: Path, silence: bytes, name: str, artist: str, title: str) -> bytes:
    """A real FLAC named and tagged the way a Bandcamp release's file is."""
    path = tmp_path / "tracks" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(silence)
    assert tags.write_tags(path, {"artist": artist, "title": title})
    return path.read_bytes()


def owned(library: Path, name: str) -> Path:
    """A file the library holds, named the library's way."""
    path = library / "Music" / "Owned" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")
    return path


def bind(monkeypatch, account: FakeAccount) -> FakeAccount:
    monkeypatch.setattr(bandcamp_cli, "transport", lambda: account)
    return account


#: The account sitting 46's shapes stand for: a new release, a release the
#: library owns, a compilation holding one owned track, a release from another
#: seller, and a preorder.
def collection(tmp_path: Path, silence: bytes, **account) -> FakeAccount:
    items = [
        item("1", seller="pulsromania", artist="Aurora Bloom", title="Sun Path",
             purchased="27 Oct 2026 10:00:00 GMT", tracks=[("", "Sun Path"), ("", "Tide")]),
        item("2", seller="pulsromania", artist="Nova Reef", title="Low Light",
             purchased="20 Oct 2026 10:00:00 GMT", tracks=[("", "Low Light")]),
        item("3", seller="pulsromania", artist="Various Artists", title="Compiled",
             purchased="12 Oct 2026 10:00:00 GMT",
             tracks=[("Coral Arc", "Glass"), ("Nova Reef", "Shore")]),
        item("4", seller="otherlabel", artist="Coral Arc", title="Drift",
             purchased="05 Oct 2026 10:00:00 GMT", tracks=[("", "Drift")]),
        item("5", seller="pulsromania", artist="Aurora Bloom", title="Soon",
             purchased="01 Oct 2026 10:00:00 GMT", preorder=True),
    ]
    archives = {
        "1": archive({
            "Aurora Bloom - Sun Path - 01 Sun Path.flac":
                track_file(tmp_path, silence, "a1.flac", "Aurora Bloom", "Sun Path"),
            "Aurora Bloom - Sun Path - 02 Tide.flac":
                track_file(tmp_path, silence, "a2.flac", "Aurora Bloom", "Tide"),
            "cover.jpg": b"art",
        }),
        "3": archive({
            "Various Artists - Compiled - 01 Coral Arc - Glass.flac":
                track_file(tmp_path, silence, "c1.flac", "Coral Arc", "Glass"),
            "Various Artists - Compiled - 02 Nova Reef - Shore.flac":
                track_file(tmp_path, silence, "c2.flac", "Nova Reef", "Shore"),
        }),
        "4": archive({
            "Coral Arc - Drift - 01 Drift.flac":
                track_file(tmp_path, silence, "d1.flac", "Coral Arc", "Drift"),
        }),
    }
    return FakeAccount(items, page_size=2, archives=archives, **account)


@pytest.fixture
def account(tmp_path, silence, library, monkeypatch) -> FakeAccount:
    owned(library, "Nova Reef - Low Light.flac")
    owned(library, "Nova Reef - Shore.flac")
    return bind(monkeypatch, collection(tmp_path, silence))


def plan(*sellers: str) -> tuple[int, dict]:
    return drive(["acquire", "bandcamp", *(arg for name in sellers for arg in ("--seller", name))])


def fetch(*args: str) -> tuple[int, dict]:
    return drive(["acquire", "bandcamp-fetch", *args])


def rows(envelope: dict) -> dict[str, dict]:
    return {row["item_id"]: row for row in envelope["data"]["summary"]["rows"]}


def dispositions(envelope: dict) -> dict[str, str]:
    return {key: row["disposition"] for key, row in rows(envelope).items()}


def staged(cfg, batch: str) -> list[str]:
    folder = Path(cfg.paths.download_staging) / batch
    return sorted(path.name for path in folder.iterdir()) if folder.is_dir() else []


# ═══════════════════════════════════════════════════════════════════════════
# The plan
# ═══════════════════════════════════════════════════════════════════════════


def test_the_plan_gives_every_purchase_newest_first_one_disposition(signed_in, account):
    code, envelope = plan()
    assert code == int(ExitCode.OK), envelope
    assert list(rows(envelope)) == ["1", "2", "3", "4", "5"]
    assert dispositions(envelope) == {
        "1": "new",
        "2": "owned",
        "3": "held",
        "4": "new",
        "5": "not-downloadable",
    }
    summary = envelope["data"]["summary"]
    assert summary["purchases"] == 5 and summary["new"] == 2 and summary["owned"] == 1
    assert summary["fetch_next"] == "crate acquire bandcamp-fetch"
    assert all(row["seller"] for row in summary["rows"])


def test_the_plan_writes_nothing_and_downloads_nothing(signed_in, account, library):
    before = sorted(path for path in library.rglob("*"))
    plan()
    assert sorted(path for path in library.rglob("*")) == before
    assert account.downloaded == []
    assert not config.state_path("bandcamp_fetched", signed_in).exists()


def test_an_owned_release_names_the_owned_file_and_is_not_fetched(signed_in, account, library):
    _code, envelope = plan()
    owned_row = rows(envelope)["2"]
    assert owned_row["held"][0]["paths"] == [str(library / "Music" / "Owned" / "Nova Reef - Low Light.flac")]
    assert owned_row["stage"] == []
    code, queued = fetch()
    assert code == int(ExitCode.OK), queued
    with jobs.open_store() as store:
        assert {one.item_id for one in jobs.items(store, queued["data"]["job_id"])} == {"1", "3", "4"}


def test_a_compilation_with_one_owned_track_stages_the_rest_and_names_the_one(signed_in, account):
    _code, envelope = plan()
    compiled = rows(envelope)["3"]
    assert [(one["artist"], one["title"]) for one in compiled["held"]] == [("Nova Reef", "Shore")]
    assert [one["title"] for one in compiled["stage"]] == ["Glass"]
    code, fetched = fetch("--batch", "Batch One")
    assert code == int(ExitCode.OK), fetched
    names = staged(signed_in, "Batch One")
    assert "Various Artists - Compiled - 01 Coral Arc - Glass.flac" in names
    assert not any("Shore" in name for name in names)
    record = bandcamp_cli.fetched(signed_in)["3"]
    assert record["held"] == ["Various Artists - Compiled - 02 Nova Reef - Shore.flac"]
    assert record["staged"] == ["Various Artists - Compiled - 01 Coral Arc - Glass.flac"]


def test_a_seller_filter_plans_only_that_seller(signed_in, account):
    _code, envelope = plan("pulsromania")
    assert dispositions(envelope)["4"] == "filtered"
    assert "filtered" not in {d for key, d in dispositions(envelope).items() if key != "4"}
    assert envelope["data"]["summary"]["fetch_next"] == "crate acquire bandcamp-fetch --seller pulsromania"


def test_a_seller_is_matched_whatever_its_case(signed_in, account):
    _code, envelope = plan("PulsRomania")
    assert dispositions(envelope)["1"] == "new"


def test_a_seller_matching_nothing_is_warned_about(signed_in, account):
    _code, envelope = plan("nosuchlabel")
    assert set(dispositions(envelope).values()) == {"filtered"}
    assert envelope["data"]["summary"]["sellers_unmatched"] == ["nosuchlabel"]
    assert any("nosuchlabel" in warning["message"] for warning in envelope["warnings"])
    assert envelope["outcome"] == "no_op"


def test_a_preorder_is_not_downloadable(signed_in, account):
    _code, envelope = plan()
    assert rows(envelope)["5"]["disposition"] == "not-downloadable"
    assert rows(envelope)["5"]["preorder"] is True


def test_a_hidden_purchase_is_planned_hidden(signed_in, tmp_path, silence, monkeypatch):
    hidden = [item("8", seller="pulsromania", artist="B", title="Hid", purchased="15 Oct 2026 10:00:00 GMT")]
    bind(monkeypatch, FakeAccount(hidden=hidden))
    _code, envelope = plan()
    assert dispositions(envelope) == {"8": "hidden"}


# ═══════════════════════════════════════════════════════════════════════════
# The session
# ═══════════════════════════════════════════════════════════════════════════


def test_an_expired_session_is_auth_failed_naming_the_login_step(signed_in, tmp_path, silence, monkeypatch):
    bind(monkeypatch, collection(tmp_path, silence, expired=True))
    for code, envelope in (plan(), fetch()):
        assert code == int(ExitCode.UPSTREAM_AUTH), envelope
        cause = envelope["cause"]
        assert cause["reason"] == "auth-failed"
        assert any(f"crate login {SESSION} --from-file" in step for step in cause["remediation"]["steps"])
        assert envelope["data"] is None or not envelope["data"].get("summary")


def test_no_recorded_session_is_auth_failed_before_any_request(cfg, monkeypatch):
    account = bind(monkeypatch, FakeAccount())
    code, envelope = plan()
    assert code == int(ExitCode.UPSTREAM_AUTH), envelope
    assert envelope["cause"]["reason"] == "auth-failed"
    assert account.requests == [] and account.posted == []


def test_login_records_the_session_from_a_file(cfg, tmp_path):
    source = tmp_path / "cookie.txt"
    source.write_text(COOKIE + "\n", encoding="utf-8")
    code, envelope = drive(["login", SESSION, "--from-file", str(source)])
    assert code == int(ExitCode.OK), envelope
    assert secrets.get(SESSION) == COOKIE
    assert IDENTITY not in json.dumps(envelope)


# ═══════════════════════════════════════════════════════════════════════════
# The fetch and the record
# ═══════════════════════════════════════════════════════════════════════════


def test_the_fetch_stages_flat_into_its_batch_folder_and_records_each(signed_in, account):
    code, envelope = fetch("--batch", "Batch One")
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "succeeded"
    assert staged(signed_in, "Batch One") == [
        "Aurora Bloom - Sun Path - 01 Sun Path.flac",
        "Aurora Bloom - Sun Path - 02 Tide.flac",
        "Coral Arc - Drift - 01 Drift.flac",
        "Various Artists - Compiled - 01 Coral Arc - Glass.flac",
    ]
    assert set(bandcamp_cli.fetched(signed_in)) == {"1", "3", "4"}
    holding = Path(signed_in.paths.download_staging) / ".cratekit-acquire-staging"
    assert not any(path.is_file() for path in holding.rglob("*")), "the holding folder is emptied"


def test_the_default_batch_is_named_for_today(signed_in, account):
    from datetime import date

    fetch()
    assert staged(signed_in, f"Bandcamp {date.today().isoformat()}")


def test_a_batch_name_that_is_not_one_folder_is_refused(signed_in, account):
    code, envelope = fetch("--batch", "../out")
    assert code == int(ExitCode.PRECONDITION), envelope
    assert account.downloaded == []


def test_a_second_run_plans_nothing(signed_in, account):
    fetch()
    _code, envelope = plan()
    assert dispositions(envelope) == {
        "1": "fetched", "2": "owned", "3": "fetched", "4": "fetched", "5": "not-downloadable",
    }
    assert envelope["outcome"] == "no_op"
    code, again = fetch()
    assert code == int(ExitCode.OK) and again["outcome"] == "no_op", again
    assert again["data"]["state"] == "nothing-new"


def test_a_purchase_filtered_out_is_offered_on_the_next_run_without_the_filter(signed_in, account):
    fetch("--seller", "pulsromania")
    assert "4" not in bandcamp_cli.fetched(signed_in)
    _code, envelope = plan()
    assert dispositions(envelope)["4"] == "new"


def test_a_name_already_in_the_batch_refuses_that_file_alone(signed_in, account):
    batch = Path(signed_in.paths.download_staging) / "Batch One"
    batch.mkdir(parents=True)
    existing = batch / "Aurora Bloom - Sun Path - 02 Tide.flac"
    existing.write_bytes(b"already here")
    code, envelope = fetch("--batch", "Batch One")
    assert code != int(ExitCode.OK), envelope
    assert existing.read_bytes() == b"already here"
    names = staged(signed_in, "Batch One")
    assert "Aurora Bloom - Sun Path - 01 Sun Path.flac" in names
    assert "Coral Arc - Drift - 01 Drift.flac" in names
    with jobs.open_store() as store:
        by_id = {one.item_id: one for one in jobs.items(store, _last_job())}
    assert by_id["1"].cause.reason == "output-exists"
    assert "Aurora Bloom - Sun Path - 02 Tide.flac" in by_id["1"].cause.message
    assert str(by_id["4"].state) == "done"
    assert bandcamp_cli.fetched(signed_in)["1"]["refused"] == ["Aurora Bloom - Sun Path - 02 Tide.flac"]


def _last_job() -> str:
    with jobs.open_store() as store:
        return jobs.list_jobs(store)[-1].job_id


def test_a_file_the_track_list_did_not_name_is_held_by_its_own_tags(signed_in, tmp_path, silence, library, monkeypatch):
    owned(library, "Aurora Bloom - Tide.flac")
    account = collection(tmp_path, silence)
    # The list spells the track differently from its file, so only the file's
    # own tags can tell the library holds it.
    account.items[0]["_tracks"][1]["title"] = "Tide (Album Edit)"
    bind(monkeypatch, account)
    _code, envelope = plan("pulsromania")
    assert rows(envelope)["1"]["disposition"] == "new"
    fetch("--seller", "pulsromania", "--batch", "Batch One")
    assert "Aurora Bloom - Sun Path - 02 Tide.flac" not in staged(signed_in, "Batch One")
    assert bandcamp_cli.fetched(signed_in)["1"]["held"] == ["Aurora Bloom - Sun Path - 02 Tide.flac"]


def _only_item(job_id: str) -> jobs.Item:
    with jobs.open_store() as store:
        [one] = jobs.items(store, job_id)
    return one


def test_strict_refuses_a_release_offered_only_lossy(signed_in, tmp_path, silence, monkeypatch):
    account = bind(monkeypatch, collection(tmp_path, silence, encodings=("mp3-320",)))
    code, envelope = fetch("--seller", "otherlabel", "--batch", "Batch One")
    assert code != int(ExitCode.OK), envelope
    assert _only_item(_last_job()).cause.reason == "lossy-refused"
    assert account.downloaded == [], "the policy is asked before anything downloads"
    assert staged(signed_in, "Batch One") == []
    assert bandcamp_cli.fetched(signed_in) == {}


def test_a_permissive_policy_takes_the_lossy_release_marked(library, tmp_path, silence, monkeypatch):
    permissive = _configure(library, "allow_lossy_marked")
    secrets.set(SESSION, COOKIE)
    account = collection(tmp_path, silence, encodings=("mp3-320",))
    account.archives["4"] = archive({"Coral Arc - Drift - 01 Drift.mp3": mp3_bytes()})
    bind(monkeypatch, account)
    code, envelope = fetch("--seller", "otherlabel", "--batch", "Batch One")
    assert code == int(ExitCode.OK), envelope
    assert staged(permissive, "Batch One") == [f"Coral Arc - Drift - 01 Drift {MARKER}.mp3"]
    assert bandcamp_cli.fetched(permissive)["4"]["encoding"] == "mp3-320"


def test_an_empty_job_identifier_is_refused(signed_in, account):
    code, envelope = fetch("--job", " ")
    assert code == int(ExitCode.PRECONDITION), envelope
    assert account.posted == []


def test_the_download_takes_flac_when_it_is_offered(signed_in, account):
    fetch("--seller", "otherlabel")
    assert all("enc=flac" in url for url in account.downloaded)
    assert bandcamp_cli.fetched(signed_in)["4"]["encoding"] == "flac"


def test_a_session_refused_in_the_worker_parks_the_job_and_a_resume_continues(signed_in, account):
    account.expired_after_listing = True
    original = account.get

    def expiring(url, *, cookie):
        if "/download" in url and getattr(account, "expired_after_listing", False):
            return type(original(url, cookie=cookie))(403, "forbidden")
        return original(url, cookie=cookie)

    account.get = expiring
    code, envelope = fetch("--seller", "otherlabel")
    assert code != int(ExitCode.OK), envelope
    job_id = _last_job()
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        assert str(job.state) == "blocked"
        assert job.cause.reason == "auth-failed"
        [pending] = jobs.items(store, job_id)
        assert str(pending.state) == "pending"
    account.expired_after_listing = False
    bandcamp_cli.forget()
    with jobs.open_store() as store:
        code, resumed = drive(cli_jobs.argv_for(jobs.get(store, job_id)))
    assert code == int(ExitCode.OK), resumed
    assert "4" in bandcamp_cli.fetched(signed_in)


def test_a_purchase_the_record_holds_is_done_on_a_resume_and_fetched_nothing_twice(signed_in, account):
    bandcamp_cli.record_fetched(signed_in, "4", {"seller": "otherlabel"})
    assert bandcamp_cli.fetched(signed_in)["4"] == {"seller": "otherlabel"}
    _code, envelope = plan("otherlabel")
    assert rows(envelope)["4"]["disposition"] == "fetched"


# ═══════════════════════════════════════════════════════════════════════════
# What is not there is not read as nothing
# ═══════════════════════════════════════════════════════════════════════════


def test_an_absent_music_folder_refuses_rather_than_planning_everything_new(signed_in, account, library):
    (library / "Music" / "Owned" / "Nova Reef - Low Light.flac").unlink()
    (library / "Music" / "Owned" / "Nova Reef - Shore.flac").unlink()
    (library / "Music" / "Owned").rmdir()
    (library / "Music").rmdir()
    code, envelope = plan()
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "library-volume-unmounted"
    assert account.posted == []


@pytest.mark.parametrize(
    "text",
    ["not json", "[]", '{"version": 2, "purchases": {}}', '{"version": 1}'],
    ids=["not-json", "not-a-map", "newer-version", "no-purchases"],
)
def test_an_unreadable_record_refuses_rather_than_offering_everything_again(signed_in, account, text):
    path = config.state_path("bandcamp_fetched", signed_in)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    code, envelope = plan()
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "bandcamp-record-unusable"
    assert account.posted == []


# ═══════════════════════════════════════════════════════════════════════════
# The session and the signed links reach nothing that is kept or shown
# ═══════════════════════════════════════════════════════════════════════════


def _every_file_under(*roots: Path) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        if root.is_dir():
            found.extend(path for path in root.rglob("*") if path.is_file())
    return found


def test_no_output_log_or_file_holds_the_identity_or_a_signed_link(
    signed_in, account, library, caplog, tmp_path
):
    caplog.set_level(logging.DEBUG)
    batch = Path(signed_in.paths.download_staging) / "Batch One"
    batch.mkdir(parents=True)
    (batch / "Aurora Bloom - Sun Path - 02 Tide.flac").write_bytes(b"x")
    shown = [plan(), fetch("--batch", "Batch One"), plan()]
    for _code, envelope in shown:
        text = json.dumps(envelope)
        assert IDENTITY not in text and "IDENTITYVALUE" not in text
        assert SIGNED not in text
    assert "IDENTITYVALUE" not in caplog.text and SIGNED not in caplog.text
    kept = _every_file_under(
        library,
        Path(signed_in.paths.download_staging),
        config.installation_state_dir(),
        config.config_dir(),
    )
    assert kept, "the run kept nothing, so this test measured nothing"
    for path in kept:
        data = path.read_bytes()
        assert b"IDENTITYVALUE" not in data, path
        assert SIGNED.encode() not in data, path
    with jobs.open_store() as store:
        for job in jobs.list_jobs(store):
            assert SIGNED not in json.dumps(job.payload)
            for one in jobs.items(store, job.job_id):
                if one.cause is not None:
                    assert SIGNED not in json.dumps(one.cause.to_json())
