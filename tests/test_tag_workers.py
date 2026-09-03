"""U3: what both tagging verbs stand on, before either one of them exists.

WHY THIS FILE EXISTS BEFORE ITS CALLERS DO. ``crate tag folder`` and ``crate tag
retag`` both queue a job today and neither one runs an item. The two pieces they
will share, the payload shell and the per item report helper, are ported from
``src/cratekit/adopt``, and a port is exactly the shape of change that arrives
green and wrong: the code compiles, the suite passes, and one of the properties
the original spelled out is quietly missing. So each property the original
states is asserted here against the copy rather than assumed to have travelled
with it.

THE THREE GUARDS THAT ARE NOT ABOUT BEHAVIOUR. A name (``drive``), a call shape
(``store_dir()`` with no argument), and a sort key are each invisible to a green
suite over this module, and each one breaks something in a file that is not this
one. They are asserted by parsing the source, which is the only place the
property lives.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path

import pytest

from cratekit.cli import output
from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError
from cratekit.tagging import artifacts, shell
from tests.test_config import valid_data
from tests.test_handlers import _drive_calls

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"
SHELL_SOURCE = SRC_ROOT / "cratekit" / "tagging" / "shell.py"
ARTIFACTS_SOURCE = SRC_ROOT / "cratekit" / "tagging" / "artifacts.py"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    """A configured machine. This is the configuration a job freezes."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    built = config.from_dict(valid_data(library))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def store(tmp_path):
    """A queue of this test's own, never the installation's."""
    with jobs.open_store(tmp_path / "queue" / jobs.QUEUE_FILENAME) as opened:
        yield opened


class Ctx:
    """The dispatcher context reduced to the one attribute ``advance`` uses.

    ``advance`` takes ``ctx`` untyped because ``cratekit.cli`` sits above the
    modules rank (KTD23), and the practical consequence is exactly this: the
    thing it needs is one method, so a test can hand it one. ``settle`` is what a
    real driver does to the rows, done here so ``advance`` re-reads a job that
    genuinely moved rather than one this stub asserted had moved.
    """

    def __init__(self, store, *, warnings=(), settle=True):
        self._store = store
        self._warnings = tuple(warnings)
        self._settle = settle
        self.driven: list[str] = []

    def run_job(self, store, job):
        self.driven.append(job.job_id)
        if self._settle:
            for item in jobs.items(store, job.job_id):
                jobs.claim(store, job.job_id, "test")
                jobs.complete_item(store, job.job_id, item.item_id)
            jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
        return None, self._warnings


def a_job(store, cfg: config.Config, *item_ids: str):
    """One queued job carrying the items named, or none at all."""
    return jobs.enqueue(
        store, handler_key="tag.folder", payload={}, cfg=cfg, item_ids=item_ids
    )


# ---------------------------------------------------------------------------
# The reported payload
# ---------------------------------------------------------------------------


def test_an_extra_mapping_rides_under_progress_and_never_beside_it(store, cfg):
    """The closed surface, asserted on the payload rather than on the intent.

    ``job_state/1`` is declared with ``additionalProperties: false``, so a per
    verb detail placed at the top level is an undeclared field and every
    consumer generated from the committed schema rejects the envelope. U51
    shipped that defect on two outbound verbs and the whole suite stayed green,
    which is why this asserts the four top level keys by equality rather than by
    membership.
    """
    job = a_job(store, cfg, "one.flac", "two.flac")

    payload = shell.reported(store, job, {"tagging": {"tagged": 2}})

    assert set(payload) == {"job_id", "state", "cause", "progress"}
    assert payload["progress"]["tagging"] == {"tagged": 2}
    assert payload["progress"]["total"] == 2
    assert output.payload_problems("job_state", payload) == []


def test_no_extra_leaves_the_progress_the_engine_reported_untouched(store, cfg):
    job = a_job(store, cfg, "one.flac")

    assert shell.reported(store, job)["progress"] == jobs.progress(store, job.job_id)


def test_a_job_carrying_a_cause_reports_it_as_the_declared_object(store, cfg):
    """``cause`` is the serialized cause, not a string and not a dropped field."""
    job = a_job(store, cfg, "one.flac")
    cancelled = jobs.cancel(store, job.job_id)

    payload = shell.reported(store, cancelled)

    assert payload["cause"]["reason"] == "cancelled"
    assert payload["state"] == str(jobs.JobState.CANCELLED)
    assert output.payload_problems("job_state", payload) == []


# ---------------------------------------------------------------------------
# The honest zero
# ---------------------------------------------------------------------------


def test_the_honest_zero_names_an_empty_job_id_rather_than_a_null():
    """R-234, which shipped once and must not be ported back in.

    ``cli.output`` requires every field of the declared surface and types this
    one as a string, so a null ``job_id`` fails the verb's own schema at the
    moment somebody validates it. The assertion is on the value rather than on
    truthiness, because ``None`` and ``""`` are both falsey and only one of them
    is the bug.
    """
    payload = shell.no_op("no-op")

    assert payload["job_id"] == ""
    assert payload["job_id"] is not None


def test_the_honest_zero_validates_against_the_job_state_surface():
    """Validated against the DECLARED schema, not against a hand written literal.

    ``output.payload_problems`` is the same check ``tests/cli_drive.py`` runs
    over a driven verb's whole envelope, narrowed to a bare payload. Asserting
    the field types by hand here would be a second opinion about a surface that
    already has an owner, and it would not notice a field added to the surface.
    """
    for state in ("no-op", "declined"):
        assert output.payload_problems("job_state", shell.no_op(state)) == [], state


# ---------------------------------------------------------------------------
# The resume
# ---------------------------------------------------------------------------


def test_a_job_with_no_items_is_refused_rather_than_driven(store, cfg):
    """The false success this refusal exists to stop.

    ``core.jobs`` reports a job with no items as SUCCEEDED by design, so driving
    one would tell a person their folder was tagged over a job that never had a
    file in it. The refusal is ``internal-error`` because no person can fix it:
    a job like this was queued by a build that did not record its items.
    """
    ctx = Ctx(store)
    job = a_job(store, cfg)

    with pytest.raises(CratekitError) as caught:
        shell.advance(
            ctx,
            store,
            job,
            origin=("tagging", "cli"),
            nothing_to_run="report a tagging sweep over a folder it never walked",
        )

    cause = caught.value.cause
    assert cause.reason == "internal-error"
    assert "never walked" in cause.message
    assert str(cause.remediation.remedy) == "report-defect"
    assert ctx.driven == []


def test_a_cancelled_job_raises_rather_than_reporting_through_a_normal_envelope(
    store, cfg
):
    """R-225, and the reason the predicate is not ``FAILED``.

    The state is built through ``jobs.cancel`` rather than by writing the row,
    so what is proved is the predicate against a state the engine actually
    produces. A run stopped with a signal lands here, closed and CANCELLED and
    carrying a cause, and the narrower predicate would hand it back as a payload
    the dispatcher exits 0 on.
    """
    ctx = Ctx(store)
    job = a_job(store, cfg, "one.flac")
    jobs.cancel(store, job.job_id)

    with pytest.raises(CratekitError) as caught:
        shell.advance(
            ctx,
            store,
            jobs.get(store, job.job_id),
            origin=("tagging", "cli"),
            nothing_to_run="report a sweep it never ran",
        )

    assert caught.value.cause.reason == "cancelled"
    assert ctx.driven == []


def test_a_succeeded_job_comes_back_without_being_driven_again(store, cfg):
    """A terminal state is a recorded answer, so a resume reports rather than reruns."""
    ctx = Ctx(store)
    job = a_job(store, cfg, "one.flac")
    jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)

    settled, warnings = shell.advance(
        ctx,
        store,
        jobs.get(store, job.job_id),
        origin=("tagging", "cli"),
        nothing_to_run="report a sweep it never ran",
    )

    assert settled.state is jobs.JobState.SUCCEEDED
    assert warnings == ()
    assert ctx.driven == []


def test_an_open_job_is_driven_and_comes_back_as_it_stands_afterwards(store, cfg):
    """The job is RE-READ after the drive, and the driver's warnings travel with it."""
    ctx = Ctx(store, warnings=({"code": "one-skipped", "message": "a file moved"},))
    job = a_job(store, cfg, "one.flac", "two.flac")

    settled, warnings = shell.advance(
        ctx,
        store,
        job,
        origin=("tagging", "cli"),
        nothing_to_run="report a sweep it never ran",
    )

    assert ctx.driven == [job.job_id]
    assert settled.state is jobs.JobState.SUCCEEDED
    assert warnings == ({"code": "one-skipped", "message": "a file moved"},)
    assert shell.reported(store, settled)["progress"]["settled"] == 2


# ---------------------------------------------------------------------------
# The name that is load bearing outside this module
# ---------------------------------------------------------------------------


def test_the_counter_this_guard_borrows_sees_a_call_it_is_meant_to_see():
    """P7's other half: a guard nobody has watched fire proves nothing.

    ``_drive_calls`` is imported from ``tests/test_handlers.py`` rather than
    copied, so the two guards cannot come to disagree about what a call to the
    driver looks like. This case is what stops the assertion below from passing
    because the counter is broken.
    """
    assert _drive_calls(ast.parse("jobs.drive(store, job)\ndrive(store, job)\n")) == 2


def test_nothing_in_the_tagging_shell_is_named_drive():
    """Why the function is called ``advance``, asserted where it can be checked.

    ``tests/test_handlers.py`` asserts that exactly one place in the package
    calls the job driver, and it counts every ``ast.Call`` whose callee is NAMED
    ``drive``. A function of that name here would read to that guard as a second
    caller, so the assertion covers a DEFINITION as well as a call: naming the
    function ``drive`` breaks a file this module has never heard of.
    """
    tree = ast.parse(SHELL_SOURCE.read_text(encoding="utf-8"))

    assert _drive_calls(tree) == 0
    defined = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    assert "drive" not in defined, defined


# ---------------------------------------------------------------------------
# Where one item's report is staged, and where it lands
# ---------------------------------------------------------------------------


def test_an_item_identifier_holding_a_separator_cannot_escape_the_directory(store, cfg):
    """The reason the filename is the ordinal, driven with an identifier that tries.

    A tagging item identifier is a file path relative to the folder being
    swept, so it holds separators as a matter of course and a filename built
    from one is a path traversal wearing a report. The adoption copy of this
    helper faced a database row identifier, which made the same rule easier to
    take on faith.
    """
    job = a_job(store, cfg, "../../escape.flac")
    item = jobs.items(store, job.job_id)[0]

    produced = artifacts.produced(cfg, job, item, {"outcome": "tagged"})
    jobs.commit_artifact(produced.staged, produced.final)

    assert produced.final.name == "0000.json"
    assert produced.final.parent.name == job.job_id
    assert "escape.flac" not in str(produced.final)
    assert produced.final.resolve().is_relative_to(jobs.store_dir(cfg).resolve())
    assert artifacts.committed(cfg, job.job_id) == ({"outcome": "tagged"},)


def test_staging_is_cleared_before_an_attempt_writes_into_it(cfg):
    """A half written report from an attempt that died is not this attempt's.

    Left in place it would be committed by the next attempt as though it
    described that attempt, which is a report that is wrong rather than missing.
    """
    first = artifacts.staged_path(cfg, "job-one", 3)
    first.write_text("half a report", encoding="utf-8")
    stray = first.parent / "left-behind.json"
    stray.write_text("{}", encoding="utf-8")

    second = artifacts.staged_path(cfg, "job-one", 3)

    assert second == first
    assert not second.exists()
    assert not stray.exists()


def test_staging_sits_on_the_same_filesystem_as_the_place_it_is_committed_to(cfg):
    """Why staging is a SIBLING rather than a temp directory.

    ``jobs.commit_artifact`` is an ``os.replace``, which is atomic only within
    one filesystem. A temp directory is free to be on another one, and the
    failure that buys is a cross device rename at the moment of commit, after
    the work is already done. Asserted as a shared device rather than as a
    shared string, because the device is the property and the path is the means.
    """
    final = artifacts.final_path(cfg, "job-one", 0)
    staged = artifacts.staged_path(cfg, "job-one", 0)
    root = jobs.store_dir(cfg)

    assert final.parents[2] == root
    assert staged.parents[3] == root
    assert os.stat(final.parent).st_dev == os.stat(staged.parent).st_dev


def test_reports_past_the_four_digit_name_come_back_in_item_order(cfg):
    """The sort key is the ordinal as a NUMBER, and a folder can reach that far.

    The name is ``{ordinal:04d}.json``, so four digits sort as text in item
    order and the ten thousandth does not: ``"10000"`` sorts before ``"9999"``.
    A folder of audio files holding ten thousand entries is reachable input, so
    two reports at the boundary are enough to tell the two sorts apart.
    """
    for ordinal in (10000, 9999):
        artifacts.write(
            artifacts.final_path(cfg, "job-one", ordinal), {"ordinal": ordinal}
        )

    assert [report["ordinal"] for report in artifacts.committed(cfg, "job-one")] == [
        9999,
        10000,
    ]


def test_a_report_that_cannot_be_parsed_is_skipped_rather_than_raised_on(cfg):
    """A summary is a display over work that already happened.

    Refusing to report would turn one unreadable file into a verb that can tell
    a person nothing about any of the other items, all of whose work is done and
    committed.
    """
    artifacts.write(artifacts.final_path(cfg, "job-one", 0), {"outcome": "tagged"})
    artifacts.final_path(cfg, "job-one", 1).write_text("{ not json", encoding="utf-8")
    artifacts.final_path(cfg, "job-one", 2).write_text('"a string"', encoding="utf-8")
    artifacts.write(artifacts.final_path(cfg, "job-one", 3), {"outcome": "skipped"})

    assert artifacts.committed(cfg, "job-one") == (
        {"outcome": "tagged"},
        {"outcome": "skipped"},
    )


def test_a_job_that_committed_nothing_reads_back_as_nothing(cfg):
    """No directory is not an error. It is a job whose first item has not landed."""
    assert artifacts.committed(cfg, "never-ran") == ()


def test_a_written_report_is_sorted_json_so_two_runs_produce_one_file(cfg):
    path = artifacts.write(
        artifacts.final_path(cfg, "job-one", 0), {"b": 2, "a": 1}
    )

    text = path.read_text(encoding="utf-8")
    assert text.index('"a"') < text.index('"b"')
    assert json.loads(text) == {"a": 1, "b": 2}


def test_the_two_directory_names_are_the_tagging_ones(cfg):
    """The only thing this copy changes from the adoption one, so it is asserted.

    A port that kept ``adopt-artifacts`` would file every tagging report under
    the adoption verb's directory, where the adoption summary would then read
    them back as its own.
    """
    assert artifacts.ARTIFACTS_DIRNAME == "tag-artifacts"
    assert artifacts.STAGING_DIRNAME == "tag-staging"
    assert artifacts.final_path(cfg, "job-one", 0).parents[1].name == "tag-artifacts"
    assert artifacts.staged_path(cfg, "job-one", 0).parents[2].name == "tag-staging"


def test_the_artifact_helper_never_resolves_the_queue_root_for_itself():
    """KTD9's defect wearing an indirection, asserted where it is visible.

    ``jobs.store_dir()`` with no argument loads the CURRENT configuration, and a
    resume that ran against a configuration somebody edited since the job was
    queued is the bug KTD9 exists to close. The handler guard in
    ``tests/test_handlers.py`` reads spellings of a reload inside a handler
    BODY, and cannot follow one through a helper this module owns, so the
    property is asserted here by parsing.

    It cannot be asserted by behaviour today. The queue is installation scoped,
    so ``store_dir`` returns the same directory whichever configuration it
    reads, and the two calls are indistinguishable from outside until the day
    that scoping changes. That is precisely the kind of property that survives
    only as a guard over the source.
    """
    tree = ast.parse(ARTIFACTS_SOURCE.read_text(encoding="utf-8"))
    bare: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        callee = node.func
        named = (
            callee.attr
            if isinstance(callee, ast.Attribute)
            else callee.id
            if isinstance(callee, ast.Name)
            else ""
        )
        if named in {"store_dir", "queue_path", "load", "load_from_path"} and not (
            node.args or node.keywords
        ):
            bare.append(named)
    assert not bare, (
        "the queue root must come from the configuration the job froze, passed "
        f"in as a parameter; these calls resolve it for themselves: {bare}"
    )
