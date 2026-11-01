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
from datetime import date
from pathlib import Path

import pytest

from cratekit.cli import jobs as cli_jobs
from cratekit.cli import registry
from cratekit.core import (
    active_taxonomy,
    artifacts,
    config,
    jobs,
    locations,
    session,
    tree_registry,
)
from cratekit.core.cause import Cause, CratekitError, Remediation
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import land_cli, missing_cli, native
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


def test_the_label_batch_debris_is_said_and_never_renamed(slim, monkeypatch):
    """R-361, the renaming path. A pass no longer queues a ` LIBRARY` name, so
    the job here is queued the way the fourth sitting's eleven were, before the
    rule existed, by lifting the rule for the pass alone. Its job succeeds and
    its tracks land, and the mark still leaves the source system's throwaway
    alone, with the reason spelled the way the pass spells it."""
    with pytest.MonkeyPatch.context() as before_the_rule:
        before_the_rule.setattr(playlists, "is_library_debris", lambda name: False)
        fake, name = _swept_pass(
            monkeypatch,
            (_playlist("pl-a", "Sol Selectas LIBRARY"), _tracks("101", "102")),
            (_playlist("pl-b", "Peak"), _tracks("201")),
        )
    assert playlists.is_library_debris("Sol Selectas LIBRARY"), "the rule did not come back"
    assert {playlists.playlist_of(job) for job in _playlist_jobs()} == {"pl-a", "pl-b"}
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")

    code, shown = _mark(xml)
    assert code == int(ExitCode.DECISION_REQUIRED), shown
    context = shown["cause"]["detail"]["shown"]
    assert context["renamed on the account"] == ["Peak -> DOWNLOADED Peak"]
    code, done = _answered(xml)
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]
    debris = _by_id(done)["pl-a"]
    assert (debris["action"], debris["reason"]) == ("skip", "label-debris")
    assert "label run debris" in debris["why"]
    assert "pl-a" not in [mark.target_id for mark in playlists.pending_marks(
        playlists.Sweep(listed=tuple(fake.account), recorded=frozenset({"pl-a", "pl-b"}))
    )]


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


# ═══════════════════════════════════════════════════════════════════════════
# R-777. A pass landed on a database native intake tree, named with --pass
# ═══════════════════════════════════════════════════════════════════════════


def _cut_over_intake(cfg: config.Config) -> str:
    """Record the intake tree database native. Only the mode is read here."""
    intake = active_taxonomy.load(cfg).intake.id
    tree_registry.write(
        cfg,
        tree_registry.Registry().with_record(
            tree_registry.TreeRecord(
                tree_id=intake,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=date(2026, 10, 7),
                root_id="900",
                source=tree_registry.DerivationSource.TAXONOMY,
            )
        ),
    )
    return intake


def _record_landing(
    cfg: config.Config,
    name: str,
    *,
    state: session.SessionState = session.SessionState.CLOSED,
    source: session.SourceState = session.SourceState.COMMITTED,
    stamp: str = "120000",
) -> str:
    """The session record a native landing given ``--pass name`` commits."""
    started = f"2026-10-07T{stamp[:2]}:{stamp[2:4]}:{stamp[4:]}+00:00"
    record = session.SessionRecord(
        session_id=f"20261007T{stamp}-landing",
        workflow=native.WORKFLOW,
        started=started,
        state=state,
        sources={active_taxonomy.load(cfg).intake.id: str(source)},
        ended=started,
        detail={native.PASS_KEY: name},
    )
    session.write_record(record, cfg)
    return record.session_id


def _hold(cfg: config.Config, *track_ids: str) -> None:
    """Put each track's file in the music folder the way a native landing does,
    with no intake file written."""
    batch = Path(cfg.library.root) / cfg.library.music_dir / "2026-10-07 Tidal playlists"
    batch.mkdir(parents=True, exist_ok=True)
    for track_id in track_ids:
        (batch / f"Artist {track_id} - Title {track_id}.flac").write_bytes(b"")


def _mark_pass(name: str, *extra: str) -> tuple[int, dict]:
    return drive(["sync", "mark", "--pass", name, *extra])


def _answered_pass(name: str, option: str = "apply") -> tuple[int, dict]:
    code, refused = _mark_pass(name)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, CONFIRM, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, "sync", "mark", "--pass", name])


def test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer(
    slim, monkeypatch
):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    tree = _cut_over_intake(slim)
    _hold(slim, "101", "102", "201")
    _record_landing(slim, name)

    code, refused = _mark_pass(name)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert account.renamed == [], "a rename landed before the gate was answered"
    shown = refused["cause"]["detail"]["shown"]
    assert shown["pass"] == f"{name}, landed on the database native {tree!r} tree"
    assert "intake file" not in shown

    code, done = _answered_pass(name)
    assert code == int(ExitCode.OK), done
    assert sorted(account.renamed) == [
        ("pl-a", "DOWNLOADED Warmup"),
        ("pl-b", "DOWNLOADED Peak"),
    ]
    item = _by_id(done)["pl-a"]
    # NO FILE SAYS WHICH LANDING BROUGHT A TRACK, so each one held is owned.
    assert (item["action"], item["landed"], item["owned"]) == ("marked", 0, 2)


def test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    _cut_over_intake(slim)
    _hold(slim, "101", "201")
    _record_landing(slim, name)

    code, done = _answered_pass(name)
    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]
    held_back = _by_id(done)["pl-a"]
    assert (held_back["action"], held_back["reason"]) == ("skip", "rows-outstanding")
    assert [row["id"] for row in held_back["outstanding"]] == ["102"]


def test_a_pass_named_on_a_tree_still_on_the_bridge_is_refused_naming_the_file(
    slim, monkeypatch
):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    _hold(slim, "101", "102", "201")

    code, refused = _mark_pass(name)
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "sync-marks-blocked"
    assert "--xml" in " ".join(refused["cause"]["remediation"]["steps"])
    assert account.renamed == []


def test_the_file_and_the_pass_are_one_or_the_other(slim, tmp_path):
    xml = tmp_path / "x_inboxed.xml"
    xml.write_bytes(b"<x/>")
    code, _ = drive(["sync", "mark", "--xml", str(xml), "--pass", "x"])
    assert code == int(ExitCode.USAGE)
    code, _ = drive(["sync", "mark"])
    assert code == int(ExitCode.USAGE)


def test_a_pass_name_no_landing_could_have_been_given_is_refused(slim, monkeypatch):
    _cut_over_intake(slim)
    code, refused = _mark_pass("../elsewhere")
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "sync-marks-blocked"
    # SAID AS A NAME NO LANDING COULD HAVE BEEN GIVEN, before any record is
    # read, and not as a pass that never landed.
    assert "not a pass name a landing could have been given" in refused["cause"]["message"]


def test_a_native_pass_of_no_jobs_is_a_gated_plan_of_nothing(slim, monkeypatch):
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    _cut_over_intake(slim)
    _record_landing(slim, "nobody_synced")
    code, done = _answered_pass("nobody_synced")
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert [warning["code"] for warning in done["warnings"]] == ["sync-mark-no-pass"]
    assert "nobody_synced" in done["warnings"][0]["message"]


def test_a_tree_put_back_on_the_bridge_after_the_plan_renames_nothing(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    _cut_over_intake(slim)
    _hold(slim, "101", "102", "201")
    _record_landing(slim, name)
    code, refused = _mark_pass(name)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, _ = drive(["run", "decide", run_id, CONFIRM, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK)

    planned = mark_cli.plan_pass(slim, pass_name=name, listing=lambda: mark_cli.listed(slim))
    tree_registry.write(slim, tree_registry.Registry())
    with pytest.raises(CratekitError) as refused_late:
        mark_cli.apply_pass(slim, planned)
    assert refused_late.value.cause.reason == "sync-marks-blocked"
    assert account.renamed == []


def test_a_native_answer_is_stale_once_another_playlist_becomes_whole(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    _cut_over_intake(slim)
    _hold(slim, "101", "201")
    _record_landing(slim, name)
    code, refused = _mark_pass(name)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, _ = drive(["run", "decide", run_id, CONFIRM, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK)
    _hold(slim, "102")
    code, stale = drive(["--run", run_id, "sync", "mark", "--pass", name])
    assert code == int(ExitCode.DECISION_STALE), stale
    assert account.renamed == []


def test_the_engine_refuses_a_mark_with_neither_proof():
    with pytest.raises(CratekitError) as nothing:
        marks.apply_deferred((), local_output=None, recheck=lambda _: True, apply=lambda _: None)
    assert nothing.value.cause.reason == "sync-marks-blocked"
    for empty in (
        marks.NativeLanding(tree_id="", pass_name="p", landings=("s",)),
        marks.NativeLanding(tree_id="inbox", pass_name="", landings=("s",)),
        marks.NativeLanding(tree_id="inbox", pass_name="p"),
    ):
        with pytest.raises(CratekitError) as unnamed:
            marks.apply_deferred(
                (), local_output=empty, recheck=lambda _: True, apply=lambda _: None
            )
        assert unnamed.value.cause.reason == "sync-marks-blocked"
    assert (
        marks.apply_deferred(
            (marks.PendingMark("pl-a", "rename"),),
            local_output=marks.NativeLanding(tree_id="inbox", pass_name="p", landings=("s",)),
            recheck=lambda _: True,
            apply=lambda _: None,
        )
        == ("pl-a",)
    )


@pytest.mark.parametrize(
    "landing",
    [
        None,
        {"state": session.SessionState.ABANDONED},
        {"source": session.SourceState.REFUSED},
        {"name": "ANOTHER_synced"},
    ],
    ids=["no-landing", "abandoned", "never-committed", "another-pass"],
)
def test_a_native_pass_no_closed_committed_landing_names_is_refused(
    slim, monkeypatch, landing
):
    """The finding the review drove: files on disk are not a landing. A landing
    refused after its moves leaves its files and no closed committed record."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    _cut_over_intake(slim)
    _hold(slim, "101", "102", "201")
    if landing is not None:
        _record_landing(slim, landing.pop("name", name), **landing)

    code, refused = _mark_pass(name)
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "sync-marks-blocked"
    assert "no landing" in refused["cause"]["message"]
    assert account.renamed == []


def test_an_unreachable_library_is_named_and_never_called_the_bridge(slim, monkeypatch):
    _cut_over_intake(slim)
    monkeypatch.setattr(
        mark_cli.ingest,
        "intake_medium",
        lambda cfg: mark_cli.ingest.IntakeMedium(declared=None, registry=None),
    )
    code, refused = _mark_pass("RUN_synced")
    assert code == int(ExitCode.PRECONDITION), refused
    assert "could not be reached" in refused["cause"]["message"]
    assert "bridge" not in refused["cause"]["message"]


def test_a_second_landing_of_the_pass_since_the_plan_makes_the_answer_stale(
    slim, monkeypatch
):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    _cut_over_intake(slim)
    _hold(slim, "101", "102", "201")
    _record_landing(slim, name)
    code, refused = _mark_pass(name)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, _ = drive(["run", "decide", run_id, CONFIRM, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK)
    _record_landing(slim, name, stamp="130000")
    code, stale = drive(["--run", run_id, "sync", "mark", "--pass", name])
    assert code == int(ExitCode.DECISION_STALE), stale
    assert account.renamed == []


def test_a_landing_recorded_between_the_plan_and_the_apply_renames_nothing(slim, monkeypatch):
    """The apply's reread compares the proof, not only the medium."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    _cut_over_intake(slim)
    _hold(slim, "101", "102", "201")
    _record_landing(slim, name)
    planned = mark_cli.plan_pass(slim, pass_name=name, listing=lambda: mark_cli.listed(slim))
    _record_landing(slim, name, stamp="130000")
    with pytest.raises(CratekitError) as refused:
        mark_cli.apply_pass(slim, planned)
    assert "changed since the plan" in refused.value.cause.message
    assert account.renamed == []


def test_a_plan_given_both_proofs_or_neither_is_refused(slim, tmp_path):
    with pytest.raises(CratekitError):
        mark_cli.plan_pass(slim)
    with pytest.raises(CratekitError):
        mark_cli.plan_pass(slim, tmp_path / "x_inboxed.xml", pass_name="x")


# ═══════════════════════════════════════════════════════════════════════════
# U174: --playlist narrows a pass's mark to the playlists named
# ═══════════════════════════════════════════════════════════════════════════


def test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named(slim, monkeypatch):
    """Sitting 48: one playlist of a pass marked, its sibling left as it was."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")

    code, refused = _mark(xml, "--playlist", "pl-b")
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["renamed on the account"] == ["Peak -> DOWNLOADED Peak"]
    assert shown["left alone"] == []
    assert shown[mark_cli.ONLY_SAID] == ["pl-b"]
    run_id = refused["run_id"]
    code, _ = drive(["run", "decide", run_id, CONFIRM, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK)
    code, done = drive(["--run", run_id, "sync", "mark", "--xml", str(xml), "--playlist", "pl-b"])

    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-b", "DOWNLOADED Peak")]
    assert list(_by_id(done)) == ["pl-b"]
    assert done["data"]["totals"] == {"count": 1, "marked": 1, "skip": 0}


def test_an_answer_to_the_narrowed_plan_does_not_carry_out_the_whole_pass(slim, monkeypatch):
    """The narrowing is in the digest: the run that answered for one playlist,
    re-invoked without ``--playlist``, is asked again and renames nothing."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    code, refused = _mark(xml, "--playlist", "pl-a", "--playlist", "pl-b")
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    assert drive(["run", "decide", run_id, CONFIRM, "apply", "--actor", "a-person"])[0] == 0

    code, whole = drive(["--run", run_id, "sync", "mark", "--xml", str(xml)])

    assert code != int(ExitCode.OK), whole
    assert account.renamed == []


def test_playlist_repeated_takes_each_named_and_no_playlist_is_the_whole_pass(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    xml = _land(slim, name, "101", "102", "201")
    both = mark_cli.plan_pass(slim, xml, playlists_named=["pl-b", "pl-a", "pl-b"])
    whole = mark_cli.plan_pass(slim, xml)
    assert both.named == ("pl-b", "pl-a")
    assert sorted(both.planned) == sorted(whole.planned) == ["pl-a", "pl-b"]
    assert whole.named == ()
    assert mark_cli.ONLY_SAID not in mark_cli.shown(whole)
    # The same marks, two questions: the narrowing is in the digest, so an
    # answer to one screen is never read as an answer to the other.
    assert both.payload["digest"] != whole.payload["digest"]


def test_a_playlist_of_no_pass_of_this_name_is_refused_before_the_account_is_listed(
    slim, monkeypatch
):
    fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    listings = fake.account_listings

    code, refused = _mark(xml, "--playlist", "pl-b", "--playlist", "pl-elsewhere")

    assert code != int(ExitCode.OK), refused
    cause = refused["cause"]
    assert cause["reason"] == "sync-marks-blocked"
    assert "pl-elsewhere" in cause["message"] and "pl-b" not in cause["detail"]["not_of_pass"]
    assert cause["detail"]["not_of_pass"] == ["pl-elsewhere"]
    assert fake.account_listings == listings, "the account was listed for a playlist of no pass"
    assert account.renamed == []


def test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name(slim, monkeypatch):
    """``102`` never arrived, so naming ``pl-a`` is refused with the track, not
    planned as a skip the person asked to be marked."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "201")

    code, refused = _mark(xml, "--playlist", "pl-a")

    assert code != int(ExitCode.OK), refused
    cause = refused["cause"]
    assert cause["reason"] == "sync-marks-blocked"
    assert cause["detail"]["not_complete"] == ["pl-a"]
    assert cause["detail"]["reasons"] == {"pl-a": mark_cli.ROWS_OUTSTANDING}
    assert "Warmup" in cause["message"] and "Artist 102 - Title 102" in cause["message"]
    assert account.renamed == []
    # The whole pass still plans its finished playlist, and leaves pl-a as a skip.
    code, whole = _mark(xml)
    assert code == int(ExitCode.DECISION_REQUIRED), whole
    assert whole["cause"]["detail"]["shown"]["renamed on the account"] == [
        "Peak -> DOWNLOADED Peak"
    ]


def test_a_named_playlist_whose_job_failed_is_refused_by_name(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO, failing=("pl-a",))
    xml = _land(slim, name, "101", "102", "201")
    with pytest.raises(CratekitError) as refused:
        mark_cli.plan_pass(slim, xml, playlists_named=["pl-a"])
    assert refused.value.cause.detail["reasons"] == {"pl-a": mark_cli.JOB_UNFINISHED}


def test_a_named_playlist_already_marked_is_a_skip_and_not_a_refusal(slim, monkeypatch):
    """Already marked is complete: the plan says so and renames nothing."""
    fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    xml = _land(slim, name, "101", "102", "201")
    fake.account = [_playlist("pl-a", "DOWNLOADED Warmup"), _playlist("pl-b", "Peak")]

    planned = mark_cli.plan_pass(slim, xml, playlists_named=["pl-a"])

    assert planned.planned == []
    (item,) = planned.payload["items"]
    assert (item["id"], item["action"], item["reason"]) == (
        "pl-a",
        mark_cli.SKIP,
        mark_cli.ALREADY_MARKED,
    )
    assert account.renamed == []


def test_the_library_is_walked_only_for_the_named_playlist(slim, monkeypatch):
    """Narrowed before the walk, so a named playlist settles only its own tracks."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    xml = _land(slim, name, "101", "102")
    asked: list[str] = []
    real = mark_cli.match.resolve_one

    def counting(wanted, *args, **kwargs):
        asked.append(wanted.ref)
        return real(wanted, *args, **kwargs)

    monkeypatch.setattr(mark_cli.match, "resolve_one", counting)
    planned = mark_cli.plan_pass(slim, xml, playlists_named=["pl-a"])
    assert planned.planned == ["pl-a"]
    assert sorted(asked) == ["101", "102"]


def test_a_native_pass_takes_playlist_as_the_file_does(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    _cut_over_intake(slim)
    _hold(slim, "101", "102", "201")
    _record_landing(slim, name)

    planned = mark_cli.plan_pass(slim, pass_name=name, playlists_named=["pl-a"])
    assert planned.planned == ["pl-a"]
    data, _warnings, landed = mark_cli.apply_pass(slim, planned)
    assert landed == ["pl-a"]
    assert account.renamed == [("pl-a", "DOWNLOADED Warmup")]
    assert [item["id"] for item in data["items"]] == ["pl-a"]


# ═══════════════════════════════════════════════════════════════════════════
# U174, R-915: organize plans a mark for every pass a native landing committed
# ═══════════════════════════════════════════════════════════════════════════


def _mark_steps(cfg: config.Config):
    from cratekit.organize import account as account_area
    from cratekit.organize.steps import Area

    area = Area(name=account_area.AREA)
    account_area._mark_steps(cfg, area)
    return area


def test_organize_plans_every_native_pass_not_only_the_latest(slim, monkeypatch):
    """Sitting 48: an earlier pass's playlist sat unmarked at the account root,
    because only the latest pass was marked and organize found none at all."""
    fake, earlier = _swept_pass(monkeypatch, (_playlist("pl-old", "Aa-Phil 10-14-26"), _tracks("301")))
    # A second pass, later, over the same account: rebind with both playlists
    # listed, so the earlier one's name is still on the account.
    _fake, later = _swept_pass(
        monkeypatch,
        (_playlist("pl-old", "Aa-Phil 10-14-26"), _tracks("301")),
        *TWO,
    )
    assert earlier != later
    _cut_over_intake(slim)
    _hold(slim, "101", "102", "201", "301")
    _record_landing(slim, earlier, stamp="100000")
    _record_landing(slim, later, stamp="120000")

    area = _mark_steps(slim)

    steps = {step.key: step for step in area.steps}
    assert set(steps) == {f"mark:{earlier}", f"mark:{later}"}
    assert [item["id"] for item in steps[f"mark:{earlier}"].items] == ["pl-old"]
    assert steps[f"mark:{earlier}"].state == "planned"
    assert steps[f"mark:{later}"].state == "planned"
    assert {item["id"] for item in steps[f"mark:{later}"].items} >= {"pl-a", "pl-b"}
    assert "native landings of no sync pass" not in area.facts


def test_organize_marks_a_native_pass_through_its_gate(slim, monkeypatch):
    """Driven through the step's own apply, the rename lands and is recorded."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    account = outbound_fakes.FakeAccount()
    bind_account(monkeypatch, account)
    _cut_over_intake(slim)
    _hold(slim, "101", "102", "201")
    _record_landing(slim, name)

    (step,) = _mark_steps(slim).steps
    assert step.counts == {"mark": 2, "skip": 0}
    applied = step.apply()

    assert applied["marked"] == 2
    assert sorted(account.renamed) == [("pl-a", "DOWNLOADED Warmup"), ("pl-b", "DOWNLOADED Peak")]


def test_a_native_landing_of_no_sync_pass_is_counted_and_is_no_step(slim, monkeypatch):
    _cut_over_intake(slim)
    _record_landing(slim, "a label batch")
    area = _mark_steps(slim)
    assert area.steps == []
    assert area.facts["native landings of no sync pass"] == 1
    assert area.facts["intake files of no sync pass"] == 0


def test_a_pass_with_an_intake_file_is_planned_once_by_its_file(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    _cut_over_intake(slim)
    _land(slim, name, "101", "102", "201")
    _record_landing(slim, name)
    steps = [step.key for step in _mark_steps(slim).steps]
    assert steps == [f"mark:{name}"]


def test_a_tree_on_the_bridge_plans_no_native_record(slim, monkeypatch):
    """A record left from before a revert is not planned as a refusal every run."""
    _fake, name = _swept_pass(monkeypatch, *TWO)
    _record_landing(slim, name)
    assert mark_cli.native_passes(slim) == ()
    assert _mark_steps(slim).steps == []


def test_landed_passes_reads_only_closed_committed_landings(slim):
    _record_landing(slim, "kept", stamp="100000")
    _record_landing(slim, "kept", stamp="110000")
    _record_landing(slim, "open", state=session.SessionState.OPEN, stamp="120000")
    _record_landing(slim, "refused", source=session.SourceState.REFUSED, stamp="130000")
    # A landing of no pass names none, and is never listed as a pass of "None".
    nameless = _record_landing(slim, "x", stamp="140000")
    record = session.read_record(nameless, slim)
    record.detail = {}
    session.write_record(record, slim)
    # Another workflow's record that carries a pass is not a landing.
    session.write_record(
        session.SessionRecord(
            session_id=f"20261007T{150000}-refill",
            workflow="not-the-intake",
            started="2026-10-07T15:00:00+00:00",
            state=session.SessionState.CLOSED,
            sources={active_taxonomy.load(slim).intake.id: str(session.SourceState.COMMITTED)},
            ended="2026-10-07T15:00:00+00:00",
            detail={native.PASS_KEY: "elsewhere"},
        ),
        slim,
    )
    assert native.landed_passes(slim) == ("kept",)


def test_an_unreachable_root_is_a_refused_step_and_never_no_pass(slim, monkeypatch):
    """The landings' records live under the root, so an unmounted volume would
    read as no pass at all and organize would ask over a clean plan."""
    _cut_over_intake(slim)
    _record_landing(slim, "a pass")
    monkeypatch.setattr(
        mark_cli.ingest,
        "intake_medium",
        lambda cfg: mark_cli.ingest.IntakeMedium(declared=None, registry=None),
    )
    with pytest.raises(CratekitError) as refused:
        mark_cli.native_passes(slim)
    assert "could not be reached" in refused.value.cause.message
    (step,) = _mark_steps(slim).steps
    assert (step.key, step.state) == ("mark:native", "refused")


def test_an_unreadable_tree_registry_refuses_the_native_step_alone(slim, monkeypatch):
    """The passes found by their intake files are still planned beside it."""
    from cratekit.core import tree_registry as registry_module

    _fake, name = _swept_pass(monkeypatch, *TWO)
    _land(slim, name, "101", "102", "201")
    _cut_over_intake(slim)
    registry_module.path_for(slim).write_text("{not json", encoding="utf-8")

    steps = {step.key: step for step in _mark_steps(slim).steps}

    assert steps["mark:native"].state == "refused"
    assert steps[f"mark:{name}"].state == "planned"


def test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate(slim, monkeypatch):
    fake, name = _swept_pass(monkeypatch, *TWO)
    xml = _land(slim, name, "101", "102", "201")
    stranger = xml.with_name(f"2020-01-01T000000Z-zzzz_synced{land_cli.INTAKE_SUFFIX}")
    xml.rename(stranger)
    listings = fake.account_listings

    code, refused = _mark(stranger, "--playlist", "pl-a")

    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["not_of_pass"] == ["pl-a"]
    assert fake.account_listings == listings


def test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name(slim, monkeypatch):
    _fake, name = _swept_pass(monkeypatch, *TWO)
    xml = _land(slim, name, "101", "102", "201")
    (job,) = [job for job in _playlist_jobs() if playlists.playlist_of(job) == "pl-a"]
    with jobs.open_store() as store:
        item = jobs.items(store, job.job_id)[0]
    artifacts.final_path(
        intake_cli.ARTIFACTS, jobs.frozen_config(job), job.job_id, item.ordinal
    ).write_text("{", encoding="utf-8")

    with pytest.raises(CratekitError) as refused:
        mark_cli.plan_pass(slim, xml, playlists_named=["pl-a"])

    assert refused.value.cause.detail["reasons"] == {"pl-a": mark_cli.REPORTS_UNREADABLE}


def test_a_native_pass_whose_plan_refuses_is_a_refused_step_and_not_dropped(slim, monkeypatch):
    """The account refusing its listing is that pass's refusal, shown on the gate."""
    from cratekit.core.cause import refuse

    _fake, name = _swept_pass(monkeypatch, *TWO)
    _cut_over_intake(slim)
    _hold(slim, "101", "102", "201")
    _record_landing(slim, name)

    def refused_listing(cfg):
        raise refuse("credential-missing", "no session is stored for the account", origin=("test",))

    monkeypatch.setattr(mark_cli, "listed", refused_listing)

    (step,) = _mark_steps(slim).steps
    assert (step.key, step.state) == (f"mark:{name}", "refused")
    assert step.cause.reason == "credential-missing"
