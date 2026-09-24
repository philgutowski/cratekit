"""R-501: a landed batch can be followed to a library the cutover precheck passes.

Every landing left an ``open`` intake session and an intake file at the library
root. Each refused ``tree_registry.assert_cutover_ready`` and no shipped verb
cleared either. These tests drive the whole path through the real command line:
land, do what the pending action says, and ask the precheck.

THE IMPORT IS SIMULATED BY THE ONE THING IT CHANGES. rekordbox importing an
intake file makes collection rows for the tracks it names, and a Fresh Export
taken afterwards names them. The intake file's own bytes, under a name that is
not an intake file's, are exactly that export, so that is what stands in for it.
"""

from __future__ import annotations

import io
import json
import re
import shutil
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output, registry
from cratekit.core import config, preflight, session, snapshot, tags, tree_registry
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import collection_xml, imported_cli, ingest, land_cli, pipeline
from cratekit.sync import mark_cli
from cratekit.write import routing_cli, routing_pass
from tests._containers import synth_container
from tests.cli_drive import drive_human
from tests.test_config import valid_data
from tests.xml_fixtures import _fresh_xml

GATE = "intake.land.confirm"
BATCH = "2026-09-19_batch"


@pytest.fixture
def cfg(tmp_path: Path) -> config.Config:
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


def _stage(cfg: config.Config, silence: Path, name: str, *, genre: str = "Deep House") -> Path:
    path = Path(cfg.paths.download_staging) / name
    shutil.copyfile(silence, path)
    assert tags.write_tags(
        path, {"title": Path(name).stem, "artist": "Probe", "genre": genre, "energylevel": 7}
    )
    return path


def _drive(argv: list[str]) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    document = json.loads(out.getvalue())
    assert output.envelope_problems(document) == [], document
    return code, document


def _land(cfg: config.Config, silence: Path, export: Path, *names: str, batch: str = BATCH) -> dict:
    for name in names or ("One.flac",):
        _stage(cfg, silence, name)
    code, envelope = _drive(
        ["-d", f"{GATE}=apply", "intake", "land", "--export", str(export), "--name", batch]
    )
    assert code == int(ExitCode.PENDING_HUMAN), envelope
    return envelope


def _intake_file(cfg: config.Config, batch: str = BATCH) -> Path:
    return Path(cfg.library.root) / f"{batch}_inboxed.xml"


def _export_after_import(tmp_path: Path, intake_file: Path, name: str = "after-import.xml") -> Path:
    """What rekordbox exports once the intake file is imported. See the module docstring."""
    path = tmp_path / name
    path.write_bytes(intake_file.read_bytes())
    return path


def _verified_snapshot(cfg: config.Config) -> None:
    capture = snapshot.store_root(cfg) / "2026-09-19T000000Z-deadbeefcafebabe"
    capture.mkdir(parents=True)
    record = snapshot.Capture(
        stamp=capture.name, root=capture, database=capture / "master.db", integrity_verified=True
    )
    (capture / snapshot.MANIFEST_NAME).write_text(
        json.dumps(record.to_json()) + "\n", encoding="utf-8"
    )


def _refusal(cfg: config.Config, export: Path) -> CratekitError:
    with pytest.raises(CratekitError) as caught:
        tree_registry.assert_cutover_ready(cfg, export=export)
    return caught.value


# ── The brief's first scenario: follow every step, and the precheck passes ──


def test_a_landing_followed_step_by_step_passes_the_cutover_precheck(
    cfg, silence, export, tmp_path
):
    """Land, do what the pending action names and nothing else, ask the precheck.

    NO HAND DELETION ANYWHERE, which is the whole finding. Before R-501 this
    library refused ``cutover-open-run``, and with the record forced terminal it
    refused ``cutover-xml-pending`` until somebody deleted the intake file.
    """
    _verified_snapshot(cfg)
    envelope = _land(cfg, silence, export, "One.flac", "Two.flac")
    pending = envelope["pending_human_action"]
    intake_file = Path(pending["artifact"])
    assert intake_file == _intake_file(cfg)

    # The landing alone leaves a library the precheck refuses, and the refusal
    # carries the run's own steps, which name the verb that clears it.
    refusal = _refusal(cfg, export).cause
    assert refusal.reason == "cutover-open-run"
    assert list(refusal.remediation.steps) == pending["steps"]

    # The steps, in order: import, take a Fresh Export, run the verify verb.
    assert pending["verify_verb"] == "intake.imported"
    assert pending["verify_verb"] in registry.VERB_NAMES
    assert str(intake_file) in pending["steps"][0]
    assert "Fresh Export" in pending["steps"][1]
    assert "crate intake imported --export" in pending["steps"][2]
    after = _export_after_import(tmp_path, intake_file)
    code, result = _drive(["intake", "imported", "--export", str(after)])

    assert code == int(ExitCode.OK), result
    (item,) = result["data"]["items"]
    assert item["action"] == imported_cli.IMPORTED
    assert item["count"] == 2
    assert not intake_file.exists()
    assert Path(item["retired_to"]).read_bytes() == after.read_bytes()
    assert tree_registry.pending_intake_xml(cfg) == ()
    tree_registry.assert_cutover_ready(cfg, export=after)


def test_a_verified_run_stays_open_with_its_placements_still_owed(cfg, silence, export, tmp_path):
    """The run is NOT closed before a cutover, and the record says why it may wait.

    The gated close refuses a run holding a deferred placement, and only a
    database native tree can place one. So the run is left open, holding no
    capture, with the proof recorded, and its intents are still outstanding for
    the pass that runs after the cutover.
    """
    _land(cfg, silence, export)
    after = _export_after_import(tmp_path, _intake_file(cfg))
    _, result = _drive(["intake", "imported", "--export", str(after)])

    (record,) = session.records(cfg)
    assert result["data"]["items"][0]["closed"] is False
    assert record.state is session.SessionState.OPEN
    assert record.pending is None
    assert session.owes_only_deferred_routing(record)
    proof = record.detail[session.IMPORT_VERIFIED_KEY]
    assert proof["evidence"] == "fresh export after-import.xml"
    assert proof["artifact"] == str(_intake_file(cfg))
    assert len(routing_pass.read(cfg).outstanding(record.session_id)) == 1


# ── What is not proof ───────────────────────────────────────────────────────


def test_an_export_taken_before_the_import_proves_nothing_and_changes_nothing(
    cfg, silence, export
):
    """The export the batch was spliced into names none of the landed files."""
    envelope = _land(cfg, silence, export, "One.flac", "Two.flac")

    code, result = _drive(["intake", "imported", "--export", str(export)])

    assert code == int(ExitCode.PENDING_HUMAN), result
    (item,) = result["data"]["items"]
    assert item["action"] == imported_cli.NOT_IMPORTED
    assert (item["count"], item["missing"]) == (2, 2)
    assert len(item["missing_locations"]) == 2
    assert result["pending_human_action"] == envelope["pending_human_action"]
    assert _intake_file(cfg).is_file()
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.AWAITING_IMPORT
    assert _refusal(cfg, export).cause.reason == "cutover-open-run"


def test_a_partly_imported_batch_is_not_imported(cfg, silence, export, tmp_path):
    """One landed track missing from the export is a batch that did not import."""
    _land(cfg, silence, export, "One.flac", "Two.flac")
    body = _intake_file(cfg).read_bytes()
    without_two = re.sub(rb"[ \t]*<TRACK [^>]*Two\.flac[^>]*>.*?</TRACK>\r?\n", b"", body, flags=re.S)
    assert body.count(b"<TRACK ") - without_two.count(b"<TRACK ") == 1
    assert b"One.flac" in without_two
    partial = tmp_path / "partial.xml"
    partial.write_bytes(without_two)

    code, result = _drive(["intake", "imported", "--export", str(partial)])

    assert code == int(ExitCode.PENDING_HUMAN), result
    (item,) = result["data"]["items"]
    assert (item["action"], item["missing"]) == (imported_cli.NOT_IMPORTED, 1)
    assert "Two.flac" in item["missing_locations"][0]
    assert _intake_file(cfg).is_file()


def test_the_intake_file_is_refused_as_its_own_proof(cfg, silence, export, tmp_path):
    """It names every landed track whether or not anybody imported it."""
    _land(cfg, silence, export)
    intake_file = _intake_file(cfg)

    code, by_name = _drive(["intake", "imported", "--export", str(intake_file)])
    assert by_name["cause"]["reason"] == "library-export-unusable", by_name
    assert code != int(ExitCode.OK)

    # The same file reached by a name that is not an intake file's.
    link = tmp_path / "looks-fresh.xml"
    link.symlink_to(intake_file)
    code, by_link = _drive(["intake", "imported", "--export", str(link)])
    assert by_link["cause"]["reason"] == "library-export-unusable", by_link
    assert "waiting on" in by_link["cause"]["message"]

    assert intake_file.is_file()
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.AWAITING_IMPORT


def test_a_stub_listing_is_refused_as_the_export(cfg, silence, export, tmp_path):
    _land(cfg, silence, export)
    stub = tmp_path / "listing.xml"
    stub.write_bytes(
        b'<?xml version="1.0" encoding="UTF-8"?>\n<DJ_PLAYLISTS Version="1.0.0">\n'
        b'  <COLLECTION Entries="1">\n    <TRACK Name="Probe - One"/>\n  </COLLECTION>\n'
        b"</DJ_PLAYLISTS>\n"
    )
    assert collection_xml.is_stub_listing(stub.read_bytes())

    _, result = _drive(["intake", "imported", "--export", str(stub)])

    assert result["cause"]["reason"] == "intake-export-is-stub", result
    assert _intake_file(cfg).is_file()


def test_a_run_the_ledger_names_no_file_for_is_left_alone(cfg, silence, export, tmp_path):
    """Nothing recorded is not nothing owed: no Location, so no export is proof."""
    _land(cfg, silence, export)
    after = _export_after_import(tmp_path, _intake_file(cfg))
    routing_pass.write(cfg, routing_pass.EMPTY)

    code, result = _drive(["intake", "imported", "--export", str(after)])

    assert code == int(ExitCode.PENDING_HUMAN), result
    assert result["data"]["items"][0]["action"] == imported_cli.UNVERIFIABLE
    assert _intake_file(cfg).is_file()
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.AWAITING_IMPORT


# ── The verb's own edges ────────────────────────────────────────────────────


def test_nothing_waiting_is_a_no_op_with_or_without_an_export(cfg, export):
    for argv in (["intake", "imported"], ["intake", "imported", "--export", str(export)]):
        code, result = _drive(argv)

        assert code == int(ExitCode.OK), result
        assert result["outcome"] == "no_op"
        assert result["data"]["items"] == []


def test_an_export_that_is_not_there_is_refused_even_with_nothing_waiting(cfg, tmp_path):
    """A mistyped path answered "nothing to do", which reads as "checked"."""
    code, result = _drive(["intake", "imported", "--export", str(tmp_path / "typo.xml")])

    assert result["cause"]["reason"] == "library-export-unusable", result
    assert code != int(ExitCode.OK)


def test_a_waiting_run_with_no_export_named_is_refused_and_says_what_to_pass(
    cfg, silence, export
):
    _land(cfg, silence, export)
    (record,) = session.records(cfg)

    _, result = _drive(["intake", "imported"])

    assert result["cause"]["reason"] == "library-export-unusable", result
    assert result["cause"]["detail"]["sessions"] == [record.session_id]
    assert _intake_file(cfg).is_file()


def test_a_named_run_that_is_not_waiting_is_refused(cfg, silence, export):
    _land(cfg, silence, export)

    _, result = _drive(["intake", "imported", "--export", str(export), "--session", "no-such"])

    assert result["cause"]["reason"] == "intake-list-unusable", result


def test_two_waiting_runs_are_settled_independently(cfg, silence, export, tmp_path):
    """The export proves the first batch and not the second, and says so per run."""
    _land(cfg, silence, export, "One.flac", batch="first")
    after_first = _export_after_import(tmp_path, _intake_file(cfg, "first"))
    _land(cfg, silence, export, "Two.flac", batch="second")

    code, result = _drive(["intake", "imported", "--export", str(after_first)])

    assert code == int(ExitCode.PENDING_HUMAN), result
    actions = {Path(item["intake_file"]).name: item["action"] for item in result["data"]["items"]}
    assert actions == {
        "first_inboxed.xml": imported_cli.IMPORTED,
        "second_inboxed.xml": imported_cli.NOT_IMPORTED,
    }
    assert not _intake_file(cfg, "first").exists()
    assert _intake_file(cfg, "second").is_file()
    assert result["pending_human_action"]["artifact"] == str(_intake_file(cfg, "second"))


def test_retiring_never_lands_on_another_file(tmp_path):
    """A batch name is free again once its file is retired, so the name can repeat."""
    first = tmp_path / "again_inboxed.xml"
    first.write_bytes(b"first")
    assert imported_cli.retire(first) == tmp_path / "again_inboxed.xml.imported"
    second = tmp_path / "again_inboxed.xml"
    second.write_bytes(b"second")

    assert imported_cli.retire(second) == tmp_path / "again_inboxed.xml.imported-2"
    assert (tmp_path / "again_inboxed.xml.imported").read_bytes() == b"first"
    assert (tmp_path / "again_inboxed.xml.imported-2").read_bytes() == b"second"


def test_retiring_renames_only_a_plain_file_this_product_named(tmp_path):
    """The path comes off a record on disk, so the name and the kind are checked."""
    stranger = tmp_path / "collection.xml"
    stranger.write_bytes(b"not ours")
    with pytest.raises(CratekitError) as caught:
        imported_cli.retire(stranger)
    assert caught.value.cause.reason == "internal-error"
    assert stranger.read_bytes() == b"not ours"

    target = tmp_path / "real.xml"
    target.write_bytes(b"real")
    link = tmp_path / "linked_inboxed.xml"
    link.symlink_to(target)
    assert imported_cli.retire(link) is None
    assert link.is_symlink() and target.read_bytes() == b"real"
    assert imported_cli.retire(tmp_path / "absent_inboxed.xml") is None


# ── The brief's second scenario: a refused call leaves no open record ───────


def test_a_refusal_before_the_write_leaves_no_session_at_all(cfg, silence, export):
    """The session opens after the last refusal that needs none."""
    music = Path(cfg.library.root) / cfg.library.music_dir
    music.mkdir(parents=True, exist_ok=True)
    path = music / "One.flac"
    shutil.copyfile(silence, path)
    no_intake_folder = export.with_name("no-intake.xml")
    no_intake_folder.write_bytes(
        b'<?xml version="1.0" encoding="UTF-8"?>\n<DJ_PLAYLISTS Version="1.0.0">\n'
        b'  <COLLECTION Entries="0">\n  </COLLECTION>\n  <PLAYLISTS>\n'
        b'    <NODE Type="0" Name="ROOT" Count="0">\n    </NODE>\n  </PLAYLISTS>\n'
        b"</DJ_PLAYLISTS>\n"
    )

    with pytest.raises(CratekitError) as caught:
        ingest.place_files(
            [path], cfg=cfg, export=no_intake_folder, destination=music / "x_inboxed.xml"
        )

    assert caught.value.cause.reason == "library-export-unusable"
    assert session.records(cfg) == ()


def test_a_refusal_after_the_session_opens_abandons_it_and_removes_the_file(
    cfg, silence, export, monkeypatch
):
    """The ledger refusing arrives after the write, which is the reachable case."""
    music = Path(cfg.library.root) / cfg.library.music_dir
    music.mkdir(parents=True, exist_ok=True)
    path = music / "One.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": "One", "genre": "Deep House", "energylevel": 7})
    destination = Path(cfg.library.root) / "refused_inboxed.xml"

    def refusing(*args, **kwargs):
        raise refuse("internal-error", "the ledger could not be written")

    monkeypatch.setattr(routing_pass, "record_intents", refusing)
    with pytest.raises(CratekitError):
        ingest.place_files([path], cfg=cfg, export=export, destination=destination)

    (record,) = session.records(cfg)
    assert record.state is session.SessionState.ABANDONED
    assert record.terminal
    assert not destination.exists()
    assert tree_registry.pending_intake_xml(cfg) == ()


def test_a_placed_call_ends_awaiting_import_with_the_action_persisted(cfg, silence, export):
    music = Path(cfg.library.root) / cfg.library.music_dir
    music.mkdir(parents=True, exist_ok=True)
    path = music / "One.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": "One", "genre": "Deep House", "energylevel": 7})
    destination = Path(cfg.library.root) / "placed_inboxed.xml"

    placed = ingest.place_files([path], cfg=cfg, export=export, destination=destination)

    (record,) = session.records(cfg)
    assert [item.session_id for item in placed] == [record.session_id]
    assert record.state is session.SessionState.AWAITING_IMPORT
    assert record.pending is not None
    assert record.pending.artifact == str(destination)
    assert record.pending.verify_verb == ingest.VERIFY_VERB == "intake.imported"
    # Spelled out, because an expected value read off ``ingest.import_steps``
    # would only say the function returns what it returns.
    first, second, third = record.pending.steps
    assert first == f"import {destination} into rekordbox as a rekordbox xml library"
    assert second == "take a Fresh Export of the collection from rekordbox"
    assert third.startswith("run crate intake imported --export with that Fresh Export")
    assert ingest.persisted_pending(cfg, placed) == record.pending


# ── The brief's third scenario: route pending before a cutover ──────────────


def test_route_pending_with_no_native_tree_is_a_no_op_that_says_so(cfg, silence, export):
    """It answered OK over a run it had not opened. THE CLOSING MOVED to
    ``intake imported``, which the tests above drive, and this verb now claims
    nothing: a no-op, a warning naming why, and the run exactly as it was."""
    _land(cfg, silence, export)
    (before,) = session.records(cfg)

    code, result = _drive(["route", "pending"])

    assert code == int(ExitCode.OK), result
    assert result["outcome"] == "no_op"
    (warning,) = result["warnings"]
    assert warning["code"] == "no-native-tree"
    assert "intake imported --export" in warning["message"]
    assert [item["session_id"] for item in result["data"]["items"]] == [before.session_id]
    (after,) = session.records(cfg)
    assert after.to_json() == before.to_json()


@pytest.fixture
def volume_agrees(cfg, monkeypatch):
    """The gated close asserts the library volume, and a temporary folder is not it."""
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())


def test_after_a_cutover_the_pass_placing_every_track_is_proof_and_closes_the_run(
    cfg, silence, export, volume_agrees
):
    """The gated close refuses ``awaiting-import``, which is what a landing now
    ends in. Every recorded track settled means the pass reached a row for each,
    so the proof is recorded and the close goes ahead."""
    _land(cfg, silence, export)
    (record,) = session.records(cfg)
    outstanding = routing_pass.read(cfg).outstanding(record.session_id)
    routing_pass.mark(
        cfg,
        [entry.track for entry in outstanding],
        routing_pass.TrackState.ROUTED,
        session_id=record.session_id,
    )

    routing_cli._close_if_settled(cfg, record.session_id)

    (closed,) = session.records(cfg)
    assert closed.state is session.SessionState.CLOSED
    assert closed.detail[session.IMPORT_VERIFIED_KEY]["evidence"] == routing_cli.PLACED_EVIDENCE

    # The run is over and its file is still here. The verb retires it, with no
    # export to read because no run is waiting on one.
    code, result = _drive(["intake", "imported"])
    assert code == int(ExitCode.OK), result
    (item,) = result["data"]["items"]
    assert item["action"] == imported_cli.RETIRED
    assert not _intake_file(cfg).exists()
    assert tree_registry.pending_intake_xml(cfg) == ()


def test_a_waiting_run_with_tracks_still_outstanding_is_not_called_imported(
    cfg, silence, export
):
    """The close is attempted as it always was, and the gate refuses it."""
    _land(cfg, silence, export)
    (record,) = session.records(cfg)

    with pytest.raises(CratekitError) as caught:
        routing_cli._close_if_settled(cfg, record.session_id)

    assert caught.value.cause.reason == "awaiting-import"
    (after,) = session.records(cfg)
    assert after.state is session.SessionState.AWAITING_IMPORT
    assert session.IMPORT_VERIFIED_KEY not in after.detail


# ── The precheck's excusal is three facts, and each one is required ─────────


def _verified(cfg: config.Config, **changes) -> session.SessionRecord:
    record = session.open_session(cfg, workflow=ingest.INTAKE_WORKFLOW)
    session.mark_awaiting_import(
        record,
        session.pending_import(record, artifact="x", summary="s", verify_verb="v"),
        cfg,
    )
    session.mark_import_verified(record, cfg, evidence="a test")
    for name, value in changes.items():
        setattr(record, name, value)
    session.write_record(record, cfg)
    return record


def test_the_precheck_excuses_a_verified_run_holding_no_capture(cfg, export):
    _verified_snapshot(cfg)
    _verified(cfg)
    tree_registry.assert_cutover_ready(cfg, export=export)


def test_the_precheck_refuses_a_verified_run_that_holds_a_capture(cfg, export):
    _verified_snapshot(cfg)
    record = _verified(cfg, snapshot_path="/captures/one")
    assert _refusal(cfg, export).cause.detail["sessions"] == [record.session_id]


def test_the_precheck_refuses_an_open_run_with_no_proof_recorded(cfg, export):
    """A landing that crashed, or any destructive session in flight."""
    _verified_snapshot(cfg)
    record = session.open_session(cfg, workflow=ingest.INTAKE_WORKFLOW)
    refusal = _refusal(cfg, export).cause
    assert refusal.detail["sessions"] == [record.session_id]
    assert refusal.detail["states"] == {record.session_id: "open"}
    assert "close or abandon every open run" in refusal.remediation.steps


def test_the_precheck_refuses_a_verified_run_that_is_not_open(cfg, export):
    _verified_snapshot(cfg)
    record = _verified(cfg, state=session.SessionState.COMMITTED_UNVERIFIED)
    assert _refusal(cfg, export).cause.detail["sessions"] == [record.session_id]


def test_only_a_run_waiting_on_an_import_has_one_to_verify(cfg):
    record = session.open_session(cfg, workflow=ingest.INTAKE_WORKFLOW)
    with pytest.raises(CratekitError) as caught:
        session.mark_import_verified(record, cfg, evidence="a test")
    assert caught.value.cause.reason == "internal-error"
    assert session.read_record(record.session_id, cfg).state is session.SessionState.OPEN


# ── The brief's fourth scenario: intake file shares place_files ─────────────


def test_intake_file_ends_pending_and_is_settled_the_same_way(cfg, silence, export, tmp_path):
    _verified_snapshot(cfg)
    music = Path(cfg.library.root) / cfg.library.music_dir
    music.mkdir(parents=True, exist_ok=True)
    path = music / "Single.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(
        path, {"title": "Single", "artist": "Probe", "genre": "Deep House", "energylevel": 7}
    )

    code, envelope = _drive(["intake", "file", str(path), "--export", str(export)])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    pending = envelope["pending_human_action"]
    intake_file = music / "Single_inboxed.xml"
    assert pending["artifact"] == str(intake_file)
    assert pending["verify_verb"] == "intake.imported"
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.AWAITING_IMPORT
    assert _refusal(cfg, export).cause.reason == "cutover-open-run"

    after = _export_after_import(tmp_path, intake_file)
    code, result = _drive(["intake", "imported", "--export", str(after)])

    assert code == int(ExitCode.OK), result
    assert not intake_file.exists()
    tree_registry.assert_cutover_ready(cfg, export=after)


def test_intake_file_with_no_export_writes_nothing_and_opens_nothing(cfg, silence):
    music = Path(cfg.library.root) / cfg.library.music_dir
    music.mkdir(parents=True, exist_ok=True)
    path = music / "Single.flac"
    shutil.copyfile(silence, path)

    code, envelope = _drive(["intake", "file", str(path)])

    assert code == int(ExitCode.OK), envelope
    assert envelope["pending_human_action"] is None
    assert session.records(cfg) == ()


def test_the_pipeline_result_carries_the_session_the_action_is_on(cfg, silence, export):
    music = Path(cfg.library.root) / cfg.library.music_dir
    music.mkdir(parents=True, exist_ok=True)
    path = music / "Single.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": "Single", "genre": "Deep House", "energylevel": 7})

    result = pipeline.ingest_file(
        path, cfg=cfg, export=export, destination=music / "Single_inboxed.xml"
    )

    (record,) = session.records(cfg)
    assert result.placed[0].session_id == record.session_id


# ── A retired file still names its pass ─────────────────────────────────────


@pytest.mark.parametrize(
    "name",
    [
        "RUN_synced_inboxed.xml",
        "RUN_synced_inboxed.xml.imported",
        "RUN_synced_inboxed.xml.imported-2",
    ],
)
def test_sync_mark_reads_the_same_pass_off_a_retired_intake_file(name):
    """``sync mark`` finds its pass from the intake file's name, and a person who
    proved the import first hands it the retired one."""
    assert mark_cli._pass_name(Path("/library") / name) == "RUN_synced"


@pytest.mark.parametrize("name", ["collection.xml.imported", "_inboxed.xml.imported", "x.imported"])
def test_a_retired_tail_does_not_make_any_file_an_intake_file(name):
    with pytest.raises(CratekitError):
        mark_cli._pass_name(Path("/library") / name)


def test_the_retired_name_is_out_of_the_pending_scan_and_reads_back(cfg):
    written = Path(cfg.library.root) / f"{BATCH}_inboxed.xml"
    written.write_bytes(b"<DJ_PLAYLISTS/>")
    assert tree_registry.pending_intake_xml(cfg) == (written,)

    retired = imported_cli.retire(written)

    assert retired is not None
    assert tree_registry.pending_intake_xml(cfg) == ()
    assert land_cli.unretired_name(retired.name) == written.name


# ── What the review found ───────────────────────────────────────────────────


def test_a_run_landed_before_the_fix_is_settled_too(cfg, silence, export, tmp_path):
    """EVERY LANDING BEFORE R-501 IS THIS SHAPE: ``open``, no pending action, no
    proof, its tracks in the ledger. It is the population the finding was about,
    and a verb that looked only for ``awaiting-import`` would leave it where it was.
    Its intake file was never recorded, so none is retired, and the item says so."""
    _verified_snapshot(cfg)
    _land(cfg, silence, export)
    (record,) = session.records(cfg)
    after = _export_after_import(tmp_path, _intake_file(cfg))
    record.state = session.SessionState.OPEN
    record.pending = None
    session.write_record(record, cfg)
    assert _refusal(cfg, export).cause.reason == "cutover-open-run"

    code, not_yet = _drive(["intake", "imported", "--export", str(export)])
    assert code == int(ExitCode.PENDING_HUMAN), not_yet
    assert not_yet["data"]["items"][0]["action"] == imported_cli.NOT_IMPORTED
    assert session.read_record(record.session_id, cfg).to_json() == record.to_json()

    code, result = _drive(["intake", "imported", "--export", str(after)])

    assert code == int(ExitCode.OK), result
    (item,) = result["data"]["items"]
    assert (item["action"], item["retired_to"]) == (imported_cli.IMPORTED, None)
    assert session.owes_only_deferred_routing(session.read_record(record.session_id, cfg))
    assert _refusal(cfg, after).cause.reason == "cutover-xml-pending"


def test_an_open_run_holding_a_capture_is_never_taken_for_a_landing(cfg, silence, export, tmp_path):
    _land(cfg, silence, export)
    (record,) = session.records(cfg)
    after = _export_after_import(tmp_path, _intake_file(cfg))
    record.state = session.SessionState.OPEN
    record.pending = None
    record.snapshot_path = "/captures/one"
    session.write_record(record, cfg)

    code, result = _drive(["intake", "imported", "--export", str(after)])

    assert (code, result["outcome"]) == (int(ExitCode.OK), "no_op")
    assert session.read_record(record.session_id, cfg).to_json() == record.to_json()


def test_tracks_acknowledged_as_gone_are_not_proof_of_an_import(cfg, silence, export):
    """Settled is not imported: acknowledging takes no row."""
    _land(cfg, silence, export)
    (record,) = session.records(cfg)
    routing_pass.acknowledge(
        cfg,
        [entry.track for entry in routing_pass.read(cfg).outstanding(record.session_id)],
        session_id=record.session_id,
        actor="a-person",
    )
    assert not routing_pass.read(cfg).outstanding(record.session_id)

    with pytest.raises(CratekitError) as caught:
        routing_cli._close_if_settled(cfg, record.session_id)

    assert caught.value.cause.reason == "awaiting-import"
    assert session.IMPORT_VERIFIED_KEY not in session.read_record(record.session_id, cfg).detail


def test_a_refused_close_is_reported_and_tried_again_next_time(
    cfg, silence, export, tmp_path, monkeypatch
):
    """The file is retired and the proof recorded by the time the gated close
    can refuse, so the refusal is on the item and the next run closes it."""
    _land(cfg, silence, export)
    (record,) = session.records(cfg)
    after = _export_after_import(tmp_path, _intake_file(cfg))
    routing_pass.mark(
        cfg,
        [entry.track for entry in routing_pass.read(cfg).outstanding(record.session_id)],
        routing_pass.TrackState.ROUTED,
        session_id=record.session_id,
    )

    # A temporary folder is not the recorded volume, so the gated close refuses.
    code, result = _drive(["intake", "imported", "--export", str(after)])

    assert code == int(ExitCode.OK), result
    (item,) = result["data"]["items"]
    assert (item["action"], item["closed"]) == (imported_cli.IMPORTED, False)
    assert item["close_refused"]
    assert [w["code"] for w in result["warnings"]] == [item["close_refused"]]
    assert not _intake_file(cfg).exists()
    assert session.read_record(record.session_id, cfg).state is session.SessionState.OPEN

    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    code, again = _drive(["intake", "imported"])

    assert code == int(ExitCode.OK), again
    (item,) = again["data"]["items"]
    assert (item["action"], item["closed"]) == (imported_cli.RETIRED, True)
    assert session.read_record(record.session_id, cfg).state is session.SessionState.CLOSED
    assert _drive(["intake", "imported"])[1]["outcome"] == "no_op"


def test_a_failed_call_leaves_an_earlier_runs_intake_file_alone(cfg, silence, export, monkeypatch):
    """The write is an overwrite, and the file already there is one an earlier
    run's steps still name."""
    music = Path(cfg.library.root) / cfg.library.music_dir
    music.mkdir(parents=True, exist_ok=True)
    path = music / "One.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": "One", "genre": "Deep House", "energylevel": 7})
    destination = music / "One_inboxed.xml"
    ingest.place_files([path], cfg=cfg, export=export, destination=destination)

    def refusing(*args, **kwargs):
        raise refuse("internal-error", "the ledger could not be written")

    monkeypatch.setattr(routing_pass, "record_intents", refusing)
    with pytest.raises(CratekitError):
        ingest.place_files([path], cfg=cfg, export=export, destination=destination)

    assert destination.is_file()
    states = sorted(str(record.state) for record in session.records(cfg))
    assert states == ["abandoned", "awaiting-import"]


def test_a_failed_call_records_no_track_the_ledger_cannot_withdraw(
    cfg, silence, export, monkeypatch
):
    """Nothing that can fail follows the ledger write, because an intent cannot
    be taken back and an abandoned run's would be outstanding for ever."""
    music = Path(cfg.library.root) / cfg.library.music_dir
    music.mkdir(parents=True, exist_ok=True)
    path = music / "One.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": "One", "genre": "Deep House", "energylevel": 7})

    def failing(*args, **kwargs):
        raise refuse("internal-error", "the session log could not be written")

    monkeypatch.setattr(session, "mark_awaiting_import", failing)
    with pytest.raises(CratekitError):
        ingest.place_files(
            [path], cfg=cfg, export=export, destination=music / "One_inboxed.xml"
        )

    assert routing_pass.read(cfg).intents == ()
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.ABANDONED


def test_a_retire_that_cannot_rename_is_a_refusal_and_changes_nothing(
    cfg, silence, export, tmp_path, monkeypatch
):
    _land(cfg, silence, export)
    after = _export_after_import(tmp_path, _intake_file(cfg))

    def denied(*args, **kwargs):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(imported_cli.os, "replace", denied)
    _, result = _drive(["intake", "imported", "--export", str(after)])

    assert result["cause"]["reason"] == "path-permission-denied", result
    assert _intake_file(cfg).is_file()
    assert not _intake_file(cfg).with_name(_intake_file(cfg).name + ".imported").exists()
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.AWAITING_IMPORT


def test_doctor_reads_a_proven_run_as_proven_and_not_as_in_progress(cfg):
    from cratekit.cli import doctor

    proven = _verified(cfg)
    in_flight = session.open_session(cfg, workflow=ingest.INTAKE_WORKFLOW)

    assert "import proven" in doctor._open_state(session.read_record(proven.session_id, cfg))
    assert doctor._open_state(in_flight) == "open"


def test_an_intake_file_no_waiting_run_names_is_still_refused_as_the_export(
    cfg, silence, export, tmp_path
):
    """THE NAME CHECK ALONE, where the identity check cannot help. A later
    batch's intake file is spliced from an export that already holds this run's
    tracks, so it names them all, and no waiting run's record points at it."""
    _land(cfg, silence, export)
    other = tmp_path / "later_inboxed.xml"
    other.write_bytes(_intake_file(cfg).read_bytes())

    _, result = _drive(["intake", "imported", "--export", str(other)])

    assert result["cause"]["reason"] == "library-export-unusable", result
    assert "carries a name" in result["cause"]["message"]
    (record,) = session.records(cfg)
    assert record.state is session.SessionState.AWAITING_IMPORT
    assert _intake_file(cfg).is_file()


# ── R-678: what a person reads without asking for json ──


def test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired(
    cfg, silence, export, tmp_path
):
    """54 proven rows and a retired intake file printed ``intake.imported: ok``."""
    _land(cfg, silence, export, "One.flac", "Two.flac", batch="first")
    after = _export_after_import(tmp_path, _intake_file(cfg, "first"))
    (waiting,) = [r for r in session.records(cfg) if r.workflow == ingest.INTAKE_WORKFLOW]

    code, text = drive_human(["intake", "imported", "--export", str(after)])

    assert code == int(ExitCode.OK), text
    lines = text.splitlines()
    retired = f"first_inboxed.xml{land_cli.RETIRED_SUFFIX}"
    assert any(
        line.startswith(f"  run {waiting.session_id}: proven imported, 2 track(s); ")
        and f"intake file retired to {retired}" in line
        for line in lines
    ), text
    assert "  proven: 1 run(s), 2 track(s); retired: 1 intake file(s)" in lines, text


def test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does(
    cfg, silence, export, tmp_path
):
    _land(cfg, silence, export, "One.flac", batch="first")
    after_first = _export_after_import(tmp_path, _intake_file(cfg, "first"))
    _land(cfg, silence, export, "Two.flac", batch="second")

    code, text = drive_human(["intake", "imported", "--export", str(after_first)])

    assert code == int(ExitCode.PENDING_HUMAN), text
    lines = text.splitlines()
    assert any(
        line.endswith(": not imported, 1 of 1 landed track(s) not in the export") for line in lines
    ), text
    assert "  proven: 1 run(s), 1 track(s); retired: 1 intake file(s)" in lines, text


def test_nothing_waiting_prints_no_proof_lines(cfg, export):
    code, text = drive_human(["intake", "imported", "--export", str(export)])

    assert code == int(ExitCode.OK), text
    assert text.splitlines()[0] == "intake.imported: no_op", text
    assert "proven:" not in text, text
