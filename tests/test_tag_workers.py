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

U4 APPENDED THE SECOND HALF, and the first sentence above is no longer the whole
story. The section at the foot of this file drives ``crate tag folder`` end to
end through the real dispatcher, so the shell and the artifact helper are now
asserted twice: once as properties of their own, and once as the thing a verb
stands on while it tags real files. The two halves are kept in one file because
the second is what the first exists for, and splitting them would let a change
to one pass while the other went unread.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path

import pytest

from cratekit.cli import handlers, output, registry
from cratekit.core import config, jobs, tags
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.tagging import artifacts, searchers, shell, tag
from cratekit.tagging.tag import SearchHit
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_handlers import _drive_calls

# THE FIXTURE BUILDERS ARE IMPORTED RATHER THAN COPIED. ``place`` is one opinion
# about what a real audio file carrying a genre is, and ``answering`` is one
# opinion about what a fake searcher remembers being asked. A second copy of
# either is a second opinion, and the copy that drifts is whichever one the next
# change does not touch. ``SPECIFIC`` is read off the same module so the genre
# this suite writes is the one the engine suite already proved writable.
from tests.test_tagging_engine import SPECIFIC, answering, place

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


# ---------------------------------------------------------------------------
# U4: ``crate tag folder`` walking a real folder, end to end
# ---------------------------------------------------------------------------
#
# EVERY CASE BELOW GOES THROUGH THE VERB rather than through :func:`handle`. The
# binding is half of what this unit lands, and a test that called the worker
# directly would pass against a handler key still sitting in
# ``HANDLERS_NOT_YET_BOUND``, which is the exact state this unit leaves behind.


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One real FLAC container, synthesized once and copied per file.

    A real container rather than a stub, because the write under test goes all
    the way through ``core.tags.write_genre`` and is read back off the file.
    """
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def folder(tmp_path) -> Path:
    """A download folder OUTSIDE the library, which is where tagging happens.

    ``crate tag folder`` is the verb a person points at what they just
    downloaded, before any of it is in the library, so a fixture that put these
    files under the library root would be asserting about a case the verb does
    not have.
    """
    out = tmp_path / "downloads"
    out.mkdir()
    return out


def bound(monkeypatch, searcher):
    """Bind ``searcher`` where the worker looks one up (KTD11, R23).

    The worker calls ``searchers.for_taxonomy`` at CALL TIME rather than
    constructing a searcher inline, and this is the whole reason for that: a
    fixed three argument ``ItemHandler`` leaves a test nowhere else to hand a
    fake in, and without one every case below would touch the network.
    """
    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared=None: searcher)
    return searcher


def raising_on(searcher, title: str):
    """``searcher``, except that one title raises the way the shipped one does.

    ``catalogue-unreachable`` rather than an invented exception, because what is
    under test is the path a real sweep takes when a network drops out part way
    through a folder, and the shipped searcher raises exactly this.
    """

    def wrapped(artist: str, name: str):
        if name == title:
            searcher.asked.append((artist, name))
            raise refuse(
                searchers.UNREACHABLE_REASON,
                f"no catalogue could be read, so nothing is known about {name!r}",
                remedy=Remedy.RETRY_LATER,
                origin=("tagging", "searchers"),
            )
        return searcher(artist, name)

    wrapped.asked = searcher.asked  # type: ignore[attr-defined]
    return wrapped


def hit(source_genre: str, genre: str | None = None) -> SearchHit:
    """One catalogue answer, carrying what it answered even when it declines.

    A decline that cannot say what it declined is one nobody can act on, which
    is the property R24's report stands on.
    """
    return SearchHit(genre=genre, source=searchers.BEATPORT, source_genre=source_genre)


def tag_job():
    """The one ``tag.folder`` job in the installation's queue."""
    with jobs.open_store() as store:
        held = [
            job
            for job in jobs.list_jobs(store)
            if job.handler_key == registry.entry("tag.folder").handler_key
        ]
    assert len(held) == 1, f"expected exactly one tagging job, found {len(held)}"
    return held[0]


def resume_argv(job_id: str) -> list[str]:
    """The command line the job driver would spawn for this job.

    THROUGH THE REAL ``argv_for`` rather than by hand, because the property
    under test is that the frozen folder survives the round trip. A hand written
    resume would assert about a string this test typed.
    """
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def item_states(job_id: str) -> dict[str, jobs.ItemState]:
    with jobs.open_store() as store:
        return {item.item_id: item.state for item in jobs.items(store, job_id)}


def item_causes(job_id: str) -> dict[str, str]:
    with jobs.open_store() as store:
        return {
            item.item_id: item.cause.reason
            for item in jobs.items(store, job_id)
            if item.cause is not None
        }


# ---------------------------------------------------------------------------
# The binding
# ---------------------------------------------------------------------------


def test_the_tag_folder_key_resolves_to_a_worker():
    """The R-203 half this unit closes, asserted against the table itself.

    ``tests/test_handlers.py`` derives its population from the registry and
    checks that every queued verb is in exactly ONE of the two mappings, which a
    key sitting in ``HANDLERS_NOT_YET_BOUND`` satisfies perfectly. Only an
    assertion naming this key can tell "declared as unbound" from "bound".
    """
    key = registry.entry("tag.folder").handler_key

    assert handlers.is_known(key), f"{key} still has no worker"
    assert handlers.unbound_reason(key) is None
    assert callable(handlers.resolve(key))


# ---------------------------------------------------------------------------
# The happy path
# ---------------------------------------------------------------------------


def test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third(
    cfg, folder, silence, monkeypatch
):
    """The whole seam in one case: queue, drive, write, and read back.

    THE FILES ARE READ BACK OFF DISK rather than taken from the report. A worker
    that reported a genre it never wrote would drive every item to done and the
    counts would still add up, which is the clean-report-over-unwritten-state
    shape the merge bar names.

    THE THIRD FILE IS THE ONE WORTH HAVING. Fill if empty is the policy this
    verb exists to hold, so a file that already carries somebody's curation must
    come back as a skip with a reason rather than as a write.
    """
    place(folder, silence, "a")
    place(folder, silence, "b")
    place(folder, silence, "c", genre=SPECIFIC)
    searcher = bound(
        monkeypatch,
        answering({"a": hit("deep house", SPECIFIC), "b": hit("deep house", SPECIFIC)}),
    )

    code, queued = drive(["tag", "folder", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = tag_job()
    assert list(item_states(job.job_id)) == ["a.flac", "b.flac", "c.flac"], (
        "the items are the engine's own walk, relative to the folder and sorted"
    )

    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed

    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    assert tags.read_genre_from_file(folder / "b.flac") == SPECIFIC
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert searcher.asked == [("", "a"), ("", "b")], (
        "the file that already carried a genre was asked about anyway"
    )

    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert len(reports) == 3, reports
    assert reports["a.flac"]["genre_written"] == SPECIFIC
    assert reports["c.flac"]["genre_written"] is None
    assert reports["c.flac"]["skipped"] == tag.HAS_GENRE


def test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged(
    cfg, folder, silence, monkeypatch
):
    """The walk recurses, so an identifier holding a separator is ordinary input.

    A download folder is a folder of release directories more often than it is a
    flat list, and the identifier is the path relative to the frozen folder. That
    makes ``sub/deep.flac`` the common case rather than the exotic one: the
    worker has to join it back onto the payload's folder, and the artifact
    helper has to name the report after the ORDINAL rather than after this
    string, which the traversal case above already pins.
    """
    place(folder / "sub", silence, "deep")
    bound(monkeypatch, answering({"deep": hit("deep house", SPECIFIC)}))

    drive(["tag", "folder", str(folder)])
    job = tag_job()
    assert list(item_states(job.job_id)) == [str(Path("sub") / "deep.flac")]

    code, resumed = drive(resume_argv(job.job_id))

    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(folder / "sub" / "deep.flac") == SPECIFIC


def test_the_skip_reason_reaches_the_report_and_not_only_the_artifact(
    cfg, folder, silence, monkeypatch
):
    """R16 at the surface a person reads.

    A reason that reaches the committed artifact and stops there is a reason
    somebody has to go and find on disk. The counts ride under ``progress``,
    which is the one place ``job_state/1`` leaves open for a per verb detail.
    """
    place(folder, silence, "a")
    place(folder, silence, "b", genre=SPECIFIC)
    bound(monkeypatch, answering({}))

    drive(["tag", "folder", str(folder)])
    job = tag_job()
    _code, resumed = drive(resume_argv(job.job_id))

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["skipped"][tag.HAS_GENRE] == 1
    assert tagging["skipped"][tag.NO_HIT] == 1
    assert tagging["tagged"] == 0
    assert set(tagging["skipped"]) == {tag.HAS_GENRE, tag.NO_HIT, tag.UNMAPPED_GENRE}, (
        "a summary listing only the reasons it saw cannot tell 'none of those "
        "here' from 'this build does not count them'"
    )


def test_the_report_names_each_unresolved_source_genre_with_its_count(
    cfg, folder, silence, monkeypatch
):
    """R24, and the reason a bare ``unmapped-genre`` total is not enough.

    An unmapped count tells a person a gap exists. The STRING tells them which
    alias their own taxonomy is missing, which is the only half of it they can
    act on.
    """
    for name in ("a", "b", "c"):
        place(folder, silence, name)
    bound(
        monkeypatch,
        answering({"a": hit("gqom"), "b": hit("gqom"), "c": hit("footwork")}),
    )

    drive(["tag", "folder", str(folder)])
    job = tag_job()
    _code, resumed = drive(resume_argv(job.job_id))

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["unresolved"] == {"gqom": 2, "footwork": 1}
    assert tagging["skipped"][tag.UNMAPPED_GENRE] == 3
    assert [report["source_genre"] for report in artifacts.committed(cfg, job.job_id)] == [
        "gqom",
        "gqom",
        "footwork",
    ]


def test_the_counts_are_read_off_the_artifacts_rather_than_accumulated_in_memory(
    cfg, folder, silence, monkeypatch
):
    """What makes the number true across a resume.

    A sweep that tagged three of five files and is continued tomorrow has five
    reports on disk, and the person asking what happened means all five. The
    total is asserted against what the queue committed rather than against a
    literal, so a summary that counted only this invocation's work fails here.
    """
    for name in ("a", "b", "c"):
        place(folder, silence, name)
    bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))

    drive(["tag", "folder", str(folder)])
    job = tag_job()
    _code, resumed = drive(resume_argv(job.job_id))

    tagging = resumed["data"]["progress"]["tagging"]
    counted = tagging["tagged"] + sum(tagging["skipped"].values())
    assert counted == len(artifacts.committed(cfg, job.job_id))
    assert counted == resumed["data"]["progress"]["total"]


# ---------------------------------------------------------------------------
# The two zeroes, which are not one zero
# ---------------------------------------------------------------------------


def test_a_folder_holding_no_audio_queues_nothing_and_says_which_zero_it_is(
    cfg, folder
):
    """AE3. Nothing is queued, and the exit code is still success.

    ``core.jobs`` reports a job with no items as SUCCEEDED by design, so a verb
    that queued one here would report a clean tagging sweep over a folder
    nothing walked.
    """
    (folder / "cover.jpg").write_bytes(b"not audio")

    code, envelope = drive(["tag", "folder", str(folder)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert [warning["code"] for warning in envelope["warnings"]] == ["tag-folder-no-audio"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_an_empty_folder_argument_never_sweeps_the_working_directory(
    cfg, folder, silence, monkeypatch
):
    """The third zero, and the only one of them that is dangerous.

    An empty string is a VALID argument to a positional that takes one, so the
    parser accepts it and ``Path("")`` is the current directory. This verb writes
    to files, so resolving an unnamed folder to whatever the person happens to be
    standing in is a sweep of their working directory that nobody asked for.
    ``tag.retag`` refuses the same argument under
    ``tag-retag-folder-unknown`` for exactly this reason.

    A NO_OP RATHER THAN A REFUSAL, and that is a limit of this unit rather than a
    judgement: a refusal needs a slug of its own in ``cause.REASONS`` and reusing
    the correction verb's would put that verb's name on this one's failure. What
    matters either way is that nothing is queued and nothing is written.

    ASSERTED WITH AUDIO IN THE WORKING DIRECTORY, because the reason this is
    worth a test at all is that it passes trivially anywhere there is none.
    """
    place(folder, silence, "a")
    monkeypatch.chdir(folder)

    code, envelope = drive(["tag", "folder", ""])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert [warning["code"] for warning in envelope["warnings"]] == ["tag-folder-unnamed"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()
    assert tags.read_genre_from_file(folder / "a.flac") in (None, "")


def test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one(cfg, tmp_path):
    """Both walk to nothing, and the person's next move is different for each.

    One says put some audio in it, the other says you named a folder that does
    not exist. Folding them into one warning makes a typed path look like an
    empty download directory.
    """
    code, envelope = drive(["tag", "folder", str(tmp_path / "no-such-folder")])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert [warning["code"] for warning in envelope["warnings"]] == ["tag-folder-absent"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


# ---------------------------------------------------------------------------
# The failure part way through, and the resume that follows it
# ---------------------------------------------------------------------------


def test_a_searcher_that_raises_part_way_fails_only_its_own_item(
    cfg, folder, silence, monkeypatch
):
    """R19x's first half, and the reason a decline and a refusal are not one thing.

    The searcher raises when it could not READ a catalogue at all, which is a
    network dropping out mid folder. That item fails, the two either side of it
    are done and stay written, and the job carries a cause, so nobody is told
    the folder was tagged.
    """
    for name in ("a", "b", "c"):
        place(folder, silence, name)
    table = {name: hit("deep house", SPECIFIC) for name in ("a", "b", "c")}
    bound(monkeypatch, raising_on(answering(table), "b"))

    drive(["tag", "folder", str(folder)])
    job = tag_job()
    code, resumed = drive(resume_argv(job.job_id))

    assert code != int(ExitCode.OK), resumed
    assert item_states(job.job_id) == {
        "a.flac": jobs.ItemState.DONE,
        "b.flac": jobs.ItemState.FAILED,
        "c.flac": jobs.ItemState.DONE,
    }
    assert item_causes(job.job_id) == {"b.flac": searchers.UNREACHABLE_REASON}
    with jobs.open_store() as store:
        assert jobs.get(store, job.job_id).state is jobs.JobState.FAILED
        assert jobs.get(store, job.job_id).cause is not None
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    assert tags.read_genre_from_file(folder / "c.flac") == SPECIFIC
    assert tags.read_genre_from_file(folder / "b.flac") in (None, "")


def test_a_retried_job_drives_only_the_item_that_failed(
    cfg, folder, silence, monkeypatch
):
    """R19x, and the guarantee this whole seam exists for.

    ASSERTED BY COUNTING THE SEARCHER'S CALLS rather than by reading the item
    states, because a resume that re-asked the catalogue about two files it had
    already tagged would leave exactly the same states behind and would cost the
    person two more requests against a rate limited source every time.
    """
    for name in ("a", "b", "c"):
        place(folder, silence, name)
    table = {name: hit("deep house", SPECIFIC) for name in ("a", "b", "c")}
    bound(monkeypatch, raising_on(answering(table), "b"))
    drive(["tag", "folder", str(folder)])
    job = tag_job()
    drive(resume_argv(job.job_id))

    second = bound(monkeypatch, answering(table))
    with jobs.open_store() as store:
        jobs.retry(store, job.job_id)
    code, resumed = drive(resume_argv(job.job_id))

    assert code == int(ExitCode.OK), resumed
    assert second.asked == [("", "b")], (
        "the resume re-attempted work whose artifact was already durable"
    )
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert tags.read_genre_from_file(folder / "b.flac") == SPECIFIC
    assert len(artifacts.committed(cfg, job.job_id)) == 3


def test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name(
    cfg, folder, silence, monkeypatch
):
    """R15. The folder is not frozen, so this is reachable input.

    Refused with its own slug rather than reported done: an item that reported
    done having tagged nothing is the clean-report-over-unreadable-state cost
    ``docs/METHOD.md`` names. It is not an internal error either, because a
    person deleting a file out of their own download folder is not a defect.
    """
    for name in ("a", "b"):
        place(folder, silence, name)
    bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))

    drive(["tag", "folder", str(folder)])
    job = tag_job()
    (folder / "b.flac").unlink()
    code, resumed = drive(resume_argv(job.job_id))

    assert code != int(ExitCode.OK), resumed
    assert item_states(job.job_id) == {
        "a.flac": jobs.ItemState.DONE,
        "b.flac": jobs.ItemState.FAILED,
    }
    assert item_causes(job.job_id) == {"b.flac": "source-missing"}


# ---------------------------------------------------------------------------
# The resume argv
# ---------------------------------------------------------------------------


def test_the_resume_argv_round_trips_the_frozen_folder_and_asks_for_no_run(
    cfg, folder, silence, monkeypatch
):
    """The payload is frozen at queue time, so only the verb can rebuild it.

    ``--run`` IS ASSERTED AS A WHOLE TOKEN. ``--run-id`` contains ``--run`` as a
    substring, so a membership check over the joined string would call a broken
    argv clean, and this project has reported exactly that once already. This
    verb declares no gate, so a resume that minted a run would be asking a
    question nobody had posed.
    """
    place(folder, silence, "a")
    bound(monkeypatch, answering({}))

    drive(["tag", "folder", str(folder)])
    job = tag_job()

    argv = resume_argv(job.job_id)

    assert argv == ["tag", "folder", job.payload["folder"], "--job", job.job_id]
    assert Path(job.payload["folder"]) == folder
    assert "--run" not in argv, argv
