"""U77: a landing given a manifest files its label tracks in the same intake file.

Manifests come from the product's own emitter, :func:`listdoc.write`, so the
format pinned is the one ``label approved`` writes. Nothing reaches a real library.
"""

from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path

import pytest

from cratekit.acquire import listdoc
from cratekit.core import config, locations, tags, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import landing
from cratekit.label import approved_cli
from cratekit.write import trees
from tests.test_active_taxonomy import shipped_without, write_active
from tests.test_landing import cfg as cfg
from tests.test_landing import export as export
from tests.test_landing import silence as silence
from tests.test_xml_splice_golden import _check
from tests.xml_fixtures import _fresh_xml, _no_bare_lf

BATCH = "2026-09-19_labels"
DECLARED = taxonomy.default_taxonomy()


def _staging(cfg: config.Config) -> Path:
    return Path(cfg.paths.download_staging)


def _music(cfg: config.Config, batch: str = BATCH) -> Path:
    return Path(cfg.library.root) / cfg.library.music_dir / batch


def _destination(cfg: config.Config, batch: str = BATCH) -> Path:
    return Path(cfg.library.root) / f"{batch}_inboxed.xml"


def _stage(cfg: config.Config, silence: Path, artist: str, title: str) -> Path:
    path = _staging(cfg) / f"{artist} - {title}.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(
        path, {"title": title, "artist": artist, "genre": "Deep House", "energylevel": 7}
    )
    return path


#: ref, artist, title, label, year. The shape every test below lists rows in.
Listed = tuple[str, str, str, str, int | None]


def _manifest(directory: Path, listed: list[Listed], *, source: str = "label") -> Path:
    rows = [listdoc.Row(ref=ref, artist=artist, title=title) for ref, artist, title, _, _ in listed]
    provenance = {
        ref: listdoc.Provenance(
            source=source, label_id=f"id-{label}", label_name=label, year=year, release_id="r"
        )
        for ref, _, _, label, year in listed
    }
    written = listdoc.write(directory, "label-approved-test", rows, provenance)
    assert written.manifest_path is not None
    return written.manifest_path


def _land(cfg, export, manifest, *, batch: str = BATCH, **given) -> landing.Landed:
    planned = landing.plan(_staging(cfg), cfg, batch)
    return landing.apply(
        planned,
        cfg=cfg,
        export=export,
        destination=_destination(cfg, batch),
        manifest=manifest,
        **given,
    )


def _refused(cfg, export, manifest, **given):
    """The cause :func:`_land` refuses with."""
    with pytest.raises(CratekitError) as excinfo:
        _land(cfg, export, manifest, **given)
    return excinfo.value.cause


def _nothing_moved(cfg: config.Config, staged: Path, cause=None) -> None:
    """The batch still staged, no batch folder and no intake file; the refusal says so."""
    assert cause is None or "nothing was moved" in cause.message
    assert staged.exists()
    assert not _music(cfg).exists()
    assert not _destination(cfg).exists()


def _kompakt(path: Path, year: int) -> bytes:
    """A fresh export at ``path`` holding a Kompakt folder of one ``year`` playlist."""
    path.write_bytes(_fresh_xml())
    trees.insert_record_labels_tree(
        path, "Kompakt", {year: [{"track_ids": [900000001]}]}, path,
        declared=DECLARED, registry=tree_registry.EMPTY,
    )
    return path.read_bytes()


def _playlist_keys(body: bytes, name: str) -> list[int]:
    """The track keys under the one playlist node called ``name``."""
    opened = re.findall(
        rb'<NODE Name="' + re.escape(name.encode()) + rb'" Type="1"[^>]*>(.*?)</NODE>', body, re.S
    )
    assert len(opened) == 1, f"{name!r} appears {len(opened)} times"
    return [int(key) for key in re.findall(rb'<TRACK Key="(\d+)"/>', opened[0])]


def _id_of(landed: landing.Landed, stem: str) -> int:
    (found,) = [item.track_id for item in landed.placed if item.path.stem == stem]
    return found


ONE: list[Listed] = [("101", "Ada", "North", "Kompakt", 2025)]
FOUR: list[Listed] = [
    ("101", "Ada", "North", "Kompakt", 2025),
    ("102", "Ada", "South", "Kompakt", 2024),
    ("103", "Bo", "East", "Ostgut Ton", 2025),
    ("104", "Bo", "West", "Ostgut Ton", 2024),
]


def test_the_source_this_engine_reads_is_the_one_label_approved_writes():
    """Two features that may not import each other; a drift would file nothing silently."""
    assert landing.LABEL_SOURCE == approved_cli.LABEL_SOURCE


def test_two_labels_across_two_years_are_four_playlists_in_the_intake_file(
    cfg, silence, export, tmp_path, monkeypatch
):
    for _, artist, title, _, _ in FOUR:
        _stage(cfg, silence, artist, title)
    real = trees.insert_record_labels_trees
    calls: list[list[str]] = []

    def counted(xml_path, catalog, out_path, **kwargs):
        calls.append(sorted(catalog))
        return real(xml_path, catalog, out_path, **kwargs)

    monkeypatch.setattr(trees, "insert_record_labels_trees", counted)
    landed = _land(cfg, export, _manifest(tmp_path, FOUR))
    # The file is a whole collection, so it is rewritten once for every label.
    assert calls == [["Kompakt", "Ostgut Ton"]]
    body = _destination(cfg).read_bytes()
    assert _no_bare_lf(body)
    assert b"<TEMPO" not in body
    assert body.count(b'<NODE Name="Record Labels" Type="0" Count="2">') == 1
    assert body.count(b'<NODE Name="Kompakt" Type="0" Count="2">') == 1
    assert body.count(b'<NODE Name="Ostgut Ton" Type="0" Count="2">') == 1
    assert _playlist_keys(body, "Kompakt 2025") == [_id_of(landed, "Ada - North")]
    assert _playlist_keys(body, "Kompakt 2024") == [_id_of(landed, "Ada - South")]
    assert _playlist_keys(body, "Ostgut Ton 2025") == [_id_of(landed, "Bo - East")]
    assert _playlist_keys(body, "Ostgut Ton 2024") == [_id_of(landed, "Bo - West")]
    assert body.find(b"Kompakt 2025") < body.find(b"Kompakt 2024"), "newest year first"
    assert body.find(b'Name="Kompakt"') < body.find(b'Name="Ostgut Ton"'), "a new tree reads A to Z"
    # ONE file carries both: every landed track is in the intake playlist too.
    assert sorted(_playlist_keys(body, BATCH)) == sorted(
        item.track_id for item in landed.placed
    )
    assert [(entry.playlist, entry.track_ids) for entry in landed.labelled] == [
        ("Kompakt 2025", (_id_of(landed, "Ada - North"),)),
        ("Kompakt 2024", (_id_of(landed, "Ada - South"),)),
        ("Ostgut Ton 2025", (_id_of(landed, "Bo - East"),)),
        ("Ostgut Ton 2024", (_id_of(landed, "Bo - West"),)),
    ]
    assert landed.unlabelled == ()
    # Writing exactly what ``labelled`` claims over the intake file moves nothing.
    again = tmp_path / "again.xml"
    shutil.copyfile(_destination(cfg), again)
    for label in sorted({entry.label for entry in landed.labelled}):
        buckets = {
            entry.year: [{"track_ids": list(entry.track_ids)}]
            for entry in landed.labelled
            if entry.label == label
        }
        trees.insert_record_labels_tree(
            again, label, buckets, again, declared=DECLARED, registry=tree_registry.read(cfg)
        )
    assert again.read_bytes() == body
    # And the whole file, byte for byte, with the library path and today fixed.
    here = locations.location_url(Path(cfg.library.root).resolve()).encode()
    assert body.count(here) == 4
    body = body.replace(here, b"file://localhost/LIBRARY")
    body = re.sub(rb'DateAdded="\d{4}-\d{2}-\d{2}"', b'DateAdded="2026-09-19"', body)
    # The container's size is the tag library's padding, not this product's.
    body, sized = re.subn(rb' Size="\d+"', b' Size="0"', body)
    assert sized == 4
    _check("land_label_tree", body)


def test_one_recording_listed_under_two_ids_is_in_its_year_once(cfg, silence, export, tmp_path):
    """A single and a compilation: two provider ids, one file, named once."""
    _stage(cfg, silence, "Ada", "North")
    manifest = _manifest(
        tmp_path,
        [("101", "Ada", "North", "Kompakt", 2025), ("201", "Ada", "North", "Kompakt", 2025)],
    )
    landed = _land(cfg, export, manifest)
    only = _id_of(landed, "Ada - North")
    body = _destination(cfg).read_bytes()
    assert _playlist_keys(body, "Kompakt 2025") == [only]
    assert b'<NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="1">' in body
    assert [entry.track_ids for entry in landed.labelled] == [(only,)]


def test_an_undeclared_catalog_tree_refuses_before_any_file_moves(
    cfg, silence, export, tmp_path, monkeypatch
):
    staged = _stage(cfg, silence, "Ada", "North")
    manifest = _manifest(tmp_path, ONE)
    # THE LIBRARY'S OWN DECLARATION, on the volume where setup puts it (R-685).
    write_active(cfg, shipped_without("catalog"))
    cause = _refused(cfg, export, manifest)
    assert cause.reason == "catalog-tree-undeclared"
    assert cause.code is ExitCode.LIBRARY_PREREQUISITE
    _nothing_moved(cfg, staged, cause)


def test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing(
    cfg, silence, export, tmp_path, monkeypatch
):
    """The tree is asked about only when something would be written into it."""
    _stage(cfg, silence, "Ada", "North")
    manifest = _manifest(tmp_path, ONE, source="favourites")
    write_active(cfg, shipped_without("catalog"))
    landed = _land(cfg, export, manifest)
    assert len(landed.moved) == 1
    assert landed.labelled == () and landed.unlabelled == ()
    assert b"Record Labels" not in _destination(cfg).read_bytes()


def test_an_export_holding_a_label_folder_twice_refuses_before_any_file_moves(
    cfg, silence, tmp_path
):
    """R-129's refusal, before the moves, which would leave no importable file."""
    staged = _stage(cfg, silence, "Ada", "North")
    body = _kompakt(tmp_path / "once.xml", 2020)
    # The folder holds one playlist, so its own close is the second one.
    start = body.index(b'<NODE Name="Kompakt" Type="0"')
    start = body.rindex(b"\r\n", 0, start) + 2
    close = b"</NODE>\r\n"
    end = body.index(close, body.index(close, start) + 1) + len(close)
    folder = body[start:end]
    doubled = tmp_path / "doubled.xml"
    doubled.write_bytes(body.replace(folder, folder + folder, 1))
    manifest = _manifest(tmp_path, ONE)
    cause = _refused(cfg, doubled, manifest)
    # The person's export, which they mend and take again. Not a defect.
    assert cause.reason == "library-export-unusable"
    assert any("export the collection again" in step for step in cause.remediation.steps)
    assert "Kompakt" in cause.message
    _nothing_moved(cfg, staged, cause)


def test_a_held_year_playlist_the_writer_cannot_extend_refuses_before_any_move(
    cfg, silence, tmp_path
):
    """The trial must reach a held playlist's layout (here, no Entries), or the
    real write refuses AFTER the moves."""
    staged = _stage(cfg, silence, "Ada", "North")
    held = tmp_path / "held.xml"
    body = _kompakt(held, 2025)
    opened = b'<NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="1">'
    assert body.count(opened) == 1
    held.write_bytes(body.replace(opened, b'<NODE Name="Kompakt 2025" Type="1" KeyType="0">'))
    manifest = _manifest(tmp_path, ONE)
    cause = _refused(cfg, held, manifest)
    assert cause.reason == "library-export-unusable"
    assert "Kompakt 2025" in cause.message
    _nothing_moved(cfg, staged)


def test_a_catalog_tree_the_database_owns_refuses_before_any_file_moves(
    cfg, silence, export, tmp_path, monkeypatch
):
    """A tree cut over to the database is never spliced (a second tree would
    grow), and the writer RAISES it: a refusal with the batch still staged."""
    staged = _stage(cfg, silence, "Ada", "North")
    manifest = _manifest(tmp_path, ONE)
    catalog = taxonomy.default_taxonomy().catalog
    assert catalog is not None
    native = tree_registry.Registry(
        (
            tree_registry.TreeRecord(
                tree_id=catalog.id,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=date(2026, 8, 1),
                root_id="123456789",
                source=tree_registry.DerivationSource.TAXONOMY,
            ),
        )
    )
    monkeypatch.setattr(landing.tree_registry, "read", lambda _cfg: native)
    cause = _refused(cfg, export, manifest)
    assert cause.inner is not None and cause.reason == cause.inner.reason
    assert cause.reason != "internal-error"
    assert catalog.id in cause.message
    _nothing_moved(cfg, staged, cause)


def test_a_label_row_no_landed_file_matches_is_reported_by_name(cfg, silence, export, tmp_path):
    _stage(cfg, silence, "Ada", "North")
    _stage(cfg, silence, "Cy", "Unlisted")
    manifest = _manifest(
        tmp_path,
        [("101", "Ada", "North", "Kompakt", 2025), ("102", "Ada", "Never Arrived", "Kompakt", 2025)],
    )
    landed = _land(cfg, export, manifest)
    (missing,) = landed.unlabelled
    assert (missing.ref, missing.artist, missing.title) == ("102", "Ada", "Never Arrived")
    assert (missing.label, missing.year) == ("Kompakt", 2025)
    assert missing.reason == landing.NO_FILE
    assert "Ada - Never Arrived" in missing.sentence
    # True of a download that never arrived AND of a row filed earlier.
    assert "is in the intake playlist" not in missing.sentence
    assert "filed under no label playlist by this run" in missing.sentence
    body = _destination(cfg).read_bytes()
    assert _playlist_keys(body, "Kompakt 2025") == [_id_of(landed, "Ada - North")]
    # The file no row names is filed under no label and is still importable.
    unlisted = _id_of(landed, "Cy - Unlisted")
    assert unlisted in _playlist_keys(body, BATCH)
    assert unlisted not in _playlist_keys(body, "Kompakt 2025")


def test_a_file_at_another_version_is_a_question_and_a_row_with_no_year_files_nothing(
    cfg, silence, export, tmp_path
):
    """An extended mix for an original row is a question only a person answers."""
    _stage(cfg, silence, "Ada", "North (Extended Mix)")
    _stage(cfg, silence, "Bo", "East")
    manifest = _manifest(
        tmp_path, [("101", "Ada", "North", "Kompakt", 2025), ("103", "Bo", "East", "Kompakt", None)]
    )
    landed = _land(cfg, export, manifest)
    asked, undated = sorted(landed.unlabelled, key=lambda entry: entry.ref)
    assert asked.reason == landing.NOT_EXACT
    assert "that file is in the intake playlist" in asked.sentence
    assert undated.reason == landing.NO_LABEL
    assert "year" in undated.sentence
    assert landed.labelled == ()
    assert b"Record Labels" not in _destination(cfg).read_bytes()


def test_a_file_already_in_the_batch_folder_is_not_filed_under_this_landing(
    cfg, silence, export, tmp_path
):
    """A folder landed into twice holds files this intake file gave no id."""
    earlier = _music(cfg) / "Ada - North.flac"
    earlier.parent.mkdir(parents=True)
    staged = _stage(cfg, silence, "Ada", "North")
    shutil.move(staged, earlier)
    _stage(cfg, silence, "Bo", "East")
    manifest = _manifest(
        tmp_path, [("101", "Ada", "North", "Kompakt", 2025), ("103", "Bo", "East", "Kompakt", 2025)]
    )
    landed = _land(cfg, export, manifest)
    assert [entry.ref for entry in landed.unlabelled] == ["101"]
    assert landed.unlabelled[0].reason == landing.NO_FILE
    body = _destination(cfg).read_bytes()
    assert _playlist_keys(body, "Kompakt 2025") == [_id_of(landed, "Bo - East")]


def test_landing_without_a_manifest_writes_no_label_tree(cfg, silence, export):
    _stage(cfg, silence, "Ada", "North")
    landed = _land(cfg, export, None)
    assert landed.labelled == () and landed.unlabelled == ()
    assert b"Record Labels" not in _destination(cfg).read_bytes()


def test_a_second_landing_into_the_first_ones_file_merges_and_duplicates_nothing(
    cfg, silence, export, tmp_path
):
    """Import, export again, land the rest: the export's tree is merged into."""
    _stage(cfg, silence, "Ada", "North")
    listed = [("101", "Ada", "North", "Kompakt", 2025), ("105", "Ada", "Later", "Kompakt", 2025)]
    manifest = _manifest(tmp_path, listed)
    first = _land(cfg, export, manifest)
    held = _id_of(first, "Ada - North")
    _stage(cfg, silence, "Ada", "Later")
    second = _land(cfg, _destination(cfg), manifest, batch="second")
    body = _destination(cfg, "second").read_bytes()
    assert body.count(b'<NODE Name="Record Labels"') == 1
    assert body.count(b'<NODE Name="Kompakt" Type="0"') == 1
    assert _playlist_keys(body, "Kompakt 2025") == [held, _id_of(second, "Ada - Later")]
    assert [entry.ref for entry in second.unlabelled] == ["101"]


def test_a_tree_the_disk_refuses_after_the_moves_is_named_and_the_file_stays(
    cfg, silence, export, tmp_path, monkeypatch
):
    """Every landed file has a routing intent by then, so the file stays and rows are named."""
    _stage(cfg, silence, "Ada", "North")
    _stage(cfg, silence, "Bo", "East")
    manifest = _manifest(
        tmp_path,
        [("101", "Ada", "North", "Kompakt", 2025), ("103", "Bo", "East", "Ostgut Ton", 2025)],
    )

    def full(*_args, **_kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(trees, "insert_record_labels_trees", full)
    landed = _land(cfg, export, manifest)
    assert [(entry.ref, entry.reason) for entry in landed.unlabelled] == [
        ("101", landing.NOT_WRITTEN),
        ("103", landing.NOT_WRITTEN),
    ]
    assert "Ada - North" in landed.unlabelled[0].sentence
    assert "No space left" in landed.unlabelled[0].sentence
    assert landed.labelled == ()
    body = _destination(cfg).read_bytes()
    assert b"Record Labels" not in body
    assert sorted(_playlist_keys(body, BATCH)) == sorted(item.track_id for item in landed.placed)


def test_a_batch_folder_that_cannot_be_indexed_reports_every_label_row(
    cfg, silence, export, tmp_path, monkeypatch
):
    _stage(cfg, silence, "Ada", "North")
    manifest = _manifest(tmp_path, ONE)

    def unreadable(_root, **_kwargs):
        raise OSError(5, "Input/output error")

    monkeypatch.setattr(landing.match, "index_library", unreadable)
    landed = _land(cfg, export, manifest)
    assert [(entry.ref, entry.reason) for entry in landed.unlabelled] == [
        ("101", landing.NOT_WRITTEN)
    ]
    assert landed.labelled == ()
    assert _destination(cfg).exists()


@pytest.mark.parametrize(
    "body, said",
    [
        (b"not json", "not JSON"),
        (json.dumps({"list": 1, "origin": "tidal", "tracks": []}).encode(), "not a manifest"),
        (json.dumps({"manifest": 2, "rows": {}}).encode(), "version 2"),
        (json.dumps({"manifest": 1}).encode(), "no rows"),
        (None, "could not be read"),
    ],
)
def test_a_manifest_that_cannot_be_read_refuses_before_any_file_moves(
    cfg, silence, export, tmp_path, body, said
):
    staged = _stage(cfg, silence, "Ada", "North")
    manifest = tmp_path / "bad.manifest.json"
    if body is not None:
        manifest.write_bytes(body)
    cause = _refused(cfg, export, manifest)
    assert cause.reason == "intake-list-unusable"
    assert said in cause.message
    _nothing_moved(cfg, staged, cause)


def test_a_manifest_rewritten_after_it_was_fingerprinted_is_stale_and_moves_nothing(
    cfg, silence, export, tmp_path
):
    """The engine reads the file again and notices bytes nobody was shown."""
    staged = _stage(cfg, silence, "Ada", "North")
    manifest = _manifest(tmp_path, ONE)
    shown = landing.read_label_manifest(manifest)
    assert shown.playlists() == {"Kompakt 2025": 1}
    manifest.write_bytes(manifest.read_bytes().replace(b"Kompakt", b"Another"))
    cause = _refused(cfg, export, manifest, manifest_digest=shown.digest)
    assert cause.reason == "decision-stale"
    _nothing_moved(cfg, staged)


def test_the_registry_is_read_before_the_first_move_and_never_after(
    cfg, silence, export, tmp_path, monkeypatch
):
    """A failed read after the moves would raise out of a landing that succeeded."""
    _stage(cfg, silence, "Ada", "North")
    manifest = _manifest(tmp_path, ONE)
    real = tree_registry.read
    seen: list[bool] = []

    def watched(config_):
        seen.append(_music(cfg).exists())
        return real(config_)

    monkeypatch.setattr(landing.tree_registry, "read", watched)
    landed = _land(cfg, export, manifest)
    assert len(landed.labelled) == 1
    # Once, before the batch folder exists; the writers are handed it (R-685).
    assert seen == [False]


def test_a_marked_lossy_file_with_no_title_tag_is_still_filed(cfg, silence, export, tmp_path):
    """Read with the library's template, as ``acquire match``, the marker is stripped."""
    marker = (cfg.naming.lossy_marker or "").strip()
    assert marker, "the fixture configuration names no lossy marker"
    # The marker is a HEAD, before the artist, where the template strips it.
    path = _staging(cfg) / f"{marker} Ada - North.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"artist": "Ada", "genre": "Deep House", "energylevel": 7})
    manifest = _manifest(tmp_path, ONE)
    landed = _land(cfg, export, manifest)
    assert landed.unlabelled == ()
    assert [entry.playlist for entry in landed.labelled] == ["Kompakt 2025"]
