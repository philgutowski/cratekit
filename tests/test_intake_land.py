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
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.acquire import listdoc
from cratekit.cli import output, registry
from cratekit.core import config, session, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import land_cli, landing
from tests._containers import synth_container
from tests.test_config import valid_data
from tests.xml_fixtures import _fresh_xml

GATE = "intake.land.confirm"
BATCH = "2026-09-18_favourites"
GUIDE = Path(__file__).resolve().parents[1] / "docs" / "GUIDE.md"


@pytest.fixture
def cfg(tmp_path: Path) -> config.Config:
    """A saved configuration the verb loads, with staging beside the library.

    The library root is whatever the autouse fixture set, whatever the dict
    names, so every path below is read back off the loaded value.
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


def _drive(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    document = json.loads(out.getvalue())
    assert output.envelope_problems(document) == [], document
    return code, document


def _land(export: Path, *extra: str) -> list[str]:
    return ["intake", "land", "--export", str(export), *extra]


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
    assert shown["intake file"] == str(Path(cfg.library.root) / f"{BATCH}_inboxed.xml")
    assert _staged_names(cfg) == ["One.flac", "Two.flac"]
    assert not _music(cfg, BATCH).exists()
    assert not (Path(cfg.library.root) / f"{BATCH}_inboxed.xml").exists()


def test_the_gate_screen_a_person_reads_names_the_files_and_the_intake_file(
    cfg, silence, export
):
    """The plan payload never reaches a person reading the default output, so
    the files have to be on the gate screen or the answer is to a bare question."""
    _stage(cfg, silence, "One.flac")
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(_land(export, "--name", BATCH), stdout=out, stderr=err)

    assert code == int(ExitCode.DECISION_REQUIRED)
    screen = err.getvalue()
    assert "One.flac" in screen
    assert f"{BATCH}_inboxed.xml" in screen
    assert str(_music(cfg, BATCH)) in screen
    assert "crate run decide" in screen and GATE in screen


def test_an_answered_run_lands_the_batch_and_names_the_xml_in_human_output(
    cfg, silence, export
):
    """R34's two acts, then the landing, read the way a person reads it."""
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    code, refused = _drive(_land(export, "--name", BATCH))
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = refused["run_id"]
    decided, _ = _drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)

    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--run", run_id, *_land(export, "--name", BATCH)], stdout=out, stderr=err)

    destination = Path(cfg.library.root) / f"{BATCH}_inboxed.xml"
    assert code == int(ExitCode.PENDING_HUMAN), err.getvalue()
    human = out.getvalue() + err.getvalue()
    assert str(destination) in human
    assert "verify: intake.imported" in human
    assert "blocks:" not in human
    assert sorted(p.name for p in _music(cfg, BATCH).iterdir()) == ["One.flac", "Two.flac"]
    assert _staged_names(cfg) == []
    body = destination.read_bytes()
    assert b'<COLLECTION Entries="2">' in body
    assert b"<TEMPO" not in body


def test_the_landed_envelope_carries_an_import_that_blocks_nothing(cfg, silence, export):
    """The pending action is state, not advice, and the state is the intake
    session's: the envelope carries the action that record holds, read back, so
    the two cannot differ (R-501, sweep finding 117.2). ``blocks`` stays empty
    because a blocking action makes every verb it names refuse, and no cost of an
    unimported landing was driven to justify that."""
    _stage(cfg, silence, "One.flac")
    code, envelope = _drive(["-d", f"{GATE}=apply", *_land(export, "--name", BATCH)])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["outcome"] == "pending"
    pending = envelope["pending_human_action"]
    assert pending["kind"] == "rekordbox_import"
    assert pending["artifact"] == str(Path(cfg.library.root) / f"{BATCH}_inboxed.xml")
    assert pending["verify_verb"] == "intake.imported"
    assert pending["verify_verb"] in registry.VERB_NAMES
    assert pending["blocks"] == []
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.AWAITING_IMPORT
    assert record.pending is not None
    assert record.pending.to_json() == pending
    data = envelope["data"]
    assert [item["action"] for item in data["items"]] == ["landed"]
    assert data["totals"] == {"count": 1, "landed": 1, "refused": 0}


def test_a_stale_answer_is_refused_and_moves_nothing(cfg, silence, export):
    _stage(cfg, silence, "One.flac")
    code, refused = _drive(_land(export, "--name", BATCH))
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = refused["run_id"]
    _drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    _stage(cfg, silence, "Arrived.flac")

    code, envelope = _drive(["--run", run_id, *_land(export, "--name", BATCH)])

    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert code != int(ExitCode.OK)
    assert _staged_names(cfg) == ["Arrived.flac", "One.flac"]
    assert not _music(cfg, BATCH).exists()


def test_an_answer_given_for_one_batch_name_is_stale_for_another(cfg, silence, export):
    """The digest covers where the files go, not only which files move. The
    same folder under a second name is a plan the person never saw."""
    _stage(cfg, silence, "One.flac")
    code, refused = _drive(_land(export, "--name", BATCH))
    run_id = refused["run_id"]
    _drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])

    code, envelope = _drive(["--run", run_id, *_land(export, "--name", "elsewhere")])

    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert _staged_names(cfg) == ["One.flac"]
    assert not _music(cfg, "elsewhere").exists()


def test_an_answer_given_against_one_export_is_stale_for_another(
    cfg, silence, export, tmp_path
):
    """The export is what the batch is spliced into, so it is part of the plan."""
    _stage(cfg, silence, "One.flac")
    code, refused = _drive(_land(export, "--name", BATCH))
    run_id = refused["run_id"]
    _drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    other = tmp_path / "other.xml"
    other.write_bytes(export.read_bytes())

    code, envelope = _drive(["--run", run_id, *_land(other, "--name", BATCH)])

    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert _staged_names(cfg) == ["One.flac"]


def test_an_answer_given_for_one_folder_is_stale_for_another_holding_the_same_names(
    cfg, silence, export
):
    """The file fingerprint is names, sizes and times. Two folders can match on
    all three, so the folder itself is in the digest."""
    _stage(cfg, silence, "One.flac")
    twin = _staging(cfg) / "twin"
    twin.mkdir()
    staged = _staging(cfg) / "One.flac"
    shutil.copy2(staged, twin / "One.flac")
    code, refused = _drive(_land(export, "--name", BATCH))
    run_id = refused["run_id"]
    _drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])

    code, envelope = _drive(["--run", run_id, *_land(export, str(twin), "--name", BATCH)])

    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert (twin / "One.flac").is_file()
    assert not _music(cfg, BATCH).exists()


def test_staging_holding_only_lists_and_dotfiles_is_a_plan_of_nothing(cfg, export):
    """What staging holds between landings: the lists folder ``intake missing``
    writes, the unfinished download directory, a Finder dotfile and a sync's
    intake file. None of it is audio, so there is nothing to land."""
    staging = _staging(cfg)
    (staging / "lists").mkdir()
    (staging / ".cratekit-acquire-staging").mkdir()
    (staging / ".DS_Store").write_bytes(b"\0")
    (staging / "run_synced.xml").write_bytes(b"<DJ_PLAYLISTS/>")

    code, envelope = _drive(["-d", f"{GATE}=apply", *_land(export, "--name", BATCH)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["items"] == []


def test_an_abort_is_no_op_and_moves_nothing(cfg, silence, export):
    _stage(cfg, silence, "One.flac")
    code, envelope = _drive(["-d", f"{GATE}=abort", *_land(export, "--name", BATCH)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["pending_human_action"] is None
    assert [item["action"] for item in envelope["data"]["items"]] == ["land"]
    assert _staged_names(cfg) == ["One.flac"]
    assert not _music(cfg, BATCH).exists()


def test_the_folder_defaults_to_staging_and_the_name_to_the_run(cfg, silence, export):
    _stage(cfg, silence, "One.flac")
    code, envelope = _drive(["-d", f"{GATE}=apply", *_land(export)])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    batch = land_cli.default_name(envelope["run_id"])
    assert ":" not in batch
    assert batch == envelope["run_id"].replace(":", "")
    assert (_music(cfg, batch) / "One.flac").is_file()
    assert envelope["pending_human_action"]["artifact"] == str(
        Path(cfg.library.root) / f"{batch}_inboxed.xml"
    )


def test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing(cfg, export):
    """Staging is empty on a fresh install and after every landing. The step
    still asks, and applying nothing makes no batch folder, no intake file and
    no pending import."""
    code, refused = _drive(_land(export, "--name", BATCH))
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["files"] == []

    code, envelope = _drive(["-d", f"{GATE}=apply", *_land(export, "--name", BATCH)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["pending_human_action"] is None
    assert envelope["data"]["items"] == []
    assert not _music(cfg, BATCH).exists()
    assert not (Path(cfg.library.root) / f"{BATCH}_inboxed.xml").exists()


def test_a_folder_that_is_not_there_is_refused_before_the_gate(cfg, export, tmp_path):
    code, envelope = _drive(_land(export, str(tmp_path / "absent"), "--name", BATCH))

    assert envelope["cause"]["reason"] == "intake-list-unusable", envelope
    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED))


def test_a_refused_file_is_a_warning_a_person_reads(cfg, silence, export):
    for name in ("Keep.flac", "Clash.flac"):
        _stage(cfg, silence, name)
    occupied = _music(cfg, BATCH)
    occupied.mkdir(parents=True)
    (occupied / "Clash.flac").write_bytes(b"the copy somebody kept")

    out, err = io.StringIO(), io.StringIO()
    code = cli.run(
        ["-d", f"{GATE}=apply", *_land(export, "--name", BATCH)], stdout=out, stderr=err
    )

    assert code == int(ExitCode.PENDING_HUMAN)
    human = out.getvalue() + err.getvalue()
    assert re.search(r"warning \[output-exists\]: .*Clash\.flac", human), human
    assert (occupied / "Clash.flac").read_bytes() == b"the copy somebody kept"
    assert _staged_names(cfg) == ["Clash.flac"]


def test_the_refused_item_is_marked_in_the_plan_payload(cfg, silence, export):
    for name in ("Keep.flac", "Clash.flac"):
        _stage(cfg, silence, name)
    occupied = _music(cfg, BATCH)
    occupied.mkdir(parents=True)
    (occupied / "Clash.flac").write_bytes(b"kept")

    code, envelope = _drive(["-d", f"{GATE}=apply", *_land(export, "--name", BATCH)])

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
    # The label playlists are in the items and the totals above. The pending
    # action is the one the intake session persisted before any label was
    # filed, so its summary names the file and not what was filed into it.
    assert f"{BATCH}_inboxed.xml" in envelope["pending_human_action"]["summary"]
    body = (Path(cfg.library.root) / f"{BATCH}_inboxed.xml").read_bytes()
    assert b'<NODE Name="Kompakt 2025" Type="1" KeyType="0" Entries="1">' in body


def test_a_landing_without_a_manifest_reports_nothing_about_labels(cfg, silence, export):
    _stage(cfg, silence, "One.flac")
    code, envelope = _drive(["-d", f"{GATE}=apply", *_land(export, "--name", BATCH)])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["data"]["totals"] == {"count": 1, "landed": 1, "refused": 0}
    assert "label playlist" not in envelope["pending_human_action"]["summary"]


def test_an_answer_given_against_one_manifest_is_stale_once_it_is_rewritten(
    cfg, silence, export, tmp_path
):
    """The same path holding other rows files other tracks under other labels,
    so the bytes are what the gate compares and not the name."""
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])
    argv = _land(export, "--name", BATCH, "--manifest", str(manifest))
    code, refused = _drive(argv)
    run_id = refused["run_id"]
    decided, _ = _drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)

    manifest.write_bytes(manifest.read_bytes().replace(b"Kompakt", b"Another"))
    code, stale = _drive(["--run", run_id, *argv])

    assert stale["cause"]["reason"] == "decision-stale", stale
    # THE GATE'S refusal and not the engine's, which carries the same reason
    # one layer down. Each is removed alone in the mutation table, and a test
    # that either one satisfies is a test of neither.
    assert stale["cause"]["detail"]["gate"] == GATE
    assert _staged_names(cfg) == ["One.flac"]


def test_the_engine_is_handed_the_fingerprint_of_the_bytes_the_gate_compared(
    cfg, silence, export, tmp_path, monkeypatch
):
    """Between the gate and the first move the file is read again. Without the
    fingerprint the engine has nothing to compare that second read against."""
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])
    real = land_cli.landing.apply
    handed: list[str | None] = []

    def watched(planned, **kwargs):
        handed.append(kwargs.get("manifest_digest"))
        return real(planned, **kwargs)

    monkeypatch.setattr(land_cli.landing, "apply", watched)

    code, envelope = _drive(
        ["-d", f"{GATE}=apply", *_land(export, "--name", BATCH, "--manifest", str(manifest))]
    )

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert handed == [hashlib.sha256(manifest.read_bytes()).hexdigest()]


def test_a_manifest_whose_only_row_matched_nothing_still_reports_it(
    cfg, silence, export, tmp_path
):
    """Nothing filed is when the report matters most."""
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("2", "Probe", "Never Arrived", "Kompakt", 2024)])

    code, envelope = _drive(
        ["-d", f"{GATE}=apply", *_land(export, "--name", BATCH, "--manifest", str(manifest))]
    )

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    data = envelope["data"]
    assert [item["action"] for item in data["items"]] == ["landed", "unfiled"]
    assert data["totals"] == {"count": 1, "landed": 1, "refused": 0, "filed": 0, "unfiled": 1}
    assert [warning["code"] for warning in envelope["warnings"]] == ["label-row-unmatched"]


def test_a_manifest_that_is_not_there_is_refused_before_the_gate(
    cfg, silence, export, tmp_path
):
    _stage(cfg, silence, "One.flac")
    code, refused = _drive(
        _land(export, "--name", BATCH, "--manifest", str(tmp_path / "absent.manifest.json"))
    )

    assert refused["cause"]["reason"] == "intake-list-unusable", refused
    assert code == int(ExitCode.PRECONDITION)
    assert _staged_names(cfg) == ["One.flac"]


def test_the_list_passed_where_the_manifest_belongs_is_refused_before_the_gate(
    cfg, silence, export, tmp_path
):
    """The mistake the two file names invite. Refused before anybody spends an
    answer on a plan that could never run."""
    _stage(cfg, silence, "One.flac")
    manifest = _manifest(tmp_path, [("1", "Probe", "One", "Kompakt", 2025)])
    listed = manifest.with_name(manifest.name.replace(".manifest.json", ".list.json"))
    assert listed.is_file()

    code, refused = _drive(_land(export, "--name", BATCH, "--manifest", str(listed)))

    assert refused["cause"]["reason"] == "intake-list-unusable", refused
    assert "not a manifest" in refused["cause"]["message"]
    assert code == int(ExitCode.PRECONDITION)
    assert _staged_names(cfg) == ["One.flac"]


# ---------------------------------------------------------------------------
# One landing per batch name (R-432)
# ---------------------------------------------------------------------------


def _answered(export: Path, *extra: str) -> list[str]:
    return ["-d", f"{GATE}=apply", *_land(export, *extra)]


def _intake(cfg: config.Config, batch: str) -> Path:
    return Path(cfg.library.root) / f"{batch}_inboxed.xml"


def _assert_free(batch: str) -> None:
    with landing.batch_lock(batch):
        pass


def test_a_second_landing_under_a_held_batch_name_refuses_and_moves_nothing(
    cfg, silence, export
):
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)

    with landing.batch_lock(BATCH) as held:
        code, envelope = _drive(_answered(export, "--name", BATCH))

    assert code == int(ExitCode.LIBRARY_BUSY), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "job-driver-held"
    assert cause["retryable"] is True
    assert cause["detail"] == {"batch": BATCH, "lock": str(held)}
    assert _staged_names(cfg) == ["One.flac", "Two.flac"]
    assert not _music(cfg, BATCH).exists()
    assert not _intake(cfg, BATCH).exists()
    assert session.records(cfg) == ()


def test_another_spelling_of_a_held_batch_folder_is_refused(cfg, silence, export):
    _stage(cfg, silence, "One.flac")

    with landing.batch_lock(BATCH):
        code, envelope = _drive(_answered(export, "--name", BATCH.upper()))

    assert code == int(ExitCode.LIBRARY_BUSY), envelope
    assert _staged_names(cfg) == ["One.flac"]


def test_a_held_batch_name_does_not_stop_anybody_reading_the_plan(cfg, silence, export):
    _stage(cfg, silence, "One.flac")

    with landing.batch_lock(BATCH):
        code, refused = _drive(_land(export, "--name", BATCH))

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE


def test_the_lock_is_held_for_the_whole_of_the_apply(cfg, silence, export, monkeypatch):
    """Asked from inside the engine call, before its first check and after its
    last write, so a lock taken late or dropped early is seen."""
    _stage(cfg, silence, "One.flac")
    real = landing.apply
    seen: list[str] = []

    def held_now() -> str:
        try:
            _assert_free(BATCH)
        except CratekitError as exc:
            return exc.cause.reason
        return "free"

    def watched(plan, **kwargs):
        seen.append(held_now())
        landed = real(plan, **kwargs)
        assert _intake(cfg, BATCH).exists()
        seen.append(held_now())
        return landed

    monkeypatch.setattr(landing, "apply", watched)

    code, envelope = _drive(_answered(export, "--name", BATCH))

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert seen == ["job-driver-held", "job-driver-held"]


def test_the_lock_is_released_after_a_landing(cfg, silence, export):
    _stage(cfg, silence, "One.flac")
    code, envelope = _drive(_answered(export, "--name", BATCH))
    assert code == int(ExitCode.PENDING_HUMAN), envelope

    _assert_free(BATCH)
    # And a following landing under the name reaches the engine, which is what
    # refuses it now, over the intake file the first one left.
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


def test_a_landing_under_another_batch_name_lands_while_one_is_held(cfg, silence, export):
    _stage(cfg, silence, "One.flac")

    with landing.batch_lock(BATCH):
        code, envelope = _drive(_answered(export, "--name", BATCH + "-second"))

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert [p.name for p in _music(cfg, BATCH + "-second").iterdir()] == ["One.flac"]
    assert not _music(cfg, BATCH).exists()


_HOLDER = """
import sys
from cratekit.intake import landing

with landing.batch_lock(sys.argv[1]):
    print("held", flush=True)
    sys.stdin.read()
"""


def test_a_landing_in_another_process_refuses_this_one_until_it_ends(cfg, silence, export):
    """The exclusion is between PROCESSES, which no test holding the lock in
    this one shows, and a holder that dies frees the name with no clean up."""
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
        assert f"pid {holder.pid}" in envelope["cause"]["inner"]["message"]
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
    """The acquisition walkthrough never said how a download reaches an intake
    file. The step sits after ``name apply`` and before ``route pending``."""
    text = GUIDE.read_text(encoding="utf-8")
    name = text.index("crate name apply --root")
    land = text.index("crate intake land", name)
    pending = text.index("crate route pending", land)
    assert name < land < pending
    assert f"`{GATE}`" in text
