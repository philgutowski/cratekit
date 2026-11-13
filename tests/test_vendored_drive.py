"""U274: a download job logs in once per drive, four provider calls a track.

``crate acquire download`` built a new adapter and a new session scope for every
track, so every track read the keychain, wrote a private token file, logged in
again (``sessions``, then ``users/<id>``) and erased the file. Phillip's answer
on the card (option 1): the session is materialised, validated and written back
once per drive of one job, and the private token file is removed when the drive
ends or fails.

THE STAND IN COUNTS EVERY CALL THROUGH THE REAL GATE. The vendored tool's two
classes and its downloader are the smallest doubles the real ``authenticate``
and ``fetch`` accept (the shape ``tests/test_provider_gate.py`` uses), and each
of them asks the provider through ``request_session.request``, which the real
gate wraps. So the verb, the job engine, the paced pool, the adapter, the gate
and the in memory keychain are all the product's own, and only the provider and
the tool's insides are stood in. The tool's own per track calls are the ones
the brief measured on the live shape: ``tracks/<id>`` (the offer, then the
tool's own), ``albums/<id>`` and ``playbackinfo``.

Nothing here reaches a network, a real keychain or a real library.
"""

from __future__ import annotations

import contextlib
import dataclasses
import json
import os
import signal
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import keyring
import pytest

import cratekit._vendor.downloader.config as tool_config
import cratekit._vendor.downloader.download as tool_download
from cratekit.acquire import cli as acquire_cli
from cratekit.acquire import download, provider_session, vendored
from cratekit.cli import handlers
from cratekit.cli import jobs as cli_jobs
from cratekit.core import binaries, config, jobs, provider_gate, secrets
from cratekit.core.exit_codes import ExitCode
from tests.acquire_fakes import tidal_list, wav_bytes
from tests.cli_drive import drive
from tests.test_config import valid_data

#: The stored session: PKCE, and obviously not a real one.
STORED = {
    "token_type": "Bearer",
    "access_token": "FAKE-value-1",
    "refresh_token": "FAKE-value-2",
    "expiry_time": 1700000000,
    "is_pkce": True,
}

BASE = "https://api.invalid/v1/"


# ═══════════════════════════════════════════════════════════════════════════
# The stand in
# ═══════════════════════════════════════════════════════════════════════════


class HTTPError(Exception):
    """The client's HTTP error, carrying its status in its words, as the real one does."""


class Response:
    def __init__(self, status: int) -> None:
        self.status_code = status
        self.ok = status < 400
        self.headers: dict[str, str] = {}


class Provider:
    """What the provider answers, and every path it was asked, in order."""

    def __init__(self) -> None:
        self.asked: list[str] = []
        #: Answer 401 to every call from this call's index on (a session the
        #: provider withdrew mid drive), or None to answer every call.
        self.withdraw_at: int | None = None
        #: Refuse the login itself.
        self.reject_login = False

    def answer(self, url: str) -> Response:
        path = url.removeprefix(BASE)
        self.asked.append(path)
        if self.reject_login and path == "sessions":
            return Response(401)
        if self.withdraw_at is not None and len(self.asked) > self.withdraw_at:
            return Response(401)
        return Response(200)

    def count(self, prefix: str) -> int:
        return sum(1 for path in self.asked if path.startswith(prefix))

    def per_track(self, key: str) -> list[str]:
        """Every call about this track: its own lookups and its album's."""
        mine = {key, f"a{key}"}
        return [path for path in self.asked if mine & set(path.split("/"))]


class Transport:
    """The ``requests.Session`` the tool's client keeps, which the gate wraps."""

    def __init__(self, provider: Provider) -> None:
        self._provider = provider

    def request(self, method: str, url: str, *args: Any, **kwargs: Any) -> Response:
        return self._provider.answer(url)


class ToolSession:
    """The tool's client session: the four token fields, and the calls the adapter
    and the tool make on it. Each call goes out through ``request_session``."""

    def __init__(self, provider: Provider) -> None:
        self.request_session = Transport(provider)
        self.token_type = self.access_token = self.refresh_token = None
        self.expiry_time: Any = None
        self.is_pkce = False
        #: Refresh the access token in memory, as the client library does on an
        #: expired answer, when this track is looked up.
        self.refresh_at: str | None = None

    def _get(self, path: str) -> Response:
        response = self.request_session.request("GET", BASE + path)
        if not response.ok:
            raise HTTPError(f"{response.status_code} Client Error: Unauthorized for url {path}")
        return response

    def load_oauth_session(self, token_type, access_token, refresh_token, expiry_time, is_pkce=False):
        self.token_type, self.access_token = token_type, access_token
        self.refresh_token, self.expiry_time, self.is_pkce = refresh_token, expiry_time, is_pkce
        if not self.request_session.request("GET", BASE + "sessions").ok:
            return False
        self._get("users/7")
        return True

    def track(self, key: str) -> Any:
        if self.refresh_at == key:
            self.access_token = "FAKE-value-3"
            self.expiry_time = datetime(2030, 1, 1)
        self._get(f"tracks/{key}")
        return SimpleNamespace(audio_quality="LOSSLESS", album=SimpleNamespace(id=f"a{key}"))

    def album(self, album_id: str) -> Any:
        self._get(f"albums/{album_id}")
        return SimpleNamespace(id=album_id)

    def playbackinfo(self, key: str) -> Any:
        self._get(f"tracks/{key}/playbackinfo")
        return SimpleNamespace()


class Tool:
    """The tool's two classes and its downloader, sharing one session per test,
    as the real singleton shares one per process."""

    def __init__(self, provider: Provider) -> None:
        self.session = ToolSession(provider)
        self.built = 0
        #: Every token file the adapter pointed the tool at, and its mode then.
        self.token_files: list[tuple[Path, int, int]] = []
        #: Called in the middle of a named track's download.
        self.during: dict[str, Any] = {}

    def settings_class(self) -> type:
        class Settings:
            def __init__(self) -> None:
                self.data = SimpleNamespace()

        return Settings

    def tidal_class(self) -> Any:
        tool = self

        class Tidal:
            def __init__(self, _settings: Any) -> None:
                tool.built += 1
                self.session = tool.session
                self.data: Any = None
                self.file_path = self.path_base = ""
                self.token_from_storage = False

            def read(self, path: str) -> bool:
                try:
                    self.data = SimpleNamespace(**json.loads(Path(path).read_text()))
                except (OSError, ValueError):
                    return False
                file = Path(path)
                tool.token_files.append(
                    (file, stat.S_IMODE(file.stat().st_mode), stat.S_IMODE(file.parent.stat().st_mode))
                )
                return True

            def login_token(self, do_pkce: bool = False) -> bool:
                # The real tool's shape: every exception is caught, the token
                # file is deleted, and the answer is False.
                try:
                    return self.session.load_oauth_session(
                        self.data.token_type,
                        self.data.access_token,
                        self.data.refresh_token,
                        self.data.expiry_time,
                        is_pkce=do_pkce,
                    )
                except Exception:  # noqa: BLE001 - the tool's own shape
                    Path(self.file_path).unlink(missing_ok=True)
                    return False

        return Tidal

    def download_class(self) -> type:
        tool = self

        class Download:
            def __init__(self, *, tidal_obj, path_base, fn_logger, **_rest: Any) -> None:
                self.session = tidal_obj.session
                self.path_base = path_base
                self.fn_logger = fn_logger

            def item(self, *, file_template, media_id, media_type) -> tuple[bool, str]:
                # The tool's own lookups, then the stream, each swallowed as the
                # real tool swallows them.
                try:
                    track = self.session.track(media_id)
                    self.session.album(track.album.id)
                    hook = tool.during.get(media_id)
                    if hook is not None:
                        hook()
                    self.session.playbackinfo(media_id)
                except Exception:  # noqa: BLE001 - the tool's own shape
                    self.fn_logger.exception("download failed")
                    return False, ""
                Path(self.path_base).mkdir(parents=True, exist_ok=True)
                landed = Path(self.path_base) / f"{media_id}.wav"
                landed.write_bytes(wav_bytes())
                return True, str(landed)

        return Download


class Keychain:
    """Counts what the in memory keychain is asked for the provider session."""

    def __init__(self, monkeypatch) -> None:
        self.session_writes: list[dict] = []
        self.reads = 0
        real_set, real_get = keyring.set_password, keyring.get_password

        def set_password(service: str, username: str, password: str) -> None:
            if "access_token" in password:
                self.session_writes.append(json.loads(password))
            real_set(service, username, password)

        def get_password(service: str, username: str):
            self.reads += 1
            return real_get(service, username)

        monkeypatch.setattr(keyring, "set_password", set_password)
        monkeypatch.setattr(keyring, "get_password", get_password)


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def temporary(tmp_path, monkeypatch) -> Path:
    """The temporary directory a token directory is made in, this test's own."""
    root = tmp_path / "tmp"
    root.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(root))
    return root


@pytest.fixture
def cfg(library, temporary, tmp_path, monkeypatch) -> config.Config:
    """An installation naming the vendored adapter, the gate at a millisecond."""
    ffmpeg = tmp_path / "ffmpeg"
    ffmpeg.write_text("#!/bin/sh\nexit 0\n")
    ffmpeg.chmod(ffmpeg.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(ffmpeg))
    built = config.from_dict(
        valid_data(
            library,
            profile={"name": "full"},
            acquisition={"adapter": "vendored", "pacing_delay_s": 3.0},
            provider={"min_interval_s": 0.001},
        )
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def provider() -> Provider:
    return Provider()


@pytest.fixture
def tool(provider, monkeypatch) -> Tool:
    stand_in = Tool(provider)
    monkeypatch.setattr(tool_config, "Settings", stand_in.settings_class())
    monkeypatch.setattr(tool_config, "Tidal", stand_in.tidal_class())
    monkeypatch.setattr(tool_download, "Download", stand_in.download_class())
    return stand_in


@pytest.fixture
def stored() -> dict:
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, dict(STORED))
    return dict(STORED)


@pytest.fixture
def keychain(stored, monkeypatch) -> Keychain:
    return Keychain(monkeypatch)


@pytest.fixture(autouse=True)
def slept(monkeypatch) -> list[float]:
    """Every pacing delay the worker's pool asked for, recorded and not taken."""
    seen: list[float] = []
    monkeypatch.setattr(acquire_cli, "_SLEEP", seen.append)
    return seen


def keys(count: int) -> list[str]:
    return [str(100 + n) for n in range(count)]


def queued(library: Path, tracks: list[str]) -> str:
    path = library / "list.json"
    path.write_text(tidal_list([(key, f"Artist {key}", f"Title {key}") for key in tracks]))
    code, envelope = drive(["acquire", "download", str(path)])
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["job_id"]


def resume_argv(job_id: str) -> list[str]:
    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def job_of(job_id: str) -> jobs.Job:
    with jobs.open_store() as store:
        return jobs.get(store, job_id)


def states(job_id: str) -> dict[str, jobs.ItemState]:
    with jobs.open_store() as store:
        return {item.item_id: item.state for item in jobs.items(store, job_id)}


def token_directories(root: Path) -> list[Path]:
    return sorted(root.glob("cratekit-session-*"))


def stored_now() -> dict:
    return secrets.get_json(secrets.Credential.PROVIDER_SESSION)


# ═══════════════════════════════════════════════════════════════════════════
# 1. One login a drive, four calls a track
# ═══════════════════════════════════════════════════════════════════════════


def test_a_ten_track_job_logs_in_once_and_spends_four_calls_a_track(
    cfg, library, tool, provider, keychain, temporary, slept
):
    tracks = keys(10)
    job_id = queued(library, tracks)

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert set(states(job_id).values()) == {jobs.ItemState.DONE}
    assert provider.count("sessions") == 1
    assert provider.count("users/") == 1
    for key in tracks:
        assert provider.per_track(key) == [
            f"tracks/{key}",
            f"tracks/{key}",
            f"albums/a{key}",
            f"tracks/{key}/playbackinfo",
        ], key
    assert len(provider.asked) == 2 + 4 * len(tracks)


def test_every_call_of_the_drive_goes_through_the_gate(cfg, library, tool, provider, stored):
    """The gate's own count is the stand in's, so nothing reached the provider
    around it, and its spacing applied to each call."""
    job_id = queued(library, keys(3))
    before = provider_gate.spend().calls

    drive(resume_argv(job_id))

    assert provider_gate.spend().calls - before == len(provider.asked) == 2 + 4 * 3


def test_the_pacing_delay_is_still_taken_before_every_acquisition(
    cfg, library, tool, provider, stored, slept
):
    job_id = queued(library, keys(4))

    drive(resume_argv(job_id))

    assert len(slept) == 4
    assert all(delay > 0 for delay in slept)


def test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing(
    cfg, library, tool, provider, keychain
):
    """One read for the drive however many tracks, and no write for a session
    the provider did not refresh."""
    one = queued(library, keys(1))
    keychain.reads = 0
    drive(resume_argv(one))
    one_track = keychain.reads

    ten = queued(library, keys(10))
    keychain.reads = 0
    drive(resume_argv(ten))

    assert one_track >= 1
    assert keychain.reads == one_track, "the keychain was read again per track"
    assert keychain.session_writes == []
    assert stored_now() == STORED


def test_the_tool_is_built_and_pointed_at_one_token_file_for_the_whole_drive(
    cfg, library, tool, provider, stored, temporary
):
    job_id = queued(library, keys(5))

    drive(resume_argv(job_id))

    assert tool.built == 1
    assert len(tool.token_files) == 1
    path, mode, parent_mode = tool.token_files[0]
    assert (mode, parent_mode) == (0o600, 0o700)
    assert path.parent.parent == temporary
    assert not path.exists()
    assert token_directories(temporary) == []


def test_each_item_still_lands_in_its_own_staging_directory(
    cfg, library, tool, provider, stored, monkeypatch
):
    """The source is reused and its settings are not: the staging directory the
    tool is told is this item's own, pushed and verified on every reuse."""
    seen: list[str] = []
    real = vendored.apply_settings

    def spy(target, settings, **kwargs):
        seen.append(str(settings.download_staging))
        return real(target, settings, **kwargs)

    monkeypatch.setattr(vendored, "apply_settings", spy)
    job_id = queued(library, keys(3))
    drive(resume_argv(job_id))

    assert len(seen) == 3
    assert len(set(seen)) == 3
    assert set(states(job_id).values()) == {jobs.ItemState.DONE}


def test_two_drives_log_in_twice(cfg, library, tool, provider, stored):
    """Once per DRIVE: a second job, or a resume, materialises and logs in again."""
    drive(resume_argv(queued(library, keys(2))))
    drive(resume_argv(queued(library, keys(2))))

    assert provider.count("sessions") == 2


# ═══════════════════════════════════════════════════════════════════════════
# 2. A refused session still parks, and is never logged into again
# ═══════════════════════════════════════════════════════════════════════════


def test_a_rejected_login_parks_the_job_after_one_login(cfg, library, tool, provider, keychain):
    provider.reject_login = True
    job_id = queued(library, keys(5))

    code, envelope = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "auth-failed", envelope
    assert job_of(job_id).state is jobs.JobState.BLOCKED
    assert set(states(job_id).values()) == {jobs.ItemState.PENDING}
    assert provider.count("sessions") == 1
    assert keychain.session_writes == []
    assert stored_now() == STORED


def test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest(
    cfg, library, tool, provider, keychain, temporary
):
    tracks = keys(5)
    job_id = queued(library, tracks)
    # The login (2) and two tracks (8) are answered, then every call is refused.
    provider.withdraw_at = 2 + 4 * 2

    code, envelope = drive(resume_argv(job_id))

    assert envelope["cause"]["reason"] == "auth-failed", envelope
    assert job_of(job_id).state is jobs.JobState.BLOCKED
    assert [states(job_id)[key] for key in tracks] == [
        jobs.ItemState.DONE,
        jobs.ItemState.DONE,
        jobs.ItemState.PENDING,
        jobs.ItemState.PENDING,
        jobs.ItemState.PENDING,
    ]
    assert provider.count("sessions") == 1, "the drive logged in again over a refused session"
    assert keychain.session_writes == []
    assert token_directories(temporary) == []

    # The person records a fresh session; the provider answers again.
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, {**STORED, "access_token": "FAKE-value-4"})
    provider.withdraw_at = None
    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert set(states(job_id).values()) == {jobs.ItemState.DONE}
    assert provider.count("sessions") == 2
    assert token_directories(temporary) == []


def test_a_missing_session_parks_and_leaves_no_file(cfg, library, tool, provider, temporary):
    """Nothing recorded: the drive's first track cannot materialise, the job
    parks on the credential, and no call or file is made."""
    job_id = queued(library, keys(3))

    code, envelope = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), envelope
    assert job_of(job_id).state is jobs.JobState.BLOCKED
    assert set(states(job_id).values()) == {jobs.ItemState.PENDING}
    assert provider.asked == []
    assert token_directories(temporary) == []


def test_a_refused_source_raises_again_with_no_call(cfg, tmp_path, tool, provider, stored):
    """The guard under the park: a source that met a refusal never logs in or
    asks again, whatever its caller does next."""
    provider.reject_login = True
    staging = tmp_path / "staging"
    staging.mkdir()
    settings = vendored.AdapterSettings.from_config(cfg)
    with vendored.drive() as held:
        source = held.source(settings)
        with pytest.raises(vendored.AdapterAuthFailed):
            source.authenticate()
        asked = len(provider.asked)
        with pytest.raises(vendored.AdapterAuthFailed):
            held.source(settings).authenticate()
    assert len(provider.asked) == asked == 1


# ═══════════════════════════════════════════════════════════════════════════
# 3. A refreshed session reaches the keychain, once
# ═══════════════════════════════════════════════════════════════════════════


def test_a_token_refreshed_during_the_drive_is_stored_once(cfg, library, tool, provider, keychain):
    tracks = keys(6)
    tool.session.refresh_at = tracks[2]
    job_id = queued(library, tracks)

    code, envelope = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), envelope
    assert len(keychain.session_writes) == 1
    written = stored_now()
    assert written["access_token"] == "FAKE-value-3"
    assert written["refresh_token"] == STORED["refresh_token"]
    assert written["is_pkce"] is True
    # The client's naive datetime is UTC, stored as the epoch.
    assert written["expiry_time"] == datetime(2030, 1, 1, tzinfo=timezone.utc).timestamp()


def test_a_refresh_before_a_withdrawal_still_reaches_the_keychain(
    cfg, library, tool, provider, keychain
):
    """The drive that parks still writes back what the provider gave it."""
    tracks = keys(4)
    tool.session.refresh_at = tracks[0]
    provider.withdraw_at = 2 + 4 * 2
    job_id = queued(library, tracks)

    drive(resume_argv(job_id))

    assert job_of(job_id).state is jobs.JobState.BLOCKED
    assert [w["access_token"] for w in keychain.session_writes] == ["FAKE-value-3"]


def test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain(
    cfg, library, tool, provider, keychain, temporary
):
    """A drive whose every item failed ends in the engine's no evidence raise,
    which is the drive scope closing by an exception."""
    tracks = keys(2)
    tool.session.refresh_at = tracks[0]

    def broken() -> None:
        raise RuntimeError("the stream manifest could not be parsed")

    for key in tracks:
        tool.during[key] = broken
    job_id = queued(library, tracks)

    code, envelope = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), envelope
    assert set(states(job_id).values()) == {jobs.ItemState.FAILED}
    assert [w["access_token"] for w in keychain.session_writes] == ["FAKE-value-3"]
    assert token_directories(temporary) == []


# ═══════════════════════════════════════════════════════════════════════════
# 4. The token file goes on every way out
# ═══════════════════════════════════════════════════════════════════════════


def test_a_drive_signalled_mid_track_leaves_no_token_file(
    cfg, library, tool, provider, stored, temporary
):
    tracks = keys(4)
    tool.during[tracks[1]] = lambda: os.kill(os.getpid(), signal.SIGTERM)
    job_id = queued(library, tracks)

    drive(resume_argv(job_id))

    assert job_of(job_id).state is jobs.JobState.CANCELLED
    assert states(job_id)[tracks[2]] is jobs.ItemState.PENDING
    assert len(tool.token_files) == 1
    assert not tool.token_files[0][0].exists()
    assert token_directories(temporary) == []


class Killed(BaseException):
    """What an interpreter that is being torn down raises through everything."""


def test_a_drive_torn_down_mid_track_leaves_no_token_file(
    cfg, library, tool, provider, stored, temporary
):
    tracks = keys(3)

    def killed() -> None:
        raise Killed

    tool.during[tracks[1]] = killed
    job_id = queued(library, tracks)

    with jobs.open_store() as store, pytest.raises(Killed):
        handlers.run_job(store, jobs.get(store, job_id))

    assert len(tool.token_files) == 1
    assert not tool.token_files[0][0].exists()
    assert token_directories(temporary) == []


def test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps(
    cfg, library, tool, provider, stored, temporary
):
    """A hard kill runs no code at all, so the next materialise removes what a
    process that is gone left behind, and nothing a live process holds."""
    dead = subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"],
                          capture_output=True, text=True, check=True)
    orphan = temporary / f"cratekit-session-{int(dead.stdout)}-abc123"
    orphan.mkdir(mode=0o700)
    (orphan / "token.json").write_text(json.dumps(STORED))
    live = temporary / f"cratekit-session-{os.getppid()}-def456"
    live.mkdir(mode=0o700)

    drive(resume_argv(queued(library, keys(1))))

    assert not orphan.exists()
    assert live.exists()


@pytest.mark.parametrize("shape", ["file", "symlink", "older-name", "own-process"])
def test_the_sweep_leaves_alone_what_it_cannot_prove_is_an_orphan(temporary, stored, shape):
    dead = subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"],
                          capture_output=True, text=True, check=True)
    pid = int(dead.stdout)
    if shape == "file":
        left = temporary / f"cratekit-session-{pid}-abc123"
        left.write_text("not a directory")
    elif shape == "symlink":
        target = temporary / "elsewhere"
        target.mkdir()
        left = temporary / f"cratekit-session-{pid}-abc123"
        left.symlink_to(target)
    elif shape == "older-name":
        left = temporary / "cratekit-session-abc123"
        left.mkdir()
    else:
        left = temporary / f"cratekit-session-{os.getpid()}-abc123"
        left.mkdir()

    with provider_session.materialised_session():
        pass

    assert left.exists() or left.is_symlink()


def test_the_sweep_leaves_another_accounts_directory_alone(temporary, stored, monkeypatch):
    dead = subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"],
                          capture_output=True, text=True, check=True)
    left = temporary / f"cratekit-session-{int(dead.stdout)}-abc123"
    left.mkdir()
    monkeypatch.setattr(os, "getuid", lambda: os.stat(left).st_uid + 1)

    with provider_session.materialised_session():
        pass

    assert left.exists()


def test_a_materialised_directory_names_its_process(temporary, stored):
    with provider_session.materialised_session() as scope:
        assert scope.directory.name.startswith(f"cratekit-session-{os.getpid()}-")
    assert not scope.directory.exists()


# ═══════════════════════════════════════════════════════════════════════════
# 5. R-293's asymmetry holds
# ═══════════════════════════════════════════════════════════════════════════


def test_a_broken_item_fails_alone_and_the_job_stays_resumable(
    cfg, library, tool, provider, stored, temporary
):
    """A tool that breaks on one track fails that track; the run goes on with
    the same login and the job ends failed, resumable, with the rest done."""
    tracks = keys(3)

    def broken() -> None:
        raise TypeError("'NoneType' object is not subscriptable")

    tool.during[tracks[1]] = broken
    job_id = queued(library, tracks)

    drive(resume_argv(job_id))

    assert job_of(job_id).state is jobs.JobState.FAILED
    assert job_of(job_id).cause.reason == "adapter-broken"
    assert states(job_id) == {
        tracks[0]: jobs.ItemState.DONE,
        tracks[1]: jobs.ItemState.FAILED,
        tracks[2]: jobs.ItemState.DONE,
    }
    assert provider.count("sessions") == 1
    assert token_directories(temporary) == []


def test_outside_a_drive_the_adapter_still_materialises_per_invocation(
    cfg, tmp_path, tool, provider, stored, temporary
):
    """No drive, no hold: the adapter's own scope is the one it always had."""
    settings = vendored.AdapterSettings.from_config(cfg)
    adapter = vendored.VendoredAdapter(settings)

    for key in ("1", "2"):
        download.acquire_paced(adapter, (vendored.TrackRequest(key=key),), sleep=lambda _s: None)

    assert provider.count("sessions") == 2
    assert token_directories(temporary) == []


# ═══════════════════════════════════════════════════════════════════════════
# 6. The engine's per drive seam
# ═══════════════════════════════════════════════════════════════════════════


def test_the_download_worker_names_the_vendored_drive():
    assert handlers.per_drive_of(acquire_cli.handle) is vendored.drive


def test_a_worker_naming_no_drive_has_none():
    assert handlers.per_drive_of(lambda job, item, cfg: None) is None


def test_a_drive_that_is_not_callable_is_refused():
    def worker(job, item, cfg):
        return None

    worker.per_drive = "vendored"  # type: ignore[attr-defined]
    with pytest.raises(Exception) as caught:
        handlers.per_drive_of(worker)
    assert caught.value.cause.reason == "internal-error"


def test_the_engine_opens_a_workers_drive_once_and_closes_it_on_a_park(
    cfg, library, monkeypatch
):
    """Three items, one open and one close, and the close runs when the drive
    ends in a park rather than a finish."""
    opened: list[str] = []
    claimed: list[str] = []

    @contextlib.contextmanager
    def held():
        opened.append("open")
        try:
            yield
        finally:
            opened.append("close")

    def worker(job, item, frozen):
        claimed.append(item.item_id)
        if item.item_id == "2":
            raise jobs.Parked(
                download.blocked_cause(
                    adapter="vendored",
                    key="2",
                    signal=download.ProviderSignal.BLOCKED,
                    detail="403 Forbidden",
                    attempts=1,
                    retry_hint_s=None,
                )
            )
        return None

    worker.per_drive = held  # type: ignore[attr-defined]
    monkeypatch.setattr(handlers, "resolve", lambda key: worker)
    with jobs.open_store() as store:
        job = jobs.enqueue(store, handler_key="acquire.download", payload={}, cfg=cfg,
                           item_ids=("1", "2", "3"))
        handlers.run_job(store, job)
        state = jobs.get(store, job.job_id).state

    assert claimed == ["1", "2"]
    assert opened == ["open", "close"]
    assert state is jobs.JobState.BLOCKED


def test_a_refusal_outlives_the_source_it_was_met_on(cfg, tool, provider, stored):
    """A drive hands out a new source only for other gate settings, which a
    frozen configuration never has; even then the refusal carries over."""
    provider.reject_login = True
    settings = vendored.AdapterSettings.from_config(cfg)
    other = dataclasses.replace(
        settings, gate=dataclasses.replace(settings.gate, min_interval_s=0.002)
    )
    with vendored.drive() as held:
        with pytest.raises(vendored.AdapterAuthFailed):
            held.source(settings).authenticate()
        fresh = held.source(other)
        with pytest.raises(vendored.AdapterAuthFailed):
            fresh.authenticate()
    assert provider.count("sessions") == 1
