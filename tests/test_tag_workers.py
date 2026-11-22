"""U3 and U4: the shell and artifact helper the tagging verbs stand on, and tag folder end to end.

Each property the adoption original states is asserted against the copy, and
three that no behaviour shows (a name, a call shape, a sort key) by parsing
the source. The second half drives ``crate tag folder`` through the real
dispatcher. Nothing here names a real volume, person or track (D1).
"""

from __future__ import annotations

import ast
import json
import os
import shlex
from pathlib import Path

import pytest

from cratekit.acquire import cli as acquire_cli
from cratekit.cli import handlers, output, registry
from cratekit.core import art, config, jobs, review, routing, tags
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.tagging import artifacts, published, retag, retag_cli, searchers, shell, tag
from cratekit.tagging import cli as tag_cli
from cratekit.tagging.tag import SearchHit
from tests._containers import synth_container
from tests._taxonomy_parses import counted, unique
from tests.cli_drive import approve_and_queue, drive, drive_human
from tests.test_catalogue_searcher import _beatport_page as beatport_page
from tests.test_catalogue_searcher import _beatport_track as beatport_track
from tests.test_config import valid_data
from tests.test_handlers import _drive_calls
from tests.test_published_genre import (
    ISRC,
    RATE_LIMITED,
    deezer_album,
    deezer_fetch,
    deezer_track,
)
from tests.test_published_genre import UNKNOWN as DEEZER_UNKNOWN

# Imported, never copied, so the builders and the genres cannot drift apart.
from tests.test_tagging_engine import CATCH_ALL, SPECIFIC, TAXONOMY, answering, place

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"
SHELL_SOURCE = SRC_ROOT / "cratekit" / "tagging" / "shell.py"
ARTIFACTS_SOURCE = SRC_ROOT / "cratekit" / "tagging" / "artifacts.py"


# Fixtures


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
    modules rank (KTD23), so a test can hand it the one method it needs.
    ``settle`` moves the rows as a real driver does, so ``advance`` re-reads a
    job that genuinely moved.
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
    return jobs.enqueue(store, handler_key="tag.folder", payload={}, cfg=cfg, item_ids=item_ids)


# The reported payload


def test_an_extra_mapping_rides_under_progress_and_never_beside_it(store, cfg):
    """The closed surface, asserted on the payload rather than on the intent.

    ``job_state/1`` declares ``additionalProperties: false``, so a per verb
    detail at the top level is an undeclared field every generated consumer
    rejects. The four top level keys are asserted by equality, not membership,
    since a green suite once missed that defect (U51).
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


# The honest zero


def test_the_honest_zero_names_an_empty_job_id_rather_than_a_null():
    """R-234, which shipped once and must not be ported back in.

    ``cli.output`` types ``job_id`` as a required string, so a null fails the
    verb's own schema. Asserted on the value rather than truthiness, because
    ``None`` and ``""`` are both falsey and only one is the bug.
    """
    payload = shell.no_op("no-op")

    assert payload["job_id"] == ""
    assert payload["job_id"] is not None


def test_the_honest_zero_validates_against_the_job_state_surface():
    """Validated against the DECLARED schema, not against a hand written literal.

    ``output.payload_problems`` is the check ``tests/cli_drive.py`` runs over a
    driven verb's envelope. Field types typed by hand would be a second opinion
    that would not notice a field added to the surface.
    """
    for state in ("no-op", "declined"):
        assert output.payload_problems("job_state", shell.no_op(state)) == [], state


# The resume


def test_a_job_with_no_items_is_refused_rather_than_driven(store, cfg):
    """The false success this refusal exists to stop.

    ``core.jobs`` reports a job with no items as SUCCEEDED, so driving one would
    tell a person a folder was tagged over a job with no file in it. It is
    ``internal-error`` because no person can fix it: a build that did not
    record its items queued it.
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


def test_a_cancelled_job_raises_rather_than_reporting_through_a_normal_envelope(store, cfg):
    """R-225, and the reason the predicate is not ``FAILED``.

    Built through ``jobs.cancel``, so the predicate meets a state the engine
    produces. A run stopped by a signal lands CANCELLED with a cause, and the
    narrower predicate would hand it back as a payload the dispatcher exits 0 on.
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


# The name that is load bearing outside this module


def test_the_counter_this_guard_borrows_sees_a_call_it_is_meant_to_see():
    """P7's other half: a guard nobody has watched fire proves nothing.

    ``_drive_calls`` is imported from ``tests/test_handlers.py``, not copied, so
    the two guards agree on what a driver call looks like. This case stops the
    assertion below from passing because the counter is broken.
    """
    assert _drive_calls(ast.parse("jobs.drive(store, job)\ndrive(store, job)\n")) == 2


def test_nothing_in_the_tagging_shell_is_named_drive():
    """Why the function is called ``advance``, asserted where it can be checked.

    ``tests/test_handlers.py`` asserts one place calls the job driver, counting
    every ``ast.Call`` whose callee is NAMED ``drive``. A function of that name
    here would read as a second caller, so a DEFINITION is covered as well.
    """
    tree = ast.parse(SHELL_SOURCE.read_text(encoding="utf-8"))

    assert _drive_calls(tree) == 0
    defined = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    assert "drive" not in defined, defined


# Where one item's report is staged, and where it lands


def test_an_item_identifier_holding_a_separator_cannot_escape_the_directory(store, cfg):
    """The reason the filename is the ordinal, driven with an identifier that tries.

    A tagging item identifier is a path relative to the swept folder, so it
    holds separators as a matter of course, and a filename built from one is a
    path traversal wearing a report.
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

    Left in place, the next attempt would commit it as its own: wrong, not missing.
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

    ``jobs.commit_artifact`` is an ``os.replace``, atomic only within one
    filesystem, and a temp directory on another fails at commit after the work
    is done. Asserted as a shared device, because the device is the property.
    """
    final = artifacts.final_path(cfg, "job-one", 0)
    staged = artifacts.staged_path(cfg, "job-one", 0)
    root = jobs.store_dir(cfg)

    assert final.parents[2] == root
    assert staged.parents[3] == root
    assert os.stat(final.parent).st_dev == os.stat(staged.parent).st_dev


def test_reports_past_the_four_digit_name_come_back_in_item_order(cfg):
    """The sort key is the ordinal as a NUMBER, and a folder can reach that far.

    The name is ``{ordinal:04d}.json``, so as text ``"10000"`` sorts before
    ``"9999"``. Two reports at that boundary tell the two sorts apart.
    """
    for ordinal in (10000, 9999):
        artifacts.write(artifacts.final_path(cfg, "job-one", ordinal), {"ordinal": ordinal})

    assert [report["ordinal"] for report in artifacts.committed(cfg, "job-one")] == [9999, 10000]


def test_a_report_that_cannot_be_parsed_is_skipped_rather_than_raised_on(cfg):
    """A summary is a display over work that already happened.

    Refusing would let one unreadable file hide every other item, all of whose
    work is done and committed.
    """
    artifacts.write(artifacts.final_path(cfg, "job-one", 0), {"outcome": "tagged"})
    artifacts.final_path(cfg, "job-one", 1).write_text("{ not json", encoding="utf-8")
    artifacts.final_path(cfg, "job-one", 2).write_text('"a string"', encoding="utf-8")
    artifacts.write(artifacts.final_path(cfg, "job-one", 3), {"outcome": "skipped"})

    assert artifacts.committed(cfg, "job-one") == ({"outcome": "tagged"}, {"outcome": "skipped"})


def test_a_job_that_committed_nothing_reads_back_as_nothing(cfg):
    """No directory is not an error. It is a job whose first item has not landed."""
    assert artifacts.committed(cfg, "never-ran") == ()


def test_a_written_report_is_sorted_json_so_two_runs_produce_one_file(cfg):
    path = artifacts.write(artifacts.final_path(cfg, "job-one", 0), {"b": 2, "a": 1})

    text = path.read_text(encoding="utf-8")
    assert text.index('"a"') < text.index('"b"')
    assert json.loads(text) == {"a": 1, "b": 2}


def test_the_two_directory_names_are_the_tagging_ones(cfg):
    """The only thing this copy changes from the adoption one, so it is asserted.

    Keeping ``adopt-artifacts`` would file tagging reports where the adoption
    summary reads them back as its own.
    """
    assert artifacts.ARTIFACTS_DIRNAME == "tag-artifacts"
    assert artifacts.STAGING_DIRNAME == "tag-staging"
    assert artifacts.final_path(cfg, "job-one", 0).parents[1].name == "tag-artifacts"
    assert artifacts.staged_path(cfg, "job-one", 0).parents[2].name == "tag-staging"


def test_the_artifact_helper_never_resolves_the_queue_root_for_itself():
    """KTD9's defect wearing an indirection, asserted where it is visible.

    ``jobs.store_dir()`` with no argument loads the CURRENT configuration, which
    a resume must not do. The handler guard cannot follow a reload through a
    helper, and the installation scoped queue makes both calls look alike, so
    the property survives only as a guard over the source.
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


# U4: ``crate tag folder`` walking a real folder, end to end, always through the
# verb, so an unbound handler key would fail.


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One real FLAC container, synthesized once and copied per file.

    Real because the write under test goes all the way through
    ``core.tags.write_genre`` and is read back off the file.
    """
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def folder(tmp_path) -> Path:
    """A download folder OUTSIDE the library, which is where tagging happens.

    ``crate tag folder`` is pointed at a fresh download before any of it is in
    the library, so files under the library root would be a case it lacks.
    """
    out = tmp_path / "downloads"
    out.mkdir()
    return out


def bound(monkeypatch, searcher):
    """Bind ``searcher`` where the worker looks one up (KTD11, R23).

    The worker calls ``searchers.for_taxonomy`` at CALL TIME because a fixed
    three argument ``ItemHandler`` leaves nowhere else to hand a fake in, and
    without one every case below would touch the network.
    """
    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared=None, refusals=None: searcher)
    # The general catalogue too, to a lookup failing on any request (R-796);
    # a test wanting an answer calls :func:`general` after this.
    general(monkeypatch, None)
    return searcher


def general(monkeypatch, track, album=None, seen: list[str] | None = None):
    """Bind the general catalogue's lookup where the worker's seam reads it.

    ``published.for_taxonomy`` is built over ``published.for_lookup`` at call
    time, so replacing the lookup is the whole substitution and the rules of
    when the catalogue is asked stay the shipped ones.
    """
    lookup = published.genre_lookup(
        fetch=deezer_fetch(track, album, seen), sleep=lambda _seconds: None
    )
    monkeypatch.setattr(published, "for_lookup", lambda: lookup)
    return lookup


def raising_on(searcher, title: str):
    """``searcher``, except that one title raises the way the shipped one does.

    ``catalogue-unreachable`` is what the shipped searcher raises when a network
    drops mid folder. RETRYABLE as the shipped raise is, since ``jobs.retry``
    reads the flag before it re-arms the item (R-390).
    """

    def wrapped(artist: str, name: str):
        if name == title:
            searcher.asked.append((artist, name))
            raise refuse(
                searchers.UNREACHABLE_REASON,
                f"no catalogue could be read, so nothing is known about {name!r}",
                remedy=Remedy.RETRY_LATER,
                retryable=True,
                origin=("tagging", "searchers"),
            )
        return searcher(artist, name)

    wrapped.asked = searcher.asked  # type: ignore[attr-defined]
    return wrapped


def hit(source_genre: str, genre: str | None = None, *, off_taxonomy: bool = False) -> SearchHit:
    """One catalogue answer, carrying what it answered even when it declines.

    A decline that cannot say what it declined is one nobody can act on (R24).
    ``off_taxonomy`` goes with a GENRE and never a decline, as the shipped
    searcher builds one: it qualifies a word about to be written.
    """
    return SearchHit(
        genre=genre,
        source=searchers.BEATPORT,
        source_genre=source_genre,
        off_taxonomy=off_taxonomy,
    )


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

    Through the real ``argv_for``, because the property is that the frozen
    folder survives the round trip, and a hand written resume would assert
    about a string this test typed.
    """
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def swept(folder: Path):
    """Queue a sweep over ``folder``, then drive it as the job driver would."""
    drive(["tag", "folder", "--queue-only", str(folder)])
    job = tag_job()
    code, resumed = drive(resume_argv(job.job_id))
    return job, code, resumed


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


# The binding


def test_the_tag_folder_key_resolves_to_a_worker():
    """The R-203 half this unit closes, asserted against the table itself.

    ``tests/test_handlers.py`` checks each queued verb is in exactly ONE of the
    two mappings, which ``HANDLERS_NOT_YET_BOUND`` satisfies. Only an assertion
    naming this key tells "declared as unbound" from "bound".
    """
    key = registry.entry("tag.folder").handler_key

    assert handlers.is_known(key), f"{key} still has no worker"
    assert handlers.unbound_reason(key) is None
    assert callable(handlers.resolve(key))


# The happy path


def test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third(
    cfg, folder, silence, monkeypatch
):
    """The whole seam in one case: queue, drive, write, and read back.

    The files are read back off disk: a worker reporting a genre it never wrote
    would still drive every item to done with the counts adding up. The third
    file holds the policy, fill if empty: its curation comes back a skip with a
    reason. It carries a picture too, since a tagged file with none is asked
    for art (U85).
    """
    from tests.test_tagging_engine import _jpeg, plant

    place(folder, silence, "a")
    place(folder, silence, "b")
    plant(place(folder, silence, "c", genre=SPECIFIC), _jpeg(320, 200), dims=(320, 200, 24))
    searcher = bound(
        monkeypatch,
        answering({"a": hit("deep house", SPECIFIC), "b": hit("deep house", SPECIFIC)}),
    )

    code, queued = drive(["tag", "folder", "--queue-only", str(folder)])
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

    A download folder is usually release directories, so ``sub/deep.flac`` is
    the common case: the worker joins it back onto the payload's folder and the
    report is named after the ORDINAL, not this string.
    """
    place(folder / "sub", silence, "deep")
    bound(monkeypatch, answering({"deep": hit("deep house", SPECIFIC)}))

    drive(["tag", "folder", "--queue-only", str(folder)])
    job = tag_job()
    assert list(item_states(job.job_id)) == [str(Path("sub") / "deep.flac")]

    code, resumed = drive(resume_argv(job.job_id))

    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(folder / "sub" / "deep.flac") == SPECIFIC


def test_the_skip_reason_reaches_the_report_and_not_only_the_artifact(
    cfg, folder, silence, monkeypatch
):
    """R16 at the surface a person reads.

    A reason that stops at the committed artifact has to be found on disk. The
    counts ride under ``progress``, the one place ``job_state/1`` leaves open
    for a per verb detail.
    """
    place(folder, silence, "a")
    place(folder, silence, "b", genre=SPECIFIC)
    bound(monkeypatch, answering({}))

    job, _code, resumed = swept(folder)

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["skipped"][tag.HAS_GENRE] == 1
    assert tagging["skipped"][tag.NO_HIT] == 1
    assert tagging["tagged"] == 0
    assert set(tagging["skipped"]) == {
        tag.HAS_GENRE,
        tag.NO_HIT,
        tag.UNMAPPED_GENRE,
        tag.SOURCES_UNREAD,
        tag.NO_ISRC,
    }, (
        "a summary listing only the reasons it saw cannot tell 'none of those "
        "here' from 'this build does not count them'"
    )


def test_the_report_names_each_unresolved_source_genre_with_its_count(
    cfg, folder, silence, monkeypatch
):
    """R24, and the reason a bare ``unmapped-genre`` total is not enough.

    A count says a gap exists; the STRING names the alias their taxonomy lacks,
    the only half a person can act on. The strings are ones the shipped resolver
    really declines, since a fake hit can carry any pair, and a fixture that
    cannot occur is METHOD's fourth defect pattern.
    """
    for name in ("a", "b", "c"):
        place(folder, silence, name)
    declines = [
        value for value in ("Techno", "Electronic") if routing.suggest_tag(TAXONOMY, value).declined
    ]
    assert declines == ["Techno", "Electronic"], "these no longer decline"
    bound(monkeypatch, answering({"a": hit("Techno"), "b": hit("Techno"), "c": hit("Electronic")}))

    job, _code, resumed = swept(folder)

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["unresolved"] == {"Techno": 2, "Electronic": 1}
    assert tagging["skipped"][tag.UNMAPPED_GENRE] == 3
    assert [report["source_genre"] for report in artifacts.committed(cfg, job.job_id)] == [
        "Techno",
        "Techno",
        "Electronic",
    ]


def test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns(
    cfg, folder, silence, monkeypatch
):
    """R-650. The written word a person was never told about.

    Three files are tagged, two with a word the declared taxonomy has never
    heard of, and the report must say so. The two maps are not one: a decline
    left its file askable and an off taxonomy write is on disk, so merging them
    would send somebody looking for files that are not there.
    """
    for name in ("a", "b", "c", "d", "e"):
        place(folder, silence, name)
    bound(
        monkeypatch,
        answering(
            {
                "a": hit("gqom", "gqom", off_taxonomy=True),
                "b": hit("gqom", "gqom", off_taxonomy=True),
                "c": hit("Deep House", "Deep House"),
                "d": hit("Techno"),
                "e": hit("bubblegum bass", "bubblegum bass", off_taxonomy=True),
            }
        ),
    )

    job, _code, resumed = swept(folder)

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["off_taxonomy"] == {"gqom": 2, "bubblegum bass": 1}
    assert tagging["unresolved"] == {"Techno": 1}
    assert tagging["tagged"] == 4, "they were written, so they are tagged"
    assert [report["off_taxonomy"] for report in artifacts.committed(cfg, job.job_id)] == [
        True,
        True,
        False,
        False,
        True,
    ]

    warnings = {warning["code"]: warning["message"] for warning in resumed["warnings"]}
    assert tag_cli.OFF_TAXONOMY == "tag-folder-off-taxonomy", (
        "the code is the surface a log filter matches on, so it is pinned here "
        "rather than only referred to by name"
    )
    assert tag_cli.OFF_TAXONOMY in warnings
    message = warnings[tag_cli.OFF_TAXONOMY]
    assert "3 of the 4 files" in message
    # Sorted, not in walk order (gqom was committed first).
    assert "bubblegum bass, gqom" in message
    assert "Deep House" not in message
    assert "Techno" not in message, "a decline is the other map's, and nothing was written"


def _catalogues(per_title: dict[str, dict[str, searchers.Fetched]]):
    """The SHIPPED searcher, over a fetch that answers per title and per source.

    R-791 is about what the searcher reports for each catalogue, and a fake
    would only report what this test told it. ``Fetched`` is the seam's own
    contract, so a 403 here is the shape ``default_fetch`` hands a fallback.
    """
    bases = {
        searchers.BEATPORT: searchers.BEATPORT_SEARCH,
        searchers.TRAXSOURCE: searchers.TRAXSOURCE_SEARCH,
        searchers.BANDCAMP: searchers.BANDCAMP_SEARCH,
    }

    def fetch(url: str) -> searchers.Fetched:
        for title, sources in per_title.items():
            if f"+{title}" not in url and f"={title}" not in url:
                continue
            for source, page in sources.items():
                if url.startswith(bases[source]):
                    return page
        return searchers.Fetched(note=f"no route for {url}")

    # THE WALK BEFORE U244, which R-791's sweeps were measured on and these
    # tests describe; the default walk's sweep is test_discogs_searcher's.
    return searchers.catalogue_searcher(
        TAXONOMY, fetch=fetch, sleep=lambda _s: None, walk=searchers.SCRAPED_WALK
    )


EMPTY_BEATPORT = searchers.Fetched(text=beatport_page([]), status=200)
EMPTY_TRAXSOURCE = searchers.Fetched(text="<html></html>", status=200)
EMPTY_BANDCAMP = searchers.Fetched(text="<html><ul></ul></html>", status=200)
TRAXSOURCE_403 = searchers.Fetched(note="HTTP 403", status=403)
BANDCAMP_CHALLENGE = searchers.Fetched(
    text="<html><head><title>Client Challenge</title></head></html>", status=200
)

#: The two states of the three record shops the general catalogue's cases are
#: driven in: every one answering MISS, and the state measured on the author's
#: machine, Beatport answering MISS and both fallbacks refusing.
ALL_MISSED = {
    searchers.BEATPORT: EMPTY_BEATPORT,
    searchers.TRAXSOURCE: EMPTY_TRAXSOURCE,
    searchers.BANDCAMP: EMPTY_BANDCAMP,
}
REFUSED_FALLBACKS = {
    searchers.BEATPORT: EMPTY_BEATPORT,
    searchers.TRAXSOURCE: TRAXSOURCE_403,
    searchers.BANDCAMP: BANDCAMP_CHALLENGE,
}


def _fetched(answer) -> searchers.Fetched:
    return answer if isinstance(answer, searchers.Fetched) else searchers.Fetched(
        text=answer, status=200
    )


def test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit(
    cfg, folder, silence, monkeypatch
):
    """R-791 end to end, through the verb.

    Beatport misses and both fallbacks refuse this machine, and every surface
    must say two catalogues were never read rather than ``no-hit``.
    """
    for name in ("a", "b"):
        place(folder, silence, name)
    refused = {
        searchers.BEATPORT: EMPTY_BEATPORT,
        searchers.TRAXSOURCE: TRAXSOURCE_403,
        searchers.BANDCAMP: BANDCAMP_CHALLENGE,
    }
    bound(monkeypatch, _catalogues({"a": refused, "b": refused}))

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    for report in artifacts.committed(cfg, job.job_id):
        assert report["skipped"] == tag.SOURCES_UNREAD
        assert [(said["source"], said["answer"]) for said in report["answers"]] == [
            (searchers.BEATPORT, "miss"),
            (searchers.TRAXSOURCE, "blocked"),
            (searchers.BANDCAMP, "blocked"),
            # The fixture files carry no ISRC, so the general catalogue was
            # never asked about them and the record says why (R-796).
            (published.SOURCE, tag.NO_ISRC),
        ]
        assert report["unread"] == {searchers.TRAXSOURCE: "blocked", searchers.BANDCAMP: "blocked"}
    assert tags.read_genre_from_file(folder / "a.flac") is None

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["skipped"][tag.SOURCES_UNREAD] == 2
    assert tagging["skipped"][tag.NO_HIT] == 0
    assert tagging["answers"][searchers.BANDCAMP]["blocked"] == 2
    assert tagging["answers"][searchers.TRAXSOURCE]["blocked"] == 2
    assert tagging["answers"][searchers.BEATPORT]["miss"] == 2
    assert tagging["answers"][searchers.BEATPORT]["blocked"] == 0, "zero filled"

    warnings = {warning["code"]: warning["message"] for warning in resumed["warnings"]}
    assert tag_cli.SOURCES_UNREAD == "tag-folder-sources-unread"
    assert tag_cli.SOURCE_BLOCKED == "tag-folder-source-blocked"
    unread = warnings[tag_cli.SOURCES_UNREAD]
    assert "2 files were left untagged" in unread
    assert "Across the sweep: traxsource refused this client on 2; bandcamp refused this client on 2" in unread
    assert "parse break" not in unread
    blocked = [w["message"] for w in resumed["warnings"] if w["code"] == tag_cli.SOURCE_BLOCKED]
    assert len(blocked) == 2
    assert blocked[0].startswith("traxsource refused every one of the 2 searches")
    assert blocked[1].startswith("bandcamp refused every one of the 2 searches")


#: Beatport's answer at sitting 97, as the shipped fetch hands it on (U281).
BEATPORT_CHALLENGE = searchers.Fetched(note="Cloudflare challenge, HTTP 403", status=403)


def _refusing_sweep(monkeypatch, seen: list[str]):
    """Bind the worker's searcher to the shipped one over a Beatport refusing every lookup.

    A searcher per call carrying the run count the worker hands in, as the
    shipped binder builds one, so what is tested is the worker's run scope.
    Discogs answers an empty result set, so every file settles
    ``sources-unread`` rather than failing.
    """
    from tests.test_discogs_searcher import SENT, results

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            return BEATPORT_CHALLENGE
        if url.startswith(searchers.DISCOGS_SEARCH):
            return searchers.Fetched(text=results(), status=200)
        return searchers.Fetched(note=f"no route for {url}")

    asker = searchers.discogs_asker(token=SENT, fetch=fetch, sleep=lambda _s: None)

    def for_taxonomy(declared=None, refusals=None):
        return searchers.catalogue_searcher(
            TAXONOMY,
            fetch=fetch,
            sleep=lambda _s: None,
            discogs=asker,
            refusals=refusals,
        )

    monkeypatch.setattr(searchers, "for_taxonomy", for_taxonomy)
    general(monkeypatch, None)


def _beatport_asked(seen: list[str]) -> int:
    return sum(url.startswith(searchers.BEATPORT_SEARCH) for url in seen)


def test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused(
    cfg, folder, silence, monkeypatch
):
    """U281 through the verb: five files, Beatport refusing every lookup with
    Cloudflare's challenge. Three requests reach Beatport, not five; the two
    files after them record it blocked and unsent, every file stays askable,
    Discogs is asked on all five, and the warning names a refusal rather than
    an outage."""
    for name in ("a", "b", "c", "d", "e"):
        place(folder, silence, name)
    seen: list[str] = []
    _refusing_sweep(monkeypatch, seen)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    assert _beatport_asked(seen) == 3
    assert sum(url.startswith(searchers.DISCOGS_SEARCH) for url in seen) == 5
    reports = sorted(artifacts.committed(cfg, job.job_id), key=lambda r: r["item"])
    assert len(reports) == 5
    notes = []
    for report in reports:
        assert report["skipped"] == tag.SOURCES_UNREAD
        assert report["unread"] == {searchers.BEATPORT: "blocked"}
        (beatport,) = [s for s in report["answers"] if s["source"] == searchers.BEATPORT]
        assert beatport["answer"] == "blocked"
        notes.append(beatport["note"])
    assert [note.startswith(searchers.NOT_SENT) for note in notes] == [
        False, False, False, True, True,
    ]
    assert tags.read_genre_from_file(folder / "e.flac") is None

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["skipped"][tag.NO_HIT] == 0
    assert tagging["answers"][searchers.BEATPORT]["blocked"] == 5
    assert tagging["answers"][searchers.BEATPORT]["unreachable"] == 0
    assert tagging["challenged"][searchers.BEATPORT] == 5
    assert tagging["not_sent"][searchers.BEATPORT] == 2
    assert tagging["not_sent"][searchers.DISCOGS] == 0, "zero filled"

    warnings = {w["code"]: w["message"] for w in resumed["warnings"]}
    unread = warnings[tag_cli.SOURCES_UNREAD]
    assert (
        "Across the sweep: beatport refused this client (Cloudflare challenge) on 5, "
        "2 of them not asked once it had refused this client"
    ) in unread
    assert "unreachable" not in unread
    blocked = warnings[tag_cli.SOURCE_BLOCKED]
    assert blocked.startswith("beatport refused every one of the 3 searches it was sent")
    assert "and was not asked about 2 more file(s) once it had refused this client" in blocked


def test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file(
    cfg, folder, silence, monkeypatch
):
    """The count is the run's: a second sweep in the same process, a new job,
    sends Beatport its first three lookups again rather than inheriting the
    first sweep's stop."""
    for name in ("a", "b", "c", "d"):
        place(folder, silence, name)
    seen: list[str] = []
    _refusing_sweep(monkeypatch, seen)

    drive(["tag", "folder", "--queue-only", str(folder)])
    first = tag_job()
    code, _ = drive(resume_argv(first.job_id))
    assert code == int(ExitCode.OK)
    assert _beatport_asked(seen) == 3

    again = folder.parent / "again"
    for name in ("f", "g", "h", "i"):
        place(again, silence, name)
    drive(["tag", "folder", "--queue-only", str(again)])
    with jobs.open_store() as store:
        (second,) = [
            job
            for job in jobs.list_jobs(store)
            if job.handler_key == registry.entry("tag.folder").handler_key
            and job.job_id != first.job_id
        ]
    code, _ = drive(resume_argv(second.job_id))
    assert code == int(ExitCode.OK)
    assert _beatport_asked(seen) == 6


def test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file(
    cfg, folder, silence, monkeypatch
):
    """The count is the RUN's, not the job's: a retried job driven again in
    the same process is a new drive, and asks Beatport its first three lookups
    again. With no Discogs token every file fails ``catalogue-unreachable``,
    retryable, which is the shape a retry re-arms."""
    from tests.test_discogs_searcher import results

    for name in ("a", "b", "c", "d", "e"):
        place(folder, silence, name)
    seen: list[str] = []

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            return BEATPORT_CHALLENGE
        return searchers.Fetched(text=results(), status=200)

    asker = searchers.discogs_asker(token=None, fetch=fetch, sleep=lambda _s: None)
    monkeypatch.setattr(
        searchers,
        "for_taxonomy",
        lambda declared=None, refusals=None: searchers.catalogue_searcher(
            TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, refusals=refusals
        ),
    )
    general(monkeypatch, None)

    drive(["tag", "folder", "--queue-only", str(folder)])
    job = tag_job()
    drive(resume_argv(job.job_id))
    assert _beatport_asked(seen) == 3
    assert set(item_causes(job.job_id).values()) == {searchers.UNREACHABLE_REASON}

    with jobs.open_store() as store:
        jobs.retry(store, job.job_id)
    drive(resume_argv(job.job_id))

    assert _beatport_asked(seen) == 6


def test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent(
    cfg, folder, silence, monkeypatch
):
    """Discogs remembers its first refusal and sends nothing more in the run,
    recording each later file blocked and unsent, so the source blocked
    warning counts the one search it was sent and names the files it was not
    (U281's review)."""
    for name in ("a", "b", "c", "d"):
        place(folder, silence, name)
    seen: list[str] = []

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            return searchers.Fetched(text=beatport_page([]), status=200)
        return searchers.Fetched(note="HTTP 403", status=403)

    from tests.test_discogs_searcher import SENT

    asker = searchers.discogs_asker(token=SENT, fetch=fetch, sleep=lambda _s: None)
    monkeypatch.setattr(
        searchers,
        "for_taxonomy",
        lambda declared=None, refusals=None: searchers.catalogue_searcher(
            TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, refusals=refusals
        ),
    )
    general(monkeypatch, None)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    assert sum(url.startswith(searchers.DISCOGS_SEARCH) for url in seen) == 1
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["answers"][searchers.DISCOGS]["blocked"] == 4
    assert tagging["not_sent"][searchers.DISCOGS] == 3
    warnings = {w["code"]: w["message"] for w in resumed["warnings"]}
    assert (
        "discogs refused this client on 4, 3 of them not asked once it had "
        "refused this client"
    ) in warnings[tag_cli.SOURCES_UNREAD]
    blocked = warnings[tag_cli.SOURCE_BLOCKED]
    assert blocked.startswith("discogs refused every one of the 1 searches it was sent")
    assert "and was not asked about 3 more file(s) once it had refused this client" in blocked


def test_a_sweep_some_of_whose_refusals_were_a_challenge_says_how_many():
    """Named whole only when every refusal counted was a challenge."""
    summary = {"challenged": {searchers.BEATPORT: 2}, "not_sent": {searchers.BEATPORT: 1}}

    said = tag_cli._unread_phrase(summary, searchers.BEATPORT, "blocked", 4)
    whole = tag_cli._unread_phrase(
        {"challenged": {searchers.BEATPORT: 4}}, searchers.BEATPORT, "blocked", 4
    )
    plain = tag_cli._unread_phrase({}, searchers.BEATPORT, "blocked", 4)

    assert said == (
        "beatport refused this client on 4 (Cloudflare challenge on 2), "
        "1 of them not asked once it had refused this client"
    )
    assert whole == "beatport refused this client (Cloudflare challenge) on 4"
    assert plain == "beatport refused this client on 4"
    assert tag_cli._unread_phrase({}, searchers.BEATPORT, "unreachable", 4) == (
        "beatport unreachable on 4"
    )


def test_an_outage_keeps_its_own_word_in_the_sweeps_warning(cfg, folder, silence, monkeypatch):
    """A Beatport that is down is unreachable, said so, and asked on every file."""
    from tests.test_discogs_searcher import SENT, results

    for name in ("a", "b", "c", "d"):
        place(folder, silence, name)
    seen: list[str] = []

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            return searchers.Fetched(note="HTTP 503", status=503)
        return searchers.Fetched(text=results(), status=200)

    asker = searchers.discogs_asker(token=SENT, fetch=fetch, sleep=lambda _s: None)
    monkeypatch.setattr(
        searchers,
        "for_taxonomy",
        lambda declared=None, refusals=None: searchers.catalogue_searcher(
            TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, refusals=refusals
        ),
    )
    general(monkeypatch, None)

    drive(["tag", "folder", "--queue-only", str(folder)])
    code, resumed = drive(resume_argv(tag_job().job_id))
    assert code == int(ExitCode.OK), resumed

    assert _beatport_asked(seen) == 4
    warnings = {w["code"]: w["message"] for w in resumed["warnings"]}
    assert "Across the sweep: beatport unreachable on 4" in warnings[tag_cli.SOURCES_UNREAD]
    assert "refused" not in warnings[tag_cli.SOURCES_UNREAD]
    assert tag_cli.SOURCE_BLOCKED not in warnings


def test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning(
    cfg, folder, silence, monkeypatch
):
    """Bandcamp blocked on every file it was SENT. One file ended at a Beatport
    match and never asked it, and that file must not hide the refusal on the
    other; Traxsource answered, so it is not named."""
    for name in ("a", "b"):
        place(folder, silence, name)
    assert tags.write_tags(folder / "a.flac", {"artist": "Somebody"})
    matched = searchers.Fetched(
        text=beatport_page([beatport_track("Somebody", "a", SPECIFIC)]), status=200
    )
    bound(
        monkeypatch,
        _catalogues(
            {
                "a": {searchers.BEATPORT: matched},
                "b": {
                    searchers.BEATPORT: EMPTY_BEATPORT,
                    searchers.TRAXSOURCE: EMPTY_TRAXSOURCE,
                    searchers.BANDCAMP: BANDCAMP_CHALLENGE,
                },
            }
        ),
    )

    job, _code, resumed = swept(folder)

    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert reports["a.flac"]["genre_written"] == SPECIFIC
    assert [said["answer"] for said in reports["a.flac"]["answers"]] == [
        "matched",
        searchers.NOT_ASKED,
        searchers.NOT_ASKED,
        searchers.NOT_ASKED,
    ]
    assert reports["b.flac"]["skipped"] == tag.SOURCES_UNREAD

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["answers"][searchers.BANDCAMP][searchers.NOT_ASKED] == 1
    blocked = [w["message"] for w in resumed["warnings"] if w["code"] == tag_cli.SOURCE_BLOCKED]
    assert len(blocked) == 1
    assert "bandcamp refused every one of the 1 searches" in blocked[0]


def test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said(
    cfg, folder, silence, monkeypatch
):
    """A parse break beside a MISS leaves the file undecided like a block does,
    and the warning must not leave it under the promise that a rerun settles
    it. One file, so the sentence reads as one."""
    place(folder, silence, "a")
    broken = searchers.Fetched(
        text='<div data-trid="1" class="trk-row"><span>moved</span></div>', status=200
    )
    bound(
        monkeypatch,
        _catalogues(
            {
                "a": {
                    searchers.BEATPORT: EMPTY_BEATPORT,
                    searchers.TRAXSOURCE: broken,
                    searchers.BANDCAMP: EMPTY_BANDCAMP,
                }
            }
        ),
    )

    job, _code, resumed = swept(folder)

    (report,) = artifacts.committed(cfg, job.job_id)
    assert report["unread"] == {searchers.TRAXSOURCE: "parse-break"}
    warnings = {warning["code"]: warning["message"] for warning in resumed["warnings"]}
    message = warnings[tag_cli.SOURCES_UNREAD]
    assert message.startswith("1 file was left untagged")
    assert "traxsource parse-break on 1" in message
    assert "defect in this software that another run will not move" in message
    assert tag_cli.SOURCE_BLOCKED not in warnings


def test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked(
    cfg, folder, silence, monkeypatch
):
    """A fallback never asked was blocked on zero of zero searches, which is not
    a refusal. Bought by row C5 of ``r791-b``, a zero: without the guard this
    sweep, the commonest clean one, warned that both fallbacks refused it."""
    place(folder, silence, "a")
    assert tags.write_tags(folder / "a.flac", {"artist": "Somebody"})
    matched = searchers.Fetched(
        text=beatport_page([beatport_track("Somebody", "a", SPECIFIC)]), status=200
    )
    bound(monkeypatch, _catalogues({"a": {searchers.BEATPORT: matched}}))

    job, _code, resumed = swept(folder)

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["tagged"] == 1
    assert tagging["answers"][searchers.BANDCAMP][searchers.NOT_ASKED] == 1
    codes = [warning["code"] for warning in resumed["warnings"]]
    assert tag_cli.SOURCE_BLOCKED not in codes
    assert tag_cli.SOURCES_UNREAD not in codes


def test_four_real_misses_are_no_hit_and_carry_no_unread_warning(cfg, folder, silence, monkeypatch):
    """Every catalogue asked, the general one included, and none knows the
    track. That is the absence ``no-hit`` means, and no warning qualifies it."""
    place(folder, silence, "a")
    assert tags.write_tags(folder / "a.flac", {"isrc": ISRC})
    bound(monkeypatch, _catalogues({"a": ALL_MISSED}))
    general(monkeypatch, DEEZER_UNKNOWN)

    job, _code, resumed = swept(folder)

    (report,) = artifacts.committed(cfg, job.job_id)
    assert report["skipped"] == tag.NO_HIT
    assert [said["answer"] for said in report["answers"]] == ["miss"] * 4
    assert report["unread"] == {}
    codes = [warning["code"] for warning in resumed["warnings"]]
    assert tag_cli.SOURCES_UNREAD not in codes
    assert tag_cli.SOURCE_BLOCKED not in codes
    assert tag_cli.PUBLISHED_UNREAD not in codes
    assert tag_cli.NO_ISRC_FILES not in codes


# R-796: the general catalogue, through the verb


def test_a_published_genre_reaches_the_file_the_artifact_and_the_summary(
    cfg, folder, silence, monkeypatch
):
    """AE1 end to end, in the state measured on the author's machine: Beatport
    misses, both fallbacks refuse, and the general catalogue knows the album."""
    place(folder, silence, "a")
    assert tags.write_tags(folder / "a.flac", {"isrc": ISRC})
    bound(monkeypatch, _catalogues({"a": REFUSED_FALLBACKS}))
    seen: list[str] = []
    general(monkeypatch, deezer_track(), deezer_album(["Rock"]), seen)
    expected = routing.suggest_tag(TAXONOMY, "Rock").tag

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    assert tags.read_genre_from_file(folder / "a.flac") == expected
    (report,) = artifacts.committed(cfg, job.job_id)
    assert report["genre_written"] == expected
    assert report["skipped"] is None
    assert (report["source"], report["source_genre"]) == (published.SOURCE, "Rock")
    assert report["off_taxonomy"] is False
    assert [(said["source"], said["answer"]) for said in report["answers"]] == [
        (searchers.BEATPORT, "miss"),
        (searchers.TRAXSOURCE, "blocked"),
        (searchers.BANDCAMP, "blocked"),
        (published.SOURCE, "matched"),
    ]
    assert report["answers"][-1]["source_genre"] == "Rock"
    assert len(seen) == 2

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["tagged"] == 1
    assert tagging["tagged_by"] == {
        searchers.BEATPORT: 0,
        searchers.DISCOGS: 0,
        searchers.TRAXSOURCE: 0,
        searchers.BANDCAMP: 0,
        published.SOURCE: 1,
        tag.LABEL_GENRE: 0,
    }
    assert tagging["answers"][published.SOURCE]["matched"] == 1
    assert set(tagging["answers"][published.SOURCE]) == set(published.ANSWERS), "zero filled"
    assert tag.NO_ISRC not in tagging["answers"][searchers.BEATPORT], (
        "a record shop is never asked by ISRC, so it carries no count for one"
    )
    codes = [warning["code"] for warning in resumed["warnings"]]
    assert tag_cli.OFF_TAXONOMY not in codes
    assert tag_cli.PUBLISHED_UNREAD not in codes
    assert tag_cli.NO_ISRC_FILES not in codes


def test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary(
    cfg, folder, silence, monkeypatch
):
    """A 429 on every file the catalogue was asked about. No file got a
    published genre, and the surface a person reads says which catalogue and
    how many, once, and does not also file it under the record shops' warning."""
    for name in ("a", "b", "c"):
        place(folder, silence, name)
    for name in ("a", "b"):
        assert tags.write_tags(folder / f"{name}.flac", {"isrc": ISRC})
    assert tags.write_tags(folder / "c.flac", {"artist": "Somebody"})
    matched = searchers.Fetched(
        text=beatport_page([beatport_track("Somebody", "c", SPECIFIC)]), status=200
    )
    bound(
        monkeypatch,
        _catalogues({"a": ALL_MISSED, "b": ALL_MISSED, "c": {searchers.BEATPORT: matched}}),
    )
    asked: list[str] = []
    general(monkeypatch, RATE_LIMITED, seen=asked)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    for name in ("a.flac", "b.flac"):
        assert reports[name]["skipped"] == tag.SOURCES_UNREAD
        assert reports[name]["unread"] == {published.SOURCE: "blocked"}
        assert tags.read_genre_from_file(folder / name) is None
    assert reports["c.flac"]["answers"][-1]["answer"] == searchers.NOT_ASKED

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["answers"][published.SOURCE]["blocked"] == 2
    assert tagging["answers"][published.SOURCE][searchers.NOT_ASKED] == 1
    assert tagging["tagged_by"][published.SOURCE] == 0
    assert len(asked) == 1, "refused on the first file, and not asked about the second"
    assert reports["b.flac"]["answers"][-1]["note"].startswith("not asked: the catalogue refused")

    assert tag_cli.PUBLISHED_UNREAD == "tag-folder-published-unread"
    named = [w["message"] for w in resumed["warnings"] if w["code"] == tag_cli.PUBLISHED_UNREAD]
    assert len(named) == 1
    assert named[0].startswith(f"{published.SOURCE}, the general catalogue asked by ISRC")
    assert "any of the 2 files it was asked about (blocked on 2)" in named[0]
    assert "no file in this run got a published genre from it" in named[0]
    assert "does not try to get past" in named[0]
    assert "parse break" not in named[0]
    blocked = [w["message"] for w in resumed["warnings"] if w["code"] == tag_cli.SOURCE_BLOCKED]
    assert blocked == [], "the general catalogue has its own warning and is named once"
    unread = [w["message"] for w in resumed["warnings"] if w["code"] == tag_cli.SOURCES_UNREAD]
    assert len(unread) == 1 and f"{published.SOURCE} refused this client on 2" in unread[0]


def test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many(
    cfg, folder, silence, monkeypatch
):
    """A miss on one file and an outage on the other. The catalogue was there
    for the run, and the file it was not there for is still said."""
    for name in ("a", "b"):
        place(folder, silence, name)
        assert tags.write_tags(folder / f"{name}.flac", {"isrc": ISRC})
    bound(monkeypatch, _catalogues({"a": ALL_MISSED, "b": ALL_MISSED}))
    answers = iter([DEEZER_UNKNOWN, searchers.Fetched(note="transport failure: down")])
    lookup = published.genre_lookup(
        fetch=lambda _url: _fetched(next(answers)), sleep=lambda _seconds: None
    )
    monkeypatch.setattr(published, "for_lookup", lambda: lookup)

    job, _code, resumed = swept(folder)

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["answers"][published.SOURCE]["miss"] == 1
    assert tagging["answers"][published.SOURCE]["unreachable"] == 1
    (named,) = [w["message"] for w in resumed["warnings"] if w["code"] == tag_cli.PUBLISHED_UNREAD]
    assert "could not be read on 1 of the 2 files it was asked about (unreachable on 1)" in named
    assert "those files got no published genre from it" in named
    assert "no file in this run" not in named


def test_a_block_on_a_file_a_record_shop_declined_is_still_said(cfg, folder, silence, monkeypatch):
    """Beatport called the track by a catch-all, so the file is
    ``unmapped-genre`` whatever the general catalogue did, and no file in the
    run is ``sources-unread``. The block is still a sentence and not only a
    count."""
    place(folder, silence, "a")
    assert tags.write_tags(folder / "a.flac", {"artist": "Somebody", "isrc": ISRC})
    declined = searchers.Fetched(
        text=beatport_page([beatport_track("Somebody", "a", CATCH_ALL)]), status=200
    )
    bound(monkeypatch, _catalogues({"a": {searchers.BEATPORT: declined}}))
    general(monkeypatch, RATE_LIMITED)

    job, _code, resumed = swept(folder)

    (report,) = artifacts.committed(cfg, job.job_id)
    assert report["skipped"] == tag.UNMAPPED_GENRE
    assert report["unread"] == {published.SOURCE: "blocked"}
    codes = [warning["code"] for warning in resumed["warnings"]]
    assert tag_cli.SOURCES_UNREAD not in codes
    assert codes.count(tag_cli.PUBLISHED_UNREAD) == 1


def test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "a")
    assert tags.write_tags(folder / "a.flac", {"isrc": ISRC})
    bound(monkeypatch, _catalogues({"a": ALL_MISSED}))
    general(monkeypatch, '["a JSON answer in a shape this reader does not know"]')

    job, _code, resumed = swept(folder)

    (named,) = [w["message"] for w in resumed["warnings"] if w["code"] == tag_cli.PUBLISHED_UNREAD]
    assert "(parse-break on 1)" in named
    assert "A parse break is a defect in this software" in named
    (unread,) = [w["message"] for w in resumed["warnings"] if w["code"] == tag_cli.SOURCES_UNREAD]
    assert f"{published.SOURCE} parse-break on 1" in unread
    assert "A parse break is a defect" not in unread, (
        "the general catalogue's parse break is said once, by its own warning"
    )


def test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason(
    cfg, folder, silence, monkeypatch
):
    """AE4 at the surface a person reads. One file's fallbacks were blocked, so
    it is ``sources-unread``; the other's all answered, so it is ``no-isrc``.
    Both were never asked about at the general catalogue, and the warning
    counts both."""
    for name in ("a", "b"):
        place(folder, silence, name)
    bound(monkeypatch, _catalogues({"a": REFUSED_FALLBACKS, "b": ALL_MISSED}))

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert reports["a.flac"]["skipped"] == tag.SOURCES_UNREAD
    assert reports["b.flac"]["skipped"] == tag.NO_ISRC
    for report in reports.values():
        assert report["answers"][-1]["answer"] == tag.NO_ISRC
        assert report["answers"][-1]["note"] == "no ISRC was given"

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["skipped"][tag.NO_ISRC] == 1
    assert tagging["skipped"][tag.NO_HIT] == 0
    assert tagging["answers"][published.SOURCE][tag.NO_ISRC] == 2

    assert tag_cli.NO_ISRC_FILES == "tag-folder-no-isrc"
    (bare,) = [w["message"] for w in resumed["warnings"] if w["code"] == tag_cli.NO_ISRC_FILES]
    assert bare.startswith("2 files were not asked about at deezer")
    assert "not reported as tracks no catalogue carries" in bare
    codes = [warning["code"] for warning in resumed["warnings"]]
    assert tag_cli.PUBLISHED_UNREAD not in codes, "a catalogue never asked was not unread"


def test_a_published_word_with_no_folder_is_listed_as_unresolved(cfg, folder, silence, monkeypatch):
    """R3 at the report. The catalogue's own word is the one a person would add
    an alias for, so it is the string the summary names."""
    place(folder, silence, "a")
    assert tags.write_tags(folder / "a.flac", {"isrc": ISRC})
    bound(monkeypatch, _catalogues({"a": ALL_MISSED}))
    general(monkeypatch, deezer_track(), deezer_album(["Films/Games"]))

    job, _code, resumed = swept(folder)

    (report,) = artifacts.committed(cfg, job.job_id)
    assert report["skipped"] == tag.UNMAPPED_GENRE
    assert report["genre_written"] is None
    assert (report["source"], report["source_genre"]) == (published.SOURCE, "Films/Games")
    assert tags.read_genre_from_file(folder / "a.flac") is None
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["unresolved"] == {"Films/Games": 1}
    assert tagging["off_taxonomy"] == {}
    assert tagging["tagged"] == 0


def test_a_sweep_with_nothing_off_taxonomy_carries_no_such_warning(
    cfg, folder, silence, monkeypatch
):
    """The quiet case, which is every ordinary sweep.

    A warning that fires on a clean run soon goes unread, so the zero is
    asserted as its own property.
    """
    for name in ("a", "b"):
        place(folder, silence, name)
    bound(monkeypatch, answering({"a": hit("Deep House", "Deep House"), "b": hit("Techno")}))

    job, _code, resumed = swept(folder)

    assert resumed["data"]["progress"]["tagging"]["off_taxonomy"] == {}
    assert tag_cli.OFF_TAXONOMY not in [warning["code"] for warning in resumed["warnings"]]


def test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status(
    cfg, folder, silence, monkeypatch
):
    """U84. The repair runs on every item and its status reaches both surfaces.

    Two files carry the downloader's zeroed block, one already tagged, which a
    repair placed after the genre skip would miss. The third carries no picture.
    Every status is counted, zeroes included.
    """
    from tests.test_tagging_engine import _jpeg, blocks, plant

    for name, genre in (("a", None), ("b", SPECIFIC), ("c", None)):
        path = place(folder, silence, name, genre=genre)
        if name != "c":
            plant(path, _jpeg(320, 200))
    bound(monkeypatch, answering({}))

    job, _code, resumed = swept(folder)

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


def test_new_art_reaches_the_file_the_artifact_and_the_summary(cfg, folder, silence, monkeypatch):
    """U85 through the verb. The worker looks its image fetch up at call time.

    Four files: no genre and no picture, a genre and no picture, a genre and a
    picture, and one whose picture 404s. The first two get art, the third is
    never asked, and the fourth still gets its genre and says its art was
    unavailable, with every status counted.
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

    job, code, resumed = swept(folder)
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


def test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first(
    cfg, folder, silence, monkeypatch
):
    """U282 through the verb, with the shipped searcher and a recorded Discogs
    and Beatport. Three files: no genre and no picture, no genre and a picture,
    a genre and no picture. Discogs decides both genres; Beatport is asked
    twice, for the two missing covers, and never for the file whose picture is
    in place; the file that had a genre keeps it; the summary says Discogs
    tagged two, Beatport matched twice and was not asked once."""
    from tests.test_catalogue_searcher import ARTIST, BUCKET_GENRE, TITLE
    from tests.test_discogs_searcher import SENT, release, results, routed
    from tests.test_tagging_engine import _jpeg, plant

    names = {"a": None, "b": None, "c": SPECIFIC}
    for name, genre in names.items():
        path = place(folder, silence, name, genre=genre)
        assert tags.write_tags(path, {"artist": ARTIST, "title": TITLE})
    plant(folder / "b.flac", _jpeg(320, 200), dims=(320, 200, 24))

    cover = "https://geo-media.beatport.com/image_size/1400x1400/cover.jpg"
    row = beatport_track(ARTIST, TITLE, BUCKET_GENRE)
    row["release"] = {"release_image_uri": cover}
    seen: list[str] = []
    fetch = routed(
        search=results(7),
        releases={7: release(7, styles=("Deep House",))},
        beatport=beatport_page([row]),
        seen=seen,
    )
    asker = searchers.discogs_asker(token=SENT, fetch=fetch, sleep=lambda _s: None)

    def for_taxonomy(declared=None, refusals=None):
        return searchers.catalogue_searcher(
            TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, refusals=refusals
        )

    monkeypatch.setattr(searchers, "for_taxonomy", for_taxonomy)
    general(monkeypatch, None)
    fetched: list[str] = []

    def fetch_image(url: str) -> bytes:
        fetched.append(url)
        return _jpeg(1000, 1000)

    monkeypatch.setattr(searchers, "for_images", lambda: fetch_image)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    decided = routing.suggest_tag(TAXONOMY, "Deep House", source=searchers.DISCOGS).tag
    assert sum(url.startswith(searchers.BEATPORT_SEARCH) for url in seen) == 2
    assert sum(url.startswith(searchers.DISCOGS_SEARCH) for url in seen) == 3
    assert len(fetched) == 2
    assert tags.read_genre_from_file(folder / "a.flac") == decided
    assert tags.read_genre_from_file(folder / "b.flac") == decided
    assert tags.read_genre_from_file(folder / "c.flac") == SPECIFIC, "never re-tagged"

    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert {name: reports[f"{name}.flac"]["art_fetch"] for name in names} == {
        "a": tag.ART_EMBEDDED,
        "b": tag.ART_PRESENT,
        "c": tag.ART_EMBEDDED,
    }
    assert reports["a.flac"]["source"] == searchers.DISCOGS

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["tagged_by"][searchers.DISCOGS] == 2
    assert tagging["tagged_by"][searchers.BEATPORT] == 0
    assert tagging["answers"][searchers.DISCOGS]["matched"] == 3
    assert tagging["answers"][searchers.BEATPORT]["matched"] == 2
    assert tagging["answers"][searchers.BEATPORT][searchers.NOT_ASKED] == 1


def test_the_sweeps_unread_warning_names_discogs_first(cfg, folder, silence, monkeypatch):
    """U282: the summary counts Discogs first, so the sentence a person reads
    names the catalogues in that order. File a: Discogs times out and Beatport
    misses. File b: Discogs misses and Beatport refuses. Both stay askable,
    and the warning names Discogs' outage before Beatport's refusal."""
    from tests.test_discogs_searcher import SENT, results

    place(folder, silence, "a")
    place(folder, silence, "b")
    seen: list[str] = []

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        query = url.split("?", 1)[-1]
        if url.startswith(searchers.BEATPORT_SEARCH):
            if query.endswith("+b") or query.endswith("q=b"):
                return BEATPORT_CHALLENGE
            return searchers.Fetched(text=beatport_page([]), status=200)
        if "track=a" in query:
            return searchers.Fetched(note="timed out")
        return searchers.Fetched(text=results(), status=200)

    asker = searchers.discogs_asker(token=SENT, fetch=fetch, sleep=lambda _s: None)
    monkeypatch.setattr(
        searchers,
        "for_taxonomy",
        lambda declared=None, refusals=None: searchers.catalogue_searcher(
            TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, refusals=refusals
        ),
    )
    general(monkeypatch, None)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert reports["a.flac"]["unread"] == {searchers.DISCOGS: "unreachable"}
    assert reports["b.flac"]["unread"] == {searchers.BEATPORT: "blocked"}
    unread = {w["code"]: w["message"] for w in resumed["warnings"]}[tag_cli.SOURCES_UNREAD]
    across = unread.split("Across the sweep: ", 1)[1]
    assert across.index(searchers.DISCOGS) < across.index(searchers.BEATPORT), across


def test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file(
    cfg, folder, silence, monkeypatch
):
    """U282's review, round two: Discogs answers 401 and Beatport matches all
    three files. They are tagged by Beatport as before, the token is sent once,
    and the sweep says Discogs refused it rather than ending clean, without
    counting the files as having no token."""
    from tests.test_catalogue_searcher import ARTIST, BUCKET_GENRE, TITLE
    from tests.test_discogs_searcher import SENT, routed

    for name in ("a", "b", "c"):
        path = place(folder, silence, name)
        assert tags.write_tags(path, {"artist": ARTIST, "title": TITLE})
    seen: list[str] = []
    fetch = routed(
        search=searchers.Fetched(note="HTTP 401", status=401),
        beatport=beatport_page([beatport_track(ARTIST, TITLE, BUCKET_GENRE)]),
        seen=seen,
    )
    asker = searchers.discogs_asker(token=SENT, fetch=fetch, sleep=lambda _s: None)
    monkeypatch.setattr(
        searchers,
        "for_taxonomy",
        lambda declared=None, refusals=None: searchers.catalogue_searcher(
            TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, refusals=refusals
        ),
    )
    general(monkeypatch, None)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed
    assert sum(url.startswith(searchers.DISCOGS_SEARCH) for url in seen) == 1
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["tagged_by"][searchers.BEATPORT] == 3
    assert tagging["discogs_token_refused"] == 3
    assert tagging["discogs_without_token"] == 0
    warnings = {w["code"]: w["message"] for w in resumed["warnings"]}
    assert tag_cli.DISCOGS_NO_TOKEN_FILES not in warnings
    refused = warnings[tag_cli.DISCOGS_TOKEN_REFUSED_FILES]
    assert "refused the recorded token" in refused and "3 file(s)" in refused
    assert "crate login discogs-token" in refused
    assert SENT not in json.dumps(resumed)


def test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep(
    cfg, folder, silence, monkeypatch
):
    """U260 through the verb. Ten files of one album name one cover address.

    Only the shipped image fetch's HTTP getter and sleep are replaced, so the
    binder the worker calls per item, its memory and the encoder's are the
    shipped ones.
    """
    from tests.test_album_cover_once import ALBUM, Host
    from tests.test_tagging_engine import _jpeg, blocks

    names = [f"t{index:02d}" for index in range(10)]
    for name in names:
        place(folder, silence, name)
    cover = _jpeg(1000, 1000)
    bound(
        monkeypatch,
        answering(
            {
                name: SearchHit(
                    genre=SPECIFIC,
                    source=searchers.BEATPORT,
                    source_genre="deep house",
                    art_url=ALBUM,
                )
                for name in names
            }
        ),
    )
    host = Host({ALBUM: [cover]})
    slept: list[float] = []
    real_fetch = searchers.default_image_fetch
    monkeypatch.setattr(
        searchers, "default_image_fetch", lambda: real_fetch(get=host, sleep=slept.append)
    )
    expected = art.to_cdj_jpeg(cover).data
    encoded: list[bytes] = []
    real_encode = art.to_cdj_jpeg

    def counting(data, *args, **kwargs):
        encoded.append(data)
        return real_encode(data, *args, **kwargs)

    monkeypatch.setattr(art, "to_cdj_jpeg", counting)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    assert host.asked == [ALBUM]
    assert len(slept) == 1
    assert encoded == [cover]
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert {reports[f"{name}.flac"]["art_fetch"] for name in names} == {tag.ART_EMBEDDED}
    for name in names:
        (block,) = blocks(folder / f"{name}.flac")
        assert block.data == expected
        assert (block.width, block.height, block.depth) == (800, 800, 24)


def test_the_counts_are_read_off_the_artifacts_rather_than_accumulated_in_memory(
    cfg, folder, silence, monkeypatch
):
    """What makes the number true across a resume.

    A sweep continued tomorrow has every report on disk, and the person means
    all of them. The total is asserted against what the queue committed, so a
    summary counting only this invocation fails.
    """
    for name in ("a", "b", "c"):
        place(folder, silence, name)
    bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))

    job, _code, resumed = swept(folder)

    tagging = resumed["data"]["progress"]["tagging"]
    counted = tagging["tagged"] + sum(tagging["skipped"].values())
    assert counted == len(artifacts.committed(cfg, job.job_id))
    assert counted == resumed["data"]["progress"]["total"]


# The two zeroes, which are not one zero


def test_a_folder_holding_no_audio_queues_nothing_and_says_which_zero_it_is(cfg, folder):
    """AE3. Nothing is queued, and the exit code is still success.

    ``core.jobs`` reports a job with no items as SUCCEEDED, so queueing one
    would report a clean sweep over a folder nothing walked.
    """
    (folder / "cover.jpg").write_bytes(b"not audio")

    code, envelope = drive(["tag", "folder", "--queue-only", str(folder)])

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

    The parser accepts an empty string and ``Path("")`` is the current
    directory, so this writing verb would sweep the working directory. It is a
    no-op rather than a refusal, since a refusal needs its own slug in
    ``cause.REASONS``. Asserted with audio in the working directory, as it
    passes trivially without.
    """
    place(folder, silence, "a")
    monkeypatch.chdir(folder)

    code, envelope = drive(["tag", "folder", "--queue-only", ""])

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

    ``acquire`` stages every item under a dot directory in the download root,
    and a staged file is a killed attempt's partial download or evidence a tag
    write would alter. It reports the SAME zero as an empty folder, since there
    is no audio here to tag.
    """
    staged = folder / acquire_cli.ACQUIRE_STAGING_DIRNAME / "job-1" / "0" / "partial"
    place(staged.parent, silence, staged.name)

    code, envelope = drive(["tag", "folder", "--queue-only", str(folder)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert [warning["code"] for warning in envelope["warnings"]] == ["tag-folder-no-audio"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_real_track_beside_the_staging_tree_is_still_queued(cfg, folder, silence):
    """The other half, because the test above passes for a verb that queues NOTHING.

    Skipping the staging tree must not cost the sweep of committed tracks
    beside it. The identifier is asserted too, being relative to the frozen
    folder.
    """
    place(folder, silence, "committed")
    staged = folder / acquire_cli.ACQUIRE_STAGING_DIRNAME / "job-1" / "0" / "partial"
    place(staged.parent, silence, staged.name)

    code, envelope = drive(["tag", "folder", "--queue-only", str(folder)])

    assert code == int(ExitCode.OK), envelope
    assert list(item_states(tag_job().job_id)) == ["committed.flac"]


def test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one(cfg, tmp_path):
    """Both walk to nothing, and the person's next move is different for each.

    One says put some audio in it, the other says the folder does not exist.
    Folded together, a typed path looks like an empty download directory.
    """
    code, envelope = drive(["tag", "folder", "--queue-only", str(tmp_path / "no-such-folder")])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert [warning["code"] for warning in envelope["warnings"]] == ["tag-folder-absent"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


# The failure part way through, and the resume that follows it


def test_a_searcher_that_raises_part_way_fails_only_its_own_item(cfg, folder, silence, monkeypatch):
    """R19x's first half, and the reason a decline and a refusal are not one thing.

    The searcher raises when it could not READ a catalogue at all. That item
    fails, its neighbours stay done and written, and the job carries a cause,
    so nobody is told the folder was tagged.
    """
    for name in ("a", "b", "c"):
        place(folder, silence, name)
    table = {name: hit("deep house", SPECIFIC) for name in ("a", "b", "c")}
    bound(monkeypatch, raising_on(answering(table), "b"))

    job, code, resumed = swept(folder)

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


def test_a_retried_job_drives_only_the_item_that_failed(cfg, folder, silence, monkeypatch):
    """R19x, and the guarantee this whole seam exists for.

    Asserted by counting the searcher's calls, since a resume re-asking about
    files already tagged leaves the same item states and costs two more
    requests against a rate limited source.
    """
    for name in ("a", "b", "c"):
        place(folder, silence, name)
    table = {name: hit("deep house", SPECIFIC) for name in ("a", "b", "c")}
    bound(monkeypatch, raising_on(answering(table), "b"))
    drive(["tag", "folder", "--queue-only", str(folder)])
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

    Refused rather than reported done, which would be a clean report over
    unreadable state. The slug is the SHARED ``source-missing`` (R-251), and
    not an internal error, since deleting one's own download is not a defect.
    """
    for name in ("a", "b"):
        place(folder, silence, name)
    bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))

    drive(["tag", "folder", "--queue-only", str(folder)])
    job = tag_job()
    (folder / "b.flac").unlink()
    code, resumed = drive(resume_argv(job.job_id))

    assert code != int(ExitCode.OK), resumed
    assert item_states(job.job_id) == {
        "a.flac": jobs.ItemState.DONE,
        "b.flac": jobs.ItemState.FAILED,
    }
    assert item_causes(job.job_id) == {"b.flac": "source-missing"}


# The resume argv


def test_the_resume_argv_round_trips_the_frozen_folder_and_asks_for_no_run(
    cfg, folder, silence, monkeypatch
):
    """The payload is frozen at queue time, so only the verb can rebuild it.

    The run flag is asserted as a whole token, since the run id flag contains
    it and a substring check would call a broken argv clean. This verb declares no gate,
    so a resume minting a run would ask a question nobody posed.
    """
    place(folder, silence, "a")
    bound(monkeypatch, answering({}))

    drive(["tag", "folder", "--queue-only", str(folder)])
    job = tag_job()

    argv = resume_argv(job.job_id)

    assert argv == ["tag", "folder", job.payload["folder"], "--job", job.job_id]
    assert Path(job.payload["folder"]) == folder
    assert "--run" not in argv, argv


# U5: ``crate tag retag`` from the confirmation to the corrected file, through
# the verb, each gate answered by ``approve_and_queue`` as R34's two acts.

#: The confirmation this verb raises over its plan. Spelled once here so the
#: cases below cannot disagree with each other about which gate they answered.
RETAG_GATE = "tag.retag.confirm"


@pytest.fixture
def repair_on(cfg) -> config.Config:
    """``cfg`` with the module that gates this verb switched on.

    ``tag.retag`` is gated by ``repair``, and under the SLIM profile the
    fixture configures the parser does not offer the verb at all. Turning the
    module on makes it reachable through the real dispatcher.
    """
    built = config.from_dict(valid_data(Path(cfg.library.root), modules={"repair": True}))
    config.save(built)
    config.reset_cache()
    return built


def coarse(folder: Path, silence: Path, name: str) -> Path:
    """One file carrying the catch-all this verb exists to replace.

    The value is the declared taxonomy's own, so a template edit moves the
    fixture with it.
    """
    return place(folder, silence, name, CATCH_ALL)


def selected(folder: Path) -> list[Path]:
    """What a fresh walk of the folder would take, as it stands right now."""
    return [candidate.path for candidate in retag.select(folder, declared=TAXONOMY).candidates]


def test_the_retag_gate_shows_every_row_the_digest_was_taken_over(repair_on, folder, silence):
    """The gate carried the question and not one file (R-693). Its ``shown``
    now holds the plan rows the digest was taken over, each file with the genre
    it carries, and the folder in front of them."""
    del repair_on
    for name in ("a", "b"):
        coarse(folder, silence, name)
    expected = retag_cli.plan_for(str(folder.absolute()), TAXONOMY)

    code, refused = drive(["tag", "retag", str(folder)])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["items"] == expected["items"]
    assert [row["current"] for row in shown["items"]] == [CATCH_ALL, CATCH_ALL]
    assert shown["digest"] == expected["digest"]
    assert shown["count"] == 2
    assert shown[retag_cli.FOLDER_KEY] == str(folder.absolute())


def test_the_retag_resume_gate_shows_the_frozen_rows_it_asks_about(repair_on, folder, silence):
    """A resume on a run holding no answer shows the rows the confirmation was
    recorded against, read off the frozen payload and never off a fresh walk."""
    del repair_on
    for name in ("a", "b"):
        coarse(folder, silence, name)
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    with jobs.open_store() as store:
        payload = jobs.get(store, job_id).payload
    # THE FOLDER MOVES ON, so a screen built from a fresh walk would differ.
    assert tags.write_genre(folder / "a.flac", SPECIFIC), "the stand-in write failed"

    code, refused = drive(["tag", "retag", str(folder), "--job", job_id])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == RETAG_GATE
    shown = refused["cause"]["detail"]["shown"]
    assert shown["items"] == payload[retag_cli.ITEMS_KEY]
    assert len(shown["items"]) == 2, "the frozen rows were not what the screen showed"
    assert shown["count"] == 2
    assert shown[retag_cli.FOLDER_KEY] == payload[retag_cli.FOLDER_KEY]
    assert shown["digest"] == retag_cli.digest_for(
        payload[retag_cli.FOLDER_KEY], payload[retag_cli.ITEMS_KEY]
    )


def test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale(
    repair_on, folder, silence, monkeypatch
):
    """KTD8 and AE4, and the permanent stall this unit would otherwise ship.

    A corrected file leaves the selection, so a plan rebuilt by walking digests
    differently from the confirmed one and every resume meets ``DecisionStale``
    for ever. The correction is written rather than driven, since the selection
    shrinking is the mechanism and ``core.tags.write_genre`` the only effect.
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


# The binding


def test_the_tag_retag_key_resolves_to_a_worker():
    """The other half of R-203 this unit closes, asserted against the table.

    ``tests/test_handlers.py`` checks each queued verb sits in exactly ONE of
    the two mappings, which ``HANDLERS_NOT_YET_BOUND`` satisfies. Only an
    assertion naming this key tells "declared as unbound" from "bound".
    """
    key = registry.entry("tag.retag").handler_key

    assert handlers.is_known(key), f"{key} still has no worker"
    assert handlers.unbound_reason(key) is None
    assert callable(handlers.resolve(key))


# The happy path


def test_three_confirmed_files_go_from_pending_to_done_and_carry_a_specific_genre(
    repair_on, folder, silence, monkeypatch
):
    """The whole seam in one case: confirm, queue, drive, write, and read back.

    The files are read back off disk: a worker reporting a genre it never wrote
    would still drive every item to done. The items are the confirmed rows, one
    per candidate path, since a shell queueing its own walk would second guess
    what was confirmed.
    """
    for name in ("a", "b", "c"):
        coarse(folder, silence, name)
    searcher = bound(monkeypatch, answering({name: hit("deep house", SPECIFIC) for name in "abc"}))

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

    All three files were confirmed and did three different things. A summary
    kept in memory would report only today's part of a continued sweep. Zeroes
    included, on ``adopt.scan.categories``'s rule: otherwise "none here" and
    "not counted" read the same.
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


# The zeroes, which are asked about and then queue nothing


def answered(argv: list[str], answer: str) -> tuple[int, dict]:
    """Drive ``argv`` to the retag gate, answer it as a person, and drive it on that run."""
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == RETAG_GATE
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, RETAG_GATE, answer, "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    return drive(["--run", run_id, *argv])


@pytest.mark.parametrize("absent", [False, True])
def test_an_empty_plan_is_still_asked_about_and_queues_nothing_and_says_which_zero(
    repair_on, folder, silence, absent
):
    """R12: asked about like its sibling; nothing coarse and no folder are two zeroes."""
    place(folder, silence, "already-specific", SPECIFIC)
    named = str(folder.parent / "no-such-folder") if absent else str(folder)

    code, envelope = answered(["tag", "retag", named], "apply")

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert [warning["code"] for warning in envelope["warnings"]] == [
        "tag-retag-folder-absent" if absent else "tag-retag-nothing-coarse"
    ]
    assert queued_jobs() == ()


def test_answering_the_confirmation_with_abort_queues_nothing_and_writes_nothing(
    repair_on, folder, silence, monkeypatch
):
    """The branch a person reaches by reading the plan and saying no.

    The payload is the declared ``job_state`` shape, through ``shell.no_op``, so
    this verb's zero paths cannot reintroduce R-234 apart from the sibling's.
    ``tests/cli_drive.drive`` validates the envelope, so the shape fails here as
    well as the outcome.
    """
    coarse(folder, silence, "a")
    bound(monkeypatch, answering({}))

    code, envelope = answered(["tag", "retag", str(folder)], "abort")

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert envelope["data"]["state"] == "declined"
    assert queued_jobs() == ()
    assert tags.read_genre_from_file(folder / "a.flac") == CATCH_ALL


# The file moved between the confirmation and the drive


@pytest.mark.parametrize(
    ("by_hand", "read_back", "reason"),
    [("Ambient", ("Ambient",), retag.GENRE_SPECIFIC), ("", (None, ""), retag.NO_GENRE)],
)
def test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner(
    repair_on, folder, silence, monkeypatch, by_hand, read_back, reason
):
    """A curation made since outranks this sweep; a blank genre is fill if empty's."""
    coarse(folder, silence, "a")
    searcher = bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    assert tags.write_genre(folder / "a.flac", by_hand)
    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(folder / "a.flac") in read_back
    assert searcher.asked == [], "the catalogue was asked about a file nobody may write"
    report = retag_reports(repair_on, job_id)[str(folder / "a.flac")]
    assert report["reason"] == reason
    assert report["written"] is None


def test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done(
    repair_on, folder, silence, monkeypatch
):
    """R15. The folder is not frozen, so this is reachable input.

    Refused rather than reported done, which would be a clean report over
    unreadable state. The slug is the SHARED ``source-missing`` (R-251), and
    not an internal error, since deleting one's own file is not a defect.
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


# The review queue, reached through the worker rather than through the sweep


def test_an_answer_that_is_itself_too_coarse_reaches_the_review_queue(
    repair_on, folder, silence, monkeypatch
):
    """The engine's rule, asserted through the WORKER that now runs it.

    The worker opens a review queue per item against the FROZEN configuration,
    unlike ``retag_folder``'s sweep. A catch-all written to a file here would
    never be selected again.
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

    Asking the catalogue before reading the verdict would spend a request per
    run on an answered question and let a fresh answer overwrite it. Only
    asserting the searcher was never asked separates the two orders.
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


# The failure part way through, and the resume that follows it


def test_a_searcher_that_raises_part_way_through_a_retag_fails_only_its_own_item(
    repair_on, folder, silence, monkeypatch
):
    """R19x's first half. A network dropping out mid folder is not a decline.

    The unanswered item fails, its neighbours stay done and written, and the
    job carries a cause, so nobody is told the folder was corrected.
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


def test_a_retried_retag_drives_only_the_item_that_failed(repair_on, folder, silence, monkeypatch):
    """R19x, and the guarantee the whole per item seam exists for.

    Asserted by counting the searcher's calls, since a resume re-asking about
    files already corrected leaves the same item states and costs two more
    requests against a rate limited source.
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

    The database half of this verb is deferred, so the library row keeps the
    catch-all the file no longer carries. A corrected file stops being
    selectable, so only the committed artifact, naming the path and the old and
    new values, can recover the row; a dropped field fails here.
    """
    for name in ("a", "b"):
        coarse(folder, silence, name)
    bound(monkeypatch, raising_on(answering({"a": hit("deep house", SPECIFIC)}), "b"))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    drive(resume_argv(job_id))

    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    sources = {
        path.relative_to(SRC_ROOT): path.read_text(encoding="utf-8")
        for path in SRC_ROOT.rglob("*.py")
    }
    planners = {relative for relative, source in sources.items() if "plan_library(" in source}
    appliers = {relative for relative, source in sources.items() if "apply_library(" in source}
    assert planners == {Path("cratekit/tagging/retag.py")}, (
        f"the file to row plan gained a caller in {planners}, so R-185's measurement "
        f"is out of date and this case is asserting about a deferral that ended"
    )
    assert appliers == {Path("cratekit/tagging/retag.py"), Path("cratekit/tagging/rows.py")}, (
        f"the database half is applied from {appliers}; the row verb is its one "
        f"caller, and the retag verb gaining one ends the deferral this case measures"
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


def job_cause(job_id: str):
    """The cause the QUEUE recorded, which is the one a refusal has to carry on.

    Read back from the store, because a cause described in the test's own words
    would pass against a verb that replaced the job's cause with its own, the
    shape ``origin`` is append-only to prevent.
    """
    with jobs.open_store() as store:
        return jobs.get(store, job_id).cause


def test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs(
    repair_on, folder, silence, monkeypatch
):
    """R-185's COST, reproduced as the thing a person is left holding.

    The file is corrected and the row is not, and no later run finds the row.
    The warning names the act, the row's own verb, not just the defect, since a
    warning that only announced a disagreement leaves nothing to do. The folder
    is in the text, because a resume's envelope is read later beside others.
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
    assert "`crate tag rows`" in told["message"], (
        f"the run named a disagreement and no act to settle it: {told['message']!r}"
    )


def test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox(
    repair_on, folder, silence, monkeypatch
):
    """The zero half, and it is what keeps the warning worth reading.

    A sweep that wrote no genre left no row stale, and an instruction shown
    whether or not it applies stops being read. Driven through the decline, not
    an empty folder, which never queues and so could not reach the resume path.
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

    A job closed with a cause leaves through that cause (R-225), yet files
    corrected before the failure have stale rows. The step rides the
    remediation's ``steps``, since a refusal carries no warnings, and the retry
    remedy stays first.
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
    stored = job_cause(job_id)
    assert refused["cause"]["reason"] == stored.reason
    assert refused["cause"]["detail"] == dict(stored.detail)
    assert tuple(refused["cause"]["origin"])[: len(stored.origin)] == stored.origin, (
        "the trail was shortened or rewritten, so some hop re-created the cause "
        "rather than extending what the job was already carrying"
    )
    assert steps[: len(stored.remediation.steps)] == list(stored.remediation.steps), (
        "the reload replaced the failure's own steps instead of joining them"
    )
    assert len(steps) == len(stored.remediation.steps) + 1


def refusing_writes_on(monkeypatch, *names: str) -> None:
    """The one genre writer, answering False for the files named (R-1103).

    What ``tags.write_genre`` answers for a locked or read only file. Patched
    after the fixture files are placed, which tag through the same writer, and
    patched at all because root ignores a read only mode and the immutable flag
    is Linux's alone and privileged.
    """
    real = tags.write_genre

    def writer(path: Path, genre: str) -> bool:
        if path.stem in names:
            return False
        return real(path, genre)

    monkeypatch.setattr(tags, "write_genre", writer)


def test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected(
    repair_on, folder, silence, monkeypatch
):
    """The brief's first scenario, through the verb a person types (R-1103).

    The refusing file's item fails under ``tag-retag-unwritten`` with the file
    named, its report is never committed, so ``corrected`` counts the two that
    landed, and the files are read back off disk rather than off the report.
    """
    for name in ("a", "b", "c"):
        coarse(folder, silence, name)
    bound(monkeypatch, answering({name: hit("deep house", SPECIFIC) for name in "abc"}))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    refusing_writes_on(monkeypatch, "b")

    code, refused = drive(resume_argv(job_id))

    assert code == int(ExitCode.PRECONDITION), refused
    refusing = str(folder / "b.flac")
    assert item_causes(job_id) == {refusing: retag.UNWRITTEN_REASON}
    states = item_states(job_id)
    assert states[str(folder / "a.flac")] is jobs.ItemState.DONE
    assert states[str(folder / "c.flac")] is jobs.ItemState.DONE
    assert tags.read_genre_from_file(folder / "b.flac") == CATCH_ALL
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    assert tags.read_genre_from_file(folder / "c.flac") == SPECIFIC
    assert refused["cause"]["reason"] == retag.UNWRITTEN_REASON
    # THE FILE IS NAMED ON THE ITEM'S OWN CAUSE, which the job's carries as its
    # inner one, beside the counts of what finished and what failed.
    named = refused["cause"]["inner"]
    assert named["reason"] == retag.UNWRITTEN_REASON
    assert named["detail"]["path"] == refusing
    assert named["detail"]["genre"] == SPECIFIC
    assert named["detail"]["current"] == CATCH_ALL
    assert refusing in named["message"]
    reports = retag_reports(repair_on, job_id)
    assert refusing not in reports, "a file that kept its old genre has no report"
    assert sorted(r["written"] for r in reports.values()) == [SPECIFIC, SPECIFIC]
    steps = refused["cause"]["remediation"]["steps"]
    assert any(str(folder) in step and "reload" in step for step in steps), (
        f"two files were corrected and their rows are stale: {steps}"
    )


def test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload(
    repair_on, folder, silence, monkeypatch
):
    """Nothing was corrected, so no row went stale and nothing is sent to rekordbox.

    Every item failed, so the job engine leaves through its own ``no-evidence``
    carrying the item's cause, which names the file.
    """
    coarse(folder, silence, "a")
    bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    refusing_writes_on(monkeypatch, "a")

    code, refused = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), refused
    named = refused["cause"]["inner"]
    assert named["reason"] == retag.UNWRITTEN_REASON
    assert named["detail"]["path"] == str(folder / "a.flac")
    assert tags.read_genre_from_file(folder / "a.flac") == CATCH_ALL
    assert retag_reports(repair_on, job_id) == {}
    steps = refused["cause"]["remediation"]["steps"]
    assert not any("reload" in step for step in steps), steps


def test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer(
    repair_on, folder, silence, monkeypatch
):
    """What a person reads at the terminal names the file, not only the counts."""
    for name in ("a", "b"):
        coarse(folder, silence, name)
    bound(monkeypatch, answering({name: hit("deep house", SPECIFIC) for name in "ab"}))
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    refusing_writes_on(monkeypatch, "b")

    code, text = drive_human(resume_argv(job_id))

    assert code == int(ExitCode.PRECONDITION), text
    assert retag.UNWRITTEN_REASON in text
    assert f"{folder / 'b.flac'} would not take the genre {SPECIFIC!r}" in text, text


def test_a_parked_retag_keeps_both_the_block_and_the_reload(
    repair_on, folder, silence, monkeypatch
):
    """R-290 through the one shell that REBUILDS its refusal, found by the review.

    A parked job leaves as ``JobBlocked`` and the dispatcher reads that TYPE as
    blocked. ``with_reload_step`` builds a new exception to append its step, so
    it must keep the type, or a parked retag reads ``failed``.
    """
    for name in ("a", "b", "c"):
        coarse(folder, silence, name)
    inner = answering({name: hit("deep house", SPECIFIC) for name in "abc"})

    def parking_on_b(artist: str, name: str):
        if name == "b":
            raise jobs.Parked(
                refuse("provider-blocked", "the catalogue refused this client", origin=("test",)).cause
            )
        return inner(artist, name)

    parking_on_b.asked = inner.asked  # type: ignore[attr-defined]
    bound(monkeypatch, parking_on_b)
    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    code, refused = drive(resume_argv(job_id))

    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.BLOCKED, refused
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    assert code != int(ExitCode.OK), refused
    assert refused["outcome"] == "blocked", refused
    steps = refused["cause"]["remediation"]["steps"]
    assert any(str(folder) in step and "reload" in step for step in steps), steps


def test_a_retag_that_failed_before_correcting_anything_names_no_reload(
    repair_on, folder, silence, monkeypatch
):
    """The zero half of the refusal, and it is the half that keeps it honest.

    A sweep whose only item could not be answered wrote no genre, so no row
    went stale. Appending the reload to every failure would send a person to
    reconcile a library against a run that changed nothing in it.
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

    This envelope is the last thing the person reads in the terminal. It cannot
    know how many files will be corrected, but every planned file was selected
    as too coarse, so saying nothing is the worse answer. The three drives are
    spelled out, since ``approve_and_queue`` consumes the envelope under test.
    """
    coarse(folder, silence, "a")
    bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))

    verb = ["tag", "retag", str(folder)]
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, decision = drive(["run", "decide", run_id, RETAG_GATE, "apply", "--actor", "a-person"])
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

    Nothing in ``src`` reaches the row relink, so declaring ``db_metadata``
    would say something false in the registry. The cloud sync decision goes
    with it, since this verb opens no database. The two are asserted together,
    because restoring either alone leaves a registry the contract suite refuses.
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


# The resume argv


def test_the_retag_resume_argv_carries_the_gate_run_before_the_verb_path(
    repair_on, folder, silence, monkeypatch
):
    """The flag belongs to the ROOT parser, so its position is the contract.

    A decision belongs to the invocation, and the run flag after the verb path
    is not a flag this parser accepts. Asserted through the real ``argv_for``, so
    the command line checked is the one the job driver would spawn.
    """
    coarse(folder, silence, "a")
    bound(monkeypatch, answering({}))
    gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)

    argv = resume_argv(job_id)

    assert argv == ["--run", gate_run, "tag", "retag", str(folder), "--job", job_id]


# R-678: the queueing half names the job it queued


def test_queueing_a_folder_names_the_job_and_the_command_that_drives_it(cfg, folder, silence):
    """Sitting 9: ``ok`` in under a second, and the identifier nowhere a person reads."""
    place(folder, silence, "a")

    code, text = drive_human(["tag", "folder", "--queue-only", str(folder)])

    assert code == int(ExitCode.OK), text
    job = tag_job()
    lines = text.splitlines()
    assert f"  job: {job.job_id}, queued" in lines, text
    drives = shlex.join(["crate", "tag", "folder", str(folder.absolute()), "--job", job.job_id])
    assert f"  drive it with: {drives}" in lines, text


def test_a_folder_with_nothing_to_tag_names_no_job(cfg, folder):
    code, text = drive_human(["tag", "folder", "--queue-only", str(folder)])

    assert code == int(ExitCode.OK), text
    assert text.splitlines()[0] == "tag.folder: no_op", text
    assert "  job:" not in text, text


# U192: run by hand, the verb drives the sweep it queues, in one command


def test_tag_folder_by_hand_queues_and_drives_its_sweep_to_succeeded_in_one_call(
    cfg, folder, silence, monkeypatch
):
    """The brief's first scenario, read back off the files rather than the report."""
    place(folder, silence, "a")
    place(folder, silence, "b")
    searcher = bound(
        monkeypatch,
        answering({"a": hit("deep house", SPECIFIC), "b": hit("deep house", SPECIFIC)}),
    )

    code, settled = drive(["tag", "folder", str(folder)])

    assert code == int(ExitCode.OK), settled
    job = tag_job()
    assert settled["data"]["job_id"] == job.job_id
    assert settled["data"]["state"] == "succeeded"
    progress = settled["data"]["progress"]
    assert progress["settled"] == progress["total"] == 2
    assert progress["tagging"]["tagged"] == 2, "the settled answer is the resume's summary"
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    assert tags.read_genre_from_file(folder / "b.flac") == SPECIFIC
    assert searcher.asked == [("", "a"), ("", "b")], "a file was asked about twice"
    with jobs.open_store() as store:
        assert jobs.get(store, job.job_id).attempts == 1


def test_tag_folder_by_hand_prints_the_settled_job_and_no_drive_command(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "a")
    bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))

    code, text = drive_human(["tag", "folder", str(folder)])

    assert code == int(ExitCode.OK), text
    job = tag_job()
    lines = text.splitlines()
    assert f"  job: {job.job_id}, succeeded" in lines, text
    assert "  items: 1 of 1 settled" in lines, text
    assert "drive it with" not in text, "a settled job was offered a second driver"


def test_tag_folder_queue_only_returns_the_sweep_queued_with_nothing_asked(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "a")
    searcher = bound(monkeypatch, answering({"a": hit("deep house", SPECIFIC)}))

    code, queued = drive(["tag", "folder", "--queue-only", str(folder)])

    assert code == int(ExitCode.OK), queued
    assert queued["data"]["state"] == "queued"
    assert set(item_states(tag_job().job_id).values()) == {jobs.ItemState.PENDING}
    assert searcher.asked == [], "a queue only call drove the sweep"


def test_tag_folder_queue_only_beside_job_is_refused_before_anything_is_queued(
    cfg, folder, silence
):
    place(folder, silence, "a")

    code, refused = drive(["tag", "folder", str(folder), "--job", "j-1", "--queue-only"])

    assert code == 2, "argparse's own refusal, before the verb runs"
    assert refused == {}, "the verb ran and answered with an envelope"
    with jobs.open_store() as store:
        assert list(jobs.list_jobs(store)) == []


def test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it(
    cfg, folder, silence, monkeypatch
):
    """A real SIGINT through the engine's checkpoint, in the call that queued the sweep."""
    import signal

    for name in ("a", "b", "c", "d"):
        place(folder, silence, name)
    answers = answering({name: hit("deep house", SPECIFIC) for name in "abcd"})

    def interrupting(artist: str, title: str):
        found = answers(artist, title)
        if len(answers.asked) == 2:
            os.kill(os.getpid(), signal.SIGINT)
        return found

    interrupting.asked = answers.asked  # type: ignore[attr-defined]
    bound(monkeypatch, interrupting)

    code, stopped = drive(["tag", "folder", str(folder)])

    assert code == int(ExitCode.INTERRUPTED), stopped
    assert stopped["outcome"] == "cancelled"
    job = tag_job()
    assert job.state is jobs.JobState.QUEUED, "the interrupted sweep was left closed"
    command = shlex.join(["crate", *resume_argv(job.job_id)])
    steps = stopped["cause"]["remediation"]["steps"]
    assert steps[0] == f"resume it with: {command}"
    done = sorted(i for i, s in item_states(job.job_id).items() if s is jobs.ItemState.DONE)
    assert done == ["a.flac"], "the interrupted item was committed, or nothing was"
    assert "1 of 4 items settled" in steps[1]

    bound(monkeypatch, answers)
    code, resumed = drive(resume_argv(job.job_id))

    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert [title for _artist, title in answers.asked].count("a") == 1, (
        "the resume asked about a file the interrupted drive had settled"
    )


def test_the_off_taxonomy_warning_names_a_folders_own_name_with_its_one_answer():
    """R-1184: a folder's own name in another case is named with the one
    answer it has, and without a readable taxonomy the warning is unchanged."""
    from cratekit.core import taxonomy

    declared = taxonomy.load_taxonomy(taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME))
    summary = {"tagged": 3, "off_taxonomy": {"gqom": 1, "nonelectronic": 2}}
    (plain,) = tag_cli._off_taxonomy_warning(summary)
    (named,) = tag_cli._off_taxonomy_warning(summary, declared)
    assert named["message"].startswith(plain["message"] + ". A word that is")
    assert "'nonelectronic' is the name of the genre folder NonElectronic" in named["message"]
    assert "neither answer takes the word" in named["message"]


def test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks(
    cfg, folder, silence, monkeypatch
):
    """R-1184 through the dispatcher. The sweep writes the catalogue's word as
    given, so a folder's own name in another case is on disk and named, with
    the alias to its own folder. A copy that no longer loads at the report
    keeps the plain warning rather than refusing the report."""
    from tests.test_active_taxonomy import write_active

    for name in ("a", "b"):
        place(folder, silence, name)
    bound(
        monkeypatch,
        answering(
            {
                "a": hit("breaks / d&b / dubstep", "breaks / d&b / dubstep", off_taxonomy=True),
                "b": hit("gqom", "gqom", off_taxonomy=True),
            }
        ),
    )
    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed
    message = {w["code"]: w["message"] for w in resumed["warnings"]}[tag_cli.OFF_TAXONOMY]
    assert "crate taxonomy alias 'breaks / d&b / dubstep' 'Breaks / D&B / Dubstep'" in message
    assert "gqom" in message.split("takes one answer only")[0]
    assert "gqom" not in message.split("takes one answer only")[1]

    write_active(cfg, "this is not a taxonomy [[[")
    code, again = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), again
    plain = {w["code"]: w["message"] for w in again["warnings"]}[tag_cli.OFF_TAXONOMY]
    assert "takes one answer only" not in plain and "breaks / d&b / dubstep" in plain


def test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit(
    cfg, folder, silence, monkeypatch
):
    """U244, through the verb: the default walk, Beatport missing both files and
    no Discogs token recorded. Both are ``sources-unread``, the warning names
    the login step, and the unread tally names Discogs rather than nothing."""
    for name in ("a", "b"):
        place(folder, silence, name)

    def fetch(url: str) -> searchers.Fetched:
        return EMPTY_BEATPORT if url.startswith(searchers.BEATPORT_SEARCH) else searchers.Fetched(
            note=f"no route for {url}"
        )

    bound(monkeypatch, searchers.catalogue_searcher(TAXONOMY, fetch=fetch, sleep=lambda _s: None))
    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    for report in artifacts.committed(cfg, job.job_id):
        assert report["skipped"] == tag.SOURCES_UNREAD
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["skipped"][tag.NO_HIT] == 0
    assert tagging["discogs_without_token"] == 2
    warnings = {w["code"]: w["message"] for w in resumed["warnings"]}
    assert "crate login discogs-token" in warnings[tag_cli.DISCOGS_NO_TOKEN_FILES]
    unread = warnings[tag_cli.SOURCES_UNREAD]
    assert "discogs not asked for want of a token on 2" in unread
    assert not unread.rstrip().endswith("the sweep:")


# The active taxonomy, parsed once a sweep (U247)


def test_a_sweep_parses_the_active_taxonomy_once_however_many_files_it_tags(
    cfg, folder, silence, monkeypatch
):
    """The worker reads the library's copy for every file and parses it for the first."""
    from cratekit.core import taxonomy
    from tests.test_tagging_engine import _jpeg, plant

    text = unique(taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME))
    active = config.state_path("taxonomy_active", cfg)
    active.parent.mkdir(parents=True, exist_ok=True)
    active.write_text(text, encoding="utf-8")
    place(folder, silence, "a")
    place(folder, silence, "b")
    plant(place(folder, silence, "c", genre=SPECIFIC), _jpeg(320, 200), dims=(320, 200, 24))
    bound(
        monkeypatch,
        answering({"a": hit("deep house", SPECIFIC), "b": hit("deep house", SPECIFIC)}),
    )
    parses = counted(monkeypatch)

    code, queued = drive(["tag", "folder", "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = tag_job()
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed

    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert len(item_states(job.job_id)) == 3
    assert tags.read_genre_from_file(folder / "a.flac") == SPECIFIC
    assert parses.of(text) == 1, f"three files parsed the active copy {parses.of(text)} times"


def test_a_retag_parses_the_active_taxonomy_once_however_many_files_it_corrects(
    repair_on, folder, silence, monkeypatch
):
    """The third per item handler the speed survey named, counted the same way."""
    from cratekit.core import taxonomy

    text = unique(taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME))
    active = config.state_path("taxonomy_active", repair_on)
    active.parent.mkdir(parents=True, exist_ok=True)
    active.write_text(text, encoding="utf-8")
    for name in ("a", "b", "c"):
        coarse(folder, silence, name)
    bound(monkeypatch, answering({name: hit("deep house", SPECIFIC) for name in "abc"}))
    parses = counted(monkeypatch)

    _gate_run, job_id = approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)
    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert item_states(job_id) == {
        str(folder / f"{name}.flac"): jobs.ItemState.DONE for name in "abc"
    }
    assert all(tags.read_genre_from_file(folder / f"{name}.flac") == SPECIFIC for name in "abc")
    assert parses.of(text) == 1, f"three files parsed the active copy {parses.of(text)} times"
