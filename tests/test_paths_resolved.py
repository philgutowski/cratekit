"""R-372: a collection most of whose rows record an unmapped drive is refused, not read as ok.

The sitting that found it: the first real ``crate metadata mytags-vocals`` plan
reported ``count 0, active 9937, unresolved 9937``, outcome ok, and ``crate
doctor`` was green beside it, because rekordbox keeps nearly every row under
the drive name it was imported with and setup had written no
``library.location_prefix_map`` rule. Three surfaces answer that here: the plan
and its apply refuse under one slug with the totals still in the payload,
doctor's ``library.paths_resolved`` reads the same ratio off a disposable copy
of the database, and setup reads rekordbox's own two drive names off a copy and
offers the rule.

EVERY OPEN IN THIS MODULE IS SPIED ON. The live database path is configured
and present, and the assertion that it was never handed to the binding is what
the standing constraint on the live database means in a test.
"""

from __future__ import annotations

import hashlib
import shutil
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import pytest

from cratekit.cli import doctor, prompt, registry
from cratekit.cli import setup as setup_verb
from cratekit.core import config, locations, rb_writer, session, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import metadata_cli
from tests import doctor_machines
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database, _row


#: The drive rekordbox recorded the rows under, and no longer mounts. Built
#: under the temporary directory rather than spelled as a volume literal, which
#: the repository scan refuses; what matters is that it is absolute, outside
#: the library root, and under no rule.
def _old_drive(tmp_path: Path) -> Path:
    return tmp_path / "Volumes" / "RENAMED"

#: The prompter class captured before any test replaces the module attribute,
#: so a scripted prompter is still built from the real one.
_RealPrompter = prompt.Prompter


@pytest.fixture
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@dataclass
class Bench:
    """One configured machine over a disposable database, and its knobs."""

    cfg: config.Config
    root: Path
    music: Path
    db_path: Path
    old_drive: Path

    def add_rows(self, *, old: int = 0, local: int = 0, silence: Path | None = None) -> None:
        """``old`` rows recorded under the renamed drive, ``local`` rows under the root.

        The old rows' files sit under the library root at the path a rule from
        the old drive to the root would rewrite them to, so the same fixture
        answers both halves: unmapped without the rule, resolved with it.
        """
        from pyrekordbox.db6 import tables
        from sqlalchemy import create_engine
        from sqlalchemy.orm import Session

        assert silence is not None
        engine = create_engine(f"sqlite:///{self.db_path}")
        with Session(engine) as db_session:
            next_id = 100
            for index in range(old):
                audio = self.music / f"old-{index}.flac"
                shutil.copy2(silence, audio)
                assert tags.write_tags(audio, {"voxlevel": 80, "voxgender": "F"})
                recorded = self.old_drive / "Music" / audio.name
                db_session.add(
                    _row(
                        tables.DjmdContent,
                        ID=str(next_id),
                        Title=audio.name,
                        rb_local_deleted=0,
                        FolderPath=locations.location_url(recorded),
                    )
                )
                next_id += 1
            for index in range(local):
                audio = self.music / f"local-{index}.flac"
                shutil.copy2(silence, audio)
                db_session.add(
                    _row(
                        tables.DjmdContent,
                        ID=str(next_id),
                        Title=audio.name,
                        rb_local_deleted=0,
                        FolderPath=locations.location_url(audio),
                    )
                )
                next_id += 1
            db_session.commit()
        engine.dispose()

    def set_drives(self, base: str | None, current: str | None) -> None:
        """What rekordbox's own registry row says about the drive."""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "UPDATE djmdProperty SET BaseDBDrive = ?, CurrentDBDrive = ?", (base, current)
        )
        conn.commit()
        conn.close()

    def record_rule(self) -> config.Config:
        """Write the rule setup should have offered, the way the sitting typed it."""
        document = dict(self.cfg.to_toml_dict())
        document["library"]["location_prefix_map"] = [
            {"from": str(self.old_drive), "to": str(self.root)}
        ]
        cfg = config.from_dict(document)
        config.save(cfg)
        config.reset_cache()
        self.cfg = config.load()
        return self.cfg

    def digest(self) -> str:
        return hashlib.sha256(self.db_path.read_bytes()).hexdigest()


@pytest.fixture
def bench(tmp_path, monkeypatch) -> Bench:
    """The ``ready`` machine of the My Tags suite, with the database's drive row set."""
    from pyrekordbox.db6 import database as binding

    from cratekit.core import preflight

    root = tmp_path / "library"
    music = root / "Music"
    music.mkdir(parents=True)
    db_path = root / "db" / "master.db"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(
        valid_data(
            root,
            profile={"name": "full"},
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    config.save(cfg)
    config.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer,
        "integrity_ok",
        lambda target, **kwargs: real_integrity_ok(target, unlock=False),
    )
    session.record_acknowledgment(cfg, terminal=lambda: True)
    _build_disposable_database(db_path, with_tag_category=True)
    machine = Bench(
        cfg=config.load(), root=root, music=music, db_path=db_path, old_drive=_old_drive(tmp_path)
    )
    machine.set_drives(f"{machine.old_drive}/", f"{root}/")
    return machine


@pytest.fixture
def opened(monkeypatch) -> list[Path]:
    """Every path handed to the opener, so the live one can be shown absent."""
    real = rb_writer.open_db
    paths: list[Path] = []

    def spy(path=None, **kwargs):
        paths.append(Path(path) if path is not None else Path("<configured>"))
        return real(path, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", spy)
    return paths


def _never_the_live_path(opened: list[Path], live: Path) -> None:
    assert opened, "nothing was opened, so nothing was read"
    assert live not in opened, opened
    assert Path("<configured>") not in opened, opened
    for path in opened:
        assert path.parent.name.startswith("cratekit-copy-"), path
        assert not path.exists(), f"the copy at {path} outlived its read"


# ---------------------------------------------------------------------------
# The rule
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("active", "unmapped", "expected"),
    [
        (0, 0, False),
        (10, 5, False),
        (10, 6, True),
        (9937, 9937, True),
        (9937, 167, False),
        (1, 1, True),
    ],
)
def test_a_majority_is_strictly_more_than_half_and_never_an_empty_collection(
    active, unmapped, expected
):
    totals = metadata_cli.ResolutionTotals(active=active, unresolved=unmapped, unmapped=unmapped)
    assert totals.majority_unmapped is expected


def test_the_verb_declares_the_check_and_the_slug_is_registered():
    assert "library.paths_resolved" in registry.entry("metadata.mytags-vocals").doctor_checks
    assert "library.paths_resolved" in doctor.CHECK_KEYS
    from cratekit.core.cause import REASONS

    assert REASONS[metadata_cli.PATHS_MAJORITY_UNRESOLVED] is ExitCode.PRECONDITION


# ---------------------------------------------------------------------------
# The plan and the apply
# ---------------------------------------------------------------------------


def test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload(
    bench, silence
):
    """The refusal half, driven: active 12, unmapped 10, outcome failed, count 0 shown."""
    bench.add_rows(old=10, silence=silence)

    code, envelope = drive(["metadata", "mytags-vocals"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["outcome"] == "failed"
    assert envelope["cause"]["reason"] == metadata_cli.PATHS_MAJORITY_UNRESOLVED
    assert envelope["cause"]["remediation"]["remedy"] == str(Remedy.RUN_SETUP)
    assert envelope["warnings"] == []
    totals = envelope["data"]["totals"]
    # The two fixture rows with no recorded path count as unresolved and are not
    # unmapped: a streaming row is not a prefix rule's to fix.
    assert (totals["active"], totals["unresolved"], totals["unmapped"]) == (12, 12, 10)
    assert totals["count"] == 0
    prefixes = envelope["cause"]["detail"]["prefixes"]
    assert sum(prefixes.values()) == 10
    assert all(str(bench.old_drive).startswith(prefix) for prefix in prefixes)
    assert "10 under " in envelope["cause"]["message"]


def test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing(bench, silence):
    bench.add_rows(old=10, silence=silence)
    before = bench.digest()

    code, envelope = drive(["metadata", "mytags-vocals", "--apply"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == metadata_cli.PATHS_MAJORITY_UNRESOLVED
    assert envelope["data"]["totals"]["written"] == 0
    assert bench.digest() == before
    assert not rb_writer.snapshot_root(bench.cfg).exists()
    db = rb_writer.open_db(bench.db_path, unlock=False, cfg=bench.cfg)
    try:
        assert metadata_cli.VALUE_VOX not in [tag.Name for tag in db.get_my_tag()]
    finally:
        rb_writer.close_db(db)


def test_a_minority_of_unmapped_rows_stays_ok_with_the_counts_visible(bench, silence):
    """The sitting after the hand edit: a minority is reported, never refused."""
    bench.add_rows(old=3, local=10, silence=silence)

    code, envelope = drive(["metadata", "mytags-vocals"])

    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert (totals["active"], totals["unresolved"], totals["unmapped"]) == (15, 5, 3)
    assert envelope["data"]["items"] == []


def test_the_rule_setup_should_have_offered_turns_the_majority_into_a_plan(bench, silence):
    """With the rule in place the same rows resolve, and the voiced files are planned."""
    bench.add_rows(old=10, silence=silence)
    bench.record_rule()

    code, envelope = drive(["metadata", "mytags-vocals"])

    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert (totals["active"], totals["unresolved"], totals["unmapped"]) == (12, 2, 0)
    assert totals["count"] == 10
    assert all(item["values"] == ["vox", "female vox"] for item in envelope["data"]["items"])


# ---------------------------------------------------------------------------
# Doctor
# ---------------------------------------------------------------------------


def _real_survey() -> doctor.Probes:
    """The green machine with the one seam under test left real."""
    return doctor_machines.green(path_survey=doctor._survey_paths)


def test_doctor_fails_paths_resolved_over_a_majority_off_a_copy(bench, silence, opened):
    bench.add_rows(old=10, silence=silence)
    before = bench.digest()

    report = doctor.run(bench.cfg, probes=_real_survey())

    finding = next(f for f in report.findings if f.key == "library.paths_resolved")
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.RUN_SETUP
    assert finding.cause is not None
    assert finding.cause.reason == metadata_cli.PATHS_MAJORITY_UNRESOLVED
    assert "10 of 12" in finding.detail
    assert doctor.failure_cause(report).reason == metadata_cli.PATHS_MAJORITY_UNRESOLVED
    _never_the_live_path(opened, bench.db_path)
    assert bench.digest() == before


def test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok(bench, silence, opened):
    bench.add_rows(old=3, local=10, silence=silence)
    minority = next(
        f
        for f in doctor.run(bench.cfg, probes=_real_survey()).findings
        if f.key == "library.paths_resolved"
    )
    assert minority.status is doctor.Status.INFO
    assert "3 of 15" in minority.detail

    bench.record_rule()
    clean = next(
        f
        for f in doctor.run(bench.cfg, probes=_real_survey()).findings
        if f.key == "library.paths_resolved"
    )
    assert clean.status is doctor.Status.OK
    assert "15 active rows" in clean.detail
    _never_the_live_path(opened, bench.db_path)


def test_doctor_says_so_when_there_is_no_database_to_read(bench, opened):
    bench.db_path.unlink()
    finding = next(
        f
        for f in doctor.run(bench.cfg, probes=_real_survey()).findings
        if f.key == "library.paths_resolved"
    )
    assert finding.status is doctor.Status.INFO
    assert "no database file" in finding.detail
    assert opened == []


def test_doctor_reports_a_copy_it_could_not_open_as_unknown_rather_than_good(bench, opened):
    bench.db_path.write_bytes(b"not a database at all, and long enough to matter" * 40)
    finding = next(
        f
        for f in doctor.run(bench.cfg, probes=_real_survey()).findings
        if f.key == "library.paths_resolved"
    )
    assert finding.status is doctor.Status.FAIL
    assert finding.cause is not None
    assert finding.remedy is not None
    assert "could not be established" in finding.detail
    _never_the_live_path(opened, bench.db_path)


def test_the_two_synthetic_machines_answer_the_check_opposite_ways(bench):
    healthy = next(
        f
        for f in doctor.run(bench.cfg, probes=doctor_machines.green()).findings
        if f.key == "library.paths_resolved"
    )
    broken = next(
        f
        for f in doctor.run(bench.cfg, probes=doctor_machines.hostile()).findings
        if f.key == "library.paths_resolved"
    )
    assert healthy.status is doctor.Status.OK
    # The hostile machine has rekordbox running, and that is the first question
    # the check asks: a copy taken under a live application is not taken.
    assert broken.status is doctor.Status.FAIL
    assert broken.remedy is Remedy.QUIT_REKORDBOX
    assert broken.cause is None
    # With the application closed and the volume recognised, the hostile
    # machine's survey is what refuses, under the plan's own slug.
    surveyed = next(
        f
        for f in doctor.run(
            bench.cfg,
            probes=doctor_machines.hostile(
                process_lister=lambda: (), identity_provider=lambda _path: doctor_machines.VOLUME
            ),
        ).findings
        if f.key == "library.paths_resolved"
    )
    assert surveyed.status is doctor.Status.FAIL
    assert surveyed.remedy is Remedy.RUN_SETUP
    assert surveyed.cause is not None


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------


def _scripted(answers: list[str]) -> prompt.Prompter:
    queued = list(answers)

    def read_line() -> str:
        if not queued:
            raise EOFError("nothing left in the script")
        return queued.pop(0) + "\n"

    return _RealPrompter(read_line=read_line, read_secret=lambda _q: "", write=lambda _t: None)


def _silent() -> prompt.Prompter:
    def read_line() -> str:
        raise EOFError("nothing can be asked")

    return _RealPrompter(read_line=read_line, read_secret=lambda _q: "", write=lambda _t: None)


def _note(wizard: setup_verb._Wizard) -> doctor.Finding:
    return next(n for n in wizard.notes if n.key == "setup.prefix_map")


def test_setup_offers_the_rule_from_the_databases_own_drive_names_off_a_copy(bench, opened):
    document = dict(bench.cfg.to_toml_dict())
    wizard = setup_verb._Wizard(document, _scripted(["yes"]))

    assert setup_verb._propose_prefix_map(wizard, document, bench.cfg) is True

    assert document["library"]["location_prefix_map"] == [
        {"from": str(bench.old_drive), "to": config.LIBRARY_ROOT_TOKEN}
    ]
    assert _note(wizard).status is doctor.Status.OK
    assert "library.location_prefix_map (answered)" in wizard.asked
    _never_the_live_path(opened, bench.db_path)
    # The document the offer wrote into is a configuration that loads.
    loaded = config.from_dict(document)
    assert loaded.library.location_prefix_map == (
        config.PrefixMapping(from_prefix=str(bench.old_drive), to_prefix=config.LIBRARY_ROOT_TOKEN),
    )
    assert loaded.resolved_prefix_map() == ((str(bench.old_drive), str(bench.root)),)


def test_setup_records_nothing_when_the_offer_goes_unanswered(bench, opened):
    document = dict(bench.cfg.to_toml_dict())
    wizard = setup_verb._Wizard(document, _silent())

    assert setup_verb._propose_prefix_map(wizard, document, bench.cfg) is False

    assert document["library"].get("location_prefix_map", []) == []
    note = _note(wizard)
    assert note.status is doctor.Status.INFO
    assert "NOT recorded" in note.detail
    _never_the_live_path(opened, bench.db_path)


def test_setup_skips_the_offer_when_no_database_is_present(bench, opened):
    bench.db_path.unlink()
    document = dict(bench.cfg.to_toml_dict())
    asked: list[str] = []
    prompter = _RealPrompter(
        read_line=lambda: (asked.append("asked"), "yes\n")[1],
        read_secret=lambda _q: "",
        write=lambda _t: None,
    )
    wizard = setup_verb._Wizard(document, prompter)

    assert setup_verb._propose_prefix_map(wizard, document, bench.cfg) is False

    assert asked == []
    assert opened == []
    assert document["library"].get("location_prefix_map", []) == []
    assert "no database file" in _note(wizard).detail


def test_setup_offers_nothing_when_the_two_drive_names_agree(bench, opened):
    bench.set_drives(f"{bench.root}/", f"{bench.root}/")
    document = dict(bench.cfg.to_toml_dict())
    asked: list[str] = []
    prompter = _RealPrompter(
        read_line=lambda: (asked.append("asked"), "yes\n")[1],
        read_secret=lambda _q: "",
        write=lambda _t: None,
    )
    wizard = setup_verb._Wizard(document, prompter)

    assert setup_verb._propose_prefix_map(wizard, document, bench.cfg) is False

    assert asked == []
    assert document["library"].get("location_prefix_map", []) == []
    assert "no prefix rule is needed" in _note(wizard).detail
    _never_the_live_path(opened, bench.db_path)


def test_setup_leaves_a_recorded_map_alone(bench, opened):
    cfg = bench.record_rule()
    document = dict(cfg.to_toml_dict())
    wizard = setup_verb._Wizard(document, _scripted(["yes"]))

    assert setup_verb._propose_prefix_map(wizard, document, cfg) is False

    assert document["library"]["location_prefix_map"] == [
        {"from": str(bench.old_drive), "to": str(bench.root)}
    ]
    assert "left alone" in _note(wizard).detail
    assert opened == []


def test_setup_notes_a_copy_it_could_not_open_and_leaves_the_verdict_to_doctor(bench, opened):
    bench.db_path.write_bytes(b"not a database at all, and long enough to matter" * 40)
    document = dict(bench.cfg.to_toml_dict())
    wizard = setup_verb._Wizard(document, _scripted(["yes"]))

    assert setup_verb._propose_prefix_map(wizard, document, bench.cfg) is False

    note = _note(wizard)
    assert note.status is doctor.Status.INFO
    assert "could not be read from a copy" in note.detail
    assert document["library"].get("location_prefix_map", []) == []
    _never_the_live_path(opened, bench.db_path)


def test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it(
    bench, silence, opened, monkeypatch
):
    """Through the real dispatcher: the offer is taken, saved once, and the closing
    doctor resolves every row through the rule it just wrote."""
    bench.add_rows(old=10, silence=silence)
    # Two answers: the backup destinations are offered first, since R-345, on
    # a full profile with none recorded, and declined here; the second answer
    # is the prefix map offer this test is about.
    monkeypatch.setattr(prompt, "Prompter", lambda: _scripted(["no", "yes"]))
    monkeypatch.setattr(
        doctor,
        "Probes",
        lambda: doctor_machines.green(
            installed_app_version=lambda _cfg: RECORDED_APP_VERSION,
            path_survey=doctor._survey_paths,
        ),
    )

    code, envelope = drive(["setup"])

    assert code == int(ExitCode.OK), envelope
    written = config.load()
    assert written.backup.dest is None
    assert written.library.location_prefix_map == (
        config.PrefixMapping(from_prefix=str(bench.old_drive), to_prefix=config.LIBRARY_ROOT_TOKEN),
    )
    checks = {check["key"]: check for check in envelope["data"]["checks"]}
    assert checks["setup.prefix_map"]["status"] == "ok"
    assert checks["library.paths_resolved"]["status"] == "ok"
    _never_the_live_path(opened, bench.db_path)


def test_doctor_takes_no_copy_while_rekordbox_is_running(bench, silence, opened):
    bench.add_rows(old=10, silence=silence)
    finding = next(
        f
        for f in doctor.run(
            bench.cfg,
            probes=doctor_machines.green(
                process_lister=lambda: ("rekordboxAgent",), path_survey=doctor._survey_paths
            ),
        ).findings
        if f.key == "library.paths_resolved"
    )
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.QUIT_REKORDBOX
    assert "rekordboxAgent" in finding.detail
    assert opened == []


def test_doctor_defers_to_the_volume_checks_before_reading_anything(bench, silence, opened):
    """A leftover mount point holding a stale database is not surveyed."""
    bench.add_rows(old=10, silence=silence)
    finding = next(
        f
        for f in doctor.run(
            bench.cfg,
            probes=doctor_machines.green(
                identity_provider=lambda _path: "0000-0000", path_survey=doctor._survey_paths
            ),
        ).findings
        if f.key == "library.paths_resolved"
    )
    assert finding.status is doctor.Status.INFO
    assert "not asserted" in finding.detail
    assert opened == []


def test_a_row_whose_location_will_not_decode_counts_as_unresolved_not_a_defect(bench, silence):
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    bench.add_rows(local=2, silence=silence)
    engine = create_engine(f"sqlite:///{bench.db_path}")
    with Session(engine) as db_session:
        db_session.add(
            _row(
                tables.DjmdContent,
                ID="900",
                Title="on another host",
                rb_local_deleted=0,
                FolderPath="file://nas.local/share/track.flac",
            )
        )
        db_session.commit()
    engine.dispose()
    with pytest.raises(locations.LocationDecodeError):
        locations.location_to_path("file://nas.local/share/track.flac")

    code, envelope = drive(["metadata", "mytags-vocals"])

    assert code == int(ExitCode.OK), envelope
    totals = envelope["data"]["totals"]
    assert (totals["active"], totals["unresolved"], totals["unmapped"]) == (5, 3, 0)


def test_setup_skips_the_offer_while_rekordbox_is_running(bench, opened, monkeypatch):
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    document = dict(bench.cfg.to_toml_dict())
    wizard = setup_verb._Wizard(document, _scripted(["yes"]))

    assert setup_verb._propose_prefix_map(wizard, document, bench.cfg) is False

    assert opened == []
    assert document["library"].get("location_prefix_map", []) == []
    # The wizard's OWN sentence, not the copy's refusal repeated through the
    # "could not be read" note: the wizard asked before it copied.
    assert "none was taken and no drive rule was offered" in _note(wizard).detail


def test_setup_notes_a_file_it_could_not_copy_rather_than_aborting(bench, opened, monkeypatch):
    """The copy itself, not the open: an OSError here used to escape the verb."""
    import shutil as _shutil

    def denied(src, dst, *args, **kwargs):
        if Path(src) == bench.db_path:
            raise PermissionError(13, "Permission denied", str(src))
        return _shutil.copy2(src, dst, *args, **kwargs)

    monkeypatch.setattr(rb_writer.shutil, "copy2", denied)
    document = dict(bench.cfg.to_toml_dict())
    wizard = setup_verb._Wizard(document, _scripted(["yes"]))

    assert setup_verb._propose_prefix_map(wizard, document, bench.cfg) is False

    note = _note(wizard)
    assert note.status is doctor.Status.INFO
    assert "could not be copied" in note.detail
    assert opened == []
    assert document["library"].get("location_prefix_map", []) == []


def test_setup_offers_the_root_when_rekordbox_still_records_the_old_name_twice(bench, opened):
    """The drive was renamed and rekordbox has not been opened since."""
    bench.set_drives(f"{bench.old_drive}/", f"{bench.old_drive}/")
    document = dict(bench.cfg.to_toml_dict())
    wizard = setup_verb._Wizard(document, _scripted(["yes"]))

    assert setup_verb._propose_prefix_map(wizard, document, bench.cfg) is True

    assert document["library"]["location_prefix_map"] == [
        {"from": str(bench.old_drive), "to": config.LIBRARY_ROOT_TOKEN}
    ]
    _never_the_live_path(opened, bench.db_path)


def test_setup_offers_nothing_when_the_root_sits_under_the_recorded_drive(bench, opened):
    """A library nested inside the recorded drive is already where the rows say."""
    bench.set_drives(f"{bench.root.parent}/", f"{bench.root.parent}/")
    document = dict(bench.cfg.to_toml_dict())
    asked: list[str] = []
    prompter = _RealPrompter(
        read_line=lambda: (asked.append("asked"), "yes\n")[1],
        read_secret=lambda _q: "",
        write=lambda _t: None,
    )
    wizard = setup_verb._Wizard(document, prompter)

    assert setup_verb._propose_prefix_map(wizard, document, bench.cfg) is False

    assert asked == []
    assert "no prefix rule is needed" in _note(wizard).detail
    _never_the_live_path(opened, bench.db_path)


def test_setup_records_a_current_drive_that_is_not_the_root_literally(bench, opened):
    """A library that is a folder on the current drive maps drive to drive."""
    elsewhere = bench.root.parent / "Volumes" / "CURRENT"
    bench.set_drives(f"{bench.old_drive}/", f"{elsewhere}/")
    document = dict(bench.cfg.to_toml_dict())
    wizard = setup_verb._Wizard(document, _scripted(["yes"]))

    assert setup_verb._propose_prefix_map(wizard, document, bench.cfg) is True

    assert document["library"]["location_prefix_map"] == [
        {"from": str(bench.old_drive), "to": str(elsewhere)}
    ]
    _never_the_live_path(opened, bench.db_path)


def test_the_disposable_copy_is_private_and_gone_afterwards(bench):
    with rb_writer.disposable_copy(bench.db_path) as copied:
        assert copied.is_file()
        assert copied != bench.db_path
        assert copied.parent.name.startswith("cratekit-copy-")
        assert (copied.parent.stat().st_mode & 0o777) == 0o700
        directory = copied.parent
    assert not directory.exists()


def test_recorded_drives_strip_the_separator_rekordbox_stores_and_blank_is_none(bench):
    bench.set_drives("/old/DRIVE/", "  ")
    db = rb_writer.open_db(bench.db_path, unlock=False, cfg=bench.cfg)
    try:
        assert rb_writer.recorded_db_drives(db) == ("/old/DRIVE", None)
    finally:
        rb_writer.close_db(db)


def test_a_refusal_built_from_the_totals_names_the_prefixes_and_the_current_map(bench):
    totals = metadata_cli.ResolutionTotals(
        active=100,
        unresolved=90,
        unmapped=90,
        prefixes={"/old/A": 60, "/old/B": 20, "/old/C": 6, "/old/D": 4},
    )
    cause = metadata_cli.majority_unmapped_cause(bench.cfg, totals)
    assert cause.reason == metadata_cli.PATHS_MAJORITY_UNRESOLVED
    assert cause.code is ExitCode.PRECONDITION
    assert "60 under /old/A" in cause.message
    assert "1 other prefix" in cause.message
    assert cause.detail["prefix_map"] == []
    assert cause.detail["unmapped"] == 90
    with pytest.raises(CratekitError):
        raise CratekitError(cause)


def test_the_read_only_copy_refuses_under_a_running_application_on_its_own(bench, monkeypatch):
    """The copy's own guard, alone: doctor and setup ask first, and this is the layer
    beneath them that a new caller inherits without asking."""
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    with pytest.raises(CratekitError) as caught:
        with rb_writer.read_only_copy(bench.db_path, cfg=bench.cfg):
            pass
    assert caught.value.cause.reason == "rekordbox-running"


# ---------------------------------------------------------------------------
# A path whose file is not a library (R-663)
# ---------------------------------------------------------------------------


def _empty(path: Path) -> Path:
    """The file sitting 5 was given: zero bytes, beside where a library would be."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")
    return path


def _foreign(path: Path, tables: tuple[str, ...] = ("manage_tbl",)) -> Path:
    """A real SQLite file holding tables, none of them the ones the canary reads.

    rekordbox keeps several of these beside its own database, so a search for
    a database file finds them too.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    for table in tables:
        conn.execute(f"CREATE TABLE {table} (ID TEXT, value TEXT)")
    conn.execute(f"INSERT INTO {tables[0]} VALUES ('1', 'x')")
    conn.commit()
    conn.close()
    return path


def _refusal_from_the_copy(path: Path, cfg: config.Config) -> CratekitError:
    with pytest.raises(CratekitError) as caught:
        with rb_writer.read_only_copy(path, cfg=cfg):
            pass
    return caught.value


def test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path(
    bench, opened, monkeypatch
):
    _empty(bench.db_path)
    measured: list[Path] = []
    real = rb_writer._not_a_library

    def spy(source, copied):
        measured.append(Path(copied))
        return real(source, copied)

    monkeypatch.setattr(rb_writer, "_not_a_library", spy)

    cause = _refusal_from_the_copy(bench.db_path, bench.cfg).cause

    assert cause.reason == "library-database-not-rekordbox"
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert str(bench.db_path) in cause.message
    assert "is empty, 0 bytes" in cause.message
    # The size and the path, NOT the table the canary tripped on.
    assert "no such table" not in cause.message
    assert "agentRegistry" not in cause.message
    assert cause.remediation.remedy is Remedy.RUN_SETUP
    assert any("--db-path" in step for step in cause.remediation.steps)
    assert cause.detail["path"] == str(bench.db_path)
    assert cause.detail["size"] == 0
    assert bench.db_path.read_bytes() == b""
    # Measured on the copy, and refused before anything was opened at all.
    assert len(measured) == 1
    assert measured[0].parent.name.startswith("cratekit-copy-"), measured
    assert not measured[0].exists()
    assert opened == []


def test_the_copy_names_a_file_holding_none_of_the_canary_tables(bench, opened):
    bench.db_path.unlink()
    _foreign(bench.db_path)
    size = bench.db_path.stat().st_size
    before = bench.digest()

    cause = _refusal_from_the_copy(bench.db_path, bench.cfg).cause

    assert cause.reason == "library-database-not-rekordbox"
    assert f"{size} bytes" in cause.message
    assert "holds none of the tables" in cause.message
    assert str(bench.db_path) in cause.message
    assert "no such table" not in cause.message
    assert cause.detail["size"] == size
    assert cause.remediation.remedy is Remedy.RUN_SETUP
    assert bench.digest() == before
    _never_the_live_path(opened, bench.db_path)


@pytest.mark.parametrize("present", rb_writer.CANARY_TABLES)
def test_a_file_holding_one_canary_table_is_drift_and_keeps_the_canarys_refusal(
    bench, present
):
    bench.db_path.unlink()
    _foreign(bench.db_path, tables=(present,))

    cause = _refusal_from_the_copy(bench.db_path, bench.cfg).cause

    assert cause.reason == "canary-read-failed"


def test_a_file_that_is_not_sqlite_at_all_keeps_the_canarys_refusal(bench):
    bench.db_path.write_bytes(b"not a database at all, and long enough to matter" * 40)

    cause = _refusal_from_the_copy(bench.db_path, bench.cfg).cause

    assert cause.reason == "canary-read-failed"


@pytest.mark.parametrize("make", [_empty, _foreign], ids=["empty", "foreign"])
def test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing(
    bench, opened, monkeypatch, make
):
    """Sitting 5 through the real dispatcher: the wrong file one directory over."""
    wrong = make(bench.root / "PIONEER" / "rekordbox" / "master.db")
    live_bytes = bench.db_path.read_bytes()
    asked: list[str] = []

    def read_line() -> str:
        asked.append("asked")
        return "no\n"

    monkeypatch.setattr(
        prompt,
        "Prompter",
        lambda: _RealPrompter(read_line=read_line, read_secret=lambda _q: "", write=lambda _t: None),
    )

    code, envelope = drive(["setup", "--db-path", str(wrong)])

    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "library-database-not-rekordbox"
    assert str(wrong) in envelope["cause"]["message"]
    assert "bytes" in envelope["cause"]["message"]
    config.reset_cache()
    assert Path(config.load().library.db_path) == bench.db_path
    # Refused before the pin and the drive rule were offered: the one answer
    # read is the backup offer that comes ahead of the validation.
    assert len(asked) <= 1
    assert bench.db_path.read_bytes() == live_bytes
    # An empty copy is refused before any open; a foreign one is opened, and
    # only ever as a copy.
    assert (opened == []) is (make is _empty)
    assert wrong not in opened
    for path in opened:
        assert path.parent.name.startswith("cratekit-copy-"), path


def test_setup_leaves_a_missing_file_to_the_notes_and_takes_no_copy(bench, opened):
    bench.db_path.unlink()
    setup_verb._refuse_a_database_that_is_not_one(bench.cfg)
    assert opened == []


def test_setup_takes_no_copy_of_a_wrong_file_while_rekordbox_is_running(
    bench, opened, monkeypatch
):
    _empty(bench.db_path)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    setup_verb._refuse_a_database_that_is_not_one(bench.cfg)
    assert opened == []


def test_setup_leaves_a_damaged_library_to_the_notes_and_doctor(bench, opened):
    bench.db_path.write_bytes(b"not a database at all, and long enough to matter" * 40)
    assert setup_verb._refuse_a_database_that_is_not_one(bench.cfg) is None
    _never_the_live_path(opened, bench.db_path)


@pytest.mark.parametrize("make", [_empty, _foreign], ids=["empty", "foreign"])
def test_the_file_whose_tables_are_listed_is_only_ever_a_copy(bench, monkeypatch, make):
    """The table listing opens its own handle, beside ``open_db`` rather than
    through it, so the spy on the opener cannot see it and this one can."""
    bench.db_path.unlink()
    make(bench.db_path)
    listed: list[Path] = []
    real = rb_writer._copy_tables

    def spy(copied):
        listed.append(Path(copied))
        return real(copied)

    monkeypatch.setattr(rb_writer, "_copy_tables", spy)
    from pyrekordbox import Rekordbox6Database

    constructed: list[Path] = []

    class Watched(Rekordbox6Database):
        def __init__(self, *args, path=None, **kwargs):
            constructed.append(Path(path))
            super().__init__(*args, path=path, **kwargs)

    import pyrekordbox

    monkeypatch.setattr(pyrekordbox, "Rekordbox6Database", Watched)

    _refusal_from_the_copy(bench.db_path, bench.cfg)

    assert (constructed == []) is (make is _empty)
    assert bench.db_path not in constructed
    assert bench.db_path not in listed
    for path in constructed + listed:
        assert path.parent.name.startswith("cratekit-copy-"), path
    # An empty copy is refused before any open at all; a foreign one is listed.
    assert (listed == []) is (make is _empty)


def test_doctor_reports_an_empty_database_path_under_the_same_cause(bench, opened):
    _empty(bench.db_path)

    finding = next(
        f
        for f in doctor.run(bench.cfg, probes=_real_survey()).findings
        if f.key == "library.paths_resolved"
    )

    assert finding.status is doctor.Status.FAIL
    assert finding.cause is not None
    assert finding.cause.reason == "library-database-not-rekordbox"
    assert finding.remedy is Remedy.RUN_SETUP
    assert "is empty, 0 bytes" in finding.detail
    assert str(bench.db_path) in finding.detail
    assert "no such table" not in finding.detail
    assert opened == []


def test_a_refusal_on_the_way_in_is_not_reclassified_as_a_wrong_path(bench, monkeypatch):
    """Only the canary's own failure is asked whether the copy is a library.

    A binding pin that refuses is a fact about this installation, true of every
    file, and a foreign file behind it must still be answered with the pin.
    """
    bench.db_path.unlink()
    _foreign(bench.db_path)

    def drifted(_cfg=None):
        raise rb_writer._unavailable("pyrekordbox-pin-drift", "the binding is not the pinned one")

    monkeypatch.setattr(rb_writer, "assert_binding_version", drifted)

    cause = _refusal_from_the_copy(bench.db_path, bench.cfg).cause

    assert cause.reason == "pyrekordbox-pin-drift"
