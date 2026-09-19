"""``crate sync mark``: a landed sync pass marks the playlists it finished (U82).

THE PRODUCER IS THE REAL SEQUENCE AND NOT A HAND BUILT MANIFEST. Every test
below drives ``crate sync all``, finishes the intake jobs it queued, and lists
the pass with ``crate intake missing --run``, so the manifest, its name and the
jobs the verb compares it with are the ones the product writes. What is faked is
the two provider seams, the catalogue and the account, and the landing itself:
the landed files are written where ``intake land`` puts them and the intake file
is a real export shape naming them, because a real landing needs a Fresh Export
and its own gate, and that verb is driven in ``tests/test_intake_land.py``.
"""

from __future__ import annotations

import errno
import os
import stat as stat_module
from pathlib import Path

import pytest

from cratekit.cli import jobs as cli_jobs
from cratekit.cli import registry
from cratekit.core import config, jobs, locations
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import land_cli, missing_cli
from cratekit.sync import marks, playlists, watermarks
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.test_outbound_workers import bind as bind_account
from tests.test_sync_all import _playlist, _playlist_jobs, _tracks, bind_playlists
from tests.test_sync_all import slim as slim  # noqa: PLC0414 - the fixture, re-exported
from tests.xml_fixtures import _xml_doc

CONFIRM = "sync.mark.confirm"


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    yield
    intake_cli.reset_cache()


# ═══════════════════════════════════════════════════════════════════════════
# The sequence a mark comes after
# ═══════════════════════════════════════════════════════════════════════════


def _swept_pass(monkeypatch, *listed) -> tuple[object, str]:
    """``sync all`` over ``listed``, every job finished, the pass listed. Returns
    the fake catalogue and the name the pass's list and batch share."""
    fake = bind_playlists(monkeypatch, *listed)
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    run_id = passed["run_id"]
    for job in _playlist_jobs():
        code, resumed = drive(cli_jobs.argv_for(job))
        assert code == int(ExitCode.OK), resumed
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    code, missing = drive(["intake", "missing", "--run", run_id])
    assert code == int(ExitCode.OK), missing
    return fake, missing_cli.synced_name(run_id)


def _land(cfg: config.Config, name: str, *track_ids: str, named: bool = True) -> Path:
    """Put each track's file where a landing puts it, and write the intake file.

    ``named=False`` leaves the files out of the intake file, which is a track
    the library holds that this landing did not bring.
    """
    batch = Path(cfg.library.root) / cfg.library.music_dir / name
    batch.mkdir(parents=True, exist_ok=True)
    collection = ['  <COLLECTION Entries="0">'.replace("0", str(len(track_ids) + 1))]
    # One track that is nobody's, so an intake file naming none of the wanted
    # files is still an intake file and the verb reaches its comparison.
    elsewhere = batch / "Somebody Else - Another Tune.flac"
    elsewhere.write_bytes(b"")
    paths = [elsewhere]
    for track_id in track_ids:
        path = batch / f"Artist {track_id} - Title {track_id}.flac"
        path.write_bytes(b"")
        if named:
            paths.append(path)
    for number, path in enumerate(paths, start=1):
        collection.append(
            f'    <TRACK TrackID="{number}" Name="{path.stem}" Artist="A" '
            f'Location="{locations.location_url(path)}"/>'
        )
    collection.append("  </COLLECTION>")
    xml = land_cli.intake_file(cfg, name)
    xml.write_bytes(_xml_doc(collection=collection, root_children=[]))
    return xml


def _mark(xml: Path, *extra: str) -> tuple[int, dict]:
    return drive(["sync", "mark", "--xml", str(xml), *extra])


def _answered(xml: Path, option: str = "apply") -> tuple[int, dict]:
    """R34's two acts on the mark's own gate, then the run that carries them out."""
    code, refused = _mark(xml)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == CONFIRM
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, CONFIRM, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, "sync", "mark", "--xml", str(xml)])


def _by_id(envelope: dict) -> dict[str, dict]:
    return {item["id"]: item for item in envelope["data"]["items"]}


TWO = (
    (_playlist("pl-a", "Warmup"), _tracks("101", "102")),
    (_playlist("pl-b", "Peak"), _tracks("201")),
)


# ═══════════════════════════════════════════════════════════════════════════
# 1. The declaration
# ═══════════════════════════════════════════════════════════════════════════


def test_the_verb_declares_one_remote_write_behind_an_explicit_gate():
    entry = registry.entry("sync.mark")
    assert entry.writes == frozenset({"remote"}) and entry.destructive
    (gate,) = entry.gates
    assert (gate.name, gate.options, gate.explicit) == (CONFIRM, ("apply", "abort"), True)
    assert gate.digest_source == "plan"


# ═══════════════════════════════════════════════════════════════════════════
# 2. The file check reads the path once (R-398)
# ═══════════════════════════════════════════════════════════════════════════


def test_the_file_check_makes_one_stat_and_refuses_whatever_it_raises(tmp_path, monkeypatch):
    """The window R-398 recorded, closed by there being no second read to race.

    ``Path.is_file`` and ``Path.stat`` both arrive at ``os.stat``, so counting
    that one function counts every read of the path, and a check that went back
    to two would count two.
    """
    output = tmp_path / "pass_inboxed.xml"
    output.write_text("<COLLECTION/>", encoding="utf-8")
    real = os.stat
    calls: list[str] = []

    def counted(path, *args, **kwargs):
        calls.append(str(path))
        return real(path, *args, **kwargs)

    monkeypatch.setattr(os, "stat", counted)
    seen = marks.require_output(output)
    assert calls == [str(output)], calls
    assert seen.st_size == len("<COLLECTION/>")

    def gone(path, *args, **kwargs):
        raise FileNotFoundError(errno.ENOENT, "No such file or directory", str(path))

    monkeypatch.setattr(os, "stat", gone)
    with pytest.raises(CratekitError) as absent:
        marks.apply_deferred((), local_output=output, recheck=lambda _: True, apply=lambda _: None)
    assert absent.value.cause.reason == "sync-marks-blocked"

    def dead_mount(path, *args, **kwargs):
        raise OSError(errno.EIO, "Input/output error", str(path))

    monkeypatch.setattr(os, "stat", dead_mount)
    with pytest.raises(CratekitError) as unreadable:
        marks.require_output(output)
    assert unreadable.value.cause.reason == "sync-marks-blocked"
    assert "Input/output error" in unreadable.value.cause.message

    # A PERMISSION IS STILL A DECLARED REFUSAL, under the slug ``core.cause``
    # gives every refusal whose cause chain holds one, because that slug
    # carries the remedy that works. What it never is, is a bare OSError.
    def denied(path, *args, **kwargs):
        raise PermissionError(errno.EACCES, "Permission denied", str(path))

    monkeypatch.setattr(os, "stat", denied)
    with pytest.raises(CratekitError) as refused:
        marks.require_output(output)
    assert refused.value.cause.reason == "path-permission-denied"


def test_a_folder_and_an_empty_file_are_not_an_importable_file(tmp_path):
    folder = tmp_path / "pass_inboxed.xml"
    folder.mkdir()
    assert stat_module.S_ISDIR(folder.stat().st_mode)
    with pytest.raises(CratekitError) as not_a_file:
        marks.require_output(folder)
    assert not_a_file.value.cause.reason == "sync-marks-blocked"
    empty = tmp_path / "empty_inboxed.xml"
    empty.write_bytes(b"")
    with pytest.raises(CratekitError) as nothing:
        marks.require_output(empty)
    assert nothing.value.cause.reason == "sync-marks-blocked"


def test_a_missing_intake_file_refuses_the_verb_before_anything_is_listed(slim, monkeypatch):
    fake = bind_playlists(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    listings = fake.account_listings
    code, refused = _mark(Path(slim.library.root) / "no-such_synced_inboxed.xml")
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "sync-marks-blocked"
    assert fake.account_listings == listings, "the account was listed before the file check"
    assert account.renamed == []


# ═══════════════════════════════════════════════════════════════════════════
# 3. Which playlists a landed file finishes
# ═══════════════════════════════════════════════════════════════════════════


def test_a_landed_pass_marks_its_playlists_only_after_the_answer(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")

    code, refused = _mark(xml)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert account.renamed == [], "a rename landed before the gate was answered"

    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert sorted(account.renamed) == [
        ("pl-a", "DOWNLOADED Warmup"),
        ("pl-b", "DOWNLOADED Peak"),
    ]
    items = _by_id(done)
    assert {key: item["action"] for key, item in items.items()} == {
        "pl-a": "marked",
        "pl-b": "marked",
    }
    assert items["pl-a"]["landed"] == 2 and items["pl-a"]["owned"] == 0
    assert done["data"]["totals"] == {"count": 2, "marked": 2, "skip": 0}


def test_a_playlist_with_one_row_not_landed_is_not_marked(slim, monkeypatch):
    """The brief's fourth scenario. ``102`` never arrived, so ``pl-a`` is left
    alone with the track named, and ``pl-b``, which is whole, is still marked."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "201")

    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]
    held_back = _by_id(done)["pl-a"]
    assert (held_back["action"], held_back["reason"]) == ("skip", "rows-outstanding")
    assert [row["id"] for row in held_back["outstanding"]] == ["102"]
    assert "Artist 102 - Title 102" in held_back["why"]


def test_a_row_the_library_holds_and_the_file_does_not_name_is_owned(slim, monkeypatch):
    """Owned counts as finished, and is said apart from landed."""
    _fake, name = _swept_pass(monkeypatch, (_playlist("pl-a", "Warmup"), _tracks("101", "102")))
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101")
    (Path(slim.library.root) / slim.library.music_dir / "Artist 102 - Title 102.flac").write_bytes(b"")

    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    item = _by_id(done)["pl-a"]
    assert (item["action"], item["landed"], item["owned"]) == ("marked", 1, 1)


def test_a_track_two_playlists_share_holds_both_back_until_it_lands(slim, monkeypatch):
    """``source_refs`` is read, and not only the first asker's ``source_ref``."""
    _fake, name = _swept_pass(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101", "900")),
        (_playlist("pl-b", "Peak"), _tracks("201", "900")),
    )
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "201")

    code, shown = _mark(xml)
    assert code == int(ExitCode.DECISION_REQUIRED), shown
    context = shown["cause"]["detail"]["shown"]
    assert context["renamed on the account"] == []
    assert len(context["left alone"]) == 2
    assert account.renamed == []


def test_an_already_prefixed_playlist_is_skipped(slim, monkeypatch):
    """The brief's second scenario, second half. The account renamed it between
    the pass and the mark, which is what the source system's own sweep does."""
    fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    fake.account = [_playlist("pl-a", "DOWNLOADED Warmup"), _playlist("pl-b", "Peak")]

    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]
    skipped = _by_id(done)["pl-a"]
    assert (skipped["action"], skipped["reason"]) == ("skip", "already-marked")


def test_a_playlist_renamed_after_the_plan_was_shown_is_skipped_and_said(slim, monkeypatch):
    """The brief's second scenario, first half: a stale recheck skips.

    The plan is taken and answered against one listing, and the account changes
    before the run that carries the answer out. That run plans against the new
    name, so the digest moves and the answer is refused as stale, which is the
    gate doing the recheck's job one step earlier. The engine's own recheck is
    driven below it, through ``mark_swept`` with a listing that moves between
    the sweep and the rename.
    """
    fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")

    with jobs.open_store() as store:
        sweep = playlists.marking_sweep(
            store, slim, fake, handler_key=registry.entry("intake.playlist").handler_key
        )
    fake.account = [_playlist("pl-a", "Warmup (edited)"), _playlist("pl-b", "Peak")]
    marked = playlists.mark_swept(
        sweep, fake, account, local_output=xml, only=frozenset({"pl-a", "pl-b"})
    )
    assert marked == ("pl-b",)
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]


def test_only_narrows_the_pending_set_and_an_empty_set_is_nothing(slim, monkeypatch):
    fake, name = _swept_pass(monkeypatch, *TWO)
    xml = _land(slim, name, "101", "102", "201")
    with jobs.open_store() as store:
        sweep = playlists.marking_sweep(
            store, slim, fake, handler_key=registry.entry("intake.playlist").handler_key
        )
    every = [mark.target_id for mark in playlists.pending_marks(sweep)]
    assert every == ["pl-a", "pl-b"]
    only_a = playlists.pending_marks(sweep, only=frozenset({"pl-a", "pl-never-recorded"}))
    assert [mark.target_id for mark in only_a] == ["pl-a"]
    assert playlists.pending_marks(sweep, only=frozenset()) == ()
    account = outbound_fakes.FakeAccount()
    assert playlists.mark_swept(sweep, fake, account, local_output=xml, only=frozenset()) == ()
    assert account.renamed == []


def test_the_mark_reads_the_cursor_and_never_writes_it(slim, monkeypatch):
    """Out of scope by the brief, so held: no verb run here moves the cursor."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    bind_account(monkeypatch, outbound_fakes.FakeAccount())
    xml = _land(slim, name, "101", "102", "201")
    before = watermarks.WatermarkStore(slim).read(playlists.SOURCE_ID)
    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert watermarks.WatermarkStore(slim).read(playlists.SOURCE_ID) == before


# ═══════════════════════════════════════════════════════════════════════════
# 4. A failure part way
# ═══════════════════════════════════════════════════════════════════════════


def test_a_partial_failure_names_what_was_marked(slim, monkeypatch):
    """The brief's third scenario. ``pl-a`` is renamed, ``pl-b``'s rename raises,
    and the refusal says which is which rather than losing the first."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount(fail_on={"pl-b"})
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")

    code, failed = _answered(xml)
    assert code != int(ExitCode.OK), failed
    cause = failed["cause"]
    assert cause["detail"]["marked"] == ["pl-a"]
    assert cause["detail"]["unmarked"] == ["pl-b"]
    assert "Warmup" in cause["message"] and "stay marked" in cause["message"]
    assert account.renamed == [("pl-a", "DOWNLOADED Warmup")]

    # The next run sees the prefix the first one left and offers only the rest.
    _fake.account = [_playlist("pl-a", "DOWNLOADED Warmup"), _playlist("pl-b", "Peak")]
    account.fail_on = frozenset()
    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert account.renamed[-1] == ("pl-b", "DOWNLOADED Peak")
    assert len(account.renamed) == 2


def test_a_failure_before_any_rename_says_nothing_was_marked(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount(fail_on={"pl-a"})
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    code, failed = _answered(xml)
    assert code != int(ExitCode.OK), failed
    assert failed["cause"]["detail"]["marked"] == []
    assert "no playlist was marked" in failed["cause"]["message"]


# ═══════════════════════════════════════════════════════════════════════════
# 5. What the verb refuses to guess
# ═══════════════════════════════════════════════════════════════════════════


def test_a_file_not_named_as_an_intake_file_refuses(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    bind_account(monkeypatch, outbound_fakes.FakeAccount())
    xml = _land(slim, name, "101", "102", "201")
    renamed = xml.with_name("collection.xml")
    xml.rename(renamed)
    code, refused = _mark(renamed)
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "sync-marks-blocked"


def test_an_intake_file_of_no_pass_is_a_gated_plan_of_nothing(slim, monkeypatch):
    """Decided before the manifest, the listing or a credential is touched, so
    the catalogue here is one that fails the test if it is asked anything."""
    fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    stranger = xml.with_name(f"2020-01-01T000000Z-zzzz_synced{land_cli.INTAKE_SUFFIX}")
    xml.rename(stranger)
    listings = fake.account_listings

    code, done = _answered(stranger)
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert done["data"]["items"] == []
    assert [warning["code"] for warning in done["warnings"]] == ["sync-mark-no-pass"]
    assert fake.account_listings == listings, "the account was listed for a file of no pass"
    assert account.renamed == []


def test_a_missing_manifest_refuses_and_never_reads_as_nothing_owed(slim, monkeypatch):
    """Absence is not evidence of absence. With no manifest every playlist would
    have no rows, and no rows is what a finished playlist looks like."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    manifest = Path(slim.paths.download_staging) / missing_cli.LISTS_DIR / f"{name}.manifest.json"
    manifest.unlink()
    code, refused = _mark(xml)
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "sync-marks-blocked"
    assert account.renamed == []


def test_an_abort_renames_nothing(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    code, done = _answered(xml, option="abort")
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert account.renamed == []


def test_an_answer_is_stale_once_the_intake_file_is_rewritten(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    code, refused = _mark(xml)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, _ = drive(["run", "decide", run_id, CONFIRM, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK)
    xml.write_bytes(xml.read_bytes() + b"\r\n<!-- landed again -->\r\n")
    code, stale = drive(["--run", run_id, "sync", "mark", "--xml", str(xml)])
    assert code != int(ExitCode.OK), stale
    assert account.renamed == []
