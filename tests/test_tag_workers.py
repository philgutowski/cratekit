"""U3 and U4: the tagging verbs' shell and artifact helper, and tag folder end to end.

Each property of the adoption original is asserted against the copy, three by
parsing the source; the second half drives ``crate tag folder`` through the
real dispatcher. D1 applies.
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
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
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
    """The dispatcher context cut to ``run_job`` (KTD23); ``settle`` moves rows as a driver does."""

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


def advance(ctx, store, job, nothing_to_run="report a sweep it never ran"):
    """``shell.advance`` as the tagging verbs call it."""
    return shell.advance(
        ctx, store, job, origin=("tagging", "cli"), nothing_to_run=nothing_to_run
    )


# The reported payload


def test_an_extra_mapping_rides_under_progress_and_never_beside_it(store, cfg):
    """``job_state/1`` forbids extra top level keys, so the four are asserted by equality (U51)."""
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
    """R-234: ``job_id`` is a required string, so the value is asserted, not its truthiness."""
    payload = shell.no_op("no-op")

    assert payload["job_id"] == ""
    assert payload["job_id"] is not None


def test_the_honest_zero_validates_against_the_job_state_surface():
    """Validated against the declared schema, the check ``tests/cli_drive.py`` runs."""
    for state in ("no-op", "declined"):
        assert output.payload_problems("job_state", shell.no_op(state)) == [], state


# The resume


def test_a_job_with_no_items_is_refused_rather_than_driven(store, cfg):
    """A job with no items reads SUCCEEDED, so it is refused as ``internal-error``, never driven."""
    ctx = Ctx(store)
    job = a_job(store, cfg)

    with pytest.raises(CratekitError) as caught:
        advance(ctx, store, job, "report a tagging sweep over a folder it never walked")

    cause = caught.value.cause
    assert cause.reason == "internal-error"
    assert "never walked" in cause.message
    assert str(cause.remediation.remedy) == "report-defect"
    assert ctx.driven == []


def test_a_cancelled_job_raises_rather_than_reporting_through_a_normal_envelope(store, cfg):
    """R-225: a run stopped by a signal lands CANCELLED, which ``FAILED`` alone would miss."""
    ctx = Ctx(store)
    job = a_job(store, cfg, "one.flac")
    jobs.cancel(store, job.job_id)

    with pytest.raises(CratekitError) as caught:
        advance(ctx, store, jobs.get(store, job.job_id))

    assert caught.value.cause.reason == "cancelled"
    assert ctx.driven == []


def test_a_succeeded_job_comes_back_without_being_driven_again(store, cfg):
    """A terminal state is a recorded answer, so a resume reports rather than reruns."""
    ctx = Ctx(store)
    job = a_job(store, cfg, "one.flac")
    jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)

    settled, warnings = advance(ctx, store, jobs.get(store, job.job_id))

    assert settled.state is jobs.JobState.SUCCEEDED
    assert warnings == ()
    assert ctx.driven == []


def test_an_open_job_is_driven_and_comes_back_as_it_stands_afterwards(store, cfg):
    """The job is RE-READ after the drive, and the driver's warnings travel with it."""
    ctx = Ctx(store, warnings=({"code": "one-skipped", "message": "a file moved"},))
    job = a_job(store, cfg, "one.flac", "two.flac")

    settled, warnings = advance(ctx, store, job)

    assert ctx.driven == [job.job_id]
    assert settled.state is jobs.JobState.SUCCEEDED
    assert warnings == ({"code": "one-skipped", "message": "a file moved"},)
    assert shell.reported(store, settled)["progress"]["settled"] == 2


# The name that is load bearing outside this module


def test_the_counter_this_guard_borrows_sees_a_call_it_is_meant_to_see():
    """P7: the borrowed ``_drive_calls`` counter is shown to fire."""
    assert _drive_calls(ast.parse("jobs.drive(store, job)\ndrive(store, job)\n")) == 2


def test_nothing_in_the_tagging_shell_is_named_drive():
    """``tests/test_handlers.py`` counts callees named ``drive``, so none is defined here."""
    tree = ast.parse(SHELL_SOURCE.read_text(encoding="utf-8"))

    assert _drive_calls(tree) == 0
    functions = (ast.FunctionDef, ast.AsyncFunctionDef)
    defined = [node.name for node in ast.walk(tree) if isinstance(node, functions)]
    assert "drive" not in defined, defined


# Where one item's report is staged, and where it lands


def test_an_item_identifier_holding_a_separator_cannot_escape_the_directory(store, cfg):
    """An item identifier holds separators, so the report is named by its ordinal."""
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
    """A dead attempt's half written report would be committed as this attempt's."""
    first = artifacts.staged_path(cfg, "job-one", 3)
    first.write_text("half a report", encoding="utf-8")
    stray = first.parent / "left-behind.json"
    stray.write_text("{}", encoding="utf-8")

    second = artifacts.staged_path(cfg, "job-one", 3)

    assert second == first
    assert not second.exists()
    assert not stray.exists()


def test_staging_sits_on_the_same_filesystem_as_the_place_it_is_committed_to(cfg):
    """``commit_artifact`` is an ``os.replace``, atomic only within one filesystem."""
    final = artifacts.final_path(cfg, "job-one", 0)
    staged = artifacts.staged_path(cfg, "job-one", 0)
    root = jobs.store_dir(cfg)

    assert final.parents[2] == root
    assert staged.parents[3] == root
    assert os.stat(final.parent).st_dev == os.stat(staged.parent).st_dev


def test_reports_past_the_four_digit_name_come_back_in_item_order(cfg):
    """The ordinal sorts as a number: as text ``"10000"`` sorts before ``"9999"``."""
    for ordinal in (10000, 9999):
        artifacts.write(artifacts.final_path(cfg, "job-one", ordinal), {"ordinal": ordinal})

    assert [report["ordinal"] for report in artifacts.committed(cfg, "job-one")] == [9999, 10000]


def test_a_report_that_cannot_be_parsed_is_skipped_rather_than_raised_on(cfg):
    """A summary is a display, so one unreadable file must not hide the rest."""
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
    """``adopt-artifacts`` would file tagging reports where adoption reads its own."""
    assert artifacts.ARTIFACTS_DIRNAME == "tag-artifacts"
    assert artifacts.STAGING_DIRNAME == "tag-staging"
    assert artifacts.final_path(cfg, "job-one", 0).parents[1].name == "tag-artifacts"
    assert artifacts.staged_path(cfg, "job-one", 0).parents[2].name == "tag-staging"


def test_the_artifact_helper_never_resolves_the_queue_root_for_itself():
    """KTD9: ``jobs.store_dir()`` bare loads the current configuration, which a resume must not."""
    tree = ast.parse(ARTIFACTS_SOURCE.read_text(encoding="utf-8"))
    bare: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        callee = node.func
        named = callee.attr if isinstance(callee, ast.Attribute) else (
            callee.id if isinstance(callee, ast.Name) else ""
        )
        bare_call = not (node.args or node.keywords)
        if named in {"store_dir", "queue_path", "load", "load_from_path"} and bare_call:
            bare.append(named)
    assert not bare, (
        "the queue root must come from the configuration the job froze, passed "
        f"in as a parameter; these calls resolve it for themselves: {bare}"
    )


# U4: ``crate tag folder`` walking a real folder, end to end, always through the
# verb, so an unbound handler key would fail.


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One real FLAC container, synthesized once and copied per file: the write is read back."""
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def folder(tmp_path) -> Path:
    """A download folder outside the library, where tagging happens."""
    out = tmp_path / "downloads"
    out.mkdir()
    return out


def bound(monkeypatch, searcher):
    """Bind ``searcher`` where the worker looks one up at call time (KTD11, R23)."""
    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared=None, refusals=None: searcher)
    # The general catalogue too, to a lookup failing on any request (R-796);
    # a test wanting an answer calls :func:`general` after this.
    general(monkeypatch, None)
    return searcher


def shipped_over(monkeypatch, fetch, *, token) -> None:
    """Bind the shipped searcher per call over ``fetch``, Discogs holding ``token``, as bound."""
    asker = searchers.discogs_asker(token=token, fetch=fetch, sleep=lambda _s: None)
    monkeypatch.setattr(
        searchers,
        "for_taxonomy",
        lambda declared=None, refusals=None: searchers.catalogue_searcher(
            TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker, refusals=refusals
        ),
    )
    general(monkeypatch, None)


def general(monkeypatch, track, album=None, seen: list[str] | None = None):
    """Bind the general catalogue's lookup, which ``published.for_taxonomy`` reads at call time."""
    lookup = published.genre_lookup(fetch=deezer_fetch(track, album, seen), sleep=lambda _s: None)
    monkeypatch.setattr(published, "for_lookup", lambda: lookup)
    return lookup


def raising_on(searcher, title: str):
    """``searcher``, except one title raises ``catalogue-unreachable``, retryable (R-390)."""

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


def hit(source_genre: str, genre: str | None = None, *, off_taxonomy: bool = False, **more):
    """One answer, naming what it answered even declining (R24); ``off_taxonomy`` with a genre."""
    return SearchHit(
        genre=genre,
        source=searchers.BEATPORT,
        source_genre=source_genre,
        off_taxonomy=off_taxonomy,
        **more,
    )


def deep(names):
    """A searcher answering each title named with ``deep house``, read as ``SPECIFIC``."""
    return answering({name: hit("deep house", SPECIFIC) for name in names})


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
    """The command line the job driver would spawn, through the real ``argv_for``."""
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def swept(folder: Path):
    """Queue a sweep over ``folder``, then drive it as the job driver would."""
    queue(folder)
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


def places(folder: Path, silence: Path, names) -> None:
    """One untagged file per name."""
    for name in names:
        place(folder, silence, name)


def queue(folder: Path):
    """``crate tag folder --queue-only`` over ``folder``."""
    return drive(["tag", "folder", "--queue-only", str(folder)])


def warning_codes(envelope: dict) -> list[str]:
    """Every warning code on one envelope, in the order the verb attached them."""
    return [warning["code"] for warning in envelope["warnings"]]


def warned(envelope: dict) -> dict[str, str]:
    """Each warning's message by its code."""
    return {warning["code"]: warning["message"] for warning in envelope["warnings"]}


def warned_all(envelope: dict, code: str) -> list[str]:
    """Every message warned under ``code``, in order."""
    return [warning["message"] for warning in envelope["warnings"] if warning["code"] == code]


def retag_reports(cfg: config.Config, job_id: str) -> dict:
    """This job's committed reports, keyed by the item they describe."""
    return {report["item"]: report for report in artifacts.committed(cfg, job_id)}


# The binding


@pytest.mark.parametrize("verb", ["tag.folder", "tag.retag"])
def test_the_tagging_key_resolves_to_a_worker(verb):
    """R-203: only an assertion naming this key tells unbound from bound."""
    key = registry.entry(verb).handler_key

    assert handlers.is_known(key), f"{key} still has no worker"
    assert handlers.unbound_reason(key) is None
    assert callable(handlers.resolve(key))


# The happy path


def test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third(
    cfg, folder, silence, monkeypatch
):
    """Read back off disk; the third holds fill if empty and a picture, so no art search (U85)."""
    from tests.test_tagging_engine import _jpeg, plant

    places(folder, silence, "ab")
    plant(place(folder, silence, "c", genre=SPECIFIC), _jpeg(320, 200), dims=(320, 200, 24))
    searcher = bound(monkeypatch, deep("ab"))

    code, queued = queue(folder)
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

    reports = retag_reports(cfg, job.job_id)
    assert len(reports) == 3, reports
    assert reports["a.flac"]["genre_written"] == SPECIFIC
    assert reports["c.flac"]["genre_written"] is None
    assert reports["c.flac"]["skipped"] == tag.HAS_GENRE


def test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged(
    cfg, folder, silence, monkeypatch
):
    """``sub/deep.flac`` is the common case, joined back onto the payload's folder."""
    place(folder / "sub", silence, "deep")
    bound(monkeypatch, deep(["deep"]))

    queue(folder)
    job = tag_job()
    assert list(item_states(job.job_id)) == [str(Path("sub") / "deep.flac")]

    code, resumed = drive(resume_argv(job.job_id))

    assert code == int(ExitCode.OK), resumed
    assert tags.read_genre_from_file(folder / "sub" / "deep.flac") == SPECIFIC


def test_the_skip_reason_reaches_the_report_and_not_only_the_artifact(
    cfg, folder, silence, monkeypatch
):
    """R16: the counts ride under ``progress``, the one open place in ``job_state/1``."""
    place(folder, silence, "a")
    place(folder, silence, "b", genre=SPECIFIC)
    bound(monkeypatch, answering({}))

    job, _code, resumed = swept(folder)

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["skipped"][tag.HAS_GENRE] == 1
    assert tagging["skipped"][tag.NO_HIT] == 1
    assert tagging["tagged"] == 0
    assert set(tagging["skipped"]) == {
        tag.HAS_GENRE, tag.NO_HIT, tag.UNMAPPED_GENRE, tag.SOURCES_UNREAD, tag.NO_ISRC
    }, (
        "a summary listing only the reasons it saw cannot tell 'none of those "
        "here' from 'this build does not count them'"
    )


def test_the_report_names_each_unresolved_source_genre_with_its_count(
    cfg, folder, silence, monkeypatch
):
    """R24: each string names an alias the taxonomy lacks, as the resolver declines it."""
    places(folder, silence, "abc")
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
        "Techno", "Techno", "Electronic"
    ]


def test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns(
    cfg, folder, silence, monkeypatch
):
    """R-650: an off taxonomy word written to disk is reported, apart from a decline."""
    places(folder, silence, "abcde")
    gqom = hit("gqom", "gqom", off_taxonomy=True)
    bubblegum = hit("bubblegum bass", "bubblegum bass", off_taxonomy=True)
    hits = {"a": gqom, "b": gqom, "c": hit("Deep House", "Deep House"), "d": hit("Techno")}
    bound(monkeypatch, answering({**hits, "e": bubblegum}))

    job, _code, resumed = swept(folder)

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["off_taxonomy"] == {"gqom": 2, "bubblegum bass": 1}
    assert tagging["unresolved"] == {"Techno": 1}
    assert tagging["tagged"] == 4, "they were written, so they are tagged"
    assert [report["off_taxonomy"] for report in artifacts.committed(cfg, job.job_id)] == [
        True, True, False, False, True
    ]

    warnings = warned(resumed)
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
    """The shipped searcher over a fetch answering per title and source (R-791)."""
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
    is_fetched = isinstance(answer, searchers.Fetched)
    return answer if is_fetched else searchers.Fetched(text=answer, status=200)


def test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit(
    cfg, folder, silence, monkeypatch
):
    """R-791: two catalogues never read are said on every surface, never as ``no-hit``."""
    places(folder, silence, "ab")
    bound(monkeypatch, _catalogues({"a": REFUSED_FALLBACKS, "b": REFUSED_FALLBACKS}))

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

    warnings = warned(resumed)
    assert tag_cli.SOURCES_UNREAD == "tag-folder-sources-unread"
    assert tag_cli.SOURCE_BLOCKED == "tag-folder-source-blocked"
    unread = warnings[tag_cli.SOURCES_UNREAD]
    assert "2 files were left untagged" in unread
    assert "Across the sweep: traxsource refused this client on 2; bandcamp refused this client on 2" in unread
    assert "parse break" not in unread
    blocked = warned_all(resumed, tag_cli.SOURCE_BLOCKED)
    assert len(blocked) == 2
    assert blocked[0].startswith("traxsource refused every one of the 2 searches")
    assert blocked[1].startswith("bandcamp refused every one of the 2 searches")


#: Beatport's answer at sitting 97, as the shipped fetch hands it on (U281).
BEATPORT_CHALLENGE = searchers.Fetched(note="Cloudflare challenge, HTTP 403", status=403)


def _refusing_sweep(monkeypatch, seen: list[str]):
    """Bind the shipped searcher per call over a refusing Beatport; Discogs answers empty."""
    from tests.test_discogs_searcher import SENT, results

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            return BEATPORT_CHALLENGE
        if url.startswith(searchers.DISCOGS_SEARCH):
            return searchers.Fetched(text=results(), status=200)
        return searchers.Fetched(note=f"no route for {url}")

    shipped_over(monkeypatch, fetch, token=SENT)


def _beatport_asked(seen: list[str]) -> int:
    return sum(url.startswith(searchers.BEATPORT_SEARCH) for url in seen)


def _by_somebody(folder: Path, name: str, genre: str = SPECIFIC) -> searchers.Fetched:
    """Credit ``name`` to Somebody, and a Beatport page listing that track in ``genre``."""
    assert tags.write_tags(folder / f"{name}.flac", {"artist": "Somebody"})
    page = beatport_page([beatport_track("Somebody", name, genre)])
    return searchers.Fetched(text=page, status=200)


def _beatport_or(seen: list[str], beatport: searchers.Fetched, rest: searchers.Fetched):
    """A fetch recording each URL, Beatport answering ``beatport`` and every other ``rest``."""

    def fetch(url: str) -> searchers.Fetched:
        seen.append(url)
        return beatport if url.startswith(searchers.BEATPORT_SEARCH) else rest

    return fetch


def test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused(
    cfg, folder, silence, monkeypatch
):
    """U281: three of five reach Beatport, the rest recorded unsent, every file askable."""
    places(folder, silence, "abcde")
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
    assert [note.startswith(searchers.NOT_SENT) for note in notes] == [False] * 3 + [True] * 2
    assert tags.read_genre_from_file(folder / "e.flac") is None

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["skipped"][tag.NO_HIT] == 0
    assert tagging["answers"][searchers.BEATPORT]["blocked"] == 5
    assert tagging["answers"][searchers.BEATPORT]["unreachable"] == 0
    assert tagging["challenged"][searchers.BEATPORT] == 5
    assert tagging["not_sent"][searchers.BEATPORT] == 2
    assert tagging["not_sent"][searchers.DISCOGS] == 0, "zero filled"

    warnings = warned(resumed)
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
    """The count is the run's: a second sweep starts from Beatport's first three lookups."""
    places(folder, silence, "abcd")
    seen: list[str] = []
    _refusing_sweep(monkeypatch, seen)

    first, code, _ = swept(folder)
    assert code == int(ExitCode.OK)
    assert _beatport_asked(seen) == 3

    again = folder.parent / "again"
    places(again, silence, "fghi")
    queue(again)
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
    """The count is the run's, not the job's: a retried job driven again asks afresh."""
    from tests.test_discogs_searcher import results

    places(folder, silence, "abcde")
    seen: list[str] = []
    fetch = _beatport_or(seen, BEATPORT_CHALLENGE, searchers.Fetched(text=results(), status=200))
    shipped_over(monkeypatch, fetch, token=None)

    job, _code, _ = swept(folder)
    assert _beatport_asked(seen) == 3
    assert set(item_causes(job.job_id).values()) == {searchers.UNREACHABLE_REASON}

    with jobs.open_store() as store:
        jobs.retry(store, job.job_id)
    drive(resume_argv(job.job_id))

    assert _beatport_asked(seen) == 6


def test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent(
    cfg, folder, silence, monkeypatch
):
    """Discogs sends nothing after its first refusal, and the warning counts one search (U281)."""
    from tests.test_discogs_searcher import SENT

    places(folder, silence, "abcd")
    seen: list[str] = []
    fetch = _beatport_or(seen, EMPTY_BEATPORT, searchers.Fetched(note="HTTP 403", status=403))
    shipped_over(monkeypatch, fetch, token=SENT)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    assert sum(url.startswith(searchers.DISCOGS_SEARCH) for url in seen) == 1
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["answers"][searchers.DISCOGS]["blocked"] == 4
    assert tagging["not_sent"][searchers.DISCOGS] == 3
    warnings = warned(resumed)
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
    challenged = {"challenged": {searchers.BEATPORT: 4}}
    whole = tag_cli._unread_phrase(challenged, searchers.BEATPORT, "blocked", 4)
    plain = tag_cli._unread_phrase({}, searchers.BEATPORT, "blocked", 4)

    assert said == (
        "beatport refused this client on 4 (Cloudflare challenge on 2), "
        "1 of them not asked once it had refused this client"
    )
    assert whole == "beatport refused this client (Cloudflare challenge) on 4"
    assert plain == "beatport refused this client on 4"
    down = tag_cli._unread_phrase({}, searchers.BEATPORT, "unreachable", 4)
    assert down == "beatport unreachable on 4"


def test_an_outage_keeps_its_own_word_in_the_sweeps_warning(cfg, folder, silence, monkeypatch):
    """A Beatport that is down is unreachable, said so, and asked on every file."""
    from tests.test_discogs_searcher import SENT, results

    places(folder, silence, "abcd")
    seen: list[str] = []
    down = searchers.Fetched(note="HTTP 503", status=503)
    fetch = _beatport_or(seen, down, searchers.Fetched(text=results(), status=200))
    shipped_over(monkeypatch, fetch, token=SENT)

    _job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    assert _beatport_asked(seen) == 4
    warnings = warned(resumed)
    assert "Across the sweep: beatport unreachable on 4" in warnings[tag_cli.SOURCES_UNREAD]
    assert "refused" not in warnings[tag_cli.SOURCES_UNREAD]
    assert tag_cli.SOURCE_BLOCKED not in warnings


def test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning(
    cfg, folder, silence, monkeypatch
):
    """Bandcamp blocked on every file it was sent is named, though one file never asked it."""
    places(folder, silence, "ab")
    matched = _by_somebody(folder, "a")
    challenged = {**ALL_MISSED, searchers.BANDCAMP: BANDCAMP_CHALLENGE}
    bound(monkeypatch, _catalogues({"a": {searchers.BEATPORT: matched}, "b": challenged}))

    job, _code, resumed = swept(folder)

    reports = retag_reports(cfg, job.job_id)
    assert reports["a.flac"]["genre_written"] == SPECIFIC
    assert [said["answer"] for said in reports["a.flac"]["answers"]] == [
        "matched", searchers.NOT_ASKED, searchers.NOT_ASKED, searchers.NOT_ASKED
    ]
    assert reports["b.flac"]["skipped"] == tag.SOURCES_UNREAD

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["answers"][searchers.BANDCAMP][searchers.NOT_ASKED] == 1
    blocked = warned_all(resumed, tag_cli.SOURCE_BLOCKED)
    assert len(blocked) == 1
    assert "bandcamp refused every one of the 1 searches" in blocked[0]


def test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said(
    cfg, folder, silence, monkeypatch
):
    """A parse break beside a miss leaves the file undecided, and the warning says the defect."""
    place(folder, silence, "a")
    broken = searchers.Fetched(
        text='<div data-trid="1" class="trk-row"><span>moved</span></div>', status=200
    )
    bound(monkeypatch, _catalogues({"a": {**ALL_MISSED, searchers.TRAXSOURCE: broken}}))

    job, _code, resumed = swept(folder)

    (report,) = artifacts.committed(cfg, job.job_id)
    assert report["unread"] == {searchers.TRAXSOURCE: "parse-break"}
    warnings = warned(resumed)
    message = warnings[tag_cli.SOURCES_UNREAD]
    assert message.startswith("1 file was left untagged")
    assert "traxsource parse-break on 1" in message
    assert "defect in this software that another run will not move" in message
    assert tag_cli.SOURCE_BLOCKED not in warnings


def test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked(
    cfg, folder, silence, monkeypatch
):
    """A fallback never asked is no refusal (row C5 of ``r791-b``)."""
    place(folder, silence, "a")
    bound(monkeypatch, _catalogues({"a": {searchers.BEATPORT: _by_somebody(folder, "a")}}))

    job, _code, resumed = swept(folder)

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["tagged"] == 1
    assert tagging["answers"][searchers.BANDCAMP][searchers.NOT_ASKED] == 1
    codes = warning_codes(resumed)
    assert tag_cli.SOURCE_BLOCKED not in codes
    assert tag_cli.SOURCES_UNREAD not in codes


def test_four_real_misses_are_no_hit_and_carry_no_unread_warning(cfg, folder, silence, monkeypatch):
    """Every catalogue asked and none knows the track: the absence ``no-hit`` means, unqualified."""
    assert tags.write_tags(place(folder, silence, "a"), {"isrc": ISRC})
    bound(monkeypatch, _catalogues({"a": ALL_MISSED}))
    general(monkeypatch, DEEZER_UNKNOWN)

    job, _code, resumed = swept(folder)

    (report,) = artifacts.committed(cfg, job.job_id)
    assert report["skipped"] == tag.NO_HIT
    assert [said["answer"] for said in report["answers"]] == ["miss"] * 4
    assert report["unread"] == {}
    codes = warning_codes(resumed)
    assert tag_cli.SOURCES_UNREAD not in codes
    assert tag_cli.SOURCE_BLOCKED not in codes
    assert tag_cli.PUBLISHED_UNREAD not in codes
    assert tag_cli.NO_ISRC_FILES not in codes


# R-796: the general catalogue, through the verb


def test_a_published_genre_reaches_the_file_the_artifact_and_the_summary(
    cfg, folder, silence, monkeypatch
):
    """AE1: Beatport misses, both fallbacks refuse, and the general catalogue knows the album."""
    assert tags.write_tags(place(folder, silence, "a"), {"isrc": ISRC})
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
        (searchers.BEATPORT, "miss"), (searchers.TRAXSOURCE, "blocked"),
        (searchers.BANDCAMP, "blocked"), (published.SOURCE, "matched"),
    ]
    assert report["answers"][-1]["source_genre"] == "Rock"
    assert len(seen) == 2

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["tagged"] == 1
    shops = (searchers.BEATPORT, searchers.DISCOGS, searchers.TRAXSOURCE, searchers.BANDCAMP)
    assert tagging["tagged_by"] == {
        **dict.fromkeys(shops, 0), published.SOURCE: 1, tag.LABEL_GENRE: 0
    }
    assert tagging["answers"][published.SOURCE]["matched"] == 1
    assert set(tagging["answers"][published.SOURCE]) == set(published.ANSWERS), "zero filled"
    assert tag.NO_ISRC not in tagging["answers"][searchers.BEATPORT], (
        "a record shop is never asked by ISRC, so it carries no count for one"
    )
    codes = warning_codes(resumed)
    assert tag_cli.OFF_TAXONOMY not in codes
    assert tag_cli.PUBLISHED_UNREAD not in codes
    assert tag_cli.NO_ISRC_FILES not in codes


def test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary(
    cfg, folder, silence, monkeypatch
):
    """A 429 on every file: the summary names the catalogue and count once."""
    places(folder, silence, "abc")
    for name in ("a", "b"):
        assert tags.write_tags(folder / f"{name}.flac", {"isrc": ISRC})
    matched = {searchers.BEATPORT: _by_somebody(folder, "c")}
    bound(monkeypatch, _catalogues({"a": ALL_MISSED, "b": ALL_MISSED, "c": matched}))
    asked: list[str] = []
    general(monkeypatch, RATE_LIMITED, seen=asked)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    reports = retag_reports(cfg, job.job_id)
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
    named = warned_all(resumed, tag_cli.PUBLISHED_UNREAD)
    assert len(named) == 1
    assert named[0].startswith(f"{published.SOURCE}, the general catalogue asked by ISRC")
    assert "any of the 2 files it was asked about (blocked on 2)" in named[0]
    assert "no file in this run got a published genre from it" in named[0]
    assert "does not try to get past" in named[0]
    assert "parse break" not in named[0]
    blocked = warned_all(resumed, tag_cli.SOURCE_BLOCKED)
    assert blocked == [], "the general catalogue has its own warning and is named once"
    unread = warned_all(resumed, tag_cli.SOURCES_UNREAD)
    assert len(unread) == 1 and f"{published.SOURCE} refused this client on 2" in unread[0]


def test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many(
    cfg, folder, silence, monkeypatch
):
    """A miss on one file and an outage on the other: the second is still said."""
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
    (named,) = warned_all(resumed, tag_cli.PUBLISHED_UNREAD)
    assert "could not be read on 1 of the 2 files it was asked about (unreachable on 1)" in named
    assert "those files got no published genre from it" in named
    assert "no file in this run" not in named


def test_a_block_on_a_file_a_record_shop_declined_is_still_said(cfg, folder, silence, monkeypatch):
    """A block is a sentence even when no file in the run is ``sources-unread``."""
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
    codes = warning_codes(resumed)
    assert tag_cli.SOURCES_UNREAD not in codes
    assert codes.count(tag_cli.PUBLISHED_UNREAD) == 1


def test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it(
    cfg, folder, silence, monkeypatch
):
    assert tags.write_tags(place(folder, silence, "a"), {"isrc": ISRC})
    bound(monkeypatch, _catalogues({"a": ALL_MISSED}))
    general(monkeypatch, '["a JSON answer in a shape this reader does not know"]')

    job, _code, resumed = swept(folder)

    (named,) = warned_all(resumed, tag_cli.PUBLISHED_UNREAD)
    assert "(parse-break on 1)" in named
    assert "A parse break is a defect in this software" in named
    (unread,) = warned_all(resumed, tag_cli.SOURCES_UNREAD)
    assert f"{published.SOURCE} parse-break on 1" in unread
    assert "A parse break is a defect" not in unread, (
        "the general catalogue's parse break is said once, by its own warning"
    )


def test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason(
    cfg, folder, silence, monkeypatch
):
    """AE4: both files lack an ISRC under different skip reasons, and the warning counts both."""
    places(folder, silence, "ab")
    bound(monkeypatch, _catalogues({"a": REFUSED_FALLBACKS, "b": ALL_MISSED}))

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    reports = retag_reports(cfg, job.job_id)
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
    (bare,) = warned_all(resumed, tag_cli.NO_ISRC_FILES)
    assert bare.startswith("2 files were not asked about at deezer")
    assert "not reported as tracks no catalogue carries" in bare
    codes = warning_codes(resumed)
    assert tag_cli.PUBLISHED_UNREAD not in codes, "a catalogue never asked was not unread"


def test_a_published_word_with_no_folder_is_listed_as_unresolved(cfg, folder, silence, monkeypatch):
    """R3: the catalogue's own word is the one to alias, so the summary names it."""
    assert tags.write_tags(place(folder, silence, "a"), {"isrc": ISRC})
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
    """The quiet case: a warning on a clean run soon goes unread."""
    places(folder, silence, "ab")
    bound(monkeypatch, answering({"a": hit("Deep House", "Deep House"), "b": hit("Techno")}))

    job, _code, resumed = swept(folder)

    assert resumed["data"]["progress"]["tagging"]["off_taxonomy"] == {}
    assert tag_cli.OFF_TAXONOMY not in warning_codes(resumed)


def test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status(
    cfg, folder, silence, monkeypatch
):
    """U84: the repair runs on every item, already tagged ones too, and every status is counted."""
    from tests.test_tagging_engine import _jpeg, blocks, plant

    for name, genre in (("a", None), ("b", SPECIFIC), ("c", None)):
        path = place(folder, silence, name, genre=genre)
        if name != "c":
            plant(path, _jpeg(320, 200))
    bound(monkeypatch, answering({}))

    job, _code, resumed = swept(folder)

    reports = artifacts.committed(cfg, job.job_id)
    assert [report["art_repair"] for report in reports] == [
        art.REPAIR_FIXED, art.REPAIR_FIXED, art.REPAIR_NONE
    ]
    assert reports[0]["art_repair_detail"] == "1 of 1 pictures re-encoded"
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["art_repair"] == {
        art.REPAIR_FIXED: 2, art.REPAIR_OK: 0, art.REPAIR_NONE: 1, art.REPAIR_ERROR: 0,
        art.REPAIR_UNCHECKED: 0,
    }
    assert tagging["skipped"][tag.HAS_GENRE] == 1
    for name in ("a", "b"):
        (block,) = blocks(folder / f"{name}.flac")
        assert (block.width, block.height, block.depth) == (320, 200, 24)


def test_a_report_from_before_the_repair_is_counted_under_no_status(cfg, store):
    """A report with no status says nothing about the art."""
    job = a_job(store, cfg, "old.flac")
    (item,) = jobs.items(store, job.job_id)
    old = {"item": "old.flac", "genre_written": None, "skipped": tag.NO_HIT}
    produced = artifacts.produced(cfg, job, item, old)
    produced.final.parent.mkdir(parents=True, exist_ok=True)
    produced.staged.replace(produced.final)

    summary = tag_cli._summary(cfg, job.job_id)

    assert summary["art_repair"] == dict.fromkeys(art.REPAIR_STATUSES, 0)
    assert summary["art_fetch"] == dict.fromkeys(tag.ART_FETCH_STATUSES, 0)
    assert summary["skipped"][tag.NO_HIT] == 1


def test_new_art_reaches_the_file_the_artifact_and_the_summary(cfg, folder, silence, monkeypatch):
    """U85: two files get art, one already has it, and a 404 keeps its genre and says so."""
    from tests.test_tagging_engine import _jpeg, blocks, plant

    place(folder, silence, "a")
    place(folder, silence, "b", genre=SPECIFIC)
    plant(place(folder, silence, "c", genre=SPECIFIC), _jpeg(320, 200), dims=(320, 200, 24))
    place(folder, silence, "d")

    art_url = "https://example.test/{}.jpg".format
    hits = {name: hit("deep house", SPECIFIC, art_url=art_url(name)) for name in "abcd"}
    searcher = bound(monkeypatch, answering(hits))
    fetched: list[str] = []

    def fetch_image(url: str) -> bytes | None:
        fetched.append(url)
        return None if url.endswith("/d.jpg") else _jpeg(1000, 1000)

    monkeypatch.setattr(searchers, "for_images", lambda: fetch_image)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed

    assert [asked for _artist, asked in searcher.asked] == ["a", "b", "d"]
    assert fetched == [f"https://example.test/{name}.jpg" for name in "abd"]
    reports = retag_reports(cfg, job.job_id)
    assert {name: reports[f"{name}.flac"]["art_fetch"] for name in "abcd"} == {
        "a": tag.ART_EMBEDDED, "b": tag.ART_EMBEDDED, "c": tag.ART_PRESENT,
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
        tag.ART_EMBEDDED: 2, tag.ART_PRESENT: 1, tag.ART_UNAVAILABLE: 1, tag.ART_ERROR: 0,
        tag.ART_UNCHECKED: 0,
    }


def test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first(
    cfg, folder, silence, monkeypatch
):
    """U282: Discogs decides both genres and Beatport is asked only for the two missing covers."""
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
    releases = {7: release(7, styles=("Deep House",))}
    fetch = routed(search=results(7), releases=releases, beatport=beatport_page([row]), seen=seen)
    shipped_over(monkeypatch, fetch, token=SENT)
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

    reports = retag_reports(cfg, job.job_id)
    assert {name: reports[f"{name}.flac"]["art_fetch"] for name in names} == {
        "a": tag.ART_EMBEDDED, "b": tag.ART_PRESENT, "c": tag.ART_EMBEDDED
    }
    assert reports["a.flac"]["source"] == searchers.DISCOGS

    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["tagged_by"][searchers.DISCOGS] == 2
    assert tagging["tagged_by"][searchers.BEATPORT] == 0
    assert tagging["answers"][searchers.DISCOGS]["matched"] == 3
    assert tagging["answers"][searchers.BEATPORT]["matched"] == 2
    assert tagging["answers"][searchers.BEATPORT][searchers.NOT_ASKED] == 1


def test_the_sweeps_unread_warning_names_discogs_first(cfg, folder, silence, monkeypatch):
    """U282: the warning names Discogs' outage before Beatport's refusal."""
    from tests.test_discogs_searcher import SENT, results

    places(folder, silence, "ab")
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

    shipped_over(monkeypatch, fetch, token=SENT)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed
    reports = retag_reports(cfg, job.job_id)
    assert reports["a.flac"]["unread"] == {searchers.DISCOGS: "unreachable"}
    assert reports["b.flac"]["unread"] == {searchers.BEATPORT: "blocked"}
    unread = warned(resumed)[tag_cli.SOURCES_UNREAD]
    across = unread.split("Across the sweep: ", 1)[1]
    assert across.index(searchers.DISCOGS) < across.index(searchers.BEATPORT), across


def test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file(
    cfg, folder, silence, monkeypatch
):
    """U282: a 401 from Discogs is warned about though Beatport tags all three."""
    from tests.test_catalogue_searcher import ARTIST, BUCKET_GENRE, TITLE
    from tests.test_discogs_searcher import SENT, routed

    for name in ("a", "b", "c"):
        path = place(folder, silence, name)
        assert tags.write_tags(path, {"artist": ARTIST, "title": TITLE})
    seen: list[str] = []
    refused = searchers.Fetched(note="HTTP 401", status=401)
    page = beatport_page([beatport_track(ARTIST, TITLE, BUCKET_GENRE)])
    fetch = routed(search=refused, beatport=page, seen=seen)
    shipped_over(monkeypatch, fetch, token=SENT)

    job, code, resumed = swept(folder)
    assert code == int(ExitCode.OK), resumed
    assert sum(url.startswith(searchers.DISCOGS_SEARCH) for url in seen) == 1
    tagging = resumed["data"]["progress"]["tagging"]
    assert tagging["tagged_by"][searchers.BEATPORT] == 3
    assert tagging["discogs_token_refused"] == 3
    assert tagging["discogs_without_token"] == 0
    warnings = warned(resumed)
    assert tag_cli.DISCOGS_NO_TOKEN_FILES not in warnings
    refused = warnings[tag_cli.DISCOGS_TOKEN_REFUSED_FILES]
    assert "refused the recorded token" in refused and "3 file(s)" in refused
    assert "crate login discogs-token" in refused
    assert SENT not in json.dumps(resumed)


def test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep(
    cfg, folder, silence, monkeypatch
):
    """U260: ten files of one album fetch and encode one cover; only HTTP and sleep are faked."""
    from tests.test_album_cover_once import ALBUM, Host
    from tests.test_tagging_engine import _jpeg, blocks

    names = [f"t{index:02d}" for index in range(10)]
    places(folder, silence, names)
    cover = _jpeg(1000, 1000)
    hits = {name: hit("deep house", SPECIFIC, art_url=ALBUM) for name in names}
    bound(monkeypatch, answering(hits))
    host = Host({ALBUM: [cover]})
    slept: list[float] = []
    real_fetch = searchers.default_image_fetch
    shipped = lambda: real_fetch(get=host, sleep=slept.append)
    monkeypatch.setattr(searchers, "default_image_fetch", shipped)
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
    reports = retag_reports(cfg, job.job_id)
    assert {reports[f"{name}.flac"]["art_fetch"] for name in names} == {tag.ART_EMBEDDED}
    for name in names:
        (block,) = blocks(folder / f"{name}.flac")
        assert block.data == expected
        assert (block.width, block.height, block.depth) == (800, 800, 24)


def test_the_counts_are_read_off_the_artifacts_rather_than_accumulated_in_memory(
    cfg, folder, silence, monkeypatch
):
    """The total is read off the committed reports, so it holds across a resume."""
    places(folder, silence, "abc")
    bound(monkeypatch, deep("a"))

    job, _code, resumed = swept(folder)

    tagging = resumed["data"]["progress"]["tagging"]
    counted = tagging["tagged"] + sum(tagging["skipped"].values())
    assert counted == len(artifacts.committed(cfg, job.job_id))
    assert counted == resumed["data"]["progress"]["total"]


# The two zeroes, which are not one zero


def queued_nothing(code: int, envelope: dict, warning: str) -> None:
    """A no-op naming no job, warned ``warning`` alone, with nothing in the queue."""
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert warning_codes(envelope) == [warning]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_folder_holding_no_audio_queues_nothing_and_says_which_zero_it_is(cfg, folder):
    """AE3: a job with no items would read as a clean sweep."""
    (folder / "cover.jpg").write_bytes(b"not audio")

    queued_nothing(*queue(folder), "tag-folder-no-audio")


def test_an_empty_folder_argument_never_sweeps_the_working_directory(
    cfg, folder, silence, monkeypatch
):
    """``Path("")`` is the working directory, so an empty folder is a no-op, with audio present."""
    place(folder, silence, "a")
    monkeypatch.chdir(folder)

    queued_nothing(*drive(["tag", "folder", "--queue-only", ""]), "tag-folder-unnamed")
    assert tags.read_genre_from_file(folder / "a.flac") in (None, "")


def test_tagging_the_download_root_queues_nothing_from_the_acquisition_staging_tree(
    cfg, folder, silence
):
    """R-289: the staging tree under the download root is never swept."""
    staged = folder / acquire_cli.ACQUIRE_STAGING_DIRNAME / "job-1" / "0" / "partial"
    place(staged.parent, silence, staged.name)

    queued_nothing(*queue(folder), "tag-folder-no-audio")


def test_a_real_track_beside_the_staging_tree_is_still_queued(cfg, folder, silence):
    """The other half: skipping staging must not skip the tracks beside it."""
    place(folder, silence, "committed")
    staged = folder / acquire_cli.ACQUIRE_STAGING_DIRNAME / "job-1" / "0" / "partial"
    place(staged.parent, silence, staged.name)

    code, envelope = queue(folder)

    assert code == int(ExitCode.OK), envelope
    assert list(item_states(tag_job().job_id)) == ["committed.flac"]


def test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one(cfg, tmp_path):
    """A missing folder and an empty one ask different next moves."""
    queued_nothing(*queue(tmp_path / "no-such-folder"), "tag-folder-absent")


# The failure part way through, and the resume that follows it


def test_a_searcher_that_raises_part_way_fails_only_its_own_item(cfg, folder, silence, monkeypatch):
    """R19x: an unread catalogue fails its item and the job carries a cause."""
    places(folder, silence, "abc")
    bound(monkeypatch, raising_on(deep("abc"), "b"))

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
    """R19x: counted by searcher calls, since re-asking leaves the same states."""
    places(folder, silence, "abc")
    bound(monkeypatch, raising_on(deep("abc"), "b"))
    job, _code, _ = swept(folder)

    second = bound(monkeypatch, deep("abc"))
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
    """R15: refused under the shared ``source-missing`` (R-251), not an internal error."""
    places(folder, silence, "ab")
    bound(monkeypatch, deep("a"))

    queue(folder)
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
    """The run flag is asserted as a whole token, since a substring would match the run id flag."""
    place(folder, silence, "a")
    bound(monkeypatch, answering({}))

    queue(folder)
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
    """``cfg`` with ``repair`` on, so the slim profile offers ``tag.retag``."""
    built = config.from_dict(valid_data(Path(cfg.library.root), modules={"repair": True}))
    config.save(built)
    config.reset_cache()
    return built


def coarse(folder: Path, silence: Path, name: str) -> Path:
    """One file carrying the declared taxonomy's catch-all."""
    return place(folder, silence, name, CATCH_ALL)


def coarses(folder: Path, silence: Path, names: str) -> None:
    """One catch-all file per name."""
    for name in names:
        coarse(folder, silence, name)


def retag_queued(folder: Path) -> str:
    """The retag over ``folder`` confirmed and queued, by its job's id."""
    return approve_and_queue(["tag", "retag", str(folder)], RETAG_GATE)[1]


def selected(folder: Path) -> list[Path]:
    """What a fresh walk of the folder would take, as it stands right now."""
    return [candidate.path for candidate in retag.select(folder, declared=TAXONOMY).candidates]


def test_the_retag_gate_shows_every_row_the_digest_was_taken_over(repair_on, folder, silence):
    """R-693: ``shown`` holds the folder and each planned file with its genre."""
    del repair_on
    coarses(folder, silence, "ab")
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
    """A resume shows the rows read off the frozen payload, never off a fresh walk."""
    del repair_on
    coarses(folder, silence, "ab")
    job_id = retag_queued(folder)
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
    """KTD8 and AE4: a corrected file leaving the selection must not make every resume stale."""
    coarses(folder, silence, "abc")
    bound(monkeypatch, deep("bc"))

    job_id = retag_queued(folder)
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


# The happy path


def test_three_confirmed_files_go_from_pending_to_done_and_carry_a_specific_genre(
    repair_on, folder, silence, monkeypatch
):
    """Confirm, queue, drive, write and read back; the items are the confirmed rows."""
    coarses(folder, silence, "abc")
    searcher = bound(monkeypatch, deep("abc"))

    job_id = retag_queued(folder)
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
    """R16: the report is read back off disk, zeroes included."""
    coarses(folder, silence, "abc")
    bound(monkeypatch, deep("a"))

    job_id = retag_queued(folder)
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

    warning = "tag-retag-folder-absent" if absent else "tag-retag-nothing-coarse"
    queued_nothing(*answered(["tag", "retag", named], "apply"), warning)


def test_answering_the_confirmation_with_abort_queues_nothing_and_writes_nothing(
    repair_on, folder, silence, monkeypatch
):
    """Abort answers the declared ``job_state`` shape through ``shell.no_op`` (R-234)."""
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
    searcher = bound(monkeypatch, deep("a"))
    job_id = retag_queued(folder)

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
    """R15: refused under the shared ``source-missing`` (R-251), not an internal error."""
    coarses(folder, silence, "ab")
    bound(monkeypatch, deep("a"))
    job_id = retag_queued(folder)

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
    """A catch-all answer goes to the review queue, opened per item on the frozen configuration."""
    path = coarse(folder, silence, "a")
    other = TAXONOMY.fallback.too_coarse_as_source[2]
    bound(monkeypatch, answering({"a": hit("some vendor genre", other)}))
    job_id = retag_queued(folder)

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
    """The verdict is read before the catalogue is asked, seen only as no search."""
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
    """R19x: the unanswered item fails, its neighbours stay done, the job carries a cause."""
    coarses(folder, silence, "abc")
    bound(monkeypatch, raising_on(deep("abc"), "b"))
    job_id = retag_queued(folder)

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
    """R19x: counted by searcher calls, since re-asking leaves the same states."""
    coarses(folder, silence, "abc")
    bound(monkeypatch, raising_on(deep("abc"), "b"))
    job_id = retag_queued(folder)
    drive(resume_argv(job_id))

    second = bound(monkeypatch, deep("abc"))
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
    """R-185 measured: the row keeps the catch-all, and only the artifact can recover it."""
    coarses(folder, silence, "ab")
    bound(monkeypatch, raising_on(answering({"a": hit("deep house", SPECIFIC)}), "b"))
    job_id = retag_queued(folder)

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


def job_cause(job_id: str):
    """The cause the queue recorded, read back from the store."""
    with jobs.open_store() as store:
        return jobs.get(store, job_id).cause


def test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs(
    repair_on, folder, silence, monkeypatch
):
    """R-185: the warning names the row's reload and the folder."""
    coarses(folder, silence, "ab")
    bound(monkeypatch, deep("ab"))
    job_id = retag_queued(folder)

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
    """The zero half, driven through a decline so the resume path is reached."""
    coarses(folder, silence, "ab")
    bound(monkeypatch, answering({}))
    job_id = retag_queued(folder)

    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["progress"]["retag"]["corrected"] == 0, resumed
    assert resumed["data"]["progress"]["retag"]["asked"] == 2, resumed
    assert retag_cli.LIBRARY_ROW_STALE not in warning_codes(resumed), resumed


def test_a_half_corrected_retag_carries_the_reload_on_its_refusal(
    repair_on, folder, silence, monkeypatch
):
    """R-185 and R-225: the reload rides the refusal's steps, the retry remedy first."""
    coarses(folder, silence, "abc")
    bound(monkeypatch, raising_on(deep("abc"), "b"))
    job_id = retag_queued(folder)

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
    """The genre writer answering False for the files named, as for a locked file (R-1103)."""
    real = tags.write_genre

    def writer(path: Path, genre: str) -> bool:
        if path.stem in names:
            return False
        return real(path, genre)

    monkeypatch.setattr(tags, "write_genre", writer)


def test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected(
    repair_on, folder, silence, monkeypatch
):
    """R-1103: the refusing file fails ``tag-retag-unwritten`` and the other two land."""
    coarses(folder, silence, "abc")
    bound(monkeypatch, deep("abc"))
    job_id = retag_queued(folder)
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
    """Nothing was corrected, so the job leaves through ``no-evidence`` and names no reload."""
    coarse(folder, silence, "a")
    bound(monkeypatch, deep("a"))
    job_id = retag_queued(folder)
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
    coarses(folder, silence, "ab")
    bound(monkeypatch, deep("ab"))
    job_id = retag_queued(folder)
    refusing_writes_on(monkeypatch, "b")

    code, text = drive_human(resume_argv(job_id))

    assert code == int(ExitCode.PRECONDITION), text
    assert retag.UNWRITTEN_REASON in text
    assert f"{folder / 'b.flac'} would not take the genre {SPECIFIC!r}" in text, text


def test_a_parked_retag_keeps_both_the_block_and_the_reload(
    repair_on, folder, silence, monkeypatch
):
    """R-290: ``with_reload_step`` must keep the ``JobBlocked`` type."""
    coarses(folder, silence, "abc")
    inner = deep("abc")

    def parking_on_b(artist: str, name: str):
        if name == "b":
            raise jobs.Parked(
                refuse("provider-blocked", "the catalogue refused this client", origin=("test",)).cause
            )
        return inner(artist, name)

    parking_on_b.asked = inner.asked  # type: ignore[attr-defined]
    bound(monkeypatch, parking_on_b)
    job_id = retag_queued(folder)

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
    """The zero half: a run that changed nothing names no reload."""
    coarse(folder, silence, "a")
    bound(monkeypatch, raising_on(answering({}), "a"))
    job_id = retag_queued(folder)

    code, refused = drive(resume_argv(job_id))

    assert code != int(ExitCode.OK), refused
    assert tags.read_genre_from_file(folder / "a.flac") == CATCH_ALL
    steps = refused["cause"]["remediation"]["steps"]
    assert not any("reload" in step for step in steps), steps


def test_the_queueing_envelope_names_the_reload_before_the_person_walks_away(
    repair_on, folder, silence, monkeypatch
):
    """The queueing envelope always names the reload: every planned file is too coarse."""
    coarse(folder, silence, "a")
    bound(monkeypatch, deep("a"))

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
    """R-246: no database is opened, so no ``db_metadata`` and no cloud sync decision."""
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
    """The run flag belongs to the root parser, so it precedes the verb path."""
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
    bound(monkeypatch, deep("a"))

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
    searcher = bound(monkeypatch, deep("a"))

    code, queued = queue(folder)

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

    places(folder, silence, "abcd")
    answers = deep("abcd")

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
    """R-1184: named with its one answer; with no readable taxonomy the warning is unchanged."""
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
    """R-1184: a folder's own name in another case is named; a broken copy warns plainly."""
    from tests.test_active_taxonomy import write_active

    places(folder, silence, "ab")
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
    message = warned(resumed)[tag_cli.OFF_TAXONOMY]
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
    """U244: with no Discogs token both files are ``sources-unread`` and the login step is named."""
    places(folder, silence, "ab")

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
    warnings = warned(resumed)
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

    code, queued = queue(folder)
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
    coarses(folder, silence, "abc")
    bound(monkeypatch, deep("abc"))
    parses = counted(monkeypatch)

    job_id = retag_queued(folder)
    code, resumed = drive(resume_argv(job_id))

    assert code == int(ExitCode.OK), resumed
    assert item_states(job_id) == {
        str(folder / f"{name}.flac"): jobs.ItemState.DONE for name in "abc"
    }
    assert all(tags.read_genre_from_file(folder / f"{name}.flac") == SPECIFIC for name in "abc")
    assert parses.of(text) == 1, f"three files parsed the active copy {parses.of(text)} times"
