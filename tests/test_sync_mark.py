"""``crate sync mark``: a landed sync pass marks the playlists it finished (U82).

THE PRODUCER IS THE REAL SEQUENCE AND NOT A HAND BUILT REPORT. Every test below
drives ``crate sync all``, finishes the intake jobs it queued, and lists the
pass with ``crate intake missing --run``, so the reports the verb reads, the
name the pass goes by and the jobs that spell it are the ones the product writes. What is faked is
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
from cratekit.core import artifacts, config, jobs, locations
from cratekit.core.cause import Cause, CratekitError, Remediation
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import land_cli, missing_cli
from cratekit.modules.outbound import account as account_module
from cratekit.sync import mark_cli, marks, playlists, watermarks
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.intake.test_workers import Track
from tests.test_intake_missing import tombstone
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


def _swept_pass(monkeypatch, *listed, failing: tuple[str, ...] = ()) -> tuple[object, str]:
    """``sync all`` over ``listed``, every job finished, the pass listed. Returns
    the fake catalogue and the name the pass's list and batch share.

    A playlist named in ``failing`` has its job FAILED and never run, and the
    pass is then listed with ``--skip-failed``, which is the one way the product
    lists a pass holding a failed job.
    """
    fake = bind_playlists(monkeypatch, *listed)
    code, passed = drive(["sync", "all"])
    assert code == int(ExitCode.OK), passed
    run_id = passed["run_id"]
    for job in _playlist_jobs():
        if playlists.playlist_of(job) in failing:
            stopped = Cause(
                reason="internal-error",
                message="stopped for the test",
                remediation=Remediation(steps=("nothing",)),
                origin=("test",),
            )
            with jobs.open_store() as store:
                jobs.transition(store, job.job_id, jobs.JobState.FAILED, cause=stopped)
            continue
        code, resumed = drive(cli_jobs.argv_for(job))
        assert code == int(ExitCode.OK), resumed
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed
    extra = ["--skip-failed"] if failing else []
    code, missing = drive(["intake", "missing", "--run", run_id, *extra])
    assert code == int(ExitCode.OK), missing
    return fake, missing_cli.synced_name(run_id)


def _land(
    cfg: config.Config, name: str, *track_ids: str, named: bool = True, spelled: Path | None = None
) -> Path:
    """Put each track's file where a landing puts it, and write the intake file.

    ``named=False`` leaves the files out of the intake file, which is a track
    the library holds that this landing did not bring. ``spelled`` is another
    way to reach the library root, a link to it, and the intake file then
    spells every file through that and not through the configured root.
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
        said = path if spelled is None else spelled / path.relative_to(cfg.library.root)
        collection.append(
            f'    <TRACK TrackID="{number}" Name="{path.stem}" Artist="A" '
            f'Location="{locations.location_url(said)}"/>'
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


def test_a_library_reached_through_a_link_still_reads_its_files_as_landed(
    slim, monkeypatch, tmp_path
):
    """Row B2 of ``docs/mutation/u82-b.md`` killed nothing until this existed.

    The intake file spells every landed file through a link to the library and
    the index spells it through the configured root, which is an ordinary state
    on a volume mounted under two names. Compared as spelled, no landed file is
    found in the intake file and the screen credits the landing with nothing.
    """
    _fake, name = _swept_pass(monkeypatch, *TWO)
    bind_account(monkeypatch, outbound_fakes.FakeAccount())
    link = tmp_path / "the-same-library"
    link.symlink_to(slim.library.root, target_is_directory=True)
    xml = _land(slim, name, "101", "102", "201", spelled=link)
    assert str(link) in xml.read_text(encoding="utf-8")

    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    item = _by_id(done)["pl-a"]
    assert (item["landed"], item["owned"]) == (2, 0)


def test_a_track_two_playlists_share_holds_both_back_until_it_lands(slim, monkeypatch):
    """Each playlist's own reports carry the shared track, so neither is whole
    until it lands, whichever of the two the pass's list credits it to."""
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


def test_a_playlist_the_account_no_longer_lists_is_said_and_not_planned(slim, monkeypatch):
    """Nothing could rename it, so a plan that showed it as a rename would be a
    declared write the run never performs."""
    fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    fake.account = [_playlist("pl-b", "Peak")]

    code, shown = _mark(xml)
    assert code == int(ExitCode.DECISION_REQUIRED), shown
    context = shown["cause"]["detail"]["shown"]
    assert context["renamed on the account"] == ["Peak -> DOWNLOADED Peak"]
    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    gone = _by_id(done)["pl-a"]
    assert (gone["action"], gone["reason"]) == ("skip", "not-listed")
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]


def test_a_playlist_whose_job_failed_is_said_and_not_planned(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO, failing=("pl-a",))
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    failed = _by_id(done)["pl-a"]
    assert (failed["action"], failed["reason"]) == ("skip", "job-unfinished")
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]


def test_an_answer_to_one_plan_does_not_carry_out_another(slim, monkeypatch):
    """The intake file is untouched, so only the plan's own marks can make the
    answer stale. ``102`` arrives after the answer, ``pl-a`` becomes whole, and
    a rename nobody was shown must not ride in on the answer to the smaller plan."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "201")
    code, refused = _mark(xml)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["renamed on the account"] == [
        "Peak -> DOWNLOADED Peak"
    ]
    run_id = refused["run_id"]
    code, _ = drive(["run", "decide", run_id, CONFIRM, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK)

    music = Path(slim.library.root) / slim.library.music_dir
    (music / "Artist 102 - Title 102.flac").write_bytes(b"")
    code, stale = drive(["--run", run_id, "sync", "mark", "--xml", str(xml)])
    assert code != int(ExitCode.OK), stale
    assert account.renamed == []


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
    assert code == int(ExitCode.INTERNAL), failed
    cause = failed["cause"]
    # THE FAKE RAISES A BARE RuntimeError, which no adapter should, so it is
    # reported as this build's defect and not as a provider to wait out.
    assert cause["reason"] == "internal-error"
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


def test_a_refusal_the_account_raised_keeps_its_reason_and_names_what_was_marked(
    slim, monkeypatch
):
    """What the real adapter raises: its provider's failure, already a cause."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    rename = account.rename_playlist

    def refusing(playlist_id: str, title: str) -> None:
        if playlist_id == "pl-b":
            raise account_module.provider_failure(TimeoutError("slow"), "rename a playlist")
        rename(playlist_id, title)

    monkeypatch.setattr(account, "rename_playlist", refusing)
    code, failed = _answered(xml)
    assert code != int(ExitCode.OK), failed
    cause = failed["cause"]
    assert cause["reason"] == "unavailable-transient"
    assert cause["detail"]["marked"] == ["pl-a"] and cause["detail"]["unmarked"] == ["pl-b"]
    assert "Warmup" in cause["message"]


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


def test_a_track_the_pass_offered_for_review_holds_its_playlist_back(slim, monkeypatch):
    """The track no manifest row ever stood for, which is why the reports are
    read. The library holds another version of ``102``, so the pass OFFERS it
    and never lists it for download, and everything that was listed lands."""
    music = Path(slim.library.root) / slim.library.music_dir
    (music / "Artist 102 - Title 102 (Someone Remix).flac").write_bytes(b"")
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "201")
    manifest = Path(slim.paths.download_staging) / missing_cli.LISTS_DIR / f"{name}.manifest.json"
    assert '"102"' not in manifest.read_text(encoding="utf-8"), "the offered track was listed"

    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]
    held_back = _by_id(done)["pl-a"]
    assert (held_back["action"], held_back["reason"]) == ("skip", "rows-outstanding")
    assert [row["id"] for row in held_back["outstanding"]] == ["102"]


def test_the_pass_is_decided_without_its_manifest(slim, monkeypatch):
    """The manifest is another pass's as easily as this one's, and a pass whose
    every missing track was handed on has none, so nothing here reads it."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "201")
    (Path(slim.paths.download_staging) / missing_cli.LISTS_DIR / f"{name}.manifest.json").unlink()
    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]
    assert _by_id(done)["pl-a"]["reason"] == "rows-outstanding"


def test_a_track_deleted_on_purpose_since_the_pass_is_not_owed(slim, monkeypatch):
    """The pass never owes a suppressed track, and a tombstone recorded after it
    is the same decision made later, so it does not hold the playlist for ever."""
    # A TRACK THAT RESEMBLES NOTHING ELSE HERE. The engine asks the tombstones
    # last, immediately before it calls a track missing, so a title close to
    # one the library holds is a question for a person and never reaches them.
    _fake, name = _swept_pass(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), [*_tracks("101"), Track("102", "Nova Reef", "Tide")]),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "201")
    code, held = _mark(xml)
    assert code == int(ExitCode.DECISION_REQUIRED), held
    assert len(held["cause"]["detail"]["shown"]["left alone"]) == 1, "it was never owed"

    tombstone(slim, "Nova Reef", "Tide")
    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    item = _by_id(done)["pl-a"]
    assert item["action"] == "marked", item.get("why")
    assert (item["landed"], item["suppressed"]) == (1, 1)


def test_a_playlist_whose_reports_cannot_be_read_is_left_alone(slim, monkeypatch):
    """Unread is not nothing owed."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    (job,) = [job for job in _playlist_jobs() if playlists.playlist_of(job) == "pl-a"]
    with jobs.open_store() as store:
        item = jobs.items(store, job.job_id)[0]
    artifacts.final_path(
        intake_cli.ARTIFACTS, jobs.frozen_config(job), job.job_id, item.ordinal
    ).write_text("{", encoding="utf-8")

    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]
    assert _by_id(done)["pl-a"]["reason"] == "reports-unreadable"


def test_the_library_is_not_walked_when_no_playlist_is_left_to_settle(slim, monkeypatch):
    """A second run over a marked pass decides every playlist by its name."""
    fake, name = _swept_pass(monkeypatch, *TWO)
    bind_account(monkeypatch, outbound_fakes.FakeAccount())
    xml = _land(slim, name, "101", "102", "201")
    fake.account = [_playlist("pl-a", "DOWNLOADED Warmup"), _playlist("pl-b", "DOWNLOADED Peak")]

    def walked(_cfg):
        raise AssertionError("the library was walked with nothing to resolve")

    monkeypatch.setattr(mark_cli.match_cli, "library_view", walked)
    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert {item["reason"] for item in done["data"]["items"]} == {"already-marked"}


def test_a_location_on_another_host_is_passed_over_and_never_a_traceback(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    body = xml.read_bytes().replace(
        b"  </COLLECTION>",
        b'    <TRACK TrackID="99" Name="Far" Artist="A" '
        b'Location="file://elsewhere.invalid/Music/Far.flac"/>\r\n  </COLLECTION>',
    )
    xml.write_bytes(body)
    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert len(account.renamed) == 2


def test_a_playlist_that_changes_between_the_plan_and_the_rename_is_said(slim, monkeypatch):
    """Through the verb, which is where the skip is reported. The answered run
    lists the account once to plan and once more to recheck, and the account
    moves between those two reads, so the plan still matches the answer and the
    recheck is what catches it."""
    fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    code, refused = _mark(xml)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, _ = drive(["run", "decide", run_id, CONFIRM, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK)

    planned_at = fake.account_listings + 1
    listing = type(fake).account_playlists

    def moving(self):
        listed = listing(self)
        if self.account_listings > planned_at:
            return (_playlist("pl-a", "Warmup (edited)"), _playlist("pl-b", "Peak"))
        return listed

    monkeypatch.setattr(type(fake), "account_playlists", moving)
    code, done = drive(["--run", run_id, "sync", "mark", "--xml", str(xml)])
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]
    skipped = _by_id(done)["pl-a"]
    assert (skipped["action"], skipped["reason"]) == ("skip", "changed-since-plan")
    assert [w["code"] for w in done["warnings"]] == ["sync-mark-changed-since-plan"]
    assert done["data"]["totals"] == {"count": 2, "marked": 1, "skip": 1}


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
