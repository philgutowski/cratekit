"""U340: ``crate tag second`` sets or clears a track's second genre on its file.

The engine against a disposable database and real containers, then the verb
through the real dispatcher, both acts. Every expected genre is a literal the
shipped taxonomy declares. D1 applies: no real volume, person or track.
"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

import pytest

from cratekit.cli import registry
from cratekit.core import active_taxonomy, config, routing, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import second, second_cli
from tests import test_tag_rows as _rows_suite
from tests import test_tag_suggest as _suggest_suite
from tests.cli_drive import drive
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414

machine = _rows_suite.machine
silence = _rows_suite.silence
_release_process_locks = _rows_suite._release_process_locks
_field_policies = _rows_suite._field_policies
_reader_cache = _rows_suite._reader_cache
_platform_seams = _rows_suite._platform_seams

Track = _suggest_suite.Track
build = _suggest_suite.build

DECLARED = taxonomy.default_taxonomy()
VERB = ["tag", "second"]
GATE = second_cli.CONFIRM_GATE

DEEP = "Deep House"
TECH = "Tech House"
MELODIC = "Melodic House"
#: A word the shipped taxonomy files nowhere but the fallback.
NOWHERE = "Polka"
#: A word the shipped taxonomy calls too coarse to be a genre.
COARSE = next(word for word in DECLARED.fallback.too_coarse_as_source if word)


def _second_of(path: Path) -> str | None:
    return tags.read_tag(path, "secondgenre")


def _plan(cfg: config.Config, **kwargs) -> second.SecondPlan:
    with _rows_suite.opened(cfg) as db:
        return second.plan(cfg, db, active_taxonomy.load(cfg), **kwargs)


def _by_row(plan: second.SecondPlan) -> dict[str, second.Item]:
    return {item.content_id: item for item in plan.items}


def _bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# 1. The rule, pure


def test_the_shipped_words_this_suite_names_file_as_it_assumes():
    assert {DEEP, TECH, MELODIC} <= {bucket.display for bucket in DECLARED.buckets}
    assert routing.files_by_genre(DECLARED, NOWHERE) is None
    assert routing.files_by_genre(DECLARED, COARSE) is None
    assert routing.second_bucket(DECLARED, DEEP, TECH) == DECLARED.bucket_for_display(TECH)
    assert routing.second_bucket(DECLARED, DEEP, DEEP) is None


@pytest.mark.parametrize("word", [NOWHERE, COARSE, "  "])
def test_a_genre_that_files_nowhere_refuses_before_anything_is_read(word):
    with pytest.raises(CratekitError) as raised:
        second.assert_genre_files(DECLARED, word)
    assert raised.value.cause.reason == "tag-second-genre-undeclared"


# 2. The plan, against a disposable database and real files


def test_each_chosen_row_lands_in_one_outcome(machine, silence):
    paths = build(
        machine, silence, Track("10", file=DEEP), Track("11", file=TECH), Track("12", file=""),
        Track("13", file=DEEP), Track("14", file=DEEP), Track("15", file=_suggest_suite.ABSENT),
    )
    assert tags.write_tags(paths["13"], {"secondgenre": TECH})
    chosen = ["10", "11", "12", "13", "14", "15", "999"]
    found = _by_row(_plan(machine, genre=TECH, chosen=chosen, leave=["14"]))
    assert {cid: (item.action, item.reason) for cid, item in found.items()} == {
        "10": (second.WRITE, ""),
        "11": (second.LEAVE, second.SAME_FOLDER),
        "12": (second.LEAVE, second.GENRE_FILES_NOWHERE),
        "13": (second.LEAVE, second.ALREADY),
        "14": (second.LEAVE, second.HELD_OUT),
        "15": (second.LEAVE, second.FILE_MISSING),
        "999": (second.LEAVE, second.ROW_GONE),
    }
    assert (found["10"].genre, found["10"].current, found["10"].wanted) == (DEEP, "", TECH)


def test_a_clear_writes_only_a_row_that_carries_one(machine, silence):
    paths = build(machine, silence, Track("10", file=DEEP), Track("11", file=DEEP))
    assert tags.write_tags(paths["10"], {"secondgenre": TECH})
    found = _by_row(_plan(machine, genre="", chosen=["10", "11"]))
    assert (found["10"].action, found["10"].current, found["10"].wanted) == (
        second.WRITE, TECH, "",
    )
    assert (found["11"].action, found["11"].reason) == (second.LEAVE, second.NONE_TO_CLEAR)


def test_the_apply_writes_the_second_genre_alone_and_reads_it_back(machine, silence):
    paths = build(machine, silence, Track("10", file=DEEP), Track("11", file=DEEP))
    plan = _plan(machine, genre=TECH, chosen=["10"])
    untouched = _bytes(paths["11"])
    written = second.apply(plan)
    assert (written.written, written.read_back, written.clean) == (1, 1, True)
    assert _second_of(paths["10"]) == TECH
    assert tags.read_genre_from_file(paths["10"]) == DEEP
    assert _bytes(paths["11"]) == untouched
    # THE SECOND RUN PLANS NOTHING.
    again = _plan(machine, genre=TECH, chosen=["10"])
    assert again.writes == () and again.counts[second.ALREADY] == 1

    cleared = second.apply(_plan(machine, genre="", chosen=["10"]))
    assert cleared.read_back == 1 and _second_of(paths["10"]) is None


def test_a_file_that_moved_since_the_plan_is_not_written(machine, silence):
    paths = build(machine, silence, Track("10", file=DEEP), Track("11", file=DEEP))
    plan = _plan(machine, genre=TECH, chosen=["10", "11"])
    assert tags.write_tags(paths["10"], {"secondgenre": MELODIC})
    assert tags.write_genre(paths["11"], MELODIC)
    written = second.apply(plan)
    assert set(written.moved) == {str(paths["10"]), str(paths["11"])}
    assert written.written == 0
    assert _second_of(paths["10"]) == MELODIC
    with pytest.raises(CratekitError) as raised:
        second_cli.assert_written(written)
    assert raised.value.cause.reason == "tag-second-unwritten"


def _seed(
    cfg: config.Config,
    nodes: list[tuple[str, str, int, str, int]],
    members: list[tuple[str, str, str, int]],
) -> None:
    """Playlist rows ``(id, name, attribute, parent, removed)`` and memberships
    ``(id, playlist, content, removed)`` written straight into the copy."""
    connection = sqlite3.connect(cfg.library.db_path)
    try:
        has_seq = any(
            row[1] == "Seq" for row in connection.execute("PRAGMA table_info(djmdPlaylist)")
        )
        for pid, name, attribute, parent, removed in nodes:
            fields = {
                "ID": pid, "Name": name, "Attribute": attribute, "ParentID": parent,
                "rb_local_deleted": removed, **({"Seq": 0} if has_seq else {}),
            }
            connection.execute(
                f"INSERT INTO djmdPlaylist ({', '.join(fields)}) "
                f"VALUES ({', '.join('?' * len(fields))})",
                tuple(fields.values()),
            )
        connection.executemany(
            "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, rb_local_deleted) "
            "VALUES (?, ?, ?, 0, ?)",
            members,
        )
        connection.commit()
    finally:
        connection.close()


def test_a_playlist_is_found_by_its_whole_path_even_with_the_separator_in_a_name(
    machine, silence
):
    build(machine, silence, Track("10", file=DEEP), Track("11", file=DEEP), Track("12", file=DEEP))
    # A folder named with the separator inside it, a playlist under it, two members.
    _seed(
        machine,
        [("900", "Minimal / Deep Tech", 1, "root", 0), ("901", "Med", 0, "900", 0),
         ("902", "Med", 0, "root", 0)],
        [("950", "901", "10", 0), ("951", "901", "11", 0)],
    )
    with _rows_suite.opened(machine) as db:
        assert second.playlist_members(db, "Minimal / Deep Tech / Med") == ("10", "11")
        for path, reason in (
            ("Minimal / Deep Tech", "it names a folder"),
            ("Nowhere / Med", "nothing in the tree"),
        ):
            with pytest.raises(CratekitError) as raised:
                second.playlist_members(db, path)
            assert raised.value.cause.reason == "tag-second-playlist-unknown"
            assert reason in raised.value.cause.message
        with pytest.raises(CratekitError) as raised:
            second.chosen_rows(db, rows_given=[], rows_file=None, playlist=None)
        assert raised.value.cause.reason == "tag-second-no-rows"


def test_a_rows_file_names_rows_one_per_line(tmp_path):
    listed = tmp_path / "rows.txt"
    listed.write_text("# chosen\n10\n\n11\n10\n", encoding="utf-8")
    assert second.chosen_rows(None, rows_given=["12"], rows_file=str(listed), playlist=None) == (
        "12", "10", "11",
    )
    with pytest.raises(CratekitError) as raised:
        second.chosen_rows(None, rows_given=[], rows_file=str(tmp_path / "gone"), playlist=None)
    assert raised.value.cause.reason == "tag-second-rows-unreadable"


# 3. The verb


def test_the_verb_is_registered_with_an_explicit_gate_and_writes_files_only():
    entry = registry.entry("tag.second")
    assert entry.writes == frozenset({"files"}) and entry.destructive
    (gate,) = entry.gates
    assert (gate.name, gate.explicit) == (GATE, True)


def test_the_verb_asks_then_writes_and_names_the_filing_step(machine, silence):
    paths = build(machine, silence, Track("10", file=DEEP))
    verb = [*VERB, TECH, "--row", "10"]
    run_id, _refused = _rows_suite.decided(verb, GATE)
    assert _second_of(paths["10"]) is None
    code, acted = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK), acted
    assert _second_of(paths["10"]) == TECH
    (said,) = [one for one in acted["warnings"] if one["code"] == second_cli.WRITTEN]
    assert "crate adopt apply" in said["message"]


@pytest.mark.parametrize(
    ("argv", "reason"),
    [
        ([TECH, "--clear", "--row", "10"], "tag-second-usage"),
        (["--row", "10"], "tag-second-usage"),
        ([NOWHERE, "--row", "10"], "tag-second-genre-undeclared"),
    ],
    ids=["both", "neither", "files-nowhere"],
)
def test_the_verb_refuses_a_request_it_cannot_plan(machine, silence, argv, reason):
    paths = build(machine, silence, Track("10", file=DEEP))
    before = _bytes(paths["10"])
    code, refused = drive([*VERB, *argv])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == reason
    assert _bytes(paths["10"]) == before
