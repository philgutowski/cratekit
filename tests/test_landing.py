"""U71: the landing engine moves a staged batch into the library, then splices it.

Real FLAC containers, tagged through the product's own writer, against the
byte fixtures every splice test uses. Nothing here reaches a real library.
"""

from __future__ import annotations

import os
import re
import shutil
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.core import config, locations, tags
from cratekit.core.cause import CratekitError
from cratekit.intake import ingest, landing
from tests._containers import synth_container
from tests.test_config import valid_data
from tests.xml_fixtures import _fresh_xml

BATCH = "2026-09-18_acquired"


@pytest.fixture
def cfg(tmp_path: Path) -> config.Config:
    root = tmp_path / "library"
    root.mkdir()
    staging = tmp_path / "staging"
    staging.mkdir()
    data = valid_data(root)
    data["paths"] = {"download_staging": str(staging)}
    built = config.from_dict(data)
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def silence(tmp_path: Path) -> Path:
    """One real FLAC, made once and copied, so each staged file is readable."""
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    return synth_container(scratch, ".flac")


@pytest.fixture
def export(tmp_path: Path) -> Path:
    path = tmp_path / "fresh.xml"
    path.write_bytes(_fresh_xml())
    return path


def _staging(cfg: config.Config) -> Path:
    return Path(cfg.paths.download_staging)


def _stage(
    cfg: config.Config,
    silence: Path,
    name: str,
    *,
    genre: str | None = "Deep House",
    energy: int | None = 7,
) -> Path:
    path = _staging(cfg) / name
    shutil.copyfile(silence, path)
    fields: dict[str, object] = {"title": Path(name).stem, "artist": "Probe"}
    if genre is not None:
        fields["genre"] = genre
    if energy is not None:
        fields["energylevel"] = energy
    assert tags.write_tags(path, fields) is True
    return path


def _destination(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / f"{BATCH}_inboxed.xml"


def _rows(body: bytes) -> list[bytes]:
    collection = body[body.index(b"<COLLECTION") : body.index(b"</COLLECTION>")]
    return re.findall(rb"<TRACK\b[^>]*?Location=\"([^\"]+)\"", collection, re.S)


def test_three_tagged_files_land_in_one_intake_file(cfg, silence, export):
    for name in ("One.flac", "Two.flac", "Three.flac"):
        _stage(cfg, silence, name)
    planned = landing.plan(_staging(cfg), cfg, BATCH)
    assert [p.name for p in planned.items] == ["One.flac", "Three.flac", "Two.flac"]

    result = landing.apply(
        planned, cfg=cfg, export=export, destination=_destination(cfg)
    )

    target = Path(cfg.library.root) / cfg.library.music_dir / BATCH
    assert sorted(p.name for p in target.iterdir()) == [
        "One.flac",
        "Three.flac",
        "Two.flac",
    ]
    assert not any(_staging(cfg).glob("*.flac"))
    assert result.refused == ()
    assert len(result.moved) == 3
    assert len(result.placed) == 3
    assert len({item.track_id for item in result.placed}) == 3

    body = _destination(cfg).read_bytes()
    assert b'<COLLECTION Entries="3">' in body
    locations_written = _rows(body)
    assert len(locations_written) == 3
    for moved in result.moved:
        assert locations.location_url(moved.target.resolve()).encode() in locations_written
    assert b"staging" not in b"".join(locations_written)
    assert body.count(f'Name="{BATCH}_inboxed"'.encode()) == 1
    assert b"<TEMPO" not in body


def test_a_name_collision_refuses_that_file_and_lands_the_rest(cfg, silence, export):
    for name in ("Keep.flac", "Clash.flac", "Also.flac"):
        _stage(cfg, silence, name)
    target = Path(cfg.library.root) / cfg.library.music_dir / BATCH
    target.mkdir(parents=True)
    kept = target / "Clash.flac"
    kept.write_bytes(b"the copy somebody kept")

    result = landing.apply(
        landing.plan(_staging(cfg), cfg, BATCH),
        cfg=cfg,
        export=export,
        destination=_destination(cfg),
    )

    assert kept.read_bytes() == b"the copy somebody kept"
    assert (_staging(cfg) / "Clash.flac").is_file()
    assert [entry.path.name for entry in result.refused] == ["Clash.flac"]
    assert result.refused[0].reason == "output-exists"
    assert "already exists" in result.refused[0].sentence
    assert sorted(item.target.name for item in result.moved) == ["Also.flac", "Keep.flac"]
    assert len(_rows(_destination(cfg).read_bytes())) == 2


def test_a_file_with_no_genre_or_energy_lands_in_the_fallback_bucket(
    cfg, silence, export
):
    """DRIVEN, not assumed. The shipped taxonomy resolves an empty genre and
    an absent energy to a bucket that declares a sub, so the untagged file
    lands and is placed, not refused."""
    _stage(cfg, silence, "Tagged.flac")
    bare = _stage(cfg, silence, "Bare.flac", genre=None, energy=None)
    assert tags.read_genre_from_file(bare) is None
    assert tags.read_energy_from_file(bare) is None

    result = landing.apply(
        landing.plan(_staging(cfg), cfg, BATCH),
        cfg=cfg,
        export=export,
        destination=_destination(cfg),
    )

    assert result.refused == ()
    placed = {item.path.name: item for item in result.placed}
    assert set(placed) == {"Bare.flac", "Tagged.flac"}
    assert placed["Bare.flac"].bucket
    assert placed["Bare.flac"].sub
    assert placed["Bare.flac"].bucket != placed["Tagged.flac"].bucket


def test_a_file_with_no_declared_sub_is_left_in_staging_naming_tag_folder(
    cfg, silence, export, monkeypatch
):
    """The other branch of the same scenario. The shipped taxonomy never
    produces it, so a placement that answers None is substituted, and the
    refusal is the engine's own, made before the file moves."""
    _stage(cfg, silence, "Placed.flac")
    _stage(cfg, silence, "Nowhere.flac", genre="Nowhere Genre")
    real = ingest.decide_placement
    monkeypatch.setattr(
        ingest,
        "decide_placement",
        lambda meta: None if meta.get("genre") == "Nowhere Genre" else real(meta),
    )

    result = landing.apply(
        landing.plan(_staging(cfg), cfg, BATCH),
        cfg=cfg,
        export=export,
        destination=_destination(cfg),
    )

    assert (_staging(cfg) / "Nowhere.flac").is_file()
    assert [entry.path.name for entry in result.refused] == ["Nowhere.flac"]
    assert "crate tag folder" in result.refused[0].sentence
    assert [item.path.name for item in result.placed] == ["Placed.flac"]


def test_a_stub_export_is_refused_before_any_move(cfg, silence, tmp_path):
    staged = [_stage(cfg, silence, name) for name in ("One.flac", "Two.flac")]
    stub = tmp_path / "stub.xml"
    stub.write_bytes(
        b'<?xml version="1.0" encoding="UTF-8"?>\r\n<DJ_PLAYLISTS>\r\n'
        b'  <COLLECTION Entries="1">\r\n    <TRACK Name="A - One"/>\r\n'
        b"  </COLLECTION>\r\n</DJ_PLAYLISTS>\r\n"
    )

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(
            landing.plan(_staging(cfg), cfg, BATCH),
            cfg=cfg,
            export=stub,
            destination=_destination(cfg),
        )

    assert excinfo.value.cause.reason == "intake-export-is-stub"
    assert all(path.is_file() for path in staged)
    assert not (Path(cfg.library.root) / cfg.library.music_dir).exists()
    assert not _destination(cfg).exists()


def test_an_export_with_no_intake_folder_is_refused_before_any_move(
    cfg, silence, tmp_path
):
    staged = _stage(cfg, silence, "One.flac")
    bare = tmp_path / "bare.xml"
    bare.write_bytes(_fresh_xml().replace(b'Name="INBOX"', b'Name="ELSEWHERE"'))

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(
            landing.plan(_staging(cfg), cfg, BATCH),
            cfg=cfg,
            export=bare,
            destination=_destination(cfg),
        )

    assert excinfo.value.cause.reason == "library-export-unusable"
    assert "nothing was moved" in excinfo.value.cause.message
    assert staged.is_file()


def test_a_missing_export_is_refused_before_any_move(cfg, silence, tmp_path):
    staged = _stage(cfg, silence, "One.flac")
    with pytest.raises(CratekitError) as excinfo:
        landing.apply(
            landing.plan(_staging(cfg), cfg, BATCH),
            cfg=cfg,
            export=tmp_path / "absent.xml",
            destination=_destination(cfg),
        )
    assert excinfo.value.cause.reason == "library-export-unusable"
    assert staged.is_file()


def test_an_added_file_makes_the_plan_stale(cfg, silence, export):
    first = _stage(cfg, silence, "One.flac")
    planned = landing.plan(_staging(cfg), cfg, BATCH)
    _stage(cfg, silence, "Late.flac")

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(planned, cfg=cfg, export=export, destination=_destination(cfg))

    assert excinfo.value.cause.reason == "decision-stale"
    assert first.is_file()
    assert not _destination(cfg).exists()


def test_a_file_replaced_under_the_same_name_makes_the_plan_stale(
    cfg, silence, export
):
    """The digest is not of names alone. Same name, same count, new bytes."""
    staged = _stage(cfg, silence, "One.flac")
    planned = landing.plan(_staging(cfg), cfg, BATCH)
    tags.write_tags(staged, {"title": "A Different Recording, Longer Title"})
    stat = staged.stat()
    os.utime(staged, ns=(stat.st_atime_ns, stat.st_mtime_ns + 5_000_000_000))

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(planned, cfg=cfg, export=export, destination=_destination(cfg))
    assert excinfo.value.cause.reason == "decision-stale"
    assert staged.is_file()


def test_a_touched_file_of_the_same_size_makes_the_plan_stale(cfg, silence, export):
    staged = _stage(cfg, silence, "One.flac")
    planned = landing.plan(_staging(cfg), cfg, BATCH)
    stat = staged.stat()
    os.utime(staged, ns=(stat.st_atime_ns, stat.st_mtime_ns + 5_000_000_000))
    assert staged.stat().st_size == stat.st_size

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(planned, cfg=cfg, export=export, destination=_destination(cfg))
    assert excinfo.value.cause.reason == "decision-stale"


def test_the_listing_is_flat_audio_only_and_skips_dotfiles(cfg, silence):
    _stage(cfg, silence, "Keep.flac")
    (_staging(cfg) / ".hidden.flac").write_bytes(b"x")
    (_staging(cfg) / "notes.txt").write_text("x")
    partial = _staging(cfg) / landing.ACQUIRE_STAGING_DIRNAME / "job" / "1"
    partial.mkdir(parents=True)
    (partial / "Half.flac").write_bytes(b"x")
    nested = _staging(cfg) / "lists"
    nested.mkdir()
    (nested / "Deep.flac").write_bytes(b"x")

    planned = landing.plan(_staging(cfg), cfg, BATCH)
    assert [p.name for p in planned.items] == ["Keep.flac"]


def test_an_empty_folder_is_refused_at_plan(cfg):
    (_staging(cfg) / "notes.txt").write_text("x")
    with pytest.raises(CratekitError) as excinfo:
        landing.plan(_staging(cfg), cfg, BATCH)
    assert excinfo.value.cause.reason == "intake-list-unusable"


@pytest.mark.parametrize("batch", ["", "..", ".hidden", "a/b", " padded", "a\\b"])
def test_a_batch_name_that_is_not_one_plain_folder_is_refused(cfg, silence, batch):
    _stage(cfg, silence, "One.flac")
    with pytest.raises(CratekitError) as excinfo:
        landing.plan(_staging(cfg), cfg, batch)
    assert excinfo.value.cause.reason == "intake-list-unusable"


def test_a_staging_folder_on_another_device_is_refused_by_name(
    cfg, silence, export, monkeypatch
):
    staged = _stage(cfg, silence, "One.flac")
    planned = landing.plan(_staging(cfg), cfg, BATCH)
    staging = _staging(cfg)
    real = landing._device_of
    monkeypatch.setattr(
        landing, "_device_of", lambda path: -1 if path == staging else real(path)
    )

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(planned, cfg=cfg, export=export, destination=_destination(cfg))

    assert excinfo.value.cause.reason == "intake-staging-refused"
    assert "different device" in excinfo.value.cause.message
    assert str(staging) in excinfo.value.cause.message
    assert staged.is_file()
    assert not (Path(cfg.library.root) / cfg.library.music_dir).exists()


def test_an_absent_library_root_is_refused_before_the_device_probe(
    cfg, silence, export
):
    staged = _stage(cfg, silence, "One.flac")
    planned = landing.plan(_staging(cfg), cfg, BATCH)
    root = Path(cfg.library.root)
    shutil.rmtree(root)

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(planned, cfg=cfg, export=export, destination=_destination(cfg))

    assert excinfo.value.cause.reason == "library-root-unreachable"
    assert not root.exists()
    assert staged.is_file()


def test_a_landing_target_under_staging_is_refused(cfg, silence, export):
    """Staging configured as the music folder itself. Built from the root the
    configuration actually holds, since the suite redirects the root."""
    music = Path(cfg.library.root) / cfg.library.music_dir
    music.mkdir()
    inside = replace(cfg, paths=replace(cfg.paths, download_staging=music))
    staged = music / "One.flac"
    shutil.copyfile(silence, staged)

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(
            landing.plan(music, inside, BATCH),
            cfg=inside,
            export=export,
            destination=_destination(cfg),
        )
    assert excinfo.value.cause.reason == "intake-staging-refused"
    assert staged.is_file()
    assert not (music / BATCH).exists()


def test_an_existing_intake_file_is_never_overwritten(cfg, silence, export):
    staged = _stage(cfg, silence, "One.flac")
    _destination(cfg).write_bytes(b"an earlier batch")

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(
            landing.plan(_staging(cfg), cfg, BATCH),
            cfg=cfg,
            export=export,
            destination=_destination(cfg),
        )

    assert excinfo.value.cause.reason == "output-exists"
    assert _destination(cfg).read_bytes() == b"an earlier batch"
    assert staged.is_file()


def test_every_file_refused_writes_nothing(cfg, silence, export):
    _stage(cfg, silence, "Clash.flac")
    target = Path(cfg.library.root) / cfg.library.music_dir / BATCH
    target.mkdir(parents=True)
    (target / "Clash.flac").write_bytes(b"kept")

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(
            landing.plan(_staging(cfg), cfg, BATCH),
            cfg=cfg,
            export=export,
            destination=_destination(cfg),
        )

    assert excinfo.value.cause.reason == "intake-list-unusable"
    assert "Clash.flac" in excinfo.value.cause.message
    assert not _destination(cfg).exists()


def test_a_move_that_fails_part_way_names_what_moved_and_writes_no_xml(
    cfg, silence, export, monkeypatch
):
    for name in ("A.flac", "B.flac", "C.flac"):
        _stage(cfg, silence, name)
    planned = landing.plan(_staging(cfg), cfg, BATCH)
    real = os.replace

    def replace(src, dst):
        if Path(src).name == "B.flac":
            raise PermissionError(13, "Permission denied", str(src))
        return real(src, dst)

    monkeypatch.setattr(landing.os, "replace", replace)

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(planned, cfg=cfg, export=export, destination=_destination(cfg))

    cause = excinfo.value.cause
    assert cause.reason == "path-permission-denied"
    assert "A.flac" in cause.message
    assert cause.detail["moved"] == [
        str(Path(cfg.library.root) / cfg.library.music_dir / BATCH / "A.flac")
    ]
    assert not _destination(cfg).exists()
    assert (_staging(cfg) / "B.flac").is_file()
    assert (_staging(cfg) / "C.flac").is_file()


def test_a_splice_that_fails_after_the_moves_names_them_and_leaves_no_xml(
    cfg, silence, export, monkeypatch
):
    """``place_files`` writes the intake file before it records intents, so a
    ledger failure arrives after the write. The engine removes what this call
    wrote and names the files it already moved, which now belong to the
    library."""
    for name in ("A.flac", "B.flac"):
        _stage(cfg, silence, name)
    planned = landing.plan(_staging(cfg), cfg, BATCH)

    def broken_ledger(_cfg, _intents):
        assert _destination(cfg).is_file()
        raise OSError("the routing ledger could not be written")

    monkeypatch.setattr(ingest.routing_pass, "record_intents", broken_ledger)

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(planned, cfg=cfg, export=export, destination=_destination(cfg))

    cause = excinfo.value.cause
    assert "A.flac" in cause.message and "B.flac" in cause.message
    assert len(cause.detail["moved"]) == 2
    assert not _destination(cfg).exists()
    target = Path(cfg.library.root) / cfg.library.music_dir / BATCH
    assert sorted(p.name for p in target.iterdir()) == ["A.flac", "B.flac"]


def test_a_refusal_from_place_files_keeps_its_own_reason(
    cfg, silence, export, monkeypatch
):
    _stage(cfg, silence, "A.flac")
    planned = landing.plan(_staging(cfg), cfg, BATCH)

    def refusing(*_args, **_kwargs):
        raise ingest.refuse(
            "intake-list-unusable", "a refusal only place_files can make"
        )

    monkeypatch.setattr(ingest, "place_files", refusing)

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(planned, cfg=cfg, export=export, destination=_destination(cfg))
    cause = excinfo.value.cause
    assert cause.reason == "intake-list-unusable"
    assert cause.inner is not None
    assert "A.flac" in cause.message


def test_a_batch_where_nothing_lands_leaves_no_batch_folder(
    cfg, silence, export, monkeypatch
):
    """The review's shape: every file refused, and the batch folder did not
    exist before the call. The earlier test made that folder itself, so it
    could never see one left behind."""
    _stage(cfg, silence, "Nowhere.flac", genre="Nowhere Genre")
    monkeypatch.setattr(ingest, "decide_placement", lambda meta: None)
    target = Path(cfg.library.root) / cfg.library.music_dir / BATCH

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(
            landing.plan(_staging(cfg), cfg, BATCH),
            cfg=cfg,
            export=export,
            destination=_destination(cfg),
        )

    assert excinfo.value.cause.reason == "intake-list-unusable"
    assert "crate tag folder" in excinfo.value.cause.message
    assert not target.exists()
    assert not _destination(cfg).exists()


def test_a_first_move_that_fails_leaves_no_batch_folder(
    cfg, silence, export, monkeypatch
):
    _stage(cfg, silence, "A.flac")
    planned = landing.plan(_staging(cfg), cfg, BATCH)

    def replace(src, _dst):
        raise PermissionError(13, "Permission denied", str(src))

    monkeypatch.setattr(landing.os, "replace", replace)
    with pytest.raises(CratekitError) as excinfo:
        landing.apply(planned, cfg=cfg, export=export, destination=_destination(cfg))

    assert excinfo.value.cause.detail["moved"] == []
    assert "nothing was moved" in excinfo.value.cause.message
    assert not (Path(cfg.library.root) / cfg.library.music_dir / BATCH).exists()


def test_a_file_arriving_between_the_passes_is_not_replaced(
    cfg, silence, export, monkeypatch
):
    """The check is asked again at the move. A file of the same name that
    appears after the first pass is refused, not overwritten."""
    _stage(cfg, silence, "A.flac")
    _stage(cfg, silence, "B.flac")
    target = Path(cfg.library.root) / cfg.library.music_dir / BATCH
    real = os.replace

    def replace(src, dst):
        result = real(src, dst)
        if Path(src).name == "A.flac":
            (target / "B.flac").write_bytes(b"arrived in between")
        return result

    monkeypatch.setattr(landing.os, "replace", replace)
    result = landing.apply(
        landing.plan(_staging(cfg), cfg, BATCH),
        cfg=cfg,
        export=export,
        destination=_destination(cfg),
    )

    assert (target / "B.flac").read_bytes() == b"arrived in between"
    assert [entry.path.name for entry in result.refused] == ["B.flac"]
    assert (_staging(cfg) / "B.flac").is_file()


def test_a_folder_the_library_already_owns_is_refused(cfg, silence, export):
    owned = Path(cfg.library.root) / cfg.library.music_dir / "OldBatch"
    owned.mkdir(parents=True)
    kept = owned / "Owned.flac"
    shutil.copyfile(silence, kept)

    with pytest.raises(CratekitError) as excinfo:
        landing.apply(
            landing.plan(owned, cfg, BATCH),
            cfg=cfg,
            export=export,
            destination=_destination(cfg),
        )

    assert excinfo.value.cause.reason == "intake-list-unusable"
    assert "already owned" in excinfo.value.cause.message
    assert kept.is_file()
    assert not (owned.parent / BATCH).exists()


def test_staging_configured_inside_the_library_still_lands(cfg, silence, export):
    downloads = Path(cfg.library.root) / "Downloads"
    downloads.mkdir()
    inside = replace(cfg, paths=replace(cfg.paths, download_staging=downloads))
    shutil.copyfile(silence, downloads / "One.flac")

    result = landing.apply(
        landing.plan(downloads, inside, BATCH),
        cfg=inside,
        export=export,
        destination=_destination(cfg),
    )

    assert [item.target.name for item in result.moved] == ["One.flac"]
    assert not (downloads / "One.flac").exists()


def test_a_directory_named_like_audio_is_not_listed(cfg, silence):
    _stage(cfg, silence, "Keep.flac")
    (_staging(cfg) / "Album.flac").mkdir()
    planned = landing.plan(_staging(cfg), cfg, BATCH)
    assert [p.name for p in planned.items] == ["Keep.flac"]


def test_every_file_taken_at_the_move_writes_no_intake_file(
    cfg, silence, export, monkeypatch
):
    """Every file passes the first pass and is found occupied at the move, the
    shape a concurrent landing produces. No intake file, no batch folder."""
    _stage(cfg, silence, "A.flac")
    _stage(cfg, silence, "B.flac")
    real = landing._occupied
    calls = {"n": 0}

    def occupied(item, final):
        calls["n"] += 1
        if calls["n"] <= 2:
            return real(item, final)
        return landing.Refused(path=item, reason="output-exists", sentence="taken")

    monkeypatch.setattr(landing, "_occupied", occupied)
    with pytest.raises(CratekitError) as excinfo:
        landing.apply(
            landing.plan(_staging(cfg), cfg, BATCH),
            cfg=cfg,
            export=export,
            destination=_destination(cfg),
        )

    assert excinfo.value.cause.reason == "intake-list-unusable"
    assert not _destination(cfg).exists()
    assert not (Path(cfg.library.root) / cfg.library.music_dir / BATCH).exists()
    assert (_staging(cfg) / "A.flac").is_file()
