"""U294: ``crate tag campaign`` applies the needs genre backlog under one gate.

Three layers, in the order they are trusted. The rules, pure: narrowing a made
plan to the rows a campaign may write, an answer checked against the plan, and
the one digest. Then the verb through the real dispatcher on a disposable
database and real tagged containers, the ``tag backlog`` suite's fixtures: the
two acts R34 requires, every step through its verb's own apply path, needs
genre before and after, a step's refusal stopping the campaign with the
earlier steps' writes intact and named, and a second run planning only what is
left. Catalogue answers are recorded, never asked of the network.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import sqlite3
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType

import pytest

from cratekit.cli.verbs import tag_campaign
from cratekit.core import active_taxonomy, config, rb_writer, tags
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import backlog, rows, suggest
from cratekit.tagging.tag import SearchHit
from cratekit.write import metadata
from tests import test_tag_backlog as _backlog_suite
from tests import test_tag_suggest as _suggest_suite
from tests.cli_drive import drive, drive_human
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414

machine = _backlog_suite.machine
acknowledged = _suggest_suite.acknowledged
silence = _backlog_suite.silence
_release_process_locks = _backlog_suite._release_process_locks
_field_policies = _backlog_suite._field_policies
_reader_cache = _backlog_suite._reader_cache
_platform_seams = _backlog_suite._platform_seams
_lookups = _backlog_suite._lookups
_active_copy = _backlog_suite._active_copy

Track = _backlog_suite.Track
build = _backlog_suite.build
_library = _backlog_suite._library
_planned = _backlog_suite._planned
_census_needing = _backlog_suite._census_needing
_tree = _backlog_suite._tree
_genre_of = _suggest_suite._genre_of
_content = _suggest_suite._content

VERB = ["tag", "campaign"]
GATE = tag_campaign.CONFIRM_GATE

MELODIC = _backlog_suite.MELODIC
DEEP = _backlog_suite.DEEP
INDIE = _backlog_suite.INDIE
GRIME = _backlog_suite.GRIME
MPB = _backlog_suite.MPB
RNB = _backlog_suite.RNB
ALTERNATIVE = _backlog_suite.ALTERNATIVE

#: The answer the backlog suite's library recommends for its one asked word.
INDIE_ALIAS = f"{INDIE}={MELODIC}"


def _first_act(argv: list[str]) -> tuple[str, dict]:
    code, refused = drive([*VERB, *argv])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE
    return refused["run_id"], refused


def _decide(run_id: str, answer: str = "apply") -> None:
    decided, envelope = drive(["run", "decide", run_id, GATE, answer, "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope


def _two_acts(argv: list[str] = ()) -> tuple[int, dict, dict]:
    run_id, refused = _first_act(list(argv))
    _decide(run_id)
    code, acted = drive(["--run", run_id, *VERB, *argv])
    return code, acted, refused


def _steps(envelope: dict) -> dict[str, dict]:
    return {step["step"]: step for step in envelope["data"]["totals"]["steps"]}


def _tempo(cfg: config.Config, paths) -> dict[str, object]:
    """Every row's BPM column and every file's tags but its genre, for the beat
    grid rule: a written file moved its genre and nothing else."""
    import mutagen

    connection = sqlite3.connect(cfg.library.db_path)
    try:
        found: dict[str, object] = {
            f"row {content_id}": bpm
            for content_id, bpm in connection.execute("SELECT ID, BPM FROM djmdContent")
        }
    finally:
        connection.close()
    for content_id, path in paths.items():
        if path.exists():
            held = mutagen.File(path).tags
            found[f"file {content_id}"] = sorted(
                (key.lower(), tuple(values)) for key, values in held.as_dict().items()
                if key.lower() != "genre"
            )
    return found


# ═══════════════════════════════════════════════════════════════════════════
# 1. The rules
# ═══════════════════════════════════════════════════════════════════════════


def _rows_plan() -> rows.RowsPlan:
    items = (
        rows.Item("1", "a", "", MELODIC, rows.WRITE, genre_id="100"),
        rows.Item("2", "b", MELODIC, INDIE, rows.WRITE, genre_id="105"),
        rows.Item("3", "c", "", COARSE_WORD, rows.LEAVE, reason=rows.FILE_TOO_COARSE),
    )
    counts = dict.fromkeys(rows.OUTCOMES, 0)
    counts.update({rows.WRITE: 2, rows.FILE_TOO_COARSE: 1, rows.AGREE: 4})
    changes = metadata.Plan(
        owner="tag-rows",
        changes=(
            metadata.Change("1", "tag-rows", "content.genre", "", "100"),
            metadata.Change("2", "tag-rows", "content.genre", "", "105"),
        ),
    )
    return rows.RowsPlan(items=items, counts=MappingProxyType(counts), changes=changes)


COARSE_WORD = _backlog_suite.COARSE


def test_a_rows_plan_narrowed_writes_only_the_rows_kept_and_holds_the_rest_out():
    narrowed = rows.narrowed(_rows_plan(), {"1"})
    assert [item.content_id for item in narrowed.writes] == ["1"]
    held = next(item for item in narrowed.items if item.content_id == "2")
    assert (held.action, held.reason, held.genre_id) == (rows.LEAVE, rows.HELD_OUT, "")
    assert [change.content_id for change in narrowed.changes.changes] == ["1"]
    assert narrowed.counts[rows.WRITE] == 1 and narrowed.counts[rows.HELD_OUT] == 1
    # Every live row is still counted once, and the other outcomes stand.
    assert narrowed.rows == _rows_plan().rows and narrowed.counts[rows.AGREE] == 4


def test_a_rows_plan_narrowed_to_nothing_writes_nothing():
    narrowed = rows.narrowed(_rows_plan(), ())
    assert narrowed.writes == () and narrowed.changes.changes == ()


def _suggest_plan() -> suggest.SuggestPlan:
    def item(content_id: str, genre: str) -> suggest.Item:
        return suggest.Item(
            content_id, "p", "", "", genre, suggest.HIGH, (genre,), ((genre, 18),), None,
            suggest.WRITE, genre_id="100",
        )

    counts = dict.fromkeys(suggest.OUTCOMES, 0)
    counts[suggest.WRITE] = 3
    return suggest.SuggestPlan(
        items=(item("1", MELODIC), item("2", DEEP), item("3", MELODIC)),
        counts=MappingProxyType(counts),
        changes=metadata.Plan(
            owner="tag-suggest",
            changes=tuple(
                metadata.Change(content_id, "tag-suggest", "content.genre", "", "100")
                for content_id in ("1", "2", "3")
            ),
        ),
        band=suggest.HIGH,
        catalogue=False,
    )


def test_a_suggest_plan_narrowed_writes_a_row_only_with_the_genre_approved():
    narrowed = suggest.narrowed(_suggest_plan(), {"1": MELODIC, "2": MELODIC})
    assert [item.content_id for item in narrowed.writes] == ["1"]
    # Row 2's suggestion moved since the approval, and row 3 was never approved.
    for content_id in ("2", "3"):
        held = next(item for item in narrowed.items if item.content_id == content_id)
        assert (held.action, held.reason) == (suggest.LEAVE, suggest.HELD_OUT)
    assert [change.content_id for change in narrowed.changes.changes] == ["1"]
    assert narrowed.counts[suggest.WRITE] == 1 and narrowed.counts[suggest.HELD_OUT] == 2


def _word(spelling: str, *, options=True, settled: str = "", unanswerable=None) -> backlog.Word:
    return backlog.Word(
        word=spelling,
        rows=2,
        spellings=((spelling, 2),),
        files_carry=2,
        several=0,
        elsewhere=0,
        on_row=0,
        neighbours=(),
        options=(
            (backlog.Option(backlog.LEAVE, "Leave it", "", "", 0),) if options else ()
        ),
        settled=settled,
        unanswerable=unanswerable,
    )


def _backlog(*words: backlog.Word, rows_=()) -> backlog.Backlog:
    return backlog.Backlog(rows=tuple(rows_), words=words, tracks=10, catalogue=False)


def test_an_answer_names_its_word_in_any_case_and_carries_the_plans_spelling():
    plan = _backlog(_word(INDIE), _word(GRIME))
    found = tag_campaign.answers(
        plan, alias=[f"indie tech={MELODIC}"], folder=[GRIME], leave_word=[]
    )
    assert [(answer.word, answer.answer, answer.genre) for answer in found] == [
        (INDIE, backlog.ALIAS, MELODIC),
        (GRIME, backlog.FOLDER, ""),
    ]


@pytest.mark.parametrize(
    ("alias", "folder", "leave_word", "said"),
    [
        (["Gqom=Deep House"], [], [], "names no word"),
        ([], ["Gqom"], [], "names no word"),
        ([], [], ["Gqom"], "names no word"),
        ([f"{INDIE}"], [], [], "is not WORD=GENRE"),
        ([f"{INDIE}="], [], [], "is not WORD=GENRE"),
        ([INDIE_ALIAS], [INDIE], [], "answered twice"),
        ([], [INDIE], ["indie tech"], "answered twice"),
        ([], [MPB], [], "already has its one answer"),
        ([], [ALTERNATIVE], [], "cannot be answered"),
    ],
)
def test_an_answer_the_plan_does_not_hold_refuses(alias, folder, leave_word, said):
    plan = _backlog(
        _word(INDIE),
        _word(MPB, options=False, settled=f"crate taxonomy alias {MPB} 'R&B'"),
        _word(ALTERNATIVE, options=False, unanswerable=("x", "no answer", "by hand")),
    )
    with pytest.raises(Exception) as raised:
        tag_campaign.answers(plan, alias=alias, folder=folder, leave_word=leave_word)
    cause = raised.value.cause
    assert cause.reason == "review-selection-invalid" and said in cause.message


def _proposed(content_id: str, genre: str = MELODIC, path: str = "p") -> backlog.Row:
    return backlog.Row(
        content_id, path, "", "", "", "", backlog.NO_GENRE, "", backlog.PROPOSED,
        verb=backlog.SUGGEST_VERB,
        proposal=backlog.Proposal(genre, suggest.HIGH, 1.0, backlog.NEIGHBOURS, "", ((genre, 18),)),
    )


def test_the_digest_moves_with_an_answer_a_proposal_or_a_row():
    plan = _backlog(_word(INDIE), rows_=[_proposed("1")])
    alias = tag_campaign.Answer(INDIE, backlog.ALIAS, MELODIC)
    base = tag_campaign.digest(plan, (alias,))
    assert tag_campaign.digest(plan, (alias,)) == base
    assert tag_campaign.digest(plan, (replace(alias, genre=DEEP),)) != base
    assert tag_campaign.digest(plan, (tag_campaign.Answer(INDIE, backlog.FOLDER, ""),)) != base
    assert tag_campaign.digest(plan, ()) != base
    moved = _backlog(_word(INDIE), rows_=[_proposed("1", DEEP)])
    assert tag_campaign.digest(moved, (alias,)) != base
    more = _backlog(_word(INDIE), rows_=[_proposed("1"), _proposed("2")])
    assert tag_campaign.digest(more, (alias,)) != base
    asked = replace(plan, catalogue=True)
    assert tag_campaign.digest(asked, (alias,)) != base


def test_the_digest_names_no_copy():
    """A rehearsal on a disposable copy reads every path somewhere else."""
    here = _backlog(_word(INDIE), rows_=[_proposed("1", path="/one/copy/a.flac")])
    there = _backlog(_word(INDIE), rows_=[_proposed("1", path="/another/copy/a.flac")])
    answer = (tag_campaign.Answer(INDIE, backlog.ALIAS, MELODIC),)
    assert tag_campaign.digest(here, answer) == tag_campaign.digest(there, answer)


def test_the_answer_order_on_the_command_line_does_not_move_the_digest():
    plan = _backlog(_word(INDIE), _word(GRIME))
    one = tag_campaign.answers(plan, alias=[INDIE_ALIAS], folder=[GRIME], leave_word=[])
    two = tag_campaign.answers(plan, alias=[INDIE_ALIAS], folder=[GRIME.lower()], leave_word=[])
    assert tag_campaign.digest(plan, one) == tag_campaign.digest(plan, two)


# ═══════════════════════════════════════════════════════════════════════════
# 2. The campaign through the dispatcher
# ═══════════════════════════════════════════════════════════════════════════


def test_the_whole_campaign_lands_and_needs_genre_falls_as_measured(acknowledged, silence):
    cfg = acknowledged
    paths = build(cfg, silence, *_library())
    tempo = _tempo(cfg, paths)
    before = _census_needing(cfg)
    assert len(before) == 11

    code, acted, refused = _two_acts(["--alias", INDIE_ALIAS])

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["digest"] == acted["data"]["digest"]
    assert shown["needs_genre"] == 11
    # Step one, tag rows: the row lagging its file.
    assert _genre_of(cfg, "10") == MELODIC
    # Step two, tag suggest at the floor: the row among eight agreeing tracks.
    assert _genre_of(cfg, "12") == MELODIC
    assert tags.read_genre_from_file(paths["12"]) == MELODIC
    # Step three: the settled word's one answer, then the answered word.
    assert tags.read_genre_from_file(paths["41"]) == RNB
    assert tags.read_genre_from_file(paths["15"]) == MELODIC
    assert tags.read_genre_from_file(paths["16"]) == MELODIC
    assert active_taxonomy.load(cfg).tagging_alias(INDIE.lower()) is not None
    # Step four, tag rows again: the rows follow their retagged files.
    assert _genre_of(cfg, "41") == RNB
    assert _genre_of(cfg, "15") == MELODIC and _genre_of(cfg, "16") == MELODIC
    # Left by hand: no lookup row, nothing beside it, a catch all, a row only
    # word, a word neither verb takes, and an alias to a genre with no entry.
    for content_id in ("11", "13", "14", "17", "18", "42"):
        assert content_id in _census_needing(cfg), content_id

    after = _census_needing(cfg)
    assert after == before - {"10", "12", "41", "15", "16"}
    needs = acted["data"]["totals"]["needs_genre"]
    assert (needs["before"], needs["after"]) == (11, 6)
    steps = _steps(acted)
    assert [step["state"] for step in steps.values()] == [tag_campaign.LANDED] * 4 + [
        tag_campaign.NEXT
    ]
    assert steps["rows"]["written"] == 1 and steps["rows"]["needs_genre_after"] == 10
    assert steps["suggest"]["written"] == 1 and steps["suggest"]["needs_genre_after"] == 9
    assert steps["words"]["files"] == 3 and steps["words"]["needs_genre_after"] == 9
    assert steps["follow"]["written"] == 3 and steps["follow"]["needs_genre_after"] == 6
    assert steps["follow"]["moved"] == [] and steps["rows"]["moved"] == []
    assert steps["resort"]["command"] == backlog.RESORT_VERB
    codes = [warning["code"] for warning in acted["warnings"]]
    assert tag_campaign.RESORT_NEXT in codes and tag_campaign.REMAINDER in codes
    # NEVER A BEAT GRID: no BPM column and no tempo tag moved anywhere.
    assert _tempo(cfg, paths) == tempo


def test_only_the_genre_column_moves_on_a_written_row(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, *_library())
    before = _content(cfg)
    code, acted, _refused = _two_acts(["--alias", INDIE_ALIAS])
    assert code == int(ExitCode.OK), acted
    after = _content(cfg)
    written = {"10", "12", "41", "15", "16"}
    for content_id, was in before.items():
        moved = {
            column
            for column, value in after[content_id].items()
            if value != was[column] and column not in rb_writer.BOOKKEEPING_COLUMNS
        }
        assert moved == ({"GenreID"} if content_id in written else set()), content_id


def test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files(acknowledged, silence):
    cfg = acknowledged
    paths = build(cfg, silence, *_library())
    code, acted, _refused = _two_acts(["--folder", INDIE])
    assert code == int(ExitCode.OK), acted
    declared = active_taxonomy.load(cfg)
    assert any(bucket.display == INDIE for bucket in declared.buckets)
    # The files are not rewritten; the row whose file carries the word follows,
    # and the one carrying another case stays, since the library has no genre
    # row for that spelling and tag rows links one and never makes one.
    assert tags.read_genre_from_file(paths["15"]) == INDIE
    assert _genre_of(cfg, "15") == INDIE and _genre_of(cfg, "16") == ""
    needing = _census_needing(cfg)
    assert "16" in needing and not {"15", "17"} & needing
    # Measured on the copy the folder answer wrote, the row it filed included.
    steps = _steps(acted)
    assert steps["follow"]["needs_genre_after"] == len(needing)
    # Row 17 is filed by the folder at the words step; rows 15 and 41 follow.
    assert steps["words"]["needs_genre_after"] == len(needing) + 2
    assert _steps(acted)["follow"]["left"] == {"16": rows.GENRE_UNKNOWN}
    (said,) = [w for w in acted["warnings"] if w["code"] == tag_campaign.ROWS_LEFT]
    assert "1 genre-unknown" in said["message"] and "16" in said["message"]


def test_a_word_left_or_unanswered_is_named_and_nothing_retags_it(acknowledged, silence):
    cfg = acknowledged
    paths = build(cfg, silence, *_library())
    code, acted, refused = _two_acts(["--leave-word", INDIE])
    assert code == int(ExitCode.OK), acted
    assert tags.read_genre_from_file(paths["15"]) == INDIE and _genre_of(cfg, "15") == ""
    assert {"15", "16", "17"} <= _census_needing(cfg)
    answered = {item["word"]: item for item in refused["cause"]["detail"]["shown"]["answers"]}
    assert answered[INDIE]["answer"] == backlog.LEAVE


def test_rows_joining_needs_genre_and_any_other_routed_row_are_never_written(
    acknowledged, silence
):
    """R-1734: tag rows would give row 70 a word no folder takes, and row 72 is
    a routed row whose file carries another routed genre. The campaign writes
    only the rows the backlog named."""
    cfg = acknowledged
    build(
        cfg,
        silence,
        Track("70", MELODIC, INDIE),
        Track("72", DEEP, MELODIC),
        Track("71", "", MELODIC),
    )
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    assert _genre_of(cfg, "71") == MELODIC
    assert _genre_of(cfg, "70") == MELODIC and _genre_of(cfg, "72") == DEEP
    assert "70" not in _census_needing(cfg)
    assert _steps(acted)["rows"]["held"] == 2


def test_a_proposal_that_appears_after_the_first_step_is_left_for_the_next_run(
    acknowledged, silence
):
    """R-1732: row 30 had no proposal when the gate was answered, and the first
    step's rows gave it one. It was never shown, so it is left and named."""
    cfg = acknowledged
    build(
        cfg,
        silence,
        Track("30", "", "", artist="The Artist", folder="one"),
        *[Track(str(31 + n), INDIE, DEEP, artist="The Artist", folder="one") for n in range(9)],
        Track("40", MELODIC, MELODIC, artist="The Artist", folder="one"),
    )
    assert _planned(cfg).proposals == ()
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    assert _genre_of(cfg, "30") == "" and _genre_of(cfg, "31") == DEEP
    suggested = _steps(acted)["suggest"]
    assert suggested["written"] == 0 and suggested["moved"] == ["30"]
    assert tag_campaign.MOVED in {warning["code"] for warning in acted["warnings"]}

    # A second run plans only what is left, and the proposal is shown there.
    run_id, refused = _first_act([])
    (item,) = [
        item for item in refused["cause"]["detail"]["shown"]["items"] if item["kind"] == "suggest"
    ]
    assert (item["content_id"], item["genre"]) == ("30", DEEP)


def test_an_answer_the_plan_does_not_hold_refuses_before_anything_is_written(
    acknowledged, silence
):
    cfg = acknowledged
    build(cfg, silence, *_library())
    before = _tree(cfg)
    code, refused = drive([*VERB, "--alias", "Gqom=Deep House"])
    assert code != int(ExitCode.OK) and refused["cause"]["reason"] == "review-selection-invalid"
    assert "gate" not in (refused["cause"].get("detail") or {})
    assert _tree(cfg) == before


def test_an_alias_to_a_genre_the_alias_verb_refuses_refuses_before_the_gate(
    acknowledged, silence
):
    cfg = acknowledged
    build(cfg, silence, *_library())
    before = _tree(cfg)
    code, refused = drive([*VERB, "--alias", f"{INDIE}=No Such Genre"])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "taxonomy-genre-unknown"
    assert _tree(cfg) == before


def test_a_row_that_changes_after_the_gate_refuses_as_stale_with_nothing_written(
    acknowledged, silence
):
    cfg = acknowledged
    paths = build(cfg, silence, *_library())
    run_id, _refused = _first_act([])
    _decide(run_id)
    assert tags.write_tags(paths["13"], {"genre": DEEP})
    before = _tree(cfg)
    code, stale = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_STALE), stale
    assert _tree(cfg) == before


def test_an_answer_that_changes_after_the_gate_refuses_as_stale(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, *_library())
    run_id, _refused = _first_act(["--alias", INDIE_ALIAS])
    _decide(run_id)
    before = _tree(cfg)
    code, stale = drive(["--run", run_id, *VERB, "--folder", INDIE])
    assert code == int(ExitCode.DECISION_STALE), stale
    assert _tree(cfg) == before


def test_a_declined_campaign_writes_nothing(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, *_library())
    before = _tree(cfg)
    run_id, _refused = _first_act([])
    _decide(run_id, "abort")
    code, declined = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK) and declined["outcome"] == "no_op", declined
    assert _tree(cfg) == before


def test_the_gate_takes_no_inline_answer(acknowledged, silence):
    build(acknowledged, silence, *_library())
    code, refused = drive(["-d", f"{GATE}=apply", *VERB])
    assert code == int(ExitCode.DECISION_REQUIRED), refused


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine, silence):
    build(machine, silence, *_library())
    before = _tree(machine)
    code, envelope = drive(VERB)
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "backup-acknowledgment-missing"
    assert _tree(machine) == before


def test_an_empty_backlog_still_asks_and_writes_nothing(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, *_backlog_suite._eight())
    before = _tree(cfg)
    code, acted, refused = _two_acts()
    assert code == int(ExitCode.OK) and acted["outcome"] == "no_op", acted
    assert tag_campaign.NOTHING in {warning["code"] for warning in acted["warnings"]}
    assert _tree(cfg) == before


# ═══════════════════════════════════════════════════════════════════════════
# 3. The stop
# ═══════════════════════════════════════════════════════════════════════════


def test_a_step_that_refuses_stops_the_campaign_with_the_earlier_writes_named(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    paths = build(cfg, silence, *_library())
    run_id, _refused = _first_act(["--alias", INDIE_ALIAS])
    _decide(run_id)

    real = tags.write_genre

    def stuck(path, genre):
        return False

    monkeypatch.setattr(tags, "write_genre", stuck)
    code, stopped = drive(["--run", run_id, *VERB, "--alias", INDIE_ALIAS])
    assert code != int(ExitCode.OK), stopped
    cause = stopped["cause"]
    # The step's own refusal, worded with what landed and what did not run.
    assert cause["reason"] == "tag-suggest-unwritten"
    assert "crate tag rows landed, 1 row(s)" in cause["message"]
    assert "not run: the words, tag rows again, route resort" in cause["message"]
    states = {step["step"]: step["state"] for step in cause["detail"]["campaign"]["steps"]}
    assert states == {
        "rows": tag_campaign.LANDED,
        "suggest": tag_campaign.REFUSED,
        "words": tag_campaign.NOT_RUN,
        "follow": tag_campaign.NOT_RUN,
        "resort": tag_campaign.NOT_RUN,
    }
    # The first step's write is intact; nothing after the refusal was written.
    assert _genre_of(cfg, "10") == MELODIC
    assert tags.read_genre_from_file(paths["15"]) == INDIE
    assert active_taxonomy.load(cfg).tagging_alias(INDIE.lower()) is None

    # A second run plans only what is left, with the writer working again.
    monkeypatch.setattr(tags, "write_genre", real)
    _run, refused = _first_act(["--alias", INDIE_ALIAS])
    shown = {item.get("content_id") for item in refused["cause"]["detail"]["shown"]["items"]}
    assert "10" not in shown and "12" in shown


def test_a_first_step_that_refuses_writes_nothing_and_runs_nothing_after(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    build(cfg, silence, *_library())
    run_id, _refused = _first_act(["--alias", INDIE_ALIAS])
    _decide(run_id)
    before = _tree(cfg)
    real = rb_writer.open_db

    def running(path, *args, require_closed=False, **kwargs):
        if require_closed:
            raise refuse("rekordbox-running", "rekordbox is running", origin=("test",))
        return real(path, *args, require_closed=require_closed, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", running)
    code, stopped = drive(["--run", run_id, *VERB, "--alias", INDIE_ALIAS])
    assert code != int(ExitCode.OK) and stopped["cause"]["reason"] == "rekordbox-running"
    assert "no step landed" in stopped["cause"]["message"]
    assert _tree(cfg) == before


# ═══════════════════════════════════════════════════════════════════════════
# 4. The catalogue, recorded
# ═══════════════════════════════════════════════════════════════════════════


def test_a_recorded_catalogue_proposal_is_written_and_asked_once_across_the_acts(
    acknowledged, silence, monkeypatch
):
    from cratekit.tagging import published, searchers

    cfg = acknowledged
    paths = build(cfg, silence, Track("60", "", "", artist="Nobody", folder="x"))
    asked: list[tuple[str, str]] = []

    def search(artist, title):
        asked.append((artist, title))
        return SearchHit(genre=DEEP, source="discogs", source_genre="Deep House")

    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared: search)
    monkeypatch.setattr(published, "for_suggestions", lambda declared: lambda hit, isrc: hit)
    code, acted, refused = _two_acts(["--catalogue"])
    assert code == int(ExitCode.OK), acted
    assert _genre_of(cfg, "60") == DEEP and tags.read_genre_from_file(paths["60"]) == DEEP
    assert asked == [("Nobody", "track 60")]
    (item,) = refused["cause"]["detail"]["shown"]["items"]
    assert (item["source"], item["band"]) == ("discogs", suggest.HIGH)


def test_no_proposal_below_the_floor_is_shown_or_written(acknowledged, silence):
    """Two artist neighbours make a medium suggestion, below the floor."""
    cfg = acknowledged
    build(
        cfg,
        silence,
        Track("80", "", "", artist="Pair", folder="p"),
        Track("81", MELODIC, MELODIC, artist="Pair", folder="q"),
        Track("82", MELODIC, MELODIC, artist="Pair", folder="r"),
    )
    code, acted, refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    assert not [item for item in refused["cause"]["detail"]["shown"]["items"] if item["kind"] == "suggest"]
    assert _genre_of(cfg, "80") == ""


# ═══════════════════════════════════════════════════════════════════════════
# 5. What a person reads
# ═══════════════════════════════════════════════════════════════════════════


def test_a_rehearsed_digest_is_set_beside_the_live_one_at_the_gate(acknowledged, silence):
    build(acknowledged, silence, *_library())
    _run, first = _first_act([])
    digest = first["cause"]["detail"]["shown"]["digest"]
    _run, again = _first_act(["--rehearsed", digest])
    assert again["cause"]["detail"]["shown"]["rehearsed"] == {"digest": digest, "matches": True}
    _run, other = _first_act(["--rehearsed", "0" * 64])
    assert other["cause"]["detail"]["shown"]["rehearsed"]["matches"] is False
    # Shown, never digested: the answer binds the plan, not the rehearsal.
    assert other["cause"]["detail"]["shown"]["digest"] == digest


def test_a_person_reads_the_campaign_and_the_resort_it_leaves(acknowledged, silence):
    build(acknowledged, silence, *_library())
    run_id, _refused = _first_act(["--alias", INDIE_ALIAS])
    _decide(run_id)
    code, text = drive_human(["--run", run_id, *VERB, "--alias", INDIE_ALIAS])
    assert code == int(ExitCode.OK), text
    assert "needs genre 11 before the campaign and 6 after" in text
    assert "crate route resort" in text


def test_the_verb_declares_one_explicit_gate_and_the_surfaces_it_writes():
    from cratekit.cli import registry

    entry = registry.entry("tag.campaign")
    gate = next(spec for spec in entry.gates if spec.name == GATE)
    assert gate.explicit and gate.digest_source == "plan" and gate.options == ("apply", "abort")
    assert entry.writes == frozenset({"files", "db_metadata"}) and entry.destructive


# ═══════════════════════════════════════════════════════════════════════════
# 6. Round one of the review
# ═══════════════════════════════════════════════════════════════════════════


def _stray(cfg: config.Config, silence: Path, name: str, genre: str) -> Path:
    """An audio file under the library root that no row names."""
    import shutil

    path = Path(cfg.library.root) / "Music" / "stray" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"genre": genre})
    return path


def test_every_file_an_alias_retags_is_on_the_gate_and_in_the_digest(acknowledged, silence):
    """F1: the alias walks every file under the root, rows or none."""
    cfg = acknowledged
    build(cfg, silence, *_library())
    _run, without = _first_act(["--alias", INDIE_ALIAS])
    stray = _stray(cfg, silence, "stray.flac", INDIE)
    _run, refused = _first_act(["--alias", INDIE_ALIAS])
    shown = refused["cause"]["detail"]["shown"]
    files = {item["path"] for item in shown["items"] if item["kind"] == "file" and item["word"] == INDIE}
    assert str(Path("Music") / "stray" / "stray.flac") in files
    assert shown["digest"] != without["cause"]["detail"]["shown"]["digest"]
    assert shown["retags"] == 4
    _decide(_run)
    code, acted = drive(["--run", _run, *VERB, "--alias", INDIE_ALIAS])
    assert code == int(ExitCode.OK), acted
    assert tags.read_genre_from_file(stray) == MELODIC


def test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale(
    acknowledged, silence, monkeypatch
):
    """F1: the walk at the apply finds a file the gate never listed."""
    cfg = acknowledged
    build(cfg, silence, *_library())
    run_id, _refused = _first_act(["--alias", INDIE_ALIAS])
    _decide(run_id)
    real = tag_campaign.taxonomy_word.plan_alias
    late: list[Path] = []

    def plan_alias(cfg_, word, genre, folder=None):
        # Only the apply plans through the verb's own plan_alias; the gate's
        # walk ran before it, so the late file is one the gate never listed.
        if word == INDIE and not late:
            late.append(_stray(cfg, silence, "late.flac", INDIE))
        return real(cfg_, word, genre, folder)

    monkeypatch.setattr(tag_campaign.taxonomy_word, "plan_alias", plan_alias)
    code, stopped = drive(["--run", run_id, *VERB, "--alias", INDIE_ALIAS])
    assert code == int(ExitCode.DECISION_STALE), stopped
    assert "The campaign stopped at the words" in stopped["cause"]["message"]
    assert "crate tag rows landed, 1 row(s)" in stopped["cause"]["message"]
    assert tags.read_genre_from_file(late[0]) == INDIE
    assert active_taxonomy.load(cfg).tagging_alias(INDIE.lower()) is None


def test_the_gate_and_the_report_say_what_the_verbs_could_not_read(acknowledged, silence):
    """F2: a row whose file is missing and a file holding the word beside another genre."""
    cfg = acknowledged
    paths = build(cfg, silence, *_library(), Track("98", "", "", artist="Gone", folder="g"))
    paths["98"].unlink()
    assert tags.write_tag_values(paths["16"], "genre", ["indie tech", DEEP])
    _run, refused = _first_act(["--alias", INDIE_ALIAS])
    shown = refused["cause"]["detail"]["shown"]
    assert shown["unread"] == {rows.FILE_MISSING: 1}
    notes = " ".join(shown["notes"])
    assert "1 row(s) are in no cause" in notes
    assert "carry the word beside another genre" in notes
    _decide(_run)
    code, acted = drive(["--run", _run, *VERB, "--alias", INDIE_ALIAS])
    assert code == int(ExitCode.OK), acted
    codes = {warning["code"] for warning in acted["warnings"]}
    assert "backlog-files-unread" in codes and "taxonomy-alias-left-alone" in codes
    # The alias verb's own advice to run tag rows is not carried: step four is it.
    assert "taxonomy-alias-retagged" not in codes


def test_a_catalogue_nobody_could_read_is_said_at_the_gate(acknowledged, silence, monkeypatch):
    from cratekit.tagging import published, searchers

    build(acknowledged, silence, Track("60", "", "", artist="Nobody", folder="x"))

    def blocked(artist, title):
        raise refuse("catalogue-unreachable", "blocked", origin=("test",))

    monkeypatch.setattr(searchers, "for_taxonomy", lambda declared: blocked)
    monkeypatch.setattr(published, "for_suggestions", lambda declared: lambda hit, isrc: hit)
    _run, refused = _first_act(["--catalogue"])
    assert any("could not be read for 1 row(s)" in note for note in refused["cause"]["detail"]["shown"]["notes"])


def test_a_follower_whose_file_carries_another_spelling_is_held_out(
    acknowledged, silence, monkeypatch
):
    """F3: row 91 is filed by the folder answer; its file's other case would unfile it."""
    monkeypatch.setattr(_suggest_suite, "LOOKUPS", (*_suggest_suite.LOOKUPS, "indie tech"))
    cfg = acknowledged
    build(
        cfg,
        silence,
        *_backlog_suite._eight(),
        Track("15", "", INDIE, artist="X", folder="w"),
        Track("91", INDIE, "indie tech", artist="X", folder="w"),
    )
    code, acted, _refused = _two_acts(["--folder", INDIE])
    assert code == int(ExitCode.OK), acted
    assert _genre_of(cfg, "15") == INDIE and _genre_of(cfg, "91") == INDIE
    assert not {"15", "91"} & _census_needing(cfg)
    assert _steps(acted)["follow"]["left"] == {"91": tag_campaign.ANOTHER_SPELLING}
    (said,) = [w for w in acted["warnings"] if w["code"] == tag_campaign.ROWS_LEFT]
    assert "another spelling" in said["message"] and "rekordbox" not in said["message"]


def test_a_step_that_refuses_after_part_of_it_landed_reports_what_the_census_reads(
    acknowledged, silence, monkeypatch
):
    """F4: row 12's file and row land; row 96's file will not take its genre."""
    cfg = acknowledged
    build(cfg, silence, *_library(), Track("96", "", "", artist="Solo", folder="one"))
    run_id, _refused = _first_act([])
    _decide(run_id)
    real = tags.write_genre

    def one_stuck(path, genre):
        return False if Path(path).name == "track-96.flac" else real(path, genre)

    monkeypatch.setattr(tags, "write_genre", one_stuck)
    code, stopped = drive(["--run", run_id, *VERB])
    assert code != int(ExitCode.OK) and stopped["cause"]["reason"] == "tag-suggest-unwritten"
    campaign = stopped["cause"]["detail"]["campaign"]
    suggested = next(step for step in campaign["steps"] if step["step"] == "suggest")
    assert suggested["sessions"] and suggested["state"] == tag_campaign.REFUSED
    assert campaign["needs_genre"]["after"] == len(_census_needing(cfg)) == 10


def test_the_same_command_after_the_words_landed_is_taken_as_given(acknowledged, silence):
    """F5: a repeated answer the copy already holds is not a new answer."""
    cfg = acknowledged
    build(cfg, silence, *_library())
    code, acted, _refused = _two_acts(["--alias", INDIE_ALIAS])
    assert code == int(ExitCode.OK), acted
    code, again = drive([*VERB, "--alias", INDIE_ALIAS])
    assert code == int(ExitCode.DECISION_REQUIRED), again
    assert again["cause"]["detail"]["shown"]["answers"] == []


def test_the_same_folder_answer_after_it_landed_is_taken_as_given(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, *_library())
    code, acted, _refused = _two_acts(["--folder", INDIE])
    assert code == int(ExitCode.OK), acted
    code, again = drive([*VERB, "--folder", INDIE])
    assert code == int(ExitCode.DECISION_REQUIRED), again


def test_a_folder_answer_shows_the_bucket_it_copies(acknowledged, silence):
    """F10: the folder's family, tempo window and rating come from its like bucket."""
    build(acknowledged, silence, *_library())
    _run, refused = _first_act(["--folder", INDIE])
    (item,) = [
        item for item in refused["cause"]["detail"]["shown"]["items"]
        if item["kind"] == "words" and item["word"] == INDIE
    ]
    assert item["answer"] == backlog.FOLDER and item["like"] and item["bucket"]


def test_the_words_step_refusing_stops_the_campaign_with_what_landed_named(
    acknowledged, silence, monkeypatch
):
    """F8: the third step's own refusal."""
    cfg = acknowledged
    build(cfg, silence, *_library())
    run_id, _refused = _first_act(["--alias", INDIE_ALIAS])
    _decide(run_id)
    real = tags.write_genre

    def alias_stuck(path, genre):
        return False if genre == RNB else real(path, genre)

    monkeypatch.setattr(tags, "write_genre", alias_stuck)
    code, stopped = drive(["--run", run_id, *VERB, "--alias", INDIE_ALIAS])
    assert code != int(ExitCode.OK) and stopped["cause"]["reason"] == "taxonomy-word-unwritten"
    message = stopped["cause"]["message"]
    assert "crate tag suggest landed, 1 row(s)" in message
    assert "not run: tag rows again, route resort" in message


def test_the_fourth_step_refusing_stops_the_campaign_after_the_words(
    acknowledged, silence, monkeypatch
):
    """F8: only the follow step opens the database to write in this library."""
    cfg = acknowledged
    paths = build(
        cfg,
        silence,
        *_backlog_suite._eight(),
        Track("15", "", INDIE, artist="X", folder="w"),
    )
    run_id, _refused = _first_act(["--alias", INDIE_ALIAS])
    _decide(run_id)
    real = rb_writer.open_db

    def running(path, *args, require_closed=False, **kwargs):
        if require_closed:
            raise refuse("rekordbox-running", "rekordbox is running", origin=("test",))
        return real(path, *args, require_closed=require_closed, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", running)
    code, stopped = drive(["--run", run_id, *VERB, "--alias", INDIE_ALIAS])
    assert code != int(ExitCode.OK) and stopped["cause"]["reason"] == "rekordbox-running"
    assert "the words landed, 1 word(s) and 1 file(s)" in stopped["cause"]["message"]
    assert tags.read_genre_from_file(paths["15"]) == MELODIC and _genre_of(cfg, "15") == ""


def test_an_unexpected_failure_in_a_step_is_this_builds_defect_with_what_landed(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    build(cfg, silence, *_library())
    run_id, _refused = _first_act([])
    _decide(run_id)

    def broken(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(tag_campaign.suggest_cli, "read_plan", broken)
    code, stopped = drive(["--run", run_id, *VERB])
    assert stopped["cause"]["reason"] == "internal-error", stopped
    assert "RuntimeError: boom" in stopped["cause"]["message"]
    assert "crate tag rows landed, 1 row(s)" in stopped["cause"]["message"]
    assert _genre_of(cfg, "10") == MELODIC


def test_the_suggest_step_plans_at_the_backlogs_floor(acknowledged, silence, monkeypatch):
    """F7: the second plan is weighed at the floor, never wider."""
    build(acknowledged, silence, *_library())
    run_id, _refused = _first_act([])
    _decide(run_id)
    real = tag_campaign.suggest_cli.read_plan
    bands: list[str] = []

    def spy(*args, band, **kwargs):
        bands.append(band)
        return real(*args, band=band, **kwargs)

    monkeypatch.setattr(tag_campaign.suggest_cli, "read_plan", spy)
    code, acted = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), acted
    assert bands == [backlog.FLOOR]


def test_a_row_that_does_not_read_back_refuses_the_rows_step(acknowledged, silence, monkeypatch):
    """F7: the campaign's rows go through tag rows' own read back."""
    cfg = acknowledged
    build(cfg, silence, *_library())
    run_id, _refused = _first_act([])
    _decide(run_id)
    real = rows.apply_rows

    def wrong(*args, **kwargs):
        written = real(*args, **kwargs)
        return replace(written, wrong=("10",))

    monkeypatch.setattr(rows, "apply_rows", wrong)
    code, stopped = drive(["--run", run_id, *VERB])
    assert code != int(ExitCode.OK), stopped
    assert "The campaign stopped at crate tag rows" in stopped["cause"]["message"]


def test_needing_counts_only_live_rows_with_a_readable_file(machine, silence):
    """F7: the census after a step leaves out a tombstone and a missing file."""
    paths = build(
        machine,
        silence,
        Track("51", "", ""),
        Track("52", "", "", deleted=True),
        Track("53", "", ""),
        *_backlog_suite._eight(),
    )
    paths["53"].unlink()
    db = rb_writer.open_db(machine.library.db_path, unlock=False, cfg=machine)
    try:
        found = backlog.needing(machine, db, active_taxonomy.load(machine))
    finally:
        rb_writer.close_db(db)
    assert found == {"51"}
    assert len(_planned(machine).rows) == 1


# ═══════════════════════════════════════════════════════════════════════════
# 7. Round two of the review
# ═══════════════════════════════════════════════════════════════════════════


def test_the_same_folder_answer_once_the_word_has_left_the_backlog_is_taken_as_given(
    acknowledged, silence
):
    """Round two: the row and the file both carry the word, so once its folder
    lands the backlog no longer holds it, and the same command still runs."""
    cfg = acknowledged
    build(cfg, silence, *_backlog_suite._eight(), Track("15", INDIE, INDIE, artist="X", folder="w"))
    code, acted, _refused = _two_acts(["--folder", INDIE])
    assert code == int(ExitCode.OK), acted
    assert "15" not in _census_needing(cfg)
    assert not [word for word in _planned(cfg).words if word.spelling == INDIE]
    code, again = drive([*VERB, "--folder", INDIE])
    assert code == int(ExitCode.DECISION_REQUIRED), again
    assert again["cause"]["detail"]["shown"]["answers"] == []


def test_the_joining_rows_are_said_in_the_campaigns_own_words(acknowledged, silence):
    build(acknowledged, silence, *_library(), Track("80", MELODIC, GRIME, artist="Y", folder="y"))
    _run, refused = _first_act([])
    (note,) = [n for n in refused["cause"]["detail"]["shown"]["notes"] if "80" in n]
    assert "the campaign holds each of them out" in note and "--leave" not in note


# ═══════════════════════════════════════════════════════════════════════════
# 8. What the mutation table found no test for
# ═══════════════════════════════════════════════════════════════════════════

ZOUK = "zouk bass"


def test_an_alias_to_the_folder_another_answer_makes_is_planned_on_that_folder(
    acknowledged, silence
):
    """M15: each word is planned on the copy the words before it leave, so an
    alias may name the genre folder the same campaign's folder answer makes."""
    cfg = acknowledged
    paths = build(cfg, silence, *_library(), Track("97", ZOUK, ZOUK, artist="Z", folder="z"))
    argv = ["--folder", INDIE, "--alias", f"{ZOUK}={INDIE}"]
    run_id, refused = _first_act(argv)
    words = [
        (item["word"], item["answer"])
        for item in refused["cause"]["detail"]["shown"]["items"]
        if item["kind"] == "words" and item["word"] in {INDIE, ZOUK}
    ]
    assert words == [(INDIE, backlog.FOLDER), (ZOUK, backlog.ALIAS)]
    _decide(run_id)
    code, acted = drive(["--run", run_id, *VERB, *argv])
    assert code == int(ExitCode.OK), acted
    assert tags.read_genre_from_file(paths["97"]) == INDIE
    assert active_taxonomy.load(cfg).tagging_alias(ZOUK) is not None


def test_a_folder_that_would_copy_another_bucket_after_the_gate_stops_the_words_as_stale(
    acknowledged, silence, monkeypatch
):
    """M25: the folder the words step would make is held to the one the gate listed."""
    cfg = acknowledged
    build(cfg, silence, *_library())
    run_id, refused = _first_act(["--folder", INDIE])
    (shown,) = [
        item for item in refused["cause"]["detail"]["shown"]["items"]
        if item["kind"] == "words" and item["word"] == INDIE
    ]
    _decide(run_id)
    real = tag_campaign.taxonomy_word.plan_folder
    other = next(
        bucket.display for bucket in active_taxonomy.load(cfg).buckets if bucket.display != shown["like"]
    )

    def plan_folder(cfg_, word, like=None):
        # The copy moved after the approval, so the folder would copy another bucket.
        return real(cfg_, word, other)

    monkeypatch.setattr(tag_campaign.taxonomy_word, "plan_folder", plan_folder)
    code, stopped = drive(["--run", run_id, *VERB, "--folder", INDIE])
    assert code == int(ExitCode.DECISION_STALE), stopped
    assert "The campaign stopped at the words" in stopped["cause"]["message"]
    assert not any(bucket.display == INDIE for bucket in active_taxonomy.load(cfg).buckets)
