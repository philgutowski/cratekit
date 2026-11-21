"""The helpers every package used to write for itself, tested once at their home (U298).

U290's survey found the same few functions written in dozens of files: the
config load that turns a ``ConfigError`` into ``config-unusable``, the lookup
of a verb's gate by name, the read of who approved it, the ``job_state``
payload, and the paths one queued item's report is staged at and lands at.
U298 gave each one home. A home is only worth having if what it does is pinned
where it lives, so that the next caller does not have to prove it again and a
change to it is one failing test, not forty.

What each section holds:

1. ``cli.output``: the plumbing a verb's shell needs. A verb that lives
   beside its domain may import that module and no other part of the shell,
   which is why it is the home.
2. ``core.jobs``: the report base, :class:`cratekit.core.jobs.Artifacts`.
   The job report and the job shell are held where they always were, in
   ``tests/test_tag_workers.py`` and ``tests/test_adopt_workers.py``, through
   the two shell modules that now only name them.
3. ``core.jobs``: the store both queues open, with each queue's own rule for
   a file it cannot make private.
"""

from __future__ import annotations

import ast
import json
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.adopt import artifacts as adopt_artifacts
from cratekit.adopt import shell as adopt_shell
from cratekit.analysis import artifacts as analysis_artifacts
from cratekit.cli import output
from cratekit.core import config, jobs, review
from cratekit.core.cause import DATABASE_PATH_ATTRIBUTE, CratekitError
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound import artifacts as outbound_artifacts
from cratekit.tagging import artifacts as tagging_artifacts
from cratekit.tagging import shell as tagging_shell
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


# ═══════════════════════════════════════════════════════════════════════════
# 1. cli.output: what a verb's shell needs
# ═══════════════════════════════════════════════════════════════════════════


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


# ═══════════════════════════════════════════════════════════════════════════
# 2. core.jobs: where one item's report is staged, and where it lands
# ═══════════════════════════════════════════════════════════════════════════

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
    """Adoption sorts every file by number and outbound by name: neither was changed.

    The base takes the order as an argument so that sharing the reader did not
    quietly decide, for two features, which files are reports.
    """
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
    """KTD9's defect behind an indirection, asserted where the paths are now built.

    ``jobs.store_dir()`` with no argument loads the CURRENT configuration, and a
    resume that ran against a configuration somebody edited since the job was
    queued is the bug KTD9 exists to close. The queue is installation scoped,
    so no behaviour tells the two calls apart today, which is why this reads
    the source. The feature modules passed this guard when they built the
    paths themselves; the base they now share has to.
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


# ═══════════════════════════════════════════════════════════════════════════
# 3. core.jobs: the store both queues open
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("kind", [jobs.JobStore, review.ReviewStore])
def test_a_store_is_opened_private_before_its_log_exists_and_on_the_queues_pragmas(
    tmp_path, monkeypatch, kind
):
    """The mode goes on before the write ahead log pragma, sidecars included.

    SQLite gives the log and the shared memory file the permissions the
    database file has when it creates them, so a mode set afterwards leaves two
    umask moded sidecars beside a correctly moded database.
    """
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
    assert jobs.JobStore._own_only is jobs._own_only
    assert review.ReviewStore._own_only is review._own_only
    assert jobs._own_only is not review._own_only


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
