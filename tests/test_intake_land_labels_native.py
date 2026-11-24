"""U156: a native landing files its label tracks under the Record Labels tree, D1 applying.

A manifest's rows, or ``--label`` and each file's date tag, become ``Record Labels / <Label> /
<Label> <year>`` in the batch's own commit."""

from __future__ import annotations

import unicodedata
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.acquire import listdoc
from cratekit.core import config, rb_writer, session, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import label_filing, landing
from tests import cutover_fixtures
from tests import test_intake_land_native as land
from tests.cli_drive import drive
from tests.test_intake_land_hearts_native import cfg as cfg  # noqa: PLC0414 - the fixture
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

DECLARED = taxonomy.default_taxonomy()
TREE = DECLARED.catalog.display


@contextmanager
def _handle(cfg: config.Config):
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        yield handle
    finally:
        rb_writer.close_db(handle)


def _dated(cfg: config.Config, silence: Path, name: str, day: str | None) -> Path:
    """One staged file, its date tag set to ``day`` or left absent."""
    path = land._stage(cfg, silence, name)
    if day is not None:
        assert tags.write_tags(path, {"date": day})
    return path


def _labelled(cfg: config.Config, silence: Path, name: str, label: str | None, day: str | None) -> Path:
    """One staged file carrying ``label`` in its label tag, as a Bandcamp fetch writes it."""
    path = _dated(cfg, silence, name, day)
    if label is not None:
        assert tags.write_tags(path, {"label": label})
    return path


def _manifest(directory: Path, listed: list[tuple[str, str, str, str, int | None]]) -> Path:
    """A manifest the product's own emitter writes: ref, artist, title, label, year."""
    rows = [listdoc.Row(ref=ref, artist=artist, title=title) for ref, artist, title, _, _ in listed]
    provenance = {
        ref: listdoc.Provenance(
            source="label", label_id=f"id-{label}", label_name=label, year=year, release_id="r")
        for ref, _, _, label, year in listed
    }
    written = listdoc.write(directory, "label-approved-test", rows, provenance)
    assert written.manifest_path is not None
    return written.manifest_path


def _titles(cfg: config.Config) -> dict[str, str]:
    return {str(i): str(t) for i, t in land._query(cfg, "SELECT ID, Title FROM djmdContent")}


def _children(cfg: config.Config, parent: str) -> list[tuple[str, str, int]]:
    """(ID, Name, Attribute) of every live node under ``parent``, in rekordbox's order."""
    rows = land._query(cfg, "SELECT ID, Name, Attribute FROM djmdPlaylist WHERE ParentID = ? "
                  "AND rb_local_deleted = 0 ORDER BY Seq", parent)
    return [(str(i), str(n), int(a or 0)) for i, n, a in rows]


def _tree_folders(cfg: config.Config) -> list[str]:
    rows = land._query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name = ? AND Attribute = 1 "
                  "AND rb_local_deleted = 0", TREE)
    return [str(i) for (i,) in rows]


def _filed(cfg: config.Config) -> dict[str, dict[str, list[str]]]:
    """``label -> year playlist -> titles`` under the one Record Labels folder."""
    titles = _titles(cfg)
    (tree,) = _tree_folders(cfg)
    out: dict[str, dict[str, list[str]]] = {}
    for folder_id, label, attribute in _children(cfg, tree):
        assert attribute == 1, f"{label!r} under {TREE!r} is not a folder"
        out[label] = {
            name: [titles[m].rsplit(" - ", 1)[-1] for m in land._members(cfg, playlist_id)]
            for playlist_id, name, _ in _children(cfg, folder_id)
        }
    return out


def _shown(envelope: dict) -> dict:
    return envelope["cause"]["detail"]["shown"]


def _item_labels(envelope: dict) -> dict[str, str]:
    items = _shown(envelope)["items"]
    return {Path(item["from"]).name: item.get("label") for item in items if "from" in item}


def _playlist(cfg: config.Config, name: str, folder: str) -> str:
    with _handle(cfg) as handle:
        row = handle.create_playlist(name, parent=handle.get_playlist(ID=folder))
        handle.session.commit()
        return str(row.ID)


def _remove(cfg: config.Config, row_id: str) -> None:
    """Mark one node removed, as rekordbox does when a person deletes it."""
    land._execute(cfg, "UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", row_id)


# A manifest
def test_a_manifest_files_its_matched_rows_under_label_and_year_and_names_the_unmatched(
        cfg, silence, tmp_path):
    for name in ("One.flac", "Two.flac", "Three.flac"):
        land._stage(cfg, silence, name)
    manifest = _manifest(tmp_path, [
        ("1", "Probe", "One", "Kompakt", 2025), ("2", "Probe", "Two", "Kompakt", 2025),
        ("3", "Probe", "Three", "Kompakt", 2024), ("4", "Probe", "Absent", "Kompakt", 2024),
    ])
    acted, refused = land._lands("--manifest", str(manifest))
    shown = _shown(refused)
    assert shown["labels filed under"] == f"{TREE}, created at the playlist root"
    assert shown["label playlists"] == ["Kompakt 2025 (2 file(s), made)", "Kompakt 2024 (1 file(s), made)"]
    (unmatched,) = shown["filed under no label"]
    assert "Absent" in unmatched
    assert _item_labels(refused) == {
        "One.flac": "Kompakt 2025", "Two.flac": "Kompakt 2025", "Three.flac": "Kompakt 2024",
    }
    assert _filed(cfg) == {"Kompakt": {"Kompakt 2025": ["One", "Two"], "Kompakt 2024": ["Three"]}}
    # The batch still holds every file, filed or not.
    ((playlist_id, _parent, _attr),) = land._batch_playlist(cfg)
    assert len(land._members(cfg, str(playlist_id))) == 3
    (warned,) = [w for w in acted["warnings"] if w["code"] == landing.NO_FILE]
    assert "Absent" in warned["message"]
    totals = acted["data"]["totals"]
    assert totals["label playlists"] == 2 and totals["label memberships"] == 3
    assert totals["filed under no label"] == 1
    years = [i for i in acted["data"]["items"] if i.get("tree") == DECLARED.catalog.id]
    assert sorted((i["playlist"], i["count"], i["created"]) for i in years) == [
        ("Kompakt 2024", 1, True), ("Kompakt 2025", 2, True),
    ]
    # The record names each year filed, what a later ``label mark`` of a
    # native batch reads in place of an intake file (R-916).
    (record,) = session.records(cfg)
    assert [
        {k: filed[k] for k in ("name", "label", "year", "tracks")}
        for filed in record.detail[label_filing.RECORD_KEY]
    ] == [
        {"name": "Kompakt 2025", "label": "Kompakt", "year": 2025, "tracks": 2},
        {"name": "Kompakt 2024", "label": "Kompakt", "year": 2024, "tracks": 1},
    ]
    changes = {change.tree: change.created for change in record.change.trees}
    assert changes[DECLARED.catalog.id] == 3
    assert record.sources[DECLARED.catalog.id] == "committed"


def test_the_record_names_each_landed_rows_provider_track_for_the_account_mirror(
        cfg, silence, tmp_path):
    """U150: a label batch is in no account playlist, so the mirror reads its manifest's tracks."""
    from cratekit.organize import account_mirror
    for name in ("One.flac", "Two.flac", "Loose.flac"):
        land._stage(cfg, silence, name)
    manifest = _manifest(
        tmp_path,
        [("101", "Probe", "One", "Kompakt", 2025), ("102", "Probe", "Two", "Kompakt", 2024)])
    acted, _ = land._lands("--manifest", str(manifest))
    titles = {title.rsplit(" - ", 1)[-1]: cid for cid, title in _titles(cfg).items()}
    (record,) = session.records(cfg)
    # The file no manifest row names records nothing, and is matched as any row is.
    expected = {titles["One"]: "101", titles["Two"]: "102"}
    assert record.detail[label_filing.PROVIDER_KEY] == expected
    assert account_mirror.landed_tracks(cfg) == expected
    ((playlist_id, _parent, _attr),) = land._batch_playlist(cfg)
    assert set(expected) < set(land._members(cfg, str(playlist_id)))


def test_the_digest_moves_with_the_manifests_bytes(cfg, silence, tmp_path):
    """The same path, other bytes: an answer given for one manifest is not one for another."""
    land._stage(cfg, silence, "One.flac")
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    first = _manifest(tmp_path / "a", [("1", "Probe", "One", "Kompakt", 2025)])
    second = _manifest(tmp_path / "b", [("1", "Probe", "One", "Kompakt", 2024)])
    _code, one = drive(land._land("--manifest", str(first)))
    first.write_bytes(second.read_bytes())
    _code, other = drive(land._land("--manifest", str(first)))
    assert _shown(one)["label playlists"] == ["Kompakt 2025 (1 file(s), made)"]
    assert _shown(other)["label playlists"] == ["Kompakt 2024 (1 file(s), made)"]
    assert _shown(one)["digest"] != _shown(other)["digest"]


# --label and the date tag
def test_label_files_each_file_once_under_the_year_its_date_tag_names(cfg, silence):
    """Sixteen files over eight release years: eight playlists, each file in one."""
    years = range(2018, 2026)
    for year in years:
        for n in (1, 2):
            _dated(cfg, silence, f"T{year}{n}.flac", f"{year}-0{n}-15")
    acted, refused = land._lands("--label", "PULS")
    assert "filed under no label" not in _shown(refused)
    filed = _filed(cfg)
    assert list(filed) == ["PULS"]
    # Newest first, since a folder this write makes takes its years in that order.
    assert list(filed["PULS"]) == [f"PULS {year}" for year in sorted(years, reverse=True)]
    for year in years:
        assert filed["PULS"][f"PULS {year}"] == [f"T{year}1", f"T{year}2"]
    every = [title for playlist in filed["PULS"].values() for title in playlist]
    assert len(every) == len(set(every)) == 16


def test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere(cfg, silence):
    _dated(cfg, silence, "Dated.flac", "2021")
    _dated(cfg, silence, "Undated.flac", None)
    _dated(cfg, silence, "Worded.flac", "March of 2021")
    acted, refused = land._lands("--label", "PULS")
    named = _shown(refused)["filed under no label"]
    assert len(named) == 2
    assert any("Undated.flac" in one for one in named)
    assert any("Worded.flac" in one for one in named)
    assert _item_labels(refused) == {
        "Dated.flac": "PULS 2021", "Undated.flac": "none", "Worded.flac": "none",
    }
    assert _filed(cfg) == {"PULS": {"PULS 2021": ["Dated"]}}
    # Each lands in INBOX all the same.
    assert sorted(p.name for p in land._music(cfg).iterdir()) == [
        "Dated.flac", "Undated.flac", "Worded.flac",
    ]
    warned = [w for w in acted["warnings"] if w["code"] == landing.NO_LABEL]
    assert len(warned) == 2


def test_an_existing_year_playlist_gains_members_and_loses_none(cfg, silence):
    tree = cutover_fixtures.add_folder(cfg, TREE)
    label = cutover_fixtures.add_folder(cfg, "PULS", under=tree)
    with _handle(cfg) as handle:
        year = handle.create_playlist("PULS 2021", parent=handle.get_playlist(ID=label))
        held = handle.create_playlist("PULS 2019", parent=handle.get_playlist(ID=label))
        rb_writer.add_memberships(handle, year, ["1"])
        handle.session.commit()
        year_id, held_id = str(year.ID), str(held.ID)
    _dated(cfg, silence, "New.flac", "2021-06-01")
    _dated(cfg, silence, "Newer.flac", "2022")
    acted, refused = land._lands("--label", "PULS")
    assert _shown(refused)["labels filed under"] == f"{TREE} (row {tree})"
    assert _shown(refused)["label playlists"] == [
        "PULS 2022 (1 file(s), made)", "PULS 2021 (1 file(s), added to)",
    ]
    assert _tree_folders(cfg) == [tree], "a second Record Labels folder was made"
    assert [name for _i, name, _a in _children(cfg, tree)] == ["PULS"]
    nodes = {name: node for node, name, _a in _children(cfg, label)}
    assert nodes["PULS 2021"] == year_id and nodes["PULS 2019"] == held_id
    # A node this write makes goes last among its siblings, the residual's order.
    assert [name for _i, name, _a in _children(cfg, label)] == ["PULS 2021", "PULS 2019", "PULS 2022"]
    members = land._members(cfg, year_id)
    assert members[0] == "1", "the member the playlist held was lost or moved"
    assert len(members) == 2
    assert _titles(cfg)[members[1]].endswith("New")
    assert land._members(cfg, held_id) == []
    added = {i["playlist"]: i for i in acted["data"]["items"] if i.get("tree") == DECLARED.catalog.id}
    assert added["PULS 2021"]["created"] is False and added["PULS 2021"]["added"] == 1
    assert added["PULS 2022"]["created"] is True


def test_the_same_files_landed_again_add_no_second_membership(cfg, silence):
    """A held file is present and in its year already; ``--label`` names no provider track."""
    _dated(cfg, silence, "One.flac", "2021")
    acted, _ = land._lands("--label", "PULS")
    (record,) = session.records(cfg)
    assert label_filing.RECORD_KEY in record.detail
    assert label_filing.PROVIDER_KEY not in record.detail
    before = _filed(cfg)
    # The landed file is held, so a second landing of its copy finds it present.
    landed = land._music(cfg) / "One.flac"
    staged = Path(cfg.paths.download_staging) / "One.flac"
    staged.write_bytes(landed.read_bytes())
    landed.unlink()
    again, _ = land._lands("--label", "PULS")
    assert _filed(cfg) == before
    assert again["data"]["totals"]["label memberships"] == 0


def test_the_label_source_moves_the_digest_and_an_answer_for_one_is_stale_for_another(cfg, silence):
    _labelled(cfg, silence, "One.flac", "PULS", "2021")
    refused, run_id = land._answered(land._land("--label", "PULS"))
    other = land._asked(land._land("--label", "Kompakt"))
    own = land._asked(land._land("--label-from-tags"))
    assert _shown(refused)["label playlists"] == _shown(own)["label playlists"]
    assert len({_shown(one)["digest"] for one in (refused, other, own)}) == 3
    code, acted = drive(["--run", run_id, *land._land("--label", "Kompakt")])
    assert code == int(ExitCode.DECISION_STALE), acted
    assert land._staged_names(cfg) == ["One.flac"]
    assert _tree_folders(cfg) == []


@pytest.mark.parametrize("day", ["2021", None])
def test_a_file_left_in_staging_is_filed_nowhere_and_not_said_to_be_in_the_intake_playlist(
        cfg, silence, day):
    _dated(cfg, silence, "One.flac", "2021")
    odd = _dated(cfg, silence, "Two.flac", day)
    odd.rename(odd.with_suffix(".opus"))
    acted, refused = land._lands("--label", "PULS")
    assert _shown(refused)["label playlists"] == ["PULS 2021 (1 file(s), made)"]
    (said,) = [one for one in _shown(refused)["filed under no label"] if "Two.opus" in one]
    assert "stays in staging" in said and "intake playlist" not in said
    (warned,) = [w["message"] for w in acted["warnings"] if "Two.opus" in w["message"] and "label" in w["message"]]
    assert "stays in staging" in warned
    assert land._staged_names_all(cfg) == ["Two.opus"]
    assert _filed(cfg) == {"PULS": {"PULS 2021": ["One"]}}


# Refused before the gate
@pytest.mark.parametrize("flag", [("--label", "PULS"), ("--label-from-tags",)], ids=lambda f: f[0])
def test_a_label_flag_on_the_bridge_is_refused_before_the_gate_naming_it(
        acknowledged, silence, flag):
    cfg = acknowledged
    land._stage(cfg, silence, "One.flac")
    code, envelope = drive(land._land(*flag))
    land._assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert flag[0] in envelope["cause"]["message"]


def test_a_blank_label_or_two_label_sources_are_refused_before_the_gate(cfg, silence, tmp_path):
    land._stage(cfg, silence, "One.flac")
    manifest = str(_manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)]))
    for verb, said in (
        (("--label", "  "), ()),
        (("--label", "PULS", "--manifest", manifest), ("--label", "--manifest")),
        (("--label-from-tags", "--label", "PULS"), ("--label-from-tags", "--label")),
        (("--label-from-tags", "--manifest", manifest), ("--label-from-tags", "--manifest")),
    ):
        code, envelope = drive(land._land(*verb))
        land._assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
        assert [one for one in said if one not in envelope["cause"]["message"]] == [], verb


def test_a_tree_the_label_write_cannot_take_is_refused_before_the_gate(cfg, silence):
    """A playlist for a label folder, a smart one for a year, and two Record Labels folders."""
    tree = cutover_fixtures.add_folder(cfg, TREE)
    _playlist(cfg, "PULS", tree)
    label = cutover_fixtures.add_folder(cfg, "Kompakt", under=tree)
    land._execute(
        cfg, "UPDATE djmdPlaylist SET Attribute = 4 WHERE ID = ?", _playlist(cfg, "Kompakt 2021", label)
    )
    _dated(cfg, silence, "One.flac", "2021")
    for named, said in (
        ("PULS", "a playlist named 'PULS'"), ("Kompakt", "a smart playlist named 'Kompakt 2021'"),
    ):
        code, envelope = drive(land._land("--label", named))
        land._assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
        assert said in envelope["cause"]["message"]
    cutover_fixtures.add_folder(cfg, TREE)
    code, envelope = drive(land._land("--label", "PULS"))
    land._assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert "side by side" in envelope["cause"]["message"]


@pytest.fixture
def no_catalog(monkeypatch):
    """A taxonomy that declares no catalogue tree."""
    from cratekit.intake import ingest
    real = ingest.intake_medium

    def without_catalog(cfg_):
        medium = real(cfg_)
        return replace(medium, declared=replace(medium.declared, catalog=None))
    monkeypatch.setattr(ingest, "intake_medium", without_catalog)


def test_a_taxonomy_with_no_catalog_tree_is_refused_by_name(cfg, silence, no_catalog):
    _dated(cfg, silence, "One.flac", "2021")
    code, envelope = drive(land._land("--label", "PULS"))
    land._assert_refused_before_the_gate(cfg, code, envelope, "catalog-tree-undeclared")


def test_a_label_on_an_unreachable_library_names_the_volume_and_not_the_bridge(cfg, silence):
    """The medium was not read, so the refusal must not tell the person to drop --label."""
    _labelled(cfg, silence, "One.flac", "PULS", "2021")
    root = Path(cfg.library.root)
    root.rename(root.with_name("unmounted"))
    for flag, said in ((("--label", "PULS"), "mount the library volume"), (("--label-from-tags",), "--label-from-tags")):
        code, envelope = drive(land._land(*flag))
        assert code != int(ExitCode.OK)
        assert envelope["cause"]["reason"] == "library-root-unreachable", envelope
        message = envelope["cause"]["message"]
        assert said in message and (flag[0] != "--label" or "bridge" not in message)
    assert land._staged_names(cfg) == ["One.flac"]


# The parts, alone
@pytest.mark.parametrize(
    ("day", "year", "why"),
    [
        ("2021", 2021, None), ("2021-03-05", 2021, None), ("  2019-12", 2019, None),
        ("", None, None), ("March 2021", None, None), ("20210305", None, None), ("21", None, None),
        (None, None, "carries no date tag"), ("0000", None, "names 0, which is no release year"),
        ("1899-01-01", None, "names 1899"), ("2999", None, "names 2999"),
        ("soon", None, "names no year"),
    ])
def test_the_year_is_the_date_tags_leading_four_digits_and_no_year_is_named_with_why(
        silence, day, year, why):
    if day:
        assert tags.write_tags(silence, {"date": day})
    assert label_filing.year_of(silence) == year
    if why is not None:
        read, said = label_filing._read_year(silence)
        assert read is None and why in said


def test_next_year_is_a_release_year_and_a_failed_read_is_said_apart(silence, tmp_path):
    from datetime import date
    assert tags.write_tags(silence, {"date": str(date.today().year + 1)})
    assert label_filing.year_of(silence) == date.today().year + 1
    broken = tmp_path / "broken.flac"
    broken.write_bytes(b"not a container at all")
    year, said = label_filing._read_year(broken)
    assert year is None and "could not be read" in said


def test_a_label_tag_that_could_not_be_read_is_said_apart_from_one_that_is_absent(silence, tmp_path):
    broken = tmp_path / "Broken.flac"
    broken.write_bytes(b"not a flac stream")
    assert label_filing._read_label(broken)[0] == ""
    assert "could not be read" in label_filing._read_label(broken)[1]
    assert label_filing._read_label(silence) == ("", "it carries no label tag")
    assert tags.write_tags(silence, {"label": "  PULS  "})
    assert label_filing._read_label(silence) == ("PULS", "")


def test_the_plan_refuses_a_library_whose_intake_tree_is_on_the_bridge(acknowledged, tmp_path):
    from cratekit.intake import ingest
    cfg = acknowledged
    with _handle(cfg) as handle, pytest.raises(Exception) as caught:
        label_filing.plan_for_label(handle, ingest.intake_medium(cfg), label="PULS", files=())
    assert caught.value.cause.reason == "internal-error"
    assert "xml bridge" in caught.value.cause.message


# What the tree already holds, and what changes between the plan and the write
def test_a_label_folder_spelled_decomposed_is_the_same_folder(cfg, silence):
    """The bridge's NFC rule: one name drawn two ways is one folder, never a second."""
    tree = cutover_fixtures.add_folder(cfg, TREE)
    composed = "Café"
    folder = cutover_fixtures.add_folder(cfg, unicodedata.normalize("NFD", composed), under=tree)
    _dated(cfg, silence, "One.flac", "2021")
    acted, _ = land._lands("--label", composed)
    assert [node for node, _n, _a in _children(cfg, tree)] == [folder]
    assert [name for _i, name, _a in _children(cfg, folder)] == [f"{composed} 2021"]


def test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made(cfg, silence):
    tree = cutover_fixtures.add_folder(cfg, TREE)
    label = cutover_fixtures.add_folder(cfg, "PULS", under=tree)
    removed = _playlist(cfg, "PULS 2021", label)
    _remove(cfg, removed)
    _dated(cfg, silence, "One.flac", "2021")
    acted, _ = land._lands("--label", "PULS")
    assert land._members(cfg, removed) == []
    ((live, name, _a),) = _children(cfg, label)
    assert name == "PULS 2021" and live != removed
    assert len(land._members(cfg, live)) == 1


def test_a_year_playlist_made_after_the_answer_makes_the_answer_stale(cfg, silence):
    """The plan named a playlist to make; one there now is a different write."""
    tree = cutover_fixtures.add_folder(cfg, TREE)
    label = cutover_fixtures.add_folder(cfg, "PULS", under=tree)
    _dated(cfg, silence, "One.flac", "2021")
    run_id = land._answered(land._land("--label", "PULS"))[1]
    made = _playlist(cfg, "PULS 2021", label)
    code, acted = drive(["--run", run_id, *land._land("--label", "PULS")])
    assert code == int(ExitCode.DECISION_STALE), acted
    assert land._members(cfg, made) == []
    assert land._staged_names(cfg) == ["One.flac"]


@pytest.mark.parametrize("again", ["2021", "2020"])
def test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest(cfg, silence, again):
    """One.flac staged again onto its landed target is refused by the move, and Two.flac
    lands; a year whose every file the move refused makes no playlist."""
    _dated(cfg, silence, "One.flac", "2021")
    land._lands("--label", "PULS")
    _dated(cfg, silence, "One.flac", again)
    _dated(cfg, silence, "Two.flac", "2021")
    acted, _ = land._lands("--label", "PULS")
    assert _filed(cfg) == {"PULS": {"PULS 2021": ["One", "Two"]}}
    left = [w["message"] for w in acted["warnings"] if w["code"] == landing.NOT_WRITTEN]
    assert any("One.flac" in one and "did not land" in one for one in left), acted["warnings"]


def test_an_undated_file_the_move_refused_is_said_not_to_have_landed(cfg, silence):
    _dated(cfg, silence, "Undated.flac", None)
    _dated(cfg, silence, "One.flac", "2021")
    land._lands("--label", "PULS")
    # Undated.flac again, its target occupied, so the move refuses it.
    _dated(cfg, silence, "Undated.flac", None)
    _dated(cfg, silence, "Two.flac", "2021")
    acted, _ = land._lands("--label", "PULS")
    said = [w["message"] for w in acted["warnings"]]
    (warned,) = [one for one in said if "Undated.flac" in one and "label playlist" in one]
    assert "did not land" in warned and "intake playlist" not in warned


def test_the_write_refuses_a_planned_node_removed_since_the_plan(cfg):
    tree = cutover_fixtures.add_folder(cfg, TREE)
    label = cutover_fixtures.add_folder(cfg, "PULS", under=tree)
    year = _playlist(cfg, "PULS 2021", label)
    plan = label_filing.LabelPlan(
        tree_id=DECLARED.catalog.id, tree_display=TREE, tree_folder=tree, source=label_filing.LABEL,
        label="PULS", manifest="", manifest_digest="", folders=(("PULS", label),),
        years=(label_filing.YearPlan(label="PULS", year=2021, playlist_id=year, targets=("t",)),),
        unfiled=())
    for gone in (year, label, tree):
        _remove(cfg, gone)
        with _handle(cfg) as handle:
            try:
                with pytest.raises(CratekitError) as caught:
                    label_filing.write(handle, plan, by_target={"t": "1"})
            finally:
                handle.session.rollback()
        assert caught.value.cause.reason == "decision-stale"


def test_an_answer_the_database_does_not_hold_is_refused():
    year = label_filing.WrittenYear(
        label="PULS", year=2021, playlist_id="7", created=True, ids=("1", "2"), added=2,
        read_back=("1",))
    written = label_filing.Written(
        tree_id="record_labels", tree_folder="9", tree_created=False, folders_created=(),
        years=(year,), left=())
    with pytest.raises(CratekitError) as caught:
        label_filing.assert_read_back(written)
    assert caught.value.cause.reason == "session-committed-unverified"
    assert caught.value.cause.detail["missing"] == ["2"]
    label_filing.assert_read_back(
        replace(written, years=(replace(written.years[0], read_back=("2", "1", "3")),)))


# Names spelled two ways, and a screen with nothing to file
def test_one_label_spelled_two_ways_is_one_folder_and_a_file_two_rows_file_names_both_years(
        cfg, silence, tmp_path):
    for name in ("One.flac", "Two.flac", "Three.flac"):
        land._stage(cfg, silence, name)
    composed = "Kölsch"
    manifest = _manifest(
        tmp_path,
        [
            ("1", "Probe", "One", composed, 2025),
            ("2", "Probe", "Two", unicodedata.normalize("NFD", composed), 2025),
            ("3", "Probe", "Three", "PULS", 2020),
            ("4", "Probe", "Three", "PULS", 2023),
        ])
    acted, refused = land._lands("--manifest", str(manifest))
    assert _item_labels(refused)["Three.flac"] == "PULS 2023, PULS 2020"
    assert _filed(cfg) == {
        composed: {f"{composed} 2025": ["One", "Two"]},
        "PULS": {"PULS 2023": ["Three"], "PULS 2020": ["Three"]},
    }
def test_a_screen_with_nothing_to_file_says_so(cfg, silence):
    _dated(cfg, silence, "Undated.flac", None)
    acted, refused = land._lands("--label", "PULS")
    assert _shown(refused)["labels filed under"].startswith("nothing")
    assert _shown(refused)["label playlists"] == []
    assert _tree_folders(cfg) == []


def test_the_screen_names_each_label_folder_the_write_makes(cfg, silence):
    tree = cutover_fixtures.add_folder(cfg, TREE)
    cutover_fixtures.add_folder(cfg, "Puls", under=tree)
    _dated(cfg, silence, "One.flac", "2021")
    assert _shown(land._asked(land._land("--label", "PULS")))["label folders made"] == ["PULS"]
    code, again = drive(land._land("--label", "Puls"))
    assert "label folders made" not in _shown(again)


def test_a_manifest_with_no_label_row_asks_nothing_of_the_catalogue_tree(
        cfg, silence, tmp_path, no_catalog):
    """As the bridge's own check returns early on it: a list manifest files nothing."""
    land._stage(cfg, silence, "One.flac")
    rows = [listdoc.Row(ref="1", artist="Probe", title="One")]
    provenance = {"1": listdoc.Provenance(source="list")}
    written = listdoc.write(tmp_path, "intake-missing-test", rows, provenance)
    assert written.manifest_path is not None
    acted, refused = land._lands("--manifest", str(written.manifest_path))
    assert "labels filed under" not in _shown(refused)
    assert _tree_folders(cfg) == []


# --label-from-tags (U177): each file under the label its own tag names
def test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label(
        cfg, silence):
    for year, names in ((2019, ("A1", "A2")), (2021, ("B1",)), (2024, ("C1", "C2"))):
        for name in names:
            _labelled(cfg, silence, f"{name}.flac", "PULS", f"{year}-05-01")
    acted, refused = land._lands("--label-from-tags")
    shown = _shown(refused)
    assert shown["labels filed from"] == "each file's own label tag, its year from its date tag"
    assert "filed under no label" not in shown
    assert _filed(cfg) == {
        "PULS": {"PULS 2024": ["C1", "C2"], "PULS 2021": ["B1"], "PULS 2019": ["A1", "A2"]}
    }
    (record,) = session.records(cfg)
    assert label_filing.RECORD_KEY in record.detail
    assert label_filing.PROVIDER_KEY not in record.detail


def test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own(cfg, silence):
    """The case one ``--label`` for the batch would file under the wrong label."""
    _labelled(cfg, silence, "Puls.flac", "PULS", "2024")
    _labelled(cfg, silence, "Kompakt.flac", "Kompakt", "2023")
    _labelled(cfg, silence, "Other.flac", None, "2022")
    acted, refused = land._lands("--label-from-tags")
    assert _filed(cfg) == {"Kompakt": {"Kompakt 2023": ["Kompakt"]}, "PULS": {"PULS 2024": ["Puls"]}}
    assert _item_labels(refused) == {
        "Puls.flac": "PULS 2024", "Kompakt.flac": "Kompakt 2023", "Other.flac": "none",
    }
    (unfiled,) = _shown(refused)["filed under no label"]
    assert "Other.flac" in unfiled and "no label tag" in unfiled
    assert sorted(p.name for p in land._music(cfg).iterdir()) == ["Kompakt.flac", "Other.flac", "Puls.flac"]
    (warned,) = [w for w in acted["warnings"] if w["code"] == landing.NO_LABEL]
    assert "Other.flac" in warned["message"]


def test_a_labelled_file_with_no_year_is_named_and_a_decomposed_label_is_the_composed_folder(
        cfg, silence):
    _labelled(cfg, silence, "Dated.flac", "PULS", "2021")
    _labelled(cfg, silence, "Undated.flac", "PULS", None)
    _labelled(cfg, silence, "One.flac", unicodedata.normalize("NFD", "Sueño"), "2021")
    _labelled(cfg, silence, "Two.flac", unicodedata.normalize("NFC", "Sueño"), "2021")
    acted, refused = land._lands("--label-from-tags")
    (unfiled,) = _shown(refused)["filed under no label"]
    assert "Undated.flac" in unfiled and "PULS year playlist" in unfiled and "no date tag" in unfiled
    composed = unicodedata.normalize("NFC", "Sueño")
    assert _filed(cfg) == {
        "PULS": {"PULS 2021": ["Dated"]}, composed: {f"{composed} 2021": ["One", "Two"]}
    }
