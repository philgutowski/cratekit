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

from cratekit.acquire import cli as acquire_cli
from cratekit.cli import handlers, output, registry
from cratekit.core import art, config, jobs, review, tags
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.tagging import artifacts, retag, retag_cli, searchers, shell, tag
from cratekit.tagging import cli as tag_cli
from cratekit.tagging.tag import SearchHit
from tests._containers import synth_container
from tests.cli_drive import approve_and_queue, drive
from tests.test_config import valid_data
from tests.test_handlers import _drive_calls

# THE FIXTURE BUILDERS ARE IMPORTED RATHER THAN COPIED. ``place`` is one opinion
# about what a real audio file carrying a genre is, and ``answering`` is one
# opinion about what a fake searcher remembers being asked. A second copy of
# either is a second opinion, and the copy that drifts is whichever one the next
# change does not touch. ``SPECIFIC`` is read off the same module so the genre
# this suite writes is the one the engine suite already proved writable, and
# ``CATCH_ALL`` so the value ``tag.retag`` selects on is the taxonomy's own
# rather than a string typed here that a template edit would leave behind.
from tests.test_tagging_engine import CATCH_ALL, SPECIFIC, TAXONOMY, answering, place

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
    come back as a skip with a reason rather than as a write. It carries a
    picture as well, because since U85 a tagged file with none is asked for art.
    """
    from tests.test_tagging_engine import _jpeg, plant

    place(folder, silence, "a")
    place(folder, silence, "b")
    plant(place(folder, silence, "c", genre=SPECIFIC), _jpeg(320, 200), dims=(320, 200, 24))
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


def test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status(
    cfg, folder, silence, monkeypatch
):
    """U84. The repair runs on every item and its status reaches both surfaces.

    Two files carry the vendored downloader's zeroed block, one of them already
    tagged, which is the file the source system repaired and a repair placed
    after the genre skip would never reach. The third carries no picture. Every
    status the repair can report is present in the counts, zeroes included.
    """
    from tests.test_tagging_engine import _jpeg, blocks, plant

    for name, genre in (("a", None), ("b", SPECIFIC), ("c", None)):
        path = place(folder, silence, name, genre=genre)
        if name != "c":
            plant(path, _jpeg(320, 200))
    bound(monkeypatch, answering({}))

    drive(["tag", "folder", str(folder)])
    job = tag_job()
    _code, resumed = drive(resume_argv(job.job_id))

    reports = artifacts.committed(cfg, job.job_id)
    assert [report["art_repair"] for report in reports] == [
        art.REPAIR_FIXED,
        art.REPAIR_FIXED,
        art.REPAIR_NONE,
    ]
    assert reports[0]["art_repair_detail"] == "1 of 1 pictures re-encoded"
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["art_repair"] == {
        art.REPAIR_FIXED: 2,
        art.REPAIR_OK: 0,
        art.REPAIR_NONE: 1,
        art.REPAIR_ERROR: 0,
        art.REPAIR_UNCHECKED: 0,
    }
    assert tagging["skipped"][tag.HAS_GENRE] == 1
    for name in ("a", "b"):
        (block,) = blocks(folder / f"{name}.flac")
        assert (block.width, block.height, block.depth) == (320, 200, 24)


def test_a_report_from_before_the_repair_is_counted_under_no_status(cfg, store):
    """A committed report carrying no status says nothing about the art.

    Counting it as ``ok`` or ``none`` would state a status nobody measured.
    """
    job = a_job(store, cfg, "old.flac")
    (item,) = jobs.items(store, job.job_id)
    produced = artifacts.produced(
        cfg, job, item, {"item": "old.flac", "genre_written": None, "skipped": tag.NO_HIT}
    )
    produced.final.parent.mkdir(parents=True, exist_ok=True)
    produced.staged.replace(produced.final)

    summary = tag_cli._summary(cfg, job.job_id)

    assert summary["art_repair"] == dict.fromkeys(art.REPAIR_STATUSES, 0)
    assert summary["art_fetch"] == dict.fromkeys(tag.ART_FETCH_STATUSES, 0)
    assert summary["skipped"][tag.NO_HIT] == 1


def test_new_art_reaches_the_file_the_artifact_and_the_summary(
    cfg, folder, silence, monkeypatch
):
    """U85 through the verb. The worker looks its image fetch up at call time.

    Four files: no genre and no picture, a genre and no picture, a genre and a
    picture, and one whose picture 404s. The first two get art, the third is
    never asked, and the fourth still gets its genre and says its art was
    unavailable, with every status counted, zeroes included.
    """
    from tests.test_tagging_engine import _jpeg, blocks, plant

    place(folder, silence, "a")
    place(folder, silence, "b", genre=SPECIFIC)
    plant(place(folder, silence, "c", genre=SPECIFIC), _jpeg(320, 200), dims=(320, 200, 24))
    place(folder, silence, "d")

    def art_hit(name: str) -> SearchHit:
        return SearchHit(
            genre=SPECIFIC,
            source=searchers.BEATPORT,
            source_genre="deep house",
            art_url=f"https://example.test/{name}.jpg",
        )

    searcher = bound(monkeypatch, answering({name: art_hit(name) for name in "abcd"}))
    fetched: list[str] = []

    def fetch_image(url: str) -> bytes | None:
        fetched.append(url)
        return None if url.endswith("/d.jpg") else _jpeg(1000, 1000)

    monkeypatch.setattr(searchers, "for_images", lambda: fetch_image)

    drive(["tag", "folder", str(folder)])
    job = tag_job()
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed

    assert [asked for _artist, asked in searcher.asked] == ["a", "b", "d"]
    assert fetched == [f"https://example.test/{name}.jpg" for name in ("a", "b", "d")]
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert {name: reports[f"{name}.flac"]["art_fetch"] for name in "abcd"} == {
        "a": tag.ART_EMBEDDED,
        "b": tag.ART_EMBEDDED,
        "c": tag.ART_PRESENT,
        "d": tag.ART_UNAVAILABLE,
    }
    assert "d.jpg" in reports["d.flac"]["art_fetch_detail"]
    assert tags.read_genre_from_file(folder / "d.flac") == SPECIFIC
    assert blocks(folder / "d.flac") == []
    for name in ("a", "b"):
        (block,) = blocks(folder / f"{name}.flac")
        assert (block.width, block.height, block.depth) == (800, 800, 24)
    assert tags.read_genre_from_file(folder / "b.flac") == SPECIFIC
    assert resumed["data"]["progress"]["tagging"]["art_fetch"] == {
        tag.ART_EMBEDDED: 2,
        tag.ART_PRESENT: 1,
        tag.ART_UNAVAILABLE: 1,
        tag.ART_ERROR: 0,
        tag.ART_UNCHECKED: 0,
    }


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


def test_tagging_the_download_root_queues_nothing_from_the_acquisition_staging_tree(
    cfg, folder, silence
):
    """R-289's measured cost, reproduced through the shipped verb.

    The folder a person points this at is their download staging root, and
    ``acquire`` stages every item of every job under a dot directory inside it.
    Before the dot skip this verb queued one item per staged file, which is the
    partial download a killed attempt left and the landing ``checked_landing``
    refused on the lossless policy and left in place as evidence. Both are
    files the person never asked to have tagged and the second is evidence a
    tag write would alter.

    A fourth zero, and it reports as the SAME zero as an empty folder, which is
    correct: there genuinely is no audio here this build should tag, and the
    person's next move is to put some in.
    """
    staged = folder / acquire_cli.ACQUIRE_STAGING_DIRNAME / "job-1" / "0" / "partial"
    place(staged.parent, silence, staged.name)

    code, envelope = drive(["tag", "folder", str(folder)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert [warning["code"] for warning in envelope["warnings"]] == ["tag-folder-no-audio"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_real_track_beside_the_staging_tree_is_still_queued(cfg, folder, silence):
    """The other half, because the test above passes for a verb that queues NOTHING.

    A download root normally holds committed tracks as well as the staging
    tree, and skipping the tree must not cost the person the sweep they asked
    for. The item identifier is asserted too, since it is derived relative to
    the frozen folder and a skipped directory changes nothing about that.
    """
    place(folder, silence, "committed")
    staged = folder / acquire_cli.ACQUIRE_STAGING_DIRNAME / "job-1" / "0" / "partial"
    place(staged.parent, silence, staged.name)

    code, envelope = drive(["tag", "folder", str(folder)])

    assert code == int(ExitCode.OK), envelope
    assert list(item_states(tag_job().job_id)) == ["committed.flac"]


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

    Refused rather than reported done: an item that reported done having
    tagged nothing is the clean-report-over-unreadable-state cost
    ``docs/METHOD.md`` names. The slug is the SHARED ``source-missing`` rather
    than one of this verb's own, which is R-251 in the ledger and a recorded
    decision rather than an oversight. It is not an internal error either, because a
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


# ---------------------------------------------------------------------------
# U5: ``crate tag retag`` from the confirmation to the corrected file
# ---------------------------------------------------------------------------
#
# EVERY CASE BELOW GOES THROUGH THE VERB, for the reason the U4 section gives:
# the binding is half of what this unit lands, and a case that called
# :func:`cratekit.tagging.retag_cli.handle` directly would pass against a handler
# key still sitting in ``HANDLERS_NOT_YET_BOUND``.
#
# AND EVERY ONE OF THEM ANSWERS THE GATE THROUGH ``approve_and_queue``, which is
# R34's two acts rather than one. A helper that answered the confirmation inline
# would be asserting that a destructive sweep can be approved by the very
# invocation that discovered it needed approving, which is what the contract
# forbids.

#: The confirmation this verb raises over its plan. Spelled once here so the
#: cases below cannot disagree with each other about which gate they answered.
RETAG_GATE = "tag.retag.confirm"


@pytest.fixture
def repair_on(cfg) -> config.Config:
    """``cfg`` with the module that gates this verb switched on.

    ``tag.retag`` is gated by ``repair`` and the fixture above configures the
    SLIM profile, under which every module row is off, so the parser does not
    offer the verb at all: the first drive of it here failed with ``invalid
    choice: 'retag'`` rather than with anything about tagging. Turning the module
    on is what makes the verb reachable, and reaching it through the real
    dispatcher is the whole point of this section.
    """
    built = config.from_dict(
        valid_data(Path(cfg.library.root), modules={"repair": True})
    )
    config.save(built)
    config.reset_cache()
    return built


def coarse(folder: Path, silence: Path, name: str) -> Path:
    """One file carrying the catch-all this verb exists to replace.

    The value is the declared taxonomy's own rather than a word typed here, so a
    template edit moves the fixture with it instead of leaving these cases
    asserting about a genre nobody calls too coarse any more.
    """
    return place(folder, silence, name, CATCH_ALL)


def selected(folder: Path) -> list[Path]:
    """What a fresh walk of the folder would take, as it stands right now."""
    return [
        candidate.path for candidate in retag.select(folder, declared=TAXONOMY).candidates
    ]


def test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale(
    repair_on, folder, silence, monkeypatch
):
    """KTD8 and AE4, and the permanent stall this unit would otherwise ship.

    THE DEFECT IS UNREACHABLE UNTIL A WORKER WRITES, which is what makes it this
    unit's. ``retag_genres`` rebuilt its plan by walking the folder on every
    invocation, the resume included. A corrected file carries a specific genre,
    so the next walk does not select it, so the plan digests differently from the
    one the person's confirmation was recorded against, so ``ctx.gate.require``
    raises ``DecisionStale``. Every respawn after the first partial run meets it,
    for ever, over work somebody already approved.

    THE CORRECTION IS WRITTEN HERE RATHER THAN DRIVEN, and that is the honest
    way round. The only effect a worker has on the folder is
    ``core.tags.write_genre``, and the mechanism under test is the SELECTION
    shrinking rather than the route by which it shrank, so this stands in for a
    run that was killed after its first item and can be measured against the code
    as it stood before the split.
    """
    for name in ("a", "b", "c"):
        coarse(folder, silence, name)
    bound(monkeypatch, answering({name: hit("deep house", SPECIFIC) for name in "bc"}))

    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    assert tags.write_genre(folder / "a.flac", SPECIFIC), "the stand-in write failed"
    assert selected(folder) == [folder / "b.flac", folder / "c.flac"], (
        "the selection did not shrink, so this case cannot see the stall it is for"
    )

    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(folder / "b.flac") == SPECIFIC
    assert tags.read_genre_from_file(folder / "c.flac") == SPECIFIC
    assert set(item_states(job_id).values()) == {jobs.ItemState.DONE}


def queued_jobs() -> tuple:
    """Every job in the installation's queue, whichever verb queued it."""
    with jobs.open_store() as store:
        return jobs.list_jobs(store)


def retag_reports(cfg: config.Config, job_id: str) -> dict:
    """This job's committed reports, keyed by the item they describe."""
    return {report["item"]: report for report in artifacts.committed(cfg, job_id)}


# ---------------------------------------------------------------------------
# The binding
# ---------------------------------------------------------------------------


def test_the_tag_retag_key_resolves_to_a_worker():
    """The other half of R-203 this unit closes, asserted against the table.

    ``tests/test_handlers.py`` derives its population from the registry and
    checks that every queued verb sits in exactly ONE of the two mappings, which
    a key parked in ``HANDLERS_NOT_YET_BOUND`` satisfies perfectly. Only an
    assertion naming this key can tell "declared as unbound" from "bound".
    """
    key = registry.entry("tag.retag").handler_key

    assert handlers.is_known(key), f"{key} still has no worker"
    assert handlers.unbound_reason(key) is None
    assert callable(handlers.resolve(key))


# ---------------------------------------------------------------------------
# The happy path
# ---------------------------------------------------------------------------


def test_three_confirmed_files_go_from_pending_to_done_and_carry_a_specific_genre(
    repair_on, folder, silence, monkeypatch
):
    """The whole seam in one case: confirm, queue, drive, write, and read back.

    THE FILES ARE READ BACK OFF DISK rather than taken from the report. A worker
    that reported a genre it never wrote would drive every item to done and the
    counts would still add up, which is the clean-report-over-unwritten-state
    shape the merge bar names.

    THE ITEMS ARE THE CONFIRMED ROWS. What a person approved is the SELECTION, so
    the queue holds one item per candidate path and the job covers exactly the
    files the plan named. A shell that queued its own walk instead would be a
    second opinion about what was confirmed.
    """
    for name in ("a", "b", "c"):
        coarse(folder, silence, name)
    searcher = bound(
        monkeypatch, answering({name: hit("deep house", SPECIFIC) for name in "abc"})
    )

    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    assert list(item_states(job_id)) == [str(folder / f"{name}.flac") for name in "abc"]

    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job_id).values()) == {jobs.ItemState.DONE}
    for name in "abc":
        assert tags.read_genre_from_file(folder / f"{name}.flac") == SPECIFIC
    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.SUCCEEDED
    assert sorted(name for _artist, name in searcher.asked) == ["a", "b", "c"]
    assert resumed["data"]["progress"]["retag"]["corrected"] == 3


def test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned(
    repair_on, folder, silence, monkeypatch
):
    """R16 at the surface a person reads, and the reason it is read back off disk.

    Every one of these three files was in the plan the person confirmed, and the
    three of them did three different things. A summary accumulated in memory
    would also have to be re-accumulated on every resume, so a sweep continued
    tomorrow would report only the part of it that ran today.

    ZEROES INCLUDED, on the rule ``adopt.scan.categories`` states: a summary
    listing only the reasons it happened to see makes "none of those here" and
    "this build does not count that" the same output.
    """
    for name in ("a", "b", "c"):
        coarse(folder, silence, name)
    bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))

    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    tags.write_genre(folder / "b.flac", SPECIFIC)
    _code, resumed = drive(resume_argv(job_id))

    summary = resumed["data"]["progress"]["retag"]
    assert summary["corrected"] == 1
    assert summary["skipped"][retag.GENRE_SPECIFIC] == 1
    assert summary["skipped"][retag.NO_ANSWER] == 1
    assert summary["asked"] == 1
    assert set(summary["skipped"]) == {
        retag.NO_GENRE,
        retag.GENRE_SPECIFIC,
        retag.NO_ANSWER,
        retag.ANSWER_TOO_COARSE,
        retag.DECLINED_IN_REVIEW,
    }
    counted = summary["corrected"] + sum(summary["skipped"].values())
    assert counted == len(artifacts.committed(repair_on, job_id)) == 3


# ---------------------------------------------------------------------------
# The zeroes, which are asked about and then queue nothing
# ---------------------------------------------------------------------------


def test_an_empty_plan_is_still_asked_about_and_still_queues_nothing(
    repair_on, folder, silence
):
    """R12, and the reversal that got this verb back in line with its sibling.

    The first draft of this unit skipped the gate when the plan was empty, on the
    argument that a person's decision should not be spent on a sweep of nothing.
    Conformance 3 reported it within minutes: it holds every declared gate to
    FIRING, and a gate the registry declares and the verb sometimes skips is a
    decision the product promises and does not always ask. ``adopt/apply_cli`` had
    already answered the same question the other way, so skipping here would have
    left two sibling verbs disagreeing about what an empty plan means.

    THE FIRST DRIVE MUST REFUSE, which is what says the gate was reached. The
    confirmation is ``explicit``, so a gate met with nothing recorded against this
    run exits DECISION_REQUIRED. Asserting only the eventual no-op would pass
    against a verb that never asked.

    THE ZERO ITEM RULE IS ENFORCED AFTER IT. ``core.jobs`` drives a job with no
    items straight to SUCCEEDED, so a confirmed empty job would report a clean
    correction over a folder nothing touched.
    """
    place(folder, silence, "already-specific", SPECIFIC)

    code, refused = drive(["tag", "retag", str(folder)])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == "tag.retag.confirm"

    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, "tag.retag.confirm", "apply", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope

    code, envelope = drive(["--run", run_id, "tag", "retag", str(folder)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert [warning["code"] for warning in envelope["warnings"]] == [
        "tag-retag-nothing-coarse"
    ]
    assert queued_jobs() == ()


def test_a_folder_that_is_not_there_is_a_different_zero_from_one_with_nothing_coarse(
    repair_on, tmp_path
):
    """Both walk to nothing, and the person's next move differs for each.

    One says every genre under that folder is already specific, the other says
    the folder they named is not on this machine. Folded into one warning, a
    mistyped path reads as a library that needs no correcting, which is the
    answer most likely to stop somebody looking.

    The gate fires here too, for the reason the test above gives, and the digest
    carries the FOLDER as well as the rows, so approving one empty sweep is not
    approving another.
    """
    absent = str(tmp_path / "no-such-folder")

    code, refused = drive(["tag", "retag", absent])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, "tag.retag.confirm", "apply", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope

    code, envelope = drive(["--run", run_id, "tag", "retag", absent])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert [warning["code"] for warning in envelope["warnings"]] == ["tag-retag-folder-absent"]
    assert queued_jobs() == ()


def test_answering_the_confirmation_with_abort_queues_nothing_and_writes_nothing(
    repair_on, folder, silence, monkeypatch
):
    """The branch a person reaches by reading the plan and saying no.

    THE PAYLOAD IS THE DECLARED ``job_state`` SHAPE. This branch used to emit a
    folder, a totals mapping and a ``summary`` object, which carries none of the
    four fields ``cli.output`` requires of that surface and two it forbids, so an
    envelope a consumer generated from the committed schema would reject. Going
    through ``shell.no_op`` is what stops this verb's zero paths reintroducing
    R-234 separately from the sibling verb's. ``tests/cli_drive.drive`` validates
    the envelope, so this case fails on the shape as well as on the outcome.
    """
    coarse(folder, silence, "a")
    bound(monkeypatch, answering({}))

    code, refused = drive(["tag", "retag", str(folder)])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, _envelope = drive(
        ["run", "decide", run_id, RETAG_GATE, "abort", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK)

    code, envelope = drive(["--run", run_id, "tag", "retag", str(folder)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert envelope["data"]["state"] == "declined"
    assert queued_jobs() == ()
    assert tags.read_genre_from_file(folder / "a.flac") == CATCH_ALL


# ---------------------------------------------------------------------------
# The file moved between the confirmation and the drive
# ---------------------------------------------------------------------------


def test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten(
    repair_on, folder, silence, monkeypatch
):
    """Somebody corrected it already, and their curation outranks this sweep.

    The confirmed plan says this file carries a catch-all, and by drive time it
    does not. Writing anyway would make a queued job the thing that overwrites a
    person's own answer, which is the whole reason this verb re-reads the genre
    at drive time rather than trusting the frozen row.
    """
    coarse(folder, silence, "a")
    searcher = bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    by_hand = "Ambient"
    assert tags.write_genre(folder / "a.flac", by_hand)
    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(folder / "a.flac") == by_hand
    assert searcher.asked == [], "the catalogue was asked about a file nobody may write"
    report = retag_reports(repair_on, job_id)[str(folder / "a.flac")]
    assert report["reason"] == retag.GENRE_SPECIFIC
    assert report["written"] is None


def test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner(
    repair_on, folder, silence, monkeypatch
):
    """The one state two verbs could both claim, and neither may.

    An empty genre is ``tag.folder``'s field under fill-if-empty. This verb OWNS
    the value it writes, so a file with nothing in the field would be corrected
    here and filled there, and one field under two policies is how a value a
    person set by hand loses to whichever verb ran last. The taxonomy answers
    ``is_too_coarse_as_source("")`` with True, so the check has to be for the
    blank rather than for the predicate.
    """
    coarse(folder, silence, "a")
    searcher = bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    assert tags.write_genre(folder / "a.flac", "")
    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(folder / "a.flac") in (None, "")
    assert searcher.asked == []
    report = retag_reports(repair_on, job_id)[str(folder / "a.flac")]
    assert report["reason"] == retag.NO_GENRE
    assert report["written"] is None


def test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done(
    repair_on, folder, silence, monkeypatch
):
    """R15. The folder is not frozen, so this is reachable input.

    Refused rather than reported done: an item that reported done having
    corrected nothing is the clean-report-over-unreadable-state cost
    ``docs/METHOD.md`` names. The slug is the SHARED ``source-missing`` rather
    than one of this verb's own, which is R-251 in the ledger and a recorded
    decision rather than an oversight. It is not an internal error either, because a
    person deleting one of their own files is not a defect in this program.
    """
    for name in ("a", "b"):
        coarse(folder, silence, name)
    bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    (folder / "b.flac").unlink()
    code, resumed = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), resumed
    assert item_states(job_id) == {
        str(folder / "a.flac"): jobs.ItemState.DONE,
        str(folder / "b.flac"): jobs.ItemState.FAILED,
    }
    assert item_causes(job_id) == {str(folder / "b.flac"): "source-missing"}


# ---------------------------------------------------------------------------
# The review queue, reached through the worker rather than through the sweep
# ---------------------------------------------------------------------------


def test_an_answer_that_is_itself_too_coarse_reaches_the_review_queue(
    repair_on, folder, silence, monkeypatch
):
    """The engine's rule, asserted through the WORKER that now runs it.

    ``tests/test_genre_retag.py`` drives this through ``retag_folder``, which is
    a different caller with a different store: the sweep opens one review queue
    for a whole folder and the worker opens one per item, against the FROZEN
    configuration. A catch-all laundered into a file here would never be selected
    again, because writing counts as progress and re-reading the write does not.
    """
    path = coarse(folder, silence, "a")
    other = TAXONOMY.fallback.too_coarse_as_source[2]
    bound(monkeypatch, answering({"a": hit("some vendor genre", other)}))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(path) == CATCH_ALL
    with review.open_store(repair_on) as store:
        page = review.list_items(store, queue=str(review.Queue.GENRE))
    assert len(page) == 1
    assert page.items[0].payload["path"] == str(path)
    assert page.items[0].payload["proposed"] == other
    assert page.items[0].handler_key == retag.HANDLER_KEY
    report = retag_reports(repair_on, job_id)[str(path)]
    assert report["reason"] == retag.ANSWER_TOO_COARSE
    assert report["review_item"] == page.items[0].item_id


def test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked(
    repair_on, folder, silence, monkeypatch
):
    """The ordering inside the worker, and the only assertion that can see it.

    Asking the catalogue first and reading the verdict afterwards would spend a
    request per run on a question a person already answered, and would let a
    fresh answer overwrite the recorded one. Asserting the written genre alone
    passes for both implementations; asserting that the searcher was never asked
    is what separates them.
    """
    path = coarse(folder, silence, "a")
    bound(monkeypatch, answering({}))
    _first_run, first_job = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    drive(resume_argv(first_job))

    with review.open_store(repair_on) as store:
        item = review.list_items(store, queue=str(review.Queue.GENRE)).items[0]
        chosen = next(option for option in item.options if option.summary == SPECIFIC)
        review.resolve(
            store,
            item.item_id,
            review.Verdict.ACCEPTED,
            option=chosen.option_id,
            actor="a-person",
        )

    second = bound(monkeypatch, answering({"a": hit("deep house", "Techno")}))
    _second_run, second_job = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    code, resumed = drive(resume_argv(second_job))

    assert code == int(ExitCode.OK), resumed
    assert second.asked == []
    assert tags.read_genre_from_file(path) == SPECIFIC


# ---------------------------------------------------------------------------
# The failure part way through, and the resume that follows it
# ---------------------------------------------------------------------------


def test_a_searcher_that_raises_part_way_through_a_retag_fails_only_its_own_item(
    repair_on, folder, silence, monkeypatch
):
    """R19x's first half. A network dropping out mid folder is not a decline.

    The item that could not be answered fails, the two either side of it are done
    and stay written, and the job carries a cause, so nobody is told the folder
    was corrected.
    """
    for name in ("a", "b", "c"):
        coarse(folder, silence, name)
    table = {name: hit("deep house", SPECIFIC) for name in "abc"}
    bound(monkeypatch, raising_on(answering(table), "b"))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    code, resumed = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), resumed
    assert item_states(job_id) == {
        str(folder / "a.flac"): jobs.ItemState.DONE,
        str(folder / "b.flac"): jobs.ItemState.FAILED,
        str(folder / "c.flac"): jobs.ItemState.DONE,
    }
    assert item_causes(job_id) == {str(folder / "b.flac"): searchers.UNREACHABLE_REASON}
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    assert tags.read_genre_from_file(folder / "c.flac") == SPECIFIC
    assert tags.read_genre_from_file(folder / "b.flac") == CATCH_ALL


def test_a_retried_retag_drives_only_the_item_that_failed(
    repair_on, folder, silence, monkeypatch
):
    """R19x, and the guarantee the whole per item seam exists for.

    ASSERTED BY COUNTING THE SEARCHER'S CALLS rather than by reading the item
    states. A resume that re-asked the catalogue about two files it had already
    corrected would leave exactly the same states behind, and would cost the
    person two more requests against a rate limited source every single time.
    """
    for name in ("a", "b", "c"):
        coarse(folder, silence, name)
    table = {name: hit("deep house", SPECIFIC) for name in "abc"}
    bound(monkeypatch, raising_on(answering(table), "b"))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    drive(resume_argv(job_id))

    second = bound(monkeypatch, answering(table))
    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert second.asked == [("", "b")], (
        "the resume re-attempted work whose artifact was already durable"
    )
    assert set(item_states(job_id).values()) == {jobs.ItemState.DONE}
    assert tags.read_genre_from_file(folder / "b.flac") == SPECIFIC
    assert len(artifacts.committed(repair_on, job_id)) == 3


def test_an_interrupted_retag_leaves_a_library_row_stale_and_the_artifact_recovers_it(
    repair_on, folder, silence, monkeypatch
):
    """R-185 DRIVEN AND MEASURED, not repaired. The measurement is the point.

    The file half of this verb writes the genre onto the file. The database half
    is deferred, so ``retag.plan_library`` and ``retag.apply_library`` still have
    no caller anywhere in ``src`` after this unit, and the library row keeps the
    catch-all the file no longer carries.

    THE POPULATION CANNOT BE RE-DERIVED LATER FROM THE FOLDER. A corrected file
    stops being selectable the moment it is written, so a second full run sees
    nothing to do and the stale row is invisible to the selection for ever. What
    makes it recoverable at all is the committed artifact, which names the path,
    the value that was there and the value that was written, which is exactly the
    input the deferred half needs. That is asserted here so a later unit that
    drops a field from the report fails in this file rather than in a library
    nobody is looking at.
    """
    for name in ("a", "b"):
        coarse(folder, silence, name)
    bound(monkeypatch, raising_on(answering({"a": hit("deep house", SPECIFIC)}), "b"))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    drive(resume_argv(job_id))

    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    callers = {
        relative
        for relative, source in (
            (path.relative_to(SRC_ROOT), path.read_text(encoding="utf-8"))
            for path in SRC_ROOT.rglob("*.py")
        )
        if "plan_library(" in source or "apply_library(" in source
    }
    assert callers == {Path("cratekit/tagging/retag.py")}, (
        f"the database half gained a caller in {callers}, so R-185's measurement "
        f"is out of date and this case is asserting about a deferral that ended"
    )
    assert selected(folder) == [folder / "b.flac"], (
        "the corrected file is still selectable, so this case cannot see why the "
        "stale row needs the artifact to be recoverable"
    )
    report = retag_reports(repair_on, job_id)[str(folder / "a.flac")]
    assert report["path"] == str(folder / "a.flac")
    assert report["current"] == CATCH_ALL
    assert report["written"] == SPECIFIC


def warning_codes(envelope: dict) -> list[str]:
    """Every warning code on one envelope, in the order the verb attached them."""
    return [warning["code"] for warning in envelope["warnings"]]


def test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs(
    repair_on, folder, silence, monkeypatch
):
    """R-185's COST, reproduced as the thing a person is left holding.

    The two halves of this verb are measured one case above: the file is
    corrected, the library row is not, and the corrected file is never selected
    again so no later run finds its way back to that row. Everything in that case
    is about the repository. This one is about the person, and before this unit
    the answer was that nothing told them anything at all. They confirmed a
    correction, the envelope reported a clean sweep, and rekordbox went on showing
    the genre the taxonomy calls too coarse for ever.

    THE WARNING NAMES THE ACT AND NOT THE DEFECT. Reloading the folder's tags in
    rekordbox is what makes the row agree with the file, and it is the only thing
    this build can put in front of them, so the assertion is on the instruction
    rather than on the code alone: a warning that announced a disagreement and
    stopped there would satisfy a code-only check while leaving a person with
    nothing to do.

    THE FOLDER IS IN THE TEXT. A resume is a detached child whose envelope is read
    later beside other runs, so an instruction that said "the folder" would not
    say which sweep it belonged to.
    """
    for name in ("a", "b"):
        coarse(folder, silence, name)
    bound(monkeypatch, answering({name: hit("deep house", SPECIFIC) for name in "ab"}))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["progress"]["retag"]["corrected"] == 2, resumed
    assert retag_cli.LIBRARY_ROW_STALE in warning_codes(resumed), resumed
    told = next(
        warning
        for warning in resumed["warnings"]
        if warning["code"] == retag_cli.LIBRARY_ROW_STALE
    )
    assert str(folder) in told["message"], told
    assert "reload" in told["message"], (
        f"the run named a disagreement and no act to settle it: {told['message']!r}"
    )


def test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox(
    repair_on, folder, silence, monkeypatch
):
    """The zero half, and it is what keeps the warning worth reading.

    A sweep whose every file went to the review queue unanswered wrote no genre,
    so no library row went stale, so there is nothing in rekordbox to reload. A
    verb that said so anyway would be sending a person to do real work over a run
    that changed nothing, and an instruction that appears whether or not it
    applies is one people stop reading, which costs the case above its whole
    value.

    DRIVEN THROUGH THE DECLINE rather than over an empty folder, deliberately: an
    empty selection never queues at all, so it could not tell a correct condition
    from a warning the resume path simply never reaches.
    """
    for name in ("a", "b"):
        coarse(folder, silence, name)
    bound(monkeypatch, answering({}))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["progress"]["retag"]["corrected"] == 0, resumed
    assert resumed["data"]["progress"]["retag"]["asked"] == 2, resumed
    assert retag_cli.LIBRARY_ROW_STALE not in warning_codes(resumed), resumed


def test_a_half_corrected_retag_carries_the_reload_on_its_refusal(
    repair_on, folder, silence, monkeypatch
):
    """The run R-185 is actually about, and the one the warning first missed.

    R-225 makes a job that closed carrying a cause leave through that cause
    rather than through a normal envelope, which is right and is not in question
    here: a person whose folder was half corrected must not be told the sweep
    succeeded. The consequence was that a warning riding the successful envelope
    reached every run EXCEPT the interrupted one, while the files corrected
    before the failure have stale rows exactly as a finished sweep's do.

    THE STEP RIDES THE REMEDIATION rather than a warning, because a refusal has
    no warnings to carry: the envelope's non-success shape is a structured cause,
    and what a person does next is what ``steps`` is for. The retry remedy is
    untouched, since retrying is still the first thing to do and the reload is
    owed either way.
    """
    for name in ("a", "b", "c"):
        coarse(folder, silence, name)
    table = {name: hit("deep house", SPECIFIC) for name in "abc"}
    bound(monkeypatch, raising_on(answering(table), "b"))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    code, refused = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), refused
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    assert tags.read_genre_from_file(folder / "c.flac") == SPECIFIC
    steps = refused["cause"]["remediation"]["steps"]
    assert any(str(folder) in step and "reload" in step for step in steps), (
        f"two files were corrected and their rows are stale, and the refusal "
        f"named nothing about it: {steps}"
    )
    assert refused["cause"]["origin"][0] != refused["cause"]["origin"][-1], (
        "the trail was shortened, so some hop re-created the cause rather than "
        "extending what it was already carrying"
    )


def test_a_retag_that_failed_before_correcting_anything_names_no_reload(
    repair_on, folder, silence, monkeypatch
):
    """The zero half of the refusal, and it is the half that keeps it honest.

    A sweep whose first and only item could not be answered wrote no genre, so
    no row went stale, so the refusal has nothing to add. A verb that appended
    the reload to every failure would be telling a person to go and reconcile a
    library against a run that changed nothing in it, which is the same wrong
    answer as the successful zero one case below, arriving on a different path.
    """
    coarse(folder, silence, "a")
    bound(monkeypatch, raising_on(answering({}), "a"))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    code, refused = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), refused
    assert tags.read_genre_from_file(folder / "a.flac") == CATCH_ALL
    steps = refused["cause"]["remediation"]["steps"]
    assert not any("reload" in step for step in steps), steps


def test_the_queueing_envelope_names_the_reload_before_the_person_walks_away(
    repair_on, folder, silence, monkeypatch
):
    """The other reader, and the reason this one is unconditional.

    The envelope above is written by a detached child into a log. THIS one is what
    comes back in the terminal from the command the person typed, and it is the
    last thing they read before leaving the sweep to run. It cannot know yet how
    many files will be corrected, and every file in the plan was selected for
    carrying a genre the taxonomy calls too coarse, so a sweep that corrects none
    of them is the unusual case and saying nothing is the worse answer.

    THE THREE DRIVES ARE SPELLED OUT HERE rather than taken from
    ``tests.cli_drive.approve_and_queue``, which is the only case in this section
    that does so. The helper CONSUMES the queueing envelope and returns the job
    identifier out of it, and the queueing envelope is precisely what is under
    test. R34's contract is unweakened: the refusal is met with nothing recorded,
    the decision is a separate act by a named actor, and only the third
    invocation, naming that run, queues.
    """
    coarse(folder, silence, "a")
    bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))

    verb = ["tag", "retag", str(folder)]
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, decision = drive(
        ["run", "decide", run_id, RETAG_GATE, "apply", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), decision

    code, queued = drive(["--run", run_id, *verb])

    assert code == int(ExitCode.OK), queued
    assert retag_cli.LIBRARY_ROW_STALE in warning_codes(queued), queued
    told = next(
        warning
        for warning in queued["warnings"]
        if warning["code"] == retag_cli.LIBRARY_ROW_STALE
    )
    assert str(folder) in told["message"], told


def test_the_retag_entry_declares_the_file_surface_alone_and_no_database_decision():
    """R-246 CLOSED, and it is asserted against the absence that caused it.

    The entry declared ``db_metadata`` after the row relink
    ``write.metadata.plan_genre_retag`` performs, and nothing in ``src`` calls the
    functions that would reach it, which the case at the head of this section
    pins by walking the tree. A declaration is a promise to whoever reads the
    registry, so a surface named by a verb that cannot touch it is the product
    saying something false about itself.

    THE CLOUD SYNC DECISION GOES WITH IT, and that is a consequence rather than a
    second opinion. The gate binds to write intent on the guarded writer and this
    verb opens no database at all, so it could never raise it;
    ``tests/test_cli_contract.py`` holds the pairing in both directions, and this
    assertion is the per verb half that says WHICH answer this entry settled on.

    THE TWO ARE ASSERTED TOGETHER ON PURPOSE. Restoring either one alone leaves a
    registry the contract suite refuses, and reading them in one place is what
    tells the next author that they move as a pair.
    """
    entry = registry.entry("tag.retag")

    assert entry.writes == frozenset({"files"}), (
        f"{entry.name} declares {sorted(entry.writes)}; the database half has no "
        f"caller in src, so a surface beyond files is a write it never performs"
    )
    assert not entry.writes & registry.DB_WRITE_SURFACES
    assert [spec.name for spec in entry.gates] == ["tag.retag.confirm"], (
        "this verb asks one question, over its plan. A cloud sync decision here "
        "would be a question its work can never raise"
    )
    assert entry.destructive, (
        "narrowing the write surface must not have taken the destructive flag "
        "with it: this verb still rewrites the genre on files a person owns"
    )


# ---------------------------------------------------------------------------
# The resume argv
# ---------------------------------------------------------------------------


def test_the_retag_resume_argv_carries_the_gate_run_before_the_verb_path(
    repair_on, folder, silence, monkeypatch
):
    """The flag belongs to the ROOT parser, so its position is the contract.

    A decision belongs to the invocation rather than to the subcommand, and
    ``--run`` after the verb path is not a flag this parser accepts. Asserted
    through the real ``argv_for`` rather than by hand, so what is checked is the
    command line the job driver would actually spawn.
    """
    coarse(folder, silence, "a")
    bound(monkeypatch, answering({}))
    gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    argv = resume_argv(job_id)

    assert argv == ["--run", gate_run, "tag", "retag", str(folder), "--job", job_id]
