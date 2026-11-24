"""U40: correcting a genre that is already wrong, end to end.

An answer that is itself a catch all is never written, and a specific genre is
never touched. Section D drives ``write.metadata``'s failure paths as its first
caller.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.core import rb_writer, review, routing, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.tagging import retag
from cratekit.tagging.tag import SearchHit
from cratekit.write import metadata, trees
from tests._containers import synth_container

TAXONOMY = taxonomy.default_taxonomy()

#: A value the shipped template declares unusable as a final tag, and one it does
#: not, read off the taxonomy so a template edit moves the fixture with it.
CATCH_ALL = TAXONOMY.fallback.too_coarse_as_source[1]
SPECIFIC = "Deep House"


@pytest.fixture(autouse=True)
def _clean_registry():
    """The field policy registry is module state, reset so file order cannot matter."""
    rb_writer.reset_field_policies()
    yield
    rb_writer.reset_field_policies()


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One real FLAC container, synthesized once and copied per file."""
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def folder(tmp_path) -> Path:
    out = tmp_path / "Music"
    out.mkdir()
    return out


def place(folder: Path, silence: Path, name: str, genre: str | None) -> Path:
    """One audio file in the folder, carrying ``genre`` or carrying none."""
    path = folder / f"{name}.flac"
    shutil.copy2(silence, path)
    if genre is not None:
        assert tags.write_genre(path, genre), f"the fixture could not tag {name}"
    return path


def answering(table: dict[str, str]):
    """A searcher that answers by title and records what it was asked."""
    asked: list[tuple[str, str]] = []

    def searcher(artist: str, title: str):
        asked.append((artist, title))
        answer = table.get(title)
        return SearchHit(genre=answer) if answer else None

    searcher.asked = asked  # type: ignore[attr-defined]
    return searcher


@pytest.fixture
def store(tmp_path):
    with review.open_store(path=tmp_path / "review.db") as opened:
        yield opened


def _select(folder: Path) -> retag.Selection:
    return retag.select(folder, declared=TAXONOMY)


def _retag(folder: Path, store=None, table: dict[str, str] | None = None, *, searcher=None):
    """One pass over ``folder``, asking ``searcher`` or one answering ``table``."""
    asking = searcher or answering(table or {})
    return retag.retag_folder(folder, searcher=asking, declared=TAXONOMY, store=store)


def _page(store):
    return review.list_items(store, queue=str(review.Queue.GENRE))


def _unresolved(store) -> int:
    return review.count_unresolved(store, queue=str(review.Queue.GENRE))


def _resolve(store, item, verdict, option=None):
    return review.resolve(store, item.item_id, verdict, option=option, actor="a-person")


def _accept_specific(store):
    """The first queued item accepted with the specific genre as its answer."""
    item = _page(store).items[0]
    chosen = next(o for o in item.options if o.summary == SPECIFIC)
    _resolve(store, item, review.Verdict.ACCEPTED, option=chosen.option_id)
    return item


def _offer(store, path: Path, option: review.Option):
    return review.offer(
        store, queue=review.Queue.GENRE, kind=retag.KIND, identity=retag.identity_for(path),
        payload={"path": str(path)}, options=(option,), handler_key=retag.HANDLER_KEY,
    )


# A. Selection


def test_a_declared_catch_all_is_selected_and_a_specific_genre_is_not(folder, silence):
    """The plan's third scenario: a correct genre is never selected."""
    coarse = place(folder, silence, "coarse", CATCH_ALL)
    curated = place(folder, silence, "curated", SPECIFIC)

    selection = _select(folder)

    assert [c.path for c in selection.candidates] == [coarse]
    assert selection.candidates[0].current == CATCH_ALL
    assert (curated, retag.GENRE_SPECIFIC) in [(p.path, p.reason) for p in selection.passed]


def test_a_file_with_no_genre_is_passed_over_rather_than_selected(folder, silence):
    """Blank is too coarse by the predicate, yet not selected: fill if empty is
    ``tag.folder``'s, so the two verbs never own one state.
    """
    blank = place(folder, silence, "blank", None)
    assert TAXONOMY.is_too_coarse_as_source(""), (
        "the shipped template stopped declaring the empty string too coarse, so "
        "the divergence this test pins no longer exists and it is now vacuous"
    )

    selection = _select(folder)

    assert selection.candidates == ()
    assert [(p.path, p.reason) for p in selection.passed] == [(blank, retag.NO_GENRE)]


def test_a_folder_that_is_not_there_selects_nothing_rather_than_raising(tmp_path):
    assert _select(tmp_path / "absent") == retag.Selection()


def test_a_padded_catch_all_reaches_the_selection_already_trimmed(folder, silence):
    """The reader alone trims, so this pass keeps no second trim to drift."""
    path = place(folder, silence, "padded", f"  {CATCH_ALL} ")
    assert tags.read_genre_from_file(path) == CATCH_ALL, (
        "core.tags stopped trimming, so this pass is now reading padded values "
        "and needs its own normalization back"
    )

    selection = _select(folder)

    assert [c.path for c in selection.candidates] == [path]
    assert selection.candidates[0].current == CATCH_ALL


def test_the_selection_is_sorted_so_one_unchanged_folder_digests_the_same_twice(folder, silence):
    """The gate's digest rests on it: an unsorted walk would digest directory order."""
    for name in ("zulu", "alpha", "mike"):
        place(folder, silence, name, CATCH_ALL)

    first = retag.plan_items(_select(folder))
    second = retag.plan_items(_select(folder))

    assert len(first) == 3, "the fixture placed nothing, so the ordering claim is vacuous"
    assert first == second
    assert [item["path"] for item in first] == sorted(item["path"] for item in first)


# B. The pass over the files


def test_a_catch_all_gets_a_specific_answer_and_the_taxonomy_recognises_it(folder, silence, store):
    """Through the real tag writer; routing must recognise the answer as a bucket."""
    path = place(folder, silence, "track", CATCH_ALL)
    tags.write_tags(path, {"title": "Track One", "artist": "An Artist"})

    outcome = _retag(folder, store, {"Track One": SPECIFIC})

    assert [(r.path, r.written) for r in outcome.results] == [(path, SPECIFIC)]
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert TAXONOMY.bucket_for_display(SPECIFIC) is not None
    assert _unresolved(store) == 0


def test_an_answer_that_is_itself_a_catch_all_is_refused_and_the_file_is_untouched(
    folder, silence, store
):
    """A lookup never launders one catch all into another."""
    path = place(folder, silence, "track", CATCH_ALL)
    tags.write_tags(path, {"title": "Track One"})
    other = TAXONOMY.fallback.too_coarse_as_source[2]

    outcome = _retag(folder, store, {"Track One": other})

    assert tags.read_genre_from_file(path) == CATCH_ALL
    assert outcome.written == ()
    assert [(r.reason, r.proposed) for r in outcome.results] == [(retag.ANSWER_TOO_COARSE, other)]


def test_a_declined_answer_lands_in_the_review_queue(folder, silence, store):
    path = place(folder, silence, "track", CATCH_ALL)
    tags.write_tags(path, {"title": "Track One"})

    outcome = _retag(folder, store)

    assert [r.reason for r in outcome.results] == [retag.NO_ANSWER]
    page = _page(store)
    assert len(page) == 1
    item = page.items[0]
    assert item.payload["path"] == str(path)
    assert item.payload["current"] == CATCH_ALL
    assert item.handler_key == retag.HANDLER_KEY
    assert tags.read_genre_from_file(path) == CATCH_ALL


def test_a_second_run_offers_one_item_rather_than_a_second(folder, silence, store):
    place(folder, silence, "track", CATCH_ALL)
    for _ in range(2):
        _retag(folder, store)

    assert _unresolved(store) == 1


def test_a_resolved_verdict_is_used_and_the_searcher_is_never_asked_again(folder, silence, store):
    """The verdict is read before the searcher, so a fresh answer never overwrites it."""
    path = place(folder, silence, "track", CATCH_ALL)
    _retag(folder, store)
    _accept_specific(store)

    searcher = answering({})
    outcome = _retag(folder, store, searcher=searcher)

    assert searcher.asked == []
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert [r.written for r in outcome.results] == [SPECIFIC]


def test_a_rejected_verdict_leaves_the_file_alone_and_asks_nobody(folder, silence, store):
    """REJECTED is a decision against every candidate, not a gap."""
    path = place(folder, silence, "track", CATCH_ALL)
    _retag(folder, store)
    _resolve(store, _page(store).items[0], review.Verdict.REJECTED)

    searcher = answering({"Track One": SPECIFIC})
    outcome = _retag(folder, store, searcher=searcher)

    assert searcher.asked == []
    assert tags.read_genre_from_file(path) == CATCH_ALL
    assert [r.reason for r in outcome.results] == [retag.DECLINED_IN_REVIEW]


def test_a_rejected_items_chosen_option_is_not_an_answer(folder, silence, store):
    """``accepted_genre`` reads the verdict: a REJECTED item can carry a chosen option."""
    path = place(folder, silence, "track", CATCH_ALL)
    option = review.Option(option_id="deep", summary=SPECIFIC, detail={"genre": SPECIFIC})
    rejected = _resolve(store, _offer(store, path, option), review.Verdict.REJECTED, "deep")

    assert rejected.option == "deep", "the fixture recorded no option, so this is vacuous"
    assert retag.accepted_genre(rejected) == ""


def test_a_review_item_is_addressed_by_the_file_path_under_that_exact_name(tmp_path):
    """Renaming the key changes every item id across builds; R-182 covers the value."""
    path = tmp_path / "track.flac"
    assert retag.identity_for(path) == {"path": str(path)}


def test_the_offered_candidates_are_the_declared_buckets_and_never_a_catch_all():
    """The offer decides the answer set, so a catch all is never offered."""
    options = retag.options_for(TAXONOMY)

    assert options, "the shipped taxonomy declares no buckets, so this is vacuous"
    assert {o.option_id for o in options} <= {b.id for b in TAXONOMY.buckets}
    offered = [o.summary for o in options]
    assert not [name for name in offered if TAXONOMY.is_too_coarse_as_source(name)]
    assert TAXONOMY.fallback.bucket not in {o.option_id for o in options}


def test_the_correction_verb_cannot_write_a_genre_off_the_declared_taxonomy():
    """R-650's shape one verb over: every offered genre resolves through ``suggest_tag``."""
    offered = [
        (option.detail or {}).get("genre") or option.summary
        for option in retag.options_for(TAXONOMY)
    ]
    assert offered, "the shipped taxonomy declares no buckets, so this is vacuous"
    assert not [name for name in offered if routing.suggest_tag(TAXONOMY, name).off_taxonomy]


def test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused(folder, silence, store):
    """Reachable only by an older or hand written item, and the write refuses it anyway."""
    path = place(folder, silence, "track", CATCH_ALL)
    coarse = review.Option(option_id="coarse", summary=CATCH_ALL, detail={"genre": CATCH_ALL})
    _resolve(store, _offer(store, path, coarse), review.Verdict.ACCEPTED, "coarse")

    outcome = _retag(folder, store)

    assert tags.read_genre_from_file(path) == CATCH_ALL
    assert [(r.reason, r.proposed) for r in outcome.results] == [
        (retag.ANSWER_TOO_COARSE, CATCH_ALL)
    ]


def test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question(
    folder, silence, store
):
    """A REJECTED item has an id, so "has an id and was not written" is no question."""
    settled = place(folder, silence, "settled", CATCH_ALL)
    open_one = place(folder, silence, "open", CATCH_ALL)
    _retag(folder, store)
    item = next(i for i in _page(store).items if i.payload["path"] == str(settled))
    _resolve(store, item, review.Verdict.REJECTED)

    outcome = _retag(folder, store)

    assert {r.path for r in outcome.asked} == {open_one}
    assert {r.path for r in outcome.results} == {settled, open_one}
    assert outcome.written == ()


def test_every_result_carries_a_reason_or_a_written_genre_and_never_both():
    """A result carrying both would be counted twice in a report."""
    cases = (
        retag.RetagResult(path=Path("a"), current=CATCH_ALL, written=SPECIFIC),
        retag.RetagResult(path=Path("b"), current=CATCH_ALL, reason=retag.NO_ANSWER),
    )
    assert len(cases) == 2, "the case table is empty, so this proves nothing"
    for case in cases:
        assert bool(case.written) != bool(case.reason)


def test_the_item_id_this_pass_computes_is_the_one_the_queue_stores(folder, silence, store):
    """Two computations of one id; diverging would re-ask a settled question for ever."""
    path = place(folder, silence, "track", CATCH_ALL)
    _retag(folder, store)

    stored = _page(store).items[0]
    computed = review.item_id_for(review.Queue.GENRE, retag.KIND, retag.identity_for(path))

    assert stored.item_id == computed


def test_a_pass_with_no_store_reports_what_it_could_not_settle(folder, silence):
    """No item id is how a caller tells "asked" from "could not ask"."""
    place(folder, silence, "track", CATCH_ALL)

    outcome = _retag(folder)

    assert [(r.reason, r.item_id) for r in outcome.results] == [(retag.NO_ANSWER, "")]


def test_a_second_run_over_a_corrected_folder_selects_nothing(folder, silence, store):
    """The unit's own verification step: every state at once, then re-run."""
    correct = place(folder, silence, "correct", SPECIFIC)
    coarse = place(folder, silence, "coarse", CATCH_ALL)
    ambiguous = place(folder, silence, "ambiguous", CATCH_ALL)
    blank = place(folder, silence, "blank", None)
    tags.write_tags(coarse, {"title": "Answerable"})
    tags.write_tags(ambiguous, {"title": "Unanswerable"})

    first = _retag(folder, store, {"Answerable": SPECIFIC})
    assert {r.path for r in first.written} == {coarse}
    assert {r.path for r in first.asked} == {ambiguous}
    assert {p.path for p in first.passed} == {correct, blank}

    second = _select(folder)

    assert [c.path for c in second.candidates] == [ambiguous], (
        "the corrected file was selected again, so the pass is not idempotent; "
        "the only candidate left is the one still waiting on a person"
    )


# C. The plan the gate is answered against


def test_the_plan_digest_changes_when_the_selection_changes(folder, silence):
    """A wider folder makes a stale decision, never a wider sweep than approved."""
    from cratekit.cli.output import digest_of

    place(folder, silence, "one", CATCH_ALL)
    before = digest_of({"items": retag.plan_items(_select(folder))})
    place(folder, silence, "two", CATCH_ALL)
    after = digest_of({"items": retag.plan_items(_select(folder))})

    assert before != after


def test_the_shell_digests_the_selection_and_the_folder_rather_than_a_constant(
    folder, silence, tmp_path
):
    """The rows and the folder are both in the digest."""
    from cratekit.tagging import retag_cli

    empty_one = tmp_path / "EmptyOne"
    empty_two = tmp_path / "EmptyTwo"
    empty_one.mkdir()
    empty_two.mkdir()
    place(folder, silence, "one", CATCH_ALL)
    before = retag_cli.plan_for(str(folder), TAXONOMY)
    place(folder, silence, "two", CATCH_ALL)
    after = retag_cli.plan_for(str(folder), TAXONOMY)

    assert before["totals"]["count"] == 1 and after["totals"]["count"] == 2
    assert before["digest"] != after["digest"], "a wider selection digests the same"
    assert (
        retag_cli.plan_for(str(empty_one), TAXONOMY)["digest"]
        != retag_cli.plan_for(str(empty_two), TAXONOMY)["digest"]
    ), "two different empty folders digest alike, so the folder is not in the digest"


def test_the_plan_carries_the_current_value_so_the_person_sees_what_is_being_replaced(
    folder, silence
):
    place(folder, silence, "one", CATCH_ALL)
    items = retag.plan_items(_select(folder))
    assert items == [{"path": str(folder / "one.flac"), "current": CATCH_ALL}]


# D. The database half. First-caller drives of write.metadata.


class Row:
    """A content row stand-in, duck-typed exactly as the writer treats one."""

    def __init__(self, ident, **fields):
        self.ID = ident
        for key, value in fields.items():
            setattr(self, key, value)


class FakeLookup:
    """The genre lookup half of the binding, and nothing else."""

    def __init__(self, rows):
        self._rows = list(rows)

    def get_genre(self, Name=None):  # noqa: N803 - the binding spells it this way
        return [row for row in self._rows if row.Name == Name]


def written_outcome(path: Path, genre: str = SPECIFIC) -> retag.RetagOutcome:
    return retag.RetagOutcome(
        results=(retag.RetagResult(path=path, current=CATCH_ALL, written=genre),)
    )


LIVE = Row("7", Name=SPECIFIC, rb_local_deleted=0)
TOMBSTONE = Row("6", Name=SPECIFIC, rb_local_deleted=1)


def one_row(tmp_path: Path, *genres: Row, genre_id: str | None = None, deleted=False):
    """One track's path, its content row, its mapped row, and a genre lookup."""
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=deleted)]
    return path, rows, {"1": Row("1", GenreID=genre_id)}, FakeLookup(genres)


def _planned(tmp_path: Path, *genres: Row, **row):
    """``one_row``'s track, written, planned against ``genres``: the path, mapped, the plan."""
    path, rows, mapped, db = one_row(tmp_path, *genres, **row)
    return path, mapped, retag.plan_library(written_outcome(path), rows, mapped, root=tmp_path, db=db)


def test_a_written_file_is_relinked_to_the_existing_genre_row(tmp_path):
    _, mapped, planned = _planned(tmp_path, LIVE)
    report = retag.apply_library(planned, mapped)

    assert planned.unmatched == ()
    assert report.written == ("1",)
    assert mapped["1"].GenreID == "7"


def test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader(tmp_path):
    """U59: through the reader every shipped verb reaches, a retired row is a
    ``genre-unknown`` skip, never a ``GenreID`` pointed at a tombstone.
    """
    _, mapped, planned = _planned(tmp_path, TOMBSTONE)
    report = retag.apply_library(planned, mapped)

    assert planned.plan.changes == (), (
        "a soft-deleted genre row was linked through the shipped read path, so "
        "the track now points at a row rekordbox has already retired"
    )
    assert [(skip.content_id, skip.reason) for skip in planned.plan.skipped] == [
        ("1", "genre-unknown")
    ]
    assert mapped["1"].GenreID is None
    assert report.written == ()


def test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader(tmp_path):
    """The control: the first active row wins, the tombstone listed first."""
    _, mapped, planned = _planned(tmp_path, TOMBSTONE, LIVE)
    retag.apply_library(planned, mapped)

    assert planned.plan.skipped == ()
    assert mapped["1"].GenreID == "7"


def test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row(tmp_path):
    """A binding that stops exposing the column is a run refusal, not per row skips."""
    path, rows, mapped, db = one_row(tmp_path, Row("6", Name=SPECIFIC))

    with pytest.raises(CratekitError) as raised:
        retag.plan_library(written_outcome(path), rows, mapped, root=tmp_path, db=db)

    cause = raised.value.cause
    assert cause.reason == "soft-delete-marker-unreadable"
    assert cause.detail["genre"] == SPECIFIC
    # A one element origin would mean a hop caught and rebuilt the cause.
    assert cause.origin[0] == "write"
    assert mapped["1"].GenreID is None


def test_the_plan_is_built_from_what_was_written_and_never_from_the_selection(tmp_path):
    """A plan built from the selection would name a row whose write was refused."""
    path, rows, mapped, db = one_row(tmp_path, LIVE)
    refused = retag.RetagOutcome(
        results=(retag.RetagResult(path=path, current=CATCH_ALL, reason=retag.ANSWER_TOO_COARSE),)
    )

    planned = retag.plan_library(refused, rows, mapped, root=tmp_path, db=db)
    retag.apply_library(planned, mapped)

    assert planned.plan.changes == ()
    # The skip list is what matters: a plan from the selection skips the refused
    # row as genre "None", so an empty change list alone holds either way.
    assert planned.plan.skipped == (), (
        "the refused file reached the plan and was rejected by the genre lookup "
        "rather than never entering it, so the plan is built from the selection"
    )
    assert mapped["1"].GenreID is None


def test_a_soft_deleted_row_is_never_retagged(tmp_path):
    """The caller drops the tombstone; the planner takes the rows it is handed."""
    path, mapped, planned = _planned(tmp_path, LIVE, deleted=True)
    retag.apply_library(planned, mapped)

    assert planned.plan.changes == ()
    assert [(u.path, u.outcome) for u in planned.unmatched] == [(str(path), "absent")]
    assert mapped["1"].GenreID is None


def test_a_genre_the_library_has_never_seen_is_skipped_and_surfaced(tmp_path):
    """``resolve_genre_id`` never creates a row."""
    _, mapped, planned = _planned(tmp_path, Row("7", Name="Something Else", rb_local_deleted=0))
    report = retag.apply_library(planned, mapped)

    assert [(s.reason, s.detail) for s in planned.plan.skipped] == [("genre-unknown", SPECIFIC)]
    assert report.written == ()
    assert mapped["1"].GenreID is None


def test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row(tmp_path):
    """Through this caller, where a real lookup returns both."""
    _, mapped, planned = _planned(tmp_path, TOMBSTONE, LIVE)
    retag.apply_library(planned, mapped)

    assert mapped["1"].GenreID == "7"


def test_a_written_file_no_live_row_claims_is_surfaced_rather_than_dropped(tmp_path):
    """The file is already corrected, so silence would misreport the sweep."""
    path = tmp_path / "track.flac"

    planned = retag.plan_library(written_outcome(path), [], {}, root=tmp_path, db=FakeLookup([LIVE]))

    assert planned.plan.changes == ()
    assert [(u.path, u.outcome) for u in planned.unmatched] == [(str(path), "absent")]


def test_two_live_rows_on_one_location_are_surfaced_rather_than_written_to_both(tmp_path):
    """A double import leaves two live rows for one file; writing both is wrong."""
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id=i, recorded=str(path), deleted=False) for i in "12"]
    mapped = {"1": Row("1", GenreID=None), "2": Row("2", GenreID=None)}

    planned = retag.plan_library(
        written_outcome(path), rows, mapped, root=tmp_path, db=FakeLookup([LIVE])
    )
    retag.apply_library(planned, mapped)

    assert planned.plan.changes == ()
    assert [(u.outcome, u.content_ids) for u in planned.unmatched] == [("ambiguous", ("1", "2"))]
    assert mapped["1"].GenreID is None and mapped["2"].GenreID is None


def test_two_written_files_resolving_to_one_row_are_both_surfaced_and_neither_wins(tmp_path):
    """The mirror of the ambiguous case: NFC and NFD names are one location, and
    keying on the content id would let the last file decide the row.
    """
    import unicodedata

    name = "café.flac"
    composed = tmp_path / unicodedata.normalize("NFC", name)
    decomposed = tmp_path / unicodedata.normalize("NFD", name)
    assert composed != decomposed, "the two forms are one string, so this is vacuous"

    outcome = retag.RetagOutcome(
        results=(
            retag.RetagResult(path=composed, current=CATCH_ALL, written=SPECIFIC),
            retag.RetagResult(path=decomposed, current=CATCH_ALL, written="Techno"),
        )
    )
    rows = [trees.ContentRow(content_id="1", recorded=str(composed), deleted=False)]
    mapped = {"1": Row("1", GenreID=None)}
    db = FakeLookup([LIVE, Row("8", Name="Techno", rb_local_deleted=0)])

    planned = retag.plan_library(outcome, rows, mapped, root=tmp_path, db=db)
    retag.apply_library(planned, mapped)

    assert [u.outcome for u in planned.unmatched] == ["contested", "contested"], (
        "one of the two files was written to the row and the other was dropped, "
        "so the last answer decided a row two files claimed"
    )
    assert {u.path for u in planned.unmatched} == {str(composed), str(decomposed)}
    assert planned.plan.changes == ()
    assert mapped["1"].GenreID is None


def test_a_matched_row_the_caller_did_not_supply_is_surfaced_rather_than_silent(tmp_path):
    """The plan says so too, as ``write_plan`` does."""
    path, rows, _, db = one_row(tmp_path, LIVE)

    planned = retag.plan_library(written_outcome(path), rows, {}, root=tmp_path, db=db)

    assert planned.plan.changes == ()
    assert [(s.content_id, s.reason) for s in planned.plan.skipped] == [("1", "row-absent")]


def test_the_apply_refuses_a_field_the_retag_policy_does_not_own(tmp_path):
    """A sweep that silently writes nothing looks like one with nothing to do."""
    del tmp_path
    foreign = metadata.Plan(
        metadata.RETAG_GENRE, (metadata.Change("1", metadata.RETAG_GENRE, "Rating", None, 4),)
    )

    with pytest.raises(CratekitError) as excinfo:
        retag.apply_library(retag.LibraryPlan(plan=foreign), {"1": Row("1", Rating=None)})

    assert excinfo.value.cause.reason == "refused-by-policy"
    assert "Rating" in excinfo.value.cause.message


def test_an_unregistered_operation_writes_nothing_and_the_apply_is_what_prevents_it(tmp_path):
    """Unregistered, a plan writes nothing and reports clean; ``apply_library`` writes."""
    _, unregistered, planned = _planned(tmp_path, LIVE)
    rb_writer.reset_field_policies()
    bare = metadata.write_plan(planned.plan, unregistered)
    assert bare.totals["skip_unowned"] == 1
    assert bare.written == ()
    assert unregistered["1"].GenreID is None

    rb_writer.reset_field_policies()
    _, guarded, planned = _planned(tmp_path, LIVE)
    report = retag.apply_library(planned, guarded)
    assert report.written == ("1",)
    assert guarded["1"].GenreID == "7"


def test_re_applying_a_plan_over_an_already_linked_row_is_a_no_op(tmp_path):
    """Idempotence at the database end: the same value twice reports skip_same."""
    _, mapped, planned = _planned(tmp_path, LIVE, genre_id="7")
    report = retag.apply_library(planned, mapped)

    assert report.totals["skip_same"] == 1
    assert report.written == ()


def test_the_retag_operation_owns_the_genre_column_and_nothing_else():
    """Widening the policy fails here as well as in the policy suite."""
    policy = metadata.OPERATIONS[metadata.RETAG_GENRE]
    assert dict(policy.fields) == {"GenreID": rb_writer.Ownership.OWNED}


# E. The shell


def test_the_resume_argv_carries_the_folder_the_job_and_the_gate_run():
    from cratekit.core import jobs
    from cratekit.tagging import retag_cli

    class _Job:
        job_id = "job-1"
        payload = {"folder": "/some/folder", jobs.GATE_RUN_KEY: "gate-run-1"}

    assert retag_cli.retag_argv(_Job()) == [
        "--run", "gate-run-1", "tag", "retag", "/some/folder", "--job", "job-1",
    ]


def test_an_empty_folder_argument_refuses_rather_than_sweeping_the_working_directory():
    """The parser accepts an empty string, so the branch refuses with a declared slug."""
    from cratekit.core.exit_codes import ExitCode
    from cratekit.tagging import retag_cli

    ctx = SimpleNamespace(args=SimpleNamespace(folder="", job=None))

    with pytest.raises(CratekitError) as excinfo:
        retag_cli.retag_genres(ctx)

    cause = excinfo.value.cause
    assert cause.reason == "tag-retag-folder-unknown"
    assert cause.code is ExitCode.PRECONDITION, (
        "the argument parser accepted this invocation, so status 2 is not this "
        "refusal's, and a destructive verb refusing is not a defect in the program"
    )


def _gated(gates) -> SimpleNamespace:
    """A handler context whose ``tag.retag`` entry declares ``gates``."""
    return SimpleNamespace(entry=SimpleNamespace(gates=gates, name="tag.retag"))


def test_the_handler_finds_its_gate_by_digest_source_and_not_by_position():
    """Indexing ``gates[0]`` would answer the wrong question once reordered.

    The neighbour is added by hand, since the entry holds one gate since R-246.
    """
    from cratekit.cli import registry
    from cratekit.tagging import retag_cli

    entry = registry.entry("tag.retag")
    assert registry.CLOUD_SYNC_UNREADABLE_GATE.digest_source is None, (
        "the neighbour has gained a plan digest source, so it is no longer the "
        "wrong answer this search has to step over"
    )
    reordered = type(entry.gates)(reversed((*entry.gates, registry.CLOUD_SYNC_UNREADABLE_GATE)))
    assert reordered[0] is not entry.gates[0], (
        "the plan gate is still first, so this case cannot see a search that "
        "indexes position instead of digest source"
    )

    assert retag_cli._plan_gate(_gated(reordered)).name == "tag.retag.confirm"


def test_the_handler_refuses_when_its_entry_declares_no_plan_gate():
    """A registry edit dropping the confirmation would sweep with nobody asked."""
    from cratekit.tagging import retag_cli

    with pytest.raises(CratekitError) as excinfo:
        retag_cli._plan_gate(_gated(()))
    assert excinfo.value.cause.reason == "refused-by-policy"


def test_the_frozen_rows_digest_the_same_after_the_folder_has_moved_under_them(folder, silence):
    """KTD8 and R13: a resume digests the frozen rows, not a fresh walk."""
    from cratekit.tagging import retag_cli

    place(folder, silence, "one", CATCH_ALL)
    place(folder, silence, "two", CATCH_ALL)
    confirmed = retag_cli.plan_for(str(folder), TAXONOMY)

    assert tags.write_genre(folder / "one.flac", SPECIFIC), "the fixture wrote nothing"
    walked_again = retag_cli.plan_for(str(folder), TAXONOMY)

    assert walked_again["digest"] != confirmed["digest"], (
        "a corrected file left the selection unchanged, so this case cannot see "
        "the staleness the frozen payload exists to prevent"
    )
    assert retag_cli.digest_for(str(folder), confirmed["items"]) == confirmed["digest"], (
        "the frozen rows no longer digest as the plan they were frozen from"
    )
    assert retag_cli.digest_for(str(folder), walked_again["items"]) != confirmed["digest"]


def test_the_frozen_rows_survive_the_json_the_payload_is_stored_as(folder, silence):
    """The resume digests rows ``core.jobs`` has serialized as JSON."""
    import json

    from cratekit.tagging import retag_cli

    place(folder, silence, "one", CATCH_ALL)
    confirmed = retag_cli.plan_for(str(folder), TAXONOMY)

    round_tripped = json.loads(json.dumps({"items": confirmed["items"]}))["items"]

    assert retag_cli.digest_for(str(folder), round_tripped) == confirmed["digest"]


def test_two_different_empty_folders_digest_differently_through_the_pure_function(tmp_path):
    """On the function the resume calls, which cannot walk and could lose the folder."""
    from cratekit.tagging import retag_cli

    one, two = (retag_cli.digest_for(str(tmp_path / name), []) for name in ("EmptyOne", "EmptyTwo"))
    assert one != two


# R-1103. A file that will not take its answer is unwritten, never corrected


def refusing_on(monkeypatch, *names: str) -> None:
    """The one genre writer, answering False for the files named, as it does for a
    locked file; patched since root ignores a read only mode (R-1103).
    """
    real = tags.write_genre

    def writer(path: Path, genre: str) -> bool:
        if path.stem in names:
            return False
        return real(path, genre)

    monkeypatch.setattr(tags, "write_genre", writer)


def test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected(
    folder, silence, store, monkeypatch
):
    """Read back off disk, since the defect is an outcome agreeing with itself."""
    paths = {name: place(folder, silence, name, CATCH_ALL) for name in ("a", "b", "c")}
    refusing_on(monkeypatch, "b")

    outcome = _retag(folder, store, {name: SPECIFIC for name in "abc"})

    assert [r.path for r in outcome.written] == [paths["a"], paths["c"]]
    unwritten = [r for r in outcome.results if r.written is None]
    assert [(r.path, r.reason, r.proposed, r.current) for r in unwritten] == [
        (paths["b"], retag.UNWRITTEN_REASON, SPECIFIC, CATCH_ALL)
    ]
    assert tags.read_genre_from_file(paths["b"]) == CATCH_ALL
    assert tags.read_genre_from_file(paths["a"]) == SPECIFIC
    assert tags.read_genre_from_file(paths["c"]) == SPECIFIC
    assert outcome.asked == ()
    assert _unresolved(store) == 0, "the answer was there, so nothing is asked of a person"


def test_an_unwritten_file_never_reaches_the_library_plan(folder, silence, monkeypatch):
    """``plan_library`` plans from what was written, and an unwritten file is not."""
    place(folder, silence, "a", CATCH_ALL)
    refusing_on(monkeypatch, "a")

    outcome = _retag(folder, table={"a": SPECIFIC})

    assert outcome.written == ()
    planned = retag.plan_library(outcome, [], {}, root=folder, db=None)
    assert planned.plan.changes == ()
    assert planned.unmatched == ()


def test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run(
    folder, silence, store, monkeypatch
):
    """A person's answer is not spent on a write that did not land."""
    path = place(folder, silence, "track", CATCH_ALL)
    _retag(folder, store)
    item = _accept_specific(store)

    with monkeypatch.context() as patched:
        refusing_on(patched, "track")
        searcher = answering({})
        refused = _retag(folder, store, searcher=searcher)
    assert searcher.asked == []
    assert [(r.reason, r.proposed, r.written) for r in refused.results] == [
        (retag.UNWRITTEN_REASON, SPECIFIC, None)
    ]
    assert tags.read_genre_from_file(path) == CATCH_ALL
    assert review.get(store, item.item_id).resolved

    landed = _retag(folder, store)
    assert [r.written for r in landed.results] == [SPECIFIC]
    assert tags.read_genre_from_file(path) == SPECIFIC
