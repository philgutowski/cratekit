"""R-1950: each guard of ``crate tag second`` that no test killed, killed.

The guards U340's review removed one at a time with the suite still green: the
apply's read back, the plan digest's items, the playlist lookup's live rows,
its refusal of two nodes at one path and its parent cycle guard, and the genre
check in the engine's plan and in the verb's read. Against a disposable
database and real containers, as ``tests/test_tag_second.py`` builds them. D1
applies: no real volume, person or track.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from cratekit.cli.output import digest_of
from cratekit.core import config, rb_writer, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import second, second_cli
from tests.cli_drive import drive
from tests.test_tag_second import DEEP, NOWHERE, TECH, Track, _plan, _second_of, build
from tests.test_tag_second import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_tag_second import _less_work as _less_work  # noqa: PLC0414
from tests.test_tag_second import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_tag_second import _reader_cache as _reader_cache  # noqa: PLC0414
from tests.test_tag_second import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_tag_second import machine as machine  # noqa: PLC0414
from tests.test_tag_second import silence as silence  # noqa: PLC0414

#: A playlist path the seeded tree holds once, live, with two live members.
LIVE_PATH = "Crates / Warm"


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


#: A folder, a live playlist under it holding 10 and 11 live and 12 removed.
_TREE = [("800", "Crates", 1, "root", 0), ("801", "Warm", 0, "800", 0)]
_MEMBERS = [("850", "801", "10", 0), ("851", "801", "11", 0), ("852", "801", "12", 1)]


def _members(cfg: config.Config, path: str) -> tuple[str, ...]:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return second.playlist_members(db, path)
    finally:
        rb_writer.close_db(db)


def _refused(cfg: config.Config, path: str) -> str:
    with pytest.raises(CratekitError) as raised:
        _members(cfg, path)
    assert raised.value.cause.reason == "tag-second-playlist-unknown"
    return raised.value.cause.message


def _three(machine, silence) -> dict[str, Path]:
    return build(
        machine, silence, Track("10", file=DEEP), Track("11", file=DEEP), Track("12", file=DEEP)
    )


# 1. The apply, the path that writes


def test_a_write_that_does_not_read_back_is_named_wrong_and_refused(
    machine, silence, monkeypatch
):
    """The read back compare: a write the tag library says took, while the file
    still carries no second genre, is counted wrong and never read back."""
    paths = build(machine, silence, Track("10", file=DEEP))
    plan = _plan(machine, genre=TECH, chosen=["10"])
    monkeypatch.setattr(tags, "write_tags", lambda path, values: True)
    written = second.apply(plan)
    assert (written.written, written.read_back) == (1, 0)
    assert written.wrong == (str(paths["10"]),)
    assert written.rewritten == () and not written.clean
    assert _second_of(paths["10"]) is None
    with pytest.raises(CratekitError) as raised:
        second_cli.assert_written(written)
    assert raised.value.cause.reason == "tag-second-unwritten"
    assert "1 were written and do not read back as wanted" in raised.value.cause.message


def test_a_clear_that_does_not_read_back_is_named_wrong(machine, silence, monkeypatch):
    paths = build(machine, silence, Track("10", file=DEEP))
    assert tags.write_tags(paths["10"], {"secondgenre": TECH})
    plan = _plan(machine, genre="", chosen=["10"])
    monkeypatch.setattr(tags, "clear_tags", lambda path, names: True)
    written = second.apply(plan)
    assert (written.written, written.read_back, written.wrong) == (1, 0, (str(paths["10"]),))
    assert _second_of(paths["10"]) == TECH


def test_a_write_that_changes_the_genre_beside_it_is_named_wrong(machine, silence, monkeypatch):
    """The genre half of the read back compare: a write that lands the second
    genre but leaves another genre on the file is not read back as written."""
    paths = build(machine, silence, Track("10", file=DEEP))
    plan = _plan(machine, genre=TECH, chosen=["10"])
    real = tags.write_tags
    monkeypatch.setattr(
        tags, "write_tags", lambda path, values: real(path, {**values, "genre": "Melodic House"})
    )
    written = second.apply(plan)
    assert (written.written, written.read_back, written.wrong) == (1, 0, (str(paths["10"]),))


# 2. The digest an approval is bound to


def _item(content_id: str, path: str, current: str = "") -> second.Item:
    return second.Item(content_id, path, DEEP, current, TECH, second.WRITE)


def test_the_plan_digest_binds_every_row_not_only_the_counts():
    """Two plans with the same genre and counts and different rows, or one row's
    second genre before, digest apart, so an approval never covers another set."""
    counts = {**dict.fromkeys(second.OUTCOMES, 0), second.WRITE: 1}
    one = second.SecondPlan(TECH, (_item("10", "/music/a.mp3"),), counts)
    other_row = second.SecondPlan(TECH, (_item("11", "/music/b.mp3"),), counts)
    other_was = second.SecondPlan(TECH, (_item("10", "/music/a.mp3", current="Melodic House"),), counts)
    assert len({one.digest, other_row.digest, other_was.digest}) == 3
    assert one.digest == digest_of(
        {
            "kind": "tag-second",
            "genre": TECH,
            "items": [
                {
                    "content_id": "10", "path": "/music/a.mp3", "genre": DEEP,
                    "second_genre_was": "", "second_genre": TECH, "action": "write",
                    "reason": "",
                }
            ],
            "counts": counts,
        }
    )


# 3. The playlist lookup, which chooses the rows a write reaches


def test_a_removed_membership_is_not_a_chosen_row(machine, silence):
    _three(machine, silence)
    _seed(machine, _TREE, _MEMBERS)
    assert _members(machine, LIVE_PATH) == ("10", "11")


def test_a_removed_playlist_is_not_in_the_tree(machine, silence):
    _three(machine, silence)
    _seed(machine, [*_TREE, ("802", "Gone", 0, "800", 1)], [("853", "802", "12", 0)])
    assert "nothing in the tree is at that path" in _refused(machine, "Crates / Gone")


def test_a_live_playlist_under_a_removed_folder_is_at_no_path(machine, silence):
    """Its parent is not in the live tree, so it answers to no path at all,
    neither its bare name nor one under an empty folder name."""
    _three(machine, silence)
    _seed(
        machine,
        [*_TREE, ("806", "Attic", 1, "root", 1), ("807", "Box", 0, "806", 0)],
        [*_MEMBERS, ("856", "807", "12", 0)],
    )
    for path in ("Box", " / Box", "Attic / Box"):
        assert "nothing in the tree is at that path" in _refused(machine, path)


def test_two_playlists_at_one_path_refuse_rather_than_choose(machine, silence):
    _three(machine, silence)
    _seed(
        machine,
        [*_TREE, ("803", "Warm", 0, "800", 0)],
        [*_MEMBERS, ("854", "803", "12", 0)],
    )
    assert "2 nodes answer to it" in _refused(machine, LIVE_PATH)


def test_a_parent_cycle_in_the_tree_names_nothing_and_breaks_no_lookup(machine, silence):
    """Two nodes each the other's parent are at no path, and the lookup of a
    live playlist beside them still answers rather than recursing forever."""
    _three(machine, silence)
    _seed(
        machine,
        [*_TREE, ("804", "Loop", 1, "805", 0), ("805", "Loop", 0, "804", 0)],
        [*_MEMBERS, ("855", "805", "12", 0)],
    )
    assert _members(machine, LIVE_PATH) == ("10", "11")
    assert "nothing in the tree is at that path" in _refused(machine, "Loop / Loop")


# 4. The genre check, in the engine and in the verb


def test_the_engine_refuses_a_genre_that_files_nowhere_itself(machine, silence):
    """``second.plan`` is the engine's public plan, so it refuses a genre naming
    no folder itself rather than trusting a caller to have checked."""
    build(machine, silence, Track("10", file=DEEP))
    with pytest.raises(CratekitError) as raised:
        _plan(machine, genre=NOWHERE, chosen=["10"])
    assert raised.value.cause.reason == "tag-second-genre-undeclared"


def test_the_verb_refuses_a_genre_that_files_nowhere_before_it_opens_the_library(
    machine, silence
):
    """With the library unreadable, the refusal is still the genre's, since the
    verb checks the genre before it opens anything."""
    paths = build(machine, silence, Track("10", file=DEEP))
    Path(machine.library.db_path).unlink()
    code, refused = drive(["tag", "second", NOWHERE, "--row", "10"])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "tag-second-genre-undeclared"
    assert _second_of(paths["10"]) is None


def test_a_good_genre_on_an_unreadable_library_is_the_library_s_refusal(machine, silence):
    """The control for the test above: the same verb with a genre that files is
    refused for the library, so the refusal above is the genre check's own."""
    build(machine, silence, Track("10", file=DEEP))
    Path(machine.library.db_path).unlink()
    code, refused = drive(["tag", "second", TECH, "--row", "10"])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] != "tag-second-genre-undeclared"
