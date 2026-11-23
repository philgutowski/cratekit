"""The helpers every package used to write for itself, tested once at their home (U298).

Functions once written in dozens of files each got one home (U290's survey),
and what each does is pinned here, so a change to one is one failing test.

Sections: 1. ``cli.output``, the plumbing a verb's shell needs. 2. ``core.jobs``,
the report base. 3. ``core.private_store``. 4. ``core.config``'s locks and its
state document read. 5. Small shared readers. 6. ``core.jobs``, the tail of every
resume. 7. ``write``: rollback, membership columns, the commit. 8. What two
modules of one feature each wrote.
"""

from __future__ import annotations

import ast
import dataclasses
import errno
import json
import logging
import os
import sqlite3
import stat
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.acquire import adapter as acquire_adapter
from cratekit.acquire import isrc_screen, match, provider_session
from cratekit.adopt import artifacts as adopt_artifacts
from cratekit.adopt import shell as adopt_shell
from cratekit.analysis import artifacts as analysis_artifacts
from cratekit.cli import output
from cratekit.core import (
    config,
    jobs,
    naming,
    preflight,
    private_store,
    rb_writer,
    review,
    session,
    tree_registry,
)
from cratekit.core.cause import DATABASE_PATH_ATTRIBUTE, CratekitError, Scope
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound import artifacts as outbound_artifacts
from cratekit.sync import marks
from cratekit.tagging import artifacts as tagging_artifacts
from cratekit.tagging import backlog_cli
from cratekit.tagging import rows as tagging_rows
from cratekit.tagging import shell as tagging_shell
from cratekit.write import row_defaults, trees
from tests.test_config import valid_data

SRC_ROOT = Path(__file__).resolve().parent.parent / "src" / "cratekit"


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    """A configured machine, saved, so ``config.load`` reads it back."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    built = config.from_dict(valid_data(library))
    config.save(built)
    config.reset_cache()
    return built


def an_entry(*names: str, verb: str = "tag.rows"):
    """A registry entry reduced to what a gate lookup reads: a name and its gates."""
    return SimpleNamespace(name=verb, gates=tuple(SimpleNamespace(name=name) for name in names))


# 1. cli.output: what a verb's shell needs


def test_a_readable_config_is_returned_as_config_load_reads_it(cfg):
    assert output.load_config(("tagging.rows_cli",)) == config.load()


@pytest.mark.parametrize(
    ("failure", "remedy"),
    [
        (config.ConfigMissing("no configuration file was found"), config.ConfigMissing.remedy),
        (config.ConfigInvalid("library.root is not a path"), config.ConfigInvalid.remedy),
        (config.ConfigInvalid("the pin was never recorded", remedy=Remedy.RUN_DOCTOR), Remedy.RUN_DOCTOR),
    ],
)
def test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it(monkeypatch, failure, remedy):
    """The cause, the message and the remedy are the failure's own; only the origin is the verb's."""

    def refuses():
        raise failure

    monkeypatch.setattr(config, "load", refuses)
    seen = []
    for origin in (("favorites.order_cli",), ("acquire.cli",), ("session", "cli")):
        with pytest.raises(CratekitError) as raised:
            output.load_config(origin)
        cause = raised.value.cause
        assert raised.value.__cause__ is failure
        assert cause.origin == origin
        seen.append((cause.reason, cause.message, cause.remediation.remedy, dict(cause.detail)))

    assert set(map(repr, seen)) == {
        repr(("config-unusable", str(failure), remedy, {"kind": type(failure).__name__}))
    }


def test_only_a_configuration_failure_is_turned_into_the_cause(monkeypatch):
    """Anything else is a defect and leaves as itself, so it is not told as a config to fix."""

    def breaks():
        raise KeyError("library")

    monkeypatch.setattr(config, "load", breaks)

    with pytest.raises(KeyError):
        output.load_config(("label.cli",))


def test_a_gate_is_found_by_its_name_and_not_by_where_it_stands():
    """A shared gate sits beside a verb's own on its entry, in either order."""
    entry = an_entry("cloud-sync-unreadable", "confirm-rows")
    turned = an_entry("confirm-rows", "cloud-sync-unreadable")

    assert output.declared_gate(entry, "confirm-rows") is entry.gates[1]
    assert output.declared_gate(turned, "confirm-rows") is turned.gates[0]
    assert output.confirm_gate(entry, "confirm-rows", origin=("x",)) is entry.gates[1]
    assert output.confirm_gate(turned, "confirm-rows", origin=("x",)) is turned.gates[0]


def test_a_missing_gate_is_a_runtime_error_for_the_verbs_that_always_raised_one():
    """The six verbs that looked a gate up this way end in a traceback, as they did."""
    with pytest.raises(RuntimeError) as raised:
        output.declared_gate(an_entry("other", verb="favorites.order"), "approve-order")

    assert str(raised.value) == "registry entry 'favorites.order' declares no gate 'approve-order'"
    assert not isinstance(raised.value, CratekitError)


def test_a_missing_gate_is_a_typed_refusal_for_the_verbs_that_ask_before_they_write():
    """The five verbs that looked a gate up this way refuse with a remedy, as they did."""
    with pytest.raises(CratekitError) as raised:
        output.confirm_gate(an_entry("other"), "confirm-rows", origin=("tagging.rows_cli",))

    cause = raised.value.cause
    assert cause.reason == "internal-error"
    assert cause.message == (
        "tag.rows declares no gate named 'confirm-rows', so there is no question to ask "
        "before it writes"
    )
    assert cause.remediation.remedy is Remedy.REPORT_DEFECT
    assert cause.origin == ("tagging.rows_cli",)
    assert dict(cause.detail) == {"verb": "tag.rows", "gate": "confirm-rows"}


def test_the_approving_actor_is_read_off_the_recorded_decision():
    """Not off the shell's default actor, which reads ``cli`` for a run nobody decided."""
    spec = SimpleNamespace(name="approve-plan")
    decided = SimpleNamespace(
        run=SimpleNamespace(decisions={"approve-plan": SimpleNamespace(actor="session")}),
        gate=SimpleNamespace(actor="cli"),
    )
    undecided = SimpleNamespace(
        run=SimpleNamespace(decisions={"another-gate": SimpleNamespace(actor="phillip")}),
        gate=SimpleNamespace(actor="cli"),
    )

    assert output.approving_actor(decided, spec) == "session"
    assert output.approving_actor(undecided, spec) == ""


def test_a_run_that_queued_nothing_reports_an_empty_string_for_its_job():
    """A null fails the verb's own schema, which types the field as a string (R-234)."""
    payload = output.no_job("no-op")

    assert payload == {"job_id": "", "state": "no-op", "cause": None, "progress": {}}
    assert output.payload_problems("job_state", payload) == []


def test_what_a_no_op_names_rides_under_progress_as_a_job_reports_it():
    counted = {"scanned": 3}
    payload = output.no_job("nothing-to-route", scanned=3, **{"left behind": 0})

    assert payload["progress"] == {"scanned": 3, "left behind": 0}
    assert set(payload) == {"job_id", "state", "cause", "progress"}
    assert output.payload_problems("job_state", payload) == []
    # A copy, so a caller that goes on to fill it cannot change another's answer.
    assert output.no_job("no-op", **counted)["progress"] is not counted


def test_the_two_shells_name_the_one_report_the_one_no_op_and_the_one_resume():
    """What ``adopt.shell`` and ``tagging.shell`` each wrote out is one function now."""
    for shell in (adopt_shell, tagging_shell):
        assert shell.reported is jobs.reported
        assert shell.advance is jobs.advance
        assert shell.no_op is output.no_job


# 2. core.jobs: where one item's report is staged, and where it lands

REPORTS = jobs.Artifacts(final="home-artifacts", staging="home-staging")


def test_a_final_a_staged_and_a_committed_path_are_built_from_the_queue_root_alone(cfg):
    """The same strings for the same job and state root, whichever feature asks."""
    root = jobs.store_dir(cfg)

    assert REPORTS.final_path(cfg, "job-1", 7) == root / "home-artifacts" / "job-1" / "0007.json"
    assert REPORTS.staged_path(cfg, "job-1", 7) == root / "home-staging" / "job-1" / "7" / "0007.json"
    assert REPORTS.final_dir(cfg, "job-1") == root / "home-artifacts" / "job-1"
    assert REPORTS.staging_dir(cfg, "job-1") == root / "home-staging" / "job-1"


@pytest.mark.parametrize(
    ("module", "final", "staging"),
    [
        (adopt_artifacts, "adopt-artifacts", "adopt-staging"),
        (outbound_artifacts, "outbound-artifacts", "outbound-staging"),
        (tagging_artifacts, "tag-artifacts", "tag-staging"),
    ],
)
def test_each_feature_keeps_its_own_two_directories_on_the_one_base(cfg, module, final, staging):
    """The names a feature's reports were committed under before U298 are the names now."""
    root = jobs.store_dir(cfg)

    assert module.final_path(cfg, "job-9", 12) == root / final / "job-9" / "0012.json"
    assert module.staged_path(cfg, "job-9", 12) == root / staging / "job-9" / "12" / "0012.json"
    assert (module.ARTIFACTS_DIRNAME, module.STAGING_DIRNAME) == (final, staging)


def test_analysis_takes_its_final_path_from_the_base_and_keeps_its_own_staging(cfg):
    """Its staging directory keeps an interrupted rename's evidence, so it is not the base's."""
    root = jobs.store_dir(cfg)

    assert analysis_artifacts.final_path(cfg, "job-9", 3) == (
        root / "analysis-artifacts" / "job-9" / "0003.json"
    )
    staged = analysis_artifacts.staged_path(cfg, "job-9", 3)
    assert staged == root / "analysis-staging" / "job-9" / "3" / "0003.json"
    intent = staged.parent / analysis_artifacts.RENAME_INTENT_FILENAME
    intent.write_text("{}", encoding="utf-8")
    assert analysis_artifacts.staged_path(cfg, "job-9", 3) == staged
    assert intent.exists(), "the base clears the directory whole; analysis must not"


def test_the_directories_are_made_private_as_the_paths_are_asked_for(cfg):
    final = REPORTS.final_path(cfg, "job-1", 0)
    staged = REPORTS.staged_path(cfg, "job-1", 0)

    for directory in (final.parent, staged.parent):
        assert directory.is_dir()
        assert directory.stat().st_mode & 0o777 == config.PRIVATE_DIR_MODE


def test_a_staging_directory_is_cleared_of_the_attempt_before_it(cfg):
    """A half written report left behind would be committed as the next attempt's own."""
    first = REPORTS.staged_path(cfg, "job-1", 4)
    first.write_text("half of a report", encoding="utf-8")
    (first.parent / "left-behind.txt").write_text("x", encoding="utf-8")

    again = REPORTS.staged_path(cfg, "job-1", 4)

    assert again == first
    assert list(again.parent.iterdir()) == []


def test_clearing_one_items_staging_leaves_its_neighbours(cfg):
    kept = REPORTS.staged_path(cfg, "job-1", 5)
    kept.write_text("{}", encoding="utf-8")

    REPORTS.staged_path(cfg, "job-1", 4)

    assert kept.read_text(encoding="utf-8") == "{}"


def test_a_produced_report_is_staged_whole_and_names_where_it_will_land(cfg):
    job = SimpleNamespace(job_id="job-1")
    item = SimpleNamespace(ordinal=2)

    produced = REPORTS.produced(cfg, job, item, {"b": 1, "a": [2, 3]})

    assert produced == jobs.Produced(
        staged=REPORTS.staging_dir(cfg, "job-1") / "2" / "0002.json",
        final=REPORTS.final_dir(cfg, "job-1") / "0002.json",
    )
    # Sorted keys and a closing newline, so two runs produce one file.
    assert produced.staged.read_text(encoding="utf-8") == '{\n  "a": [\n    2,\n    3\n  ],\n  "b": 1\n}\n'
    assert not produced.final.exists(), "the engine commits it, never the handler"
    assert jobs.commit_artifact(produced.staged, produced.final) == produced.final
    assert REPORTS.committed(cfg, "job-1") == ({"a": [2, 3], "b": 1},)


def _commit(cfg, where: jobs.Artifacts, job_id: str, ordinal: int, report) -> Path:
    path = where.final_path(cfg, job_id, ordinal)
    path.write_text(report if isinstance(report, str) else json.dumps(report), encoding="utf-8")
    return path


def test_committed_reports_are_read_back_in_item_order_as_numbers(cfg):
    """Four digits sort as text in item order and the ten thousandth does not."""
    for ordinal in (10000, 2, 9999):
        _commit(cfg, REPORTS, "job-1", ordinal, {"ordinal": ordinal})

    assert [report["ordinal"] for report in REPORTS.committed(cfg, "job-1")] == [2, 9999, 10000]


def test_a_job_with_no_reports_yet_has_none_and_makes_no_directory(cfg):
    assert REPORTS.committed(cfg, "never-ran") == ()
    assert not REPORTS.final_dir(cfg, "never-ran").exists()


def test_a_report_that_cannot_be_read_is_skipped_and_the_rest_are_reported(cfg):
    """One unreadable file must not turn into a verb that can say nothing of the others."""
    _commit(cfg, REPORTS, "job-1", 0, {"ordinal": 0})
    _commit(cfg, REPORTS, "job-1", 1, "{ not json")
    _commit(cfg, REPORTS, "job-1", 2, "[1, 2]")
    _commit(cfg, REPORTS, "job-1", 3, {"ordinal": 3})
    REPORTS.final_path(cfg, "job-1", 4).write_bytes(b"\xff\xfe not utf-8")

    assert REPORTS.committed(cfg, "job-1") == ({"ordinal": 0}, {"ordinal": 3})


def test_a_file_that_is_named_for_no_ordinal_is_no_report(cfg):
    """A stray ``notes.json`` once raised out of the sort key and took a resume down."""
    _commit(cfg, REPORTS, "job-1", 0, {"ordinal": 0})
    (REPORTS.final_dir(cfg, "job-1") / "notes.json").write_text('{"stray": true}', encoding="utf-8")

    assert REPORTS.committed(cfg, "job-1") == ({"ordinal": 0},)


def test_each_feature_orders_its_committed_reports_as_it_did_before_the_base(cfg):
    """Adoption sorts every file by number and outbound by name: neither was changed."""
    for module in (adopt_artifacts, outbound_artifacts):
        for ordinal in (10000, 2, 9999):
            module.final_path(cfg, "job-1", ordinal).write_text(
                json.dumps({"ordinal": ordinal}), encoding="utf-8"
            )
    numbered = [report["ordinal"] for report in adopt_artifacts.committed(cfg, "job-1")]
    named = [report["ordinal"] for report in outbound_artifacts.committed(cfg, "job-1")]

    assert numbered == [2, 9999, 10000]
    assert named == [2, 10000, 9999]

    (outbound_artifacts.final_path(cfg, "job-1", 0).parent / "notes.json").write_text(
        '{"stray": true}', encoding="utf-8"
    )
    assert {"stray": True} in outbound_artifacts.committed(cfg, "job-1")
    (adopt_artifacts.final_path(cfg, "job-1", 0).parent / "notes.json").write_text(
        '{"stray": true}', encoding="utf-8"
    )
    with pytest.raises(ValueError):
        adopt_artifacts.committed(cfg, "job-1")


@pytest.mark.parametrize(
    ("final", "staging"),
    [("", "s"), ("f", ""), ("a/b", "s"), ("f", "a/b"), (".", "s"), ("f", ".."), ("same", "same")],
)
def test_a_report_location_is_two_different_directory_names(final, staging):
    """One path component each, and never one directory: a commit is an ``os.replace``."""
    with pytest.raises(ValueError):
        jobs.Artifacts(final=final, staging=staging)


def test_the_report_base_never_resolves_the_queue_root_for_itself():
    """KTD9: the paths are built from the job's configuration, never the current one.

    No behaviour tells the two calls apart today, so this reads the source.
    """
    tree = ast.parse((SRC_ROOT / "core" / "jobs.py").read_text(encoding="utf-8"))
    (base,) = [
        node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Artifacts"
    ]
    resolvers = [
        node
        for node in ast.walk(base)
        if isinstance(node, ast.Call)
        and isinstance(node.func, (ast.Name, ast.Attribute))
        and (node.func.id if isinstance(node.func, ast.Name) else node.func.attr)
        in {"store_dir", "queue_path", "load", "load_from_path"}
    ]

    assert resolvers, "the base no longer builds a path from the queue root; move this guard"
    assert all(len(call.args) == 1 and not call.keywords for call in resolvers)
    assert all(isinstance(call.args[0], ast.Name) and call.args[0].id == "cfg" for call in resolvers)


# 3. core.private_store: the store both queues open


@pytest.mark.parametrize("kind", [jobs.JobStore, review.ReviewStore])
def test_a_store_is_opened_private_before_its_log_exists_and_on_the_queues_pragmas(
    tmp_path, monkeypatch, kind
):
    """The mode goes on before the write ahead log pragma, so SQLite's sidecars inherit it."""
    path = tmp_path / "store.db"
    seen: list[tuple[str, bool]] = []

    def records(target: Path) -> None:
        seen.append((target.name, path.with_name(path.name + "-wal").exists()))

    monkeypatch.setattr(kind, "_own_only", staticmethod(records))

    with kind(path) as store:
        assert seen == [("store.db", False), ("store.db-wal", False), ("store.db-shm", False)]
        assert store.conn.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
        assert store.conn.execute("PRAGMA synchronous").fetchone()[0] == 2
        assert store.conn.execute("PRAGMA busy_timeout").fetchone()[0] == 30000
        assert store.conn.row_factory is sqlite3.Row


def test_each_queue_keeps_its_own_rule_for_a_file_it_cannot_make_private():
    """The job queue passes over a mode it could not set; the review queue refuses."""
    assert issubclass(jobs.JobStore, private_store.PrivateStore)
    assert issubclass(review.ReviewStore, private_store.PrivateStore)
    assert jobs.JobStore._own_only is jobs._own_only
    assert review.ReviewStore._own_only is review._own_only
    assert jobs._own_only is not review._own_only


def test_the_review_queue_opens_its_store_without_the_job_engine():
    """The reports package persists through ``core.review`` alone (R12), never ``core.jobs``."""
    tree = ast.parse((SRC_ROOT / "core" / "review.py").read_text(encoding="utf-8"))
    imported = {
        alias.name if isinstance(node, ast.Import) else f"{node.module}.{alias.name}"
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    assert "cratekit.core.private_store.PrivateStore" in imported
    assert not {name for name in imported if name.startswith("cratekit.core.jobs")}
    assert "cratekit.core.jobs" not in imported


@pytest.mark.parametrize("kind", [jobs.JobStore, review.ReviewStore])
def test_an_immediate_transaction_commits_what_it_wrote_and_rolls_back_what_failed(tmp_path, kind):
    with kind(tmp_path / "store.db") as store:
        with store.immediate() as conn:
            conn.execute("CREATE TABLE kept (word TEXT)")
            conn.execute("INSERT INTO kept VALUES ('one')")

        with pytest.raises(RuntimeError):
            with store.immediate() as conn:
                conn.execute("INSERT INTO kept VALUES ('two')")
                assert conn.in_transaction
                raise RuntimeError("the write after it failed")

        assert [row["word"] for row in store.conn.execute("SELECT word FROM kept")] == ["one"]
        assert not store.conn.in_transaction


@pytest.mark.parametrize("kind", [jobs.JobStore, review.ReviewStore])
def test_a_store_that_cannot_be_opened_names_its_path_on_the_drivers_own_error(tmp_path, kind):
    """The driver's refusal carries no path and no errno, so the opening sequence names it."""
    missing = tmp_path / "no-such-directory" / "store.db"

    with pytest.raises(sqlite3.OperationalError) as raised:
        kind(missing)

    assert getattr(raised.value, DATABASE_PATH_ATTRIBUTE) == str(missing)


# 4. core.config: the lock and the read every state document's store shared


class StoreRefused(Exception):
    """A store's own refusal, as each caller builds one from what went wrong."""


def is_free(lock: Path) -> bool:
    """Whether nothing holds the lock at ``lock``, asked without waiting."""
    handle, had = config.lock_now(lock)
    handle.close()
    return had


@pytest.fixture
def descriptors(monkeypatch):
    """Every descriptor ``os.open`` hands out during the test, by the path it was opened on."""
    opened: list[tuple[str, int]] = []
    real = os.open

    def remembering(path, *args, **kwargs):
        descriptor = real(path, *args, **kwargs)
        opened.append((str(path), descriptor))
        return descriptor

    monkeypatch.setattr(os, "open", remembering)
    return opened


def is_closed(descriptor: int) -> bool:
    try:
        os.fstat(descriptor)
    except OSError:
        return True
    return False


def test_a_held_lock_shuts_out_a_second_holder_until_the_body_ends(tmp_path):
    lock = tmp_path / "state" / "ledger.lock"

    with config.held(lock, StoreRefused):
        assert not is_free(lock)

    assert is_free(lock)
    assert lock.is_file(), "the lock file is never unlinked"


def test_a_lock_that_cannot_be_taken_is_refused_in_the_stores_own_words(tmp_path):
    """The store's refusal is built from the lock's, and raised from it."""
    lock = tmp_path / "ledger.lock"
    lock.mkdir()  # a directory where the lock file belongs cannot be opened to lock
    met: list[BaseException] = []

    def refused(exc):
        met.append(exc)
        return StoreRefused("the ledger is in use")

    with pytest.raises(StoreRefused) as raised:
        with config.held(lock, refused):
            pytest.fail("the body ran without the lock")

    assert [type(one) for one in met] == [config.ConfigLockUnavailable]
    assert raised.value.__cause__ is met[0]


def test_a_failure_in_the_body_keeps_its_own_name_and_gives_the_lock_back(tmp_path):
    lock = tmp_path / "ledger.lock"

    with pytest.raises(KeyError):
        with config.held(lock, StoreRefused):
            raise KeyError("a row")

    assert is_free(lock)


def test_the_locks_own_error_raised_by_the_body_is_not_the_stores_refusal(tmp_path):
    """Only a failed ACQUISITION is translated; an inner store's refusal is its own."""
    lock = tmp_path / "ledger.lock"
    inner = config.ConfigLockUnavailable("an inner store could not take its lock")

    with pytest.raises(config.ConfigLockUnavailable) as raised:
        with config.held(lock, StoreRefused):
            raise inner

    assert raised.value is inner
    assert is_free(lock)


def test_a_lock_had_in_time_is_yielded_as_had_and_its_file_is_private_and_stays(tmp_path):
    lock = tmp_path / "state" / "cache.lock"
    slept: list[float] = []

    with config.lock_within(lock, wait_s=1.0, poll_s=0.25, sleep=slept.append) as had:
        assert had is True
        assert not is_free(lock)

    assert slept == []
    assert is_free(lock)
    assert lock.is_file()
    assert stat.S_IMODE(lock.stat().st_mode) == config.PRIVATE_FILE_MODE
    assert stat.S_IMODE(lock.parent.stat().st_mode) == config.PRIVATE_DIR_MODE


def test_a_lock_another_holds_is_asked_for_until_the_wait_is_spent_and_then_given_up(tmp_path):
    lock = tmp_path / "cache.lock"
    slept: list[float] = []
    holder, _ = config.lock_now(lock)
    try:
        with config.lock_within(lock, wait_s=1.0, poll_s=0.25, sleep=slept.append) as had:
            assert had is False
    finally:
        holder.close()

    assert slept == [0.25, 0.25, 0.25, 0.25]


def test_a_lock_freed_during_the_wait_is_had_at_the_next_look(tmp_path):
    lock = tmp_path / "cache.lock"
    holder, _ = config.lock_now(lock)
    slept: list[float] = []

    def sleep(seconds: float) -> None:
        slept.append(seconds)
        holder.close()

    with config.lock_within(lock, wait_s=1.0, poll_s=0.25, sleep=sleep) as had:
        assert had is True

    assert slept == [0.25]


def test_a_lock_file_that_cannot_be_opened_is_not_had_and_raises_nothing(tmp_path):
    """A writer that would rather skip than wait skips here too, without a sleep."""
    lock = tmp_path / "cache.lock"
    lock.mkdir()
    slept: list[float] = []

    with config.lock_within(lock, wait_s=1.0, poll_s=0.25, sleep=slept.append) as had:
        assert had is False

    assert slept == []


def test_a_failure_under_a_lock_had_in_time_gives_the_lock_back(tmp_path):
    lock = tmp_path / "cache.lock"

    with pytest.raises(KeyError):
        with config.lock_within(lock, wait_s=1.0, poll_s=0.25, sleep=lambda _s: None):
            raise KeyError("a tally")

    assert is_free(lock)


def test_a_lock_taken_without_waiting_is_had_by_one_and_read_by_the_other(tmp_path):
    """The loser keeps an open handle, since the holder's own words are in the file."""
    lock = tmp_path / "state" / "staging.lock"
    first, had_first = config.lock_now(lock)
    second, had_second = config.lock_now(lock)
    try:
        assert (had_first, had_second) == (True, False)
        first.write("crate sync night")
        first.flush()
        second.seek(0)
        assert second.read() == "crate sync night"
        assert stat.S_IMODE(lock.stat().st_mode) == config.PRIVATE_FILE_MODE
        assert stat.S_IMODE(lock.parent.stat().st_mode) == config.PRIVATE_DIR_MODE
    finally:
        first.close()
        second.close()

    assert is_free(lock)


def test_a_lock_without_waiting_that_fails_some_other_way_closes_its_handle(
    tmp_path, monkeypatch, descriptors
):
    """Held by another is an answer; anything else leaves as itself with nothing left open."""
    import fcntl  # noqa: PLC0415 - POSIX only, as the lock is

    lock = tmp_path / "staging.lock"

    def breaks(handle, how):
        raise OSError(errno.EIO, "the volume went away")

    monkeypatch.setattr(fcntl, "flock", breaks)

    with pytest.raises(OSError) as raised:
        config.lock_now(lock)

    assert raised.value.errno == errno.EIO
    mine = [descriptor for path, descriptor in descriptors if path == str(lock)]
    assert len(mine) == 1 and is_closed(mine[0])


def test_the_waiting_lock_hardens_its_file_before_it_locks_and_returns_the_holder(tmp_path):
    target = tmp_path / "reconcile.lock"
    hardened: list[tuple[Path, bool]] = []

    def harden(path: Path) -> None:
        hardened.append((path, is_free(path)))

    handle = config.flock_exclusive(target, harden)
    try:
        assert hardened == [(target, True)], "hardened once, before the lock was taken"
        assert not is_free(target)
        assert stat.S_IMODE(target.stat().st_mode) == config.PRIVATE_FILE_MODE
    finally:
        handle.close()

    assert is_free(target)


@pytest.mark.parametrize("failure", [PermissionError("another account's lock"), KeyboardInterrupt()])
def test_a_waiting_lock_that_fails_closes_its_handle_and_leaves_as_itself(
    tmp_path, descriptors, failure
):
    """An interrupt included: the caller decides which failure is its own refusal."""
    target = tmp_path / "reconcile.lock"

    def harden(path: Path) -> None:
        raise failure

    with pytest.raises(type(failure)) as raised:
        config.flock_exclusive(target, harden)

    assert raised.value is failure
    mine = [descriptor for path, descriptor in descriptors if path == str(target)]
    assert len(mine) == 1 and is_closed(mine[0])
    assert is_free(target)


def test_an_absent_state_file_is_no_bytes_and_any_other_failure_is_its_own(tmp_path):
    held = tmp_path / "held.bin"
    held.write_bytes(b"\x00\xff")

    assert config.read_bytes_if_present(tmp_path / "absent.bin") is None
    assert config.read_bytes_if_present(held) == b"\x00\xff"
    with pytest.raises(IsADirectoryError):
        config.read_bytes_if_present(tmp_path)


def test_an_absent_document_is_not_a_document_that_holds_null(tmp_path):
    path = tmp_path / "document.json"

    assert config.read_json(path, StoreRefused) == (False, None)
    path.write_text("null", encoding="utf-8")
    assert config.read_json(path, StoreRefused) == (True, None)
    path.write_text('{"since": "2026-11-21", "count": 2}', encoding="utf-8")
    assert config.read_json(path, StoreRefused) == (True, {"since": "2026-11-21", "count": 2})


@pytest.mark.parametrize("content", [b"{not json", b"", b"\xff\xfe\x00"])
def test_a_document_that_does_not_parse_is_refused_and_never_read_as_empty(tmp_path, content):
    """Bytes that are not UTF-8 are told as not JSON as well, in the store's own refusal."""
    path = tmp_path / "document.json"
    path.write_bytes(content)

    with pytest.raises(StoreRefused) as raised:
        config.read_json(path, StoreRefused)

    assert raised.value.args == ("it is not JSON",)
    assert isinstance(raised.value.__cause__, ValueError)


def test_a_document_that_cannot_be_opened_is_refused_and_never_read_as_empty(tmp_path):
    path = tmp_path / "document.json"
    path.mkdir()

    with pytest.raises(StoreRefused) as raised:
        config.read_json(path, StoreRefused)

    assert raised.value.args == ("it could not be opened",)
    assert isinstance(raised.value.__cause__, OSError)


def test_a_document_read_as_a_map_is_none_when_absent_and_the_map_when_it_is_one(tmp_path):
    path = tmp_path / "document.json"

    assert config.read_json_map(path, StoreRefused) is None
    path.write_text('{"version": 1}', encoding="utf-8")
    assert config.read_json_map(path, StoreRefused) == {"version": 1}


@pytest.mark.parametrize(
    ("text", "kind"), [("[]", "list"), ('"words"', "str"), ("3", "int"), ("null", "NoneType")]
)
def test_a_document_that_is_no_map_is_refused_by_what_it_is(tmp_path, text, kind):
    """A list or a scalar read as an empty record is deleted by the next write."""
    path = tmp_path / "document.json"
    path.write_text(text, encoding="utf-8")

    with pytest.raises(StoreRefused) as raised:
        config.read_json_map(path, StoreRefused)

    assert raised.value.args == (f"the document is a {kind}, not a map",)


def test_the_read_in_the_platforms_encoding_agrees_with_the_other_on_every_shared_case(tmp_path):
    path = tmp_path / "document.json"
    assert config.read_json_as_text(path, StoreRefused) == (False, None)
    path.write_text('{"version": 1}')
    assert config.read_json_as_text(path, StoreRefused) == (True, {"version": 1})
    path.write_text("{not json")
    with pytest.raises(StoreRefused) as raised:
        config.read_json_as_text(path, StoreRefused)
    assert raised.value.args == ("it is not JSON",)

    folder = tmp_path / "folder.json"
    folder.mkdir()
    with pytest.raises(StoreRefused) as raised:
        config.read_json_as_text(folder, StoreRefused)
    assert raised.value.args == ("it could not be opened",)


def test_bytes_that_are_not_text_leave_the_platform_read_as_the_decoding_failure_they_are(tmp_path):
    """The one case the two reads differ on; the platform decoder is read, not assumed."""
    path = tmp_path / "document.json"
    path.write_bytes(b"\xff\xfe\x00")
    try:
        path.read_text()
    except UnicodeDecodeError:
        expected: type[BaseException] = UnicodeDecodeError
    else:
        expected = StoreRefused

    with pytest.raises(expected):
        config.read_json_as_text(path, StoreRefused)
    with pytest.raises(StoreRefused):
        config.read_json(path, StoreRefused)


def test_a_remedied_error_carries_its_classes_remedy_unless_the_raise_names_one():
    class ShopClosed(config.RemediedError):
        remedy = Remedy.RUN_DOCTOR

    plain = ShopClosed("the shop is closed")
    named = ShopClosed("the shop is closed", remedy=Remedy.REPORT_DEFECT)

    assert str(plain) == "the shop is closed"
    assert plain.remedy is Remedy.RUN_DOCTOR
    assert named.remedy is Remedy.REPORT_DEFECT
    assert ShopClosed.remedy is Remedy.RUN_DOCTOR, "a raise's remedy is that raise's alone"


def test_a_config_failure_and_an_adapter_failure_are_remedied_and_neither_is_the_other():
    """A handler written for one of them never catches the other by their shared base."""
    assert issubclass(config.ConfigError, config.RemediedError)
    assert issubclass(acquire_adapter.AdapterError, config.RemediedError)
    assert not issubclass(acquire_adapter.AdapterError, config.ConfigError)
    assert not issubclass(config.ConfigError, acquire_adapter.AdapterError)


# 5. The small readers a second package came to need


@pytest.mark.parametrize(
    ("value", "count"),
    [(0, 0), (7, 7), (-1, None), (True, None), (False, None), (2.0, None), ("3", None), (None, None)],
)
def test_a_count_is_a_whole_number_that_is_not_negative_and_never_a_boolean(value, count):
    read = output.count_of(value)

    assert read == count and type(read) is type(count)


def test_the_lossy_template_declares_the_marker_in_the_text_configuration_holds():
    assert naming.NameTemplate.lossy("[MP3]") == naming.NameTemplate(
        markers=(naming.MarkerRule(field="lossy", literal="[MP3]"),)
    )
    assert naming.NameTemplate.lossy(" [MP3] ").markers[0].literal == " [MP3] "


def test_a_marker_of_nothing_is_refused_by_the_strict_template_and_plain_for_the_tolerant_one():
    with pytest.raises(ValueError, match="empty literal"):
        naming.NameTemplate.lossy("")

    for absent in (None, "", "   "):
        assert naming.NameTemplate.lossy_if_marked(absent) == naming.NameTemplate()
    assert naming.NameTemplate.lossy_if_marked(" [MP3] ") == naming.NameTemplate.lossy("[MP3]")


def test_the_name_budget_is_the_two_ceilings_a_naming_section_holds():
    section = SimpleNamespace(path_budget_bytes=411, filename_max_bytes=177)

    budget = naming.NameBudget.of(section)

    assert (budget.path_budget_bytes, budget.filename_max_bytes) == (411, 177)
    assert budget == naming.NameBudget(path_budget_bytes=411, filename_max_bytes=177)


def test_the_device_of_a_path_is_read_off_its_nearest_ancestor_that_exists(tmp_path):
    here = tmp_path.stat().st_dev

    assert preflight.device_of(tmp_path) == here
    assert preflight.device_of(tmp_path / "not" / "yet" / "made") == here


def test_a_path_nothing_can_be_read_above_has_no_device(monkeypatch):
    """So a caller comparing two devices never takes two unreadable paths for one volume."""
    asked: list[str] = []

    def refuses(self, **_kwargs):
        asked.append(str(self))
        raise PermissionError(str(self))

    with monkeypatch.context() as patched:
        patched.setattr(Path, "stat", refuses)
        found = preflight.device_of(Path("/library/Music/House"))

    assert found is None
    assert asked == ["/library/Music/House", "/library/Music", "/library", "/"]


def test_a_registry_entry_is_found_by_its_tree_identifier_and_the_first_recorded_wins():
    entries = [
        SimpleNamespace(tree_id="genres", name="first"),
        SimpleNamespace(tree_id="labels", name="second"),
        SimpleNamespace(tree_id="genres", name="third"),
    ]

    assert tree_registry.by_tree_id(entries, "genres").name == "first"
    assert tree_registry.by_tree_id(entries, "labels").name == "second"
    assert tree_registry.by_tree_id(entries, "first") is None, "never found by a name"
    assert tree_registry.by_tree_id(iter(()), "genres") is None


# 6. core.jobs: the tail of every resume


def a_job(job_id: str, *, is_open: bool):
    return SimpleNamespace(job_id=job_id, is_open=lambda: is_open)


def test_a_job_still_open_is_driven_once_and_read_again_before_it_is_judged(monkeypatch):
    calls: list[tuple] = []
    queued, ended = a_job("job-1", is_open=True), a_job("job-1", is_open=False)
    warnings = ({"code": "slow", "message": "one item took a minute"},)

    def run_job(store, job):
        calls.append(("drive", store, job))
        return "the driver's result", warnings

    def get(store, job_id):
        calls.append(("read", store, job_id))
        return ended

    monkeypatch.setattr(jobs, "get", get)
    monkeypatch.setattr(jobs, "raise_for_state", lambda job: calls.append(("judge", job)))

    assert jobs.resumed(SimpleNamespace(run_job=run_job), "the store", queued) == (ended, warnings)
    assert calls == [
        ("drive", "the store", queued),
        ("read", "the store", "job-1"),
        ("judge", ended),
    ]


def test_a_job_already_closed_is_judged_without_being_driven(monkeypatch):
    """The raise is outside the open branch, so the second ask answers as the first did (R-225)."""
    failed = a_job("job-2", is_open=False)
    cause = RuntimeError("the job failed when it ran")

    def judge(job):
        assert job is failed
        raise cause

    def run_job(store, job):
        pytest.fail("a closed job was driven")

    monkeypatch.setattr(jobs, "get", lambda store, job_id: pytest.fail("a closed job was read again"))
    monkeypatch.setattr(jobs, "raise_for_state", judge)

    with pytest.raises(RuntimeError) as raised:
        jobs.resumed(SimpleNamespace(run_job=run_job), "the store", failed)
    assert raised.value is cause


def test_a_job_that_ended_cleanly_before_the_ask_is_returned_with_no_warnings(monkeypatch):
    done = a_job("job-3", is_open=False)
    monkeypatch.setattr(jobs, "raise_for_state", lambda job: None)

    assert jobs.resumed(SimpleNamespace(run_job=None), "the store", done) == (done, ())


# 7. write: what every guarded writer does on its way in and on its way out


def a_handle(rollback):
    return SimpleNamespace(session=SimpleNamespace(rollback=rollback))


def test_a_rollback_that_works_says_nothing(caplog):
    done: list[str] = []

    with caplog.at_level(logging.WARNING, logger=trees.logger.name):
        trees.rollback_quietly(a_handle(lambda: done.append("rolled back")))

    assert done == ["rolled back"]
    assert caplog.records == []


def test_a_rollback_that_fails_is_said_once_and_never_replaces_the_failure_it_follows(caplog):
    def fails():
        raise sqlite3.OperationalError("database is locked")

    with caplog.at_level(logging.WARNING, logger=trees.logger.name):
        try:
            raise ValueError("the write that failed")
        except ValueError as original:
            trees.rollback_quietly(a_handle(fails))
            kept = original

    assert str(kept) == "the write that failed"
    assert [record.getMessage() for record in caplog.records] == [
        "could not roll back the pending session after a failed write"
    ]


def test_an_interrupt_during_the_rollback_is_not_swallowed():
    def interrupted():
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        trees.rollback_quietly(a_handle(interrupted))


def test_membership_positions_are_read_off_the_tables_own_column_order():
    columns = ["ID", rb_writer.SOFT_DELETE_COLUMN, "ContentID", "TrackNo", "PlaylistID"]

    found = trees.membership_positions(SimpleNamespace(membership_columns=columns))

    assert found == (4, 2, 1), "the playlist, the content row, the removal marker"


def test_a_row_write_that_wrote_nothing_claims_no_commit(monkeypatch):
    """A restore reads a committed source as work it would discard."""
    recorded: list[tuple] = []
    monkeypatch.setattr(session, "record_commit", lambda *args: recorded.append(args))

    row_defaults.record_commit("the record", "genre", 0, "the config")
    row_defaults.record_commit("the record", "genre", -1, "the config")

    assert recorded == []


def test_a_row_write_records_its_commit_under_its_key_as_rows_updated(monkeypatch):
    recorded: list[tuple] = []
    monkeypatch.setattr(session, "record_commit", lambda *args: recorded.append(args))

    row_defaults.record_commit("the record", "genre", 3, "the config")

    assert recorded == [
        (
            "the record",
            "genre",
            session.ChangeSummary((session.TreeChange(tree="genre", updated=3),)),
            "the config",
        )
    ]


def test_the_two_row_writes_report_through_one_shape_and_one_adds_what_it_renumbered():
    base = row_defaults.RowsWritten(session_id="s-1", written=2, read_back=2)
    defaults = row_defaults.Written(session_id="s-1", written=2, read_back=2, renumbered=1)
    genres = tagging_rows.Written(session_id="s-1", written=2, read_back=2)

    assert (base.wrong, base.moved) == ((), ())
    assert [one.name for one in dataclasses.fields(base)] == [
        "session_id",
        "written",
        "read_back",
        "wrong",
        "moved",
    ]
    assert [one.name for one in dataclasses.fields(genres)] == [
        one.name for one in dataclasses.fields(base)
    ]
    assert [one.name for one in dataclasses.fields(defaults)][-1] == "renumbered"
    assert isinstance(defaults, row_defaults.RowsWritten)
    assert isinstance(genres, row_defaults.RowsWritten)
    assert not isinstance(genres, row_defaults.Written)


# 8. What two modules of one feature each wrote, held where it now lives


def test_a_module_this_build_can_import_is_importable_and_one_it_cannot_is_not(tmp_path, monkeypatch):
    """An import that fails INSIDE the module counts: its client library is part of it."""
    (tmp_path / "u298_needs_a_client.py").write_text(
        "import u298_a_client_library_nobody_installed\n", encoding="utf-8"
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    assert provider_session.importable("json") is True
    assert provider_session.importable("u298_no_such_module") is False
    assert provider_session.importable("u298_needs_a_client") is False


def test_a_marks_refusal_carries_the_verbs_own_origin_its_steps_and_its_detail():
    refusal = marks.blocked(
        ("sync", "cli", "mark"),
        "the account's marks cannot be read",
        "log in again",
        "run crate sync mark again",
        playlist="Inbox",
        tracks=3,
    )

    cause = refusal.cause
    assert (cause.reason, cause.message) == ("sync-marks-blocked", "the account's marks cannot be read")
    assert cause.origin == ("sync", "cli", "mark")
    assert tuple(cause.remediation.steps) == ("log in again", "run crate sync mark again")
    assert cause.scope is Scope.SOURCE
    assert dict(cause.detail) == {"playlist": "Inbox", "tracks": 3}


def test_the_first_few_of_a_list_are_named_and_the_rest_are_counted():
    few = [f"word {number}" for number in range(backlog_cli._NAMED)]

    assert backlog_cli.named([]) == ""
    assert backlog_cli.named(few) == ", ".join(few)
    assert backlog_cli.named([*few, "one over", "two over"]) == ", ".join(few) + " and 2 more"


def test_a_review_question_is_addressed_by_the_three_fields_the_exact_test_compares():
    typed = match.Wanted(artist="Beyoncé", title="Halo (Remastered)", version="Extended Mix")

    assert typed.folded_row() == {
        "artist": "beyonce",
        "title": "halo remastered",
        "version": "extended mix",
    }


def test_a_screen_leaves_out_every_code_the_cache_already_answers(monkeypatch):
    """A batch about an answered code would be the one request a second run still paid."""
    asked: list[tuple[object, list[str]]] = []
    held = {("GBAYE0000001", "US"), ("", "US")}
    cache = SimpleNamespace(holds=lambda code, country: (code, country) in held)
    screen = isrc_screen.Screen.__new__(isrc_screen.Screen)
    monkeypatch.setattr(isrc_screen.isrc_cache, "country_of", lambda client: "US")
    monkeypatch.setattr(
        isrc_screen.Screen,
        "screen",
        lambda self, client, codes: asked.append((client, list(codes))) or len(asked[-1][1]),
    )

    sent = screen.screen_uncached("the client", cache, ["GBAYE0000001", "GBAYE0000002", None, "USRC10000003"])

    assert asked == [("the client", ["GBAYE0000002", "USRC10000003"])]
    assert sent == 2
