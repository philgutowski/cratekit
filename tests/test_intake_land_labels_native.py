"""U156: a native landing files its label tracks under the Record Labels tree.

R-771 refused ``--manifest`` on a native intake tree, because label filing was
written into the intake file the native medium never makes, so a label batch
reached INBOX filed under nothing. Driven here through the real dispatcher
against the disposable database the native landing suite builds: a manifest's
rows, or one label named with ``--label`` and each file's date tag, become
``Record Labels / <Label> / <Label> <year>`` in the batch's own commit, read
back from SQL. The bridge keeps ``tests/test_landing_labels.py`` unchanged.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import sqlite3
import unicodedata
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.acquire import listdoc
from cratekit.core import config, rb_writer, session, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import label_filing, landing
from tests import cutover_fixtures
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.test_intake_land_native import (
    _assert_refused_before_the_gate,
    _batch_playlist,
    _land,
    _members,
    _music,
    _query,
    _stage,
    _staged_names,
    _staged_names_all,
    _two_acts,
)
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _dated(cfg: config.Config, silence: Path, name: str, day: str | None) -> Path:
    """One staged file, its date tag set to ``day`` or left absent."""
    path = _stage(cfg, silence, name)
    if day is not None:
        assert tags.write_tags(path, {"date": day})
    return path


def _manifest(directory: Path, listed: list[tuple[str, str, str, str, int | None]]) -> Path:
    """A manifest the product's own emitter writes: ref, artist, title, label, year."""
    rows = [listdoc.Row(ref=ref, artist=artist, title=title) for ref, artist, title, _, _ in listed]
    provenance = {
        ref: listdoc.Provenance(
            source="label", label_id=f"id-{label}", label_name=label, year=year, release_id="r"
        )
        for ref, _, _, label, year in listed
    }
    written = listdoc.write(directory, "label-approved-test", rows, provenance)
    assert written.manifest_path is not None
    return written.manifest_path


def _titles(cfg: config.Config) -> dict[str, str]:
    return {str(i): str(t) for i, t in _query(cfg, "SELECT ID, Title FROM djmdContent")}


def _children(cfg: config.Config, parent: str) -> list[tuple[str, str, int]]:
    """(ID, Name, Attribute) of every live node under ``parent``, in rekordbox's order."""
    return [
        (str(i), str(n), int(a or 0))
        for i, n, a in _query(
            cfg,
            "SELECT ID, Name, Attribute FROM djmdPlaylist WHERE ParentID = ? "
            "AND rb_local_deleted = 0 ORDER BY Seq",
            parent,
        )
    ]


def _tree_folders(cfg: config.Config) -> list[str]:
    return [
        str(i)
        for (i,) in _query(
            cfg,
            "SELECT ID FROM djmdPlaylist WHERE Name = ? AND Attribute = 1 "
            "AND rb_local_deleted = 0",
            TREE,
        )
    ]


def _filed(cfg: config.Config) -> dict[str, dict[str, list[str]]]:
    """``label -> year playlist -> titles`` under the one Record Labels folder."""
    titles = _titles(cfg)
    (tree,) = _tree_folders(cfg)
    out: dict[str, dict[str, list[str]]] = {}
    for folder_id, label, attribute in _children(cfg, tree):
        assert attribute == 1, f"{label!r} under {TREE!r} is not a folder"
        out[label] = {
            name: [titles[m].rsplit(" - ", 1)[-1] for m in _members(cfg, playlist_id)]
            for playlist_id, name, _ in _children(cfg, folder_id)
        }
    return out


def _shown(envelope: dict) -> dict:
    return envelope["cause"]["detail"]["shown"]


def _item_labels(envelope: dict) -> dict[str, str]:
    return {
        Path(item["from"]).name: item.get("label")
        for item in _shown(envelope)["items"]
        if "from" in item
    }


# ---------------------------------------------------------------------------
# A manifest
# ---------------------------------------------------------------------------


def test_a_manifest_files_its_matched_rows_under_label_and_year_and_names_the_unmatched(
    native_library, silence, tmp_path
):
    cfg, _root = native_library
    for name in ("One.flac", "Two.flac", "Three.flac"):
        _stage(cfg, silence, name)
    manifest = _manifest(
        tmp_path,
        [
            ("1", "Probe", "One", "Kompakt", 2025),
            ("2", "Probe", "Two", "Kompakt", 2025),
            ("3", "Probe", "Three", "Kompakt", 2024),
            ("4", "Probe", "Absent", "Kompakt", 2024),
        ],
    )

    code, acted, refused = _two_acts(_land("--manifest", str(manifest)))

    assert code == int(ExitCode.OK), acted
    shown = _shown(refused)
    assert shown["labels filed under"] == f"{TREE}, created at the playlist root"
    assert shown["label playlists"] == ["Kompakt 2025 (2 file(s), made)", "Kompakt 2024 (1 file(s), made)"]
    (unmatched,) = shown["filed under no label"]
    assert "Absent" in unmatched
    assert _item_labels(refused) == {
        "One.flac": "Kompakt 2025",
        "Two.flac": "Kompakt 2025",
        "Three.flac": "Kompakt 2024",
    }
    assert _filed(cfg) == {"Kompakt": {"Kompakt 2025": ["One", "Two"], "Kompakt 2024": ["Three"]}}
    # The batch still holds every file, filed or not.
    ((playlist_id, _parent, _attr),) = _batch_playlist(cfg)
    assert len(_members(cfg, str(playlist_id))) == 3
    (warned,) = [w for w in acted["warnings"] if w["code"] == landing.NO_FILE]
    assert "Absent" in warned["message"]
    totals = acted["data"]["totals"]
    assert totals["label playlists"] == 2 and totals["label memberships"] == 3
    assert totals["filed under no label"] == 1
    years = [i for i in acted["data"]["items"] if i.get("tree") == DECLARED.catalog.id]
    assert sorted((i["playlist"], i["count"], i["created"]) for i in years) == [
        ("Kompakt 2024", 1, True),
        ("Kompakt 2025", 2, True),
    ]


def test_the_record_names_each_year_filed_and_counts_it_under_the_catalogue_tree(
    native_library, silence, tmp_path
):
    """What a later ``label mark`` of a native batch reads in place of an intake file (R-916)."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])

    code, acted, _ = _two_acts(_land("--manifest", str(manifest)))

    assert code == int(ExitCode.OK), acted
    (record,) = session.records(cfg)
    ((filed,),) = [record.detail[label_filing.RECORD_KEY]]
    assert {k: filed[k] for k in ("name", "label", "year", "tracks")} == {
        "name": "Kompakt 2025",
        "label": "Kompakt",
        "year": 2025,
        "tracks": 1,
    }
    changes = {change.tree: change.created for change in record.change.trees}
    assert changes[DECLARED.catalog.id] == 1
    assert record.sources[DECLARED.catalog.id] == "committed"


def test_the_record_names_each_landed_rows_provider_track_for_the_account_mirror(
    native_library, silence, tmp_path
):
    """U150. A label batch is in no account playlist, so the mirror fills its INBOX
    playlist from the provider track each file's manifest row names."""
    from cratekit.organize import account_mirror

    cfg, _root = native_library
    for name in ("One.flac", "Two.flac", "Loose.flac"):
        _stage(cfg, silence, name)
    manifest = _manifest(
        tmp_path,
        [("101", "Probe", "One", "Kompakt", 2025), ("102", "Probe", "Two", "Kompakt", 2024)],
    )

    code, acted, _ = _two_acts(_land("--manifest", str(manifest)))

    assert code == int(ExitCode.OK), acted
    titles = {title.rsplit(" - ", 1)[-1]: cid for cid, title in _titles(cfg).items()}
    (record,) = session.records(cfg)
    # The file no manifest row names records nothing, and is matched as any row is.
    expected = {titles["One"]: "101", titles["Two"]: "102"}
    assert record.detail[label_filing.PROVIDER_KEY] == expected
    assert account_mirror.landed_tracks(cfg) == expected
    ((playlist_id, _parent, _attr),) = _batch_playlist(cfg)
    assert set(expected) < set(_members(cfg, str(playlist_id)))


def test_a_landing_with_label_records_no_provider_track(native_library, silence):
    """``--label`` names no track, so there is nothing to record."""
    cfg, _root = native_library
    _dated(cfg, silence, "One.flac", "2025-03-01")

    code, acted, _ = _two_acts(_land("--label", "Kompakt"))

    assert code == int(ExitCode.OK), acted
    (record,) = session.records(cfg)
    assert label_filing.RECORD_KEY in record.detail
    assert label_filing.PROVIDER_KEY not in record.detail


def test_the_digest_moves_with_the_manifests_bytes(native_library, silence, tmp_path):
    """The same path, other bytes: an answer given for one manifest is not one for another."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    first = _manifest(tmp_path / "a", [("1", "Probe", "One", "Kompakt", 2025)])
    second = _manifest(tmp_path / "b", [("1", "Probe", "One", "Kompakt", 2024)])

    _code, one = drive(_land("--manifest", str(first)))
    first.write_bytes(second.read_bytes())
    _code, other = drive(_land("--manifest", str(first)))

    assert _shown(one)["label playlists"] == ["Kompakt 2025 (1 file(s), made)"]
    assert _shown(other)["label playlists"] == ["Kompakt 2024 (1 file(s), made)"]
    assert _shown(one)["digest"] != _shown(other)["digest"]


# ---------------------------------------------------------------------------
# --label and the date tag
# ---------------------------------------------------------------------------


def test_label_files_each_file_once_under_the_year_its_date_tag_names(native_library, silence):
    """Sixteen files over eight release years: eight playlists, each file in one."""
    cfg, _root = native_library
    years = range(2018, 2026)
    for year in years:
        for n in (1, 2):
            _dated(cfg, silence, f"T{year}{n}.flac", f"{year}-0{n}-15")

    code, acted, refused = _two_acts(_land("--label", "PULS"))

    assert code == int(ExitCode.OK), acted
    assert "filed under no label" not in _shown(refused)
    filed = _filed(cfg)
    assert list(filed) == ["PULS"]
    # Newest first, since a folder this write makes takes its years in that order.
    assert list(filed["PULS"]) == [f"PULS {year}" for year in sorted(years, reverse=True)]
    for year in years:
        assert filed["PULS"][f"PULS {year}"] == [f"T{year}1", f"T{year}2"]
    every = [title for playlist in filed["PULS"].values() for title in playlist]
    assert len(every) == len(set(every)) == 16


def test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere(native_library, silence):
    cfg, _root = native_library
    _dated(cfg, silence, "Dated.flac", "2021")
    _dated(cfg, silence, "Undated.flac", None)
    _dated(cfg, silence, "Worded.flac", "March of 2021")

    code, acted, refused = _two_acts(_land("--label", "PULS"))

    assert code == int(ExitCode.OK), acted
    named = _shown(refused)["filed under no label"]
    assert len(named) == 2
    assert any("Undated.flac" in one for one in named)
    assert any("Worded.flac" in one for one in named)
    assert _item_labels(refused) == {
        "Dated.flac": "PULS 2021",
        "Undated.flac": "none",
        "Worded.flac": "none",
    }
    assert _filed(cfg) == {"PULS": {"PULS 2021": ["Dated"]}}
    # Each lands in INBOX all the same.
    assert sorted(p.name for p in _music(cfg).iterdir()) == [
        "Dated.flac",
        "Undated.flac",
        "Worded.flac",
    ]
    warned = [w for w in acted["warnings"] if w["code"] == landing.NO_LABEL]
    assert len(warned) == 2


def test_an_existing_year_playlist_gains_members_and_loses_none(native_library, silence):
    cfg, _root = native_library
    tree = cutover_fixtures.add_folder(cfg, TREE)
    label = cutover_fixtures.add_folder(cfg, "PULS", under=tree)
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        year = handle.create_playlist("PULS 2021", parent=handle.get_playlist(ID=label))
        held = handle.create_playlist("PULS 2019", parent=handle.get_playlist(ID=label))
        rb_writer.add_memberships(handle, year, ["1"])
        handle.session.commit()
        year_id, held_id = str(year.ID), str(held.ID)
    finally:
        rb_writer.close_db(handle)
    _dated(cfg, silence, "New.flac", "2021-06-01")
    _dated(cfg, silence, "Newer.flac", "2022")

    code, acted, refused = _two_acts(_land("--label", "PULS"))

    assert code == int(ExitCode.OK), acted
    assert _shown(refused)["labels filed under"] == f"{TREE} (row {tree})"
    assert _shown(refused)["label playlists"] == [
        "PULS 2022 (1 file(s), made)",
        "PULS 2021 (1 file(s), added to)",
    ]
    assert _tree_folders(cfg) == [tree], "a second Record Labels folder was made"
    assert [name for _i, name, _a in _children(cfg, tree)] == ["PULS"]
    nodes = {name: node for node, name, _a in _children(cfg, label)}
    assert nodes["PULS 2021"] == year_id and nodes["PULS 2019"] == held_id
    # A node this write makes goes last among its siblings, the residual's order.
    assert [name for _i, name, _a in _children(cfg, label)] == ["PULS 2021", "PULS 2019", "PULS 2022"]
    members = _members(cfg, year_id)
    assert members[0] == "1", "the member the playlist held was lost or moved"
    assert len(members) == 2
    assert _titles(cfg)[members[1]].endswith("New")
    assert _members(cfg, held_id) == []
    added = {i["playlist"]: i for i in acted["data"]["items"] if i.get("tree") == DECLARED.catalog.id}
    assert added["PULS 2021"]["created"] is False and added["PULS 2021"]["added"] == 1
    assert added["PULS 2022"]["created"] is True


def test_the_same_files_landed_again_add_no_second_membership(native_library, silence):
    """A file the collection already holds is present, and its year playlist already holds it."""
    cfg, _root = native_library
    _dated(cfg, silence, "One.flac", "2021")
    code, acted, _ = _two_acts(_land("--label", "PULS"))
    assert code == int(ExitCode.OK), acted
    before = _filed(cfg)

    # The landed file is held, so a second landing of its copy finds it present.
    landed = _music(cfg) / "One.flac"
    staged = Path(cfg.paths.download_staging) / "One.flac"
    staged.write_bytes(landed.read_bytes())
    landed.unlink()

    code, again, _ = _two_acts(_land("--label", "PULS"))
    assert code == int(ExitCode.OK), again
    assert _filed(cfg) == before
    assert again["data"]["totals"]["label memberships"] == 0


def test_the_digest_moves_with_the_label(native_library, silence):
    cfg, _root = native_library
    _dated(cfg, silence, "One.flac", "2021")

    _code, puls = drive(_land("--label", "PULS"))
    _code, other = drive(_land("--label", "Kompakt"))

    assert _shown(puls)["digest"] != _shown(other)["digest"]


def test_an_answer_given_for_one_label_is_stale_for_another(native_library, silence):
    cfg, _root = native_library
    _dated(cfg, silence, "One.flac", "2021")
    code, refused = drive(_land("--label", "PULS"))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, land_gate(), "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)

    code, acted = drive(["--run", run_id, *_land("--label", "Kompakt")])

    assert code == int(ExitCode.DECISION_STALE), acted
    assert _staged_names(cfg) == ["One.flac"]
    assert _tree_folders(cfg) == []


def land_gate() -> str:
    from cratekit.intake import land_cli

    return land_cli.NATIVE_GATE


def test_a_file_left_in_staging_is_filed_nowhere(native_library, silence):
    cfg, _root = native_library
    _dated(cfg, silence, "One.flac", "2021")
    odd = _dated(cfg, silence, "Two.flac", "2021")
    odd.rename(odd.with_suffix(".opus"))

    code, acted, refused = _two_acts(_land("--label", "PULS"))

    assert code == int(ExitCode.OK), acted
    assert _shown(refused)["label playlists"] == ["PULS 2021 (1 file(s), made)"]
    assert any("Two.opus" in one for one in _shown(refused)["filed under no label"])
    assert _staged_names_all(cfg) == ["Two.opus"]
    assert _filed(cfg) == {"PULS": {"PULS 2021": ["One"]}}


# ---------------------------------------------------------------------------
# Refused before the gate
# ---------------------------------------------------------------------------


def test_label_on_the_bridge_is_refused_before_the_gate_naming_the_flag(acknowledged, silence):
    cfg = acknowledged
    _stage(cfg, silence, "One.flac")
    code, envelope = drive(_land("--label", "PULS"))
    _assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert "--label" in envelope["cause"]["message"]


def test_label_beside_a_manifest_is_refused_before_the_gate(native_library, silence, tmp_path):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])
    code, envelope = drive(_land("--label", "PULS", "--manifest", str(manifest)))
    _assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert "--label" in envelope["cause"]["message"] and "--manifest" in envelope["cause"]["message"]


def test_a_blank_label_is_refused_before_the_gate(native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, envelope = drive(_land("--label", "  "))
    _assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")


def test_two_record_labels_folders_are_refused_before_the_gate(native_library, silence):
    cfg, _root = native_library
    cutover_fixtures.add_folder(cfg, TREE)
    cutover_fixtures.add_folder(cfg, TREE)
    _dated(cfg, silence, "One.flac", "2021")
    code, envelope = drive(_land("--label", "PULS"))
    _assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert "side by side" in envelope["cause"]["message"]


def test_a_playlist_where_the_label_folder_belongs_is_refused_before_the_gate(
    native_library, silence
):
    cfg, _root = native_library
    tree = cutover_fixtures.add_folder(cfg, TREE)
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.create_playlist("PULS", parent=handle.get_playlist(ID=tree))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    _dated(cfg, silence, "One.flac", "2021")
    code, envelope = drive(_land("--label", "PULS"))
    _assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert "a playlist named 'PULS'" in envelope["cause"]["message"]


def test_a_taxonomy_with_no_catalog_tree_is_refused_by_name(native_library, silence, monkeypatch):
    cfg, _root = native_library
    _dated(cfg, silence, "One.flac", "2021")
    from cratekit.intake import ingest

    real = ingest.intake_medium

    def without_catalog(cfg_):
        medium = real(cfg_)
        return replace(medium, declared=replace(medium.declared, catalog=None))

    monkeypatch.setattr(ingest, "intake_medium", without_catalog)
    code, envelope = drive(_land("--label", "PULS"))
    _assert_refused_before_the_gate(cfg, code, envelope, "catalog-tree-undeclared")


# ---------------------------------------------------------------------------
# The parts, alone
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("day", "year"),
    [
        ("2021", 2021),
        ("2021-03-05", 2021),
        ("  2019-12", 2019),
        ("", None),
        ("March 2021", None),
        ("20210305", None),
        ("21", None),
    ],
)
def test_the_year_is_the_date_tags_leading_four_digits(tmp_path, day, year):
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    path = synth_container(scratch, ".flac")
    if day:
        assert tags.write_tags(path, {"date": day})
    assert label_filing.year_of(path) == year


def test_the_plan_refuses_a_library_whose_intake_tree_is_on_the_bridge(acknowledged, tmp_path):
    from cratekit.intake import ingest

    cfg = acknowledged
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        with pytest.raises(Exception) as caught:
            label_filing.plan_for_label(handle, ingest.intake_medium(cfg), label="PULS", files=())
    finally:
        rb_writer.close_db(handle)
    assert caught.value.cause.reason == "internal-error"
    assert "xml bridge" in caught.value.cause.message


# ---------------------------------------------------------------------------
# What the tree already holds, and what changes between the plan and the write
# ---------------------------------------------------------------------------


def _playlist(cfg: config.Config, name: str, folder: str) -> str:
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        row = handle.create_playlist(name, parent=handle.get_playlist(ID=folder))
        handle.session.commit()
        return str(row.ID)
    finally:
        rb_writer.close_db(handle)


def _remove(cfg: config.Config, row_id: str) -> None:
    """Mark one node removed, as rekordbox does when a person deletes it."""
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        conn.execute("UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", (row_id,))
        conn.commit()
    finally:
        conn.close()


def test_a_label_folder_spelled_decomposed_is_the_same_folder(native_library, silence):
    """The bridge's NFC rule: one name drawn two ways is one folder, never a second."""
    cfg, _root = native_library
    tree = cutover_fixtures.add_folder(cfg, TREE)
    composed = "Café"
    folder = cutover_fixtures.add_folder(cfg, unicodedata.normalize("NFD", composed), under=tree)
    _dated(cfg, silence, "One.flac", "2021")

    code, acted, _ = _two_acts(_land("--label", composed))

    assert code == int(ExitCode.OK), acted
    assert [node for node, _n, _a in _children(cfg, tree)] == [folder]
    assert [name for _i, name, _a in _children(cfg, folder)] == [f"{composed} 2021"]


def test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made(native_library, silence):
    cfg, _root = native_library
    tree = cutover_fixtures.add_folder(cfg, TREE)
    label = cutover_fixtures.add_folder(cfg, "PULS", under=tree)
    removed = _playlist(cfg, "PULS 2021", label)
    _remove(cfg, removed)
    _dated(cfg, silence, "One.flac", "2021")

    code, acted, _ = _two_acts(_land("--label", "PULS"))

    assert code == int(ExitCode.OK), acted
    assert _members(cfg, removed) == []
    ((live, name, _a),) = _children(cfg, label)
    assert name == "PULS 2021" and live != removed
    assert len(_members(cfg, live)) == 1


def test_a_year_playlist_made_after_the_answer_makes_the_answer_stale(native_library, silence):
    """The plan named a playlist to make; one there now is a different write."""
    cfg, _root = native_library
    tree = cutover_fixtures.add_folder(cfg, TREE)
    label = cutover_fixtures.add_folder(cfg, "PULS", under=tree)
    _dated(cfg, silence, "One.flac", "2021")
    code, refused = drive(_land("--label", "PULS"))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, land_gate(), "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    made = _playlist(cfg, "PULS 2021", label)

    code, acted = drive(["--run", run_id, *_land("--label", "PULS")])

    assert code == int(ExitCode.DECISION_STALE), acted
    assert _members(cfg, made) == []
    assert _staged_names(cfg) == ["One.flac"]


def test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest(native_library, silence):
    cfg, _root = native_library
    _dated(cfg, silence, "One.flac", "2021")
    code, acted, _ = _two_acts(_land("--label", "PULS"))
    assert code == int(ExitCode.OK), acted
    # One.flac again, its target occupied, so the move refuses it; Two.flac lands.
    _dated(cfg, silence, "One.flac", "2021")
    _dated(cfg, silence, "Two.flac", "2021")

    code, acted, _ = _two_acts(_land("--label", "PULS"))

    assert code == int(ExitCode.OK), acted
    assert _filed(cfg) == {"PULS": {"PULS 2021": ["One", "Two"]}}
    left = [w["message"] for w in acted["warnings"] if w["code"] == landing.NOT_WRITTEN]
    assert any("One.flac" in one and "did not land" in one for one in left), acted["warnings"]


def test_a_year_whose_every_file_the_move_refused_makes_no_playlist(native_library, silence):
    cfg, _root = native_library
    _dated(cfg, silence, "One.flac", "2021")
    code, acted, _ = _two_acts(_land("--label", "PULS"))
    assert code == int(ExitCode.OK), acted
    _dated(cfg, silence, "One.flac", "2020")
    _dated(cfg, silence, "Two.flac", "2021")

    code, acted, _ = _two_acts(_land("--label", "PULS"))

    assert code == int(ExitCode.OK), acted
    assert _filed(cfg) == {"PULS": {"PULS 2021": ["One", "Two"]}}


def test_the_write_refuses_a_planned_node_removed_since_the_plan(native_library):
    cfg, _root = native_library
    tree = cutover_fixtures.add_folder(cfg, TREE)
    label = cutover_fixtures.add_folder(cfg, "PULS", under=tree)
    year = _playlist(cfg, "PULS 2021", label)
    plan = label_filing.LabelPlan(
        tree_id=DECLARED.catalog.id,
        tree_display=TREE,
        tree_folder=tree,
        source=label_filing.LABEL,
        label="PULS",
        manifest="",
        manifest_digest="",
        folders=(("PULS", label),),
        years=(label_filing.YearPlan(label="PULS", year=2021, playlist_id=year, targets=("t",)),),
        unfiled=(),
    )
    for gone in (year, label, tree):
        _remove(cfg, gone)
        handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
        try:
            with pytest.raises(CratekitError) as caught:
                label_filing.write(handle, plan, by_target={"t": "1"})
        finally:
            handle.session.rollback()
            rb_writer.close_db(handle)
        assert caught.value.cause.reason == "decision-stale"


def test_an_answer_the_database_does_not_hold_is_refused():
    written = label_filing.Written(
        tree_id="record_labels",
        tree_folder="9",
        tree_created=False,
        folders_created=(),
        years=(
            label_filing.WrittenYear(
                label="PULS", year=2021, playlist_id="7", created=True, ids=("1", "2"),
                added=2, read_back=("1",),
            ),
        ),
        left=(),
    )
    with pytest.raises(CratekitError) as caught:
        label_filing.assert_read_back(written)
    assert caught.value.cause.reason == "session-committed-unverified"
    assert caught.value.cause.detail["missing"] == ["2"]
    label_filing.assert_read_back(
        label_filing.Written(
            tree_id="record_labels", tree_folder="9", tree_created=False, folders_created=(),
            years=(replace(written.years[0], read_back=("2", "1", "3")),), left=(),
        )
    )


# ---------------------------------------------------------------------------
# The first review round
# ---------------------------------------------------------------------------


def test_label_on_an_unreachable_library_names_the_volume_and_not_the_bridge(
    native_library, silence
):
    """The medium was not read, so the refusal must not say the tree is on the
    bridge or tell the person to drop --label, which would land the batch
    filed under nothing once the volume is back."""
    cfg, _root = native_library
    _dated(cfg, silence, "One.flac", "2021")
    root = Path(cfg.library.root)
    root.rename(root.with_name("unmounted"))

    code, envelope = drive(_land("--label", "PULS"))

    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "library-root-unreachable", envelope
    message = envelope["cause"]["message"]
    assert "mount the library volume" in message and "bridge" not in message
    assert _staged_names(cfg) == ["One.flac"]


def test_a_smart_playlist_where_a_year_playlist_belongs_is_refused_before_the_gate(
    native_library, silence
):
    """The binding refuses a membership in one at the write, after the moves."""
    cfg, _root = native_library
    tree = cutover_fixtures.add_folder(cfg, TREE)
    label = cutover_fixtures.add_folder(cfg, "PULS", under=tree)
    smart = _playlist(cfg, "PULS 2021", label)
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        conn.execute("UPDATE djmdPlaylist SET Attribute = 4 WHERE ID = ?", (smart,))
        conn.commit()
    finally:
        conn.close()
    _dated(cfg, silence, "One.flac", "2021")

    code, envelope = drive(_land("--label", "PULS"))

    _assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert "a smart playlist named 'PULS 2021'" in envelope["cause"]["message"]


def test_one_label_spelled_two_ways_in_a_manifest_is_one_folder(native_library, silence, tmp_path):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")
    composed = "Kölsch"
    manifest = _manifest(
        tmp_path,
        [
            ("1", "Probe", "One", composed, 2025),
            ("2", "Probe", "Two", unicodedata.normalize("NFD", composed), 2025),
        ],
    )

    code, acted, _ = _two_acts(_land("--manifest", str(manifest)))

    assert code == int(ExitCode.OK), acted
    assert _filed(cfg) == {composed: {f"{composed} 2025": ["One", "Two"]}}


def test_a_file_two_rows_file_in_two_years_names_both_on_its_item(
    native_library, silence, tmp_path
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(
        tmp_path,
        [("1", "Probe", "One", "PULS", 2020), ("2", "Probe", "One", "PULS", 2023)],
    )

    code, acted, refused = _two_acts(_land("--manifest", str(manifest)))

    assert code == int(ExitCode.OK), acted
    assert _item_labels(refused) == {"One.flac": "PULS 2023, PULS 2020"}
    assert _filed(cfg) == {"PULS": {"PULS 2023": ["One"], "PULS 2020": ["One"]}}


def test_a_screen_with_nothing_to_file_says_so(native_library, silence):
    cfg, _root = native_library
    _dated(cfg, silence, "Undated.flac", None)

    code, acted, refused = _two_acts(_land("--label", "PULS"))

    assert code == int(ExitCode.OK), acted
    assert _shown(refused)["labels filed under"].startswith("nothing")
    assert _shown(refused)["label playlists"] == []
    assert _tree_folders(cfg) == []


@pytest.mark.parametrize(
    ("day", "why"),
    [
        (None, "carries no date tag"),
        ("0000", "names 0, which is no release year"),
        ("1899-01-01", "names 1899"),
        ("2999", "names 2999"),
        ("soon", "names no year"),
    ],
)
def test_a_year_with_no_reason_behind_it_is_named_with_why(tmp_path, day, why):
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    path = synth_container(scratch, ".flac")
    if day is not None:
        assert tags.write_tags(path, {"date": day})
    year, said = label_filing._read_year(path)
    assert year is None and why in said


def test_next_year_is_a_release_year_and_a_failed_read_is_said_apart(tmp_path):
    from datetime import date

    scratch = tmp_path / "scratch"
    scratch.mkdir()
    path = synth_container(scratch, ".flac")
    assert tags.write_tags(path, {"date": str(date.today().year + 1)})
    assert label_filing.year_of(path) == date.today().year + 1
    broken = tmp_path / "broken.flac"
    broken.write_bytes(b"not a container at all")
    year, said = label_filing._read_year(broken)
    assert year is None and "could not be read" in said


# ---------------------------------------------------------------------------
# The second review round
# ---------------------------------------------------------------------------


def test_an_undated_file_left_in_staging_is_not_said_to_be_in_the_intake_playlist(
    native_library, silence
):
    cfg, _root = native_library
    _dated(cfg, silence, "One.flac", "2021")
    odd = _dated(cfg, silence, "Two.flac", None)
    odd.rename(odd.with_suffix(".opus"))

    code, acted, refused = _two_acts(_land("--label", "PULS"))

    assert code == int(ExitCode.OK), acted
    (said,) = [one for one in _shown(refused)["filed under no label"] if "Two.opus" in one]
    assert "stays in staging" in said and "intake playlist" not in said
    (warned,) = [w["message"] for w in acted["warnings"] if "Two.opus" in w["message"] and "label" in w["message"]]
    assert "stays in staging" in warned


def test_an_undated_file_the_move_refused_is_said_not_to_have_landed(native_library, silence):
    cfg, _root = native_library
    _dated(cfg, silence, "Undated.flac", None)
    _dated(cfg, silence, "One.flac", "2021")
    code, acted, _ = _two_acts(_land("--label", "PULS"))
    assert code == int(ExitCode.OK), acted
    # Undated.flac again, its target occupied, so the move refuses it.
    _dated(cfg, silence, "Undated.flac", None)
    _dated(cfg, silence, "Two.flac", "2021")

    code, acted, _ = _two_acts(_land("--label", "PULS"))

    assert code == int(ExitCode.OK), acted
    (warned,) = [
        w["message"]
        for w in acted["warnings"]
        if "Undated.flac" in w["message"] and "label playlist" in w["message"]
    ]
    assert "did not land" in warned and "intake playlist" not in warned


def test_the_screen_names_each_label_folder_the_write_makes(native_library, silence):
    cfg, _root = native_library
    tree = cutover_fixtures.add_folder(cfg, TREE)
    cutover_fixtures.add_folder(cfg, "Puls", under=tree)
    _dated(cfg, silence, "One.flac", "2021")

    code, refused = drive(_land("--label", "PULS"))

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _shown(refused)["label folders made"] == ["PULS"]
    code, again = drive(_land("--label", "Puls"))
    assert "label folders made" not in _shown(again)


def test_a_manifest_with_no_label_row_asks_nothing_of_the_catalogue_tree(
    native_library, silence, tmp_path, monkeypatch
):
    """As the bridge's own check returns early on it: a list manifest files nothing."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    rows = [listdoc.Row(ref="1", artist="Probe", title="One")]
    provenance = {"1": listdoc.Provenance(source="list")}
    written = listdoc.write(tmp_path, "intake-missing-test", rows, provenance)
    assert written.manifest_path is not None
    from cratekit.intake import ingest

    real = ingest.intake_medium

    def without_catalog(cfg_):
        medium = real(cfg_)
        return replace(medium, declared=replace(medium.declared, catalog=None))

    monkeypatch.setattr(ingest, "intake_medium", without_catalog)

    code, acted, refused = _two_acts(_land("--manifest", str(written.manifest_path)))

    assert code == int(ExitCode.OK), acted
    assert "labels filed under" not in _shown(refused)
    assert _tree_folders(cfg) == []


# ---------------------------------------------------------------------------
# --label-from-tags (U177): each file under the label its own tag names
# ---------------------------------------------------------------------------


def _labelled(cfg: config.Config, silence: Path, name: str, label: str | None, day: str | None) -> Path:
    """One staged file carrying ``label`` in its label tag, as a Bandcamp fetch writes it."""
    path = _dated(cfg, silence, name, day)
    if label is not None:
        assert tags.write_tags(path, {"label": label})
    return path


def test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label(
    native_library, silence
):
    cfg, _root = native_library
    for year, names in ((2019, ("A1", "A2")), (2021, ("B1",)), (2024, ("C1", "C2"))):
        for name in names:
            _labelled(cfg, silence, f"{name}.flac", "PULS", f"{year}-05-01")

    code, acted, refused = _two_acts(_land("--label-from-tags"))

    assert code == int(ExitCode.OK), acted
    shown = _shown(refused)
    assert shown["labels filed from"] == "each file's own label tag, its year from its date tag"
    assert "filed under no label" not in shown
    assert _filed(cfg) == {
        "PULS": {
            "PULS 2024": ["C1", "C2"],
            "PULS 2021": ["B1"],
            "PULS 2019": ["A1", "A2"],
        }
    }
    (record,) = session.records(cfg)
    assert label_filing.RECORD_KEY in record.detail
    assert label_filing.PROVIDER_KEY not in record.detail


def test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own(
    native_library, silence
):
    """The case one ``--label`` for the batch would file under the wrong label."""
    cfg, _root = native_library
    _labelled(cfg, silence, "Puls.flac", "PULS", "2024")
    _labelled(cfg, silence, "Kompakt.flac", "Kompakt", "2023")
    _labelled(cfg, silence, "Other.flac", None, "2022")

    code, acted, refused = _two_acts(_land("--label-from-tags"))

    assert code == int(ExitCode.OK), acted
    assert _filed(cfg) == {"Kompakt": {"Kompakt 2023": ["Kompakt"]}, "PULS": {"PULS 2024": ["Puls"]}}
    assert _item_labels(refused) == {
        "Puls.flac": "PULS 2024",
        "Kompakt.flac": "Kompakt 2023",
        "Other.flac": "none",
    }
    (unfiled,) = _shown(refused)["filed under no label"]
    assert "Other.flac" in unfiled and "no label tag" in unfiled
    assert sorted(p.name for p in _music(cfg).iterdir()) == ["Kompakt.flac", "Other.flac", "Puls.flac"]
    (warned,) = [w for w in acted["warnings"] if w["code"] == landing.NO_LABEL]
    assert "Other.flac" in warned["message"]


def test_a_labelled_file_with_no_year_is_named_with_its_label_and_filed_nowhere(
    native_library, silence
):
    cfg, _root = native_library
    _labelled(cfg, silence, "Dated.flac", "PULS", "2021")
    _labelled(cfg, silence, "Undated.flac", "PULS", None)

    code, acted, refused = _two_acts(_land("--label-from-tags"))

    assert code == int(ExitCode.OK), acted
    (unfiled,) = _shown(refused)["filed under no label"]
    assert "Undated.flac" in unfiled and "PULS year playlist" in unfiled and "no date tag" in unfiled
    assert _filed(cfg) == {"PULS": {"PULS 2021": ["Dated"]}}


def test_a_label_tag_spelled_decomposed_files_under_the_composed_folder(native_library, silence):
    cfg, _root = native_library
    _labelled(cfg, silence, "One.flac", unicodedata.normalize("NFD", "Sueño"), "2021")
    _labelled(cfg, silence, "Two.flac", unicodedata.normalize("NFC", "Sueño"), "2021")

    code, acted, _ = _two_acts(_land("--label-from-tags"))

    assert code == int(ExitCode.OK), acted
    composed = unicodedata.normalize("NFC", "Sueño")
    assert _filed(cfg) == {composed: {f"{composed} 2021": ["One", "Two"]}}


def test_the_digest_moves_between_one_label_and_each_files_own(native_library, silence):
    cfg, _root = native_library
    _labelled(cfg, silence, "One.flac", "PULS", "2021")

    _code, one = drive(_land("--label", "PULS"))
    _code, own = drive(_land("--label-from-tags"))

    assert _shown(one)["label playlists"] == _shown(own)["label playlists"]
    assert _shown(one)["digest"] != _shown(own)["digest"]


def test_label_from_tags_on_the_bridge_is_refused_before_the_gate_naming_the_flag(
    acknowledged, silence
):
    cfg = acknowledged
    _stage(cfg, silence, "One.flac")
    code, envelope = drive(_land("--label-from-tags"))
    _assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    assert "--label-from-tags" in envelope["cause"]["message"]


@pytest.mark.parametrize("beside", ["--label", "--manifest"])
def test_label_from_tags_beside_another_label_source_is_refused_before_the_gate(
    native_library, silence, tmp_path, beside
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    value = (
        "PULS"
        if beside == "--label"
        else str(_manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)]))
    )
    code, envelope = drive(_land("--label-from-tags", beside, value))
    _assert_refused_before_the_gate(cfg, code, envelope, "intake-list-unusable")
    message = envelope["cause"]["message"]
    assert "--label-from-tags" in message and beside in message


def test_label_from_tags_on_an_unreachable_library_names_the_volume(native_library, silence):
    cfg, _root = native_library
    _labelled(cfg, silence, "One.flac", "PULS", "2021")
    root = Path(cfg.library.root)
    root.rename(root.with_name("unmounted"))

    code, envelope = drive(_land("--label-from-tags"))

    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "library-root-unreachable", envelope
    assert "--label-from-tags" in envelope["cause"]["message"]
    assert _staged_names(cfg) == ["One.flac"]


def test_a_label_tag_that_could_not_be_read_is_said_apart_from_one_that_is_absent(tmp_path):
    broken = tmp_path / "Broken.flac"
    broken.write_bytes(b"not a flac stream")
    plain = synth_container(tmp_path, ".flac")

    assert label_filing._read_label(broken)[0] == ""
    assert "could not be read" in label_filing._read_label(broken)[1]
    assert label_filing._read_label(plain) == ("", "it carries no label tag")
    assert tags.write_tags(plain, {"label": "  PULS  "})
    assert label_filing._read_label(plain) == ("PULS", "")
