"""U327: ``crate analyze adopt`` gives a landed title rekordbox's key and tempo.

The splice on values built here; then the plan and the write through the real
dispatcher on the native landing suite's disposable database, real tagged
containers named the library's way (the head in the file name and the title
tag alike), rekordbox's analysis simulated by its columns, an analysis file and
a key. Every column of every row, every analysis file and every file name is
compared across the write. D1 applies.
"""

from __future__ import annotations

import hashlib
import shutil
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.analysis import check_cli, head_adopt_cli
from cratekit.analysis import head_adopt as ha
from cratekit.analysis import rekordbox_check as rc
from cratekit.cli import gates, registry
from cratekit.core import analysis_store, config, locations, rb_writer, session, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.core.naming import NameTemplate, parse_head, stamp_head
from cratekit.intake import native
from cratekit.write import metadata
from tests.cli_drive import drive
from tests.test_analyze_check import CONSTANT_GRID, PATH_TAG, _key_id, anlz
from tests.test_inbox_refill import offline as offline  # noqa: PLC0414
from tests.test_intake_land_account_playlists_native import (
    pinned_day as pinned_day,  # noqa: PLC0414
)
from tests.test_intake_land_native import _configured, _cut_over_intake, _query, _staging
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import _two_acts as _land_acts
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_no_beatgrid_ever import FORBIDDEN_TAG_KEYS

VERB = ["analyze", "adopt"]
GATE = head_adopt_cli.CONFIRM_GATE
#: The library's shape, the lossy marker in config's text.
TEMPLATE = NameTemplate.lossy("[MP3]")


@pytest.fixture
def full_machine(library, monkeypatch) -> tuple[config.Config, str]:
    """A machine on the full profile, whose analysis module carries the verb, its
    intake tree cut over. Answers (cfg, the intake root's id)."""
    cfg = _configured(library, monkeypatch, profile="full")
    return cfg, _cut_over_intake(cfg)


@pytest.fixture
def unacknowledged(full_machine) -> config.Config:
    return full_machine[0]


@pytest.fixture
def native_library(full_machine) -> tuple[config.Config, str]:
    """The machine with a backup acknowledgment recorded."""
    session.record_acknowledgment(full_machine[0], terminal=lambda: True)
    return full_machine


@pytest.fixture(autouse=True)
def _field_policies():
    """The policy registry is process wide and the apply registers into it."""
    rb_writer.reset_field_policies()
    yield
    rb_writer.reset_field_policies()


# 1. The splice, pure


@pytest.mark.parametrize(
    ("title", "key", "tempo", "expected"),
    [
        pytest.param("01A - 124 - Alpha", "07B", 124, "07B - 124 - Alpha", id="a-far-key"),
        pytest.param("01A - 124 - Alpha", "02A", 124, "02A - 124 - Alpha", id="a-one-step-key"),
        pytest.param("01A - 124 - Alpha", "01B", 124, "01B - 124 - Alpha", id="a-relative-key"),
        pytest.param("01A - 124 - Alpha", "01A", 124, "01A - 124 - Alpha", id="an-equal-key"),
        pytest.param("1A - 124 - Alpha", "01A", 124, "1A - 124 - Alpha", id="unpadded-equal-stands"),
        pytest.param("1A - 124 - Alpha", "05B", 124, "05B - 124 - Alpha", id="unpadded-far-padded"),
        pytest.param("01A - 124 - Alpha", "01A", 125, "01A - 124 - Alpha", id="one-beat-off-left"),
        pytest.param("01A - 124 - Alpha", "01A", 123, "01A - 124 - Alpha", id="one-beat-under-left"),
        pytest.param("01A - 124 - Alpha", "01A", 126, "01A - 126 - Alpha", id="two-off-taken"),
        pytest.param("08A - 85 - The Curse", "08A", 128, "08A - 128 - The Curse", id="two-thirds"),
        pytest.param("08A - 84 - Hostile", "08A", 126, "08A - 126 - Hostile", id="four-to-six"),
        pytest.param("08A - 107 - SPEED", "08A", 80, "08A - 80 - SPEED", id="four-to-three"),
        pytest.param("08A - 100 - Feminine", "08A", 150, "08A - 150 - Feminine", id="two-to-three"),
        pytest.param("08A - 64 - Half", "08A", 128, "08A - 128 - Half", id="a-half"),
        pytest.param("01A - 124 - Alpha", "09B", 98, "09B - 98 - Alpha", id="both-wrong"),
        pytest.param(
            "01A - 124 - [MP3] Alpha", "09B", 98, "09B - 98 - [MP3] Alpha", id="the-marker-kept"
        ),
        pytest.param(
            "01A - 101 - 1A - 101 - Body", "11A", 140, "11A - 140 - 1A - 101 - Body",
            id="a-body-that-begins-like-a-head",
        ),
        pytest.param("01A - 124 - Alpha", None, 140, "01A - 140 - Alpha", id="no-key-tempo-still"),
        pytest.param("01A - 124 - Alpha", "06A", None, "06A - 124 - Alpha", id="no-tempo-key-still"),
        pytest.param("01A - 124 - Alpha", None, None, "01A - 124 - Alpha", id="no-answer-no-change"),
        pytest.param("Alpha", "06A", 124, None, id="no-head"),
        pytest.param("[MP3] Alpha", "06A", 124, None, id="a-marker-only-head"),
    ],
)
def test_the_head_takes_rekordbox_s_key_and_tempo_and_no_other_byte(title, key, tempo, expected):
    assert ha.adopted(title, key=key, tempo=tempo, template=TEMPLATE) == expected


@pytest.mark.parametrize(
    ("key_id", "scale", "expected"),
    [
        ("k", "8A", ("08A", "")),
        ("k", "08A", ("08A", "")),
        ("k", "Am", ("08A", "")),
        ("k", "F#m", ("11A", "")),
        ("k", "Lydian", (None, ha.KEY_NOT_CAMELOT)),
        ("k", "13A", (None, ha.KEY_NOT_CAMELOT)),
        ("k", "", (None, ha.KEY_EMPTY)),
        ("k", None, (None, ha.KEY_EMPTY)),
        (None, "8A", (None, ha.KEY_EMPTY)),
        (0, "8A", (None, ha.KEY_EMPTY)),
        ("0", "8A", (None, ha.KEY_EMPTY)),
    ],
)
def test_the_key_column_reads_in_either_notation_or_says_why_it_does_not(key_id, scale, expected):
    assert ha.reference_key(key_id, scale) == expected


@pytest.mark.parametrize(
    ("hundredths", "expected"),
    [
        (12484, (125, "")),
        (12450, (125, "")),
        (12449, (124, "")),
        (12800, (128, "")),
        (0, (None, ha.TEMPO_ZERO)),
        (None, (None, ha.TEMPO_ZERO)),
        (-100, (None, ha.TEMPO_ZERO)),
    ],
)
def test_the_tempo_is_the_column_rounded_half_up_or_zero(hundredths, expected):
    assert ha.reference_tempo(hundredths) == expected


# 2. The library: landed rows named the library's way, and rekordbox's visit


def _land_headed(cfg: config.Config, silence: Path, batch: str, heads: dict[str, str]) -> None:
    """Stage each track with its head in the file name and the title tag, then land."""
    for stem, head in heads.items():
        path = _staging(cfg) / f"{head} - {stem}.flac"
        shutil.copyfile(silence, path)
        assert tags.write_tags(
            path, {"title": f"{head} - {stem}", "artist": "Probe", "genre": "Deep House"}
        )
    code, acted, _refused = _land_acts(["intake", "land", "--name", batch])
    assert code == int(ExitCode.OK), acted


def _id(cfg: config.Config, stem: str) -> str:
    """The row whose title ends in ``stem`` after a head, a marker, or nothing (U342)."""
    ((content_id,),) = _query(
        cfg,
        "SELECT ID FROM djmdContent WHERE (Title LIKE ? OR Title LIKE ? OR Title = ?) "
        "AND rb_local_deleted = 0",
        f"% - {stem}",
        f"%] {stem}",
        stem,
    )
    return str(content_id)


def _visit(
    cfg: config.Config, stem: str, *, scale: str | None, bpm: int | None, analysed: bool = True
) -> None:
    """Simulate rekordbox analysing one row: its analysis file, key and tempo."""
    content_id = _id(cfg, stem)
    stored = f"/PIONEER/USBANLZ/c0f/{content_id}/ANLZ0000.DAT"
    path = analysis_store.analysis_file(cfg, stored)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(anlz(CONSTANT_GRID, before=PATH_TAG))
    key_id = _key_id(cfg, scale) if scale else None
    with sqlite3.connect(cfg.library.db_path) as conn:
        conn.execute(
            "UPDATE djmdContent SET Analysed = ?, AnalysisDataPath = ?, KeyID = ?, BPM = ? "
            "WHERE ID = ?",
            (105 if analysed else 0, stored if analysed else None, key_id, bpm, content_id),
        )
    conn.close()


def _file(cfg: config.Config, stem: str) -> Path:
    ((recorded,),) = _query(cfg, "SELECT FolderPath FROM djmdContent WHERE ID = ?", _id(cfg, stem))
    resolved = locations.resolve_recorded_path(
        locations.location_to_path(recorded), root=cfg.library.root, prefix_map=()
    )
    return Path(resolved.path)


def _surfaces(cfg: config.Config, stem: str) -> tuple[str, str | None, str | None, str]:
    """(database Title, title tag, initialkey, file name) of one track."""
    ((title,),) = _query(cfg, "SELECT Title FROM djmdContent WHERE ID = ?", _id(cfg, stem))
    path = _file(cfg, stem)
    read = tags.read_tags(path, ("title", "initialkey"))
    return title, read["title"], read["initialkey"], path.name


def _content(cfg: config.Config) -> dict[str, dict]:
    conn = sqlite3.connect(cfg.library.db_path)
    conn.row_factory = sqlite3.Row
    try:
        return {str(r["ID"]): dict(r) for r in conn.execute("SELECT * FROM djmdContent")}
    finally:
        conn.close()


def _analysis_bytes(cfg: config.Config) -> dict[str, str]:
    root = Path(cfg.library.root)
    return {
        str(path): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix in {".DAT", ".EXT", ".2EX", ".3EX"}
    }


def _decide(run_id: str, answer: str = "apply") -> None:
    decided, envelope = drive(["run", "decide", run_id, GATE, answer, "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope


def _two_acts(argv: list[str] = VERB) -> tuple[int, dict, dict]:
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    _decide(refused["run_id"])
    code, acted = drive(["--run", refused["run_id"], *argv])
    return code, acted, refused


def _items(envelope: dict) -> dict[str, dict]:
    return {item["title"].rsplit(" - ", 1)[-1]: item for item in envelope["data"]["items"]}


#: The visit of 2026-11-22 in miniature: a far key, a one step key, an equal one,
#: a tempo a beat off, one two off, a dyn style average, both wrong, a four to
#: three error.
LANDED = {
    "Alpha": "01A - 124",
    "Bravo": "01A - 124",
    "Charlie": "01A - 124",
    "Delta": "05A - 124",
    "Echo": "05A - 124",
    "Foxtrot": "05A - 124",
    "Golf": "01A - 124",
    "Hotel": "08A - 107",
}
VISITED = {
    "Alpha": ("7B", 12400),
    "Bravo": ("2A", 12400),
    "Charlie": ("1A", 12400),
    "Delta": ("5A", 12500),
    "Echo": ("5A", 12600),
    "Foxtrot": ("5A", 12484),
    "Golf": ("Em", 9800),
    "Hotel": ("08A", 8000),
}
AFTER = {
    "Alpha": "07B - 124 - Alpha",
    "Bravo": "02A - 124 - Bravo",
    "Charlie": "01A - 124 - Charlie",
    "Delta": "05A - 124 - Delta",
    "Echo": "05A - 126 - Echo",
    "Foxtrot": "05A - 124 - Foxtrot",
    "Golf": "09A - 98 - Golf",
    "Hotel": "08A - 80 - Hotel",
}


def _landed_and_visited(cfg: config.Config, silence: Path) -> None:
    _land_headed(cfg, silence, "2026-11-22_visit", LANDED)
    for stem, (scale, bpm) in VISITED.items():
        _visit(cfg, stem, scale=scale, bpm=bpm)


def test_the_plan_shows_each_row_before_and_after_with_its_key_relation_and_tempo(
    native_library, silence
):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)

    code, refused = drive(VERB)

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    with plan_handle(cfg) as found:
        items = {item.title.rsplit(" - ", 1)[-1]: item for item in found.items}
    assert {stem: item.new_title for stem, item in items.items()} == AFTER
    assert {stem: item.action for stem, item in items.items()} == {
        stem: ha.AGREE if stem in ("Charlie", "Delta", "Foxtrot") else ha.ADOPT for stem in AFTER
    }
    assert items["Alpha"].relation == rc.KEY_FAR
    assert items["Bravo"].relation == rc.KEY_ONE_STEP
    assert items["Charlie"].relation == rc.KEY_EQUAL
    assert (items["Foxtrot"].tempo_hundredths, items["Foxtrot"].tempo) == (12484, 125)
    assert (items["Hotel"].head_tempo, items["Hotel"].tempo) == (107, 80)
    # The title tag is planned off its own head, and the key tag set to rekordbox's.
    assert items["Golf"].new_tag_title == "09A - 98 - Golf"
    assert items["Golf"].new_initialkey == "09A"
    assert items["Echo"].new_initialkey == "05A"


class plan_handle:  # noqa: N801 - a context manager read as a phrase
    """The plan the verb reads, off a read handle, for a test to look inside."""

    def __init__(self, cfg: config.Config, **args):
        self.cfg = cfg
        self.args = SimpleNamespace(pass_name=None, session_id=None, leave=[], **args)

    def __enter__(self) -> ha.AdoptPlan:
        from cratekit.core import active_taxonomy

        return head_adopt_cli.read_plan(
            self.cfg,
            self.args,
            declared=active_taxonomy.load(self.cfg),
            template=check_cli.template_of(self.cfg),
        )

    def __exit__(self, *exc) -> None:
        return None


def test_the_apply_writes_title_title_tag_and_key_tag_and_nothing_else(native_library, silence):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    before = _content(cfg)
    grids = _analysis_bytes(cfg)
    names = {stem: _surfaces(cfg, stem)[3] for stem in LANDED}

    code, acted, _refused = _two_acts()

    assert code == int(ExitCode.OK), acted
    after = _content(cfg)
    changed = {
        content_id: sorted(
            column
            for column in after[content_id]
            if column not in rb_writer.BOOKKEEPING_COLUMNS
            and after[content_id][column] != before[content_id].get(column)
        )
        for content_id in after
    }
    written = {_id(cfg, stem) for stem in ("Alpha", "Bravo", "Echo", "Golf", "Hotel")}
    assert {cid: cols for cid, cols in changed.items() if cols} == {
        cid: ["Title"] for cid in written
    }
    for stem, title in AFTER.items():
        db_title, tag_title, initialkey, name = _surfaces(cfg, stem)
        assert (db_title, tag_title) == (title, title), stem
        # THE FILE NAME KEEPS ITS OLD HEAD: no verb renames a referenced file.
        assert name == names[stem]
    assert _surfaces(cfg, "Golf")[2] == "09A"
    # KeyID, the BPM column and every analysis file byte for byte.
    for content_id in after:
        for column in ("KeyID", "BPM", "Analysed", "AnalysisDataPath"):
            assert after[content_id][column] == before[content_id][column]
    assert _analysis_bytes(cfg) == grids
    totals = acted["data"]["totals"]
    assert (totals["written"], totals["read_back"]) == (5, 5)
    codes = [warning["code"] for warning in acted["warnings"]]
    assert codes[0] == head_adopt_cli.HEADS_WRITTEN


def test_no_tempo_tag_or_grid_reaches_a_file_the_verb_wrote(native_library, silence):
    """R17 on the file surface: the head's text changes, and no tempo key appears."""
    import mutagen

    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    for stem in LANDED:
        handle = mutagen.File(_file(cfg, stem))
        keys = {str(key).lower() for key in (handle.tags or {}).keys()}
        assert not keys & {"bpm", "tbpm", "tmpo", "averagebpm", "beatgrid"}, (stem, keys)


def test_the_record_keeps_every_surface_s_old_value_for_a_restore(native_library, silence):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    (record,) = [r for r in session.records(cfg) if r.workflow == ha.WORKFLOW]
    kept = {entry["content_id"]: entry for entry in record.detail[ha.RECORD_KEY]}
    golf = kept[_id(cfg, "Golf")]
    assert (golf["title"], golf["tag_title"], golf["initialkey"]) == (
        "01A - 124 - Golf",
        "01A - 124 - Golf",
        "",
    )
    assert golf["path"] == str(_file(cfg, "Golf"))
    assert len(kept) == 5
    assert record.snapshot_path


def test_a_second_run_plans_nothing_still_asks_and_ends_no_op(native_library, silence):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    before = _content(cfg)

    code, again, refused = _two_acts()

    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    assert again["warnings"][0]["code"] == head_adopt_cli.NOTHING_TO_WRITE
    assert refused["cause"]["detail"]["gate"] == GATE
    assert _content(cfg) == before
    assert len([r for r in session.records(cfg) if r.workflow == ha.WORKFLOW]) == 1


def test_leave_holds_a_row_out_in_the_plan_and_on_the_apply(native_library, silence):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    golf = _id(cfg, "Golf")

    code, acted, _refused = _two_acts([*VERB, "--leave", golf, "--leave", "no-such-row"])

    assert code == int(ExitCode.OK), acted
    assert _surfaces(cfg, "Golf")[:2] == ("01A - 124 - Golf", "01A - 124 - Golf")
    assert _surfaces(cfg, "Alpha")[0] == "07B - 124 - Alpha"
    held = {item["content_id"]: item for item in acted["data"]["items"]}[golf]
    assert (held["action"], held["reason"], held["new_title"]) == (
        ha.LEAVE_ACTION,
        ha.HELD_OUT,
        "09A - 98 - Golf",
    )
    codes = [warning["code"] for warning in acted["warnings"]]
    assert head_adopt_cli.LEAVE_UNMATCHED in codes and head_adopt_cli.ROWS_LEFT in codes


def test_the_same_leave_is_needed_on_the_run_that_applies(native_library, silence):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    golf = _id(cfg, "Golf")
    code, refused = drive([*VERB, "--leave", golf])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    _decide(refused["run_id"])
    before = _content(cfg)

    code, stale = drive(["--run", refused["run_id"], *VERB])

    assert stale["cause"]["reason"] == "decision-stale", stale
    assert _content(cfg) == before


def test_a_title_changed_between_plan_and_apply_refuses_and_writes_nothing(native_library, silence):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    code, refused = drive(VERB)
    _decide(refused["run_id"])
    with sqlite3.connect(cfg.library.db_path) as conn:
        conn.execute(
            "UPDATE djmdContent SET BPM = 13000 WHERE ID = ?", (_id(cfg, "Alpha"),)
        )
    conn.close()
    before = _content(cfg)
    tagged = _surfaces(cfg, "Golf")

    code, stale = drive(["--run", refused["run_id"], *VERB])

    assert stale["cause"]["reason"] == "decision-stale", stale
    assert _content(cfg) == before and _surfaces(cfg, "Golf") == tagged
    assert not [r for r in session.records(cfg) if r.workflow == ha.WORKFLOW]


def test_a_plan_that_moves_on_the_write_handle_refuses_before_any_file(native_library, silence, monkeypatch):
    """The plan taken again on the write handle is the last word: a file gone between
    the gate's check and the write handle's plan refuses, and no file is written."""
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    code, refused = drive(VERB)
    _decide(refused["run_id"])
    gone = _file(cfg, "Hotel")
    tagged = _surfaces(cfg, "Golf")
    real = head_adopt_cli.scope_and_plan
    calls: list[int] = []

    def plan_then_lose_a_file(*args, **kwargs):
        calls.append(1)
        if len(calls) == 2:
            gone.unlink()
        return real(*args, **kwargs)

    monkeypatch.setattr(head_adopt_cli, "scope_and_plan", plan_then_lose_a_file)
    code, stale = drive(["--run", refused["run_id"], *VERB])

    assert stale["cause"]["reason"] == "decision-stale", stale
    assert _id(cfg, "Hotel") in stale["cause"]["detail"]["moved"]
    assert _surfaces(cfg, "Golf") == tagged
    assert not [r for r in session.records(cfg) if r.workflow == ha.WORKFLOW]


def test_a_file_gone_before_the_plan_is_left_and_named(native_library, silence):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    _file(cfg, "Hotel").unlink()
    with plan_handle(cfg) as found:
        items = {item.title.rsplit(" - ", 1)[-1]: item for item in found.items}
    assert (items["Hotel"].action, items["Hotel"].reason) == (ha.LEAVE_ACTION, ha.FILE_MISSING)
    assert found.counts[ha.FILE_MISSING] == 1


def test_a_missing_key_never_stops_the_tempo_nor_a_missing_tempo_the_key(native_library, silence):
    cfg, _root = native_library
    _land_headed(
        cfg, silence, "2026-11-22_halves",
        {"Kilo": "01A - 124", "Lima": "01A - 124", "Mike": "01A - 124", "November": "01A - 124"},
    )
    _visit(cfg, "Kilo", scale=None, bpm=14000)
    _visit(cfg, "Lima", scale="6A", bpm=0)
    _visit(cfg, "Mike", scale=None, bpm=0)
    _visit(cfg, "November", scale="Lydian", bpm=12400)

    with plan_handle(cfg) as found:
        items = {item.title.rsplit(" - ", 1)[-1]: item for item in found.items}

    assert (items["Kilo"].action, items["Kilo"].new_title) == (ha.ADOPT, "01A - 140 - Kilo")
    assert items["Kilo"].notes == (ha.KEY_EMPTY,) and items["Kilo"].new_initialkey == ""
    assert (items["Lima"].action, items["Lima"].new_title) == (ha.ADOPT, "06A - 124 - Lima")
    assert items["Lima"].notes == (ha.TEMPO_ZERO,)
    assert (items["Mike"].action, items["Mike"].reason) == (ha.LEAVE_ACTION, ha.NO_REFERENCE)
    assert (items["November"].action, items["November"].notes) == (ha.AGREE, (ha.KEY_NOT_CAMELOT,))
    assert dict(found.notes) == {ha.KEY_EMPTY: 2, ha.KEY_NOT_CAMELOT: 1, ha.TEMPO_ZERO: 2}


def test_rows_not_analysed_with_no_head_or_a_differing_tag_are_left_and_named(
    native_library, silence
):
    cfg, _root = native_library
    _land_headed(
        cfg, silence, "2026-11-22_left",
        {"Oscar": "01A - 124", "Papa": "01A - 124", "Quebec": "01A - 124"},
    )
    _visit(cfg, "Oscar", scale="6A", bpm=12400, analysed=False)
    _visit(cfg, "Papa", scale="6A", bpm=12400)
    _visit(cfg, "Quebec", scale="6A", bpm=12400)
    # Papa's tag spells another body. Quebec's row lost its head by hand while its
    # tag kept one, so the tag is another title and the row is never stamped
    # (U342); a title the engine could not stamp and read back is no head.
    assert tags.write_tags(_file(cfg, "Papa"), {"title": "01A - 124 - Papa (Edit)"})
    quebec = _id(cfg, "Quebec")
    with sqlite3.connect(cfg.library.db_path) as conn:
        conn.execute("UPDATE djmdContent SET Title = 'Quebec' WHERE ID = ?", (quebec,))
    conn.close()

    with plan_handle(cfg) as found:
        reasons = {item.title: item.reason for item in found.items}

    assert reasons == {
        "01A - 124 - Oscar": ha.NOT_ANALYSED,
        "01A - 124 - Papa": ha.TAG_DIFFERS,
        "Quebec": ha.TAG_DIFFERS,
    }
    with sqlite3.connect(cfg.library.db_path) as conn:
        conn.execute("UPDATE djmdContent SET Title = ' Quebec' WHERE ID = ?", (quebec,))
    conn.close()
    with plan_handle(cfg) as found:
        reasons = {item.title: item.reason for item in found.items}
    assert reasons[" Quebec"] == ha.NO_HEAD
    assert found.writes == ()


def test_a_file_already_corrected_is_continued_by_planning_again(native_library, silence):
    """A run stopped after the files and before the rows: the file reads as planned,
    so only the row is written, and the key tag already right is left."""
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    assert tags.write_tags(_file(cfg, "Golf"), {"title": "09A - 98 - Golf", "initialkey": "9A"})

    with plan_handle(cfg) as found:
        golf = {item.title.rsplit(" - ", 1)[-1]: item for item in found.items}["Golf"]

    assert golf.action == ha.ADOPT and golf.writes_title and not golf.writes_file
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    assert _surfaces(cfg, "Golf")[:3] == ("09A - 98 - Golf", "09A - 98 - Golf", "9A")


def test_the_scope_is_never_the_back_catalogue_unasked(native_library, silence):
    """INBOX / Analyze emptied by the clear: the default scope is empty, and the
    landing's session still reaches the rows, as the visit of 2026-11-22 needs."""
    cfg, root_id = native_library
    _landed_and_visited(cfg, silence)
    from cratekit.intake import native

    ((analyze,),) = _query(
        cfg, "SELECT ID FROM djmdPlaylist WHERE Name = ? AND ParentID = ?", native.ANALYZE, root_id
    )
    with sqlite3.connect(cfg.library.db_path) as conn:
        conn.execute("UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE PlaylistID = ?", (analyze,))
        # A back catalogue row rekordbox has not analysed, which the check would read.
        conn.execute("UPDATE djmdContent SET Analysed = 0 WHERE ID = '1'")
    conn.close()

    with plan_handle(cfg) as found:
        assert (found.scope.kind, found.items) == (rc.SCOPE_ANALYZE, ())
    (landing,) = [
        r.session_id for r in session.records(cfg) if r.workflow == native.WORKFLOW
    ]
    code, acted, _refused = _two_acts([*VERB, "--session", landing])
    assert code == int(ExitCode.OK), acted
    assert _surfaces(cfg, "Golf")[0] == "09A - 98 - Golf"


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(unacknowledged, silence):
    code, envelope = drive(VERB)
    assert envelope["cause"]["reason"] == "backup-acknowledgment-missing", envelope
    assert code != int(ExitCode.OK)
    assert "gate" not in (envelope["cause"].get("detail") or {})
    assert not gates.run_path(envelope["run_id"]).exists()


def test_the_gate_takes_no_inline_answer(native_library, silence):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    before = _content(cfg)
    code, refused = drive(["-d", f"{GATE}=apply", *VERB])
    assert code != int(ExitCode.OK), refused
    assert _content(cfg) == before


def test_an_empty_plan_still_asks(native_library, silence):
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    _decide(refused["run_id"])
    code, acted = drive(["--run", refused["run_id"], *VERB])
    assert code == int(ExitCode.OK) and acted["outcome"] == "no_op", acted


def test_the_verb_declares_its_explicit_gate_and_the_analysis_module():
    entry = registry.entry("analyze.adopt")
    (confirm,) = [spec for spec in entry.gates if spec.name == GATE]
    assert confirm.explicit is True and confirm.digest_source == "plan"
    assert registry.CLOUD_SYNC_UNREADABLE_GATE in entry.gates
    assert entry.module_id == "analysis" and entry.extras is None
    assert entry.writes == frozenset({"files", "db_metadata"})


def test_the_operation_owns_title_alone_and_never_the_key_or_tempo():
    metadata.enable((metadata.ADOPT_REKORDBOX_HEAD,))
    policy = rb_writer.registered_field_policies()[metadata.ADOPT_REKORDBOX_HEAD]
    assert dict(policy.fields) == {"Title": rb_writer.Ownership.OWNED}
    for column in ("KeyID", "BPM", "FileNameL", "FolderPath"):
        assert (
            rb_writer.metadata_decision(metadata.ADOPT_REKORDBOX_HEAD, column, None, "x")
            is rb_writer.Decision.SKIP_UNOWNED
        )


# 3. What runs after: the check and name apply; restamp is in
# tests/test_analysis_workers.py, beside the restamp it drives


def test_the_check_after_the_adopt_reads_every_title_equal(native_library, silence):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    code, before = drive(["analyze", "check"])
    assert code == int(ExitCode.OK), before
    assert before["data"]["summary"]["differs"] == 5
    detail = [c for c in before["data"]["checks"] if c["key"] == "check.key_agreement"][0]
    assert detail["status"] == "info" and check_cli.ADOPT_VERB in detail["detail"]

    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted

    code, after = drive(["analyze", "check"])
    summary = after["data"]["summary"]
    assert (summary["differs"], summary["tempo_differs"]) == (0, 0)
    assert summary["key_agreement"][rc.KEY_EQUAL] == len(LANDED)


def test_a_full_library_name_apply_after_the_adopt_brings_nothing_back(native_library, silence):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    surfaces = {stem: _surfaces(cfg, stem) for stem in LANDED}

    argv = ["name", "apply", "--root", str(Path(cfg.library.root))]
    code, planned = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), planned
    decided, envelope = drive(
        ["run", "decide", planned["run_id"], "name.apply.confirm", "apply", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, applied = drive(["--run", planned["run_id"], *argv])
    assert code == int(ExitCode.OK), applied
    # A CORRECTED TRACK RENDERS UNDER ITS TITLE'S HEAD, so it is a candidate the
    # collection holds back, and one that agrees renders as it is named.
    held = sorted(Path(item["path"]).name for item in applied["data"]["items"])
    assert held == sorted(surfaces[stem][3] for stem in ("Alpha", "Bravo", "Echo", "Golf", "Hotel"))
    assert {item["action"] for item in applied["data"]["items"]} == {"referenced"}
    assert applied["data"]["totals"]["renamed"] == 0
    assert {stem: _surfaces(cfg, stem) for stem in LANDED} == surfaces


# 4. The guard under the write, driven


def test_a_plan_that_would_write_the_tempo_column_is_refused_by_policy(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    before = _content(cfg)
    real = ha.row_changes

    def with_a_tempo(items):
        plan = real(items)
        sneaked = metadata.Change(plan.changes[0].content_id, plan.owner, "BPM", 12400, 12800)
        return metadata.Plan(plan.owner, (*plan.changes, sneaked))

    monkeypatch.setattr(ha, "row_changes", with_a_tempo)
    tagged = {stem: _surfaces(cfg, stem) for stem in LANDED}
    code, acted, _refused = _two_acts()

    assert acted["cause"]["reason"] == "refused-by-policy", acted
    assert _content(cfg) == before
    # ASKED BEFORE THE FIRST FILE: no title tag or key tag moved either.
    assert {stem: _surfaces(cfg, stem) for stem in LANDED} == tagged


def test_a_tempo_set_on_the_row_behind_the_policy_is_refused_at_the_commit(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    before = _content(cfg)
    real = metadata.write_plan

    def and_the_tempo(plan, rows_by_id, **kwargs):
        report = real(plan, rows_by_id, **kwargs)
        for row in rows_by_id.values():
            row.BPM = 12800
        return report

    monkeypatch.setattr(metadata, "write_plan", and_the_tempo)
    code, acted, _refused = _two_acts()

    assert code != int(ExitCode.OK), acted
    assert "BPM" in acted["cause"]["message"], acted
    assert _content(cfg) == before


# 5. A file that does not take, and the row read back


def test_a_file_that_cannot_be_written_keeps_its_row_s_title_and_is_named(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    golf = _file(cfg, "Golf")
    real = tags.write_tags

    def refuses_golf(path, fields):
        return False if Path(path) == golf else real(path, fields)

    monkeypatch.setattr(tags, "write_tags", refuses_golf)
    _file(cfg, "Hotel").write_bytes(b"not audio at all")
    code, acted, _refused = _two_acts()

    # THE REST LANDED AND THE RUN SAYS IT IS NOT WHOLE: never an ok exit.
    assert code == int(ExitCode.PRECONDITION), acted
    cause = acted["cause"]
    assert cause["reason"] == head_adopt_cli.UNWRITTEN
    assert "1 could not be written: 01A - 124 - Golf" in cause["message"]
    assert "3 row(s)" in cause["message"]
    assert cause["detail"]["failed"] == [_id(cfg, "Golf")]
    # EVERY ADVISORY KEPT ON THE REFUSAL (review round two): what was written is
    # said first, and a row left for its file is named as on every other path.
    codes = [warning["code"] for warning in acted["warnings"]]
    assert codes[:2] == [head_adopt_cli.HEADS_WRITTEN, head_adopt_cli.ROWS_LEFT], codes
    assert "08A - 107 - Hotel (file-unreadable)" in acted["warnings"][1]["message"]
    assert _surfaces(cfg, "Golf")[:3] == ("01A - 124 - Golf", "01A - 124 - Golf", None)
    assert _surfaces(cfg, "Alpha")[:2] == ("07B - 124 - Alpha", "07B - 124 - Alpha")


def test_a_file_that_does_not_read_back_keeps_its_row_s_title_and_is_named(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    golf = _file(cfg, "Golf")
    real = tags.write_tags

    def says_it_wrote_golf(path, fields):
        return True if Path(path) == golf else real(path, fields)

    monkeypatch.setattr(tags, "write_tags", says_it_wrote_golf)
    code, acted, _refused = _two_acts()

    assert code == int(ExitCode.PRECONDITION), acted
    assert acted["cause"]["reason"] == head_adopt_cli.UNWRITTEN
    assert "1 do not read back as written: 01A - 124 - Golf" in acted["cause"]["message"]
    assert acted["cause"]["detail"]["wrong"] == [_id(cfg, "Golf")]
    assert _surfaces(cfg, "Golf")[0] == "01A - 124 - Golf"


def test_the_read_back_names_a_title_not_carried_and_a_column_moved():
    item = ha.Item("1", ha.ADOPT, title="01A - 124 - A", new_title="07B - 124 - A")
    before = {"1": {"ID": "1", "Title": "01A - 124 - A", "BPM": 12400, "updated_at": "a"}}

    def now(**columns):
        return {"1": {**before["1"], "updated_at": "b", **columns}}

    assert ha.judge([item], before, now(Title="07B - 124 - A")) == ((), ())
    wrong, moved = ha.judge([item], before, now())
    assert wrong == ("1: reads '01A - 124 - A', not '07B - 124 - A'",) and moved == ()
    wrong, moved = ha.judge([item], before, now(Title="07B - 124 - A", BPM=12800))
    assert (wrong, moved) == ((), ("1: BPM",))
    wrong, moved = ha.judge([item], before, now(BPM=12800))
    assert wrong and moved
    assert ha.judge([item], before, {})[0] == ("1: the row could not be read",)


def test_a_read_back_wrong_or_moved_refuses_naming_the_session_that_undoes_it():
    ha.assert_read_back(ha.Written(session_id="s-1", written=1, read_back=1))
    with pytest.raises(CratekitError) as wrong:
        ha.assert_read_back(ha.Written(session_id="s-1", written=1, read_back=0, wrong=("1: x",)))
    assert wrong.value.cause.reason == "internal-error"
    assert "restore session s-1" in " ".join(wrong.value.cause.remediation.steps)
    with pytest.raises(CratekitError) as moved:
        ha.assert_read_back(
            ha.Written(session_id="s-1", written=1, read_back=1, moved=("1: BPM",))
        )
    assert moved.value.cause.reason == "whitelist-violation"
    # BOTH AT ONCE: the moved column outranks the title not carried.
    with pytest.raises(CratekitError) as both:
        ha.assert_read_back(
            ha.Written(session_id="s-1", written=1, read_back=0, wrong=("1: x",), moved=("1: BPM",))
        )
    assert both.value.cause.reason == "whitelist-violation"


def test_an_intake_tree_that_cannot_be_read_refuses_before_the_gate(library, monkeypatch, silence):
    """Review rounds one and two, B1: INBOX / Analyze that was never read is never an
    empty plan. The intake tree still on the xml bridge refuses with its own reason."""
    cfg = _configured(library, monkeypatch, profile="full")
    session.record_acknowledgment(cfg, terminal=lambda: True)

    code, refused = drive(VERB)

    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert "xml bridge" in refused["cause"]["message"], refused
    assert "gate" not in (refused["cause"].get("detail") or {})
    assert not gates.run_path(refused["run_id"]).exists()


def test_an_empty_inbox_analyze_says_why_nothing_was_planned(native_library):
    """Read and empty: the plan is empty, the gate asks, and the answer says why."""
    code, acted, refused = _two_acts()

    assert code == int(ExitCode.OK) and acted["outcome"] == "no_op", acted
    codes = [warning["code"] for warning in acted["warnings"]]
    assert codes == [head_adopt_cli.NOTHING_TO_WRITE, head_adopt_cli.SCOPE_EMPTY]
    assert "holds no row in scope" in acted["warnings"][0]["message"]
    (shown,) = refused["cause"]["detail"]["shown"]["unread"]
    assert f"no {native.ANALYZE} playlist" in shown or "holds no row" in shown


def test_session_records_the_log_could_not_read_are_said(native_library, silence, monkeypatch):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    (landing,) = [r.session_id for r in session.records(cfg) if r.workflow == native.WORKFLOW]
    real = rc.resolve_scope

    def with_one_unread(*args, **kwargs):
        from dataclasses import replace

        return replace(real(*args, **kwargs), unreadable_records=1)

    monkeypatch.setattr(rc, "resolve_scope", with_one_unread)
    code, refused = drive([*VERB, "--session", landing])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    (shown,) = refused["cause"]["detail"]["shown"]["unread"]
    assert "1 session record(s) could not be read" in shown


def test_a_row_gone_from_the_collection_or_with_an_unreadable_file_is_left_and_named(
    native_library, silence
):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    _file(cfg, "Hotel").write_bytes(b"not audio at all")
    alpha = _id(cfg, "Alpha")
    with sqlite3.connect(cfg.library.db_path) as conn:
        conn.execute("UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", (alpha,))
    conn.close()

    with plan_handle(cfg) as found:
        reasons = {item.content_id: item.reason for item in found.items}

    assert reasons[alpha] == ha.GONE
    assert reasons[_id(cfg, "Hotel")] == ha.FILE_UNREADABLE
    assert alpha not in {item.content_id for item in found.writes}


def test_an_out_of_band_restore_is_looked_for_before_the_session_opens(
    native_library, silence, monkeypatch
):
    from cratekit.core import convergence
    from cratekit.core.cause import refuse

    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    tagged = {stem: _surfaces(cfg, stem) for stem in LANDED}
    before = _content(cfg)

    def restored(*args, **kwargs):
        raise refuse("tree-unconverged", "restored out of band", origin=("test",))

    monkeypatch.setattr(convergence, "detect_out_of_band_restore", restored)
    code, acted, _refused = _two_acts()

    assert acted["cause"]["reason"] == "tree-unconverged", acted
    assert _content(cfg) == before
    assert {stem: _surfaces(cfg, stem) for stem in LANDED} == tagged


def test_the_old_values_are_on_disk_before_the_first_file_is_written(
    native_library, silence, monkeypatch
):
    """A run killed at its first file leaves a record a person can put the files back from."""
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    seen: list[list] = []

    def crash(path, fields):
        (record,) = [r for r in session.records(cfg) if r.workflow == ha.WORKFLOW]
        seen.append(record.detail.get(ha.RECORD_KEY))
        raise RuntimeError("the process died here")

    monkeypatch.setattr(tags, "write_tags", crash)
    code, acted, _refused = _two_acts()

    assert code != int(ExitCode.OK), acted
    (kept,) = seen
    assert len(kept) == 5 and {entry["title"] for entry in kept} >= {"01A - 124 - Golf"}


def test_the_check_counts_only_a_title_whose_own_head_differs(native_library, silence):
    """Review round one, R4: a bare title beside a headed file name is not one
    ``analyze adopt`` corrects or stamps (it leaves it, its title tag differing), so
    the check does not name the verb for it, nor count it among the bare titles (U343)."""
    cfg, _root = native_library
    _land_headed(cfg, silence, "2026-11-22_bare", {"Romeo": "01A - 124"})
    _visit(cfg, "Romeo", scale="7B", bpm=9000)
    with sqlite3.connect(cfg.library.db_path) as conn:
        conn.execute("UPDATE djmdContent SET Title = 'Romeo' WHERE ID = ?", (_id(cfg, "Romeo"),))
    conn.close()

    code, checked = drive(["analyze", "check"])

    assert code == int(ExitCode.OK), checked
    assert checked["data"]["summary"]["differs"] == 0
    detail = [c for c in checked["data"]["checks"] if c["key"] == "check.key_agreement"][0]
    assert check_cli.ADOPT_VERB not in detail["detail"]
    assert checked["data"]["summary"]["headless"] == 0, "adopt leaves it, so it is not counted"


def test_a_commit_that_lands_and_then_raises_is_still_recorded(native_library, silence, monkeypatch):
    """The witness, not the exception, says whether the rows landed: a commit that
    lands and then raises keeps its record, so a restore knows to undo it."""
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    real = rb_writer.commit_guarded

    def lands_then_raises(db, *args, **kwargs):
        real(db, *args, **kwargs)
        raise RuntimeError("the connection dropped after the commit")

    monkeypatch.setattr(rb_writer, "commit_guarded", lands_then_raises)
    code, acted, _refused = _two_acts()

    assert code != int(ExitCode.OK), acted
    (record,) = [r for r in session.records(cfg) if r.workflow == ha.WORKFLOW]
    assert record.sources == {ha.CHANGE_KEY: str(session.SourceState.COMMITTED)}
    assert _surfaces(cfg, "Golf")[0] == "09A - 98 - Golf"


def test_a_commit_that_raises_before_landing_records_no_commit(native_library, silence, monkeypatch):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)

    def refuses(db, *args, **kwargs):
        raise RuntimeError("the database is locked")

    monkeypatch.setattr(rb_writer, "commit_guarded", refuses)
    code, acted, _refused = _two_acts()

    assert code != int(ExitCode.OK), acted
    (record,) = [r for r in session.records(cfg) if r.workflow == ha.WORKFLOW]
    assert ha.CHANGE_KEY not in record.sources
    assert _surfaces(cfg, "Golf")[0] == "01A - 124 - Golf"


def test_a_bare_title_s_tempo_is_not_counted_as_differing(native_library, silence):
    """Review round two: the tempo count is scoped to a title's own head as the
    differing count is."""
    cfg, _root = native_library
    _land_headed(cfg, silence, "2026-11-22_bare", {"Romeo": "01A - 124"})
    _visit(cfg, "Romeo", scale="1A", bpm=9000)
    with sqlite3.connect(cfg.library.db_path) as conn:
        conn.execute("UPDATE djmdContent SET Title = 'Romeo' WHERE ID = ?", (_id(cfg, "Romeo"),))
    conn.close()

    code, checked = drive(["analyze", "check"])

    assert code == int(ExitCode.OK), checked
    summary = checked["data"]["summary"]
    assert (summary["differs"], summary["tempo_differs"]) == (0, 0)


# U342: a title with no head is given one built from rekordbox's key and tempo.


def _land_bare(cfg: config.Config, silence: Path, batch: str, titles: dict[str, str]) -> None:
    """Stage each track with no head in its file name or title tag, then land, as a
    landing that wrote no head before the visit leaves it."""
    for stem, title in titles.items():
        path = _staging(cfg) / f"{stem}.flac"
        shutil.copyfile(silence, path)
        assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
    code, acted, _refused = _land_acts(["intake", "land", "--name", batch])
    assert code == int(ExitCode.OK), acted


#: Bare titles: a plain one, the lossy marker, and bodies that begin like a head.
BARE = {
    "Sierra": "Sierra",
    "Tango": "[MP3] Tango",
    "Uniform": "1A - Uniform",
    "Victor": "124 - Victor",
}
BARE_VISITED = {
    "Sierra": ("6A", 12400),
    "Tango": ("Em", 9850),
    "Uniform": ("12B", 12049),
    "Victor": ("3A", 17000),
}
STAMPED = {
    "Sierra": "06A - 124 - Sierra",
    "Tango": "09A - 99 - [MP3] Tango",
    "Uniform": "12B - 120 - 1A - Uniform",
    "Victor": "03A - 170 - 124 - Victor",
}


def _bare_and_visited(cfg: config.Config, silence: Path) -> None:
    _land_bare(cfg, silence, "2026-11-23_bare", BARE)
    for stem, (scale, bpm) in BARE_VISITED.items():
        _visit(cfg, stem, scale=scale, bpm=bpm)


@pytest.mark.parametrize(
    ("title", "key", "tempo", "expected"),
    [
        pytest.param("Sierra", "06A", 124, "06A - 124 - Sierra", id="plain"),
        pytest.param("Sierra", "6A", 124, "06A - 124 - Sierra", id="the-key-padded"),
        pytest.param("[MP3] Tango", "09A", 99, "09A - 99 - [MP3] Tango", id="the-marker-kept"),
        pytest.param("[MP3]Tango", "09A", 99, "09A - 99 - [MP3]Tango", id="every-marker-byte"),
        pytest.param("1A - Uniform", "12B", 120, "12B - 120 - 1A - Uniform", id="a-key-led-body"),
        pytest.param(
            "08A - 124 Victor", "03A", 170, "03A - 170 - 08A - 124 Victor", id="a-near-head-body"
        ),
        pytest.param("01A - 124 - Alpha", "06A", 124, None, id="a-head-already"),
        pytest.param(" Sierra", "06A", 124, None, id="a-body-that-would-not-read-back"),
        pytest.param("", "06A", 124, None, id="nothing-to-follow-the-head"),
        pytest.param("Sierra", "06A", 1000, None, id="a-tempo-no-head-carries"),
        pytest.param("Sierra", "13A", 124, None, id="a-key-off-the-wheel"),
        pytest.param("Victor - 06A - 124", "06A", 124, None, id="a-head-at-the-end"),
        pytest.param("[MP3]", "06A", 124, None, id="a-marker-and-nothing-after"),
        pytest.param("[MP3]  ", "06A", 124, None, id="a-marker-and-blanks"),
    ],
)
def test_a_title_with_no_head_is_stamped_and_keeps_every_byte(title, key, tempo, expected):
    stamped = stamp_head(title, key=key, bpm=tempo, template=TEMPLATE)
    assert stamped == expected
    if stamped is not None:
        assert stamped.endswith(title)
        assert parse_head(stamped, template=TEMPLATE) == {"key": stamped[:3], "bpm": str(tempo)}


def test_the_check_names_adopt_for_the_bare_titles_a_landing_since_u343_leaves(
    native_library, silence
):
    """U343: a run writes no head, so every landed title is bare after the visit, and
    the check counts each and names the verb that stamps it; none reads as suspect."""
    cfg, _root = native_library
    _bare_and_visited(cfg, silence)

    code, checked = drive(["analyze", "check"])

    assert code == int(ExitCode.OK), checked
    summary = checked["data"]["summary"]
    assert summary["verdict"] == rc.DONE and summary["differs"] == 0
    assert summary["headless"] == len(BARE)
    assert summary["key_agreement"][rc.KEY_UNKEYED] == len(BARE)
    (line,) = [c for c in checked["data"]["checks"] if c["key"] == "check.key_agreement"]
    assert line["status"] == "info"
    assert (
        f"; {len(BARE)} title(s) rekordbox keyed carry no head, and {check_cli.ADOPT_VERB} "
        f"gives each it can one built from rekordbox's key and tempo, naming any it leaves: "
    ) in line["detail"]
    for title in BARE.values():
        assert title in line["detail"], title

    drive(VERB)
    with plan_handle(cfg) as found:
        stamped = {item.title for item in found.items if item.action == ha.STAMPED}
    assert stamped == set(BARE.values()), "the rows the check names are the rows adopt stamps"


def test_a_file_with_no_title_tag_is_titled_by_the_run_so_adopt_stamps_it_after_the_visit(
    native_library, silence, monkeypatch
):
    """U343 review round one: the run writes no head, so it gives a file with no title
    tag its stem as one, the title the landing lands; adopt then stamps that row, as
    a run before U343, which wrote a headed title on every file, let it."""
    import numpy as np

    from cratekit.analysis import energy, light, vocals
    from tests.test_analysis import _FakeModel

    cfg, _root = native_library
    monkeypatch.setattr(light, "_DETECT", lambda path: {
        "path": path, "rate": 124, "energy": 6, "energy_status": energy.STATUS_CALIBRATED,
    })
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", _FakeModel)
    monkeypatch.setattr(vocals, "_DECODER", lambda path: np.full(16000, 0.2, dtype=np.float32))
    staging = _staging(cfg)
    untitled = staging / "Probe - Whiskey.flac"
    titled = staging / "Probe - Xray.flac"
    for path, fields in ((untitled, {}), (titled, {"title": "Xray"})):
        shutil.copyfile(silence, path)
        assert tags.write_tags(path, {"artist": "Probe", "genre": "Deep House", **fields})

    code, ran = drive(["analyze", "run", str(staging)])
    assert code == int(ExitCode.OK), ran
    assert tags.read_tag(untitled, "title") == "Probe - Whiskey", "the stem, with no head"
    assert tags.read_tag(titled, "title") == "Xray", "a title already there is left alone"
    code, acted, _refused = _land_acts(["intake", "land", "--name", "2026-11-23_untitled"])
    assert code == int(ExitCode.OK), acted
    for stem in ("Whiskey", "Xray"):
        _visit(cfg, stem, scale="6A", bpm=12600)

    code, refused = drive(VERB)

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    with plan_handle(cfg) as found:
        planned = {item.title: (item.action, item.new_title) for item in found.items}
    assert planned == {
        "Probe - Whiskey": (ha.STAMPED, "06A - 126 - Probe - Whiskey"),
        "Xray": (ha.STAMPED, "06A - 126 - Xray"),
    }


def test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows(
    native_library, silence
):
    cfg, _root = native_library
    _landed_and_visited(cfg, silence)
    _bare_and_visited(cfg, silence)

    code, refused = drive(VERB)

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    with plan_handle(cfg) as found:
        items = {_stem(item.title): item for item in found.items}
    for stem, title in STAMPED.items():
        item = items[stem]
        assert (item.action, item.title, item.new_title) == (ha.STAMPED, BARE[stem], title), stem
        assert (item.tag_title, item.new_tag_title) == (BARE[stem], title), stem
        assert (item.head_key, item.head_tempo, item.relation) == (None, None, rc.KEY_UNKEYED)
        assert item.new_initialkey == title[:3]
    assert items["Alpha"].action == ha.ADOPT
    counts = refused["cause"]["detail"]["shown"]["outcomes"]
    assert (counts[ha.STAMPED], counts[ha.ADOPT], counts[ha.AGREE]) == (4, 5, 3)
    assert {item.content_id for item in found.writes} == {
        _id(cfg, stem) for stem in (*STAMPED, "Alpha", "Bravo", "Echo", "Golf", "Hotel")
    }


def _stem(title: str) -> str:
    """The stem a test landed under, off any head, marker or body prefix."""
    for stem in (*LANDED, *BARE, *UNANSWERED):
        if title.endswith(stem):
            return stem
    return title


def test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else(native_library, silence):
    import mutagen

    cfg, _root = native_library
    _bare_and_visited(cfg, silence)
    before = _content(cfg)
    grids = _analysis_bytes(cfg)
    names = {stem: _file(cfg, stem).name for stem in BARE}

    code, acted, _refused = _two_acts()

    assert code == int(ExitCode.OK), acted
    after = _content(cfg)
    changed = {
        content_id: sorted(
            column
            for column in after[content_id]
            if column not in rb_writer.BOOKKEEPING_COLUMNS
            and after[content_id][column] != before[content_id].get(column)
        )
        for content_id in after
    }
    assert {cid: cols for cid, cols in changed.items() if cols} == {
        _id(cfg, stem): ["Title"] for stem in BARE
    }
    for stem, title in STAMPED.items():
        db_title, tag_title, initialkey, name = _surfaces(cfg, stem)
        assert (db_title, tag_title, initialkey) == (title, title, title[:3]), stem
        # THE FILE NAME IS NEVER CHANGED: it keeps having no head.
        assert name == names[stem] == f"{stem}.flac"
        handle = mutagen.File(_file(cfg, stem))
        keys = {str(key).lower() for key in (handle.tags or {}).keys()}
        spelled = keys | {key.split(":", 1)[-1] for key in keys}
        assert not spelled & {key.lower() for key in FORBIDDEN_TAG_KEYS}, (stem, keys)
    for content_id in after:
        for column in ("KeyID", "BPM", "Analysed", "AnalysisDataPath", "FolderPath"):
            assert after[content_id][column] == before[content_id][column]
    assert _analysis_bytes(cfg) == grids
    assert (acted["data"]["totals"]["written"], acted["data"]["totals"]["read_back"]) == (4, 4)
    said = acted["warnings"][0]
    assert said["code"] == head_adopt_cli.HEADS_WRITTEN
    assert "4 of them a title that had no head" in said["message"]
    assert "no file is renamed" in said["message"]
    (record,) = [r for r in session.records(cfg) if r.workflow == ha.WORKFLOW]
    kept = {entry["content_id"]: entry for entry in record.detail[ha.RECORD_KEY]}
    tango = kept[_id(cfg, "Tango")]
    assert (tango["title"], tango["tag_title"], tango["initialkey"]) == (
        "[MP3] Tango", "[MP3] Tango", ""
    )


#: Headless rows rekordbox did not fully answer: never stamped half.
UNANSWERED = {
    "Whiskey": (None, 12400, (ha.KEY_EMPTY,)),
    "Xray": ("6A", 0, (ha.TEMPO_ZERO,)),
    "Yankee": (None, 0, (ha.KEY_EMPTY, ha.TEMPO_ZERO)),
    "Zulu": ("Lydian", 12400, (ha.KEY_NOT_CAMELOT,)),
}


def test_a_headless_row_rekordbox_did_not_key_or_time_is_left_and_named(native_library, silence):
    cfg, _root = native_library
    _land_bare(cfg, silence, "2026-11-23_unanswered", {stem: stem for stem in UNANSWERED})
    for stem, (scale, bpm, _notes) in UNANSWERED.items():
        _visit(cfg, stem, scale=scale, bpm=bpm)
    before = _content(cfg)

    code, acted, _refused = _two_acts()

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    items = {item["title"]: item for item in acted["data"]["items"]}
    for stem, (_scale, _bpm, notes) in UNANSWERED.items():
        item = items[stem]
        assert (item["action"], item["reason"], item["new_title"]) == (
            ha.LEAVE_ACTION, ha.NO_HEAD_UNANSWERED, stem
        ), stem
        assert tuple(item["notes"]) == notes, stem
    left = {warning["code"]: warning["message"] for warning in acted["warnings"]}
    assert "Yankee (no-head-unanswered: key-empty, tempo-zero)" in left[head_adopt_cli.ROWS_LEFT]
    assert "Zulu (no-head-unanswered: key-not-camelot)" in left[head_adopt_cli.ROWS_LEFT]
    assert head_adopt_cli.HALF_READ not in left
    assert _content(cfg) == before
    assert {stem: _surfaces(cfg, stem)[1] for stem in UNANSWERED} == {s: s for s in UNANSWERED}


def test_leave_holds_a_stamped_row_out_in_the_plan_and_on_the_apply(native_library, silence):
    cfg, _root = native_library
    _bare_and_visited(cfg, silence)
    sierra = _id(cfg, "Sierra")

    code, acted, _refused = _two_acts([*VERB, "--leave", sierra])

    assert code == int(ExitCode.OK), acted
    assert _surfaces(cfg, "Sierra")[:3] == ("Sierra", "Sierra", None)
    assert _surfaces(cfg, "Tango")[0] == STAMPED["Tango"]
    held = {item["content_id"]: item for item in acted["data"]["items"]}[sierra]
    assert (held["action"], held["reason"], held["new_title"]) == (
        ha.LEAVE_ACTION, ha.HELD_OUT, STAMPED["Sierra"]
    )
    assert head_adopt_cli.LEAVE_UNMATCHED not in [w["code"] for w in acted["warnings"]]


def test_a_stamped_row_moved_between_plan_and_apply_refuses_and_writes_nothing(
    native_library, silence
):
    cfg, _root = native_library
    _bare_and_visited(cfg, silence)
    code, refused = drive(VERB)
    _decide(refused["run_id"])
    with sqlite3.connect(cfg.library.db_path) as conn:
        conn.execute("UPDATE djmdContent SET BPM = 13000 WHERE ID = ?", (_id(cfg, "Sierra"),))
    conn.close()
    before = _content(cfg)
    tags_before = {stem: _surfaces(cfg, stem) for stem in BARE}

    code, stale = drive(["--run", refused["run_id"], *VERB])

    assert stale["cause"]["reason"] == "decision-stale", stale
    assert _content(cfg) == before
    assert {stem: _surfaces(cfg, stem) for stem in BARE} == tags_before


def test_a_second_run_after_a_stamp_plans_nothing_and_ends_no_op(native_library, silence):
    cfg, _root = native_library
    _bare_and_visited(cfg, silence)
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    before = _content(cfg)

    code, again, _refused = _two_acts()

    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    assert again["warnings"][0]["code"] == head_adopt_cli.NOTHING_TO_WRITE
    assert {item["action"] for item in again["data"]["items"]} == {ha.AGREE}
    assert _content(cfg) == before


def test_a_file_already_stamped_is_continued_by_planning_again(native_library, silence):
    """A run stopped after the files and before the rows: the tag already reads as
    the stamped title, so only the row is written."""
    cfg, _root = native_library
    _bare_and_visited(cfg, silence)
    assert tags.write_tags(_file(cfg, "Sierra"), {"title": STAMPED["Sierra"], "initialkey": "6A"})

    with plan_handle(cfg) as found:
        sierra = {_stem(item.title): item for item in found.items}["Sierra"]

    assert sierra.action == ha.STAMPED and sierra.writes_title and not sierra.writes_file
    code, acted, _refused = _two_acts()
    assert code == int(ExitCode.OK), acted
    assert _surfaces(cfg, "Sierra")[:3] == (STAMPED["Sierra"], STAMPED["Sierra"], "6A")


def test_a_headless_row_whose_tag_carries_another_title_is_left(native_library, silence):
    cfg, _root = native_library
    _bare_and_visited(cfg, silence)
    assert tags.write_tags(_file(cfg, "Sierra"), {"title": "Sierra (Edit)"})

    with plan_handle(cfg) as found:
        sierra = {_stem(item.title): item for item in found.items}["Sierra"]

    assert (sierra.action, sierra.reason) == (ha.LEAVE_ACTION, ha.TAG_DIFFERS)
    assert sierra.content_id not in {item.content_id for item in found.writes}


@pytest.mark.parametrize("suffix", tags.SUPPORTED_SUFFIXES)
def test_a_stamped_file_carries_the_tempo_as_text_and_no_tempo_tag_in_any_container(
    tmp_path, suffix
):
    """The gridless rule on the stamped path, in every container the tag module writes."""
    import mutagen

    from tests._containers import synth_container

    path = synth_container(tmp_path, suffix)
    assert tags.write_tags(path, {"title": "Sierra"})
    stamped = stamp_head("Sierra", key="06A", bpm=128, template=TEMPLATE)
    item = ha.Item(
        content_id="1", action=ha.STAMPED, path=str(path), title="Sierra",
        new_title=stamped, tag_title="Sierra", new_tag_title=stamped, new_initialkey="06A",
        key="06A", tempo=128,
    )

    written = ha.write_files([item])

    assert written.read_back == ("1",), written
    assert tags.read_tag(path, "title") == "06A - 128 - Sierra"
    handle = mutagen.File(path)
    held = {str(key) for key in (handle.tags or {}).keys()}
    spelled = {key.lower() for key in held} | {key.split(":", 1)[-1].lower() for key in held}
    assert not spelled & {key.lower() for key in FORBIDDEN_TAG_KEYS}, sorted(held)


def test_a_stamped_row_is_counted_written_and_never_as_left(native_library, silence, monkeypatch):
    """The rows left count names only rows left, never a stamped one, and the written
    message counts a stamped title only when its file took it."""
    cfg, _root = native_library
    _bare_and_visited(cfg, silence)
    _land_bare(cfg, silence, "2026-11-23_one_left", {"Whiskey": "Whiskey"})
    _visit(cfg, "Whiskey", scale=None, bpm=12400)
    tango = _file(cfg, "Tango")
    real = tags.write_tags

    def refuses_tango(path, fields):
        return False if Path(path) == tango else real(path, fields)

    monkeypatch.setattr(tags, "write_tags", refuses_tango)
    code, acted, _refused = _two_acts()

    assert acted["cause"]["reason"] == head_adopt_cli.UNWRITTEN, acted
    said = {warning["code"]: warning["message"] for warning in acted["warnings"]}
    assert said[head_adopt_cli.ROWS_LEFT].startswith(
        "1 of 5 row(s) were left alone (1 no-head-unanswered): "
    ), said[head_adopt_cli.ROWS_LEFT]
    assert _surfaces(cfg, "Tango")[:2] == ("[MP3] Tango", "[MP3] Tango")
    assert _surfaces(cfg, "Sierra")[0] == STAMPED["Sierra"]
    assert acted["data"]["totals"]["outcomes"][ha.STAMPED] == 4
    assert acted["data"]["totals"]["written"] == 3


def test_the_written_message_counts_only_stamped_files_that_took_it():
    plan_items = (
        ha.Item("1", ha.STAMPED, title="A", new_title="06A - 124 - A"),
        ha.Item("2", ha.STAMPED, title="B", new_title="06A - 124 - B"),
        ha.Item("3", ha.ADOPT, title="01A - 124 - C", new_title="06A - 124 - C"),
    )
    plan = ha.AdoptPlan(
        scope=rc.Scope(kind=rc.SCOPE_ANALYZE, name="INBOX / Analyze", content_ids=("1", "2", "3")),
        items=plan_items,
        counts={},
        notes={},
    )
    written = ha.Written(
        session_id="s", written=2, read_back=2, files=ha.FilesWritten(read_back=("1", "3"))
    )
    message = head_adopt_cli._written(plan, written)["message"]
    assert "2 file(s) carry rekordbox's key and tempo" in message
    assert "1 of them a title that had no head" in message
