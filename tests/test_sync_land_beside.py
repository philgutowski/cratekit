"""R-1499: ``crate sync land`` lands only its own pass's tracks.

Every download stages into the one folder and ``intake land`` lands the whole
of it. Until R-1499 a sync pass ran its tail and planned its landing over
whatever the folder held, so a label go's download waiting at its own
landing's gate, a plain ``acquire download`` or an earlier pass's unlanded
download landed under this pass's name. R-1467 built the reading for the
label go; the pass now reads the folder the same way,
:func:`cratekit.intake.beside.beside`, before its download and again before
its tail, and refuses beside anything that is not its own.

WHAT STANDS IN. The suite's ``Tail`` answers ``name apply`` with nothing
renamed; the real one renames every track before the landing's gate, so the
stand in here renames them, at that moment (:class:`RenamingTail`). Every
other step is :mod:`tests.test_sync_land`'s: the pass, its intake jobs, the
missing list and the download are real.
"""

# ruff: noqa: F811, the fixtures below are imported from the sync land suite by name
from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.cli import sync_land
from cratekit.cli import tail as tail_chain
from cratekit.core.cause import Cause, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import beside as staged_reading
from cratekit.intake import land_cli
from tests.acquire_fakes import Landing
from tests.cli_drive import drive
from tests.test_label_sync_go import (
    approved_go,
    downloaded_by_hand,
    one_release_answered,
    our_jobs,
)
from tests.test_sync_all import _playlist, bind_playlists
from tests.test_sync_land import (  # noqa: F401 - fixtures by name
    Tail,
    _account,
    _by_key,
    _check,
    _refused,
    _staged,
    _summary,
    full,
    machine,
    tail,
    vocal_model,
)
from tests.test_sync_land_staged import ISRC, _rows


class RenamingTail(Tail):
    """The suite's tail, whose ``name apply`` renames every track as the real one does.

    Each audio file in the folder not yet renamed is renamed to ``Artist -
    <stem>.wav`` when the name step runs, before the landing's gate, which is
    the state every batch stopped at its gate is in.
    """

    def __call__(self, argv: list[str]) -> tuple[int, dict]:
        if "name" in argv and "apply" in argv:
            folder = Path(argv[argv.index("--root") + 1])
            for path in sorted(folder.iterdir()):
                if path.is_file() and path.suffix == ".wav" and not path.name.startswith("Artist - "):
                    path.rename(folder / f"Artist - {path.stem}.wav")
        return super().__call__(argv)


@pytest.fixture
def renaming(monkeypatch) -> RenamingTail:
    stand_in = RenamingTail()
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)
    return stand_in


def _files(cfg) -> list[str]:
    return sorted(path.name for path in _staged(cfg).iterdir() if path.is_file())


def _queued_tail(tail: Tail) -> list[list[str]]:
    """Every command of the tail or the landing the stand in was given."""
    return [
        argv
        for argv in tail.calls
        if argv[:1] in (["tag"], ["analyze"])
        or ("name" in argv and "apply" in argv)
        or argv[:2] == ["intake", "land"]
    ]


def _refused_beside(envelope: dict, step: str) -> dict:
    cause = envelope["cause"]
    assert cause["reason"] == "refused-by-policy", cause
    assert "cli.sync_land" in cause["origin"], cause
    assert _summary(envelope)["stopped_at"] == step
    return cause


def _pass(monkeypatch, *ids: str, name: str = "Warmup", playlist: str = "pl-a") -> tuple[int, dict]:
    bind_playlists(monkeypatch, (_playlist(playlist, name), _rows(*ids)))
    return drive(["sync", "land"])


def _landable(script) -> None:
    for n in ISRC:
        script.landings.setdefault(n, Landing())


# ═══════════════════════════════════════════════════════════════════════════
# 1. A label go's download waiting at its landing's gate
# ═══════════════════════════════════════════════════════════════════════════


def test_a_label_gos_download_at_its_landings_gate_renamed_refuses_the_pass_before_it_downloads(
    full, monkeypatch, renaming
):
    """The card's scenario: the go ran its tail, which renamed its tracks, and
    stopped at its landing's gate. A sync pass then downloaded and landed them
    under its own pass. Now it refuses before its download, naming the go and
    the command that lands it."""
    cfg, script = full
    one_release_answered(monkeypatch, script)
    go_run, code, envelope = approved_go()
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    (go_job,) = our_jobs()
    held = _files(cfg)
    assert held and all(name.startswith("Artist - ") for name in held), held
    renaming.calls.clear()
    _landable(script)
    script.fetched.clear()

    code, envelope = _pass(monkeypatch, "101")

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = _refused_beside(envelope, sync_land.DOWNLOAD)
    assert [request.key for request in script.fetched] == [], "the pass downloaded beside the go"
    assert _queued_tail(renaming) == [], "the tail ran over the go's tracks"
    assert _files(cfg) == held
    (waiting,) = cause["detail"]["waiting"]
    assert waiting["job"] == go_job.job_id and waiting["run"] == go_run
    assert waiting["tracks"] == 0
    assert cause["detail"]["unnamed"] == held
    command = f"crate --run {go_run} label sync --go"
    assert any(command in step for step in cause["remediation"]["steps"]), cause
    assert cause["remediation"]["steps"][-1].endswith(
        f"continue the pass with: crate sync land --pass-run {_summary(envelope)['pass_run']}"
    )


def test_a_gos_download_arriving_while_the_pass_downloads_refuses_its_tail(
    machine, monkeypatch, tail, tmp_path
):
    """Read again before the tail: what arrived during the download is beside
    the pass too, and the tail is not run over it."""
    cfg, script = machine
    real = sync_land._download
    other: list[str] = []

    def and_another(report, listed, cfg_):
        done = real(report, listed, cfg_)
        other.append(downloaded_by_hand(script, tmp_path, "x1"))
        return done

    monkeypatch.setattr(sync_land, "_download", and_another)
    _account(monkeypatch, script, "101")

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = _refused_beside(envelope, sync_land.TAG)
    assert [one["job"] for one in cause["detail"]["waiting"]] == other
    assert _queued_tail(tail) == [], "the tail ran over another download"
    assert _check(envelope, "download")["status"] == "ok"


# ═══════════════════════════════════════════════════════════════════════════
# 2. A plain download, and an earlier pass's
# ═══════════════════════════════════════════════════════════════════════════


def test_a_plain_download_beside_the_pass_refuses_naming_it(machine, monkeypatch, tail, tmp_path):
    cfg, script = machine
    plain = downloaded_by_hand(script, tmp_path, "x1")
    script.fetched.clear()
    _account(monkeypatch, script, "101")

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = _refused_beside(envelope, sync_land.DOWNLOAD)
    assert cause["detail"]["waiting"] == [
        {
            "job": plain,
            "run": None,
            "verb": "acquire.download",
            "tracks": 1,
            "pass": None,
            "pass_run": None,
        }
    ]
    assert f"move the tracks of job {plain} out of {_staged(cfg)}" in " ".join(
        cause["remediation"]["steps"]
    )
    assert script.fetched == []
    assert _queued_tail(tail) == []


def test_an_earlier_passes_unlanded_download_refuses_a_new_pass_naming_how_it_lands(
    machine, monkeypatch, tail
):
    """U212's second pass landed the first pass's tracks it also wanted under
    its own pass. They are another download's, so it refuses now, and names
    the first pass's own continue command."""
    cfg, script = machine
    _landable(script)
    code, first = _pass(monkeypatch, "101", "102")
    assert code == int(ExitCode.PENDING_HUMAN), first
    (download,) = _by_key("acquire.download")
    first_run = _summary(first)["pass_run"]
    script.fetched.clear()

    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _rows("101", "102")),
        (_playlist("pl-b", "Peak"), _rows("101", "103")),
    )
    code, second = drive(["sync", "land"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), second
    cause = _refused_beside(second, sync_land.DOWNLOAD)
    assert script.fetched == []
    assert cause["detail"]["waiting"] == [
        {
            "job": download.job_id,
            "run": None,
            "verb": "acquire.download",
            "tracks": 2,
            "pass": _summary(first)["land_name"],
            "pass_run": first_run,
        }
    ]
    assert (
        f"take the sync pass {_summary(first)['land_name']} to its landing with: "
        f"crate sync land --pass-run {first_run}"
    ) in " ".join(cause["remediation"]["steps"])


def test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass(machine, monkeypatch, renaming):
    """Sitting 55's state: the first pass's tail renamed its tracks and its
    landing's gate was never answered. No download names them, and the
    first pass, whose pass has no landing proof, is named as whose tail may
    have renamed them."""
    cfg, script = machine
    _landable(script)
    code, first = _pass(monkeypatch, "101", "102")
    assert code == int(ExitCode.PENDING_HUMAN), first
    renamed = _files(cfg)
    assert renamed == ["Artist - 101.wav", "Artist - 102.wav"]
    first_run = _summary(first)["pass_run"]

    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _rows("101", "102")),
        (_playlist("pl-b", "Peak"), _rows("103")),
    )
    code, second = drive(["sync", "land"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), second
    cause = _refused_beside(second, sync_land.DOWNLOAD)
    assert cause["detail"]["unnamed"] == renamed
    (waiting,) = cause["detail"]["waiting"]
    assert (waiting["pass_run"], waiting["tracks"]) == (first_run, 0)
    assert f"crate sync land --pass-run {first_run}" in " ".join(cause["remediation"]["steps"])


def test_a_pass_whose_landing_is_proven_is_not_named(machine, monkeypatch, renaming):
    cfg, script = machine
    _landable(script)
    code, first = _pass(monkeypatch, "101")
    assert code == int(ExitCode.PENDING_HUMAN), first
    (Path(cfg.library.root) / f"{_summary(first)['land_name']}{land_cli.INTAKE_SUFFIX}").write_text(
        "<xml/>"
    )
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _rows("101")),
        (_playlist("pl-b", "Peak"), _rows("103")),
    )

    code, second = drive(["sync", "land"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), second
    cause = _refused_beside(second, sync_land.DOWNLOAD)
    assert cause["detail"]["waiting"] == []
    assert cause["detail"]["unnamed"] == ["Artist - 101.wav"]


# ═══════════════════════════════════════════════════════════════════════════
# 3. The pass's own tracks, renamed by its own tail
# ═══════════════════════════════════════════════════════════════════════════


def _refusing_landing(tail: Tail) -> None:
    tail.landing = lambda _argv: _refused(
        Cause(
            reason="library-export-unusable",
            message="the rekordbox export could not be read",
            remediation=Remediation(remedy=Remedy.PREPARE_LIBRARY_IN_REKORDBOX),
            origin=("test",),
        )
    )


@pytest.mark.parametrize("stop", ["gate", "failed"])
def test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on(
    machine, monkeypatch, renaming, stop
):
    cfg, script = machine
    _landable(script)
    if stop == "failed":
        _refusing_landing(renaming)
    code, first = _pass(monkeypatch, "101", "102")
    assert code != int(ExitCode.REFUSED_BY_POLICY), first
    assert _files(cfg) == ["Artist - 101.wav", "Artist - 102.wav"]
    run_id = _summary(first)["pass_run"]
    renaming.landing = Tail().landing
    landings = sum(1 for argv in renaming.calls if argv[:2] == ["intake", "land"])

    code, again = drive(["sync", "land", "--pass-run", run_id])

    assert code == int(ExitCode.PENDING_HUMAN), again
    assert sum(1 for argv in renaming.calls if argv[:2] == ["intake", "land"]) == landings + 1
    assert _summary(again)["stopped_at"] == sync_land.LAND_GATE


def test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own(
    machine, monkeypatch, renaming
):
    cfg, script = machine
    _landable(script)
    code, first = _pass(monkeypatch, "101")
    assert code == int(ExitCode.PENDING_HUMAN), first
    run_id = _summary(first)["pass_run"]
    (_staged(cfg) / "Someone - Else.wav").write_bytes(b"RIFF")
    landings = sum(1 for argv in renaming.calls if argv[:2] == ["intake", "land"])

    code, again = drive(["sync", "land", "--pass-run", run_id])

    assert code == int(ExitCode.REFUSED_BY_POLICY), again
    cause = _refused_beside(again, sync_land.DOWNLOAD)
    assert cause["detail"]["unnamed"] == ["Someone - Else.wav"]
    assert sum(1 for argv in renaming.calls if argv[:2] == ["intake", "land"]) == landings


def test_a_file_the_passes_tail_left_and_then_changed_is_not_its_own(
    machine, monkeypatch, renaming
):
    """The record is the identity the landing's digest reads, not the name."""
    cfg, script = machine
    _landable(script)
    code, first = _pass(monkeypatch, "101")
    assert code == int(ExitCode.PENDING_HUMAN), first
    run_id = _summary(first)["pass_run"]
    (_staged(cfg) / "Artist - 101.wav").write_bytes(b"something else entirely")

    code, again = drive(["sync", "land", "--pass-run", run_id])

    assert code == int(ExitCode.REFUSED_BY_POLICY), again
    assert _refused_beside(again, sync_land.DOWNLOAD)["detail"]["unnamed"] == ["Artist - 101.wav"]


def test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own(
    machine, monkeypatch, renaming
):
    cfg, script = machine
    _landable(script)
    code, first = _pass(monkeypatch, "101")
    assert code == int(ExitCode.PENDING_HUMAN), first
    run_id = _summary(first)["pass_run"]
    name = _summary(first)["land_name"]
    (Path(cfg.library.root) / f"{name}{land_cli.INTAKE_SUFFIX}").write_text("<xml/>")

    code, again = drive(["sync", "land", "--pass-run", run_id])

    assert code == int(ExitCode.REFUSED_BY_POLICY), again
    assert _refused_beside(again, sync_land.DOWNLOAD)["detail"]["unnamed"] == ["Artist - 101.wav"]


def test_the_record_is_kept_under_the_pass_at_each_tail_stop(machine, monkeypatch, renaming):
    cfg, script = machine
    _landable(script)
    code, first = _pass(monkeypatch, "101")
    assert code == int(ExitCode.PENDING_HUMAN), first
    record = staged_reading.pass_record(cfg, _summary(first)["land_name"])
    kept = staged_reading.kept(record)
    assert {name for name, _size, _mtime in kept} == {"Artist - 101.wav"}


def test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses(
    machine, monkeypatch, renaming
):
    cfg, script = machine
    _landable(script)
    real_keep = staged_reading.keep

    def unwritable(*_args, **_kwargs):
        raise OSError("read-only file system")

    monkeypatch.setattr(staged_reading, "keep", unwritable)
    code, first = _pass(monkeypatch, "101")

    assert code == int(ExitCode.PENDING_HUMAN), first
    (warning,) = [one for one in first["warnings"] if one["code"] == sync_land.UNRECORDED_WARNING]
    assert "read-only file system" in warning["message"]
    monkeypatch.setattr(staged_reading, "keep", real_keep)

    code, again = drive(["sync", "land", "--pass-run", _summary(first)["pass_run"]])

    assert code == int(ExitCode.REFUSED_BY_POLICY), again
    cause = _refused_beside(again, sync_land.DOWNLOAD)
    assert cause["detail"]["unnamed"] == ["Artist - 101.wav"]
    # REVIEW ROUND ONE, finding 5: the way on names the landing under the pass.
    name = _summary(first)["land_name"]
    assert (
        f"if the track(s) no download names are this pass's own, renamed by its tail "
        f"and no longer known to it, land them under the pass with: crate intake land "
        f"{_staged(cfg)} --pass {name}"
    ) in cause["remediation"]["steps"]


# ═══════════════════════════════════════════════════════════════════════════
# 4. A folder or a root that cannot be read
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unreadable_staging_folder_refuses_the_pass_before_it_downloads(
    machine, monkeypatch, tail
):
    cfg, script = machine
    _staged(cfg).mkdir(parents=True, exist_ok=True)

    def unlistable(folder):
        raise PermissionError(13, "Permission denied", str(folder))

    monkeypatch.setattr(staged_reading, "folder_listing", unlistable)
    _account(monkeypatch, script, "101")

    code, envelope = drive(["sync", "land"])

    cause = envelope["cause"]
    assert cause["detail"].get("declared_reason", cause["reason"]) == "intake-list-unusable"
    assert "could not be listed" in cause["message"], cause
    assert _summary(envelope)["stopped_at"] == sync_land.DOWNLOAD
    assert script.fetched == []
    assert _queued_tail(tail) == []
    assert code != int(ExitCode.OK)


def test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks(
    machine, monkeypatch, renaming
):
    cfg, script = machine
    _landable(script)
    code, first = _pass(monkeypatch, "101")
    assert code == int(ExitCode.PENDING_HUMAN), first
    run_id = _summary(first)["pass_run"]

    def unreadable(_cfg, name):
        raise land_cli.refuse(
            "library-root-unreachable",
            f"the library root could not be read for {name}",
            origin=("intake.land",),
        )

    monkeypatch.setattr(land_cli, "pass_landed", unreadable)

    code, again = drive(["sync", "land", "--pass-run", run_id])

    assert again["cause"]["reason"] == "library-root-unreachable", again
    assert _summary(again)["stopped_at"] == sync_land.DOWNLOAD
    assert code != int(ExitCode.OK)


# ═══════════════════════════════════════════════════════════════════════════
# 5. The go reads a sync pass's download the same way
# ═══════════════════════════════════════════════════════════════════════════


def test_a_fresh_go_beside_a_sync_passes_download_names_its_continue_command(
    full, monkeypatch, tail
):
    cfg, script = full
    _landable(script)
    code, first = _pass(monkeypatch, "101")
    assert code == int(ExitCode.PENDING_HUMAN), first
    first_run = _summary(first)["pass_run"]
    one_release_answered(monkeypatch, script)

    code, envelope = drive(["label", "sync", "--go"])

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = envelope["cause"]
    (waiting,) = cause["detail"]["waiting"]
    assert waiting["pass_run"] == first_run and waiting["run"] is None
    assert f"crate sync land --pass-run {first_run}" in " ".join(cause["remediation"]["steps"])
    assert our_jobs() == []


# ═══════════════════════════════════════════════════════════════════════════
# 6. What arrives while the tail runs (review round one)
# ═══════════════════════════════════════════════════════════════════════════


class ArrivingTail(RenamingTail):
    """The renaming tail, with something arriving in the folder while ``analyze run`` runs.

    ``arrive`` runs once, inside the first driven ``analyze run``, as a second
    terminal finishing a download meanwhile would; the tail's ``name apply``
    then renames what arrived with the batch's own.
    """

    def __init__(self, arrive) -> None:
        super().__init__()
        self.arrive = arrive
        self.arrived = None

    def __call__(self, argv: list[str]) -> tuple[int, dict]:
        if argv[:2] == ["analyze", "run"] and "--job" in argv and self.arrived is None:
            self.arrived = self.arrive()
        return super().__call__(argv)


def _landings(tail: Tail) -> int:
    return sum(1 for argv in tail.calls if argv[:2] == ["intake", "land"])


def test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing(
    machine, monkeypatch, tmp_path
):
    """Review round one, finding 1: a download another process finished while
    the tail ran was renamed with the pass's own, planned into its landing and
    kept as its own. Now the landing is not planned and nothing is kept."""
    cfg, script = machine
    _landable(script)
    stand_in = ArrivingTail(lambda: downloaded_by_hand(script, tmp_path, "x1"))
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)

    code, envelope = _pass(monkeypatch, "101")

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = _refused_beside(envelope, sync_land.LAND)
    assert cause["detail"]["arrived"] == [stand_in.arrived]
    assert (cause["detail"]["before"], cause["detail"]["after"]) == (1, 2)
    assert _landings(stand_in) == 0, "the landing was planned over what arrived"
    name = _summary(envelope)["land_name"]
    assert (
        f"crate intake land {_staged(cfg)} --pass {name}" in " ".join(cause["remediation"]["steps"])
    )
    record = staged_reading.pass_record(cfg, name)
    assert not record.exists(), "the record kept what arrived as the pass's own"
    warnings = cause["detail"]["sync_land"]["warnings"]
    assert [one["code"] for one in warnings].count(sync_land.UNRECORDED_WARNING) == 1, warnings


def test_a_file_a_person_put_there_while_the_tail_ran_refuses_its_landing(
    machine, monkeypatch
):
    cfg, script = machine
    _landable(script)

    def put_there():
        (_staged(cfg) / "dropped.wav").write_bytes(b"RIFF")
        return "a person"

    stand_in = ArrivingTail(put_there)
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)

    code, envelope = _pass(monkeypatch, "101")

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = _refused_beside(envelope, sync_land.LAND)
    assert cause["detail"]["arrived"] == []
    assert (cause["detail"]["before"], cause["detail"]["after"]) == (1, 2)
    assert _landings(stand_in) == 0


def test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing(
    full, monkeypatch, tmp_path
):
    """The class one file over: the go's tail, in ``cli.label_sync``."""
    cfg, script = full
    stand_in = ArrivingTail(lambda: downloaded_by_hand(script, tmp_path, "x1"))
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)
    one_release_answered(monkeypatch, script)

    _go_run, code, envelope = approved_go()

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "refused-by-policy", cause
    assert cause["detail"]["arrived"] == [stand_in.arrived]
    assert _landings(stand_in) == 0
    (go_job,) = our_jobs()
    assert staged_reading.kept(staged_reading.go_record(cfg, go_job.job_id)) == frozenset()


# ═══════════════════════════════════════════════════════════════════════════
# 7. Whose a download is, by its list (review round one's zero rows)
# ═══════════════════════════════════════════════════════════════════════════


def _download_over(cfg, listed: str, *, key: str = "acquire.download") -> str:
    from cratekit.acquire import cli as acquire_cli
    from cratekit.core import jobs

    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key=key, payload={acquire_cli.LIST: listed}, cfg=cfg, item_ids=("1",)
        )
    return job.job_id


def test_a_passes_own_downloads_are_this_librarys_over_its_own_list_by_name(machine):
    from cratekit.core import jobs
    from tests.test_sync_land import dataclasses_replace_library

    cfg, _script = machine
    name = "2026-11-11T000000Z-abcd_synced"
    own = _download_over(cfg, f"/lists/{name}.list.json")
    _download_over(dataclasses_replace_library(cfg), f"/lists/{name}.list.json")
    _download_over(cfg, "/lists/2026-11-12T000000Z-abcd_synced.list.json")
    _download_over(cfg, f"/lists/{name}.list.json", key="acquire.fallback-fetch")

    with jobs.open_store() as store:
        assert sync_land._own_downloads(store, name, cfg) == {own}


def test_only_a_download_over_a_synced_list_is_a_passes():
    from cratekit.core import jobs

    def job(listed: str, key: str = "acquire.download") -> jobs.Job:
        return jobs.Job(
            job_id="j",
            handler_key=key,
            payload={"list": listed},
            config_fingerprint="",
            config_toml="",
            library_id="",
            state=jobs.JobState.SUCCEEDED,
            created="",
            updated="",
        )

    assert staged_reading.pass_of(job("/x/p_synced.list.json")) == "p_synced"
    assert staged_reading.pass_of(job("/x/label-sync-ab12.list.json")) is None
    assert staged_reading.pass_of(job("/x/p_synced.json")) is None
    assert staged_reading.pass_of(job("/x/p_synced.list.json", "acquire.fallback-fetch")) is None
