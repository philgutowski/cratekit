"""U39: ``name.apply`` carries an existing head through instead of destroying it.

Every test drives the real dispatcher over real audio files. The tempo is text,
parsed from the filename and the title, and lands in those alone, never a tag.
"""

from __future__ import annotations

import io
import json
import unicodedata
from pathlib import Path

import mutagen
import pytest
from pyrekordbox.db6 import tables
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from cratekit import cli
from cratekit.core import config, locations, naming, rb_writer, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.write import naming_cli
from cratekit.write.naming_cli import _template
from tests._containers import synth_container
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database, _row


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def configured(library, monkeypatch):
    """A machine set up far enough that the verb reaches its own logic."""
    resolved = config.from_dict(valid_data(library))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: ())
    return resolved


def drive(argv: list[str]) -> tuple[int, str, str]:
    """Run the real dispatcher and return (status, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


#: One second of silence, synthesized once per process: ffmpeg writes the same
#: bytes every time, and a subprocess per track was half of each test's time.
_SILENCE: list[bytes] = []


def _silence(target: Path) -> Path:
    """A real audio file at ``target``, synthesized once and copied after."""
    if _SILENCE:
        target.write_bytes(_SILENCE[0])
    else:
        synth_container(target.parent, ".flac").rename(target)
        _SILENCE.append(target.read_bytes())
    return target


def _track(folder: Path, name: str, *, title: str | None = None, key: str | None = None) -> Path:
    """A real audio file under ``folder`` with the given name and tags."""
    target = _silence(folder / name)
    fields: dict[str, object] = {}
    if title is not None:
        fields["title"] = title
    if key is not None:
        fields["initialkey"] = key
    if fields:
        tags.write_tags(target, fields)
    return target


def _folder(cfg) -> Path:
    folder = Path(cfg.library.root) / "Music" / "wave"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _answer(folder: Path, option: str = "apply") -> tuple[int, dict]:
    """Status and whole envelope from one run answered ``option``, whatever it exits with."""
    code, out, _ = drive([
        "--output", "json", "-d", f"name.apply.confirm={option}",
        "name", "apply", "--root", str(folder),
    ])
    return code, json.loads(out)


def _drive(folder: Path, option: str) -> dict:
    code, envelope = _answer(folder, option)
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]


def _plan(folder: Path) -> dict:
    """Read the plan without touching anything, through the abort option."""
    return _drive(folder, "abort")


def _apply(folder: Path) -> dict:
    return _drive(folder, "apply")


def _refused(folder: Path, *untouched: Path) -> dict:
    """The envelope of an apply refused before any rename, every file in ``untouched`` in place."""
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert all(path.is_file() for path in untouched), envelope
    return envelope


def _moves(plan: dict) -> list[tuple[str, str]]:
    return [(item["from"], item["to"]) for item in plan["items"]]


def _actions(plan: dict) -> dict[str, str]:
    return {item["from"]: item["action"] for item in plan["items"]}


@pytest.mark.parametrize(
    ("name", "title", "key"),
    [
        pytest.param("01A - 124 - Cola.flac", "01A - 124 - Cola", "01A", id="in-convention"),
        pytest.param("{marker} Cola.flac", "{marker} Cola", None, id="marked-plan-agrees-with-apply"),
        pytest.param("13A - 124 - Cola.flac", "13A - 124 - Cola", None, id="13A-is-no-head"),
        pytest.param("{marker} Cola.flac", "Cola", None, id="marker-in-filename-alone-kept"),
    ],
)
def test_a_file_the_pass_must_leave_proposes_no_rename(configured, name, title, key):
    """The pass is idempotent, leaves an unparseable head as the body, and keeps a marker."""
    marker = configured.naming.lossy_marker
    folder = _folder(configured)
    _track(folder, name.format(marker=marker), title=title.format(marker=marker), key=key)
    assert _plan(folder)["items"] == []


@pytest.mark.parametrize(
    ("name", "title", "key", "to"),
    [
        pytest.param(
            "1A - 124 - Cola.flac", "1A - 124 - Cola", "Amaj", "01A - 124 - Cola.flac",
            id="a-key-tag-not-camelot-is-ignored",
        ),
        pytest.param(
            "1A - 124 - Cola.flac", "5B - 95 - Cola", None, "01A - 124 - Cola.flac",
            id="the-filename-head-wins-over-the-title-head",
        ),
        pytest.param(
            "1A - 124 - Artist Name - Song Title.flac", "1A - 124 - Song Title", "1A",
            "01A - 124 - Artist Name - Song Title.flac", id="the-filename-body-is-carried-R-168",
        ),
        pytest.param(
            "5A - 122 - Golden Boy - Alphadog - Golden Boy.flac", "5A - 122 - Golden Boy", None,
            "05A - 122 - Golden Boy - Alphadog.flac", id="a-trailing-repeat-of-the-lead-is-deduped",
        ),
        pytest.param(
            "6A - 118 - Track - Artist - Track (Deluxe Edition).flac", "6A - 118 - Track", None,
            "06A - 118 - Track - Artist - Track (Deluxe Edition).flac",
            id="a-segment-only-starting-with-the-lead-survives",
        ),
        pytest.param(
            "Cola.flac", "{marker} Cola", None, "{marker} Cola.flac",
            id="a-marker-in-the-title-alone-is-recovered",
        ),
    ],
)
def test_one_file_is_planned_its_one_rename(configured, name, title, key, to):
    """The head is derived and padded; each surface keeps its own body (U41, R-168)."""
    marker = configured.naming.lossy_marker
    folder = _folder(configured)
    _track(folder, name, title=title.format(marker=marker), key=key)
    assert _moves(_plan(folder)) == [(name, to.format(marker=marker))]


@pytest.mark.parametrize(
    ("name", "title", "key", "to", "tag"),
    [
        pytest.param(
            "1A - 124 - Cola.flac", "1A - 124 - Cola", "1A", "01A - 124 - Cola.flac",
            "01A - 124 - Cola", id="an-unpadded-head-is-padded-with-the-tempo-intact",
        ),
        pytest.param(
            "Cola.flac", "01A - 124 - Cola", "01A", "01A - 124 - Cola.flac", "01A - 124 - Cola",
            id="the-head-is-recovered-from-the-title-tag",
        ),
        pytest.param(
            "1A - 124 - Cola.flac", "Cola", None, "01A - 124 - Cola.flac", "01A - 124 - Cola",
            id="the-filename-head-alone-is-enough",
        ),
        pytest.param(
            "01A - 124 - Cola.flac", "01A - 124 - Cola", "2A", "02A - 124 - Cola.flac",
            "02A - 124 - Cola", id="the-tag-key-wins-over-a-stale-head",
        ),
        pytest.param(
            "1A - 124 - Artist Name - Song Title.flac", "1A - 124 - Song Title", "1A",
            "01A - 124 - Artist Name - Song Title.flac", "01A - 124 - Song Title",
            id="the-title-tag-is-not-given-the-filename-body",
        ),
        pytest.param(
            "1A - 124 - Artist Name - Song Title.flac", None, "1A",
            "01A - 124 - Artist Name - Song Title.flac", "01A - 124 - Artist Name - Song Title",
            id="no-title-tag-takes-the-body-from-the-filename",
        ),
        pytest.param(
            "5A - 122 - Golden Boy - Alphadog - Golden Boy.flac", "5A - 122 - Golden Boy", None,
            "05A - 122 - Golden Boy - Alphadog.flac", "05A - 122 - Golden Boy",
            id="a-deduping-rename-converges-on-one-pass",
        ),
    ],
)
def test_an_applied_rename_lands_its_name_and_title_tag_and_converges(
    configured, name, title, key, to, tag
):
    """One apply renames the file, writes the head into the title tag, and converges."""
    folder = _folder(configured)
    path = _track(folder, name, title=title, key=key)
    assert _moves(_plan(folder)) == [(name, to)]
    _apply(folder)
    renamed = folder / to
    assert renamed.is_file() and not path.exists()
    assert tags.read_tag(renamed, "title") == tag
    assert _plan(folder)["items"] == []


def test_both_library_grammars_survive_a_rename(configured):
    """`Artist - Title` and `Title - Artist - Album` both occur, and no rule tells them apart."""
    folder = _folder(configured)
    _track(folder, "2A - 120 - Artist - Song.flac", title="2A - 120 - Song")
    _track(folder, "3A - 121 - Song Two - Artist Two - Some Album.flac", title="3A - 121 - Song Two")
    assert sorted(_moves(_plan(folder))) == sorted(
        [
            ("2A - 120 - Artist - Song.flac", "02A - 120 - Artist - Song.flac"),
            (
                "3A - 121 - Song Two - Artist Two - Some Album.flac",
                "03A - 121 - Song Two - Artist Two - Some Album.flac",
            ),
        ]
    )


def test_a_rename_never_replaces_the_body_with_the_title_tag(configured):
    """The structural form of R-168, stated as what it actually forbids."""
    folder = _folder(configured)
    names = [
        "1A - 124 - Artist Name - Song Title.flac",
        "2A - 120 - Song - Artist - Album.flac",
        "4A - 90 - Just A Body.flac",
    ]
    for name in names:
        _track(folder, name, title="Song")
    template = _template(configured)
    moves = _moves(_plan(folder))
    # All three are unpadded and must move, or the loop below passes vacuously.
    assert len(moves) == 3, f"expected three renames, got {moves!r}"
    for frm, to in moves:
        before = naming.strip_head(Path(frm).stem, template=template)
        after = naming.strip_head(Path(to).stem, template=template)
        assert after != "Song", f"{frm} was rebuilt from the title tag: {before!r} became {after!r}"
        assert after == before, f"{frm} lost body text: {before!r} became {after!r}"


def test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt(configured):
    """Truncation keeps the body's lead and marks the cut, rather than rebuilding it."""
    folder = _folder(configured)
    body = "Artist Name - " + ("Extremely Long Song Title Part " * 6).strip()
    name = f"1A - 124 - {body}.flac"
    _track(folder, name, title="1A - 124 - Short")
    moves = _moves(_plan(folder))
    assert len(moves) == 1
    template = _template(configured)
    before = naming.strip_head(Path(moves[0][0]).stem, template=template)
    after = naming.strip_head(Path(moves[0][1]).stem, template=template)
    assert after != "Short", "the body was rebuilt from the title tag"
    assert after.startswith("Artist Name - "), "the leading artist was lost"
    assert "~" in after, "an over ceiling name should carry the truncation hash"
    assert len(after) < len(before), "nothing was truncated"


@pytest.fixture
def prefix_map() -> list[dict[str, str]]:
    """No volume rewrites, unless a test parametrizes this name."""
    return []


@pytest.fixture
def collected(library, monkeypatch, prefix_map):
    """A configured machine whose collection is a real, readable database (U67)."""
    from pyrekordbox.db6 import database as binding

    data = valid_data(
        library,
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
    )
    if prefix_map:
        data["library"]["location_prefix_map"] = prefix_map
    resolved = config.from_dict(data)
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(rb_writer, "read_rekordbox_settings", lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0})
    _build_disposable_database(Path(resolved.library.db_path), with_tag_category=False)
    return resolved


def _record(cfg, recorded: str, *, identifier: str, deleted: int = 0) -> None:
    """Add one collection row recording ``recorded`` as its path."""
    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        fields = {"Title": Path(recorded).name, "rb_local_deleted": deleted, "FolderPath": recorded}
        db_session.add(_row(tables.DjmdContent, ID=identifier, **fields))
        db_session.commit()
    engine.dispose()


def _pair(folder: Path) -> tuple[Path, Path]:
    """Two unpadded files, each of which the pass would rename."""
    held = _track(folder, "1A - 124 - Held.flac", title="1A - 124 - Held", key="1A")
    free = _track(folder, "2A - 124 - Free.flac", title="2A - 124 - Free", key="2A")
    return held, free


def test_a_referenced_file_is_untouched_and_its_sibling_is_renamed(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, str(held), identifier="10")
    before = held.read_bytes()
    plan = _plan(folder)
    assert _actions(plan) == {held.name: "referenced", free.name: "rename"}
    assert plan["totals"] == {"count": 1, "referenced": 1, "collides": 0, "unnamed": 0}
    _apply(folder)
    assert held.is_file() and held.read_bytes() == before
    assert not free.exists() and (folder / "02A - 124 - Free.flac").is_file()


@pytest.mark.parametrize(
    ("spelled", "deleted"),
    [
        pytest.param(locations.location_url, 0, id="recorded-as-a-location-url"),
        pytest.param(lambda held: str(held).replace("Held", "HELD"), 0, id="a-case-variant"),
        pytest.param(str, 1, id="a-tombstoned-row"),
    ],
)
def test_a_row_naming_the_file_another_way_still_protects_it(collected, spelled, deleted):
    """A URL, a case variant and a tombstone each still hold the file they name."""
    folder = _folder(collected)
    held, _free = _pair(folder)
    _record(collected, spelled(held), identifier="10", deleted=deleted)
    _apply(folder)
    assert held.is_file()


@pytest.mark.parametrize("prefix_map", [[{"from": "/mnt/volume", "to": "{library.root}"}]])
def test_a_row_under_a_remapped_volume_still_protects_its_file(collected):
    folder = _folder(collected)
    held, _free = _pair(folder)
    relative = held.relative_to(collected.library.root)
    _record(collected, f"/mnt/volume/{relative}", identifier="10")
    assert _plan(folder)["totals"]["referenced"] == 1
    _apply(folder)
    assert held.is_file()


def test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    relative = held.relative_to(collected.library.root)
    _record(collected, f"/mnt/volume/{relative}", identifier="10")
    envelope = _refused(folder, held, free)
    cause = envelope["cause"]
    assert cause["reason"] == "collection-row-unmapped"
    assert cause["remediation"]["remedy"] == "fix-config-values"
    assert "location_prefix_map" in cause["remediation"]["steps"][0]
    assert "no rule can place it" in cause["remediation"]["steps"][1]
    assert cause["message"].startswith("1 collection row records")
    assert f"/mnt/volume/{relative}" in cause["message"]
    assert cause["detail"]["unmapped"] == 1
    assert cause["detail"]["unmapped_locations"] == [f"/mnt/volume/{relative}"]
    assert cause["detail"]["unmapped_prefixes"] == ["/mnt/volume"]


def test_an_unmapped_row_refuses_the_plan_too(collected):
    """A plan over a collection with a hole would show a rename the apply would never allow."""
    folder = _folder(collected)
    _pair(folder)
    _record(collected, "/mnt/volume/Music/1A - 124 - Held.flac", identifier="10")
    code, envelope = _answer(folder, "abort")
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "collection-row-unmapped"


def test_every_unmapped_row_is_counted_and_the_first_is_named(collected):
    """Two dark rows under candidates' names, one a tombstone (R-524), and one that resolves."""
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, "/mnt/volume/Music/2A - 124 - Free.flac", identifier="10", deleted=1)
    _record(collected, "/mnt/library/Music/1A - 124 - Held.flac", identifier="11")
    # A row under the root resolves whether or not its file is there, so it is not dark.
    _record(collected, str(folder / "03A - 124 - Other.flac"), identifier="12")
    envelope = _refused(folder, held, free)
    cause = envelope["cause"]
    assert cause["message"].startswith("2 collection rows record")
    assert "/mnt/volume/Music/2A - 124 - Free.flac" in cause["message"]
    assert "/mnt/library/Music/1A - 124 - Held.flac" not in cause["message"]
    assert cause["detail"]["unmapped"] == 2
    assert cause["detail"]["unmapped_prefixes"] == ["/mnt/library", "/mnt/volume"]
    # Each dark row with the files it could be naming, in the locations' order.
    assert cause["detail"]["could_name"] == [
        {"row": "/mnt/volume/Music/2A - 124 - Free.flac", "files": [str(free)]},
        {"row": "/mnt/library/Music/1A - 124 - Held.flac", "files": [str(held)]},
    ]


def test_two_dark_rows_under_one_candidate_name_each_name_it(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, "/mnt/volume/Music/1A - 124 - Held.flac", identifier="10")
    _record(collected, "/mnt/library/Contents/1A - 124 - Held.flac", identifier="11", deleted=1)
    _code, envelope = _answer(folder)
    assert envelope["cause"]["detail"]["unmapped"] == 2
    assert [pair["files"] for pair in envelope["cause"]["detail"]["could_name"]] == [[str(held)]] * 2
    assert held.is_file() and free.is_file()


def test_a_dark_row_is_matched_across_folders_by_leaf_alone(collected, tmp_path):
    """A renamed volume or a moved mount changes a path's prefix and never its leaf."""
    folder = _folder(collected)
    held, free = _pair(folder)
    elsewhere = tmp_path / "old-laptop" / "Downloads" / "stick" / "1A - 124 - Held.flac"
    _record(collected, str(elsewhere), identifier="10")
    envelope = _refused(folder, held, free)
    assert envelope["cause"]["detail"]["could_name"] == [{"row": str(elsewhere), "files": [str(held)]}]


def test_a_dark_row_under_a_held_candidate_name_refuses_nothing(collected):
    """A referenced candidate is never renamed (R-407), so a dark row under its name doubts nothing."""
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, str(held), identifier="10")
    _record(collected, "/mnt/volume/Music/1A - 124 - Held.flac", identifier="11", deleted=1)
    plan = _plan(folder)
    assert plan["totals"] == {"count": 1, "referenced": 1, "collides": 0, "unnamed": 0}
    _apply(folder)
    assert held.is_file()
    assert not free.exists() and (folder / "02A - 124 - Free.flac").is_file()


@pytest.mark.parametrize("prefix_map", [[{"from": "/mnt/VOLUME", "to": "{library.root}"}]])
def test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses(collected):
    """The shared resolver compares a prefix exactly; matching it here alone would be a second locate."""
    folder = _folder(collected)
    held, free = _pair(folder)
    relative = held.relative_to(collected.library.root)
    _record(collected, f"/mnt/volume/{relative}", identifier="10")
    envelope = _refused(folder, held, free)
    assert envelope["cause"]["reason"] == "collection-row-unmapped"
    assert "/mnt/volume/" in envelope["cause"]["message"]


def test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename(collected, monkeypatch):
    """The re-read before the rename, on its own."""
    folder = _folder(collected)
    held, free = _pair(folder)
    reads = iter([(), ("/mnt/volume/Music/1A - 124 - Held.flac",)])
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: next(reads))
    envelope = _refused(folder, held, free)
    assert envelope["cause"]["reason"] == "collection-row-unmapped"


def test_the_refusal_names_the_decoded_location_a_rule_is_matched_against(collected):
    """A row recorded as a location URL is quoted DECODED, as a rule is matched against it."""
    folder = _folder(collected)
    _pair(folder)
    _record(collected, "file://localhost/mnt/volume/My%20Music/1A%20-%20124%20-%20Held.flac", identifier="10")
    _code, envelope = _answer(folder)
    cause = envelope["cause"]
    assert "/mnt/volume/My Music/1A - 124 - Held.flac" in cause["message"]
    assert "%20" not in cause["message"]
    assert cause["detail"]["unmapped_locations"] == ["/mnt/volume/My Music/1A - 124 - Held.flac"]


def test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name(collected, tmp_path):
    """A gone file under a candidate's name may be naming that candidate, so it refuses."""
    folder = tmp_path / "laptop" / "Downloads"
    folder.mkdir(parents=True)
    held, free = _pair(folder)
    gone = tmp_path / "elsewhere" / "1A - 124 - Held.flac"
    _record(collected, str(gone), identifier="10")
    envelope = _refused(folder, held, free)
    assert envelope["cause"]["detail"]["unmapped_locations"] == [str(gone)]
    assert envelope["cause"]["detail"]["could_name"] == [{"row": str(gone), "files": [str(held)]}]


def test_a_gone_file_under_another_name_refuses_nothing(collected, tmp_path):
    """R-523: a dark row whose file name is no candidate's holds nothing and refuses nothing."""
    folder = tmp_path / "laptop" / "Downloads"
    folder.mkdir(parents=True)
    held, free = _pair(folder)
    _record(collected, str(folder / "moved away.flac"), identifier="10")
    _apply(folder)
    assert not held.exists() and not free.exists()
    assert (folder / "01A - 124 - Held.flac").is_file()


@pytest.mark.parametrize(
    ("recorded", "deleted"),
    [
        pytest.param(
            "/Users/somebody/Music/Original_Tracks/Adam Ten - Magic Circus.flac", 1,
            id="a-dark-tombstone-under-another-name-R-524",
        ),
        pytest.param("/v4/catalog/tracks/17477108/", 0, id="a-streamed-catalogue-path"),
        pytest.param("Contents/Artist/1A - 124 - Held.flac", 0, id="a-device-relative-row"),
        pytest.param("tidal:tracks:12345", 0, id="a-streaming-pseudo-location"),
        pytest.param("file://elsewhere.invalid{held}", 0, id="a-row-naming-another-host"),
    ],
)
def test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects(collected, recorded, deleted):
    """A row under no candidate's name, or with no local path, puts no rename in doubt."""
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, recorded.format(held=held), identifier="10", deleted=deleted)
    _apply(folder)
    assert not held.exists() and not free.exists()


def test_a_dark_tombstone_under_a_candidate_name_still_refuses(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, "/mnt/volume/Music/2A - 124 - Free.flac", identifier="10", deleted=1)
    envelope = _refused(folder, held, free)
    assert envelope["cause"]["detail"]["could_name"] == [{"row": "/mnt/volume/Music/2A - 124 - Free.flac", "files": [str(free)]}]


def test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case(collected):
    """The leaf is casefolded and composed, as the library's volume ignores case."""
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, "/mnt/volume/Music/1a - 124 - HELD.FLAC", identifier="10")
    _refused(folder, held, free)


def test_a_row_whose_file_exists_elsewhere_does_not_hold_a_namesake_in_the_library(collected, tmp_path):
    """The existence half of dark, reached alone."""
    folder = _folder(collected)
    held, free = _pair(folder)
    downloads = tmp_path / "laptop" / "Downloads"
    downloads.mkdir(parents=True)
    namesake = _track(downloads, "1A - 124 - Held.flac", key="1A")
    _record(collected, str(namesake), identifier="10")
    _apply(folder)
    assert not held.exists() and (folder / "01A - 124 - Held.flac").is_file()
    assert not free.exists()
    assert namesake.is_file()


def test_a_dark_row_is_only_asked_about_the_files_being_renamed(collected):
    """An unnamed file is not renamed, so a dark row under its name refuses nothing."""
    folder = _folder(collected)
    _track(folder, "12345.flac")
    held, _free = _pair(folder)
    _record(collected, "/mnt/volume/Music/12345.flac", identifier="10")
    plan = _plan(folder)
    assert plan["totals"]["unnamed"] == 1
    assert plan["totals"]["count"] == 2
    _code, envelope = _answer(folder)
    assert envelope["cause"]["reason"] == "rename-incomplete", envelope
    assert [item["from"] for item in envelope["cause"]["detail"]["incomplete"]] == ["12345.flac"]
    assert not held.exists()


def test_the_refusal_counts_every_row_and_lists_no_more_than_twenty(collected):
    """A fresh setup was measured at 9937 unmapped rows, too many to list in one envelope."""
    recorded = tuple(f"/absent-{index:02d}/music/track.flac" for index in range(25))
    with pytest.raises(naming_cli.CratekitError) as refused:
        naming_cli._referenced(recorded, cfg=collected, renaming=[Path("/x/track.flac")])
    detail = refused.value.cause.detail
    assert detail["unmapped"] == 25
    assert detail["unmapped_locations"] == list(recorded[:20])
    assert detail["unmapped_prefixes"] == [f"/absent-{index:02d}/music" for index in range(20)]
    assert [pair["row"] for pair in detail["could_name"]] == list(recorded[:20])
    assert refused.value.cause.message.startswith("25 collection rows record")


def test_a_row_recording_a_link_to_nothing_is_dark(collected, tmp_path):
    """The name is on this machine and the file behind it is not, so the row has not answered."""
    folder = _folder(collected)
    held, free = _pair(folder)
    dangling = tmp_path / "elsewhere" / "1A - 124 - Held.flac"
    dangling.parent.mkdir()
    dangling.symlink_to(tmp_path / "elsewhere" / "never there.flac")
    _record(collected, str(dangling), identifier="10")
    _refused(folder, held, free)


def test_an_unmapped_row_over_an_empty_folder_refuses_nothing(collected):
    """With no rename candidate the collection is not read, so the empty plan stays readable."""
    folder = _folder(collected)
    _record(collected, "/mnt/volume/Music/elsewhere.flac", identifier="10")
    assert _plan(folder)["items"] == []


@pytest.mark.parametrize("form", ["NFD", "NFC"])
def test_a_composition_variant_of_the_name_still_protects_its_file(collected, form):
    folder = _folder(collected)
    other = "NFC" if form == "NFD" else "NFD"
    name = unicodedata.normalize(form, "1A - 124 - Café.flac")
    held = _track(folder, name, key="1A")
    recorded = str(folder / unicodedata.normalize(other, "1A - 124 - Café.flac"))
    assert recorded != str(held)
    _record(collected, recorded, identifier="10")
    _apply(folder)
    assert held.is_file()


def test_a_root_outside_the_library_is_still_checked(collected, tmp_path):
    """A row under no rule whose file is on this machine has answered (R-500), and protects it."""
    folder = tmp_path / "laptop" / "Downloads"
    folder.mkdir(parents=True)
    held, free = _pair(folder)
    _record(collected, str(held), identifier="10")
    _apply(folder)
    assert held.is_file()
    assert not free.exists()


def test_a_database_with_no_matching_row_proceeds(collected):
    """Zero referencing rows from a database that OPENED is a fact, not a failure."""
    folder = _folder(collected)
    held, free = _pair(folder)
    _apply(folder)
    assert not held.exists() and not free.exists()


def test_the_digest_changes_when_a_row_starts_referencing_a_file(collected):
    folder = _folder(collected)
    held, _free = _pair(folder)
    before = _plan(folder)["digest"]
    _record(collected, str(held), identifier="10")
    assert _plan(folder)["digest"] != before


def test_a_missing_database_refuses_and_renames_nothing(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    Path(collected.library.db_path).unlink()
    code, envelope = _answer(folder)
    assert code == int(ExitCode.LIBRARY_UNREADABLE), envelope
    assert envelope["cause"]["reason"] == "collection-unreadable"
    assert envelope["cause"]["remediation"]["remedy"] != "restore-from-snapshot"
    assert held.is_file() and free.is_file()


def test_an_unopenable_database_refuses_and_renames_nothing(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    Path(collected.library.db_path).write_bytes(b"not a database at all")
    code, envelope = _answer(folder)
    assert code == int(ExitCode.LIBRARY_UNREADABLE), envelope
    assert envelope["cause"]["reason"] == "collection-unreadable"
    assert held.is_file() and free.is_file()


def test_an_empty_folder_needs_no_database(collected):
    """With nothing to rename, a machine with no database can still read an empty plan."""
    folder = _folder(collected)
    Path(collected.library.db_path).unlink()
    assert _plan(folder)["items"] == []


def test_a_row_that_appears_after_the_gate_still_protects_its_file(collected, monkeypatch):
    """The re-check before the rename, on its own."""
    folder = _folder(collected)
    held, free = _pair(folder)
    reads = iter([(), (str(held),)])
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: next(reads))
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    incomplete = envelope["cause"]["detail"]["incomplete"]
    assert [item["from"] for item in incomplete] == [held.name]
    assert "began referencing it" in incomplete[0]["why"]
    assert held.is_file()
    assert not free.exists()


def test_a_library_with_cloud_sync_on_refuses_and_names_the_real_cause(collected, monkeypatch):
    """The read open still runs the canary, which refuses a library whose cloud sync is ON."""
    folder = _folder(collected)
    held, free = _pair(folder)
    monkeypatch.setattr(rb_writer, "read_rekordbox_settings", lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 1})
    code, envelope = _answer(folder)
    assert code == int(ExitCode.LIBRARY_UNREADABLE), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "collection-unreadable"
    assert cause["remediation"]["remedy"] == "disable-cloud-sync"
    assert "Cloud Library Sync" in cause["message"]
    assert held.is_file() and free.is_file()


@pytest.mark.parametrize("through_link", [False, True], ids=["real-path-recorded", "link-recorded"])
def test_a_file_is_protected_through_a_linked_root(collected, tmp_path, through_link):
    """A root given through a link matches a row by the resolved or the absolute spelling."""
    folder = _folder(collected)
    held, free = _pair(folder)
    link = tmp_path / "linked"
    link.symlink_to(folder, target_is_directory=True)
    _record(collected, str(link / held.name if through_link else held), identifier="10")
    _apply(link)
    assert held.is_file()
    assert not free.exists()


def test_a_read_that_fails_after_the_open_refuses_and_renames_nothing(collected, monkeypatch):
    """The open succeeds and the query does not, a failure no open side check classifies."""
    folder = _folder(collected)
    held, free = _pair(folder)

    class _Broken:
        def get_content(self):
            raise RuntimeError("the query failed")

    monkeypatch.setattr(rb_writer, "open_db", lambda *args, **kwargs: _Broken())
    monkeypatch.setattr(rb_writer, "close_db", lambda handle: None)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.LIBRARY_UNREADABLE), envelope
    assert envelope["cause"]["reason"] == "collection-unreadable"
    assert envelope["cause"]["remediation"]["remedy"] == "report-defect"
    assert held.is_file() and free.is_file()


def test_a_rename_onto_a_name_another_file_holds_overwrites_nothing(configured):
    """The unpadded file would be renamed onto its padded namesake, which replaces it silently."""
    folder = _folder(configured)
    kept = _track(folder, "01A - 124 - Cola.flac", title="01A - 124 - Cola", key="01A")
    other = _track(folder, "1A - 124 - Cola.flac", title="1A - 124 - Cola", key="1A")
    tags.write_tags(kept, {"artist": "the one already in place"})
    assert _actions(_plan(folder)) == {other.name: "collides"}
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "rename-incomplete"
    assert other.name in envelope["cause"]["message"]
    assert other.is_file()
    assert tags.read_tag(kept, "artist") == "the one already in place"


def _colliding_pair(folder: Path) -> tuple[Path, Path]:
    """Two files that render to one name, each needing a rename; neither is skipped silently (R-172)."""
    first = _track(folder, "5A - 120 - Song - Artist - Song.flac", title="5A - 120 - Song", key="5A")
    second = _track(folder, "5A - 120 - Song - Artist.flac", title="5A - 120 - Song", key="5A")
    return first, second


def test_two_files_rendering_to_one_name_are_not_promised_two_renames(configured):
    """The plan pass owns the collision, which is where the ledger put it."""
    folder = _folder(configured)
    first, second = _colliding_pair(folder)
    plan = _plan(folder)
    assert _actions(plan) == {first.name: "collides", second.name: "collides"}
    assert plan["totals"] == {"count": 0, "referenced": 0, "collides": 2, "unnamed": 0}
    assert first.is_file() and second.is_file()


def test_a_collision_answers_with_the_files_that_stayed_put(configured):
    """The apply over that plan renames nothing and says so."""
    folder = _folder(configured)
    first, second = _colliding_pair(folder)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "rename-incomplete"
    assert sorted(cause["detail"]["incomplete"], key=lambda item: item["from"]) == [
        {
            "from": first.name,
            "path": str(first),
            "why": f"{second.name} renders to the same name, and neither is renamed",
        },
        {
            "from": second.name,
            "path": str(second),
            "why": f"{first.name} renders to the same name, and neither is renamed",
        },
    ]
    totals = {"count": 0, "referenced": 0, "collides": 2, "unnamed": 0, "renamed": 0, "incomplete": 2}
    assert envelope["data"]["totals"] == totals
    assert first.is_file() and second.is_file()


def test_a_target_a_collider_holds_is_held_back_too(configured):
    """The collision detection runs to a fixpoint, which the review found."""
    folder = _folder(configured)
    marker = configured.naming.lossy_marker
    first = _track(folder, "05A - 120 - Song - Artist.flac", title=f"05A - 120 - Song {marker}", key="05A")
    second = _track(folder, "5A - 120 - Song - Artist.flac", title=f"5A - 120 - Song {marker}", key="5A")
    third = _track(folder, "05A - 120 - Song - Artist - Song.flac", title="05A - 120 - Song", key="05A")
    plan = _plan(folder)
    assert _actions(plan) == {first.name: "collides", second.name: "collides", third.name: "collides"}
    assert plan["totals"] == {"count": 0, "referenced": 0, "collides": 3, "unnamed": 0}
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["data"]["totals"]["renamed"] == 0
    assert first.is_file() and second.is_file() and third.is_file()


def test_two_targets_differing_only_in_case_are_one_name(configured):
    """The collision is keyed through ``_key``, NFC and casefolded."""
    folder = _folder(configured)
    upper = _track(folder, "5A - 120 - Song - Artist - Song.flac", title="5A - 120 - Song", key="5A")
    lower = _track(folder, "5A - 120 - song - artist.flac", title="5A - 120 - song", key="5A")
    assert _actions(_plan(folder)) == {upper.name: "collides", lower.name: "collides"}
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["data"]["totals"]["renamed"] == 0
    assert upper.is_file() and lower.is_file()


def test_a_referenced_file_does_not_hold_a_name_it_will_never_take(collected):
    """A file the collection references is not a mover, so it cannot collide."""
    folder = _folder(collected)
    held = _track(folder, "5A - 120 - Song - Artist - Song.flac", title="5A - 120 - Song", key="5A")
    free = _track(folder, "5A - 120 - Song - Artist.flac", title="5A - 120 - Song", key="5A")
    _record(collected, str(held), identifier="10")
    plan = _plan(folder)
    assert _actions(plan) == {held.name: "referenced", free.name: "rename"}
    code, envelope = _answer(folder)
    assert code == int(ExitCode.OK), envelope
    assert held.is_file()
    assert (folder / "05A - 120 - Song - Artist.flac").is_file()


def test_the_remediation_only_names_a_hand_rename_over_a_real_collision(configured, monkeypatch):
    """A collision is the one reason a person has to name a file themselves."""
    folder = _folder(configured)
    _track(folder, "1A - 124 - Alpha.flac", title="1A - 124 - Alpha", key="1A")
    monkeypatch.setattr(naming_cli.tags, "write_tags", lambda path, fields: False)
    _, envelope = _answer(folder)
    steps = envelope["cause"]["remediation"]["steps"]
    assert len(steps) == 1
    assert "reason its rename did not happen" in steps[0]

    collisions = _folder(configured) / "second"
    collisions.mkdir()
    _colliding_pair(collisions)
    _, envelope = _answer(collisions)
    steps = envelope["cause"]["remediation"]["steps"]
    assert len(steps) == 2
    assert "needs a name of its own" in steps[1]


def test_a_sweep_that_carried_out_every_rename_still_answers_ok(configured):
    """The other half of the outcome, so the new answer cannot swallow the old one."""
    folder = _folder(configured)
    _track(folder, "1A - 124 - Alpha.flac", title="1A - 124 - Alpha", key="1A")
    _track(folder, "2A - 124 - Beta.flac", title="2A - 124 - Beta", key="2A")
    code, envelope = _answer(folder)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert envelope["cause"] is None
    assert envelope["data"]["totals"] == {
        "count": 2,
        "referenced": 0,
        "collides": 0,
        "unnamed": 0,
        "renamed": 2,
        "incomplete": 0,
    }
    assert (folder / "01A - 124 - Alpha.flac").is_file()
    assert (folder / "02A - 124 - Beta.flac").is_file()


def test_a_target_another_mover_still_holds_is_promised_and_then_reported(configured):
    """The collision the plan CANNOT rule out, driven with nothing faked."""
    folder = _folder(configured)
    marker = configured.naming.lossy_marker
    lead = _track(
        folder,
        "01A - 120 - Alpha - Artist - Alpha.flac",
        title="01A - 120 - Alpha",
        key="01A",
    )
    marked = _track(
        folder,
        "01A - 120 - Alpha - Artist.flac",
        title=f"01A - 120 - Alpha {marker}",
        key="01A",
    )
    assert _actions(_plan(folder)) == {lead.name: "rename", marked.name: "rename"}
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    incomplete = envelope["cause"]["detail"]["incomplete"]
    assert [item["from"] for item in incomplete] == [lead.name]
    assert "already taken" in incomplete[0]["why"]
    assert envelope["data"]["totals"]["renamed"] == 1
    assert lead.is_file()
    assert not marked.exists()


def test_a_file_gone_after_the_plan_is_named_rather_than_skipped(configured, monkeypatch):
    """A file moved or deleted while the gate waits on a person."""
    folder = _folder(configured)
    vanishing = _track(folder, "1A - 124 - Gone.flac", title="1A - 124 - Gone", key="1A")
    staying = _track(folder, "2A - 124 - Here.flac", title="2A - 124 - Here", key="2A")
    real = naming_cli._plan_for

    def _plan_then_delete(root, *, cfg):
        plan = real(root, cfg=cfg)
        vanishing.unlink()
        return plan

    monkeypatch.setattr(naming_cli, "_plan_for", _plan_then_delete)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    incomplete = envelope["cause"]["detail"]["incomplete"]
    assert [item["from"] for item in incomplete] == [vanishing.name]
    assert "no longer there" in incomplete[0]["why"]
    assert not staying.exists() and (folder / "02A - 124 - Here.flac").is_file()


def test_a_rename_the_filesystem_refuses_is_named_and_leaves_no_claim(configured, monkeypatch):
    """The ``OSError`` branch removes its claim and names the file it could not rename."""
    folder = _folder(configured)
    track = _track(folder, "1A - 124 - Alpha.flac", title="1A - 124 - Alpha", key="1A")
    original = Path.rename

    def _refuse_rename(self, target):
        if self.name == track.name:
            raise OSError(28, "no space left on device")
        return original(self, target)

    monkeypatch.setattr(Path, "rename", _refuse_rename)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    incomplete = envelope["cause"]["detail"]["incomplete"]
    assert [item["from"] for item in incomplete] == [track.name]
    assert "no space left on device" in incomplete[0]["why"]
    assert track.is_file()
    assert not (folder / "01A - 124 - Alpha.flac").exists()


def test_a_title_tag_that_could_not_be_written_is_named(configured, monkeypatch):
    """The same shape one file over, which METHOD's fifth pattern asks for."""
    folder = _folder(configured)
    _track(folder, "1A - 124 - Alpha.flac", title="1A - 124 - Alpha", key="1A")
    renamed = folder / "01A - 124 - Alpha.flac"
    monkeypatch.setattr(naming_cli.tags, "write_tags", lambda path, fields: False)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    incomplete = envelope["cause"]["detail"]["incomplete"]
    why = "it was renamed and its title tag could not be written"
    assert incomplete == [{"from": renamed.name, "path": str(renamed), "why": why}]
    assert envelope["data"]["totals"]["renamed"] == 1
    assert renamed.is_file()


def _acquired(folder: Path, name: str, **fields: str) -> Path:
    """A file as the downloader leaves it, named for its identifier and tagged (R-669)."""
    target = _silence(folder / name)
    if fields:
        assert tags.write_tags(target, dict(fields))
    return target


def _held(plan: dict) -> dict[str, str]:
    return {item["from"]: item["why"] for item in plan["items"] if item["action"] == "unnamed"}


def _renames(plan: dict) -> list[tuple[str, str]]:
    return [(item["from"], item["to"]) for item in plan["items"] if item["action"] == "rename"]


def _shown(folder: Path) -> dict:
    """What the gate shows before any answer."""
    code, out, _ = drive(["--output", "json", "name", "apply", "--root", str(folder)])
    assert code == int(ExitCode.DECISION_REQUIRED), out
    return json.loads(out)["cause"]["detail"]["shown"]


def test_an_identifier_stem_is_composed_from_the_artist_and_title_tags(configured):
    """A key the wheel does not hold and no tempo give no head, and the body is both tags."""
    folder = _folder(configured)
    _acquired(folder, "92654769.flac", artist="Tirzah", title="Affection", isrc="GBCEL1800129", initialkey="Bb")
    plan = _plan(folder)
    assert _moves(plan) == [("92654769.flac", "Tirzah - Affection.flac")]
    assert plan["totals"] == {"count": 1, "referenced": 0, "collides": 0, "unnamed": 0}


@pytest.mark.parametrize(
    ("name", "fields", "to"),
    [
        pytest.param(
            "92654769.flac", {"artist": "Tirzah", "title": "Affection", "initialkey": "7A"},
            "Tirzah - Affection.flac", id="a-camelot-key-without-a-tempo-renders-no-head",
        ),
        pytest.param(
            "12345.flac", {"artist": "Tirzah", "title": "07A - 126 - Affection"},
            "07A - 126 - Tirzah - Affection.flac", id="a-head-in-the-title-tag-stays-out-of-the-body",
        ),
        pytest.param(
            "12345.flac", {"artist": "AC/DC", "title": "Affection"},
            "AC-DC - Affection.flac", id="a-slash-takes-the-body-form-of-a-segment",
        ),
    ],
)  # fmt: skip
def test_an_identifier_stem_composes_its_one_name(configured, name, fields, to):
    """Before analysis there is no tempo; a head belongs to the head derivation, a slash to a segment."""
    folder = _folder(configured)
    _acquired(folder, name, **fields)
    assert _moves(_plan(folder)) == [(name, to)]


def test_a_stem_carrying_text_is_not_recomposed_from_its_tags(configured):
    """R-168: tags that disagree with the filename change nothing but the padded head."""
    folder = _folder(configured)
    _acquired(folder, "4A - 126 - Burning (Extended Mix).flac", artist="Someone Else", title="Burning", initialkey="4A")
    assert _moves(_plan(folder)) == [
        ("4A - 126 - Burning (Extended Mix).flac", "04A - 126 - Burning (Extended Mix).flac")
    ]


def test_a_padded_text_stem_with_tags_plans_nothing(configured):
    folder = _folder(configured)
    _acquired(folder, "04A - 126 - Burning (Extended Mix).flac", artist="Someone Else", title="Burning (Extended Mix)")
    assert _plan(folder)["items"] == []


def test_an_identifier_with_no_artist_tag_is_held_and_named_in_the_plan(configured):
    """Never renamed to its title alone nor left out: held with its reason, under the digest."""
    folder = _folder(configured)
    _acquired(folder, "12345.flac", title="Affection")
    plan = _plan(folder)
    assert _renames(plan) == []
    assert _held(plan) == {"12345.flac": (
        "its name is an identifier and it carries no artist tag, so it is not "
        "renamed to its title alone"
    )}
    assert plan["totals"] == {"count": 0, "referenced": 0, "collides": 0, "unnamed": 1}
    before = plan["digest"]
    assert tags.write_tags(folder / "12345.flac", {"artist": "Tirzah"})
    assert _plan(folder)["digest"] != before


@pytest.mark.parametrize(
    ("fields", "phrases"),
    [
        pytest.param({}, ("neither an artist tag nor a title tag",), id="no-tags-at-all"),
        pytest.param({"artist": "Tirzah", "title": "07A - 126 - "}, ("title tag is only a head",), id="title-only-a-head-R-664"),
        pytest.param({"artist": "Tirzah"}, ("no title tag", "artist alone"), id="an-artist-and-no-title"),
    ],
)
def test_an_identifier_it_cannot_name_is_held_with_its_own_reason(configured, fields, phrases):
    folder = _folder(configured)
    _acquired(folder, "12345.flac", **fields)
    why = _held(_plan(folder))["12345.flac"]
    assert all(phrase in why for phrase in phrases), why


@pytest.mark.parametrize(
    ("credits", "body"),
    [(["Tirzah", "Coby Sey"], "Tirzah, Coby Sey"), (["", "Tirzah"], "Tirzah")],
    ids=["every-credited-artist", "an-empty-value-leads-with-no-comma"],
)
def test_every_credited_artist_reaches_the_composed_body(configured, credits, body):
    """A Vorbis comment can hold the credit as several fields; the single value reader takes the first."""
    folder = _folder(configured)
    path = _acquired(folder, "12345.flac", title="Affection")
    handle = mutagen.File(path)
    handle["ARTIST"] = credits
    handle.save()
    assert _moves(_plan(folder)) == [("12345.flac", f"{body} - Affection.flac")]


def test_a_composed_body_over_the_ceiling_is_fitted_not_left_as_a_number(configured):
    folder = _folder(configured)
    title = ("Extremely Long Song Title Part " * 8).strip()
    _acquired(folder, "12345.flac", artist="Artist Name", title=title)
    moves = _moves(_plan(folder))
    assert len(moves) == 1
    after = Path(moves[0][1]).stem
    assert after.startswith("Artist Name - ")
    assert "~" in after, "an over ceiling name should carry the truncation hash"
    assert len(moves[0][1].encode()) <= configured.naming.filename_max_bytes


def test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher(configured):
    """Composed names land, text stems stay, and the title tag keeps its own body (R-168)."""
    folder = _folder(configured)
    _acquired(folder, "92654769.flac", artist="Tirzah", title="Affection", initialkey="7A")
    _acquired(folder, "4A - 126 - Burning (Extended Mix).flac", artist="Someone", title="Burning")
    _acquired(folder, "12345.flac", title="Nameless")
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    totals = {"count": 2, "referenced": 0, "collides": 0, "unnamed": 1, "renamed": 2, "incomplete": 1}
    assert envelope["data"]["totals"] == totals
    assert sorted(p.name for p in folder.glob("*.flac")) == [
        "04A - 126 - Burning (Extended Mix).flac",
        "12345.flac",
        "Tirzah - Affection.flac",
    ]
    assert tags.read_tag(folder / "Tirzah - Affection.flac", "title") == "Affection"
    assert tags.read_tag(folder / "04A - 126 - Burning (Extended Mix).flac", "title") == "04A - 126 - Burning"
    incomplete = envelope["cause"]["detail"]["incomplete"]
    assert [item["from"] for item in incomplete] == ["12345.flac"]
    assert "no artist tag" in incomplete[0]["why"]


def test_an_artist_tag_removed_while_the_gate_waits_holds_the_file(configured, monkeypatch):
    """The apply re-reads the tags after the gate, so a body from a tag that is gone is not written."""
    folder = _folder(configured)
    path = _acquired(folder, "12345.flac", artist="Tirzah", title="Affection")
    real = naming_cli._plan_for

    def plan_then_strip(root, *, cfg):
        plan = real(root, cfg=cfg)
        handle = mutagen.File(path)
        del handle["ARTIST"]
        handle.save()
        return plan

    monkeypatch.setattr(naming_cli, "_plan_for", plan_then_strip)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert path.is_file()
    assert not (folder / "Tirzah - Affection.flac").exists()
    assert "no artist tag" in envelope["cause"]["detail"]["incomplete"][0]["why"]


def test_the_gate_shows_the_totals_and_every_item(configured):
    """R-670: the screen carried the question and not one rename."""
    folder = _folder(configured)
    _acquired(folder, "92654769.flac", artist="Tirzah", title="Affection")
    _acquired(folder, "12345.flac", title="Nameless")
    shown = _shown(folder)
    assert shown["root"] == str(folder)
    assert (shown["renames"], shown["referenced"], shown["collides"], shown["unnamed"]) == (1, 0, 0, 1)
    assert shown["planned"] == [{"from": "92654769.flac", "to": "Tirzah - Affection.flac"}]
    assert shown["held"] == [
        {"from": "12345.flac", "as": "unnamed", "why": (
            "its name is an identifier and it carries no artist tag, so it is not "
            "renamed to its title alone"
        )}
    ]
    assert sorted(p.name for p in folder.glob("*.flac")) == ["12345.flac", "92654769.flac"]


def test_the_gate_names_a_referenced_file_among_the_held(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, str(held), identifier="10")
    shown = _shown(folder)
    assert shown["held"] == [
        {"from": held.name, "as": "referenced", "why": "the rekordbox collection references it"}
    ]
    assert [item["from"] for item in shown["planned"]] == [free.name]


def test_a_letterless_stem_that_is_not_a_number_is_carried_as_it_is(configured):
    """An identifier is digits only; a name of symbols a person chose stands under R-168."""
    folder = _folder(configured)
    _acquired(folder, "2 + 2 = 5.flac")
    assert _plan(folder)["items"] == []


def test_the_digest_covers_a_held_identifier_file(configured):
    """One held file and an empty folder are different plans to approve."""
    folder = _folder(configured)
    empty = _plan(folder)["digest"]
    _acquired(folder, "12345.flac", title="Nameless")
    assert _plan(folder)["digest"] != empty


def test_a_referenced_identifier_file_is_held_as_referenced_and_never_owed(collected):
    """An imported identifier file is never renamed (R-407), whatever its tags say."""
    folder = _folder(collected)
    path = _acquired(folder, "12345.flac", title="Nameless")
    _record(collected, str(path), identifier="10")
    plan = _plan(folder)
    assert _actions(plan) == {"12345.flac": "referenced"}
    assert plan["totals"] == {"count": 0, "referenced": 1, "collides": 0, "unnamed": 0}
    code, envelope = _answer(folder)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert path.is_file()


def test_a_held_identifier_file_reads_the_collection_even_with_nothing_to_rename(collected, monkeypatch):
    """The collection decides referenced from unnamed, so a held file alone still reads it."""
    folder = _folder(collected)
    _acquired(folder, "12345.flac", title="Nameless")
    reads: list[int] = []
    real = naming_cli._recorded
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: (reads.append(1), real(cfg))[1])
    _plan(folder)
    assert reads == [1]


def test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw(configured, monkeypatch):
    """The plan showed one name and the tags now render another."""
    folder = _folder(configured)
    path = _acquired(folder, "12345.flac", artist="Tirzah", title="Affection")
    real = naming_cli._plan_for

    def plan_then_edit(root, *, cfg):
        plan = real(root, cfg=cfg)
        assert tags.write_tags(path, {"artist": "Tirza"})
        return plan

    monkeypatch.setattr(naming_cli, "_plan_for", plan_then_edit)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert sorted(p.name for p in folder.glob("*.flac")) == ["12345.flac"]
    why = envelope["cause"]["detail"]["incomplete"][0]["why"]
    assert "Tirza - Affection.flac" in why and "Tirzah - Affection.flac" in why


def test_the_report_over_a_held_identifier_says_to_tag_it(configured):
    """Running it again cannot fix an unnamed file, so the cause carries the step that can."""
    folder = _folder(configured)
    _acquired(folder, "12345.flac", title="Nameless")
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    steps = envelope["cause"]["remediation"]["steps"]
    assert any("artist tag and a title tag" in step for step in steps), steps


def test_the_gate_screen_lists_no_more_than_the_bound_and_counts_the_rest():
    """A sweep of the library root is thousands of items, so the lists stop at the bound."""
    bound = naming_cli.PLAN_SHOWN
    items = [
        {"action": "rename", "from": f"{n}.flac", "to": f"A - {n}.flac", "path": f"/x/{n}.flac"}
        for n in range(bound + 3)
    ] + [
        {"action": "unnamed", "from": f"h{n}.flac", "path": f"/x/h{n}.flac", "why": "held"}
        for n in range(bound + 1)
    ]
    plan = {"items": items, "totals": {"count": bound + 3, "referenced": 0, "collides": 0, "unnamed": bound + 1}}
    shown = naming_cli._shown(plan, root=Path("/x"))
    assert len(shown["planned"]) == bound and shown["planned not listed"] == 3
    assert len(shown["held"]) == bound and shown["held not listed"] == 1
    assert shown["renames"] == bound + 3


def test_the_gate_screen_omits_the_not_listed_keys_under_the_bound(configured):
    folder = _folder(configured)
    _acquired(folder, "12345.flac", artist="Tirzah", title="Affection")
    code, out, _ = drive(["--output", "json", "name", "apply", "--root", str(folder)])
    shown = json.loads(out)["cause"]["detail"]["shown"]
    assert "planned not listed" not in shown and "held not listed" not in shown
