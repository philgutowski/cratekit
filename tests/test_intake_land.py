"""U72: ``crate intake land`` plans, stops at its gate, then lands the batch.

Every test drives the real dispatcher over real FLAC containers tagged through
the product's own writer, against the byte fixture every splice test uses. The
engine's own refusals are pinned in ``tests/test_landing.py``; this file pins
what the verb adds: nothing moves before an answer, a stale answer moves
nothing, and a landed batch leaves a pending import a person can see.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.acquire import listdoc
from cratekit.cli import gates, output, registry
from cratekit.core import config, session, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, land_cli, landing, native
from tests._containers import synth_container
from tests.test_config import valid_data
from tests.xml_fixtures import _fresh_xml

GATE = "intake.land.confirm"
BATCH = "2026-09-18_favourites"
GUIDE = Path(__file__).resolve().parents[1] / "docs" / "GUIDE.md"


@pytest.fixture
def cfg(tmp_path: Path) -> config.Config:
    """A saved configuration the verb loads, with staging beside the library.

    The library root is whatever the autouse fixture set, so every path below
    is read back off the loaded value.
    """
    root = tmp_path / "library"
    root.mkdir()
    staging = tmp_path / "staging"
    staging.mkdir()
    data = valid_data(root)
    data["paths"] = {"download_staging": str(staging)}
    built = config.from_dict(data)
    Path(built.library.root).mkdir(parents=True, exist_ok=True)
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def silence(tmp_path: Path) -> Path:
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


def _stage(cfg: config.Config, silence: Path, name: str) -> Path:
    path = _staging(cfg) / name
    shutil.copyfile(silence, path)
    assert tags.write_tags(
        path,
        {"title": Path(name).stem, "artist": "Probe", "genre": "Deep House", "energylevel": 7},
    )
    return path


def _music(cfg: config.Config, batch: str) -> Path:
    return Path(cfg.library.root) / cfg.library.music_dir / batch


def _intake(cfg: config.Config, batch: str) -> Path:
    return Path(cfg.library.root) / f"{batch}_inboxed.xml"


def _drive(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    document = json.loads(out.getvalue())
    assert output.envelope_problems(document) == [], document
    return code, document


def _human(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def _land(export: Path, *extra: str) -> list[str]:
    return ["intake", "land", "--export", str(export), *extra]


def _answered(export: Path, *extra: str, answer: str = "apply") -> list[str]:
    return ["-d", f"{GATE}={answer}", *_land(export, *extra)]


def _decided(export: Path, *extra: str, answer: str = "apply") -> str:
    """Plan to the gate, record ``answer`` as a separate act, and answer the run id."""
    code, refused = _drive(_land(export, *extra))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    decided, _ = _drive(["run", "decide", refused["run_id"], GATE, answer, "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    return refused["run_id"]


def _staged_names(cfg: config.Config) -> list[str]:
    return sorted(p.name for p in _staging(cfg).glob("*.flac"))


def test_the_first_run_stops_at_the_gate_and_moves_nothing(cfg, silence, export):
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)

    code, refused = _drive(_land(export, "--name", BATCH))

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE
    assert detail["options"] == ["apply", "abort"]
    shown = detail["shown"]
    assert shown["files"] == ["One.flac", "Two.flac"]
    assert shown["lands in"] == str(_music(cfg, BATCH))
    assert shown["intake file"] == str(_intake(cfg, BATCH))
    # U127: an uncalibrated library is told to calibrate, never to tag from the default cut.
    assert shown["vox My Tag"].startswith(land_cli.BRIDGE_VOX_NONE)
    assert native.VOX_UNCALIBRATED in shown["vox My Tag"]
    assert _staged_names(cfg) == ["One.flac", "Two.flac"]
    assert not _music(cfg, BATCH).exists()
    assert not _intake(cfg, BATCH).exists()


def test_on_a_calibrated_library_the_bridge_screen_names_the_vocals_verb_as_owed(
    cfg, silence, export
):
    """U127. The bridge cannot carry a My Tag, so its screen names the step owed."""
    from tests.test_intake_land_vox_native import _calibrate

    _calibrate(cfg)
    _stage(cfg, silence, "One.flac")
    code, refused = _drive(_land(export, "--name", BATCH))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["vox My Tag"] == land_cli.BRIDGE_VOX_OWED
    assert "crate metadata mytags-vocals --apply" in shown["vox My Tag"]


def test_the_gate_screen_a_person_reads_names_the_files_and_the_intake_file(cfg, silence, export):
    """The plan payload never reaches a person reading the default output."""
    _stage(cfg, silence, "One.flac")
    code, _out, screen = _human(_land(export, "--name", BATCH))
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert "One.flac" in screen
    assert f"{BATCH}_inboxed.xml" in screen
    assert str(_music(cfg, BATCH)) in screen
    assert "crate run decide" in screen and GATE in screen


def test_an_answered_run_lands_the_batch_and_names_the_xml_in_human_output(cfg, silence, export):
    """R34's two acts, then the landing, read the way a person reads it."""
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    run_id = _decided(export, "--name", BATCH)

    code, out, err = _human(["--run", run_id, *_land(export, "--name", BATCH)])

    assert code == int(ExitCode.PENDING_HUMAN), err
    human = out + err
    assert str(_intake(cfg, BATCH)) in human
    assert "verify: intake.imported" in human
    assert "blocks:" not in human
    assert sorted(p.name for p in _music(cfg, BATCH).iterdir()) == ["One.flac", "Two.flac"]
    assert _staged_names(cfg) == []
    body = _intake(cfg, BATCH).read_bytes()
    assert b'<COLLECTION Entries="2">' in body
    assert b"<TEMPO" not in body


def test_the_landed_envelope_carries_an_import_that_blocks_nothing(cfg, silence, export):
    """The pending action is the intake session's, read back, so the two cannot
    differ (R-501). ``blocks`` stays empty: no cost of an unimported landing
    was driven to justify refusing every verb it names."""
    _stage(cfg, silence, "One.flac")
    code, envelope = _drive(_answered(export, "--name", BATCH))

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["outcome"] == "pending"
    pending = envelope["pending_human_action"]
    assert pending["kind"] == "rekordbox_import"
    assert pending["artifact"] == str(_intake(cfg, BATCH))
    assert pending["verify_verb"] == "intake.imported"
    assert pending["verify_verb"] in registry.VERB_NAMES
    assert pending["blocks"] == []
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.AWAITING_IMPORT
    assert record.pending is not None
    assert record.pending.to_json() == pending
    data = envelope["data"]
    assert [item["action"] for item in data["items"]] == ["landed"]
    # A landing without a manifest reports nothing about labels.
    assert data["totals"] == {"count": 1, "landed": 1, "refused": 0}
    assert "label playlist" not in pending["summary"]


@pytest.mark.parametrize("change", ["a file arrived", "batch name", "export", "folder"])
def test_an_answer_is_stale_for_any_other_plan_and_moves_nothing(
    cfg, silence, export, tmp_path, change
):
    """The digest covers the files, where they go, the export they are spliced
    into, and the folder itself, since two folders can match on names, sizes
    and times. Each is a plan the person never saw."""
    _stage(cfg, silence, "One.flac")
    run_id = _decided(export, "--name", BATCH)
    argv = _land(export, "--name", BATCH)
    twin = _staging(cfg) / "twin"
    if change == "a file arrived":
        _stage(cfg, silence, "Arrived.flac")
    elif change == "batch name":
        argv = _land(export, "--name", "elsewhere")
    elif change == "export":
        other = tmp_path / "other.xml"
        other.write_bytes(export.read_bytes())
        argv = _land(other, "--name", BATCH)
    else:
        twin.mkdir()
        shutil.copy2(_staging(cfg) / "One.flac", twin / "One.flac")
        argv = _land(export, str(twin), "--name", BATCH)

    code, envelope = _drive(["--run", run_id, *argv])

    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert code != int(ExitCode.OK)
    arrived = ["Arrived.flac"] if change == "a file arrived" else []
    assert _staged_names(cfg) == [*arrived, "One.flac"]
    assert not _music(cfg, BATCH).exists() and not _music(cfg, "elsewhere").exists()
    assert change != "folder" or (twin / "One.flac").is_file()


def test_staging_holding_only_lists_and_dotfiles_is_a_plan_of_nothing(cfg, export):
    """What staging holds between landings: the lists folder, the unfinished
    download directory, a Finder dotfile and a sync's intake file. None is audio."""
    staging = _staging(cfg)
    (staging / "lists").mkdir()
    (staging / ".cratekit-acquire-staging").mkdir()
    (staging / ".DS_Store").write_bytes(b"\0")
    (staging / "run_synced.xml").write_bytes(b"<DJ_PLAYLISTS/>")

    code, envelope = _drive(_answered(export, "--name", BATCH))

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["items"] == []


def test_an_abort_is_no_op_and_moves_nothing(cfg, silence, export):
    _stage(cfg, silence, "One.flac")
    code, envelope = _drive(_answered(export, "--name", BATCH, answer="abort"))

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["pending_human_action"] is None
    assert [item["action"] for item in envelope["data"]["items"]] == ["land"]
    assert _staged_names(cfg) == ["One.flac"]
    assert not _music(cfg, BATCH).exists()


def test_the_folder_defaults_to_staging_the_batch_to_the_date_and_the_file_to_the_run(
    cfg, silence, export, monkeypatch
):
    """U110. The batch a person reads in INBOX is the date and the source, and
    the run's identifier, colons removed, names only the intake file."""
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 3))
    _stage(cfg, silence, "One.flac")
    code, envelope = _drive(_answered(export))

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert (_music(cfg, "2026-10-03 Downloads") / "One.flac").is_file()
    stem = land_cli.default_name(envelope["run_id"])
    assert ":" not in stem
    assert stem == envelope["run_id"].replace(":", "")
    assert envelope["pending_human_action"]["artifact"] == str(_intake(cfg, stem))


def test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing(cfg, export):
    """The step still asks, and applying nothing makes no batch folder, no
    intake file and no pending import."""
    code, refused = _drive(_land(export, "--name", BATCH))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["files"] == []

    code, envelope = _drive(_answered(export, "--name", BATCH))

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["pending_human_action"] is None
    assert envelope["data"]["items"] == []
    assert not _music(cfg, BATCH).exists()
    assert not _intake(cfg, BATCH).exists()
    # A plan of nothing splices nothing, so it is not refused over the export.
    code, refused = _drive(_land(export.with_name("absent.xml"), "--name", BATCH))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["count"] == 0


def test_a_folder_that_is_not_there_is_refused_before_the_gate(cfg, export, tmp_path):
    code, envelope = _drive(_land(export, str(tmp_path / "absent"), "--name", BATCH))

    assert envelope["cause"]["reason"] == "intake-list-unusable", envelope
    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED))


def _occupied(cfg: config.Config, silence: Path, kept: bytes) -> Path:
    """Two files staged, and the batch folder already holding one of their names."""
    for name in ("Keep.flac", "Clash.flac"):
        _stage(cfg, silence, name)
    occupied = _music(cfg, BATCH)
    occupied.mkdir(parents=True)
    (occupied / "Clash.flac").write_bytes(kept)
    return occupied / "Clash.flac"


def test_a_refused_file_is_a_warning_a_person_reads(cfg, silence, export):
    clash = _occupied(cfg, silence, b"the copy somebody kept")

    code, out, err = _human(_answered(export, "--name", BATCH))

    assert code == int(ExitCode.PENDING_HUMAN)
    assert re.search(r"warning \[output-exists\]: .*Clash\.flac", out + err), out + err
    assert clash.read_bytes() == b"the copy somebody kept"
    assert _staged_names(cfg) == ["Clash.flac"]


def test_the_refused_item_is_marked_in_the_plan_payload(cfg, silence, export):
    _occupied(cfg, silence, b"kept")

    code, envelope = _drive(_answered(export, "--name", BATCH))

    items = {Path(item["from"]).name: item for item in envelope["data"]["items"]}
    assert items["Keep.flac"]["action"] == "landed"
    assert items["Clash.flac"]["action"] == "refused"
    assert items["Clash.flac"]["reason"] == "output-exists"
    assert envelope["data"]["totals"] == {"count": 2, "landed": 1, "refused": 1}


def _manifest(tmp_path: Path, listed: list[tuple[str, str, str, str, int]]) -> Path:
    """Written by the product's own emitter, the way ``label approved`` does."""
    rows = [listdoc.Row(ref=ref, artist=artist, title=title) for ref, artist, title, _, _ in listed]
    provenance = {
        ref: listdoc.Provenance(source="label", label_name=label, year=year)
        for ref, _, _, label, year in listed
    }
    written = listdoc.write(tmp_path, "label-approved-verb", rows, provenance)
    assert written.manifest_path is not None
    return written.manifest_path


def test_a_manifest_is_on_the_gate_screen_and_its_labels_are_in_the_envelope(
    cfg, silence, export, tmp_path
):
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(
        tmp_path,
        [("1", "Probe", "One", "Kompakt", 2025), ("2", "Probe", "Never Arrived", "Kompakt", 2024)],
    )
    argv = _land(export, "--name", BATCH, "--manifest", str(manifest))

    code, refused = _drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["labels filed from"] == str(manifest)
    assert shown["label playlists named"] == ["Kompakt 2024 (1 listed)", "Kompakt 2025 (1 listed)"]

    code, envelope = _drive(["-d", f"{GATE}=apply", *argv])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    data = envelope["data"]
    assert [item["action"] for item in data["items"]] == ["landed", "filed", "unfiled"]
    assert data["items"][1] == {
        "action": "filed",
        "label": "Kompakt",
        "year": 2025,
        "playlist": "Kompakt 2025",
        "count": 1,
    }
    unfiled = data["items"][2]
    assert (unfiled["id"], unfiled["title"], unfiled["reason"]) == (
        "2",
        "Never Arrived",
        "label-row-unmatched",
    )
    assert data["totals"] == {"count": 1, "landed": 1, "refused": 0, "filed": 1, "unfiled": 1}
    (warning,) = envelope["warnings"]
    assert warning["code"] == "label-row-unmatched"
    assert "Probe - Never Arrived" in warning["message"]
    # The pending action is the one the session persisted before any label was
    # filed, so its summary names the file and not what was filed into it.
    assert f"{BATCH}_inboxed.xml" in envelope["pending_human_action"]["summary"]
    body = _intake(cfg, BATCH).read_bytes()
    assert b'<NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="1">' in body


def test_an_answer_given_against_one_manifest_is_stale_once_it_is_rewritten(
    cfg, silence, export, tmp_path
):
    """The same path holding other rows files other tracks under other labels,
    so the bytes are what the gate compares and not the name."""
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])
    extra = ("--name", BATCH, "--manifest", str(manifest))
    run_id = _decided(export, *extra)

    manifest.write_bytes(manifest.read_bytes().replace(b"Kompakt", b"Another"))
    code, stale = _drive(["--run", run_id, *_land(export, *extra)])

    assert stale["cause"]["reason"] == "decision-stale", stale
    # THE GATE'S refusal and not the engine's, which carries the same reason one
    # layer down: each is removed alone in the mutation table.
    assert stale["cause"]["detail"]["gate"] == GATE
    assert _staged_names(cfg) == ["One.flac"]


def test_the_engine_is_handed_the_fingerprint_of_the_bytes_the_gate_compared(
    cfg, silence, export, tmp_path, monkeypatch
):
    """Between the gate and the first move the file is read again, and the
    engine needs the fingerprint to compare that second read against."""
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])
    real = land_cli.landing.apply
    handed: list[str | None] = []

    def watched(planned, **kwargs):
        handed.append(kwargs.get("manifest_digest"))
        return real(planned, **kwargs)

    monkeypatch.setattr(land_cli.landing, "apply", watched)

    code, envelope = _drive(_answered(export, "--name", BATCH, "--manifest", str(manifest)))

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert handed == [hashlib.sha256(manifest.read_bytes()).hexdigest()]


def test_a_manifest_whose_only_row_matched_nothing_still_reports_it(cfg, silence, export, tmp_path):
    """Nothing filed is when the report matters most."""
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("2", "Probe", "Never Arrived", "Kompakt", 2024)])

    code, envelope = _drive(_answered(export, "--name", BATCH, "--manifest", str(manifest)))

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    data = envelope["data"]
    assert [item["action"] for item in data["items"]] == ["landed", "unfiled"]
    assert data["totals"] == {"count": 1, "landed": 1, "refused": 0, "filed": 0, "unfiled": 1}
    assert [warning["code"] for warning in envelope["warnings"]] == ["label-row-unmatched"]


@pytest.mark.parametrize("given", ["absent", "the list"])
def test_a_manifest_that_is_not_a_manifest_is_refused_before_the_gate(
    cfg, silence, export, tmp_path, given
):
    """A path with nothing at it, and the list the two file names invite passing
    in its place: refused before anybody answers a plan that could never run."""
    _stage(cfg, silence, "One.flac")
    path = tmp_path / "absent.manifest.json"
    if given == "the list":
        manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])
        path = manifest.with_name(manifest.name.replace(".manifest.json", ".list.json"))
        assert path.is_file()

    code, refused = _drive(_land(export, "--name", BATCH, "--manifest", str(path)))

    assert refused["cause"]["reason"] == "intake-list-unusable", refused
    assert given != "the list" or "not a manifest" in refused["cause"]["message"]
    assert code == int(ExitCode.PRECONDITION)
    assert _staged_names(cfg) == ["One.flac"]


# The engine's pre-move checks are asked before the gate (R-677)


def _assert_refused_before_the_gate(
    cfg: config.Config,
    code: int,
    envelope: dict,
    reason: str = "library-export-unusable",
    exit_code: ExitCode = ExitCode.PRECONDITION,
) -> None:
    """Refused with no gate offered, no run left to resume, and nothing moved."""
    assert envelope["cause"]["reason"] == reason, envelope
    assert code == int(exit_code)
    assert "gate" not in (envelope["cause"].get("detail") or {})
    assert envelope["outcome"] != "blocked"
    assert not gates.run_path(envelope["run_id"]).exists()
    assert _staged_names(cfg) == ["One.flac"]
    assert not _music(cfg, BATCH).exists()


def _spy_preflight(monkeypatch) -> list[dict]:
    """Every call the verb makes to the engine's preflight, by keyword."""
    asked: list[dict] = []
    real = landing.preflight

    def spied(plan, **kwargs):
        asked.append(kwargs)
        return real(plan, **kwargs)

    monkeypatch.setattr(landing, "preflight", spied)
    return asked


def _absent(tmp_path: Path) -> tuple[Path, str]:
    return tmp_path / "absent.xml", str(tmp_path / "absent.xml")


def _not_a_collection(tmp_path: Path) -> tuple[Path, str]:
    notes = tmp_path / "notes.xml"
    notes.write_bytes(b'<?xml version="1.0"?><NOTES>not a rekordbox export</NOTES>\n')
    return notes, "COLLECTION"


def _no_intake_folder(tmp_path: Path) -> tuple[Path, str]:
    """A collection the intake playlist cannot be written into, which only the
    engine's trial splice on a copy can see."""
    bare = tmp_path / "bare.xml"
    bare.write_bytes(_fresh_xml().replace(b'Name="INBOX"', b'Name="ELSEWHERE"'))
    return bare, "intake playlist"


@pytest.mark.parametrize("unusable", [_absent, _not_a_collection, _no_intake_folder])
def test_a_plan_over_an_unusable_export_refuses_before_the_gate(cfg, silence, tmp_path, unusable):
    """The eighth sitting's order among them, the verb run before the export was written."""
    _stage(cfg, silence, "One.flac")
    given, named = unusable(tmp_path)

    code, envelope = _drive(_land(given, "--name", BATCH))

    _assert_refused_before_the_gate(cfg, code, envelope)
    assert named in envelope["cause"]["message"]
    assert not _intake(cfg, BATCH).exists()


def test_an_unmounted_library_is_named_as_the_library_and_not_as_the_export(cfg, silence):
    """The engine asks the library before the export, and so does the plan read,
    so the person is sent to mount the drive, not to export again."""
    _stage(cfg, silence, "One.flac")
    root = Path(cfg.library.root)
    shutil.rmtree(root)

    code, envelope = _drive(_land(root / "export.xml", "--name", BATCH))

    _assert_refused_before_the_gate(
        cfg, code, envelope, "library-root-unreachable", ExitCode.LIBRARY_UNAVAILABLE
    )


def test_an_intake_file_already_there_refuses_before_the_gate(cfg, silence, export):
    """The engine never overwrites the intake file, so the plan read refuses too."""
    _stage(cfg, silence, "One.flac")
    _intake(cfg, BATCH).write_bytes(b"<DJ_PLAYLISTS/>")

    code, envelope = _drive(_land(export, "--name", BATCH))

    _assert_refused_before_the_gate(cfg, code, envelope, "output-exists")
    assert _intake(cfg, BATCH).read_bytes() == b"<DJ_PLAYLISTS/>"


def test_a_plan_over_a_usable_export_reaches_the_gate_with_the_digest_it_had_before(
    cfg, silence, export, monkeypatch
):
    """The check adds a refusal and nothing else: an answer recorded before the
    check existed is not made stale by it."""
    _stage(cfg, silence, "One.flac")
    asked = _spy_preflight(monkeypatch)
    code, refused = _drive(_land(export, "--name", BATCH))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE
    assert [call["export"] for call in asked] == [export]
    offered = gates.load(refused["run_id"]).offers[GATE]

    monkeypatch.setattr(landing, "preflight", lambda *args, **kwargs: None)
    code, without = _drive(_land(export, "--name", BATCH))
    assert code == int(ExitCode.DECISION_REQUIRED), without
    assert gates.load(without["run_id"]).offers[GATE] == offered


def test_the_plan_read_hands_the_engine_the_manifest_rows_the_gate_will_show(
    cfg, silence, export, tmp_path, monkeypatch
):
    """The label tree check is part of the engine's export check."""
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])
    asked = _spy_preflight(monkeypatch)

    code, refused = _drive(_land(export, "--name", BATCH, "--manifest", str(manifest)))

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert len(asked) == 1
    rows = asked[0]["label_rows"]
    assert [(row.provenance.label_name, row.provenance.year) for row in rows] == [("Kompakt", 2025)]


@pytest.mark.parametrize("gone", ["export", "library"])
def test_a_recorded_abort_is_honored_over_what_went_missing(cfg, silence, export, gone):
    """An answer given before the export or the library went bad is honoured as
    it was before the check existed (R-677), and the medium's read under the
    library root (R-746) must not refuse ahead of the gate either."""
    _stage(cfg, silence, "One.flac")
    run_id = _decided(export, "--name", BATCH, answer="abort")
    if gone == "export":
        export.unlink()
    else:
        shutil.rmtree(cfg.library.root)

    code, envelope = _drive(["--run", run_id, *_land(export, "--name", BATCH)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert _staged_names(cfg) == ["One.flac"]


def test_a_stale_answer_stays_stale_over_an_export_that_is_not_there(
    cfg, silence, export, tmp_path
):
    """Only the refusal that asks for an answer gives way to the preflight: the
    person is told the plan moved, not only that the new export is missing."""
    _stage(cfg, silence, "One.flac")
    run_id = _decided(export, "--name", BATCH)

    code, envelope = _drive(["--run", run_id, *_land(tmp_path / "absent.xml", "--name", BATCH)])

    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert _staged_names(cfg) == ["One.flac"]


def _watch_apply(monkeypatch, before=None, after=None) -> list[str]:
    """The engine's apply, run for real with ``before`` and ``after`` asked around it."""
    real = landing.apply
    seen: list[str] = []

    def watched(plan, **kwargs):
        seen.append(before() if before else "apply")
        landed = real(plan, **kwargs)
        if after:
            seen.append(after())
        return landed

    monkeypatch.setattr(landing, "apply", watched)
    return seen


def test_a_recorded_apply_over_an_export_that_went_missing_is_the_engine_s_refusal(
    cfg, silence, export, monkeypatch
):
    """An answered apply reaches the engine, which asks its own checks again."""
    _stage(cfg, silence, "One.flac")
    run_id = _decided(export, "--name", BATCH)
    export.unlink()
    reached = _watch_apply(monkeypatch)

    code, envelope = _drive(["--run", run_id, *_land(export, "--name", BATCH)])

    assert envelope["cause"]["reason"] == "library-export-unusable", envelope
    assert reached == ["apply"]
    assert _staged_names(cfg) == ["One.flac"]


# One landing per batch name (R-432)


def _assert_free(batch: str) -> None:
    with landing.batch_lock(batch):
        pass


def test_a_second_landing_under_a_held_batch_name_refuses_and_moves_nothing(cfg, silence, export):
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)

    with landing.batch_lock(BATCH) as held:
        code, envelope = _drive(_answered(export, "--name", BATCH))

    assert code == int(ExitCode.LIBRARY_BUSY), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "job-driver-held"
    assert cause["retryable"] is True
    assert cause["detail"]["batch"] == BATCH
    assert cause["detail"]["lock"] == str(held)
    assert len(cause["remediation"]["steps"]) == 2
    assert _staged_names(cfg) == ["One.flac", "Two.flac"]
    assert not _music(cfg, BATCH).exists()
    assert not _intake(cfg, BATCH).exists()
    assert session.records(cfg) == ()


def test_another_spelling_of_a_held_batch_folder_is_refused_and_the_plan_still_read(
    cfg, silence, export
):
    """A held name stops a second apply under any spelling, and nobody reading the plan."""
    _stage(cfg, silence, "One.flac")

    with landing.batch_lock(BATCH):
        code, envelope = _drive(_answered(export, "--name", BATCH.upper()))
        planned, refused = _drive(_land(export, "--name", BATCH))
        assert code == int(ExitCode.LIBRARY_BUSY), envelope
        assert _staged_names(cfg) == ["One.flac"]
        # A landing under another batch name lands while the one is held.
        landed, other = _drive(_answered(export, "--name", BATCH + "-second"))

    assert planned == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE
    assert landed == int(ExitCode.PENDING_HUMAN), other
    assert [p.name for p in _music(cfg, BATCH + "-second").iterdir()] == ["One.flac"]
    assert not _music(cfg, BATCH).exists()


def test_the_lock_is_held_for_the_whole_of_the_apply(cfg, silence, export, monkeypatch):
    """Asked from inside the engine call, before its first check and after its
    last write, so a lock taken late or dropped early is seen."""
    _stage(cfg, silence, "One.flac")

    def held_now() -> str:
        try:
            _assert_free(BATCH)
        except CratekitError as exc:
            return exc.cause.reason
        return "free"

    def written() -> str:
        assert _intake(cfg, BATCH).exists()
        return held_now()

    seen = _watch_apply(monkeypatch, before=held_now, after=written)

    code, envelope = _drive(_answered(export, "--name", BATCH))

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert seen == ["job-driver-held", "job-driver-held"]


def test_the_lock_is_released_after_a_landing(cfg, silence, export):
    _stage(cfg, silence, "One.flac")
    code, envelope = _drive(_answered(export, "--name", BATCH))
    assert code == int(ExitCode.PENDING_HUMAN), envelope

    _assert_free(BATCH)
    # A following landing under the name reaches the engine, which refuses it
    # over the intake file the first one left.
    _stage(cfg, silence, "Two.flac")
    code, envelope = _drive(_answered(export, "--name", BATCH))
    assert envelope["cause"]["reason"] == "output-exists", envelope
    assert _staged_names(cfg) == ["Two.flac"]


def _an_export_that_is_not_there(cfg, export) -> None:
    export.unlink()


def _an_intake_file_already_there(cfg, export) -> None:
    _intake(cfg, BATCH).write_bytes(b"<DJ_PLAYLISTS/>")


def _every_target_taken(cfg, export) -> None:
    _music(cfg, BATCH).mkdir(parents=True)
    (_music(cfg, BATCH) / "One.flac").write_bytes(b"already here")


@pytest.mark.parametrize(
    "arrange",
    [_an_export_that_is_not_there, _an_intake_file_already_there, _every_target_taken],
)
def test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after(
    cfg, silence, export, tmp_path, arrange
):
    _stage(cfg, silence, "One.flac")
    kept = tmp_path / "kept.xml"
    shutil.copyfile(export, kept)
    arrange(cfg, export)

    code, envelope = _drive(_answered(export, "--name", BATCH))

    assert code not in (int(ExitCode.OK), int(ExitCode.PENDING_HUMAN)), envelope
    assert envelope["cause"]["reason"] != "job-driver-held"
    assert _staged_names(cfg) == ["One.flac"]
    _assert_free(BATCH)

    # What refused it is put right, and the same name lands in the same process.
    shutil.copyfile(kept, export)
    _intake(cfg, BATCH).unlink(missing_ok=True)
    shutil.rmtree(_music(cfg, BATCH), ignore_errors=True)
    code, envelope = _drive(_answered(export, "--name", BATCH))
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert _staged_names(cfg) == []


def test_the_lock_is_released_when_the_engine_fails_with_no_refusal(
    cfg, silence, export, monkeypatch
):
    _stage(cfg, silence, "One.flac")

    def broken(plan, **kwargs):
        raise RuntimeError("the engine failed with no cause")

    with monkeypatch.context() as patched:
        patched.setattr(landing, "apply", broken)
        code, envelope = _drive(_answered(export, "--name", BATCH))
    assert code not in (int(ExitCode.OK), int(ExitCode.PENDING_HUMAN)), envelope

    _assert_free(BATCH)
    code, envelope = _drive(_answered(export, "--name", BATCH))
    assert code == int(ExitCode.PENDING_HUMAN), envelope


def test_a_lock_directory_this_account_cannot_write_refuses_by_name_and_moves_nothing(
    cfg, silence, export
):
    """The lock is taken before the first move, so a state directory that
    refuses leaves staging whole, named by path and permission."""
    _stage(cfg, silence, "One.flac")
    state = config.installation_state_dir()
    state.mkdir(parents=True, exist_ok=True)
    os.chmod(state, 0o500)
    try:
        code, envelope = _drive(_answered(export, "--name", BATCH))
    finally:
        os.chmod(state, 0o700)

    cause = envelope["cause"]
    assert cause["reason"] == "path-permission-denied", envelope
    assert cause["detail"]["path"].endswith("landing_locks")
    assert _staged_names(cfg) == ["One.flac"]
    assert not _music(cfg, BATCH).exists()


_HOLDER = """
import sys
from cratekit.intake import landing

with landing.batch_lock(sys.argv[1]):
    print("held", flush=True)
    sys.stdin.read()
"""


def test_a_landing_in_another_process_refuses_this_one_until_it_ends(cfg, silence, export):
    """The exclusion is between PROCESSES, and a holder that dies frees the name."""
    _stage(cfg, silence, "One.flac")
    holder = subprocess.Popen(
        [sys.executable, "-c", _HOLDER, BATCH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        assert holder.stdout.readline().strip() == "held"

        code, envelope = _drive(_answered(export, "--name", BATCH))

        assert code == int(ExitCode.LIBRARY_BUSY), envelope
        assert f"pid {holder.pid}" in envelope["cause"]["message"]
        assert _staged_names(cfg) == ["One.flac"]

        holder.kill()
        holder.wait(timeout=30)
        code, envelope = _drive(_answered(export, "--name", BATCH))
        assert code == int(ExitCode.PENDING_HUMAN), envelope
        assert _staged_names(cfg) == []
    finally:
        if holder.poll() is None:
            holder.kill()
            holder.wait(timeout=30)
        holder.stdin.close()
        holder.stdout.close()


def test_guide_names_the_verb_between_naming_and_routing():
    """The step sits after ``name apply`` and before ``route pending``."""
    text = GUIDE.read_text(encoding="utf-8")
    name = text.index("crate name apply --root")
    land = text.index("crate intake land", name)
    pending = text.index("crate route pending", land)
    assert name < land < pending
    assert f"`{GATE}`" in text
