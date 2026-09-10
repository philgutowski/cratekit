"""U40: correcting a genre that is already wrong, end to end.

WHAT THIS SUITE IS ACTUALLY GUARDING. ``tag.folder`` is fill-if-empty by
construction, so a file that arrives carrying a vendor catch-all is skipped by
every tagging verb this product had, routes to the fallback bucket, and stays
there. This verb is the only thing that can look a better answer up, which makes
two properties load bearing above all others: it must never write an answer that
is itself a catch-all, because that launders the problem into a value it would
never select again, and it must never touch a file whose genre is specific,
because that is somebody's curation.

THE FIRST-CALLER OBLIGATION IS DISCHARGED HERE. ``write.metadata`` shipped in
U21 with three planners and NO caller anywhere in ``src``: a grep for
``plan_genre_retag`` over ``main`` at ``dbc7150`` returns the definition, the
``__all__`` entry, and two tests. This unit is the first caller, so under
``docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md``
its failure paths are this unit's to drive. Section D below drives them: the
unresolvable genre name, the row nothing supplied, the tombstone, and the one
that is a real hole rather than a documented skip, an operation nobody registered
deciding SKIP_UNOWNED for every change and reporting a clean run over a library
it did not touch.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from cratekit.core import rb_writer, review, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.tagging import retag
from cratekit.tagging.tag import SearchHit
from cratekit.write import metadata, trees
from tests._containers import synth_container

TAXONOMY = taxonomy.default_taxonomy()

#: A value the shipped template declares unusable as a final tag, and one it does
#: not. Read off the taxonomy rather than typed, so a template edit moves the
#: fixture with it instead of leaving a test asserting about a value nobody
#: declares any more.
CATCH_ALL = TAXONOMY.fallback.too_coarse_as_source[1]
SPECIFIC = "Deep House"


@pytest.fixture(autouse=True)
def _clean_registry():
    """The field-policy registry is module state in core, so it is reset around
    every test here. ``apply_library`` enables an operation on purpose; without
    this, whether a later suite's "this field is not writable" assertion passes
    would depend on file order.
    """
    rb_writer.reset_field_policies()
    yield
    rb_writer.reset_field_policies()


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One real FLAC container, synthesized once and copied per file.

    A real container rather than a stub, because the write under test goes through
    ``core.tags.write_genre`` and a stub would prove the selection and nothing
    about the write.
    """
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
    """A searcher that answers by TITLE, and records what it was asked.

    The recording is not decoration: two tests below assert that the searcher was
    not asked at all, and a searcher with no memory cannot tell "asked and
    declined" from "never asked".
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# A. Selection
# ═══════════════════════════════════════════════════════════════════════════


def test_a_declared_catch_all_is_selected_and_a_specific_genre_is_not(folder, silence):
    """The plan's third scenario: a correct genre is never selected."""
    coarse = place(folder, silence, "coarse", CATCH_ALL)
    curated = place(folder, silence, "curated", SPECIFIC)

    selection = retag.select(folder, declared=TAXONOMY)

    assert [c.path for c in selection.candidates] == [coarse]
    assert selection.candidates[0].current == CATCH_ALL
    assert (curated, retag.GENRE_SPECIFIC) in [(p.path, p.reason) for p in selection.passed]


def test_a_file_with_no_genre_is_passed_over_rather_than_selected(folder, silence):
    """THE PREDICATE SAYS BLANK IS TOO COARSE AND THE SELECTION STILL REFUSES IT.

    ``is_too_coarse_as_source("")`` is True because the declared list carries the
    empty string, so selecting on that predicate alone would put this verb and
    ``tag.folder`` on one state under two different ownership policies: fill if
    empty there, OWNED here. This asserts the predicate's answer AND the
    selection's, because the whole content of the decision is that they differ.
    """
    blank = place(folder, silence, "blank", None)
    assert TAXONOMY.is_too_coarse_as_source(""), (
        "the shipped template stopped declaring the empty string too coarse, so "
        "the divergence this test pins no longer exists and it is now vacuous"
    )

    selection = retag.select(folder, declared=TAXONOMY)

    assert selection.candidates == ()
    assert [(p.path, p.reason) for p in selection.passed] == [(blank, retag.NO_GENRE)]


def test_a_folder_that_is_not_there_selects_nothing_rather_than_raising(tmp_path):
    assert retag.select(tmp_path / "absent", declared=TAXONOMY) == retag.Selection()


def test_a_padded_catch_all_reaches_the_selection_already_trimmed(folder, silence):
    """WHY THIS PASS DOES NO TRIMMING OF ITS OWN, pinned where somebody would add
    one back.

    The obvious guard, stripping the value `select` reads, is dead code:
    `tags.read_tag` trims every value it returns, so no input can reach the
    selection padded and a mutation removing a strip here killed nothing. That
    measurement is what this test records. The candidate's `current` is what the
    plan shows a person and what the review payload stores, so it matters that it
    is trimmed; it just is not this module's job to trim it, and doing it twice is
    two opinions that agree until one of them moves.
    """
    path = place(folder, silence, "padded", f"  {CATCH_ALL} ")
    assert tags.read_genre_from_file(path) == CATCH_ALL, (
        "core.tags stopped trimming, so this pass is now reading padded values "
        "and needs its own normalization back"
    )

    selection = retag.select(folder, declared=TAXONOMY)

    assert [c.path for c in selection.candidates] == [path]
    assert selection.candidates[0].current == CATCH_ALL


def test_the_selection_is_sorted_so_one_unchanged_folder_digests_the_same_twice(
    folder, silence
):
    """The property the gate's digest rests on. An unsorted walk would make the
    digest depend on directory order, so a run that changed nothing could present
    a person with a stale decision.
    """
    for name in ("zulu", "alpha", "mike"):
        place(folder, silence, name, CATCH_ALL)

    first = retag.plan_items(retag.select(folder, declared=TAXONOMY))
    second = retag.plan_items(retag.select(folder, declared=TAXONOMY))

    assert len(first) == 3, "the fixture placed nothing, so the ordering claim is vacuous"
    assert first == second
    assert [item["path"] for item in first] == sorted(item["path"] for item in first)


# ═══════════════════════════════════════════════════════════════════════════
# B. The pass over the files
# ═══════════════════════════════════════════════════════════════════════════


def test_a_catch_all_gets_a_specific_answer_and_the_taxonomy_recognises_it(
    folder, silence, store
):
    """The plan's first scenario, through the real tag writer.

    The last assertion is the half that makes the write worth anything: routing
    places a track by looking its genre up as a bucket display name, so an answer
    the taxonomy cannot recognise corrects the tag and leaves the track exactly
    where it was.
    """
    path = place(folder, silence, "track", CATCH_ALL)
    tags.write_tags(path, {"title": "Track One", "artist": "An Artist"})

    outcome = retag.retag_folder(
        folder, searcher=answering({"Track One": SPECIFIC}), declared=TAXONOMY, store=store
    )

    assert [(r.path, r.written) for r in outcome.results] == [(path, SPECIFIC)]
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert TAXONOMY.bucket_for_display(SPECIFIC) is not None
    assert review.count_unresolved(store, queue=str(review.Queue.GENRE)) == 0


def test_an_answer_that_is_itself_a_catch_all_is_refused_and_the_file_is_untouched(
    folder, silence, store
):
    """The plan's second scenario. A lookup can never launder one catch-all into
    another: writing it would count as progress and re-reading the write would
    not, so the file would never be selected again.
    """
    path = place(folder, silence, "track", CATCH_ALL)
    tags.write_tags(path, {"title": "Track One"})
    other = TAXONOMY.fallback.too_coarse_as_source[2]

    outcome = retag.retag_folder(
        folder, searcher=answering({"Track One": other}), declared=TAXONOMY, store=store
    )

    assert tags.read_genre_from_file(path) == CATCH_ALL
    assert outcome.written == ()
    assert [(r.reason, r.proposed) for r in outcome.results] == [
        (retag.ANSWER_TOO_COARSE, other)
    ]


def test_a_declined_answer_lands_in_the_review_queue(folder, silence, store):
    """The plan's fourth scenario, first half."""
    path = place(folder, silence, "track", CATCH_ALL)
    tags.write_tags(path, {"title": "Track One"})

    outcome = retag.retag_folder(
        folder, searcher=answering({}), declared=TAXONOMY, store=store
    )

    assert [r.reason for r in outcome.results] == [retag.NO_ANSWER]
    page = review.list_items(store, queue=str(review.Queue.GENRE))
    assert len(page) == 1
    item = page.items[0]
    assert item.payload["path"] == str(path)
    assert item.payload["current"] == CATCH_ALL
    assert item.handler_key == retag.HANDLER_KEY
    assert tags.read_genre_from_file(path) == CATCH_ALL


def test_a_second_run_offers_one_item_rather_than_a_second(folder, silence, store):
    """``review.offer`` is idempotent on the identity, and this is what that buys."""
    place(folder, silence, "track", CATCH_ALL)
    for _ in range(2):
        retag.retag_folder(folder, searcher=answering({}), declared=TAXONOMY, store=store)

    assert review.count_unresolved(store, queue=str(review.Queue.GENRE)) == 1


def test_a_resolved_verdict_is_used_and_the_searcher_is_never_asked_again(
    folder, silence, store
):
    """The plan's fourth scenario, second half, and the ORDERING inside it.

    Asking the searcher first and reading the verdict afterwards would spend a
    lookup per run on a question a person already answered, and would let a fresh
    answer overwrite the recorded one. The assertion that the searcher was not
    asked is what separates the two implementations; asserting only the written
    genre passes for both.
    """
    path = place(folder, silence, "track", CATCH_ALL)
    retag.retag_folder(folder, searcher=answering({}), declared=TAXONOMY, store=store)
    item = review.list_items(store, queue=str(review.Queue.GENRE)).items[0]
    chosen = next(o for o in item.options if o.summary == SPECIFIC)
    review.resolve(store, item.item_id, review.Verdict.ACCEPTED, option=chosen.option_id,
                   actor="a-person")

    searcher = answering({})
    outcome = retag.retag_folder(folder, searcher=searcher, declared=TAXONOMY, store=store)

    assert searcher.asked == []
    assert tags.read_genre_from_file(path) == SPECIFIC
    assert [r.written for r in outcome.results] == [SPECIFIC]


def test_a_rejected_verdict_leaves_the_file_alone_and_asks_nobody(folder, silence, store):
    """REJECTED is settled AGAINST every candidate, which is a decision and not a
    gap. The file keeps its coarse genre, the searcher is not spent on it, and
    nothing is re-offered.
    """
    path = place(folder, silence, "track", CATCH_ALL)
    retag.retag_folder(folder, searcher=answering({}), declared=TAXONOMY, store=store)
    item = review.list_items(store, queue=str(review.Queue.GENRE)).items[0]
    review.resolve(store, item.item_id, review.Verdict.REJECTED, actor="a-person")

    searcher = answering({"Track One": SPECIFIC})
    outcome = retag.retag_folder(folder, searcher=searcher, declared=TAXONOMY, store=store)

    assert searcher.asked == []
    assert tags.read_genre_from_file(path) == CATCH_ALL
    assert [r.reason for r in outcome.results] == [retag.DECLINED_IN_REVIEW]


def test_a_rejected_items_chosen_option_is_not_an_answer(folder, silence, store):
    """``accepted_genre`` reads the VERDICT, not just the option, and this is the
    drive that separates the two.

    A person can reject an item and still have chosen a candidate along the way,
    so an option is present on a REJECTED item. A reader that took the option and
    skipped the verdict would turn every rejection into an acceptance, and the
    pass-level test cannot see it, because ``retag_folder`` checks ``suppressed``
    first and never reaches this function on that path.
    """
    path = place(folder, silence, "track", CATCH_ALL)
    option = review.Option(option_id="deep", summary=SPECIFIC, detail={"genre": SPECIFIC})
    offered = review.offer(
        store,
        queue=review.Queue.GENRE,
        kind=retag.KIND,
        identity=retag.identity_for(path),
        payload={"path": str(path)},
        options=(option,),
        handler_key=retag.HANDLER_KEY,
    )
    rejected = review.resolve(
        store, offered.item_id, review.Verdict.REJECTED, option="deep", actor="a-person"
    )

    assert rejected.option == "deep", "the fixture recorded no option, so this is vacuous"
    assert retag.accepted_genre(rejected) == ""


def test_a_review_item_is_addressed_by_the_file_path_under_that_exact_name(tmp_path):
    """THE KEY NAME IS PINNED, and no same-run test can pin it.

    ``review.item_id_for`` hashes this mapping, so renaming the key changes every
    item identifier. Within one run both halves rename together and everything
    stays self-consistent, which is why every other test here passes either way.
    What breaks is across builds: every question a person already answered becomes
    unreachable and is asked again under a new identifier. R-182 records the
    related cost of the VALUE moving; this pins the NAME.
    """
    path = tmp_path / "track.flac"
    assert retag.identity_for(path) == {"path": str(path)}


def test_the_offered_candidates_are_the_declared_buckets_and_never_a_catch_all():
    """``review.resolve`` refuses an option the item does not offer, so the OFFER
    is where the answer set is decided. A catch-all among the candidates would put
    an answer in front of a person that the write is then going to refuse.
    """
    options = retag.options_for(TAXONOMY)

    assert options, "the shipped taxonomy declares no buckets, so this is vacuous"
    assert {o.option_id for o in options} <= {b.id for b in TAXONOMY.buckets}
    offered = [o.summary for o in options]
    assert not [name for name in offered if TAXONOMY.is_too_coarse_as_source(name)]
    assert TAXONOMY.fallback.bucket not in {o.option_id for o in options}


def test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused(
    folder, silence, store
):
    """BELT AND BRACES, and the braces are what this drives. The offer filters the
    catch-alls out, so this state is reachable only through an item written by an
    older build or by hand. The write refuses it anyway rather than trusting that
    the offer upstream was the one that produced the item.
    """
    path = place(folder, silence, "track", CATCH_ALL)
    coarse = review.Option(option_id="coarse", summary=CATCH_ALL, detail={"genre": CATCH_ALL})
    item = review.offer(
        store,
        queue=review.Queue.GENRE,
        kind=retag.KIND,
        identity=retag.identity_for(path),
        payload={"path": str(path)},
        options=(coarse,),
        handler_key=retag.HANDLER_KEY,
    )
    review.resolve(store, item.item_id, review.Verdict.ACCEPTED, option="coarse",
                   actor="a-person")

    outcome = retag.retag_folder(
        folder, searcher=answering({}), declared=TAXONOMY, store=store
    )

    assert tags.read_genre_from_file(path) == CATCH_ALL
    assert [(r.reason, r.proposed) for r in outcome.results] == [
        (retag.ANSWER_TOO_COARSE, CATCH_ALL)
    ]


def test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question(
    folder, silence, store
):
    """A REJECTED item carries an item id, because the item is what settled it.

    So "has an id and was not written" counts a decision as a question, and a
    report built on it tells a person there is work waiting that they already
    did. This is the drive that separates the two, and the assertion on the
    written half is what stops it passing against a pass that reports nothing.
    """
    settled = place(folder, silence, "settled", CATCH_ALL)
    open_one = place(folder, silence, "open", CATCH_ALL)
    retag.retag_folder(folder, searcher=answering({}), declared=TAXONOMY, store=store)
    item = next(
        i
        for i in review.list_items(store, queue=str(review.Queue.GENRE)).items
        if i.payload["path"] == str(settled)
    )
    review.resolve(store, item.item_id, review.Verdict.REJECTED, actor="a-person")

    outcome = retag.retag_folder(
        folder, searcher=answering({}), declared=TAXONOMY, store=store
    )

    assert {r.path for r in outcome.asked} == {open_one}
    assert {r.path for r in outcome.results} == {settled, open_one}
    assert outcome.written == ()


def test_every_result_carries_a_reason_or_a_written_genre_and_never_both():
    """The invariant RetagResult's own docstring states, asserted over the type
    rather than left as prose. A result carrying both would let a report count one
    file twice, once as corrected and once as outstanding.
    """
    cases = (
        retag.RetagResult(path=Path("a"), current=CATCH_ALL, written=SPECIFIC),
        retag.RetagResult(path=Path("b"), current=CATCH_ALL, reason=retag.NO_ANSWER),
    )
    assert len(cases) == 2, "the case table is empty, so this proves nothing"
    for case in cases:
        assert bool(case.written) != bool(case.reason)


def test_the_item_id_this_pass_computes_is_the_one_the_queue_stores(folder, silence, store):
    """TWO COMPUTATIONS OF ONE FACT, held to agreeing.

    ``retag_folder`` derives an item id from ``review.item_id_for`` to look a
    verdict up, and ``review.offer`` derives it again from the same identity when
    it inserts. Both normalize the identity, and if that normalization ever
    diverged the pass would look up an id the queue does not hold and re-ask a
    settled question for ever, with the suite green because each half is correct
    on its own.
    """
    path = place(folder, silence, "track", CATCH_ALL)
    retag.retag_folder(folder, searcher=answering({}), declared=TAXONOMY, store=store)

    stored = review.list_items(store, queue=str(review.Queue.GENRE)).items[0]
    computed = review.item_id_for(review.Queue.GENRE, retag.KIND, retag.identity_for(path))

    assert stored.item_id == computed


def test_a_pass_with_no_store_reports_what_it_could_not_settle(folder, silence):
    """A pass driven without a queue reports the reason rather than pretending it
    settled the file. The result carries no item id, which is how a caller tells
    "asked" from "could not ask".
    """
    place(folder, silence, "track", CATCH_ALL)

    outcome = retag.retag_folder(folder, searcher=answering({}), declared=TAXONOMY)

    assert [(r.reason, r.item_id) for r in outcome.results] == [(retag.NO_ANSWER, "")]


def test_a_second_run_over_a_corrected_folder_selects_nothing(folder, silence, store):
    """THE UNIT'S OWN VERIFICATION STEP. Every state at once, then re-run."""
    correct = place(folder, silence, "correct", SPECIFIC)
    coarse = place(folder, silence, "coarse", CATCH_ALL)
    ambiguous = place(folder, silence, "ambiguous", CATCH_ALL)
    blank = place(folder, silence, "blank", None)
    tags.write_tags(coarse, {"title": "Answerable"})
    tags.write_tags(ambiguous, {"title": "Unanswerable"})

    first = retag.retag_folder(
        folder, searcher=answering({"Answerable": SPECIFIC}), declared=TAXONOMY, store=store
    )
    assert {r.path for r in first.written} == {coarse}
    assert {r.path for r in first.asked} == {ambiguous}
    assert {p.path for p in first.passed} == {correct, blank}

    second = retag.select(folder, declared=TAXONOMY)

    assert [c.path for c in second.candidates] == [ambiguous], (
        "the corrected file was selected again, so the pass is not idempotent; "
        "the only candidate left is the one still waiting on a person"
    )


# ═══════════════════════════════════════════════════════════════════════════
# C. The plan the gate is answered against
# ═══════════════════════════════════════════════════════════════════════════


def test_the_plan_digest_changes_when_the_selection_changes(folder, silence):
    """A person who approves forty files and then drops another hundred into the
    folder gets a stale decision rather than a wider sweep than they agreed to.
    """
    from cratekit.cli.output import digest_of

    place(folder, silence, "one", CATCH_ALL)
    before = digest_of({"items": retag.plan_items(retag.select(folder, declared=TAXONOMY))})
    place(folder, silence, "two", CATCH_ALL)
    after = digest_of({"items": retag.plan_items(retag.select(folder, declared=TAXONOMY))})

    assert before != after


def test_the_shell_digests_the_selection_and_the_folder_rather_than_a_constant(
    folder, silence, tmp_path
):
    """THE PROPERTY THAT WAS UNREACHABLE UNTIL THE PLAN CAME OUT OF THE HANDLER.

    Built inline, the digest could only be driven through a configured machine, a
    job store and a gate, so a mutation replacing it with a constant killed
    nothing. Both halves are asserted because both are decisions: the rows, so a
    person who approved forty files has not approved a hundred and forty, and the
    folder, so a decision recorded over one empty folder does not satisfy the gate
    for a different one.
    """
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
    items = retag.plan_items(retag.select(folder, declared=TAXONOMY))
    assert items == [{"path": str(folder / "one.flac"), "current": CATCH_ALL}]


# ═══════════════════════════════════════════════════════════════════════════
# D. The database half. First-caller drives of write.metadata.
# ═══════════════════════════════════════════════════════════════════════════


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


def test_a_written_file_is_relinked_to_the_existing_genre_row(tmp_path):
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    mapped = {"1": Row("1", GenreID=None)}
    db = FakeLookup([Row("7", Name=SPECIFIC, rb_local_deleted=0)])

    planned = retag.plan_library(
        written_outcome(path), rows, mapped, root=tmp_path, db=db
    )
    report = retag.apply_library(planned, mapped)

    assert planned.unmatched == ()
    assert report.written == ("1",)
    assert mapped["1"].GenreID == "7"


def test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader(tmp_path):
    """U59's first scenario, driven at the reader every shipped verb reaches.

    ``resolve_genre_id`` has its own rows in tests/test_metadata_policy.py, and
    those prove the FUNCTION. They do not prove the path, and the path is what
    the finding was about: this defect was dormant until U40 gave the function a
    caller a person can reach, through ``crate tag retag`` into
    ``plan_library`` into ``plan_genre_retag``. So the assertion belongs here,
    where the whole chain runs, and not only one layer down.

    The library has exactly one row named for this genre and rekordbox has
    already retired it. The honest answer is that the library has no active genre
    by that name, which is a per-row ``genre-unknown`` skip the user can act on.
    The answer this pins against is the row being linked anyway, which is a
    ``GenreID`` pointed at a tombstone with the run reporting success.
    """
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    mapped = {"1": Row("1", GenreID=None)}
    db = FakeLookup([Row("6", Name=SPECIFIC, rb_local_deleted=1)])

    planned = retag.plan_library(
        written_outcome(path), rows, mapped, root=tmp_path, db=db
    )
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
    """The control, and without it the row above is satisfied by refusing everything.

    "The first ACTIVE row wins rather than the first row" is the other half of
    the rule, and a reader that simply stopped at the first row would report "no
    such genre" for a genre the library plainly has. The tombstone is listed
    FIRST here on purpose, because that ordering is what makes the two
    implementations differ.
    """
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    mapped = {"1": Row("1", GenreID=None)}
    db = FakeLookup(
        [
            Row("6", Name=SPECIFIC, rb_local_deleted=1),
            Row("7", Name=SPECIFIC, rb_local_deleted=0),
        ]
    )

    planned = retag.plan_library(
        written_outcome(path), rows, mapped, root=tmp_path, db=db
    )
    retag.apply_library(planned, mapped)

    assert planned.plan.skipped == ()
    assert mapped["1"].GenreID == "7"


def test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row(tmp_path):
    """The refusal reaches a person through the shipped path, not just the unit.

    A binding that stops exposing the column is not a per-row problem and must
    not arrive as one. Collapsed into ``genre-unknown`` it would report a
    binding regression as thousands of skips naming the user's own taxonomy,
    sending them to fix a taxonomy that was never wrong. Driven here so that the
    distinction is proved to survive ``plan_library``, which is where it would be
    lost if a caller ever caught the refusal and continued.
    """
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    mapped = {"1": Row("1", GenreID=None)}
    db = FakeLookup([Row("6", Name=SPECIFIC)])

    with pytest.raises(CratekitError) as raised:
        retag.plan_library(written_outcome(path), rows, mapped, root=tmp_path, db=db)

    cause = raised.value.cause
    assert cause.reason == "soft-delete-marker-unreadable"
    assert cause.detail["genre"] == SPECIFIC
    # THE TRAIL IS THE HALF THAT ONLY THIS LAYER CAN PROVE. A cause arriving with
    # a one-element origin means a hop caught it and rebuilt it, which is exactly
    # how a run-scoped refusal would decay into a per-row skip somewhere between
    # the reader and the verb.
    assert cause.origin[0] == "write"
    assert mapped["1"].GenreID is None


def test_the_plan_is_built_from_what_was_written_and_never_from_the_selection(tmp_path):
    """The reporting half of the first-caller defect the corpus records.

    A plan built from the selection would name a row for a file whose write was
    refused, and the database would then disagree with the file on disk in the
    one direction nobody checks afterwards.
    """
    path = tmp_path / "track.flac"
    refused = retag.RetagOutcome(
        results=(
            retag.RetagResult(
                path=path, current=CATCH_ALL, reason=retag.ANSWER_TOO_COARSE
            ),
        )
    )
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    mapped = {"1": Row("1", GenreID=None)}
    db = FakeLookup([Row("7", Name=SPECIFIC, rb_local_deleted=0)])

    planned = retag.plan_library(refused, rows, mapped, root=tmp_path, db=db)
    retag.apply_library(planned, mapped)

    assert planned.plan.changes == ()
    # THE SKIP LIST IS THE ASSERTION THAT MATTERS, and asserting only the empty
    # change list is what let a mutation of this exact line survive. Planning from
    # the selection puts the refused row in the plan with its genre stringified
    # from None, the lookup for a genre named "None" resolves to nothing, and the
    # row comes back SKIPPED rather than changed. So the change list is empty for
    # the wrong reason and the weaker assertion holds for both implementations.
    assert planned.plan.skipped == (), (
        "the refused file reached the plan and was rejected by the genre lookup "
        "rather than never entering it, so the plan is built from the selection"
    )
    assert mapped["1"].GenreID is None


def test_a_soft_deleted_row_is_never_retagged(tmp_path):
    """``plan_genre_retag`` does not read the soft-delete marker, and it is right
    not to: three sibling planners in that module take the rows their caller
    chose. Choosing them is this caller's job, and the tombstone is dropped before
    the planner ever sees it.
    """
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=True)]
    mapped = {"1": Row("1", GenreID=None)}
    db = FakeLookup([Row("7", Name=SPECIFIC, rb_local_deleted=0)])

    planned = retag.plan_library(written_outcome(path), rows, mapped, root=tmp_path, db=db)
    retag.apply_library(planned, mapped)

    assert planned.plan.changes == ()
    assert [(u.path, u.outcome) for u in planned.unmatched] == [(str(path), "absent")]
    assert mapped["1"].GenreID is None


def test_a_genre_the_library_has_never_seen_is_skipped_and_surfaced(tmp_path):
    """``resolve_genre_id`` NEVER CREATES, so an answer this library has no lookup
    row for is a fact the person can act on rather than a fabricated row.
    """
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    mapped = {"1": Row("1", GenreID=None)}
    db = FakeLookup([Row("7", Name="Something Else", rb_local_deleted=0)])

    planned = retag.plan_library(written_outcome(path), rows, mapped, root=tmp_path, db=db)
    report = retag.apply_library(planned, mapped)

    assert [(s.reason, s.detail) for s in planned.plan.skipped] == [
        ("genre-unknown", SPECIFIC)
    ]
    assert report.written == ()
    assert mapped["1"].GenreID is None


def test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row(tmp_path):
    """Driven through this caller rather than only against the resolver, because
    the ordering only matters where a real lookup returns both.
    """
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    mapped = {"1": Row("1", GenreID=None)}
    db = FakeLookup(
        [
            Row("6", Name=SPECIFIC, rb_local_deleted=1),
            Row("7", Name=SPECIFIC, rb_local_deleted=0),
        ]
    )

    planned = retag.plan_library(written_outcome(path), rows, mapped, root=tmp_path, db=db)
    retag.apply_library(planned, mapped)

    assert mapped["1"].GenreID == "7"


def test_a_written_file_no_live_row_claims_is_surfaced_rather_than_dropped(tmp_path):
    """The file is already corrected on disk, so silence here would report a full
    sweep over a library half of which never moved.
    """
    path = tmp_path / "track.flac"
    db = FakeLookup([Row("7", Name=SPECIFIC, rb_local_deleted=0)])

    planned = retag.plan_library(written_outcome(path), [], {}, root=tmp_path, db=db)

    assert planned.plan.changes == ()
    assert [(u.path, u.outcome) for u in planned.unmatched] == [(str(path), "absent")]


def test_two_live_rows_on_one_location_are_surfaced_rather_than_written_to_both(tmp_path):
    """An import that ran twice against a renamed volume leaves two live rows for
    one file. Writing the genre to both puts one track in the tree twice under two
    identities, which the person then cannot correct by correcting it once.
    """
    path = tmp_path / "track.flac"
    rows = [
        trees.ContentRow(content_id="1", recorded=str(path), deleted=False),
        trees.ContentRow(content_id="2", recorded=str(path), deleted=False),
    ]
    mapped = {"1": Row("1", GenreID=None), "2": Row("2", GenreID=None)}
    db = FakeLookup([Row("7", Name=SPECIFIC, rb_local_deleted=0)])

    planned = retag.plan_library(written_outcome(path), rows, mapped, root=tmp_path, db=db)
    retag.apply_library(planned, mapped)

    assert planned.plan.changes == ()
    assert [(u.outcome, u.content_ids) for u in planned.unmatched] == [
        ("ambiguous", ("1", "2"))
    ]
    assert mapped["1"].GenreID is None and mapped["2"].GenreID is None


def test_two_written_files_resolving_to_one_row_are_both_surfaced_and_neither_wins(
    tmp_path,
):
    """The mirror of the ambiguous case, and the one a dictionary hides.

    Keying on the content id and moving on would let whichever file came last
    decide the row while the report named both as written.

    THE PRODUCER IS UNICODE COMPOSITION, NOT A CONTRIVANCE. Two filenames that
    differ only in whether the accent is one codepoint or two are two different
    files to ``rglob`` and one location to ``locations.norm_for_compare``, which
    folds both to NFC on purpose. That folding is what this repository's own
    "144 files with accented names went missing" incident bought.

    WHAT IS NOT DRIVEN HERE, said rather than left implied: a folder actually
    holding both forms at once. This function takes values and touches no
    filesystem, so the collision is handed to it directly. Whether macOS will let
    a person create both files side by side is unmeasured, and the guard is
    cheap enough that it is worth holding either way.
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
    db = FakeLookup(
        [
            Row("7", Name=SPECIFIC, rb_local_deleted=0),
            Row("8", Name="Techno", rb_local_deleted=0),
        ]
    )

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
    """``write_plan`` surfaces a row it was not handed, and this asserts the plan
    says so too. Two answers about one absent row would eventually disagree.
    """
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    db = FakeLookup([Row("7", Name=SPECIFIC, rb_local_deleted=0)])

    planned = retag.plan_library(written_outcome(path), rows, {}, root=tmp_path, db=db)

    assert planned.plan.changes == ()
    assert [(s.content_id, s.reason) for s in planned.plan.skipped] == [("1", "row-absent")]


def test_the_apply_refuses_a_field_the_retag_policy_does_not_own(tmp_path):
    """The plan's seventh scenario. ``assert_within_policy`` exists because
    harmless is not the same as correct: a sweep that silently writes nothing
    looks exactly like a sweep with nothing to do.
    """
    del tmp_path
    foreign = metadata.Plan(
        metadata.RETAG_GENRE,
        (metadata.Change("1", metadata.RETAG_GENRE, "Rating", None, 4),),
    )

    with pytest.raises(CratekitError) as excinfo:
        retag.apply_library(retag.LibraryPlan(plan=foreign), {"1": Row("1", Rating=None)})

    assert excinfo.value.cause.reason == "refused-by-policy"
    assert "Rating" in excinfo.value.cause.message


def test_an_unregistered_operation_writes_nothing_and_the_apply_is_what_prevents_it(
    tmp_path,
):
    """THE FIRST-CALLER HOLE, DRIVEN IN BOTH DIRECTIONS.

    ``metadata_decision`` answers SKIP_UNOWNED for an operation nobody registered.
    So a caller that built a correct plan and applied it without enabling first
    would write nothing, raise nothing, and report a clean run. The first half
    below drives exactly that state; the second half shows that going through
    ``apply_library`` is what turns it into a write. Asserting only the second
    half would pass against a build where ``enable`` had been deleted, because the
    registry is process-wide and some earlier test would have set it.
    """
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    db = FakeLookup([Row("7", Name=SPECIFIC, rb_local_deleted=0)])

    unregistered = {"1": Row("1", GenreID=None)}
    planned = retag.plan_library(
        written_outcome(path), rows, unregistered, root=tmp_path, db=db
    )
    rb_writer.reset_field_policies()
    bare = metadata.write_plan(planned.plan, unregistered)
    assert bare.totals["skip_unowned"] == 1
    assert bare.written == ()
    assert unregistered["1"].GenreID is None

    rb_writer.reset_field_policies()
    guarded = {"1": Row("1", GenreID=None)}
    planned = retag.plan_library(
        written_outcome(path), rows, guarded, root=tmp_path, db=db
    )
    report = retag.apply_library(planned, guarded)
    assert report.written == ("1",)
    assert guarded["1"].GenreID == "7"


def test_re_applying_a_plan_over_an_already_linked_row_is_a_no_op(tmp_path):
    """Idempotence at the database end, which is a property of the DECISION rather
    than of the selection: the same value twice reports skip_same.
    """
    path = tmp_path / "track.flac"
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    mapped = {"1": Row("1", GenreID="7")}
    db = FakeLookup([Row("7", Name=SPECIFIC, rb_local_deleted=0)])

    planned = retag.plan_library(written_outcome(path), rows, mapped, root=tmp_path, db=db)
    report = retag.apply_library(planned, mapped)

    assert report.totals["skip_same"] == 1
    assert report.written == ()


def test_the_retag_operation_owns_the_genre_column_and_nothing_else():
    """The policy this unit is the first caller of, asserted where its caller is,
    so widening it later fails here as well as in the policy suite.
    """
    policy = metadata.OPERATIONS[metadata.RETAG_GENRE]
    assert dict(policy.fields) == {"GenreID": rb_writer.Ownership.OWNED}


# ═══════════════════════════════════════════════════════════════════════════
# E. The shell
# ═══════════════════════════════════════════════════════════════════════════


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
    """THE BRANCH THIS SUITE DID NOT DRIVE UNTIL A POPULATION PIN REPORTED IT.

    ``cause.refuse`` raises ``UnknownReason`` for a slug the registry does not
    declare, so this branch raised a KeyError at the boundary instead of refusing,
    and every test here passed because none of them typed an empty folder. The
    parser accepts it, since an empty string is a valid argument to a positional
    that takes one, so the branch is reachable by a person.
    """
    from cratekit.core.exit_codes import ExitCode
    from cratekit.tagging import retag_cli

    class _Ctx:
        pass

    ctx = _Ctx()
    ctx.args = type("A", (), {"folder": "", "job": None})()

    with pytest.raises(CratekitError) as excinfo:
        retag_cli.retag_genres(ctx)

    cause = excinfo.value.cause
    assert cause.reason == "tag-retag-folder-unknown"
    assert cause.code is ExitCode.PRECONDITION, (
        "the argument parser accepted this invocation, so status 2 is not this "
        "refusal's, and a destructive verb refusing is not a defect in the program"
    )


def test_the_handler_finds_its_gate_by_digest_source_and_not_by_position():
    """Indexing ``gates[0]`` would silently answer the wrong question the day the
    tuple is reordered, and the cloud-sync gate sitting beside the confirm is
    exactly such a neighbour.
    """
    from cratekit.cli import registry
    from cratekit.tagging import retag_cli

    entry = registry.entry("tag.retag")
    reordered = type(entry.gates)(reversed(entry.gates))

    class _Ctx:
        pass

    ctx = _Ctx()
    ctx.entry = type("E", (), {"gates": reordered, "name": "tag.retag"})()

    assert retag_cli._plan_gate(ctx).name == "tag.retag.confirm"


def test_the_handler_refuses_when_its_entry_declares_no_plan_gate():
    """A registry edit that dropped the confirmation would otherwise run a
    destructive sweep with nobody asked, and the conformance suite's reach check
    reads the registry rather than this handler.
    """
    from cratekit.tagging import retag_cli

    class _Ctx:
        pass

    ctx = _Ctx()
    ctx.entry = type("E", (), {"gates": (), "name": "tag.retag"})()

    with pytest.raises(CratekitError) as excinfo:
        retag_cli._plan_gate(ctx)
    assert excinfo.value.cause.reason == "refused-by-policy"


def test_the_frozen_rows_digest_the_same_after_the_folder_has_moved_under_them(
    folder, silence
):
    """KTD8 and R13, asserted on the function rather than through the dispatcher.

    THE STALL THIS SPLIT CLOSES. ``plan_for`` walks the folder, so the digest it
    returns describes the folder AS IT STANDS. That was stable only while nothing
    wrote: a corrected file carries a specific genre, the selection shrinks, and
    the plan digests differently from the one the confirmation was recorded
    against, so every resume after the first partial run meets ``DecisionStale``
    for ever. Driven end to end in ``tests/test_tag_workers.py``; measured here on
    the two functions, because this is the only place the property can be stated
    without a job store and a gate.

    THE THIRD DIGEST IS WHAT MAKES THE OTHER TWO MEAN ANYTHING. Without it, a
    ``digest_for`` that ignored its rows entirely would satisfy the first two
    assertions perfectly.
    """
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
    assert (
        retag_cli.digest_for(str(folder), confirmed["items"]) == confirmed["digest"]
    ), "the frozen rows no longer digest as the plan they were frozen from"
    assert (
        retag_cli.digest_for(str(folder), walked_again["items"]) != confirmed["digest"]
    )


def test_the_frozen_rows_survive_the_json_the_payload_is_stored_as(folder, silence):
    """The payload is JSON on disk, and the digest is compared across that trip.

    The rows go into the job payload, which ``core.jobs`` serializes, so the
    resume digests values that have been through a text encoding rather than the
    objects the plan built. A digest taken over anything that does not survive
    that trip refuses a decision nobody changed.
    """
    import json

    from cratekit.tagging import retag_cli

    place(folder, silence, "one", CATCH_ALL)
    confirmed = retag_cli.plan_for(str(folder), TAXONOMY)

    round_tripped = json.loads(json.dumps({"items": confirmed["items"]}))["items"]

    assert retag_cli.digest_for(str(folder), round_tripped) == confirmed["digest"]


def test_two_different_empty_folders_digest_differently_through_the_pure_function(
    tmp_path,
):
    """The property the split had to carry down with it, stated where it now lives.

    Two different empty folders are two different decisions: approving a sweep of
    one is not approving a sweep of the other. The test above this asserts it
    through ``plan_for``, which walks; this asserts it on the function the resume
    calls, which cannot walk and would otherwise be free to lose the folder.
    """
    from cratekit.tagging import retag_cli

    assert retag_cli.digest_for(str(tmp_path / "EmptyOne"), []) != retag_cli.digest_for(
        str(tmp_path / "EmptyTwo"), []
    )
