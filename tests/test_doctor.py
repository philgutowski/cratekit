"""U27: the setup wizard, the doctor, and the two reports beside them.

Each part guards a way this unit could be green and wrong: the check table is complete
and ordered, the derived families really are derived (P4), the brief's scenarios run
through the real checks, the wizard never overwrites what it cannot read, ``crate
login`` takes no credential as an argument, and each guard meets its evasion.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import copy
import dataclasses
import errno
import io
import json
import os
import pathlib
import select
import shlex
import shutil
import sqlite3
import subprocess
import sys
import time
import tomllib
import types
from datetime import datetime, timedelta, timezone
from importlib import metadata as importlib_metadata
from pathlib import Path
from types import SimpleNamespace

import keyring
import pytest

from cratekit import acquire, cli
from cratekit.acquire import adapter as adapter_contract
from cratekit.analysis import vocals
from cratekit.cli import (
    doctor,
    doctor_backup,
    doctor_keys,
    doctor_library,
    doctor_model,
    doctor_state,
    gates,
    output,
    prompt,
    registry,
    render,
)
from cratekit.cli import jobs as jobs_cli
from cratekit.cli import setup as setup_verb
from cratekit.cli.doctor import Probes as RealProbes
from cratekit.cli.verbs import login as login_verb
from cratekit.core import (
    backup_facts,
    binaries,
    config,
    jobs,
    preflight,
    profiles,
    rb_writer,
    secrets,
    session,
    snapshot,
    taxonomy,
    tree_registry,
)
from cratekit.core import cause as cause_module
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.deletion import trash
from cratekit.write import metadata_cli
from tests import doctor_machines
from tests._hardware import filesystem_kind, hdiutil_available, read_only_volume
from tests.test_active_taxonomy import shipped_without, write_active
from tests.test_cli_contract import INTERACTIVE_ALLOWLIST
from tests.test_session_log_unlisted import _refuse_listing
from tests.test_taxonomy_upgrade import live_shaped

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

#: Shared with ``doctor_machines`` so both suites describe one disk; synthetic (R1).
VOLUME = doctor_machines.VOLUME

OK, FAIL, INFO = doctor.Status.OK, doctor.Status.FAIL, doctor.Status.INFO


# ═══ Fixtures ═══════════════════════════════════════════════════════════════


def document_for(root: Path, **library_overrides) -> dict:
    """The smallest configuration that validates, against a synthetic library."""
    library = {"root": str(root), "volume_id": VOLUME, "db_path": str(root / "db" / "master.db")}
    library.update(library_overrides)
    return {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": library,
        "paths": {"download_staging": str(root.parent / "staging")},
        "profile": {"name": "full"},
        "rekordbox": {"pinned_app_version": "7.0.1", "validated_on": "2026-08-01"},
    }


@pytest.fixture(autouse=True)
def _trap_standard_input(monkeypatch):
    """No test may reach a real terminal: under ``pytest -s`` a read would hang, not fail."""

    class Trapped:
        def __getattr__(self, name):
            raise AssertionError(f"a test in this file read standard input (sys.stdin.{name})")
    monkeypatch.setattr(sys, "stdin", Trapped())
    monkeypatch.setattr(
        "builtins.input",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("a test called input()")))


def fresh_root(tmp_path: Path, monkeypatch, *parts: str) -> Path:
    """A synthetic library root at ``tmp_path / parts`` with its Music folder, set as the root."""
    root = tmp_path.joinpath(*parts)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def library(tmp_path, monkeypatch):
    """A synthetic library root, re-set over the suite-wide override (P2)."""
    return fresh_root(tmp_path, monkeypatch, "library")


@pytest.fixture
def configured(library):
    cfg = config.from_dict(document_for(library))
    config.save(cfg)
    config.reset_cache()
    return config.load()


def probes(**overrides) -> doctor.Probes:
    """A green machine minus ``overrides``, shared with the conformance suite."""
    return doctor_machines.green(**overrides)


def seed_taxonomy(cfg: config.Config) -> None:
    path = config.state_path("taxonomy_active", cfg)
    config.atomic_write_bytes(setup_verb.template_text("default").encode("utf-8"), path)


def find(report: doctor.Report, key: str) -> doctor.Finding:
    return next(finding for finding in report.findings if finding.key == key)


def report_on(where=None, **overrides) -> doctor.Report:
    """A run on a config, a document or a library root, on ``probes(**overrides)``."""
    if isinstance(where, Path):
        where = document_for(where)
    if isinstance(where, dict):
        where = config.from_dict(where)
    return doctor.run(where, probes=probes(**overrides))


def finding_on(where, key: str, **overrides) -> doctor.Finding:
    return find(report_on(where, **overrides), key)


def checked(finding: doctor.Finding, status: doctor.Status, remedy=...) -> doctor.Finding:
    """``finding``, asserted to answer ``status`` and, when one is named, ``remedy``."""
    assert finding.status is status, finding.detail
    if remedy is not ...:
        assert finding.remedy is remedy, finding.remedy
    return finding


#: A configuration naming a library root at ``/tmp/x``, which nothing here mounts.
LIBRARY_AT_X = 'schema_version = 1\n[library]\nroot = "/tmp/x"\n'


def _isolated_config(tmp_path: Path, monkeypatch) -> None:
    """A config directory and a state root of the test's own, the cache cleared."""
    cfg_dir = made(tmp_path / "cfg")
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(cfg_dir))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "state"))
    config.reset_cache()


def isolated_library(tmp_path: Path, monkeypatch, *, save: bool = False) -> config.Config:
    """A config directory, a state root and a library root of the test's own."""
    _isolated_config(tmp_path, monkeypatch)
    cfg = config.from_dict(document_for(fresh_root(tmp_path, monkeypatch, "library")))
    if save:
        config.save(cfg)
        config.reset_cache()
    return cfg


def caught(kind: type[BaseException], call, void: str) -> BaseException:
    """The ``kind`` ``call`` raises; ``void`` says why the arrangement fails if it raises none."""
    try:
        call()
    except kind as exc:
        return exc
    raise AssertionError(void)


def made(path: Path, *, parents: bool = False) -> Path:
    path.mkdir(parents=parents)
    return path


def planted(path: Path, data: str | bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    (path.write_bytes if isinstance(data, bytes) else path.write_text)(data)
    return path


def _config_file(tmp_path: Path, monkeypatch, text: str = LIBRARY_AT_X) -> Path:
    _isolated_config(tmp_path, monkeypatch)
    path = planted(config.config_path(), text)
    return path


@contextlib.contextmanager
def _sealed(*paths: Path, mode: int = 0o000, reset_config: bool = False):
    """Each path set to a real ``mode``, 0o000 unless named, restored however the test ends."""
    before = [path.stat().st_mode & 0o777 for path in paths]
    for path in paths:
        path.chmod(mode)
    try:
        yield paths[0]
    finally:
        for path, kept in zip(paths, before):
            path.chmod(kept)
        if reset_config:
            config.reset_cache()


def _archive_remote(configured: config.Config) -> config.Config:
    """``configured``'s library with its backup remote set to ``archive:``."""
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:"}
    return config.from_dict(document)


#: A machine whose library volume is mounted nowhere.
UNMOUNTED = {"identity_provider": lambda _p: "0000-0000", "mount_enumerator": lambda: ()}

#: The slim preset, for the profile section of a document.
SLIM = {"name": "slim"}


def mounted_at(where: Path) -> dict:
    """Probe overrides for a library volume mounted at ``where`` instead of its root."""
    return {
        "identity_provider": lambda path: VOLUME if path == where else "0000-0000",
        "mount_enumerator": lambda: (where,),
    }


def mount_state(cfg: config.Config, machine: doctor.Probes) -> preflight.MountStatus:
    return preflight.resolve_mount_state(
        cfg.library.root, cfg.library.volume_id,
        identity_provider=machine.identity_provider, mount_enumerator=machine.mount_enumerator)


def lacking(missing: str):
    return lambda name: None if name == missing else f"/bin/{name}"


def green_probes(monkeypatch, **overrides) -> None:
    """Every ``doctor.Probes()`` a verb builds answers as ``probes(**overrides)``."""
    monkeypatch.setattr(doctor, "Probes", lambda: probes(**overrides))


def document_with(root: Path, **sections) -> dict:
    """``document_for(root)`` with each named top level section replaced by a copy."""
    return {**document_for(root), **copy.deepcopy(sections)}


def seeded(cfg: config.Config, machine: doctor.Probes | None = None) -> setup_verb._Wizard:
    """A wizard that has run the taxonomy seed on ``cfg``, over a green machine by default."""
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, cfg, machine or probes())
    return wizard


def seed_note(wizard: setup_verb._Wizard) -> doctor.Finding:
    return next(n for n in wizard.notes if n.key == "setup.taxonomy")


def derive(root, identity: str, wizard: setup_verb._Wizard | None = None) -> str:
    """The identity setup derives for ``root`` on a machine whose volumes answer ``identity``."""
    wizard = wizard or setup_verb._Wizard({}, silent())
    machine = probes(identity_provider=lambda _p: identity)
    return setup_verb._resolve_volume_id(wizard, str(root), None, machine)


def refusal(call, *args, **kwargs) -> Cause:
    """The cause ``call(*args, **kwargs)`` refuses with, which it must."""
    with pytest.raises(CratekitError) as excinfo:
        call(*args, **kwargs)
    return excinfo.value.cause


def refused_derive(root, identity: str = "BOOT-DISK") -> Cause:
    """The cause setup's derive refuses ``root`` with, on a machine answering ``identity``."""
    return refusal(derive, root, identity)


#: A committed session nobody has verified, which only a restore answers.
UNVERIFIED = session.SessionState.COMMITTED_UNVERIFIED

FILES, DATABASE = backup_facts.Portion.FILES, backup_facts.Portion.DATABASE


def backed_up(cfg: config.Config, portion, at: datetime, destination: str = "remote:backups"):
    backup_facts.record(cfg, portion, completed_at=at, destination=destination)


def write_session(cfg: config.Config, session_id: str = "s-2", **fields) -> None:
    fields.setdefault("workflow", "sync.labels")
    record = session.SessionRecord(session_id, started="2026-08-02T00:00:00+00:00", **fields)
    session.write_record(record, cfg)


def root_volume_refusal(name: str) -> OSError:
    """What a mkdir of ``/name`` meets on this machine's read only system volume."""
    try:
        os.mkdir(f"/{name}")
    except OSError as exc:
        return exc
    else:  # pragma: no cover - only on a machine with a writable root volume
        os.rmdir(f"/{name}")
        raise AssertionError("this machine's root volume is writable, so it proves nothing")


def a_finding(**fields) -> doctor.Finding:
    """A failing finding about the active template, ``fields`` replacing its defaults."""
    defaults = {"key": "setup.taxonomy", "title": "active taxonomy template", "status": FAIL}
    return doctor.Finding(**{**defaults, **fields})


def drive(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def setup_argv(root: str, tmp_path: Path, *flags: str) -> list[str]:
    """``crate --output json setup`` at ``root`` with ``flags``, slim, default taxonomy."""
    return [
        "--output", "json", "setup",
        "--library-root", root,
        *flags,
        "--staging", str(tmp_path / "staging"),
        "--profile", "slim",
        "--taxonomy", "default",
    ]


def login_from(holder: Path) -> tuple[int, str, str]:
    return drive(["--output", "json", "login", "provider-session", "--from-file", str(holder)])


def setup_at(root: Path, tmp_path: Path) -> tuple[int, str, str]:
    """Setup driven at ``root`` with its database under it and the recorded volume supplied."""
    db = str(root / "db" / "master.db")
    return drive(setup_argv(str(root), tmp_path, "--db-path", db, "--volume-id", VOLUME))


# ═══ 1. The check table ═════════════════════════════════════════════════════


def test_every_run_answers_every_declared_check_in_the_declared_order(configured):
    """Every key, every run, in order, so reports diff and no check quietly disappears."""
    report = report_on(configured)
    assert tuple(f.key for f in report.findings) == doctor.CHECK_KEYS
    assert len(set(doctor.CHECK_KEYS)) == len(doctor.CHECK_KEYS), "a key is declared twice"


def test_the_interpreter_is_checked_before_anything_else():
    """Nothing below the interpreter means anything on one the tree cannot run on."""
    assert doctor.CHECK_KEYS[0] == "interpreter.version"


def test_every_check_key_and_its_place_in_the_run_order_is_written_out():
    """The whole table spelled out, so dropping, renaming or reordering a check fails."""
    assert doctor.CHECK_KEYS == (
        "interpreter.version", "config.present", "library.mounted", "library.identity",
        "library.db_containment", "library.trash", "taxonomy.active", "taxonomy.schema",
        "rekordbox.closed", "rekordbox.pins", "library.paths_resolved", "keychain.reachable",
        "credential.bandcamp", "credential.catalogue", "credential.cyanite", "credential.discogs",
        "credential.provider", "credential.recognition",
        *(f"binary.{name}" for name in doctor.BINARY_NAMES), "adapter.contract",
        *(f"backup.age.{portion}" for portion in backup_facts.PORTIONS), "backup.acknowledgment",
        "backup.full_comparison", "backup.full_check", "backup.remote", "deadca7.push",
        "session.unresolved", "runs.open-gates", "provider.isrc-cache", "provider.budget",
        "sync.night", "tree.registry", "repo.commit_hook", "install.extras", "install.release",
    )
    platform = sorted(binaries.PLATFORM_BINARIES)
    assert doctor.BINARY_NAMES == (*binaries.INSTALLABLE_BINARIES, *platform)


def test_doctor_never_raises_when_there_is_no_configuration_at_all(tmp_path, monkeypatch):
    """Downstream of a missing config everything reads unchecked, so the one failure shows."""
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "empty"))
    config.reset_cache()
    report = report_on()
    assert tuple(f.key for f in report.findings) == doctor.CHECK_KEYS
    checked(find(report, "config.present"), FAIL, Remedy.RUN_SETUP)
    assert find(report, "library.mounted").status is INFO
    assert "not checked" in find(report, "library.mounted").detail


def test_a_configuration_from_a_newer_build_keeps_its_own_remedy(tmp_path, monkeypatch):
    """Each way a config can be unusable keeps its own remedy, not the class default."""
    _isolated_config(tmp_path, monkeypatch)
    config.config_path().write_text(f"schema_version = {config.CURRENT_SCHEMA_VERSION + 5}\n")
    checked(finding_on(None, "config.present"), FAIL, Remedy.UPGRADE_CRATEKIT)


# ═══ 2. The derived families ═══════════════════════════════════════════════


def test_every_stored_credential_is_covered_by_exactly_one_check():
    """A derivation that misses one credential leaves it silently unchecked (P4)."""
    covered = [name for names in doctor.CREDENTIALS_BY_CHECK.values() for name in names]
    assert sorted(str(n) for n in covered) == sorted(str(n) for n in secrets.Credential)
    assert len(covered) == len(set(covered)), "one credential is claimed by two checks"


def test_every_credential_check_the_registry_declares_has_a_group_and_a_remedy():
    checks = (key for entry in registry.entries() for key in entry.doctor_checks)
    declared = {key for key in checks if key.startswith("credential.")}
    assert declared <= set(doctor.CREDENTIALS_BY_CHECK)
    for key in doctor.CREDENTIALS_BY_CHECK:
        assert f"binary.{key}" not in doctor.CHECK_KEYS
        assert isinstance(Remedy(str(doctor_keys._CREDENTIAL_REMEDY[key])), Remedy)


def test_every_binary_the_resolver_knows_about_is_probed():
    """Both ``core/binaries`` tables are expanded, so a new binary is checked at once (P3)."""
    probed = {key[len("binary.") :] for key in doctor.CHECK_KEYS if key.startswith("binary.")}
    assert probed == set(binaries.INSTALLABLE_BINARIES) | set(binaries.PLATFORM_BINARIES)


def test_the_acquisition_contract_is_read_off_the_protocol():
    """Asserted against the protocol, so a member added to it is checked without an edit."""
    assert doctor.contract_members() == ("acquire", "name")

    class Grown(adapter_contract.AcquisitionAdapter):
        capabilities: tuple[str, ...]

        def reset(self) -> None: ...
    assert set(doctor.contract_members(Grown)) >= {"capabilities", "reset"}


def test_every_backup_portion_gets_its_own_answer():
    """One aggregate age would call "files current, database stale" protected."""
    reported = {key for key in doctor.CHECK_KEYS if key.startswith("backup.age.")}
    assert reported == {f"backup.age.{portion}" for portion in backup_facts.PORTIONS}


# ═══ 3. The five scenarios in the brief ═════════════════════════════════════


def test_an_unmounted_volume_and_a_moved_volume_produce_different_messages(tmp_path, monkeypatch):
    """Not mounted says attach the disk; moved says it is attached elsewhere."""
    absent = tmp_path / "not-mounted"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(absent))
    unmounted = report_on(absent, **UNMOUNTED)
    elsewhere_root = fresh_root(tmp_path, monkeypatch, "configured")
    actually_at = made(tmp_path / "actually-here")
    moved = report_on(elsewhere_root, **mounted_at(actually_at))
    first = find(unmounted, "library.mounted")
    second = find(moved, "library.mounted")
    assert first.status is FAIL and second.status is FAIL
    assert first.detail != second.detail
    assert "not mounted anywhere" in first.detail
    assert "different mount point" in second.detail and str(actually_at) in second.detail


def test_a_foreign_volume_at_the_configured_root_is_its_own_answer(library):
    """A restored clone at the root is its own answer, since a directory check says yes."""
    report = report_on(library, identity_provider=lambda _p: "9999-9999")
    identity = checked(find(report, "library.identity"), FAIL, Remedy.MOUNT_LIBRARY_VOLUME)
    assert "9999-9999" in identity.detail and VOLUME in identity.detail


def test_a_module_enabled_without_its_credential_is_reported_with_the_fix(library):
    """The same missing credential fails with ``identify`` on and is a note with it off."""
    missing = probes(credential_recorded=lambda name: name != str(secrets.Credential.IDENTIFY_KEY))
    on = doctor.run(config.from_dict(document_for(library)), probes=missing)
    finding = checked(find(on, "credential.recognition"), FAIL, Remedy.SET_CREDENTIAL)
    assert render.remedy_text(finding.remedy), "the fix must render to something"
    off = doctor.run(config.from_dict(document_with(library, profile=SLIM)), probes=missing)
    assert find(off, "credential.recognition").status is INFO


def _break_the_presence_index(monkeypatch) -> Path:
    """Leave a credential recorded and the index unreadable, through the real reader."""
    secrets.set(secrets.Credential.PROVIDER_SESSION, "value-from-the-user")
    index = config.state_path("credential_index")
    real = Path.read_text

    def refuse(self, *args, **kwargs):
        if self == index:
            raise PermissionError(13, "Permission denied", str(index))
        return real(self, *args, **kwargs)
    monkeypatch.setattr(Path, "read_text", refuse)
    return index


def test_an_unreadable_credential_index_is_reported_as_unread_not_as_unrecorded(
        library, monkeypatch):
    """An unreadable index is unread, not "not recorded": recording again never fixes it (R-116)."""
    index = _break_the_presence_index(monkeypatch)
    finding = finding_on(library, "credential.provider", credential_recorded=secrets.exists)
    checked(finding, FAIL, Remedy.GRANT_PATH_ACCESS)
    assert str(index) in finding.detail
    assert "not recorded" not in finding.detail
    assert finding.remedy is not Remedy.AUTHENTICATE_PROVIDER
    assert render.remedy_text(finding.remedy), "the fix must render to something"


def test_an_unreadable_credential_index_costs_one_check_and_not_the_report(library, monkeypatch):
    """Every other check still answers, so the report's length stays fixed."""
    _break_the_presence_index(monkeypatch)
    keys = {f.key for f in report_on(library, credential_recorded=secrets.exists).findings}
    green = {f.key for f in report_on(library).findings}
    assert keys == green


def test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying(configured, monkeypatch):
    """Credentials are captured after the config is saved, so a raise would lose the report."""
    index = _break_the_presence_index(monkeypatch)
    wizard = setup_verb._Wizard({}, Scripted(["yes", "yes", "yes"], ["k3y", "s1gn", "s3cret"]))
    setup_verb._capture_credentials(wizard, configured)
    offered = [note for note in wizard.notes if note.key.startswith("setup.credential.")]
    assert offered, "no credential was reported, so nothing here was exercised"
    broken = [note for note in offered if note.status is FAIL]
    assert broken, "an unanswerable presence question was not reported at all"
    assert all(str(index) in note.detail for note in broken)
    assert all(note.remedy is Remedy.GRANT_PATH_ACCESS for note in broken)


def test_the_wizard_notes_an_index_that_refuses_the_write_rather_than_dying(
        configured, monkeypatch):
    """An index damaged while the secret is typed is noted: ``CredentialError`` is no refusal."""
    index = config.state_path("credential_index")
    answers = ["yes", "yes", "yes"]
    held = ["k3y", "s1gn", "s3cret"]

    def read_secret(_question):
        planted(index, "{not json at all")
        return held.pop(0) if held else _eof()
    scripted = prompt.Prompter(
        read_line=lambda: (answers.pop(0) + "\n") if answers else _eof(), read_secret=read_secret,
        write=lambda _text: None)
    wizard = setup_verb._Wizard({}, scripted)
    setup_verb._capture_credentials(wizard, configured)
    offered = [note for note in wizard.notes if note.key.startswith("setup.credential.")]
    assert offered, "no credential was reported, so nothing here was exercised"
    assert all(note.status is FAIL for note in offered)
    assert all(str(index) in note.detail for note in offered)
    assert all(note.remedy is Remedy.REPAIR_CREDENTIAL_STORE for note in offered)
    rendered = json.dumps([note.to_json() for note in wizard.notes])
    for value in ("k3y", "s1gn", "s3cret"):
        assert value not in rendered


def test_a_missing_binary_is_reported_with_where_it_comes_from(library):
    """A missing binary is reported before any spend, not part way through a paid download."""
    finding = finding_on(library, "binary.ffmpeg", find_binary=lacking("ffmpeg"))
    checked(finding, FAIL, Remedy.INSTALL_BINARY)
    assert binaries.env_var("ffmpeg") in finding.detail


def test_a_missing_ffmpeg_names_the_analysis_whose_decoder_it_is(library):
    """U263: with analysis on, a missing ffmpeg names the verbs it stops (M4A decodes by it)."""
    document = document_with(library, profile=SLIM, modules={"analysis": True})
    finding = checked(finding_on(document, "binary.ffmpeg", find_binary=lacking("ffmpeg")), FAIL)
    for verb in ("analyze run", "analyze restamp", "analyze calibrate"):
        assert verb in finding.detail, finding.detail
    for entry in ("analyze.run", "analyze.restamp", "analyze.calibrate", "analyze.vocals"):
        assert "binary.ffmpeg" in registry.entry(entry).doctor_checks, entry


def test_a_binary_no_enabled_verb_needs_is_a_note_rather_than_a_failure(library):
    """A binary only a disabled module needs is a note: red that is no problem is ignored (P7)."""
    report = report_on(document_with(library, profile=SLIM), find_binary=lacking("rclone"))
    assert find(report, "binary.rclone").status is INFO
    assert "no verb this profile switches on" in find(report, "binary.rclone").detail


def test_doctor_verifies_the_configured_adapter_against_the_contract(library):
    """A substitute adapter is checked at configuration, not at the first download (R9)."""
    streamrip = document_with(library, acquisition={"adapter": "streamrip"})
    ok = finding_on(streamrip, "adapter.contract")
    assert "streamrip" in checked(ok, OK).detail
    unknown = document_with(library, acquisition={"adapter": "not-a-real-adapter"})
    checked(finding_on(unknown, "adapter.contract"), FAIL, Remedy.CHOOSE_KNOWN_ADAPTER)


def test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check(library):
    """U197: the retired vendored key is folded on read, so the check passes with the new key."""
    document = document_with(library, acquisition={"adapter": "tidal_dl_ng"})
    finding = checked(finding_on(document, "adapter.contract"), OK)
    assert "'vendored'" in finding.detail
    assert "tidal_dl_ng" not in finding.detail


def test_an_adapter_whose_name_disagrees_with_the_configuration_is_refused(library, monkeypatch):
    """Two names for one adapter would report work against an adapter nobody chose."""

    class Impostor:
        name = "something-else"

        def acquire(self, requests):  # pragma: no cover - never called
            raise NotImplementedError
    monkeypatch.setattr("cratekit.acquire.load", lambda _name: Impostor)
    checked(finding_on(library, "adapter.contract"), FAIL, Remedy.SWITCH_ADAPTER)


def test_an_adapter_missing_a_contract_member_is_refused(library, monkeypatch):
    class Partial:
        name = "vendored"
    monkeypatch.setattr("cratekit.acquire.load", lambda _name: Partial)
    finding = checked(finding_on(library, "adapter.contract"), FAIL)
    assert "acquire" in finding.detail


# ── the interpreter bound ────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "version, specifier, expected",
    [
        ((3, 12, 4), ">=3.12,<3.14", True),
        ((3, 13, 0), ">=3.12,<3.14", True),
        ((3, 14, 0), ">=3.12,<3.14", False),
        ((3, 11, 9), ">=3.12,<3.14", False),
        ((3, 12), ">=3.12", True),
        ((3, 12, 1), "==3.12.1", True),
        ((3, 12, 1), "!=3.12.1", False),
        ((3, 12, 1), "~=3.12", None),
        ((3, 12, 1), ">=3.12.*", None),
        # A specifier with no clause compares nothing, so it answers nothing.
        ((3, 12, 1), "", None),
        ((3, 12, 1), "   ", None),
        ((3, 12, 1), ",,", None),
        # A bound that compares still answers, even with one meaningful clause.
        ((3, 12, 1), ">=3.12,", True),
    ])
def test_the_interpreter_specifier_parser_answers_or_says_it_cannot(version, specifier, expected):
    """An unknown specifier shape answers None ("not asserted"), never a guessed pass."""
    assert doctor.satisfies(version, specifier) is expected


def test_a_specifier_that_compares_nothing_is_not_a_pass():
    """A specifier the loop walks without a comparison must not fall through to True."""
    for specifier in ("", "   ", ",", " , ", "\t"):
        assert doctor.satisfies((3, 12, 5), specifier) is None, specifier


def test_an_unsupported_interpreter_fails_and_an_unreadable_bound_does_not(library):
    outside = finding_on(library, "interpreter.version", python_version=(3, 14, 0))
    checked(outside, FAIL, Remedy.UNSUPPORTED_PLATFORM)
    checked(finding_on(library, "interpreter.version", requires_python=None), INFO)


def test_the_declared_bound_is_read_from_packaging_rather_than_repeated():
    """KTD19's bound is read from packaging, not copied into doctor."""
    declared = (REPO_ROOT / "pyproject.toml").read_text()
    cli_dir = SRC_ROOT / "cratekit" / "cli"
    sources = {path.name: path.read_text() for path in cli_dir.glob("doctor*.py")}
    assert {"doctor.py", "doctor_library.py", "doctor_model.py"} <= set(sources)
    for bound in (">=3.12", "<3.14"):
        assert bound in declared
        for name, source in sources.items():
            assert bound not in source, name


# ── the pins, the processes, the sessions ────────────────────────────────────


def test_an_unrecorded_application_pin_fails_and_names_the_installed_version(library):
    """S2: an unset pin refuses every database write, so doctor says so every run."""
    finding = finding_on(document_with(library, rekordbox={}), "rekordbox.pins")
    checked(finding, FAIL, Remedy.RECORD_REKORDBOX_PIN)
    assert "7.0.1" in finding.detail


def test_a_drifted_application_pin_is_a_different_answer_from_an_unset_one(library):
    finding = finding_on(library, "rekordbox.pins", installed_app_version=lambda _cfg: "8.0.0")
    checked(finding, FAIL, Remedy.REVALIDATE_PINS)
    assert "frozen by design" in finding.detail


def test_a_pin_that_was_never_confirmed_against_a_write_is_reported(library):
    document = document_with(library, rekordbox={"pinned_app_version": "7.0.1"})
    finding = checked(finding_on(document, "rekordbox.pins"), INFO)
    assert "a number somebody typed" in finding.detail


def test_a_running_rekordbox_agent_is_reported_even_with_the_window_closed(library):
    agent = ("rekordboxAgent.exe",)
    finding = finding_on(library, "rekordbox.closed", process_lister=lambda: agent)
    checked(finding, FAIL, Remedy.QUIT_REKORDBOX)
    assert "rekordboxAgent" in finding.detail


def test_a_committed_unverified_session_is_reported_before_the_next_write(configured):
    """The log survives a rollback, so doctor shows the session until a restore answers it."""
    write_session(configured, "s-1", workflow="route.inbox", state=UNVERIFIED)
    finding = finding_on(configured, "session.unresolved")
    checked(finding, FAIL, Remedy.RESTORE_FROM_SNAPSHOT)
    assert "s-1" in finding.detail


def test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it(configured):
    """R-598: a record a hard kill left is not a run in progress; the live record is the control."""
    finished = subprocess.Popen([sys.executable, "-c", "pass"])
    finished.wait()
    here = session.current_holder()
    gone = session.Holder(host=here.host, boot=here.boot, pid=finished.pid, started="1.000")
    orphan = session.open_session(configured, workflow="w", session_id="s-dead", holder=gone)
    live = session.open_session(configured, workflow="w", session_id="s-live", holder=here)
    finding = checked(finding_on(configured, "session.unresolved"), INFO)
    gone_line = f"{orphan.session_id} (open, its process is gone, crate session release"
    assert gone_line in finding.detail
    assert f"{live.session_id} (open)" in finding.detail


def test_an_unreadable_session_record_is_reported_rather_than_dropped(configured):
    """A tolerant reader would fail open, so doctor reports the half that refuses."""
    log = session.log_dir(configured)
    planted(log / "wrecked.json", "{not json")
    finding = checked(finding_on(configured, "session.unresolved"), FAIL)
    assert "wrecked.json" in finding.detail


def test_a_backup_recorded_in_the_future_is_refused_rather_than_treated_as_fresh(configured):
    """A negative age would satisfy every freshness check, so it is refused."""
    backed_up(configured, FILES, datetime(2026, 9, 1, tzinfo=timezone.utc), "somewhere")
    checked(finding_on(configured, "backup.age.files"), FAIL, Remedy.REPAIR_BACKUP_FACTS)


def test_a_recorded_backup_reports_its_age_and_its_destination(configured):
    at = datetime(2026, 8, 2, tzinfo=timezone.utc) - timedelta(days=9)
    backed_up(configured, DATABASE, at, "a-remote:bucket")
    finding = checked(finding_on(configured, "backup.age.database"), INFO)
    assert "9 days ago" in finding.detail and "a-remote:bucket" in finding.detail


#: U184: one clock, so "valid" and "expired" are measured against doctor's instant.
ACK_NOW = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)


def _acknowledged(cfg: config.Config, at: datetime) -> session.Acknowledgment:
    """An acknowledgment minted at ``at`` by the session rule, over young backups."""
    for portion in backup_facts.Portion:
        backed_up(cfg, portion, at - timedelta(days=1), "probe")
    return session.record_acknowledgment(cfg, now=at, decided_by=session.SESSION_ACTOR)


def test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages(configured):
    """U184: the third fact a destructive verb consults, after the two it was minted over."""
    minted = _acknowledged(configured, ACK_NOW - timedelta(hours=2, minutes=30))
    report = report_on(configured, now=ACK_NOW)
    finding = checked(find(report, "backup.acknowledgment"), INFO)
    expires = minted.expires_at.replace(microsecond=0).isoformat()
    said = f"valid until {expires}, 9h 30m from now, minted by the session-ages rule"
    assert finding.detail == said
    keys = [one.key for one in report.findings]
    ages = [keys.index(f"backup.age.{portion}") for portion in backup_facts.PORTIONS]
    assert keys.index("backup.acknowledgment") == max(ages) + 1


def test_doctor_names_when_an_acknowledgment_lapsed(configured):
    minted = _acknowledged(configured, ACK_NOW - timedelta(hours=13))
    finding = checked(finding_on(configured, "backup.acknowledgment", now=ACK_NOW), INFO)
    expires = minted.expires_at.replace(microsecond=0).isoformat()
    assert finding.detail.startswith(f"expired at {expires};"), finding.detail
    assert "crate session ack" in finding.detail


def test_doctor_says_when_no_acknowledgment_is_on_record(configured):
    finding = checked(finding_on(configured, "backup.acknowledgment"), INFO)
    assert finding.detail.startswith("none on record"), finding.detail


def test_an_acknowledgment_that_cannot_be_understood_is_a_failure(configured):
    planted(session.ack_path(configured), "{ not json")
    finding = finding_on(configured, "backup.acknowledgment")
    checked(finding, FAIL, Remedy.REPORT_DEFECT)
    assert "not readable as JSON" in finding.detail


def test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read(configured, tmp_path):
    """The record lives on the library volume, so a missing volume is not "none"."""
    _acknowledged(configured, ACK_NOW)
    configured.library.root.rename(tmp_path / "detached")
    finding = checked(finding_on(configured, "backup.acknowledgment", now=ACK_NOW), INFO)
    assert "not asserted" in finding.detail
    assert "none on record" not in finding.detail


def test_a_remote_whose_provider_trashes_on_delete_is_reported(configured):
    """A trashing provider is reported: a pruned archive would keep counting against the quota."""
    cfg = _archive_remote(configured)
    trashing = probes(rclone_remotes=lambda _r: {"archive": {"type": "drive"}})
    finding = checked(find(doctor.run(cfg, probes=trashing), "backup.remote"), FAIL)
    assert "use_trash" in finding.detail
    disabled = probes(
        rclone_remotes=lambda _r: {"archive": {"type": "drive", "use_trash": "false"}})
    assert find(doctor.run(cfg, probes=disabled), "backup.remote").status is OK


def test_a_backup_module_with_no_destination_is_a_note_rather_than_a_failure(library):
    """The full preset turns backup on for everyone, so failing paints a new install red (P7)."""
    checked(finding_on(library, "backup.remote"), INFO)


#: pre-commit's installed hook, reduced to the lines that decide its dispatch.
INSTALLED_HOOK = (
    "#!/usr/bin/env bash\n"
    "# File generated by pre-commit: https://pre-commit.com\n"
    "ARGS=(hook-impl --config=.pre-commit-config.yaml --hook-type=pre-commit)\n"
    'exec pre-commit "${ARGS[@]}"\n')


def _remote_finding(configured: config.Config, settings: dict, name: str = "archive"):
    """``backup.remote`` with the backup remote ``archive:`` and rclone's ``name`` set so."""
    return finding_on(
        _archive_remote(configured), "backup.remote", rclone_remotes=lambda _r: {name: settings})


def hooked_checkout(root: Path, body: str = INSTALLED_HOOK, *, config_file: bool = True):
    """A synthetic checkout with a git directory, a hook, and its configuration."""
    (root / ".git" / "hooks").mkdir(parents=True, exist_ok=True)
    (root / ".git" / "hooks" / "pre-commit").write_text(body)
    if config_file:
        (root / ".pre-commit-config.yaml").write_text("repos: []\n")
    return root


def hook_finding(library, checkout) -> doctor.Finding:
    return finding_on(library, "repo.commit_hook", checkout_root=lambda: checkout)


def test_the_commit_hook_check_says_nothing_on_an_installed_package(library):
    """The commit hook check is for developers, so an installed package hears nothing."""
    checked(finding_on(library, "repo.commit_hook"), INFO)
    bare = library / "checkout"
    (bare / ".git" / "hooks").mkdir(parents=True)
    missing = checked(hook_finding(library, bare), FAIL)
    assert "pre-commit install" in missing.detail
    checked(hook_finding(library, hooked_checkout(bare)), OK)


@pytest.mark.parametrize(
    "body, config_file, because",
    [
        # A hook that only mentions the word runs nothing.
        ("#!/bin/sh\n# pre-commit\nexit 0\n", True, "hook-impl"),
        # A hook installed for a different stage, copied into this file.
        (
            "ARGS=(hook-impl --config=.pre-commit-config.yaml --hook-type=pre-push)\n",
            True,
            "--hook-type=pre-commit",
        ),
        # A hook dispatching to another repository's configuration.
        (
            "ARGS=(hook-impl --config=/elsewhere/.pre-commit-config.yaml "
            "--hook-type=pre-commit)\n",
            True,
            "outside",
        ),
        # A hook naming a configuration this repository does not have.
        (
            "ARGS=(hook-impl --config=.pre-commit-other.yaml --hook-type=pre-commit)\n",
            False,
            "does not exist",
        ),
    ])
def test_a_hook_that_does_not_dispatch_to_this_repository_is_refused(
        library, tmp_path, body, config_file, because):
    """Each row passes a ``"pre-commit" in body`` test yet scans none of these commits."""
    checkout = hooked_checkout(tmp_path / "checkout", body, config_file=config_file)
    finding = checked(hook_finding(library, checkout), FAIL)
    assert because in finding.detail


def test_the_repositorys_own_installed_hook_passes_the_check(library):
    """This checkout's real hook passes, so the guard does not fire on a correct setup (P7)."""
    root = doctor_model._checkout_root()
    if root is None:  # pragma: no cover - an installed wheel has no checkout
        return
    git_dir, unreadable, _remedy = doctor_model._git_dir(root)
    assert unreadable is None, unreadable
    hook = git_dir / "hooks" / "pre-commit" if git_dir else None
    if hook is None or not hook.is_file():  # pragma: no cover - a clone with no hook
        return
    assert doctor_state._hook_dispatch_problem(hook.read_text(), root) is None


def _worktree(tmp_path: Path, commondir: bytes) -> tuple[Path, Path]:
    """A worktree ``w1`` of ``main``, its per-tree ``commondir`` holding ``commondir``."""
    common = tmp_path / "main" / ".git"
    (common / "hooks").mkdir(parents=True)
    per_tree = made(common / "worktrees" / "w1", parents=True)
    (per_tree / "commondir").write_bytes(commondir)
    worktree = made(tmp_path / "w1")
    (worktree / ".git").write_text(f"gitdir: {per_tree}\n")
    return worktree, common


def test_a_worktree_finds_the_hook_in_the_common_git_directory(tmp_path):
    """A worktree's ``.git`` leads to the common directory; one hop reports it unhooked (P7)."""
    worktree, common = _worktree(tmp_path, b"../..\n")
    (common / "hooks" / "pre-commit").write_text(INSTALLED_HOOK)
    assert doctor_model._git_dir(worktree) == (common.resolve(), None, None)
    assert doctor_model._git_dir(tmp_path / "main") == (common, None, None)


#: This repository's configuration shape: one default stage hook, one commit-msg hook.
TWO_STAGE_CONFIG = (
    "repos:\n"
    "  - repo: local\n"
    "    hooks:\n"
    "      - id: scan\n"
    "        name: scan\n"
    "        entry: 'true'\n"
    "        language: system\n"
    "      - id: closing\n"
    "        name: closing\n"
    "        entry: 'true'\n"
    "        language: system\n"
    "        stages: [commit-msg]\n")

#: The installer's commit-msg hook: the same template bound to the other stage.
INSTALLED_COMMIT_MSG_HOOK = INSTALLED_HOOK.replace(
    "--hook-type=pre-commit", "--hook-type=commit-msg")

TWO_STAGE_COMMAND = "pre-commit install --hook-type pre-commit --hook-type commit-msg"


def two_stage_checkout(root: Path, *, commit_msg: str | None = INSTALLED_COMMIT_MSG_HOOK):
    """A synthetic checkout configured for two stages, with the pre-commit hook installed."""
    hooked_checkout(root)
    (root / ".pre-commit-config.yaml").write_text(TWO_STAGE_CONFIG)
    if commit_msg is not None:
        (root / ".git" / "hooks" / "commit-msg").write_text(commit_msg)
    return root


def test_a_configured_commit_msg_stage_with_no_hook_is_refused(library, tmp_path):
    """``pre-commit install`` alone omits the commit-msg hook a configured stage needs."""
    finding = hook_finding(library, two_stage_checkout(tmp_path / "checkout", commit_msg=None))
    assert finding.status is FAIL, finding.detail
    assert "no commit-msg hook" in finding.detail
    assert TWO_STAGE_COMMAND in finding.detail


def test_every_configured_hook_type_installed_passes_the_check(library, tmp_path):
    """The other half of every guard: the correct setup is green, and says why."""
    finding = checked(hook_finding(library, two_stage_checkout(tmp_path / "checkout")), OK)
    assert "commit-msg" in finding.detail


def test_a_commit_msg_hook_installed_for_another_stage_is_refused(library, tmp_path):
    """A pre-commit hook copied into the commit-msg slot runs the scan, not the closing check."""
    checkout = two_stage_checkout(tmp_path / "checkout", commit_msg=INSTALLED_HOOK)
    finding = checked(hook_finding(library, checkout), FAIL)
    assert "--hook-type=commit-msg" in finding.detail
    assert TWO_STAGE_COMMAND in finding.detail


def test_a_fresh_clone_is_told_the_whole_install_line(library, tmp_path):
    """R-1's own scenario, a clone with no hook at all, gets the line that installs both."""
    checkout = tmp_path / "checkout"
    (checkout / ".git" / "hooks").mkdir(parents=True)
    (checkout / ".pre-commit-config.yaml").write_text(TWO_STAGE_CONFIG)
    finding = checked(hook_finding(library, checkout), FAIL)
    assert "no pre-commit hook" in finding.detail
    assert TWO_STAGE_COMMAND in finding.detail


def test_a_commit_msg_hook_that_cannot_be_read_is_unknown_not_missing(library, tmp_path):
    """The split the pre-commit hook already makes, carried to every other type."""
    checkout = two_stage_checkout(tmp_path / "checkout")
    other = checkout / ".git" / "hooks" / "commit-msg"
    with _sealed(other):
        finding = hook_finding(library, checkout)
    checked(finding, FAIL, Remedy.GRANT_PATH_ACCESS)
    assert "unknown rather than no" in finding.detail
    assert "no commit-msg hook" not in finding.detail


def test_a_configuration_that_does_not_parse_is_not_read_as_one_hook_type(library, tmp_path):
    """Falling back to the floor would report green over the gap this check closes."""
    checkout = two_stage_checkout(tmp_path / "checkout", commit_msg=None)
    (checkout / ".pre-commit-config.yaml").write_text("repos: [\n")
    finding = checked(hook_finding(library, checkout), FAIL)
    assert "not valid YAML" in finding.detail


def test_a_configuration_that_cannot_be_read_is_unknown_and_asks_for_access(library, tmp_path):
    """An unreadable configuration is a permission to grant, and its stages are unknown."""
    checkout = two_stage_checkout(tmp_path / "checkout", commit_msg=None)
    config_file = checkout / ".pre-commit-config.yaml"
    with _sealed(config_file):
        finding = hook_finding(library, checkout)
    checked(finding, FAIL, Remedy.GRANT_PATH_ACCESS)
    assert "could not be read" in finding.detail
    assert "unknown rather than no" in finding.detail


def test_a_clone_with_no_configuration_is_told_the_floor(library, tmp_path):
    """With no configuration, the line names the one type always needed, not a bare installer."""
    checkout = tmp_path / "checkout"
    (checkout / ".git" / "hooks").mkdir(parents=True)
    finding = checked(hook_finding(library, checkout), FAIL)
    assert "Run `pre-commit install --hook-type pre-commit` in" in finding.detail


def test_no_yaml_reader_is_unknown_rather_than_one_hook_type(library, tmp_path, monkeypatch):
    """PyYAML arrives with the dev extra, not the runtime, so its absence is reachable."""
    monkeypatch.setitem(sys.modules, "yaml", None)
    finding = checked(hook_finding(library, two_stage_checkout(tmp_path / "checkout")), FAIL)
    assert "PyYAML is not importable" in finding.detail
    assert "pip install -e '.[dev]'" in finding.detail


def _stage_config(stages: str) -> str:
    return (
        "repos:\n"
        "  - repo: local\n"
        "    hooks:\n"
        "      - id: one\n"
        "        name: one\n"
        "        entry: 'true'\n"
        "        language: system\n"
        f"        stages: {stages}\n")


@pytest.mark.parametrize(
    "text, expected",
    [
        ("repos: []\n", ("pre-commit",)),
        (TWO_STAGE_CONFIG, ("pre-commit", "commit-msg")),
        ("default_install_hook_types: [pre-push]\nrepos: []\n", ("pre-commit", "pre-push")),
        # A legacy spelling names the hook it always named.
        ("default_stages: [push]\nrepos: []\n", ("pre-commit", "pre-push")),
        (_stage_config("[commit, merge-commit]"), ("pre-commit", "pre-merge-commit")),
        # Manual is run by hand and has no git hook to install.
        (_stage_config("[manual]"), ("pre-commit",)),
        # Named twice, needed once, in first-named order.
        (_stage_config("[prepare-commit-msg, commit-msg, prepare-commit-msg]"),
         ("pre-commit", "prepare-commit-msg", "commit-msg")),
    ])
def test_the_hook_types_a_configuration_needs(tmp_path, text, expected):
    config_file = planted(tmp_path / ".pre-commit-config.yaml", text)
    assert doctor_state._configured_hook_types(config_file) == (expected, None, None)


@pytest.mark.parametrize(
    "text, because",
    [
        (_stage_config("[on-commit]"), "'on-commit'"),
        (_stage_config("[{stage: commit}]"), "installs no hook for"),
        ("- just\n- a list\n", "is not a pre-commit configuration"),
    ])
def test_a_configuration_this_cannot_understand_is_a_sentence(tmp_path, text, because):
    """An unknown stage is not a stage that needs nothing."""
    config_file = planted(tmp_path / ".pre-commit-config.yaml", text)
    types, problem, _remedy = doctor_state._configured_hook_types(config_file)
    assert types == ()
    assert problem is not None and because in problem


def test_this_repositorys_own_configuration_needs_both_hook_types():
    """Pinned against the tree rather than a fixture authored beside the reader."""
    root = doctor_model._checkout_root()
    if root is None:  # pragma: no cover - an installed wheel has no checkout
        return
    types, problem, _remedy = doctor_state._configured_hook_types(root / ".pre-commit-config.yaml")
    assert problem is None, problem
    assert types == ("pre-commit", "commit-msg")


def test_a_commit_msg_hook_on_another_configuration_is_refused(library, tmp_path):
    """A hook for a configured type dispatching to another file never runs its closing check."""
    checkout = two_stage_checkout(
        tmp_path / "checkout",
        commit_msg=INSTALLED_COMMIT_MSG_HOOK.replace(".pre-commit-config.yaml", "tools/other.yaml"))
    (checkout / "tools").mkdir()
    (checkout / "tools" / "other.yaml").write_text("repos: []\n")
    finding = checked(hook_finding(library, checkout), FAIL)
    assert "dispatches to tools/other.yaml, not .pre-commit-config.yaml" in finding.detail


def test_the_install_line_names_a_configuration_that_is_not_the_default(library, tmp_path):
    """The install line names a non-default configuration, or the advice breaks a working hook."""
    checkout = tmp_path / "checkout"
    (checkout / "tools").mkdir(parents=True)
    (checkout / "tools" / "hooks.yaml").write_text(TWO_STAGE_CONFIG)
    hooked_checkout(
        checkout, INSTALLED_HOOK.replace(".pre-commit-config.yaml", "tools/hooks.yaml"),
        config_file=False)
    finding = checked(hook_finding(library, checkout), FAIL)
    assert (
        "pre-commit install --config tools/hooks.yaml --hook-type pre-commit --hook-type commit-msg"
    ) in finding.detail


# ═══ 4. The wizard ══════════════════════════════════════════════════════════


class Scripted(prompt.Prompter):
    """A prompter with its answers queued, driving the REAL ask and confirm."""

    def __new__(cls, answers, secrets_=()):
        queued = list(answers)
        held = list(secrets_)
        return prompt.Prompter(
            read_line=lambda: (queued.pop(0) + "\n") if queued else _eof(),
            read_secret=lambda _q: held.pop(0) if held else _eof(), write=lambda _text: None)


def _eof():
    raise EOFError("nothing left in the script")


def silent() -> prompt.Prompter:
    """A machine where nothing can be asked, which is every scripted run."""
    return prompt.Prompter(read_line=_eof, read_secret=lambda _q: _eof(), write=lambda _t: None)


def test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor(
        tmp_path, monkeypatch):
    """The first scenario end to end, every answer a flag, so the one interactive verb scripts."""
    root = fresh_root(tmp_path, monkeypatch, "fresh")
    green_probes(monkeypatch)
    code, out, err = setup_at(root, tmp_path)
    envelope = json.loads(out)
    written = config.load()
    assert written.library.volume_id == VOLUME
    assert written.profile.name == "slim"
    assert config.state_path("taxonomy_active", written).is_file()
    # The pin is the one thing setup may not adopt for the user (S2).
    failing = [c["key"] for c in envelope["data"]["checks"] if c["status"] == "fail"]
    assert failing == ["rekordbox.pins"], (envelope["data"]["checks"], err)
    assert code == int(ExitCode.PRECONDITION)
    document = json.loads(json.dumps(document_for(root)))
    document["profile"] = {"name": "slim"}
    assert config.validate(document) == []
    assert report_on(document).ok


def state_fingerprint(*roots) -> dict[str, tuple[int, int]]:
    """Size and mtime of every file under each root, so "wrote nothing" is observed."""
    found: dict[str, tuple[int, int]] = {}
    for root in roots:
        base = Path(root)
        if not base.is_dir():
            continue
        for current, _directories, files in os.walk(base):
            for name in files:
                path = Path(current) / name
                stat = path.stat()
                found[str(path)] = (stat.st_size, stat.st_mtime_ns)
    return found


def test_doctor_writes_nothing_at_all(configured):
    """``run`` writes nothing, even on a foreign volume; the run record is the shell's."""
    seed_taxonomy(configured)
    roots = (configured.library.root, config.installation_state_dir(), config.config_dir())
    before = state_fingerprint(*roots)
    report = report_on(configured, identity_provider=lambda _p: "9999")
    assert not report.ok
    assert state_fingerprint(*roots) == before


def test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to(
        configured, monkeypatch):
    """A re-run resolves every answer from the record, prompts nothing and changes nothing."""
    seed_taxonomy(configured)
    green_probes(monkeypatch)
    before = config.load().to_toml_dict()
    code, out, err = drive(["--output", "json", "setup"])
    assert code == int(ExitCode.OK), err
    envelope = json.loads(out)
    assert envelope["data"]["summary"]["answered"] == []
    assert envelope["data"]["summary"]["provenance"] == "existing"
    config.reset_cache()
    assert config.load().to_toml_dict() == before


def test_the_wizard_reports_no_check_key_twice(configured, monkeypatch):
    """Two credentials share one check key, so a note keyed on the check would appear twice."""
    seed_taxonomy(configured)
    green_probes(monkeypatch, credential_recorded=lambda _n: False)
    _code, out, _err = drive(["--output", "json", "setup"])
    keys = [check["key"] for check in json.loads(out)["data"]["checks"]]
    assert len(keys) == len(set(keys)), sorted(k for k in keys if keys.count(k) > 1)


def test_the_wizard_never_puts_a_credential_value_in_its_own_report(configured):
    """Only a credential's name reaches the report, which lands in every log of the run."""
    wizard = setup_verb._Wizard({}, Scripted(["yes", "yes", "yes"], ["s3cret", "k3y", "s1gn"]))
    setup_verb._capture_credentials(wizard, configured)
    rendered = json.dumps([note.to_json() for note in wizard.notes])
    for value in ("s3cret", "k3y", "s1gn"):
        assert value not in rendered


def test_the_wizard_refuses_to_overwrite_a_configuration_it_cannot_understand(
        tmp_path, monkeypatch):
    """An unreadable config is refused, not overwritten; only a missing file starts empty."""
    directory = made(tmp_path / "cfg")
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(directory))
    path = planted(directory / config.CONFIG_FILENAME, "this is not toml = = =\n")
    config.reset_cache()
    assert refusal(setup_verb.existing_document).remediation.remedy is Remedy.REPAIR_CONFIG_FILE
    assert path.read_text() == "this is not toml = = =\n", "the original was rewritten"


def test_the_wizard_completes_an_incomplete_configuration_rather_than_refusing(
        tmp_path, monkeypatch):
    """A config missing a required key is what setup is for, so it is completed."""
    directory = made(tmp_path / "cfg")
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(directory))
    (directory / config.CONFIG_FILENAME).write_text(
        f'schema_version = {config.CURRENT_SCHEMA_VERSION}\n'
        f'[library]\nroot = "{tmp_path / "kept"}"\n')
    config.reset_cache()
    document, provenance = setup_verb.existing_document()
    assert provenance == "incomplete"
    assert document["library"]["root"] == str(tmp_path / "kept")


def test_the_wizard_never_re_derives_a_volume_identity_it_already_recorded(configured):
    """A recorded identity is never re-read, or a re-run would adopt a restored clone (R38)."""
    wizard = setup_verb._Wizard(dict(configured.to_toml_dict()), silent())
    root = str(configured.library.root)
    assert setup_verb._resolve_volume_id(wizard, root, None, probes()) == VOLUME
    overridden = setup_verb._resolve_volume_id(wizard, root, "1111-2222", probes())
    assert overridden == "1111-2222", "an explicit answer is the only thing that replaces it"


def test_the_wizard_proposes_the_installed_pin_and_records_it_only_on_a_yes(
        configured, monkeypatch):
    """S2: a pin copied from the installed version refuses nothing, so only a yes records it."""
    monkeypatch.setattr(setup_verb.rb_writer, "read_installed_app_version", lambda **_k: "9.9.9")
    document = dict(configured.to_toml_dict())
    document["rekordbox"] = {}
    unpinned = config.from_dict(document)
    declined = setup_verb._Wizard(document, silent())
    assert setup_verb._propose_pin(declined, document, unpinned) is False
    assert "rekordbox" not in document or not document["rekordbox"].get("pinned_app_version")
    assert any("NOT recorded" in note.detail for note in declined.notes)
    accepted = setup_verb._Wizard(document, Scripted(["yes"]))
    assert setup_verb._propose_pin(accepted, document, unpinned) is True
    assert document["rekordbox"]["pinned_app_version"] == "9.9.9"
    # Never written here: it means "confirmed against a real write".
    assert "validated_on" not in document["rekordbox"]


def _backup_flags(dest=None, archive_root=None, db_dest_root=None, remote=None):
    """Setup's four backup flags as parsed, each unset unless given."""
    return SimpleNamespace(
        backup_dest=dest, backup_archive_root=archive_root, backup_db_dest_root=db_dest_root,
        backup_remote=remote)


#: The three backup destinations, all on one ``gdrive`` remote.
GDRIVE = {"dest": "gdrive:mirror", "archive_root": "gdrive:archive", "db_dest_root": "gdrive:db"}

_GDRIVE_DESTINATIONS = [
    "--backup-dest", "gdrive:mirror",
    "--backup-archive-root", "gdrive:archive",
    "--backup-db-dest-root", "gdrive:db",
]


def _recording_wizard(document: dict) -> tuple[setup_verb._Wizard, list[str]]:
    """A wizard that answers yes to anything and records whatever it was shown."""
    written: list[str] = []
    yes = prompt.Prompter(
        read_line=lambda: "yes\n", read_secret=lambda _q: "", write=written.append)
    return setup_verb._Wizard(document, yes), written


def test_the_wizard_asks_for_the_backup_destinations_when_the_module_is_on(configured):
    """R-345: with nothing recorded, a yes asks all three destinations and derives the remote."""
    document = dict(configured.to_toml_dict())
    assert "backup" not in document
    wizard = setup_verb._Wizard(document, Scripted(["yes", *GDRIVE.values()]))
    setup_verb._resolve_backup(wizard, document, _backup_flags(), probes())
    assert document["backup"] == {**GDRIVE, "remote": "gdrive"}
    assert [line for line in wizard.asked if line.startswith("backup.")] == [
        "backup.dest (answered)", "backup.archive_root (answered)", "backup.db_dest_root (answered)"
    ]
    assert config.validate(document) == []


def test_the_wizard_records_nothing_for_backup_when_the_offer_goes_unanswered(configured):
    """An unanswered offer records nothing and refuses nothing; the note names the flags."""
    document = dict(configured.to_toml_dict())
    wizard = setup_verb._Wizard(document, silent())
    setup_verb._resolve_backup(wizard, document, _backup_flags(), probes())
    assert "backup" not in document
    assert wizard.asked == []
    note = checked(next(n for n in wizard.notes if n.key == "setup.backup"), INFO)
    assert "backup.dest" in note.detail and "not recorded" in note.detail
    assert "--backup-dest" in note.detail


def test_the_wizard_asks_nothing_about_backup_when_the_module_is_off(configured):
    """Slim has no backup module, so there is no destination to ask for."""
    document = dict(configured.to_toml_dict())
    document["profile"] = SLIM
    wizard, written = _recording_wizard(document)
    setup_verb._resolve_backup(wizard, document, _backup_flags(), probes())
    assert written == []
    assert "backup" not in document
    note = next(n for n in wizard.notes if n.key == "setup.backup")
    assert "off in this profile" in note.detail


def test_backup_flags_are_recorded_even_when_the_module_is_off(configured):
    """A flag is an answer whatever the profile says, and validation judges its shape."""
    document = dict(configured.to_toml_dict())
    document["profile"] = SLIM
    wizard = setup_verb._Wizard(document, silent())
    setup_verb._resolve_backup(wizard, document, _backup_flags(**GDRIVE), probes())
    assert document["backup"] == {**GDRIVE, "remote": "gdrive"}
    assert len([line for line in wizard.asked if "command line" in line]) == 3
    assert any("off in this profile" in n.detail for n in wizard.notes if n.key == "setup.backup")


def test_a_declined_offer_still_records_the_flags_that_were_given(configured):
    """With the offer declined, given flags land, the missing one stays unset."""
    document = dict(configured.to_toml_dict())
    wizard = setup_verb._Wizard(document, Scripted(["no"]))
    given = {"dest": "gdrive:mirror", "archive_root": "gdrive:archive"}
    setup_verb._resolve_backup(wizard, document, _backup_flags(**given), probes())
    assert document["backup"] == {**given, "remote": "gdrive"}
    note = next(n for n in wizard.notes if n.key == "setup.backup")
    assert "backup.db_dest_root not recorded" in note.detail
    assert "backup.dest" not in note.detail.split(" not recorded")[0]


def test_a_mistyped_module_name_is_still_a_named_problem_not_a_traceback(configured, monkeypatch):
    """A mistyped module (``bakcup = true``) is a named config problem, not a traceback."""
    seed_taxonomy(configured)
    green_probes(monkeypatch)
    path = config.config_path()
    path.write_text(path.read_text() + "\n[modules]\nbakcup = true\n")
    config.reset_cache()
    code, out, err = drive(["--output", "json", "setup"])
    envelope = json.loads(out)
    assert envelope["cause"]["reason"] == "config-unusable", envelope["cause"]
    problems = envelope["cause"]["detail"]["problems"]
    assert any("modules.bakcup is not a known module" in p for p in problems), problems


def test_the_wizard_keeps_recorded_backup_destinations_without_asking(configured):
    """Recorded destinations and a spelled remote reach no prompt and are kept."""
    document = _spelled_remote_document(configured, "gdrive:")
    before = json.loads(json.dumps(document))
    wizard, written = _recording_wizard(document)
    setup_verb._resolve_backup(wizard, document, _backup_flags(), probes())
    assert written == []
    assert wizard.asked == []
    assert document == before


def test_the_backup_flags_are_recorded_without_a_question(configured, monkeypatch):
    """Through the dispatcher, the destination flags land, the remote is derived, nothing asked."""
    seed_taxonomy(configured)
    # The closing doctor looks the derived remote up in rclone's configuration.
    green_probes(monkeypatch, rclone_remotes=lambda _rclone: {"gdrive": {"type": "sftp"}})
    code, out, err = drive(["--output", "json", "setup", *_GDRIVE_DESTINATIONS])
    assert code == int(ExitCode.OK), err
    envelope = json.loads(out)
    assert envelope["data"]["summary"]["answered"] == [
        "backup.dest (from the command line)",
        "backup.archive_root (from the command line)",
        "backup.db_dest_root (from the command line)",
    ]
    config.reset_cache()
    written = config.load()
    assert written.backup.dest == "gdrive:mirror"
    assert written.backup.archive_root == "gdrive:archive"
    assert written.backup.db_dest_root == "gdrive:db"
    assert written.backup.remote == "gdrive"
    raw = tomllib.loads(config.config_path().read_text())
    assert raw["backup"]["remote"] == "gdrive"


@pytest.mark.parametrize("how", ["flag", "prompt"])
def test_a_bare_folder_name_is_refused_by_the_wizard_however_it_arrives(
        configured, monkeypatch, how):
    """A bare folder name is refused by flag or prompt, never given to rclone (R-345)."""
    seed_taxonomy(configured)
    green_probes(monkeypatch)
    argv = ["--output", "json", "setup"]
    if how == "flag":
        argv += [
            "--backup-dest", "MusicBackup",
            "--backup-archive-root", "gdrive:archive",
            "--backup-db-dest-root", "gdrive:db",
        ]
    else:
        # Built BEFORE the patch, because ``Scripted`` constructs the real class.
        scripted = Scripted(["yes", "MusicBackup", "gdrive:archive", "gdrive:db"])
        monkeypatch.setattr(prompt, "Prompter", lambda: scripted)
    code, out, err = drive(argv)
    assert code != int(ExitCode.OK), out
    envelope = json.loads(out)
    assert envelope["cause"]["reason"] == "config-unusable", envelope["cause"]
    problems = envelope["cause"]["detail"]["problems"]
    assert len(problems) == 1, problems
    assert "backup.dest" in problems[0] and "'MusicBackup'" in problems[0]
    config.reset_cache()
    assert config.load().backup.dest is None, "the refused answer reached the file"


def _spelled_remote_document(configured, spelled="remote"):
    document = dict(configured.to_toml_dict())
    document["backup"] = {"remote": spelled, **GDRIVE}
    return document


def test_a_spelled_remote_rclone_lacks_is_replaced_by_the_destinations_remote(configured):
    """R-662: a spelled remote rclone was read and lacks is replaced, and the run says so."""
    document = _spelled_remote_document(configured)
    wizard = setup_verb._Wizard(document, silent())
    machine = probes(rclone_remotes=lambda _rclone: {"gdrive": {"type": "sftp"}})
    setup_verb._resolve_backup(wizard, document, _backup_flags(), machine)
    assert document["backup"]["remote"] == "gdrive"
    note = next(n for n in wizard.notes if n.key == "setup.backup.remote")
    assert "'remote'" in note.detail and "replaced with 'gdrive'" in note.detail
    assert config.validate(document) == []


@pytest.mark.parametrize(
    "machine",
    [
        pytest.param(
            {"rclone_remotes": lambda _r: {"remote": {}, "gdrive": {}}}, id="rclone-knows-it"),
        pytest.param({"rclone_remotes": lambda _r: None}, id="rclone-unreadable"),
        # An empty dump lacks every name, so the destinations may be the typo.
        pytest.param({"rclone_remotes": lambda _r: {}}, id="rclone-knows-neither"),
        pytest.param({"find_binary": lambda _name: None}, id="rclone-absent"),
    ])
def test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it(configured, machine):
    """A spelled remote rclone knows or could not be asked about is kept, and still refused."""
    document = _spelled_remote_document(configured)
    wizard = setup_verb._Wizard(document, silent())
    setup_verb._resolve_backup(wizard, document, _backup_flags(), probes(**machine))
    assert document["backup"]["remote"] == "remote"
    assert not any(n.key == "setup.backup.remote" for n in wizard.notes)
    problems = config.validate(document)
    assert len(problems) == 1 and "backup.remote names 'remote'" in problems[0], problems


def test_no_disagreement_is_read_where_there_is_nothing_to_compare(configured):
    """A blank spelled remote, or destinations naming several remotes, is no disagreement."""
    blank = _spelled_remote_document(configured, spelled="  ")
    assert config.backup_remote_disagreement(blank) is None
    several = _spelled_remote_document(configured)
    several["backup"]["archive_root"] = "dropbox:archive"
    assert config.backup_remote_disagreement(several) is None
    problems = config.validate(several)
    assert len(problems) == 1 and "name several" in problems[0], problems


def test_the_backup_remote_flag_replaces_a_spelled_remote_rclone_knows(configured):
    document = _spelled_remote_document(configured)
    wizard = setup_verb._Wizard(document, silent())
    machine = probes(rclone_remotes=lambda _r: {"remote": {}, "gdrive": {}})
    setup_verb._resolve_backup(wizard, document, _backup_flags(remote="gdrive"), machine)
    assert document["backup"]["remote"] == "gdrive"
    assert "backup.remote (from the command line)" in wizard.asked
    assert config.validate(document) == []


def _spell_the_backup_remote(name: str) -> None:
    path = config.config_path()
    path.write_text(path.read_text() + f'\n[backup]\nremote = "{name}"\n')
    config.reset_cache()


def test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it(
        configured, monkeypatch):
    """The disagreeing remote refusal's fix names the flag, and running it writes the file."""
    seed_taxonomy(configured)
    _spell_the_backup_remote("remote")
    both = {"remote": {"type": "sftp"}, "gdrive": {"type": "sftp"}}
    green_probes(monkeypatch, rclone_remotes=lambda _r: both)
    code, _out, err = drive(["setup", *_GDRIVE_DESTINATIONS])
    assert code != int(ExitCode.OK), err
    assert "config-unusable" in err
    assert "fix: re-run crate setup with --backup-remote gdrive" in err, err
    assert "fix: crate setup\n" not in err
    assert "Setup's --backup-remote replaces the spelled one" in err
    code, out, err = drive(["--output", "json", "setup", "--backup-remote", "gdrive"])
    assert code == int(ExitCode.OK), err
    assert "backup.remote (from the command line)" in json.loads(out)["data"]["summary"]["answered"]
    config.reset_cache()
    assert config.load().backup.remote == "gdrive"
    assert tomllib.loads(config.config_path().read_text())["backup"]["remote"] == "gdrive"


def test_the_setup_token_stays_when_the_disagreement_is_not_the_only_problem(configured):
    """Beside other problems the run-setup token stays and the flag leads the steps."""
    document = _spelled_remote_document(configured)
    only = config.validate(document)
    alone = setup_verb._answers_remediation(document, only)
    assert alone.remedy is None
    assert alone.steps[0].startswith("re-run crate setup with --backup-remote gdrive")
    several = [*only, "library.root is not set"]
    beside = setup_verb._answers_remediation(document, several)
    assert beside.remedy is Remedy.RUN_SETUP
    assert beside.steps[0].startswith("re-run crate setup with --backup-remote gdrive")
    assert list(beside.steps[1:]) == several


def test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know(configured, monkeypatch):
    """R-662: a spelled name rclone lacks is settled by the destination flags alone."""
    seed_taxonomy(configured)
    _spell_the_backup_remote("remote")
    green_probes(monkeypatch, rclone_remotes=lambda _r: {"gdrive": {"type": "sftp"}})
    code, out, err = drive(["--output", "json", "setup", *_GDRIVE_DESTINATIONS])
    assert code == int(ExitCode.OK), err
    checks = json.loads(out)["data"]["checks"]
    assert any(c["key"] == "setup.backup.remote" for c in checks), checks
    config.reset_cache()
    assert config.load().backup.remote == "gdrive"


def test_the_wizard_refuses_a_required_answer_it_cannot_obtain(tmp_path, monkeypatch):
    """An answer nobody gave and nothing derives is a refusal naming the key, never a guess."""
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "cfg"))
    config.reset_cache()
    wizard = setup_verb._Wizard({}, silent())
    cause = refusal(wizard.resolve, "library.root", flag=None, question="Where is the library")
    assert cause.remediation.remedy is Remedy.RUN_SETUP
    assert "library.root" in cause.message


def test_a_derived_default_is_taken_when_nothing_can_be_asked(tmp_path):
    wizard = setup_verb._Wizard({}, silent())
    answer = wizard.resolve(
        "paths.download_staging", flag=None, question="Where", default=str(tmp_path / "staging"))
    assert answer == str(tmp_path / "staging")
    assert any("nothing could be asked" in line for line in wizard.asked)


def test_a_closed_question_refuses_a_default_outside_its_own_option_set():
    """A default a user cannot accept by pressing return is not a default."""
    wizard = setup_verb._Wizard({}, silent())
    with pytest.raises(ValueError, match="not one of them"):
        wizard.resolve(
            "profile.name", flag=None, question="Which preset", default="enormous",
            choices=profiles.PROFILE_NAMES)


def test_the_active_taxonomy_is_copied_once_and_never_overwritten(configured):
    """S6: the taxonomy copy is written once, so a template the user edited is never replaced."""
    wizard = seeded(configured)
    path = config.state_path("taxonomy_active", configured)
    assert path.is_file()
    path.write_text("# edited by hand\n" + path.read_text())
    setup_verb._seed_taxonomy(wizard, configured, probes())
    assert path.read_text().startswith("# edited by hand")


def test_the_wizard_offers_every_credential_the_profile_needs_and_records_it(configured):
    """Credentials offered come from the same registry question doctor asks."""
    values = ["one", "two", "three", "four"]
    wizard = setup_verb._Wizard({}, Scripted(["yes", "yes", "yes", "yes"], values))
    setup_verb._capture_credentials(wizard, configured)
    # The Discogs token is its own step, ``_link_discogs`` (U283).
    assert not secrets.exists(str(secrets.Credential.DISCOGS_TOKEN))
    assert secrets.exists(str(secrets.Credential.PROVIDER_SESSION))
    assert secrets.exists(str(secrets.Credential.IDENTIFY_KEY))
    assert all(note.status is OK for note in wizard.notes)


def test_an_unanswered_credential_offer_leaves_it_outstanding_rather_than_empty(configured):
    """An unanswered offer leaves the credential outstanding, the same as a no."""
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._capture_credentials(wizard, configured)
    assert not secrets.recorded()
    assert all(note.status is INFO for note in wizard.notes)


def test_only_the_wizard_and_the_label_sync_are_interactive_and_neither_reads_stdin():
    """Both are interactive, yet the stdin allowlist names only ``cli/prompt.py``."""
    interactive = [entry.name for entry in registry.entries() if entry.interactive]
    assert interactive == ["setup", "label.sync"]
    tree = ast.parse((SRC_ROOT / "cratekit" / "cli" / "setup.py").read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in {"input", "raw_input"}
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = (
                [a.name for a in node.names]
                if isinstance(node, ast.Import)
                else [node.module or ""])
            assert all(name.split(".")[0] != "getpass" for name in names)


# ═══ 5. crate login ═════════════════════════════════════════════════════════


def test_a_credential_offer_accepted_and_left_empty_is_the_same_note_as_a_no(configured):
    """R-347: a yes with nothing typed is a no, since only login makes the provider session."""
    wizard = setup_verb._Wizard({}, Scripted(["yes", "yes", "yes"], ["", "  ", ""]))
    setup_verb._capture_credentials(wizard, configured)
    offered = [note for note in wizard.notes if note.key.startswith("setup.credential.")]
    assert offered, "no credential was offered, so nothing here was exercised"
    assert all(note.status is INFO for note in offered)
    assert not secrets.recorded()


def test_a_credential_offer_that_could_not_be_read_still_fails(configured):
    """An empty answer is a person; a dead stream is not."""
    wizard = setup_verb._Wizard({}, Scripted(["yes", "yes", "yes", "yes"]))
    setup_verb._capture_credentials(wizard, configured)
    offered = [note for note in wizard.notes if note.key.startswith("setup.credential.")]
    assert offered
    assert all(note.status is FAIL for note in offered)


def test_an_empty_credential_leaves_the_exit_code_to_doctor(tmp_path, monkeypatch):
    """R-347: with the offer left empty, the only failing check is the unset pin."""
    root = fresh_root(tmp_path, monkeypatch, "fresh")
    green_probes(monkeypatch)
    scripted = Scripted(["no", "yes", "yes", "yes"], ["", "", ""])
    monkeypatch.setattr(setup_verb.prompt, "Prompter", lambda: scripted)
    code, out, err = setup_at(root, tmp_path)
    checks = json.loads(out)["data"]["checks"]
    credential = [c for c in checks if c["key"].startswith("setup.credential.")]
    assert credential and all(c["status"] == "info" for c in credential), (checks, err)
    failing = [c["key"] for c in checks if c["status"] == "fail"]
    assert failing == ["rekordbox.pins"], (checks, err)
    assert code == int(ExitCode.PRECONDITION)


def test_an_identity_typed_as_diskutil_prints_it_passes_the_mount_check(library):
    """R-344: an uppercase UUID is recorded as given and matches the platform's lowercase one."""
    reported = "0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"
    wizard = setup_verb._Wizard({}, silent())
    recorded = setup_verb._resolve_volume_id(wizard, str(library), reported.upper(), probes())
    cfg = config.from_dict(document_for(library, volume_id=recorded))
    machine = probes(identity_provider=lambda _path: reported)
    assert mount_state(cfg, machine).state is setup_verb.preflight.MountState.OK
    setup_verb._seed_taxonomy(wizard, cfg, machine)
    assert not [note for note in wizard.notes if note.status is FAIL]
    assert config.state_path("taxonomy_active", cfg).is_file()


def test_a_question_reaches_a_real_pipe_before_its_answer_is_read():
    """R-346: unbuffered or not, the question reaches a real stderr pipe before the answer."""
    environment = {k: v for k, v in os.environ.items() if k != "PYTHONUNBUFFERED"}
    script = (
        "import sys\n"
        "from cratekit.cli import prompt\n"
        "sys.stdout.write(prompt.Prompter().ask('Which crate'))\n")
    child = subprocess.Popen(
        [sys.executable, "-c", script], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, env=environment)
    try:
        shown = b""
        deadline = time.monotonic() + 15
        while b"Which crate: " not in shown:
            remaining = deadline - time.monotonic()
            assert remaining > 0, f"the question never reached the pipe: {shown!r}"
            ready, _, _ = select.select([child.stderr], [], [], remaining)
            assert ready, f"the question never reached the pipe: {shown!r}"
            chunk = os.read(child.stderr.fileno(), 4096)
            assert chunk, f"the child closed standard error first: {shown!r}"
            shown += chunk
        answered, _ = child.communicate(b"techno\n", timeout=15)
        assert answered == b"techno"
    finally:
        if child.poll() is None:
            child.kill()
            child.wait()


def test_login_never_accepts_a_credential_as_an_argument():
    """An argument is visible in the process listing and the shell history."""
    parser = argparse.ArgumentParser()
    login_verb.build(parser, registry.entry("login"))
    options = {
        option
        for action in parser._actions
        for option in action.option_strings
        if option not in ("-h", "--help")
    }
    assert options == {"--from-file"}
    assert set(login_verb.CREDENTIAL_NAMES) == {str(name) for name in secrets.Credential}


def test_login_refuses_with_both_ways_of_supplying_a_value(configured):
    code, out, _ = drive(["--output", "json", "login", "provider-session"])
    assert code == int(ExitCode.PRECONDITION)
    envelope = json.loads(out)
    assert envelope["cause"]["remediation"]["remedy"] == str(Remedy.SET_CREDENTIAL)
    assert "--from-file" in envelope["cause"]["message"]
    assert secrets.ENV_ALLOW_ENV_CREDENTIALS in envelope["cause"]["message"]


def test_login_records_a_value_from_a_file(configured, tmp_path):
    holder = planted(tmp_path / "token.txt", "  a-real-looking-token\n")
    code, out, err = login_from(holder)
    assert code == int(ExitCode.OK), err
    assert secrets.get("provider-session") == "a-real-looking-token"
    assert json.loads(out)["data"]["summary"]["credential"] == "provider-session"


def test_login_refuses_a_file_holding_nothing(configured, tmp_path):
    """An empty credential reads as absent on some backends, breaking the presence question."""
    holder = planted(tmp_path / "empty.txt", "   \n")
    code, out, _ = login_from(holder)
    assert code == int(ExitCode.PRECONDITION)
    assert not secrets.recorded()


def test_login_reads_the_environment_fallback_through_the_store_that_owns_it(
        configured, monkeypatch):
    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    monkeypatch.setenv(secrets.ENV_CREDENTIAL_PREFIX + "IDENTIFY_KEY", "from-the-environment")
    code, _, err = drive(["login", "identify-key"])
    assert code == int(ExitCode.OK), err
    monkeypatch.delenv(secrets.ENV_ALLOW_ENV_CREDENTIALS)
    assert secrets.environment_value("identify-key") is None


# ═══ 6. The reports, and the rendering ══════════════════════════════════════


def test_doctor_exits_with_a_precondition_status_and_keeps_its_report(configured, monkeypatch):
    """A failing doctor keeps its report, which is why it builds its own envelope."""
    green_probes(monkeypatch, keychain_available=lambda: False)
    code, out, err = drive(["--output", "json", "doctor"])
    envelope = json.loads(out)
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "doctor-check-failed"
    assert len(envelope["data"]["checks"]) == len(doctor.CHECK_KEYS)
    assert "keychain.reachable" in envelope["cause"]["detail"]["failing"]
    assert "keychain.reachable" in err, "the failure has to reach a person too"


def test_a_green_doctor_exits_zero(configured, monkeypatch):
    seed_taxonomy(configured)
    green_probes(monkeypatch)
    code, out, err = drive(["--output", "json", "doctor"])
    assert code == int(ExitCode.OK), err
    assert json.loads(out)["outcome"] == str(Outcome.OK)


def test_status_reports_open_runs_sessions_and_trees(configured):
    state = gates.new_run(registry.entry("profile.set"))
    state.open_gate = "profile.set.apply"
    gates.save(state)
    write_session(configured, sources={"labels": str(session.SourceState.REFUSED)})
    code, out, err = drive(["--output", "json", "status"])
    assert code == int(ExitCode.OK), err
    data = json.loads(out)["data"]
    keys = {check["key"] for check in data["checks"]}
    assert f"run.{state.run_id}" in keys
    assert "source.labels" in keys
    assert data["summary"]["open_runs"] == 1


def test_status_names_a_session_log_it_cannot_list_and_still_reports_the_rest(
        configured, monkeypatch):
    """R-1255: an unlistable session log is its own failure; runs and trees still report."""
    write_session(configured, sources={"labels": str(session.SourceState.REFUSED)})
    log = Path(session.log_dir(configured))
    _refuse_listing(monkeypatch, log)
    code, out, err = drive(["--output", "json", "status"])
    assert code == int(ExitCode.OK), err
    checks = {check["key"]: check for check in json.loads(out)["data"]["checks"]}
    assert "source.labels" not in checks
    named = checks["source.session-log"]
    assert named["status"] == "fail"
    assert f"the session log directory {log} exists and cannot be listed" in named["detail"]


def test_status_reads_one_damaged_record_as_a_record_not_as_an_unlisted_log(configured):
    write_session(configured, sources={"labels": str(session.SourceState.REFUSED)})
    (Path(session.log_dir(configured)) / "s-0-dead.json").write_text("{not json")
    code, out, err = drive(["--output", "json", "status"])
    assert code == int(ExitCode.OK), err
    keys = {check["key"] for check in json.loads(out)["data"]["checks"]}
    assert "source.labels" in keys
    assert "source.session-log" not in keys


def test_the_human_rendering_shows_the_checks_rather_than_only_a_status(configured, monkeypatch):
    green_probes(monkeypatch, keychain_available=lambda: False)
    _code, _out, err = drive(["doctor"])
    assert "keychain.reachable" in err
    assert render.remedy_text(Remedy.INSTALL_KEYCHAIN_BACKEND) in err


def test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb(
        configured, monkeypatch):
    """U97 (R-411): the procedure is offered, not bare ``crate login``, a line the verb is in."""
    session_credential = str(secrets.Credential.PROVIDER_SESSION)
    green_probes(monkeypatch, credential_recorded=lambda name: name != session_credential)
    _code, _out, err = drive(["doctor"])
    assert "credential.provider" in err
    assert "fix: crate login\n" not in err
    assert "crate login provider-session --from-file" in err
    assert "erase the plaintext file" in err
    assert "docs/adapters.md" in err


def test_the_cause_steps_are_not_printed_twice_beside_the_check_table():
    """The table lists each failure's fix, so the cause's steps are not repeated."""
    ffmpeg = {"key": "binary.ffmpeg", "title": "external binary ffmpeg", "detail": "not found"}
    report = doctor.Report((a_finding(**ffmpeg, remedy=Remedy.INSTALL_BINARY),))
    envelope = output.build(
        verb="doctor", run_id="r", schema=output.current_schema("diagnostic"),
        started="2026-08-02T00:00:00+00:00", outcome=Outcome.FAILED, code=ExitCode.PRECONDITION,
        data=report.payload(), cause=doctor.failure_cause(report))
    text = render.render(envelope)
    assert text.count("binary.ffmpeg") == 1
    assert "[FAIL]" in text


def test_a_check_table_is_rendered_only_for_the_diagnostic_surface():
    """Gated on the schema, not a ``checks`` key another surface may carry."""
    plan = output.build(
        verb="profile.set", run_id="r", schema=output.current_schema("plan"),
        started="2026-08-02T00:00:00+00:00",
        data={"digest": "d", "items": [], "totals": {}, "chunk": None})
    assert render.render_checks(plan) == []


# ═══ 7. The prompt module, and the guard it is exempt from ══════════════════


def test_a_prompt_that_cannot_be_answered_is_a_typed_refusal(monkeypatch):
    """Anything the reader raises is one type, so required and optional answers differ."""
    for boom in (EOFError("closed"), OSError("descriptor gone"), AssertionError("trapped")):

        def reader(exc=boom):
            raise exc
        asking = prompt.Prompter(read_line=reader, write=lambda _t: None)
        with pytest.raises(prompt.PromptUnavailable):
            asking.ask("anything")


def test_a_prompt_never_writes_to_standard_output(capsys):
    """R32: standard output carries exactly one JSON envelope, so no question goes there."""
    asking = prompt.Prompter(read_line=lambda: "yes\n")
    assert asking.confirm("proceed") is True
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "proceed" in captured.err


def test_an_answer_outside_a_closed_set_is_re_asked_and_then_abandoned():
    queued = ["nonsense", "rubbish", "drivel"]
    asking = prompt.Prompter(read_line=lambda: queued.pop(0) + "\n", write=lambda _t: None)
    with pytest.raises(prompt.PromptUnavailable):
        asking.choose("which", ["a", "b"], default="a")
    assert queued == [], "the bounded retry is what stops a pipe spinning forever"


def test_no_mapping_in_this_unit_has_a_key_written_twice():
    """No mapping literal writes a key twice, which parse time collapses unseen at runtime."""
    cli_dir = SRC_ROOT / "cratekit" / "cli"
    doctors = sorted(path.name for path in cli_dir.glob("doctor*.py"))
    for name in (*doctors, "setup.py", "prompt.py", "render.py"):
        source = (cli_dir / name).read_text()
        for node in ast.walk(ast.parse(source)):
            if not isinstance(node, ast.Dict):
                continue
            written = [
                ast.unparse(key)
                for key in node.keys
                if key is not None and isinstance(key, (ast.Constant, ast.Attribute))
            ]
            duplicates = sorted({k for k in written if written.count(k) > 1})
            assert not duplicates, f"{name} line {node.lineno}: written twice: {duplicates}"


def test_the_identity_check_never_reports_green_over_an_identity_that_did_not_match():
    """Identity is green only for the two outcomes meaning equal identities, never by default."""
    matched = {preflight.MountState.OK, preflight.MountState.LIBRARY_PATH_MISSING}
    for state in preflight.MountState:
        verdict, remedy = doctor_library._IDENTITY_VERDICT[state]
        assert (verdict is OK) == (state in matched), state
        assert (remedy is None) == (verdict is not FAIL), state


def test_a_volume_mounted_elsewhere_is_one_problem_reported_once(tmp_path, monkeypatch):
    """Only one of the two findings carries a fix, or a healthy drive gets unplugged."""
    root = tmp_path / "configured"
    (root / "Music").mkdir(parents=True)
    elsewhere = made(tmp_path / "actually-here")
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    report = report_on(root, **mounted_at(elsewhere))
    assert find(report, "library.mounted").status is FAIL
    identity = checked(find(report, "library.identity"), INFO, None)
    assert VOLUME in identity.detail


def test_an_unmounted_volume_never_reports_a_matching_identity(tmp_path, monkeypatch):
    absent = tmp_path / "not-mounted"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(absent))
    report = report_on(absent, **UNMOUNTED)
    identity = find(report, "library.identity")
    assert identity.status is not OK
    assert "matches" not in identity.detail


def test_every_mount_outcome_has_a_sentence_of_its_own():
    """The mapping over the mount enum is total, or a state renders as a ``KeyError``."""
    assert set(doctor_library._MOUNT_DETAIL) == set(preflight.MountState)
    assert len({str(v) for v in doctor_library._MOUNT_DETAIL.values()}) == len(preflight.MountState)


def test_a_seam_default_is_a_plain_function_and_never_a_bound_method():
    """Seam defaults stay plain functions (``slots=True``), never bound methods."""
    # These seams answer through the module owning the rule, asserted by identity.
    assert RealProbes().environment_credential is secrets.environment_value
    assert RealProbes().binary_override_problem is binaries.override_problem
    for holder in (RealProbes(), prompt.Prompter()):
        for field_name in holder.__dataclass_fields__:
            value = getattr(holder, field_name)
            assert not isinstance(value, types.MethodType), (
                f"{type(holder).__name__}.{field_name} arrived bound to its own "
                f"instance, so its first argument is now the holder")


def test_the_interactive_allowlist_still_holds_exactly_one_file():
    """``tests/test_cli_contract.py`` owns the allowlist; no second file joins it."""
    assert INTERACTIVE_ALLOWLIST == frozenset({"cratekit/cli/prompt.py"})
    assert (SRC_ROOT / "cratekit" / "cli" / "prompt.py").is_file()


# ═══ 8. A positive claim reached by falling through ═════════════════════════
# Each defect here reported OK by reaching the end of a function; each is driven
# on the machine that gave the false green and on the one where the answer is yes.


class _Volumes:
    """A synthetic mount directory, with the mount seam: ``attach`` or ``eject`` a volume."""

    def __init__(self, path):
        self.path = path
        self.mounted: set = set()

    def __truediv__(self, other):
        return self.path / other

    def resolve(self):
        return self.path.resolve()

    def attach(self, name):
        """A volume mounted at ``name``: the directory is there and IS a mount."""
        mount = (self.path / name).resolve()
        mount.mkdir(parents=True, exist_ok=True)
        self.mounted.add(mount)
        return mount

    def eject(self, name):
        """The leftover: the directory is there and nothing is mounted in it."""
        mount = (self.path / name).resolve()
        mount.mkdir(parents=True, exist_ok=True)
        self.mounted.discard(mount)
        return mount


@pytest.fixture
def volumes_directory(tmp_path, monkeypatch):
    """A synthetic, resolved directory this platform mounts volumes into."""
    volumes = made((tmp_path / "Volumes").resolve())
    synthetic = _Volumes(volumes)
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((volumes, 1),))
    monkeypatch.setattr(
        preflight, "is_mount_point", lambda path: Path(path).resolve() in synthetic.mounted)
    return synthetic


def test_the_wizard_will_not_read_an_identity_from_a_volume_that_is_not_there(volumes_directory):
    """With the drive unplugged no identity is derived, or the boot disk's would be (R38)."""
    absent = volumes_directory / "not-attached"
    boot = "BOOT-DISK-IDENTITY"
    cause = refused_derive(absent, boot)
    assert cause.remediation.remedy is Remedy.MOUNT_LIBRARY_VOLUME
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert boot not in str(cause.message), "the wrong identity was still read"
    assert "--volume-id" in cause.message


def test_an_identity_is_derived_when_the_root_really_is_on_the_volume(tmp_path):
    """The correct case still derives."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    wizard = setup_verb._Wizard({}, silent())
    derived = derive(root, VOLUME, wizard)
    assert derived == VOLUME
    assert any("read from the mounted volume" in line for line in wizard.asked)


def test_setup_refuses_end_to_end_rather_than_recording_the_boot_disk(
        tmp_path, monkeypatch, volumes_directory):
    """Through the dispatcher the refusal writes nothing, since an identity is never re-derived."""
    absent = volumes_directory / "not-attached"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(absent))
    green_probes(monkeypatch, identity_provider=lambda _p: "BOOT")
    code, _out, _err = drive(
        setup_argv(str(absent), tmp_path, "--db-path", str(absent / "db" / "master.db")))
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE)
    with pytest.raises(config.ConfigMissing):
        config.reset_cache()
        config.load()


def test_setup_writes_nothing_beside_the_library_until_the_volume_is_asserted(
        tmp_path, monkeypatch):
    """No library state is written until the volume is asserted (``/Volumes/NAME 1``)."""
    root = fresh_root(tmp_path, monkeypatch, "Volumes", "library")
    # The recorded identity is supplied; the write is against another disk.
    green_probes(monkeypatch, identity_provider=lambda _p: "0000")
    code, out, _err = setup_at(root, tmp_path)
    assert code == int(ExitCode.PRECONDITION)
    assert not (root / config.from_dict(document_for(root)).library.state_dirname).exists(), (
        "setup created its own state directory on a volume it had not asserted")
    assert not config.state_path("taxonomy_active", config.load()).exists()
    checks = {c["key"]: c for c in json.loads(out)["data"]["checks"]}
    assert checks["setup.taxonomy"]["status"] == "fail"
    assert checks["setup.taxonomy"]["remedy"] == str(Remedy.MOUNT_LIBRARY_VOLUME)


def test_the_wizard_still_writes_on_a_platform_that_reports_no_volume_identity(configured):
    """With no identity adapter the existing root is the signal, or nothing is ever written."""
    wizard = seeded(configured, probes(identity_provider=preflight.null_volume_identity))
    assert config.state_path("taxonomy_active", configured).is_file()
    assert all(note.status is not FAIL for note in wizard.notes)


def test_the_wizard_writes_the_active_template_once_the_volume_is_the_recorded_one(
        tmp_path, monkeypatch):
    """The correct case still writes."""
    root = fresh_root(tmp_path, monkeypatch, "Volumes", "library")
    green_probes(monkeypatch)
    setup_at(root, tmp_path)
    assert config.state_path("taxonomy_active", config.load()).is_file()


# ── session.unresolved: an empty scan is not an answer ───────────────────────


def test_an_unresolved_session_is_never_reported_clean_because_its_disk_is_gone(
        configured, tmp_path):
    """An empty scan of a missing log is not "none open"; ``scan_log`` cannot tell them apart."""
    write_session(configured, "s-9", workflow="route.inbox", state=UNVERIFIED)
    checked(finding_on(configured, "session.unresolved"), FAIL, Remedy.RESTORE_FROM_SNAPSHOT)
    # The volume goes with the log: no files, over a library nobody can vouch for.
    configured.library.root.rename(tmp_path / "detached")
    for machine in (
        probes(),  # the identity still matches further up: the ROOT is missing
        probes(**UNMOUNTED),
    ):
        finding = find(doctor.run(configured, probes=machine), "session.unresolved")
        assert finding.status is not OK, finding.detail
        assert "not asserted" in finding.detail
        assert "none of them open" not in finding.detail


def test_an_unreadable_session_log_directory_is_not_an_empty_one(configured):
    """The right disk and no permission is not an empty log, in this check's own sentence."""
    log = session.log_dir(configured)
    planted(log / "s-1.json", "{}")
    with _sealed(log):
        finding = finding_on(configured, "session.unresolved")
    assert finding.status is FAIL
    assert str(log) in finding.detail
    assert "did not complete" not in finding.detail, "the blanket rescue answered"
    assert "cannot be listed by this account" in finding.detail
    assert "An unreadable log is not an empty one" in finding.detail


def test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check(configured, monkeypatch):
    """R-1255: the same under root, where no mode bars the listing, in the probe's own sentence."""
    log = Path(session.log_dir(configured))
    planted(log / "s-1.json", "{}")
    _refuse_listing(monkeypatch, log)
    finding = checked(finding_on(configured, "session.unresolved"), FAIL)
    assert (
        f"the session log directory {log} exists and cannot be listed by this account"
        in finding.detail)
    assert "session record(s) in the log cannot be read" not in finding.detail


def test_a_library_with_no_sessions_still_reports_a_clean_log(configured):
    """The OK says what it established, not what it failed to find."""
    finding = checked(finding_on(configured, "session.unresolved"), OK)
    assert "on the recorded library volume was read" in finding.detail
    assert "0 recorded session(s), none of them open" in finding.detail


#: What each mount outcome permits, written out so a mutation must be made twice.
EXPECTED_READABLE = {
    "ok": "always",
    "library_path_missing": "never",
    "not_mounted": "never",
    "mounted_elsewhere": "never",
    "foreign_volume": "never",
    "identity_unavailable": "if-root-exists",
    "identity_not_recorded": "if-root-exists",
}
EXPECTED_WRITABLE = {
    "ok": "always",
    "library_path_missing": "always",
    "not_mounted": "never",
    "mounted_elsewhere": "never",
    "foreign_volume": "never",
    "identity_unavailable": "if-root-can-be-created",
    "identity_not_recorded": "if-root-can-be-created",
}


@pytest.mark.parametrize(
    "table, expected",
    [("_STATE_READABLE", EXPECTED_READABLE), ("_STATE_WRITABLE", EXPECTED_WRITABLE)])
def test_every_mount_outcome_permits_exactly_what_it_is_declared_to(table, expected):
    """Every row of both tables, since a shape check passes a state flipped in both."""
    mapping = getattr(preflight, table)
    assert set(mapping) == set(preflight.MountState), "the table is not total"
    assert {state.value: verdict.value for state, verdict in mapping.items()} == expected


def test_the_two_tables_differ_in_three_rows_and_every_one_is_a_read_signal_removed():
    """The tables differ in three rows, each a write a read answer must not decide."""
    readable = preflight._STATE_READABLE
    writable = preflight._STATE_WRITABLE
    differ = {state for state in readable if readable[state] != writable[state]}
    assert differ == {
        preflight.MountState.LIBRARY_PATH_MISSING,
        preflight.MountState.IDENTITY_UNAVAILABLE,
        preflight.MountState.IDENTITY_NOT_RECORDED,
    }


@pytest.mark.parametrize("state", ["IDENTITY_UNAVAILABLE", "IDENTITY_NOT_RECORDED"])
def test_a_platform_with_no_identity_adapter_may_create_a_library_it_cannot_read_yet(
        tmp_path, state):
    """With no identity adapter there is nothing to read, and creating the root is setup's job."""
    present = made(tmp_path / "library")
    not_yet = tmp_path / "not-created-yet"
    for root, readable, writable in ((present, True, True), (not_yet, False, True)):
        status = preflight.MountStatus(
            state=getattr(preflight.MountState, state), configured_root=root)
        assert preflight.library_state_is_readable(status) is readable
        assert preflight.library_state_may_be_written(status) is writable


def test_a_first_run_on_a_platform_with_no_identity_adapter_writes_its_template(
        configured, tmp_path):
    """Through the product seam, a first run with no root and no adapter writes its template."""
    configured.library.root.rename(tmp_path / "moved-away")
    wizard = seeded(configured, probes(identity_provider=preflight.null_volume_identity))
    assert config.state_path("taxonomy_active", configured).is_file()
    assert all(note.status is not FAIL for note in wizard.notes), [
        note.detail for note in wizard.notes
    ]


def test_a_renamed_library_folder_on_the_right_volume_is_written_not_refused(
        configured, tmp_path, monkeypatch):
    """A renamed folder on the right volume is written: the identity still matches."""
    configured.library.root.rename(tmp_path / "renamed-by-hand")
    wizard = seeded(configured)
    assert config.state_path("taxonomy_active", configured).is_file()
    assert all(note.status is not FAIL for note in wizard.notes), [
        note.detail for note in wizard.notes
    ]


def test_a_refusal_to_write_never_contradicts_its_own_parenthetical(configured):
    """A wrong volume is refused with a sentence the printed identities support."""
    wizard = seeded(configured, probes(identity_provider=lambda _p: "0000-0000"))
    note = checked(wizard.notes[0], FAIL)
    assert "could not establish" in note.detail
    assert "0000-0000" in note.detail and VOLUME in note.detail
    assert not config.state_path("taxonomy_active", configured).exists()


# ── taxonomy.active: two claims, neither of them checked ─────────────────────


def test_a_configured_template_that_ships_nowhere_is_refused(configured):
    """A configured template shipping nowhere is refused; ``validate`` accepts any bare token."""
    seed_taxonomy(configured)
    document = document_for(configured.library.root)
    document["taxonomy"] = {"template": "no-such-template"}
    finding = checked(finding_on(document, "taxonomy.active"), FAIL, Remedy.RUN_SETUP)
    assert "no-such-template" in finding.detail


def test_the_active_template_is_not_reported_at_all_when_its_disk_is_absent(configured):
    """With its disk absent the template is not reported, or setup would copy onto that path."""
    seed_taxonomy(configured)
    gone = probes(**UNMOUNTED)
    checked(find(doctor.run(configured, probes=gone), "taxonomy.active"), INFO, None)


def test_an_active_template_on_the_recorded_volume_reports_what_it_verified(configured):
    seed_taxonomy(configured)
    finding = checked(finding_on(configured, "taxonomy.active"), OK)
    assert "on the recorded library volume" in finding.detail
    assert "'default'" in finding.detail


# ── taxonomy.active: a stale copy told from an edited one (R-689) ────────────
# Doctor compares recorded, copy and shipped digests; a copy matching its record
# while the shipped text moved on is INFO.


def _seed_with_origin(cfg: config.Config) -> Path:
    """What setup leaves: the copy and the record, through the wizard's own code."""
    seeded(cfg)
    return config.state_path("taxonomy_origin", cfg)


def _copied_from(cfg: config.Config, older: str) -> None:
    """An active copy of ``older`` with the record setup writes, as if ``older`` had shipped."""
    write_active(cfg, older)
    origin = config.state_path("taxonomy_origin", cfg)
    origin.write_text(taxonomy.origin_record_text("default", older), encoding="utf-8")


def _taxonomy_finding(cfg: config.Config) -> doctor.Finding:
    return finding_on(cfg, "taxonomy.active")


def test_setup_records_which_shipped_text_the_copy_was_made_from(configured):
    origin = _seed_with_origin(configured)
    assert origin.is_file()
    assert origin.parent == config.state_path("taxonomy_active", configured).parent
    record = tomllib.loads(origin.read_text(encoding="utf-8"))
    shipped = setup_verb.template_text("default")
    assert record == {"template": "default", "sha256": taxonomy.template_digest(shipped)}
    assert config.state_path("taxonomy_active", configured).read_text(encoding="utf-8") == shipped


def test_setup_writes_no_record_for_a_copy_it_left_alone(configured):
    """Setup cannot know where an existing copy came from, so it records nothing."""
    seed_taxonomy(configured)
    origin = _seed_with_origin(configured)
    assert not origin.exists()


def test_a_copy_setup_made_that_the_shipped_template_has_since_outgrown_is_info(configured):
    """A copy still matching its record while the shipped text moved on is INFO."""
    older = shipped_without("long_tracks")
    _copied_from(configured, older)
    finding = checked(_taxonomy_finding(configured), INFO, None)
    assert "unedited" in finding.detail
    assert "[long_tracks]" in finding.detail
    assert "does not rewrite the copy" in finding.detail
    # Reported, never repaired: the copy is exactly what it was.
    assert config.state_path("taxonomy_active", configured).read_text(encoding="utf-8") == older


def test_a_copy_the_person_edited_is_theirs_whatever_the_shipped_template_did(configured):
    older = shipped_without("long_tracks")
    _copied_from(configured, older)
    active = config.state_path("taxonomy_active", configured)
    active.write_text("# mine\n" + older, encoding="utf-8")
    finding = checked(_taxonomy_finding(configured), OK)
    assert "edited since setup copied the shipped 'default'" in finding.detail
    assert "long_tracks" not in finding.detail


def test_a_copy_setup_made_from_the_text_that_still_ships_is_ok_and_says_so(configured):
    _seed_with_origin(configured)
    finding = checked(_taxonomy_finding(configured), OK)
    assert "unedited since setup copied the shipped 'default', which has not changed" in (
        finding.detail)


def test_a_copy_with_no_record_says_the_origin_is_unrecorded(configured):
    """With no record, a match is said, and a difference is undecidable."""
    seed_taxonomy(configured)
    matching = checked(_taxonomy_finding(configured), OK)
    assert "nothing records which shipped text" in matching.detail
    assert "matches the shipped 'default' as it ships now" in matching.detail
    write_active(configured, shipped_without("long_tracks"))
    differing = checked(_taxonomy_finding(configured), OK)
    assert "nothing records which shipped text" in differing.detail
    assert "cannot be told" in differing.detail
    assert "long_tracks" not in differing.detail


def test_a_record_that_cannot_be_used_is_said_rather_than_read_as_no_record(configured):
    origin = _seed_with_origin(configured)
    origin.write_text('template = "default"\nsha256 = "short"\n', encoding="utf-8")
    finding = checked(_taxonomy_finding(configured), INFO)
    assert "is not usable" in finding.detail
    assert "cannot be told" in finding.detail


def test_a_record_this_account_cannot_read_is_said_rather_than_read_as_no_record(configured):
    origin = _seed_with_origin(configured)
    with _sealed(origin):
        finding = _taxonomy_finding(configured)
    checked(finding, INFO, None)
    assert "could not be read" in finding.detail


def test_a_shipped_template_that_dropped_a_section_the_copy_still_has_is_named_too(configured):
    """A section the shipped template dropped is named, not claimed as inside shared ones."""
    older = shipped_without("long_tracks") + "\n[retired_section]\nkept = true\n"
    _copied_from(configured, older)
    finding = checked(_taxonomy_finding(configured), INFO)
    assert "it now declares [long_tracks], which the copy does not" in finding.detail
    assert "it no longer declares [retired_section], which the copy still does" in finding.detail


def test_a_shipped_change_inside_a_section_both_declare_is_said_as_such(configured):
    shipped = setup_verb.template_text("default")
    bucket = taxonomy.load_taxonomy(shipped).buckets[0]
    older = shipped.replace(f'display = "{bucket.display}"', 'display = "Older Name"', 1)
    assert older != shipped
    _copied_from(configured, older)
    finding = checked(_taxonomy_finding(configured), INFO)
    assert "the difference is inside sections both declare" in finding.detail
    assert "[" not in finding.detail.split("has changed since:")[1].split(".")[0]


def test_a_record_naming_a_template_other_than_the_configured_one_is_info(configured):
    origin = _seed_with_origin(configured)
    record = origin.read_text(encoding="utf-8").replace('template = "default"', 'template = "club"')
    origin.write_text(record, encoding="utf-8")
    finding = checked(_taxonomy_finding(configured), INFO)
    assert "made from the shipped 'club'" in finding.detail
    assert "taxonomy.template now names 'default'" in finding.detail
    assert "leaves an existing copy alone" in finding.detail


def test_a_packaged_text_that_cannot_be_read_is_a_damaged_install_and_compares_nothing(
        configured, monkeypatch):
    _seed_with_origin(configured)

    def unreadable(name: str) -> taxonomy.Fingerprint:
        raise OSError(errno.EIO, "packaged text", name)
    monkeypatch.setattr(taxonomy, "shipped_template_fingerprint", unreadable)
    finding = checked(_taxonomy_finding(configured), INFO)
    assert "could not be read" in finding.detail
    assert "damaged or partial install" in finding.detail


def test_a_record_that_cannot_be_written_does_not_uncopy_the_template(configured, monkeypatch):
    """A failed record write keeps the copy and names no remedy."""
    real = config.atomic_write_bytes
    active = config.state_path("taxonomy_active", configured)

    def refuse_second(data: bytes, path: Path, *args, **kwargs):
        if path != active:
            raise OSError(errno.EROFS, "read only", str(path))
        return real(data, path, *args, **kwargs)
    monkeypatch.setattr(config, "atomic_write_bytes", refuse_second)
    wizard = seeded(configured)
    assert active.is_file()
    assert not config.state_path("taxonomy_origin", configured).exists()
    notes = [n for n in wizard.notes if n.key == "setup.taxonomy"]
    assert [n.status for n in notes] == [INFO]
    assert "could not be written" in notes[0].detail
    assert "leaves the copy alone" in notes[0].detail
    assert notes[0].remedy is None


def test_the_origin_record_rolls_back_with_the_copy_it_describes():
    """A restored older copy under a newer record would read as edited."""
    entry = config.state_file("taxonomy_origin")
    assert entry.snapshot is config.SnapshotRole.COUPLED
    assert entry.root is config.StateRoot.LIBRARY
    assert entry.rollback_effects == (config.RollbackEffect.NONE,)


def test_a_taxonomy_typo_is_repaired_by_the_verb_whose_remedy_names_it(configured):
    """A recorded taxonomy outside the closed set is repaired by setup, as its remedy says."""
    document = dict(configured.to_toml_dict())
    document["taxonomy"] = {"template": "defualt"}
    wizard = setup_verb._Wizard(document, silent())
    answer = wizard.resolve(
        "taxonomy.template", flag=None, question="Which taxonomy template", default="default",
        choices=setup_verb.template_names())
    assert answer == "default"
    assert any("is not one of" in note.detail for note in wizard.notes)


def test_the_taxonomy_flag_is_a_closed_set_like_the_profile_beside_it(capsys):
    """argparse refuses a mistyped taxonomy before anything can persist it."""
    code, _out, _err = drive(["setup", "--taxonomy", "defualt"])
    assert code == int(ExitCode.USAGE)
    # argparse owns this message and its stream (KTD25 reserves status 2 for it).
    assert "invalid choice: 'defualt'" in capsys.readouterr().err


def test_a_template_name_shaped_like_a_path_is_a_configuration_problem(library):
    """A separator in a template name would read another packaged file, so validation refuses."""
    document = document_for(library)
    document["taxonomy"] = {"template": "../../etc/passwd"}
    assert any(config.TAXONOMY_TEMPLATE_KEY in p for p in config.validate(document))
    assert config.validate(document_for(library)) == []


# ── backup.remote: every provider nobody had gotten around to adding ─────────


@pytest.mark.parametrize("kind", ["onedrive", "box", "pcloud", "dropbox"])
def test_a_provider_with_a_recycle_bin_is_no_longer_green_by_default(configured, kind):
    """A provider with a recycle bin is not green just for lacking a table row."""
    finding = _remote_finding(configured, {"type": kind})
    assert finding.status is not OK, finding.detail


def test_a_provider_whose_no_trash_option_is_set_the_other_way_round_is_read_correctly(configured):
    """Drive's option must be false and OneDrive's true, each read the right way."""
    cfg = _archive_remote(configured)
    business = {"type": "onedrive", "drive_type": "business"}
    hardened = probes(rclone_remotes=lambda _r: {"archive": {**business, "hard_delete": "true"}})
    assert find(doctor.run(cfg, probes=hardened), "backup.remote").status is OK
    trashing = probes(rclone_remotes=lambda _r: {"archive": {**business, "hard_delete": "false"}})
    assert find(doctor.run(cfg, probes=trashing), "backup.remote").failed


@pytest.mark.parametrize("drive_type", ["personal", None])
@pytest.mark.parametrize("hard_delete", ["true", "false"])
def test_a_onedrive_remote_where_hard_delete_does_nothing_is_a_note(
        configured, drive_type, hard_delete):
    """OneDrive hard_delete works only on business drives and libraries, else a note."""
    settings = {"type": "onedrive", "hard_delete": hard_delete}
    if drive_type is not None:
        settings["drive_type"] = drive_type
    finding = checked(_remote_finding(configured, settings), INFO)
    assert f"drive_type is {drive_type or 'unset'}" in finding.detail


@pytest.mark.parametrize("extra", [{}, {"permanent_delete": "true"}])
def test_dropbox_is_not_told_to_set_an_option_rclone_does_not_have(configured, extra):
    """rclone's Dropbox backend has no per-remote delete option, so none is named."""
    finding = checked(_remote_finding(configured, {"type": "dropbox", **extra}), INFO)
    assert "permanent_delete" not in finding.detail
    assert "no per-remote option" in finding.detail


def test_a_remote_type_with_no_row_says_so_rather_than_passing(configured):
    finding = checked(_remote_finding(configured, {"type": "s3"}), INFO)
    assert "no row" in finding.detail


def test_a_remote_where_a_delete_is_a_delete_is_the_one_that_reports_green(configured):
    checked(_remote_finding(configured, {"type": "local"}), OK)


def test_the_remote_path_form_resolves_to_the_remote_it_names(configured):
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:library/archive"}
    cfg = config.from_dict(document)
    finding = finding_on(
        cfg, "backup.remote",
        rclone_remotes=lambda _r: {"archive": {"type": "drive", "use_trash": "false"}})
    assert finding.status is OK


def test_an_unknown_remote_is_not_sent_to_a_verb_that_cannot_fix_it(configured):
    """The wizard has no question, no flag and no code path for backup.remote."""
    finding = _remote_finding(configured, {"type": "local"}, name="other")
    checked(finding, FAIL, Remedy.FIX_CONFIG_VALUES)
    assert not any(
        "backup" in argument for entry in registry.entries() if entry.name == "setup"
        for argument in entry.doctor_checks)


# ── a broken override, a headless machine, and the metadata bound ────────────


def test_a_set_but_broken_binary_override_gets_the_remedy_that_exists_for_it(
        configured, tmp_path, monkeypatch):
    """A set but broken override gets ``FIX_BINARY_OVERRIDE``: installing would not help."""
    broken = planted(tmp_path / "not-executable", "")
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(broken))
    # The real rule against a real variable; the green machine answers None.
    machine = probes(find_binary=lambda _n: None, binary_override_problem=binaries.override_problem)
    finding = find(doctor.run(configured, probes=machine), "binary.ffmpeg")
    checked(finding, FAIL, Remedy.FIX_BINARY_OVERRIDE)
    assert str(broken) in finding.detail


def test_a_binary_that_is_simply_absent_still_says_install_it(configured):
    finding = finding_on(configured, "binary.ffmpeg", find_binary=lambda _n: None)
    assert finding.remedy is Remedy.INSTALL_BINARY


def test_a_headless_machine_that_opted_into_the_environment_fallback_is_not_red(
        configured, monkeypatch):
    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    for credential in secrets.Credential:
        monkeypatch.setenv(
            f"CRATEKIT_CREDENTIAL_{str(credential).upper().replace('-', '_')}", "value")
    seed_taxonomy(configured)
    machine = probes(
        keychain_available=lambda: False, environment_credential=secrets.environment_value)
    report = doctor.run(configured, probes=machine)
    checked(find(report, "keychain.reachable"), INFO)
    assert not report.failures, [f.key for f in report.failures]


def test_a_machine_with_no_keychain_and_no_fallback_is_still_red(configured):
    finding = finding_on(configured, "keychain.reachable", keychain_available=lambda: False)
    checked(finding, FAIL, Remedy.INSTALL_KEYCHAIN_BACKEND)


def test_a_fallback_supplying_only_some_of_what_is_needed_is_still_red(configured, monkeypatch):
    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    monkeypatch.setenv("CRATEKIT_CREDENTIAL_PROVIDER_SESSION", "value")
    machine = probes(
        keychain_available=lambda: False, environment_credential=secrets.environment_value)
    finding = checked(find(doctor.run(configured, probes=machine), "keychain.reachable"), FAIL)
    assert "identify-key" in finding.detail


# ── the containment report ──────────────────────────────────────────────────


def test_a_database_outside_the_library_root_is_reported_on_every_run(
        library, tmp_path, monkeypatch):
    """A database outside the root is reported every run: its snapshots span two filesystems."""
    document = document_for(library)
    document["library"]["db_path"] = str(tmp_path / "elsewhere" / "master.db")
    document["library"]["db_outside_root_acknowledged_on"] = "2026-08-01"
    finding = checked(finding_on(document, "library.db_containment"), INFO)
    assert str(tmp_path / "elsewhere" / "master.db") in finding.detail
    assert str(library) in finding.detail
    assert "2026-08-01" in finding.detail
    assert "two filesystems" in finding.detail


def test_a_contained_database_says_the_snapshot_commits_with_a_rename(configured):
    finding = checked(finding_on(configured, "library.db_containment"), OK)
    assert "under library.root" in finding.detail


# ── the Trash on the library volume, which deletion refuses without ──────────


def test_a_volume_whose_trash_accepts_a_move_reads_green(configured):
    finding = checked(finding_on(configured, "library.trash"), OK, None)
    assert str(configured.library.root) in finding.detail


def test_a_volume_with_no_usable_trash_refuses_because_a_verb_depends_on_it(configured):
    """R35 trashes a deletion, so no usable Trash fails here, with a remedy other than doctor."""
    finding = find(doctor.run(configured, probes=doctor_machines.hostile()), "library.trash")
    checked(finding, FAIL, Remedy.GRANT_PATH_ACCESS)
    assert "not writable" in finding.detail
    assert "never unlinks it" in finding.detail


def test_a_volume_with_no_trash_directory_yet_is_not_a_failure(configured):
    """No Trash yet is not red, the deletion pass creates it; doctor probes ``create=False``."""
    finding = finding_on(configured, "library.trash", trash_probe=doctor_machines._absent_trash)
    checked(finding, OK, None)
    assert "creates it on first use" in finding.detail


def test_the_two_probe_answers_that_made_the_false_red_are_really_different(tmp_path):
    """The real probe answers differently with and without ``create``, pinning the seam."""
    volume = tmp_path / "volume"
    (volume / "Music").mkdir(parents=True)
    home = tmp_path / "home"
    common = {"home": home, "uid": 501, "platform": "linux"}
    asked = trash.probe(volume, create=False, **common)
    made = trash.probe(volume, create=True, **common)
    assert not asked.usable and asked.absent, "doctor's question"
    assert made.usable, "the deletion pass's question, on the same volume"


def test_a_broken_trash_is_informational_when_no_verb_this_profile_needs_it(library):
    """With deletion off, nothing trashes a file, so a broken Trash is INFO."""
    document = document_for(library)
    document["profile"] = {"name": "slim"}
    cfg = config.from_dict(document)
    finding = finding_on(cfg, "library.trash", trash_probe=doctor_machines._no_trash)
    checked(finding, INFO, None)
    assert "nothing depends on it today" in finding.detail


def test_the_trash_check_cannot_pass_by_having_run(tmp_path, monkeypatch):
    """The seam binds ``create=False``, so the check cannot pass by creating the folder."""
    seen: list[dict] = []

    def recording(path, **kwargs):
        seen.append(dict(kwargs, path=path))
        return trash.TrashStatus(None, False, "not probed for real")
    monkeypatch.setattr(trash, "probe", recording)
    volume = tmp_path / "volume"
    (volume / "Music").mkdir(parents=True)
    doctor._probe_trash(volume)
    assert len(seen) == 1
    assert seen[0]["create"] is False, (
        "the doctor probe took the creating default, so the check can pass by having run")
    assert seen[0]["path"] == volume


def test_a_trash_probe_the_operating_system_refuses_is_a_failure_with_the_right_act(configured):
    """A refused probe fails, the act following the refusal: permission or read only volume."""

    def refuses(path):
        # With a filename, since ``access_refusal`` names a path.
        raise PermissionError(errno.EACCES, "Operation not permitted", str(path))
    finding = checked(finding_on(configured, "library.trash", trash_probe=refuses), FAIL)
    assert "could not be established" in finding.detail
    assert finding.remedy is not None
    assert finding.remedy is not Remedy.REPORT_DEFECT


def test_an_unanswerable_trash_probe_is_informational_when_no_verb_needs_it(library):
    """With deletion off, an unanswerable Trash probe is INFO, not a fault."""

    def refuses(path):
        raise PermissionError(errno.EACCES, "Operation not permitted", str(path))
    document = document_for(library)
    document["profile"] = {"name": "slim"}
    finding = checked(finding_on(document, "library.trash", trash_probe=refuses), INFO, None)
    assert "could not be established" in finding.detail


def test_the_trash_check_is_unchecked_when_there_is_no_configuration(tmp_path, monkeypatch):
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "empty"))
    config.reset_cache()
    finding = checked(finding_on(None, "library.trash"), INFO)
    assert "no usable configuration" in finding.detail


# ═══ 9. A truth teller that could refuse to run ═════════════════════════════
# A doctor that cannot start on a broken machine fails the machine it exists for.


class _StubResources:
    """``importlib.resources`` pointed at another root: a partial install, injected."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def files(self, _package: str) -> Path:
        return self.root


@pytest.fixture
def stripped_install(monkeypatch, tmp_path):
    """A cratekit whose templates directory does not exist."""
    monkeypatch.setattr(taxonomy, "resources", _StubResources(tmp_path / "pkg"))
    return tmp_path


@pytest.fixture
def unreadable_install(monkeypatch, tmp_path):
    """A cratekit whose templates directory exists and cannot be listed."""
    templates = made(tmp_path / "pkg" / "templates", parents=True)
    (templates / "taxonomy.default.toml").write_text("")
    monkeypatch.setattr(taxonomy, "resources", _StubResources(tmp_path / "pkg"))
    with _sealed(templates):
        yield tmp_path


@pytest.mark.parametrize("install", ["stripped_install", "unreadable_install"])
def test_the_whole_command_line_survives_an_install_with_no_readable_templates(
        install, request, configured, monkeypatch):
    """Every run builds every parser, so doctor and help survive missing or unreadable templates."""
    request.getfixturevalue(install)
    green_probes(monkeypatch)
    assert drive(["--help"])[0] == int(ExitCode.OK)
    code, out, err = drive(["--output", "json", "doctor"])
    assert code == int(ExitCode.PRECONDITION), err
    checks = {c["key"]: c for c in json.loads(out)["data"]["checks"]}
    # Packaged data unread, not an unknown name: run-setup cannot repair it.
    assert checks["taxonomy.active"]["status"] == "fail"
    assert "could not be listed" in checks["taxonomy.active"]["detail"]
    assert "not established" in checks["taxonomy.active"]["detail"]
    assert checks["taxonomy.active"]["remedy"] != "run-setup"


def test_a_missing_templates_directory_is_an_empty_answer_not_an_exception(stripped_install):
    assert taxonomy.shipped_template_names() == ()


def test_an_install_with_no_templates_offers_no_closed_set_rather_than_an_empty_one(
        stripped_install, tmp_path, monkeypatch):
    """With nothing shipped the flag has no closed set, since empty ``choices`` rejects all."""
    root = fresh_root(tmp_path, monkeypatch, "library")
    green_probes(monkeypatch)
    code, out, err = setup_at(root, tmp_path)
    assert code != int(ExitCode.USAGE), err
    checks = {c["key"]: c for c in json.loads(out)["data"]["checks"]}
    assert checks["setup.taxonomy"]["status"] == "fail"
    # A missing directory is a damaged install, as doctor says further down.
    assert "could not be listed" in checks["setup.taxonomy"]["detail"]
    assert "damaged or partial install" in checks["setup.taxonomy"]["detail"]
    assert checks["setup.taxonomy"]["remedy"] == str(Remedy.REPORT_DEFECT)


def test_a_shipped_name_configuration_would_reject_is_never_offered(monkeypatch, tmp_path):
    """A shipped name such as ``deep.house`` that validation refuses is never offered."""
    templates = made(tmp_path / "pkg" / "templates", parents=True)
    for name in ("taxonomy.default.toml", "taxonomy.deep.house.toml", "taxonomy..toml"):
        (templates / name).write_text("")
    monkeypatch.setattr(taxonomy, "resources", _StubResources(tmp_path / "pkg"))
    assert taxonomy.shipped_template_names() == ("default",)


def test_every_name_the_wheel_actually_ships_is_one_configuration_accepts(library):
    """The real packaged set, against the real validator."""
    shipped = taxonomy.shipped_template_names()
    assert shipped, "the wheel ships no taxonomy template"
    for name in shipped:
        document = document_for(library)
        document["taxonomy"] = {"template": name}
        assert config.validate(document) == [], name


# ── the derive guard ─────────────────────────────────────────────────────────


def test_a_library_folder_not_yet_created_under_a_real_mount_is_not_refused():
    """A library folder not yet created under an attached mount derives (the root is a mount)."""
    not_yet_created = Path("/") / "cratekit-library-that-does-not-exist"
    assert not not_yet_created.exists()
    assert preflight.deepest_existing(not_yet_created) == Path("/")
    assert derive(not_yet_created, VOLUME) == VOLUME


@pytest.mark.parametrize(
    "gap", ["library", "Music/library", "Music/a/b/library"], ids=["one", "two", "four"])
def test_a_library_nested_under_an_attached_volume_derives_at_any_depth(volumes_directory, gap):
    """Depth is not the hazard: a library at any depth under an attached volume derives."""
    attached = volumes_directory.attach("DISK_THAT_IS_ATTACHED")
    (attached / "Music" / "a" / "b").mkdir(parents=True, exist_ok=True)
    root = attached / gap
    assert not root.exists()
    assert derive(root, VOLUME) == VOLUME


def test_the_derive_still_refuses_when_the_mount_point_is_empty(volumes_directory):
    """With the drive unplugged ``/Volumes/NAME/Music`` refuses; a walk finds the disk above."""
    root = volumes_directory / "EP_LIBRARY" / "Music"
    assert preflight.deepest_existing(root) == volumes_directory.resolve()
    assert preflight.identity_source(root) is None
    cause = refused_derive(root, "BOOT")
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert "no volume is mounted there right now" in cause.message
    assert str(volumes_directory / "EP_LIBRARY") in cause.message


@pytest.mark.parametrize(
    "gap", ["", "library", "Music/library", "Music/a/b/library"],
    ids=["at-the-mount-point", "one", "two", "four"])
def test_an_ejected_volume_leaves_a_mount_POINT_behind_and_the_derive_refuses_it(
        volumes_directory, gap):
    """An ejected volume's leftover mount point is refused, not walked past to the boot disk."""
    leftover = volumes_directory.eject("EP_LIBRARY")
    (leftover / "Music" / "a" / "b").mkdir(parents=True, exist_ok=True)
    root = leftover / gap if gap else leftover
    boot = preflight.containing_mount(root)
    # The shape: the directory IS there, and it is not a mount.
    assert leftover.is_dir()
    assert boot != leftover
    assert preflight.identity_source(root) is None, "the boot disk was offered"
    assert preflight.root_can_be_created(root) is False
    assert refused_derive(root).code is ExitCode.LIBRARY_UNAVAILABLE


def test_the_identity_source_refuses_an_empty_mount_slot_and_nothing_else(
        tmp_path, volumes_directory):
    existing = made(tmp_path / "library")
    # No mount slot on the way down: the identity is its own volume's, asserted as a
    # property since the temporary directory's mount differs by machine.
    source = preflight.identity_source(existing)
    assert source is not None
    assert os.path.ismount(source), "an identity may only be read from a mount"
    assert source == existing or source in existing.parents
    # Missing directories at any depth would be created on the parent's volume.
    for gap in ("one", "one/two", "one/two/three/four"):
        answer = preflight.identity_source(tmp_path / gap)
        assert answer == source, gap
    # A mount slot with nothing in it, ABSENT.
    assert preflight.identity_source(volumes_directory / "DISK") is None
    assert preflight.identity_source(volumes_directory / "DISK" / "Music") is None
    # A mount slot with nothing in it, PRESENT as a leftover directory.
    volumes_directory.eject("DISK")
    assert preflight.identity_source(volumes_directory / "DISK") is None
    assert preflight.identity_source(volumes_directory / "DISK" / "Music") is None
    # A mount slot with a volume in it, at any depth below it.
    attached = volumes_directory.attach("DISK")
    assert preflight.identity_source(attached) is not None
    for gap in ("library", "Music/library", "Music/a/b/library"):
        assert preflight.identity_source(attached / gap) is not None, gap


def test_more_than_one_declared_depth_may_answer_and_only_one_is_the_mount(tmp_path, monkeypatch):
    """Every matching declared slot is asked; one mounted slot is enough."""
    media = (tmp_path / "media").resolve()
    mount = made(media / "phil" / "EP_LIBRARY", parents=True)
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((media, 1), (media, 2)))
    monkeypatch.setattr(preflight, "is_mount_point", lambda path: Path(path) == mount)
    assert preflight.mount_location_ancestors(mount / "library") == (mount, media / "phil")
    # The shallow slot is an ordinary directory and the deep one is the volume.
    assert preflight.identity_source(mount / "library") is not None
    # The mirror: the volume at the shallow slot, an ordinary subdirectory below.
    monkeypatch.setattr(preflight, "is_mount_point", lambda path: Path(path) == media / "phil")
    assert preflight.identity_source(media / "phil" / "sub" / "library") is not None


# ── an OK detail may claim only what the run established ────────────────────


def test_no_ok_detail_claims_a_volume_the_run_never_identified(configured):
    seed_taxonomy(configured)
    report = report_on(configured, identity_provider=preflight.null_volume_identity)
    assert find(report, "library.identity").status is FAIL
    for key in ("taxonomy.active", "session.unresolved"):
        finding = checked(find(report, key), OK)
        assert "recorded library volume" not in finding.detail, finding.detail
        assert "could not be compared" in finding.detail


def test_the_strong_claim_survives_where_the_identity_really_was_compared(configured):
    seed_taxonomy(configured)
    report = report_on(configured)
    for key in ("taxonomy.active", "session.unresolved"):
        assert "on the recorded library volume" in find(report, key).detail


# ── the credential store and its index never disagree ───────────────────────


def _refuse_the_index_lock(monkeypatch):
    """Make the presence index unlockable, the way a read-only state root does."""
    real_open = os.open

    def refuse(path, *args, **kwargs):
        if str(path).endswith("credential_index.lock"):
            raise PermissionError("no")
        return real_open(path, *args, **kwargs)
    monkeypatch.setattr(os, "open", refuse)


def test_a_refused_index_lock_leaves_the_keychain_untouched_on_a_record(monkeypatch):
    """The index lock is taken before the keychain write, so a refused lock changes nothing."""
    _refuse_the_index_lock(monkeypatch)
    with pytest.raises(secrets.CredentialIndexUnusable) as excinfo:
        secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    assert "NOTHING WAS CHANGED" in str(excinfo.value)
    assert not secrets.exists(secrets.Credential.IDENTIFY_KEY)
    with pytest.raises(secrets.CredentialMissing):
        secrets.get(secrets.Credential.IDENTIFY_KEY)


def test_a_refused_index_lock_leaves_the_keychain_untouched_on_a_delete(monkeypatch):
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    _refuse_the_index_lock(monkeypatch)
    with pytest.raises(secrets.CredentialIndexUnusable):
        secrets.delete(secrets.Credential.IDENTIFY_KEY)
    assert secrets.exists(secrets.Credential.IDENTIFY_KEY)
    assert secrets.get(secrets.Credential.IDENTIFY_KEY) == "value-from-the-user"


def test_a_delete_that_fails_between_the_two_stores_never_reports_green(monkeypatch):
    """The index entry goes first, so a failed delete leaves the safe disagreement."""
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")

    def refuse(_service, _name):
        raise RuntimeError("the keychain went away mid-delete")
    monkeypatch.setattr(keyring, "delete_password", refuse)
    with pytest.raises(secrets.CredentialBackendUnavailable):
        secrets.delete(secrets.Credential.IDENTIFY_KEY)
    assert not secrets.exists(secrets.Credential.IDENTIFY_KEY)


def test_recording_and_removing_still_work_when_the_lock_is_available():
    """The correct path, since every guard above is a refusal."""
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    assert secrets.exists(secrets.Credential.IDENTIFY_KEY)
    assert secrets.get(secrets.Credential.IDENTIFY_KEY) == "value-from-the-user"
    secrets.delete(secrets.Credential.IDENTIFY_KEY)
    assert not secrets.exists(secrets.Credential.IDENTIFY_KEY)


# ── the hook check, against what pre-commit actually writes ──────────────────


@pytest.mark.parametrize("filename", ["my config.yaml", "cfg(2).yaml", "plain.yaml"])
def test_a_hook_whose_configuration_name_needed_quoting_still_passes(library, tmp_path, filename):
    """A configuration name ``shlex.join`` quoted still passes, built with the real join."""
    checkout = tmp_path / "checkout"
    (checkout / ".git" / "hooks").mkdir(parents=True)
    (checkout / filename).write_text("repos: []\n")
    args = shlex.join(["hook-impl", f"--config={filename}", "--hook-type=pre-commit"])
    (checkout / ".git" / "hooks" / "pre-commit").write_text(
        f"#!/usr/bin/env bash\nARGS=({args})\nexec pre-commit \"${{ARGS[@]}}\"\n")
    finding = checked(hook_finding(library, checkout), OK)
    assert filename in finding.detail, "the detail names a file it did not check"


def test_the_hook_ok_names_the_configuration_it_actually_resolved(library, tmp_path):
    checkout = hooked_checkout(
        tmp_path / "checkout",
        "ARGS=(hook-impl --config=tools/hooks.yaml --hook-type=pre-commit)\n", config_file=False)
    (checkout / "tools").mkdir()
    (checkout / "tools" / "hooks.yaml").write_text("repos: []\n")
    finding = checked(hook_finding(library, checkout), OK)
    assert "tools/hooks.yaml" in finding.detail
    assert ".pre-commit-config.yaml" not in finding.detail


# ── two partial tables over one key space ───────────────────────────────────


def test_the_two_remote_tables_never_answer_for_the_same_type():
    """The two partial remote tables never overlap, or a type would have two answers."""
    overlap = set(doctor_backup._REMOTE_TRASH_POLICY) & doctor_backup._NON_TRASHING_REMOTE_TYPES
    assert not overlap, overlap
    for kind, policy in doctor_backup._REMOTE_TRASH_POLICY.items():
        assert policy.option is None or policy.disabled in ("true", "false"), kind
        # A gate on an option that does not exist is a gate on nothing.
        assert policy.applies_when is None or policy.option is not None, kind


# ── the write refusals, driven rather than read off the table ────────────────


def test_the_wizard_refuses_to_write_when_the_volume_is_not_mounted_at_all(configured, tmp_path):
    """NOT_MOUNTED is refused when driven, not only read off the table."""
    configured.library.root.rename(tmp_path / "detached")
    machine = probes(**UNMOUNTED)
    assert mount_state(configured, machine).state is preflight.MountState.NOT_MOUNTED
    wizard = seeded(configured, machine)
    assert wizard.notes[0].status is FAIL
    assert wizard.notes[0].remedy is Remedy.MOUNT_LIBRARY_VOLUME
    assert not config.state_path("taxonomy_active", configured).exists()
    assert not configured.library.root.exists(), "the refusal created the root anyway"


def test_the_wizard_refuses_to_write_when_the_volume_is_mounted_somewhere_else(
        configured, tmp_path):
    """MOUNTED_ELSEWHERE is refused: writing would send the real volume to ``<name> 1``."""
    elsewhere = made(tmp_path / "actually-here")
    machine = probes(**mounted_at(elsewhere))
    assert mount_state(configured, machine).state is preflight.MountState.MOUNTED_ELSEWHERE
    wizard = seeded(configured, machine)
    assert wizard.notes[0].status is FAIL
    assert not config.state_path("taxonomy_active", configured).exists()
    assert not (configured.library.root / configured.library.state_dirname).exists()


def test_the_zip_backed_shape_of_a_missing_packaged_directory_is_also_caught(monkeypatch, tmp_path):
    """"Never raises" holds for a zip-backed traversable, whose ``ValueError`` is no OSError."""
    class ZipBacked:
        name = "templates"

        def __truediv__(self, _other):
            return self

        def iterdir(self):
            raise ValueError("Can't listdir a file")

    class _Zip:
        def files(self, _package):
            return ZipBacked()
    monkeypatch.setattr(taxonomy, "resources", _Zip())
    assert taxonomy.shipped_template_names() == ()
    assert drive(["--help"])[0] == int(ExitCode.OK)


def test_the_presence_index_has_no_locking_helper_left_to_deadlock_on():
    """The index has no self-locking wrapper: ``flock`` per description would deadlock."""
    assert not hasattr(secrets, "_index_add")
    assert not hasattr(secrets, "_index_remove")
    assert hasattr(secrets, "_record_name") and hasattr(secrets, "_forget_name")


# ── a check that cannot answer says so, and the report survives ──────────────


def test_a_check_whose_probe_raises_becomes_a_failed_check_not_a_lost_report(configured, tmp_path):
    """A raising probe fails its check: a permission grants access, a fall keeps report-defect."""
    sealed = made(tmp_path / "sealed")
    inside = planted(sealed / "inside", "x")

    def blind():
        inside.read_text()
    with _sealed(sealed):
        report = report_on(configured, process_lister=blind)
    assert [f.key for f in report.findings] == list(doctor.CHECK_KEYS)
    broken = find(report, "rekordbox.closed")
    assert broken.status is FAIL, "unknown was reported as healthy"
    assert "did not complete" in broken.detail
    assert "PermissionError" in broken.detail
    assert broken.remedy is Remedy.GRANT_PATH_ACCESS
    assert "rather than a defect in this program" in broken.detail
    assert str(inside) in broken.detail, "a permission with no path to grant is unactionable"
    # The answers either side of it are the real ones.
    assert find(report, "interpreter.version").status is OK
    assert find(report, "library.identity").status is OK

    def fell_over():
        raise RuntimeError("psutil returned a shape this reader has never seen")
    ordinary = finding_on(configured, "rekordbox.closed", process_lister=fell_over)
    checked(ordinary, FAIL, Remedy.REPORT_DEFECT)


def test_the_rescue_reports_a_broken_check_as_FAIL_rather_than_as_a_note(configured):
    """A broken check is FAIL, never INFO, or ``report.ok`` stays true over no answer."""

    def explode(_inputs):
        raise RuntimeError("the probe fell over")
    finding = checked(doctor.answer(doctor.Check("made.up", explode), object()), FAIL)
    assert doctor.Report((finding,)).ok is False


def test_a_library_root_this_account_cannot_traverse_is_reported_not_raised(tmp_path, monkeypatch):
    """An untraversable ancestor is reported, though ``Path.exists`` re-raises."""
    sealed = tmp_path / "sealed"
    root = made(sealed / "library", parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(document_for(root))
    assert cfg.library.root == root, "the environment override moved the root"
    with _sealed(sealed):
        report = report_on(cfg)
    assert [f.key for f in report.findings] == list(doctor.CHECK_KEYS)
    assert report.ok is False
    mounted = checked(find(report, "library.mounted"), FAIL)
    assert "did not complete" in mounted.detail
    for finding in report.failures:
        assert finding.remedy is not Remedy.REPORT_DEFECT, finding.key
    assert find(report, "library.identity").remedy is Remedy.GRANT_PATH_ACCESS
    assert find(report, "taxonomy.active").remedy is Remedy.GRANT_PATH_ACCESS


def test_a_session_log_this_account_cannot_traverse_is_not_an_empty_one(configured, tmp_path):
    """An untraversable session log is not "no sessions", in the check's own sentence."""
    directory = session.log_dir(configured)
    directory.mkdir(parents=True, exist_ok=True)
    with _sealed(directory.parent):
        report = report_on(configured)
    finding = checked(find(report, "session.unresolved"), FAIL, Remedy.REPORT_DEFECT)
    assert "none of them open" not in finding.detail
    assert "cannot be listed by this account" in finding.detail
    assert str(directory) in finding.detail
    assert "did not complete" not in finding.detail, "the blanket rescue answered"


# ── present and unreadable is not the same answer as absent ──────────────────


def test_a_commit_hook_that_exists_and_cannot_be_read_is_not_a_missing_hook(configured, tmp_path):
    """An unreadable existing hook is unknown, not missing: git still runs it."""
    root = tmp_path / "checkout"
    (root / ".git" / "hooks").mkdir(parents=True)
    hook = root / ".git" / "hooks" / "pre-commit"
    hook.write_text("exec pre-commit hook-impl --hook-type=pre-commit\n")
    (root / ".pre-commit-config.yaml").write_text("repos: []\n")
    with _sealed(hook):
        unreadable = finding_on(configured, "repo.commit_hook", checkout_root=lambda: root)
    hook.unlink()
    absent = finding_on(configured, "repo.commit_hook", checkout_root=lambda: root)
    assert unreadable.status is absent.status is FAIL
    assert unreadable.detail != absent.detail, "one sentence for two conditions"
    assert "could not be read" in unreadable.detail
    assert "unknown rather than no" in unreadable.detail
    # Refused by the operating system, so the act is to grant access.
    assert unreadable.remedy is Remedy.GRANT_PATH_ACCESS
    assert "did not complete" not in unreadable.detail, "the blanket rescue answered"
    # An untraversable hooks directory raises this too.
    assert "exists at" not in unreadable.detail
    assert "no pre-commit hook" in absent.detail


def test_an_active_template_that_exists_and_cannot_be_read_is_not_a_missing_one(configured):
    """An unreadable template is not missing: run-setup leaves a copy alone and would loop."""
    seed_taxonomy(configured)
    path = config.state_path("taxonomy_active", configured)
    with _sealed(path):
        unreadable = finding_on(configured, "taxonomy.active")
    path.unlink()
    absent = finding_on(configured, "taxonomy.active")
    assert unreadable.status is absent.status is FAIL
    assert "could not be read" in unreadable.detail
    assert unreadable.remedy is not Remedy.RUN_SETUP
    # Refused by the operating system, so the act is to grant access.
    assert unreadable.remedy is Remedy.GRANT_PATH_ACCESS
    assert "did not complete" not in unreadable.detail, "the blanket rescue answered"
    # Not claimed present: an untraversable parent raises the same error.
    assert "exists and could not be read" not in unreadable.detail
    assert "whether the file is even there is unknown" in unreadable.detail.lower()
    assert "no active taxonomy template" in absent.detail
    assert absent.remedy is Remedy.RUN_SETUP


def test_an_unlistable_packaged_directory_is_not_a_shipped_set_of_none(
        configured, unreadable_install):
    names, problem = taxonomy.shipped_templates()
    assert names == ()
    assert problem is not None and "could not be listed" in problem
    # The parser-facing half still answers a list, so no verb dies here.
    assert taxonomy.shipped_template_names() == ()
    finding = checked(finding_on(configured, "taxonomy.active"), FAIL)
    assert "no template ships under that name" not in finding.detail
    assert "not established" in finding.detail
    assert finding.remedy is not Remedy.RUN_SETUP


def test_a_readable_packaged_directory_reports_no_problem_at_all(configured):
    """A readable directory reports no problem, so the problem is a signal."""
    names, problem = taxonomy.shipped_templates()
    assert problem is None
    assert "default" in names
    seed_taxonomy(configured)
    assert finding_on(configured, "taxonomy.active").status is OK


# ── the write leg of the reachability rule, both directions ──────────────────


def test_a_first_run_into_an_empty_mount_slot_may_not_write_library_state(volumes_directory):
    """A first run into an empty mount slot may not create the root (``<name> 1``)."""
    for root in (
        volumes_directory / "NOT_ATTACHED" / "library",       # absent slot
        volumes_directory.eject("EJECTED") / "library",       # leftover slot
    ):
        assert preflight.root_can_be_created(root) is False
        for state in (
            preflight.MountState.IDENTITY_UNAVAILABLE, preflight.MountState.IDENTITY_NOT_RECORDED
        ):
            status = preflight.MountStatus(state=state, configured_root=root)
            assert preflight.library_state_may_be_written(status) is False
            assert preflight.library_state_is_readable(status) is False
    attached = volumes_directory.attach("ATTACHED")
    assert preflight.root_can_be_created(attached / "library") is True


def test_the_mount_location_table_is_resolved_so_a_symlink_cannot_disarm_it(monkeypatch):
    """The mount table is resolved, or a symlinked temporary directory disarms the rule."""
    monkeypatch.setattr(preflight, "_VOLUME_MOUNT_LOCATIONS", {sys.platform: (("/tmp", 1),)})
    rows = preflight.volume_mount_locations()
    assert rows == ((Path("/tmp").resolve(), 1),)
    assert all(row[0] == row[0].resolve() for row in rows)


def test_where_each_platform_mounts_a_volume_is_declared_row_by_row():
    """Each platform's mount table spelled out, so an edit is made twice deliberately."""
    assert dict(preflight._VOLUME_MOUNT_LOCATIONS) == {
        # An external volume mounts one level under this directory.
        "darwin": (("/Volumes", 1),),
        # Removable media mounters, not ``/mnt``, which is for mounting by hand.
        "linux": (("/media", 1), ("/media", 2), ("/run/media", 2)),
    }
    assert ("/mnt", 1) not in preflight._VOLUME_MOUNT_LOCATIONS["linux"]
    # No other platform has a row; Windows refusing nothing is a residual.
    assert "win32" not in preflight._VOLUME_MOUNT_LOCATIONS


# ═══ 10. A guard that answers about something it did not observe ════════════
# Everything below drives both directions, since earlier corrections each also
# refused a correct install.


def _case_insensitive(directory: Path) -> bool:
    """Whether ``directory``'s volume folds case, asked of the volume, not the platform."""
    made(directory / "CaseProbe")
    return (directory / "caseprobe").is_dir()


def test_a_differently_cased_spelling_of_the_mount_directory_does_not_disarm_the_rule(tmp_path):
    """A lower-cased spelling disarms nothing, and two real directories are never conflated."""
    volumes = made((tmp_path / "Volumes").resolve())
    rows = ((volumes, 1),)
    lowered = Path(str(volumes).replace("Volumes", "volumes"))
    # The canonical spelling is a slot at the declared depth, always.
    assert preflight._is_a_volume_mount_location(volumes / "EP", rows) is True
    assert preflight._is_a_volume_mount_location(volumes / "EP" / "Music", rows) is False
    if _case_insensitive(tmp_path):
        assert lowered.is_dir(), "the filesystem folds case, so this is one directory"
        assert preflight._is_a_volume_mount_location(lowered / "EP", rows) is True
    else:  # pragma: no cover - only on a case-sensitive volume
        (tmp_path / "volumes").mkdir()
        assert preflight._is_a_volume_mount_location(lowered / "EP", rows) is False
    # A genuinely different directory is never conflated with the row.
    other = made(tmp_path / "VolumesElsewhere")
    assert preflight._is_a_volume_mount_location(other / "EP", rows) is False


def test_two_spellings_of_one_directory_are_one_directory_however_they_differ(tmp_path):
    """Two spellings of one directory compare equal through ``(st_dev, st_ino)``."""
    real = made(tmp_path / "Volumes")
    link = tmp_path / "linked-volumes"
    link.symlink_to(real, target_is_directory=True)
    assert preflight.names_one_path(real, real) is True
    assert preflight.names_one_path(link, real) is True
    assert preflight._is_a_volume_mount_location(link / "EP", ((real, 1),)) is True
    apart = made(tmp_path / "other")
    assert preflight.names_one_path(apart, real) is False
    # Neither side exists, so False, the accepting direction.
    assert preflight.names_one_path(tmp_path / "a", tmp_path / "b") is False
    # The filesystem's answer, so two different directories stay different.
    for left, right in ((real, real), (link, real), (apart, real), (real, apart)):
        assert preflight.names_one_path(left, right) is os.path.samefile(left, right)


def test_a_symlinked_mount_point_pointing_out_of_the_mount_directory_still_refuses(
        volumes_directory, tmp_path):
    elsewhere = tmp_path / "elsewhere"
    (elsewhere / "library").mkdir(parents=True)
    (volumes_directory.path / "SYMVOL").symlink_to(elsewhere, target_is_directory=True)
    root = volumes_directory / "SYMVOL" / "library"
    assert preflight.mount_location_ancestors(root) == (volumes_directory / "SYMVOL",)
    assert preflight.identity_source(root) is None
    assert preflight.root_can_be_created(root) is False
    assert refused_derive(root).code is ExitCode.LIBRARY_UNAVAILABLE


def test_a_symlinked_mount_point_that_names_a_real_mount_is_still_a_mounted_volume(
        volumes_directory, tmp_path):
    """A symlinked entry naming a real mount is a mounted volume, unlike ``ismount`` (P7)."""
    attached = volumes_directory.attach("REAL")
    (attached / "Music").mkdir(parents=True)
    (volumes_directory.path / "ALIAS").symlink_to(attached, target_is_directory=True)
    alias_root = volumes_directory / "ALIAS" / "Music"
    assert preflight.slot_holds_a_volume(volumes_directory / "ALIAS") is True
    assert preflight.identity_source(alias_root) is not None
    assert preflight.root_can_be_created(alias_root) is True


def test_a_declared_mount_directory_absent_from_this_machine_still_names_itself(
        tmp_path, monkeypatch):
    """An absent declared mount directory still names itself, by the equality shortcut."""
    absent = tmp_path.resolve() / "run" / "media"
    assert not absent.exists()
    assert preflight.names_one_path(absent, absent) is True
    root = absent / "phil" / "EP_LIBRARY" / "Music"
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((absent, 2),))
    monkeypatch.setattr(preflight, "is_mount_point", lambda _path: False)
    assert preflight.mount_location_ancestors(root) == (absent / "phil" / "EP_LIBRARY",)
    assert preflight.identity_source(root) is None


def test_the_walk_up_to_an_ancestor_never_clamps_at_the_filesystem_root(tmp_path):
    """The ancestor walk never clamps at ``/``, or one directory would match two depths."""
    anchor = Path(tmp_path.anchor)
    # Zero levels up is the mount directory; one level up is off the top.
    assert preflight._is_a_volume_mount_location(anchor, ((anchor, 0),)) is True
    assert preflight._is_a_volume_mount_location(anchor, ((anchor, 1),)) is False
    assert preflight._is_a_volume_mount_location(anchor / "Volumes", ((anchor, 1),)) is True


def test_a_library_reached_through_a_symlinked_parent_still_finds_its_slot(
        volumes_directory, tmp_path):
    """A library through a symlinked parent still finds its slot on the resolved chain."""
    shortcut = tmp_path / "EP_LIBRARY"
    shortcut.symlink_to(volumes_directory.path / "EXT", target_is_directory=True)
    root = shortcut / "Music"
    assert preflight.mount_location_ancestors(root) == (volumes_directory / "EXT",)
    assert preflight.identity_source(root) is None
    assert refused_derive(root).code is ExitCode.LIBRARY_UNAVAILABLE


def test_identity_source_asks_whether_the_slot_holds_a_volume_not_whether_it_is_one(
        tmp_path, monkeypatch):
    """``identity_source`` asks ``slot_holds_a_volume``, not ``is_mount_point`` (P7)."""
    volumes = made((tmp_path / "Volumes").resolve())
    (volumes / "ALIAS").symlink_to(Path(tmp_path.anchor), target_is_directory=True)
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((volumes, 1),))
    # The real seam, deliberately left alone.
    assert preflight.is_mount_point(volumes / "ALIAS") is False
    assert preflight.identity_source(volumes / "ALIAS" / "Music") is not None


def test_is_mount_point_is_the_one_fact_the_rule_turns_on_and_it_is_pinned(tmp_path, monkeypatch):
    """``is_mount_point`` delegates to ``os.path.ismount``, driven both ways."""
    ordinary = made(tmp_path / "not-a-mount")
    assert preflight.is_mount_point(Path(tmp_path.anchor)) is True
    assert preflight.is_mount_point(ordinary) is False
    # Absent or unstattable is False, the safe direction.
    assert preflight.is_mount_point(tmp_path / "never-existed") is False
    monkeypatch.setattr(os.path, "ismount", lambda path: str(path) == "sentinel")
    assert preflight.is_mount_point(Path("sentinel")) is True
    assert preflight.is_mount_point(Path(tmp_path.anchor)) is False


def test_a_linux_library_on_an_ordinary_directory_is_not_refused_forever(tmp_path, monkeypatch):
    """A Linux library at ``/mnt/<name>/music`` on an ordinary filesystem is not refused."""
    mnt = (tmp_path / "mnt").resolve()
    root = made(mnt / "data" / "music", parents=True)
    media = (tmp_path / "media").resolve()
    (media / "phil" / "EP_LIBRARY").mkdir(parents=True)
    # The shipped Linux rows, rebased under the temporary directory.
    rebased = tuple(
        ((tmp_path / directory.lstrip("/")).resolve(), depth)
        for directory, depth in preflight._VOLUME_MOUNT_LOCATIONS["linux"])
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: rebased)
    monkeypatch.setattr(preflight, "is_mount_point", lambda path: False)
    assert preflight.mount_location_ancestors(root) == ()
    assert preflight.identity_source(root) is not None
    assert preflight.root_can_be_created(root) is True
    status = preflight.MountStatus(
        state=preflight.MountState.IDENTITY_UNAVAILABLE, configured_root=root)
    assert preflight.library_state_may_be_written(status) is True
    assert preflight.library_state_is_readable(status) is True
    # A drive the automounter would place is refused while nothing is mounted there.
    detached = media / "phil" / "EP_LIBRARY" / "Music"
    assert preflight.mount_location_ancestors(detached) != ()
    assert preflight.identity_source(detached) is None
    assert preflight.root_can_be_created(detached) is False


def test_the_wizard_writes_the_active_template_on_a_linux_style_ordinary_directory(
        tmp_path, monkeypatch):
    root = (tmp_path / "mnt" / "data" / "music").resolve()
    (root / "Music").mkdir(parents=True)
    rebased = tuple(
        ((tmp_path / directory.lstrip("/")).resolve(), depth)
        for directory, depth in preflight._VOLUME_MOUNT_LOCATIONS["linux"])
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: rebased)
    monkeypatch.setattr(preflight, "is_mount_point", lambda path: False)
    green_probes(monkeypatch, identity_provider=preflight.null_volume_identity)
    code, out, err = setup_at(root, tmp_path)
    assert code != int(ExitCode.USAGE), err
    checks = {c["key"]: c for c in json.loads(out)["data"]["checks"]}
    assert checks["setup.taxonomy"]["status"] == "ok", checks["setup.taxonomy"]["detail"]
    config.reset_cache()
    assert config.state_path("taxonomy_active", config.load()).is_file()


def test_a_library_on_the_boot_disk_itself_is_not_refused(tmp_path):
    """A library on the boot disk crosses no declared mount location, at any depth."""
    here = made(tmp_path / "Music")
    assert preflight.identity_source(here) is not None
    assert preflight.root_can_be_created(here) is True
    # A first run: the root will be created on its parent's volume.
    assert preflight.root_can_be_created(tmp_path / "not" / "yet" / "here") is True


def test_a_platform_with_no_declared_row_refuses_nothing(tmp_path, monkeypatch):
    """An empty table refuses nothing rather than inventing a location."""
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ())
    monkeypatch.setattr(preflight, "is_mount_point", lambda path: False)
    assert preflight.mount_location_ancestors(tmp_path / "anything") == ()
    assert preflight.identity_source(tmp_path / "anything") is not None


# ── an unreadable .git marker is not a marker that names nothing ─────────────


def test_a_git_marker_that_cannot_be_read_is_not_a_marker_that_names_nothing(configured, tmp_path):
    """An unreadable ``.git`` marker is not one that names nothing (INFO, ``ok`` true)."""
    root = made(tmp_path / "checkout")
    marker = planted(root / ".git", "gitdir: /somewhere/else\n")
    with _sealed(marker):
        pointed, unreadable, remedy = doctor_model._git_dir(root)
        report = report_on(configured, checkout_root=lambda: root)
    assert pointed is None
    assert unreadable is not None and str(marker) in unreadable
    finding = checked(find(report, "repo.commit_hook"), FAIL, Remedy.GRANT_PATH_ACCESS)
    # Refused by the operating system, so a permission to grant, not a defect.
    assert remedy is Remedy.GRANT_PATH_ACCESS
    assert "unknown rather than no" in finding.detail
    assert "names no git directory" not in finding.detail
    assert report.ok is False, "doctor exited 0 over an unanswered commit scan"
    # A marker that was read and named nothing is still INFO with no remedy.
    marker.write_text("this is not a gitdir pointer\n")
    named_nothing = finding_on(configured, "repo.commit_hook", checkout_root=lambda: root)
    assert doctor_model._git_dir(root) == (None, None, None)
    # Not text: ``UnicodeDecodeError`` is a ``ValueError``, not an ``OSError``.
    marker.write_bytes(b"gitdir: \xff\xfe/somewhere\n")
    pointed, not_text, not_text_remedy = doctor_model._git_dir(root)
    assert pointed is None
    assert not_text is not None and "not readable text" in not_text
    # The bytes were read and would not decode, so this leg keeps report-defect.
    assert not_text_remedy is Remedy.REPORT_DEFECT
    assert named_nothing.status is INFO
    assert "names no git directory" in named_nothing.detail


def test_a_commondir_that_cannot_be_read_is_reported_rather_than_swallowed(configured, tmp_path):
    worktree, common = _worktree(tmp_path, b"../..\n")
    with _sealed(common / "worktrees" / "w1" / "commondir"):
        pointed, unreadable, remedy = doctor_model._git_dir(worktree)
        finding = finding_on(configured, "repo.commit_hook", checkout_root=lambda: worktree)
    assert pointed is None
    assert unreadable is not None and "commondir" in unreadable
    checked(finding, FAIL, Remedy.GRANT_PATH_ACCESS)
    assert remedy is Remedy.GRANT_PATH_ACCESS


def test_a_commondir_that_is_present_and_is_not_text_is_reported_too(configured, tmp_path):
    worktree, _common = _worktree(tmp_path, b"..\xff\xfe/..\n")
    pointed, unreadable, remedy = doctor_model._git_dir(worktree)
    finding = finding_on(configured, "repo.commit_hook", checkout_root=lambda: worktree)
    assert pointed is None
    assert unreadable is not None and "commondir" in unreadable
    checked(finding, FAIL, Remedy.REPORT_DEFECT)
    # Nothing was refused, so a damaged checkout keeps report-defect.
    assert remedy is Remedy.REPORT_DEFECT
    assert "did not complete" not in finding.detail, "the blanket rescue answered"


# ── the wizard reports a damaged install as a damaged install ────────────────


def test_the_wizard_tells_an_unlistable_template_directory_from_an_absent_name(
        configured, unreadable_install):
    """An unlistable template directory is a damaged install, agreeing with doctor."""
    cfg = configured
    note = seed_note(seeded(cfg))
    checked(note, FAIL, Remedy.REPORT_DEFECT)
    assert "could not be listed" in note.detail
    assert "damaged or partial install" in note.detail
    assert "no shipped template is named" not in note.detail
    assert "shipped: " not in note.detail, "an empty set was printed as a fact"
    # It agrees with what doctor says about the same install.
    doctor_finding = finding_on(cfg, "taxonomy.active")
    assert doctor_finding.remedy is note.remedy


def test_the_wizard_still_names_a_template_that_simply_does_not_ship(configured):
    """A listable set without the name is a config error the user can fix."""
    document = configured.to_toml_dict()
    document.setdefault("taxonomy", {})["template"] = "no-such-template"
    note = seed_note(seeded(config.from_dict(document)))
    checked(note, FAIL, Remedy.FIX_CONFIG_VALUES)
    assert "no shipped template is named 'no-such-template'" in note.detail
    assert "default" in note.detail, "the shipped set is named"


def test_a_template_that_ships_and_will_not_open_is_a_damaged_install_too(configured, monkeypatch):
    def refuse(_name):
        raise PermissionError(13, "Permission denied")
    monkeypatch.setattr(setup_verb, "template_text", refuse)
    note = seed_note(seeded(configured))
    checked(note, FAIL, Remedy.REPORT_DEFECT)
    assert "ships and its packaged text could not be read" in note.detail
    assert "damaged or partial install" in note.detail
    # Packaged bytes that are not text arrive as a ``ValueError``.

    def mojibake(_name):
        raise UnicodeDecodeError("utf-8", b"\xff\xfe", 0, 1, "invalid start byte")
    monkeypatch.setattr(setup_verb, "template_text", mojibake)
    note = seed_note(seeded(configured))
    checked(note, FAIL, Remedy.REPORT_DEFECT)
    assert "ships and its packaged text could not be read" in note.detail


def test_the_status_verb_survives_a_state_directory_that_cannot_be_walked(monkeypatch):
    """A state walk that refuses costs ``crate status`` its run records, not the verb."""

    class Refuses:
        def glob(self, _pattern):
            raise PermissionError(13, "Permission denied")
    monkeypatch.setattr(doctor.gates, "run_dir", lambda: Refuses())
    assert doctor._run_findings() == []


# ── a structured refusal is an answer, not a check that broke ────────────────


def _refusing_check(key: str = "library.mounted") -> doctor.Check:
    """A check that REFUSES under a declared reason with a reserved code."""

    def run(_inputs):
        raise CratekitError(
            Cause(
                reason="library-volume-unmounted",
                message="the library volume is not mounted",
                remediation=Remediation(
                    remedy=Remedy.MOUNT_LIBRARY_VOLUME, steps=("attach the drive",)),
                scope=Scope.RUN,
                origin=("tests",),
            ))
    return doctor.Check(key, run)


def test_a_structured_refusal_keeps_its_reason_remedy_steps_and_reserved_code():
    inputs = doctor._Inputs(None, None, probes())
    finding = doctor.answer(_refusing_check(), inputs)
    checked(finding, FAIL, Remedy.MOUNT_LIBRARY_VOLUME)
    assert "did not complete" not in finding.detail
    assert "attach the drive" in finding.detail
    assert finding.cause is not None
    assert finding.cause.reason == "library-volume-unmounted"
    cause = doctor.failure_cause(doctor.Report((finding,)))
    assert cause.reason == "library-volume-unmounted"
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert "attach the drive" in cause.remediation.steps
    assert cause.remediation.remedy is Remedy.MOUNT_LIBRARY_VOLUME


def test_an_unstructured_break_is_still_rescued_as_a_check_that_did_not_complete():
    """An unstructured break is still rescued, so the report survives."""
    def explode(_inputs):
        raise RuntimeError("psutil said no")
    inputs = doctor._Inputs(None, None, probes())
    finding = doctor.answer(doctor.Check("library.mounted", explode), inputs)
    checked(finding, FAIL, Remedy.REPORT_DEFECT)
    assert finding.cause is None
    assert "did not complete" in finding.detail
    assert doctor.failure_cause(doctor.Report((finding,))).reason == "doctor-check-failed"


def test_a_report_with_no_structured_refusal_still_exits_precondition(configured):
    report = report_on(configured, find_binary=lambda _n: None)
    assert report.ok is False
    cause = doctor.failure_cause(report)
    assert cause.reason == "doctor-check-failed"
    assert cause.code is ExitCode.PRECONDITION


def test_doctor_leaves_under_the_code_a_refusing_check_reserved(monkeypatch, configured):
    """Through the real dispatcher, since the code is the contract."""
    monkeypatch.setattr(doctor, "CHECKS", (_refusing_check(),))
    code, out, _err = drive(["--output", "json", "doctor"])
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE)
    assert json.loads(out)["cause"]["reason"] == "library-volume-unmounted"


def test_the_rescue_still_lets_the_three_control_exceptions_through():
    """The three control exceptions pass through, or a Ctrl-C becomes a green check."""
    inputs = doctor._Inputs(None, None, probes())
    for kind in (KeyboardInterrupt, SystemExit, GeneratorExit):
        def raiser(_inputs, _kind=kind):
            raise _kind()
        with pytest.raises(kind):
            doctor.answer(doctor.Check("library.mounted", raiser), inputs)
    # A MemoryError is caught, since the report is worth more than the check.

    def hungry(_inputs):
        raise MemoryError()
    assert doctor.answer(doctor.Check("k", hungry), inputs).status is FAIL


# ── an ancestor this account cannot traverse ─────────────────────────────────


@pytest.fixture
def sealed_ancestor(tmp_path):
    """A library root under a directory this account cannot traverse (no Full Disk Access)."""
    sealed = made(tmp_path / "sealed")
    (sealed / "lib").mkdir()
    with _sealed(sealed):
        yield sealed / "lib"


def test_the_wizard_refuses_an_unreachable_ancestor_rather_than_filing_a_defect(sealed_ancestor):
    cause = refused_derive(sealed_ancestor, "X")
    assert cause.reason == "library-root-unreachable"
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert str(sealed_ancestor) in cause.message
    assert "Full Disk Access" in cause.message
    assert render.remedy_text(Remedy.GRANT_PATH_ACCESS)


def test_setup_end_to_end_names_the_path_instead_of_asking_for_a_bug_report(
        sealed_ancestor, tmp_path, monkeypatch):
    """Through the real dispatcher, where the defect was visible."""
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(sealed_ancestor))
    green_probes(monkeypatch)
    code, out, err = drive(
        setup_argv(
            str(sealed_ancestor), tmp_path, "--db-path", str(sealed_ancestor / "db" / "master.db")))
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), err
    envelope = json.loads(out)
    assert envelope["cause"]["reason"] == "library-root-unreachable"
    assert envelope["cause"]["reason"] != "internal-error"
    assert "report it" not in envelope["cause"]["remediation"].get("remedy", "")
    # The slug itself, since it persists into every stored cause.
    assert envelope["cause"]["remediation"]["remedy"] == "grant-path-access"


def test_the_taxonomy_seed_reports_an_unreachable_root_rather_than_raising(
        sealed_ancestor, monkeypatch):
    """The taxonomy seed notes an unreachable root rather than raising after the save."""
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(sealed_ancestor))
    cfg = config.from_dict(document_for(sealed_ancestor))
    assert Path(cfg.library.root) == sealed_ancestor
    note = seed_note(seeded(cfg))
    checked(note, FAIL, Remedy.GRANT_PATH_ACCESS)
    assert "Full Disk Access" in note.detail
    assert str(sealed_ancestor) in note.detail


def test_the_seed_reports_a_state_directory_it_could_not_look_into(library):
    """An untraversable ``.cratekit`` under a reachable root is noted, not a defect."""
    cfg = config.from_dict(document_for(library))
    state = config.state_path("taxonomy_active", cfg).parent
    state.mkdir(parents=True, exist_ok=True)
    wizard = setup_verb._Wizard({}, silent())
    with _sealed(state):
        setup_verb._seed_taxonomy(wizard, cfg, probes())
    note = seed_note(wizard)
    checked(note, FAIL, Remedy.GRANT_PATH_ACCESS)
    assert "could not be examined" in note.detail
    assert "Full Disk Access" in note.detail


def test_the_seed_reports_a_write_it_was_refused_rather_than_filing_a_defect(library):
    """A refused write is noted with its own act, not the read only one."""
    cfg = config.from_dict(document_for(library))
    state = config.state_path("taxonomy_active", cfg).parent
    state.mkdir(parents=True, exist_ok=True)
    wizard = setup_verb._Wizard({}, silent())
    # Readable, listable, and not writable.
    with _sealed(state, mode=0o500):
        setup_verb._seed_taxonomy(wizard, cfg, probes())
    note = seed_note(wizard)
    checked(note, FAIL, Remedy.GRANT_PATH_ACCESS)
    assert "could not be written" in note.detail
    assert "Full Disk Access" in note.detail
    # The act for the other kind is absent, since it did not occur.
    assert "mounted read only" not in note.detail
    assert "chflags nouchg" not in note.detail
    # It does not claim the path could not be looked at.
    assert "could not be examined" not in note.detail
    assert not config.state_path("taxonomy_active", cfg).exists()


def test_the_grant_path_access_advice_claims_neither_act_over_the_other(library):
    """One token covers two conditions, so its advice asserts neither."""
    advice = render.remedy_text(Remedy.GRANT_PATH_ACCESS)
    assert advice
    assert "cannot reach or write" in advice
    assert "on the way to" not in advice


def test_doctor_still_answers_every_check_over_an_unreachable_root(sealed_ancestor, monkeypatch):
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(sealed_ancestor))
    report = report_on(sealed_ancestor)
    assert tuple(f.key for f in report.findings) == doctor.CHECK_KEYS
    mounted = checked(find(report, "library.mounted"), FAIL)
    assert "did not complete" in mounted.detail


# ── one classification, made once, for a permission the user can grant ───────
# ``cause.permission_denied`` answers, ``cause.access_remedy`` chooses the act;
# driven on real 0o000 directories.


@pytest.mark.parametrize("arrangement", ["configuration-directory", "library-root"])
def test_both_verbs_answer_a_real_permission_with_an_act_the_user_can_perform(
        tmp_path, monkeypatch, arrangement):
    """A sealed root or config directory gets, from both verbs, an act the user can do."""
    sealed = tmp_path / "sealed"
    (sealed / "cfg").mkdir(parents=True)
    library = (sealed / "lib") if arrangement == "library-root" else (tmp_path / "library")
    if arrangement == "library-root":
        library.mkdir()
        monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "cfg"))
    else:
        monkeypatch.setenv(config.ENV_CONFIG_DIR, str(sealed / "cfg"))
    config.reset_cache()
    green_probes(monkeypatch)
    argv = setup_argv(str(library), tmp_path, "--db-path", str(library / "db" / "master.db"))
    if arrangement == "configuration-directory":
        # The identity is supplied, so the run reaches the configuration file.
        argv += ["--volume-id", VOLUME]
    with _sealed(sealed, reset_config=True):
        doctor_code, doctor_out, doctor_err = drive(["--output", "json", "doctor"])
        setup_code, setup_out, setup_err = drive(argv)
    surfaces = [(setup_code, setup_out, setup_err)]
    if arrangement == "configuration-directory":
        # Doctor reports on the config it could not load.
        surfaces.append((doctor_code, doctor_out, doctor_err))
    for code, out, err in surfaces:
        cause = json.loads(out)["cause"]
        assert cause["remediation"]["remedy"] == "grant-path-access", err
        assert "report it" not in err
        assert "report-defect" not in out
        assert str(sealed) in cause["message"]
        assert cause["detail"]["path"] is not None
        if arrangement == "library-root":
            assert cause["reason"] == "library-root-unreachable"
            assert code == int(ExitCode.LIBRARY_UNAVAILABLE)
        else:
            assert cause["reason"] == "path-permission-denied"
            assert code == int(ExitCode.PRECONDITION)
            assert f"The path is {cause['detail']['path']}." in cause["message"]


def test_the_help_screen_survives_a_configuration_directory_it_cannot_open(
        tmp_path, monkeypatch, capsys):
    """``crate --help`` survives a sealed config directory, read during parser construction."""
    sealed = tmp_path / "sealed"
    (sealed / "cfg").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(sealed / "cfg"))
    config.reset_cache()
    with _sealed(sealed, reset_config=True):
        code, _out, _err = drive(["--help"])
    assert code == int(ExitCode.OK)
    assert "usage: crate" in capsys.readouterr().out


def test_a_mount_slot_this_account_cannot_stat_is_not_an_empty_mount_slot(tmp_path):
    """A slot this account cannot stat is not empty, behind a sealed parent or sealed itself."""
    behind_a_seal = tmp_path / "sealed"
    (behind_a_seal / "EXT").mkdir(parents=True)
    itself = made(tmp_path / "EXT2")
    with _sealed(behind_a_seal, itself):
        with pytest.raises(PermissionError):
            preflight.is_mount_point(behind_a_seal / "EXT")
        with pytest.raises(PermissionError):
            preflight.is_mount_point(itself)
    # The real answers are unchanged: absent is False, from the standard library.
    assert preflight.is_mount_point(tmp_path / "never-existed") is False
    assert preflight.is_mount_point(itself) is False
    assert preflight.is_mount_point(Path(tmp_path.anchor)) is True


def test_the_wizard_does_not_claim_an_unmounted_volume_it_could_not_observe(tmp_path, monkeypatch):
    """End to end, an unobservable slot refuses as unopened, not as unmounted."""
    volumes = made((tmp_path / "Volumes").resolve())
    slot = volumes / "EXT"
    root = made(slot / "Music", parents=True)
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((volumes, 1),))
    with _sealed(slot):
        cause = refused_derive(root, "X")
    assert cause.reason == "library-root-unreachable"
    assert cause.reason != "library-volume-unmounted"
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert "no volume is mounted there right now" not in cause.message
    assert "Attach the library volume" not in cause.message
    assert str(root) in cause.message


def test_one_pair_of_paths_does_not_get_two_answers_decided_by_permission(tmp_path, monkeypatch):
    """``samefile`` does not answer "different" when it could not stat."""
    sealed = tmp_path / "sealed"
    (sealed / "Volumes").mkdir(parents=True)
    declared = sealed / "Volumes"
    ordinary = made(tmp_path / "elsewhere")
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((declared, 1),))
    assert preflight.names_one_path(declared, declared) is True
    assert preflight.names_one_path(ordinary, declared) is False
    with _sealed(sealed):
        # The identical pair may not silently become "different".
        with pytest.raises(PermissionError):
            preflight.names_one_path(ordinary, declared)
        # The rule refuses rather than falling to the boot disk.
        with pytest.raises(PermissionError):
            preflight.mount_location_ancestors(ordinary / "EP" / "Music")
    # Absent on both sides is still False: nothing was refused.
    assert preflight.names_one_path(tmp_path / "a", tmp_path / "b") is False


def test_the_database_probe_survives_a_recorded_path_it_cannot_stat(tmp_path, monkeypatch):
    """An unstattable database path does not kill setup and is still proposed."""
    root = tmp_path / "library"
    locked = made(root / "db", parents=True)
    (root / "Music").mkdir()
    (locked / "master.db").write_bytes(b"")
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "cfg"))
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    config.reset_cache()
    monkeypatch.setattr(
        setup_verb.rb_writer, "read_rekordbox_settings",
        lambda: {"db_path": str(locked / "master.db")})
    green_probes(monkeypatch)
    with _sealed(locked, reset_config=True):
        assert setup_verb._probe_db_path() == str(locked / "master.db")
        code, out, err = drive(setup_argv(str(root), tmp_path, "--volume-id", VOLUME))
    envelope = json.loads(out)
    assert code != int(ExitCode.INTERNAL), err
    assert envelope.get("cause", {}).get("reason") != "internal-error"
    assert "report-defect" not in out
    # The verb completed with the proposal taken as the default.
    assert config.load().library.db_path == locked / "master.db"


def test_an_unreadable_backup_fact_file_is_a_permission_not_a_corruption(configured):
    path = planted(backup_facts.path_for(configured), '{"schema_version": 1, "portions": {}}')
    with _sealed(path):
        report = report_on(configured)
    for portion in backup_facts.PORTIONS:
        finding = checked(find(report, f"backup.age.{portion}"), FAIL, Remedy.GRANT_PATH_ACCESS)
        assert "repair or reset" not in (render.remedy_text(finding.remedy) or "")
        assert "exists but could not be read" not in finding.detail
    # A real corruption still asks for a repair.
    path.write_text("this is not JSON at all")
    checked(finding_on(configured, "backup.age.files"), FAIL, Remedy.REPAIR_BACKUP_FACTS)


def test_an_active_template_that_is_present_and_is_not_text_is_reported(configured):
    path = config.state_path("taxonomy_active", configured)
    planted(path, b"trees:\n  - name: \xff\xfe\n")
    finding = finding_on(configured, "taxonomy.active")
    checked(finding, FAIL, Remedy.REPORT_DEFECT)
    assert "could not be read" in finding.detail
    assert "did not complete" not in finding.detail, "the blanket rescue answered"
    # Nothing was refused by the operating system, so this one is a repair.


def test_a_commit_hook_that_is_present_and_is_not_text_is_reported(configured, tmp_path):
    """The same decode leg at ``repo.commit_hook``."""
    root = tmp_path / "checkout"
    (root / ".git" / "hooks").mkdir(parents=True)
    (root / ".pre-commit-config.yaml").write_text("repos: []\n")
    (root / ".git" / "hooks" / "pre-commit").write_bytes(b"#!/bin/sh\n\xff\xfe\n")
    finding = finding_on(configured, "repo.commit_hook", checkout_root=lambda: root)
    checked(finding, FAIL, Remedy.REPORT_DEFECT)
    assert "could not be read" in finding.detail
    assert "did not complete" not in finding.detail, "the blanket rescue answered"


def test_the_classification_reads_the_declared_cause_and_not_the_context(tmp_path):
    denied = PermissionError(13, "refused")
    assert cause_module.permission_denied(denied) is denied
    assert cause_module.permission_denied(RuntimeError("fell over")) is None
    assert cause_module.permission_denied(None) is None
    # The errno is read as well as the class.
    rebuilt = OSError("the operating system refused this account")
    rebuilt.errno = errno.EACCES
    assert type(rebuilt) is OSError
    assert cause_module.permission_denied(rebuilt) is rebuilt
    other = OSError("no such file")
    other.errno = errno.ENOENT
    assert cause_module.permission_denied(other) is None
    declared = RuntimeError("wrapped")
    declared.__cause__ = denied
    assert cause_module.permission_denied(declared) is denied
    try:
        try:
            raise denied
        except PermissionError:
            raise ValueError("a defect discovered while handling it")
    except ValueError as exc:
        assert exc.__context__ is denied
        assert cause_module.permission_denied(exc) is None
    # ``access_remedy`` requires a path; ``permission_denied`` only decides to re-raise.
    named = PermissionError(13, "refused", str(tmp_path / "sealed" / "inside"))

    def remedy(error):
        return cause_module.access_remedy(error, otherwise=Remedy.REPORT_DEFECT)
    assert remedy(named) is Remedy.GRANT_PATH_ACCESS
    assert remedy(RuntimeError("x")) is Remedy.REPORT_DEFECT
    no_path = "a refusal naming no path has no path to grant access to"
    assert remedy(denied) is Remedy.REPORT_DEFECT, no_path


# ═══ The classification lives where a refusal is constructed ════════════════
# Every structured refusal passes through ``cause.classified``; driven with real
# permissions, a read only volume, a locked file and the state store's driver error.


def test_a_sealed_state_database_answers_with_its_path_and_an_act(tmp_path, monkeypatch):
    """A sealed ``queue.db`` answers with its path and an act, recorded at the connection."""
    isolated_library(tmp_path, monkeypatch, save=True)
    code, _out, _err = drive(["--output", "json", "job", "list"])
    assert code == 0, "the arrangement itself must be green before it is broken"
    queue = jobs.queue_path()
    assert queue.exists()
    with _sealed(queue):
        code, out, err = drive(["--output", "json", "job", "list"])
    cause = json.loads(out)["cause"]
    assert cause["reason"] == "path-permission-denied", cause
    assert cause["remediation"]["remedy"] == "grant-path-access"
    assert cause["detail"]["path"] == str(queue)
    assert str(queue) in cause["message"]
    assert code == int(ExitCode.PRECONDITION)
    assert "report it" not in err
    assert "report-defect" not in out


def test_a_refusal_that_names_no_path_does_not_claim_one(tmp_path, monkeypatch):
    isolated_library(tmp_path, monkeypatch, save=True)

    def refused(_ctx):
        # A real pathless refusal: signal 0 to pid 1. Root would fail loudly here.
        os.kill(1, 0)
        raise AssertionError("this account signalled pid 1, so the arrangement is void")
    monkeypatch.setattr(jobs_cli, "list_jobs", refused)
    code, out, err = drive(["--output", "json", "job", "list"])
    cause = json.loads(out)["cause"]
    assert cause["reason"] == "internal-error", cause
    assert cause["remediation"]["remedy"] == "report-defect"
    assert "path named below" not in err
    assert "the arrangement is void" not in cause["message"]
    assert code == int(ExitCode.INTERNAL)
    # The sentence is not produced at all, rather than produced empty.
    assert render.access_note(PermissionError(1, "Operation not permitted")) is None


def test_a_read_only_volume_is_not_sent_to_full_disk_access(tmp_path):
    """A read only volume gets the remount act, not Full Disk Access (real EROFS)."""
    refused = root_volume_refusal("cratekit-u27-read-only-probe")
    assert refused.errno == errno.EROFS, (
        f"this machine's root volume answered {refused.errno} rather than EROFS, "
        f"so the arrangement is not a read only volume")
    refusal = cause_module.access_refusal(refused)
    assert refusal is not None, "a read only volume was read as an unanticipated failure"
    assert refusal.kind is cause_module.AccessKind.READ_ONLY
    assert refusal.path == "/cratekit-u27-read-only-probe"
    assert refusal.remedy is Remedy.REMOUNT_WRITABLE
    assert refusal.reason == "path-read-only"
    words = render.remedy_text(Remedy.REMOUNT_WRITABLE)
    assert "Full Disk Access" not in words
    assert "read only" in words
    note = render.access_note(refused)
    assert "/cratekit-u27-read-only-probe" in note
    assert "Full Disk Access" not in note
    # An EROFS anywhere is answered with the read only act.
    try:
        try:
            os.mkdir("/cratekit-u27-read-only-probe")
        except OSError as inner:
            raise refuse(
                "library-root-unreachable", "the library root could not be created",
                remedy=Remedy.GRANT_PATH_ACCESS) from inner
    except CratekitError as err:
        assert err.cause.remediation.remedy is Remedy.REMOUNT_WRITABLE
        assert err.declared_cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS


def test_a_locked_file_is_routed_to_the_lock_and_names_the_destination(tmp_path, monkeypatch):
    """A locked file (``uchg``) is routed to ``chflags nouchg`` naming the destination."""
    destination = _config_file(tmp_path, monkeypatch)
    locked = subprocess.run(["chflags", "uchg", str(destination)], check=False)
    assert locked.returncode == 0, "this platform has no per-file lock flag to drive"
    try:
        code, out, err = setup_at(tmp_path / "library", tmp_path)
    finally:
        subprocess.run(["chflags", "nouchg", str(destination)], check=False)
        config.reset_cache()
    cause = json.loads(out)["cause"]
    assert cause["reason"] == "path-locked", cause
    assert cause["remediation"]["remedy"] == "unlock-path"
    assert cause["detail"]["path"] == str(destination), "the temporary file was named again"
    assert ".tmp" not in cause["detail"]["path"]
    assert "chflags nouchg" in err
    assert "Full Disk Access" not in err
    assert code == int(ExitCode.PRECONDITION)
    # A rename into an unwritable directory, driven separately from the lock.
    source = made(tmp_path / "source")
    staged = planted(source / "tmpABCD.tmp", "x")
    unwritable = made(tmp_path / "unwritable")
    landing = unwritable / "config.toml"
    with _sealed(unwritable, mode=0o500):
        try:
            os.replace(staged, landing)
        except OSError as exc:
            renamed = cause_module.access_refusal(exc)
    assert renamed is not None
    assert renamed.path == str(landing), "the temporary file was named instead"
    assert ".tmp" not in renamed.path


def test_the_session_reader_does_not_read_absence_out_of_a_refusal(tmp_path, monkeypatch):
    """A session record this account cannot open is neither absent nor a defect."""
    cfg = isolated_library(tmp_path, monkeypatch)
    path = planted(session.log_path("session-abc", cfg), "{}")
    with _sealed(path):
        cause = refusal(session.read_record, "session-abc", cfg)
    assert cause.reason == "path-permission-denied"
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert cause.detail["path"] == str(path)
    assert "no session is recorded" not in cause.message
    assert "was not established" in cause.message
    # A record that is genuinely not there still says so.
    path.unlink()
    assert "no session is recorded" in refusal(session.read_record, "session-abc", cfg).message


def test_the_acknowledgment_reader_does_not_claim_the_file_exists(tmp_path, monkeypatch):
    cfg = isolated_library(tmp_path, monkeypatch)
    ack = planted(session.ack_path(cfg), "{}")
    with _sealed(ack):
        cause = refusal(session.read_acknowledgment, cfg)
    assert cause.reason == "path-permission-denied"
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert "exists and could not be read" not in cause.message
    assert "whether it is even there was not established" in cause.message


def test_an_unreadable_capture_manifest_is_not_a_defect_report(tmp_path):
    capture = made(tmp_path / "capture")
    manifest = planted(capture / snapshot.MANIFEST_NAME, "{}")
    with _sealed(manifest):
        cause = refusal(snapshot.read_manifest, capture)
    assert cause.reason == "path-permission-denied"
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert cause.detail["path"] == str(manifest)
    # The site's own reading is kept.
    assert cause.detail["declared_reason"] == "internal-error"


def test_the_wizard_does_not_call_an_intact_configuration_corrupt(tmp_path, monkeypatch):
    document = _config_file(tmp_path, monkeypatch)
    intact = document.read_bytes()
    with _sealed(document, reset_config=True):
        code, out, err = setup_at(tmp_path / "library", tmp_path)
    cause = json.loads(out)["cause"]
    assert cause["remediation"]["remedy"] != "repair-config-file", cause
    assert cause["remediation"]["remedy"] == "grant-path-access"
    assert cause["reason"] == "path-permission-denied"
    assert code == int(ExitCode.PRECONDITION)
    assert "repair or recreate" not in err
    assert document.read_bytes() == intact, "the file it called unrepairable was never touched"


def test_the_wizards_second_read_does_not_call_an_intact_configuration_corrupt(
        tmp_path, monkeypatch):
    """The wizard's raw second read does not call a sealed incomplete config corrupt."""
    document = _config_file(tmp_path, monkeypatch, "schema_version = 1\n")
    intact = document.read_bytes()
    real_load = config.load

    def load_then_seal():
        try:
            return real_load()
        finally:
            document.chmod(0o000)
    monkeypatch.setattr(setup_verb.config, "load", load_then_seal)
    try:
        cause = refusal(setup_verb.existing_document)
    finally:
        document.chmod(0o600)
        config.reset_cache()
    assert cause.remediation.remedy is not Remedy.REPAIR_CONFIG_FILE
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert cause.reason == "path-permission-denied"
    assert cause.detail["path"] == str(document)
    assert cause.detail["declared_reason"] == "config-unusable"
    assert document.read_bytes() == intact, "the file it called unrepairable was never touched"


def test_doctors_configuration_check_does_not_call_an_intact_file_corrupt(tmp_path, monkeypatch):
    document = _config_file(tmp_path, monkeypatch)
    with _sealed(document, reset_config=True):
        finding = finding_on(None, "config.present")
    checked(finding, FAIL, Remedy.GRANT_PATH_ACCESS)
    assert finding.remedy is not Remedy.REPAIR_CONFIG_FILE
    assert str(document) in finding.detail
    assert "repair or recreate" not in (render.remedy_text(finding.remedy) or "")


def test_a_verb_that_lets_a_config_error_escape_is_classified_too(tmp_path, monkeypatch):
    """A ``ConfigError`` escaping a verb is classified at the dispatcher."""
    document = _config_file(tmp_path, monkeypatch)
    with _sealed(document, reset_config=True):
        code, out, err = drive(["--output", "json", "review", "list"])
    cause = json.loads(out)["cause"]
    assert cause["remediation"]["remedy"] == "grant-path-access", cause
    assert cause["reason"] == "path-permission-denied"
    assert cause["detail"]["path"] == str(document)
    assert cause["detail"]["declared_reason"] == "config-unusable"
    assert code == int(ExitCode.PRECONDITION)
    assert "repair or recreate" not in err


def test_the_access_sentence_names_the_path_it_is_about(tmp_path):
    """The access sentence's own path clause is asserted."""
    sealed = made(tmp_path / "sealed")
    inside = planted(sealed / "inside", "x")
    with _sealed(sealed):
        try:
            inside.read_text()
        except OSError as exc:
            note = render.access_note(exc)
    assert note.startswith(f"The path is {inside}. ")
    assert "rather than a defect in this program" in note


def test_the_cause_walk_terminates_on_a_chain_that_names_itself(tmp_path):
    """The cause walk terminates on a self-naming chain, in a subprocess with a deadline."""
    script = (
        "from cratekit.core import cause\n"
        "a = OSError('one')\n"
        "b = OSError('two')\n"
        "a.__cause__ = b\n"
        "b.__cause__ = a\n"
        "assert cause.permission_denied(a) is None\n"
        "assert cause.access_refusal(a) is None\n"
        "print('terminated')\n")
    done = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=60)
    assert done.returncode == 0, done.stderr
    assert "terminated" in done.stdout


def test_is_mount_point_answers_an_unrepresentable_path(tmp_path):
    assert os.path.ismount("a\x00b") is False
    assert preflight.is_mount_point(Path("a\x00b")) is False
    assert preflight.slot_holds_a_volume(Path("a\x00b")) is False


# ── the handler sweep: every rescue answers something, or says why it cannot ──


def test_the_declared_interpreter_bound_is_none_when_it_cannot_be_read(monkeypatch):
    """No readable bound is "nothing asserted", not a pass."""
    monkeypatch.setattr(doctor.registry, "DISTRIBUTION", "cratekit-no-such-distribution")
    assert doctor._declared_python_bound() is None
    monkeypatch.setattr(importlib_metadata, "metadata", lambda _name: {})
    assert doctor._declared_python_bound() is None
    finding = checked(finding_on(None, "interpreter.version", requires_python=None), INFO)
    assert "nothing was asserted about it" in finding.detail


def test_the_binding_pin_problem_is_whatever_the_writers_own_assertion_says(monkeypatch):
    def refuse(_cfg):
        raise CratekitError(
            Cause(
                reason="pyrekordbox-pin-drift", message="pyrekordbox 0.4.0 is not the pinned 0.3.0",
                remediation=Remediation(remedy=Remedy.REVALIDATE_PINS), scope=Scope.RUN,
                origin=("tests",)))
    monkeypatch.setattr(rb_writer, "assert_binding_version", refuse)
    assert doctor_model._binding_pin_problem(None) == "pyrekordbox 0.4.0 is not the pinned 0.3.0"

    def uninstalled(_cfg):
        raise ImportError("No module named 'pyrekordbox'")
    monkeypatch.setattr(rb_writer, "assert_binding_version", uninstalled)
    answer = doctor_model._binding_pin_problem(None)
    assert answer is not None and "could not be imported" in answer
    monkeypatch.setattr(rb_writer, "assert_binding_version", lambda _cfg: None)
    assert doctor_model._binding_pin_problem(None) is None


def test_the_rclone_dump_answers_none_for_every_way_it_can_fail(monkeypatch, tmp_path):
    assert doctor_model._rclone_remotes(str(tmp_path / "no-such-rclone")) is None

    def timed_out(*_a, **_k):
        raise subprocess.TimeoutExpired(cmd="rclone", timeout=10)

    def ran(returncode, stdout):
        return lambda *_a, **_k: SimpleNamespace(returncode=returncode, stdout=stdout)
    for broken in (timed_out, ran(1, ""), ran(0, "not json at all"), ran(0, "[1, 2]")):
        monkeypatch.setattr(subprocess, "run", broken)
        assert doctor_model._rclone_remotes("rclone") is None
    # The working answer, so none of the above passes by accident.
    working = '{"gdrive": {"type": "drive", "use_trash": "false"}}'
    monkeypatch.setattr(subprocess, "run", ran(0, working))
    remotes = {"gdrive": {"type": "drive", "use_trash": "false"}}
    assert doctor_model._rclone_remotes("rclone") == remotes


def test_an_active_template_that_does_not_validate_is_its_own_answer(configured):
    path = config.state_path("taxonomy_active", configured)
    config.atomic_write_bytes(b"schema_version = 99\n", path)
    finding = finding_on(configured, "taxonomy.active")
    checked(finding, FAIL, Remedy.RUN_SETUP)
    assert "is not usable" in finding.detail


def test_a_registered_adapter_whose_tool_is_not_installed_says_so(configured, monkeypatch):
    """An adapter whose module will not import says install the tool (R9)."""
    def uninstalled(_name):
        raise ImportError("No module named 'yt_dlp'")
    monkeypatch.setattr(acquire, "load", uninstalled)
    finding = finding_on(configured, "adapter.contract")
    checked(finding, FAIL, Remedy.INSTALL_ADAPTER)
    assert "is not installed here" in finding.detail


def test_unreadable_backup_facts_are_reported_per_portion(configured, monkeypatch):
    """Unreadable fact files are reported per portion, never as "no backup recorded"."""
    def refuse(_cfg, *, now):
        raise backup_facts.BackupFactsUnreadable(
            "the backup facts file is not readable JSON", path=Path("/nowhere/backup.json"),
            remedy=Remedy.REPAIR_BACKUP_FACTS)
    monkeypatch.setattr(doctor.backup_facts, "ages", refuse)
    report = report_on(configured)
    for portion in backup_facts.PORTIONS:
        finding = checked(find(report, f"backup.age.{portion}"), FAIL, Remedy.REPAIR_BACKUP_FACTS)
        assert "not readable JSON" in finding.detail


def test_a_hook_line_with_an_unbalanced_quote_falls_back_to_the_default_config():
    assert (
        doctor_state._hook_config_name('exec pre-commit hook-impl --config="unbalanced')
        == doctor_state._HOOK_CONFIG_DEFAULT)
    # A quoted path with a space is read, which is why shlex is used.
    assert (
        doctor_state._hook_config_name("exec pre-commit hook-impl --config='my config.yaml'")
        == "my config.yaml")


def test_a_run_record_that_will_not_load_is_reported_rather_than_skipped(configured):
    """A run record that will not load is reported, or its open gate vanishes."""
    directory = gates.run_dir()
    planted(directory / "r-broken.json", "{ this is not json")
    findings = doctor._run_findings()
    checked(next(f for f in findings if f.key == "run.r-broken"), FAIL, Remedy.REPORT_DEFECT)


def test_a_tree_registry_that_will_not_load_is_never_read_as_no_record(configured):
    planted(tree_registry.path_for(configured), b"{ not json")
    findings = doctor._tree_findings(configured)
    assert [f.key for f in findings] == ["tree.registry"]
    assert findings[0].status is FAIL
    assert findings[0].remedy is Remedy.RUN_DOCTOR


def test_setup_refuses_a_config_that_stopped_being_readable_between_the_two_reads(
        monkeypatch, tmp_path):
    """A config unreadable between the two reads is refused, not written over as empty."""
    missing = tmp_path / "vanished.toml"

    def incomplete():
        raise config.ConfigInvalid("library.root is missing")
    monkeypatch.setattr(config, "load", incomplete)
    monkeypatch.setattr(config, "config_path", lambda: missing)
    cause = refusal(setup_verb.existing_document)
    assert "will not overwrite a configuration it cannot read" in cause.message
    assert cause.remediation.remedy is Remedy.REPAIR_CONFIG_FILE


def test_setup_refuses_when_the_migration_ladder_refuses(monkeypatch, tmp_path):
    path = planted(tmp_path / "config.toml", "schema_version = 1\n")

    def incomplete():
        raise config.ConfigInvalid("library.root is missing")

    def refuse(_raw):
        raise config.ConfigTooNew("written by a newer Cratekit")
    monkeypatch.setattr(config, "load", incomplete)
    monkeypatch.setattr(config, "config_path", lambda: path)
    monkeypatch.setattr(config, "migrate", refuse)
    cause = refusal(setup_verb.existing_document)
    assert "will not overwrite this configuration" in cause.message
    assert cause.remediation.remedy is Remedy.UPGRADE_CRATEKIT


def test_the_database_probe_is_a_proposal_and_never_a_failure(monkeypatch, tmp_path):
    """The database probe reads another application's format, so a failure is no proposal."""
    def unexpected():
        raise RuntimeError("the settings file is in a shape this reader has never seen")
    monkeypatch.setattr(setup_verb.rb_writer, "read_rekordbox_settings", unexpected)
    assert setup_verb._probe_db_path() is None
    # A recorded path not on this machine is not proposed either.
    monkeypatch.setattr(
        setup_verb.rb_writer, "read_rekordbox_settings",
        lambda: {"db_path": str(tmp_path / "absent" / "master.db")})
    assert setup_verb._probe_db_path() is None
    real = planted(tmp_path / "master.db", b"")
    monkeypatch.setattr(
        setup_verb.rb_writer, "read_rekordbox_settings", lambda: {"db_path": str(real)})
    assert setup_verb._probe_db_path() == str(real)


def test_a_credential_that_cannot_be_read_and_one_that_cannot_be_stored_differ(
        configured, monkeypatch):
    """An unreadable credential and a refusing store carry different remedies."""
    wizard = setup_verb._Wizard({}, silent())
    wizard.optional = lambda *_a, **_k: True  # the user said yes to every offer
    monkeypatch.setattr(doctor, "requires_check", lambda _key, _m: True)
    monkeypatch.setattr(secrets, "exists", lambda _name: False)
    setup_verb._capture_credentials(wizard, configured)
    unreadable = [n for n in wizard.notes if n.key.startswith("setup.credential.")]
    assert unreadable, "no credential was offered at all"
    for note in unreadable:
        checked(note, FAIL, Remedy.SET_CREDENTIAL)
        assert "was offered and nothing could be read" in note.detail

    def rejected(_name, _value):
        raise secrets.CredentialBackendUnavailable("no keychain backend resolves here")
    stored = setup_verb._Wizard({}, Scripted([], secrets_=["a-value"] * 8))
    stored.optional = lambda *_a, **_k: True
    monkeypatch.setattr(secrets, "set", rejected)
    setup_verb._capture_credentials(stored, configured)
    refused = [n for n in stored.notes if n.key.startswith("setup.credential.")]
    assert refused
    for note in refused:
        checked(note, FAIL, Remedy.INSTALL_KEYCHAIN_BACKEND)
        assert "could not be recorded" in note.detail


def test_a_hook_config_path_that_cannot_be_resolved_is_a_refusal_not_a_crash(tmp_path):
    """A hook config path in a symlink loop (``RuntimeError``) is a refusal, not a crash."""
    root = tmp_path / "checkout"
    (root / ".git" / "hooks").mkdir(parents=True)
    (root / "loop").symlink_to(root / "loop-b")
    (root / "loop-b").symlink_to(root / "loop")
    body = "exec pre-commit hook-impl --hook-type=pre-commit --config=loop/config.yaml\n"
    problem = doctor_state._hook_dispatch_problem(body, root)
    assert problem is not None
    assert "cannot be resolved" in problem
    (root / ".git" / "hooks" / "pre-commit").write_text(body)
    finding = checked(finding_on(None, "repo.commit_hook", checkout_root=lambda: root), FAIL)
    assert "did not complete" not in finding.detail, "the blanket rescue answered"
    assert "cannot be resolved" in finding.detail


def test_a_slot_holds_a_volume_when_a_symlink_in_it_names_a_real_mount(tmp_path):
    mount = Path(tmp_path.anchor)
    to_a_mount = tmp_path / "alias-to-a-real-mount"
    to_a_mount.symlink_to(mount, target_is_directory=True)
    ordinary = made(tmp_path / "ordinary")
    to_a_directory = tmp_path / "alias-to-an-ordinary-directory"
    to_a_directory.symlink_to(ordinary, target_is_directory=True)
    # The seam itself is unchanged: a symlink is never a mount point.
    assert preflight.is_mount_point(to_a_mount) is False
    assert preflight.is_mount_point(to_a_directory) is False
    # The rule asks whether a volume is behind the slot.
    assert preflight.slot_holds_a_volume(mount) is True
    assert preflight.slot_holds_a_volume(to_a_mount) is True
    assert preflight.slot_holds_a_volume(to_a_directory) is False
    assert preflight.slot_holds_a_volume(ordinary) is False


def test_setup_leaves_under_the_code_a_refusing_check_reserved(monkeypatch, tmp_path):
    root = fresh_root(tmp_path, monkeypatch, "fresh")
    green_probes(monkeypatch)
    monkeypatch.setattr(doctor, "CHECKS", (_refusing_check(),))
    code, out, err = setup_at(root, tmp_path)
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), err
    assert json.loads(out)["cause"]["reason"] == "library-volume-unmounted"


# ═══ The channel a refusal travels when nothing is raised ═══════════════════
# A ``doctor.Finding`` built from an exception never reached ``cause.classified``.


def test_a_finding_that_carries_a_refusal_is_classified_where_it_is_built(tmp_path):
    """A ``Finding`` handed an exception classifies its act where it is built, three kinds."""
    sealed = tmp_path / "sealed.toml"
    sealed.write_text("x = 1\n", encoding="utf-8")
    with _sealed(sealed):
        refused = caught(
            OSError, lambda: sealed.open("rb"), "a 0o000 file opened, so the arrangement is void")
        # The site's own reading, deliberately a different act's token.
        read = "the template could not be read"
        finding = a_finding(detail=read, remedy=Remedy.REMOUNT_WRITABLE, error=refused)
    assert finding.remedy is Remedy.GRANT_PATH_ACCESS
    assert finding.cause is not None, "a failing refusal must reach the envelope as one"
    assert finding.cause.reason == "path-permission-denied"
    assert finding.cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert finding.cause.detail["path"] == str(sealed)
    assert finding.cause.detail["check"] == "setup.taxonomy"
    read_only = root_volume_refusal("cratekit-u27-finding-probe")
    assert read_only.errno == errno.EROFS
    written = "the template could not be written"
    remedy = Remedy.GRANT_PATH_ACCESS
    on_a_read_only_volume = a_finding(detail=written, remedy=remedy, error=read_only)
    assert on_a_read_only_volume.remedy is Remedy.REMOUNT_WRITABLE
    assert on_a_read_only_volume.cause.reason == "path-read-only"
    not_toml = {"key": "taxonomy.active", "detail": "the file is not valid TOML"}
    ordinary = a_finding(**not_toml, remedy=Remedy.REPORT_DEFECT, error=ValueError("not a refusal"))
    assert ordinary.remedy is Remedy.REPORT_DEFECT
    assert ordinary.cause is None
    assert (
        doctor.Finding(key="k", title="t", status=FAIL, detail="d", remedy=Remedy.RUN_DOCTOR).remedy
        is Remedy.RUN_DOCTOR)


def test_the_seed_on_a_read_only_library_volume_is_not_sent_to_full_disk_access(monkeypatch):
    """The taxonomy seed on a read only volume gets the remount act (real EROFS at ``/``)."""
    # Over the suite-wide override (P2).
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, "/")
    # This write aims outside the temporary root on purpose (R-926).
    monkeypatch.setattr(config, "_TEST_WRITE_ROOT", Path("/"))
    cfg = config.from_dict(document_for(Path("/")))
    state = config.state_path("taxonomy_active", cfg)
    assert state.parent.parent == Path("/.cratekit"), state
    exc = root_volume_refusal("cratekit-u27-seed-probe")
    assert exc.errno == errno.EROFS, (
        f"this machine's root volume answered {exc.errno} rather than EROFS, "
        f"so the arrangement is not a read only volume")
    wizard = seeded(cfg)
    note = checked(seed_note(wizard), FAIL)
    assert note.remedy is Remedy.REMOUNT_WRITABLE, "a read only volume is not a grant"
    assert "Full Disk Access" not in note.detail
    assert "mounted read only" in note.detail
    assert "/.cratekit" in note.detail
    # The one-line fix is the act for this kind.
    assert "Full Disk Access" not in render.remedy_text(note.remedy)
    # The envelope carries it, rather than a null remedy.
    cause = doctor.failure_cause(doctor.Report(tuple(wizard.notes)), origin="cli.setup")
    assert cause.reason == "path-read-only"
    assert cause.remediation.remedy is Remedy.REMOUNT_WRITABLE
    assert cause.detail["access"] == "read-only"
    assert not state.exists()


def test_a_path_no_filesystem_can_represent_is_answered_rather_than_raised():
    """A path with an embedded null is answered, not raised inside the handler."""
    unrepresentable = "/tmp/cratekit-u27\0probe"
    with pytest.raises(ValueError):
        os.lstat(unrepresentable)
    with pytest.raises(ValueError):
        os.open(unrepresentable, os.O_RDONLY)
    # The two seams answer instead, as ``os.path.ismount`` does.
    assert os.path.ismount(unrepresentable) is False
    assert cause_module._immutable(unrepresentable) is False
    assert cause_module._probe_readable(unrepresentable) is None
    assert cause_module._probe_writable(unrepresentable) is None
    # Constructed, since no syscall can carry one.
    assert cause_module.access_refusal(
        PermissionError(errno.EACCES, "Permission denied", unrepresentable)
    ) == cause_module.AccessRefusal(kind=cause_module.AccessKind.PERMISSION, path=unrepresentable)


def test_the_write_probe_classifies_every_way_a_write_is_refused(tmp_path):
    """The write probe classifies mode, immutable flag and ACL refusals, all three kept (R-80)."""
    # 1. Readable and not writable by mode.
    mode = planted(tmp_path / "mode.db", b"x")
    mode.chmod(0o444)
    assert cause_module._probe_readable(str(mode)) is None, "the read probe cannot see this"
    refused = cause_module._probe_writable(str(mode))
    assert refused is not None and refused.kind is cause_module.AccessKind.PERMISSION
    assert refused.path == str(mode)
    # 2. The immutable flag (Finder's Locked), EPERM rather than EACCES.
    locked = planted(tmp_path / "locked.db", b"x")
    if subprocess.run(["chflags", "uchg", str(locked)]).returncode == 0:
        try:
            assert cause_module._probe_readable(str(locked)) is None
            found = cause_module._probe_writable(str(locked))
            assert found is not None and found.kind is cause_module.AccessKind.LOCKED
        finally:
            subprocess.run(["chflags", "nouchg", str(locked)], check=False)
    # 3. An ACL denying write while the mode allows it, where chmod can set one.
    acl = planted(tmp_path / "acl.db", b"x")
    denied = subprocess.run(
        ["chmod", "+a", "everyone deny write,append", str(acl)], capture_output=True)
    if denied.returncode == 0:
        assert oct(acl.stat().st_mode)[-3:] == "644", "the mode still says writable"
        assert cause_module._probe_readable(str(acl)) is None
        found = cause_module._probe_writable(str(acl))
        assert found is not None and found.kind is cause_module.AccessKind.PERMISSION
    # The negative row, so the probe does not refuse everything.
    ordinary = planted(tmp_path / "ordinary.db", b"x")
    assert cause_module._probe_writable(str(ordinary)) is None


def test_the_write_probe_names_the_medium_rather_than_the_account():
    """A read only medium is named as such, not as a permission."""
    on_the_system_volume = "/usr/bin/true"
    assert os.path.exists(on_the_system_volume), (
        "this machine has no /usr/bin/true, so the arrangement is not the one this test names")
    assert os.statvfs(on_the_system_volume).f_flag & os.ST_RDONLY, (
        "this machine's system volume is writable, so it proves nothing")
    assert cause_module._probe_readable(on_the_system_volume) is None, "the read probe can see it"
    refused = cause_module._probe_writable(on_the_system_volume)
    assert refused is not None
    assert refused.kind is cause_module.AccessKind.READ_ONLY, (
        "a medium that refuses every writer was reported as this account's "
        "permission, which is an act the user can take and that cannot work")
    assert refused.remedy is Remedy.REMOUNT_WRITABLE
    assert refused.path == on_the_system_volume


def test_the_write_probe_answers_for_a_path_it_cannot_reach_at_all(tmp_path):
    """A path the probe cannot reach answers through the read probe's classification."""
    sealed = made(tmp_path / "sealed")
    target = planted(sealed / "library.db", b"x")
    with _sealed(sealed):
        assert (os.statvfs(str(sealed)).f_flag & os.ST_RDONLY) == 0, (
            "this temporary directory is on a read only volume, so the read only "
            "branch would answer before the delegation does")
        refused = cause_module._probe_writable(str(target))
    assert refused is not None, (
        "a path this account cannot reach was answered with silence, which "
        "reaches the user as an unanticipated failure rather than as an act")
    assert refused.kind is cause_module.AccessKind.PERMISSION
    assert refused.path == str(target)


def test_a_two_path_refusal_names_the_side_the_operating_system_refused(tmp_path):
    """A two path refusal names the side refused: destination for a rename, source for a link."""
    sealed_dir = made(tmp_path / "sealed")
    source = planted(sealed_dir / "source.bin", b"x")
    destination = tmp_path / "destination.bin"
    with _sealed(sealed_dir):
        refused = caught(
            OSError, lambda: os.link(source, destination),
            "a link out of a 0o000 directory succeeded")
        assert refused.filename == str(source), "the arrangement is not the one described"
        assert refused.filename2 == str(destination)
        refusal = cause_module.access_refusal(refused)
        assert refusal is not None
        assert refusal.path == str(source), "the refusal named the path the account can write"
        assert refusal.kind is cause_module.AccessKind.PERMISSION
    # The rename case: an unwritable destination is named first.
    unwritable = made(tmp_path / "unwritable")
    target = planted(unwritable / "config.toml", b"y")
    temporary = planted(tmp_path / "tmpXXXX.tmp", b"z")
    with _sealed(target), _sealed(unwritable, mode=0o500):
        renamed = caught(
            OSError, lambda: os.replace(temporary, target),
            "a rename into a 0o500 directory succeeded")
        found = cause_module.access_refusal(renamed)
        assert found is not None
        assert found.path == str(target), "the user was sent to a temporary file again"


def test_a_copy_that_gave_up_on_one_member_is_classified_by_its_paths(tmp_path):
    """A ``copytree`` ``shutil.Error`` is classified by the paths in its triples."""
    tree = tmp_path / "source"
    (tree / "inner").mkdir(parents=True)
    member = planted(tree / "inner" / "member.bin", b"z")
    with _sealed(member):
        gave_up = caught(
            shutil.Error, lambda: shutil.copytree(tree, tmp_path / "captured"),
            "a 0o000 member copied, so the arrangement is void")
        # The shape the classification works from, stated.
        assert isinstance(gave_up, OSError)
        assert gave_up.errno is None
        assert gave_up.filename is None
        assert gave_up.__cause__ is None
        refusal = cause_module.access_refusal(gave_up)
        assert refusal is not None, "a sealed member was read as an unanticipated failure"
        assert refusal.path == str(member)
        assert refusal.kind is cause_module.AccessKind.PERMISSION
        assert refusal.remedy is Remedy.GRANT_PATH_ACCESS
        # It travels to the dispatcher's blanket, which an unguarded copy reaches.
        blanket = cli._unhandled_cause(gave_up)
        assert blanket.reason == "path-permission-denied"
        assert blanket.remediation.remedy is Remedy.GRANT_PATH_ACCESS
        assert str(member) in blanket.message


# ═══ Two answers a double cannot give ═══════════════════════════════════════
# Real identity, mount table, detach and EROFS, failing rather than skipping
# without hdiutil, since a skipped proof reads as a pass.


def _require_hdiutil() -> None:
    if not hdiutil_available():
        pytest.fail(
            "hdiutil is required to prove these two answers against real mounts "
            "and it is missing here. It ships with macOS, which is the platform "
            "this unit targets first. This fails rather than skips because a "
            "skipped hardware proof reads as a passing one.")


def _library_on(volume: Path) -> None:
    """What ``read_only_volume`` writes while the image is still writable."""
    (volume / "library" / "Music").mkdir(parents=True)


def test_an_unmounted_volume_and_a_moved_volume_are_told_apart_on_a_real_volume(tmp_path):
    """On one real volume, OK, LIBRARY_PATH_MISSING, MOUNTED_ELSEWHERE and NOT_MOUNTED differ."""
    _require_hdiutil()
    identity_of = preflight.macos_volume_identity
    gone_root = tmp_path / "no-such-mount-point" / "library"
    with read_only_volume(_library_on) as volume:
        # The mount table, never a behaviour probe.
        assert filesystem_kind(volume) == "hfs", filesystem_kind(volume)
        recorded = identity_of(volume)
        assert recorded, (
            "the fixture volume reports no identity through getattrlist, so this "
            "test would be asserting about IDENTITY_UNAVAILABLE rather than about "
            "the distinction it names")

        def resolve(root, **seams):
            seams["identity_provider"] = identity_of
            return preflight.resolve_mount_state(root, recorded, **seams)
        local = {"mount_enumerator": preflight.local_mount_points}
        on_it = resolve(volume / "library")
        moved_within = resolve(volume / "not-that-folder")
        elsewhere = resolve(gone_root, **local)
    unmounted = resolve(gone_root, **local)
    assert on_it.state is preflight.MountState.OK, on_it
    assert moved_within.state is preflight.MountState.LIBRARY_PATH_MISSING, moved_within
    assert elsewhere.state is preflight.MountState.MOUNTED_ELSEWHERE, elsewhere
    assert unmounted.state is preflight.MountState.NOT_MOUNTED, unmounted
    # The moved answer says where; the unmounted one has no place to name.
    assert elsewhere.found_at is not None
    assert unmounted.found_at is None
    # The two sentences carry different acts.
    moved_detail = doctor_library._MOUNT_DETAIL[elsewhere.state]
    absent_detail = doctor_library._MOUNT_DETAIL[unmounted.state]
    assert moved_detail != absent_detail
    assert "Nothing needs plugging in" in moved_detail
    assert "Attach it" in absent_detail
    assert not preflight.library_state_is_readable(elsewhere)
    assert not preflight.library_state_is_readable(unmounted)


def test_a_real_read_only_volume_reaches_the_user_as_remount_not_as_a_permission(monkeypatch):
    """A real read only mount reaches the user as remount, in token, cause and sentence."""
    _require_hdiutil()
    with read_only_volume(_library_on) as volume:
        root = volume / "library"
        monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
        cfg = config.from_dict(document_for(root))
        wizard = seeded(cfg)
        failures = [note for note in wizard.notes if note.status is FAIL]
        assert len(failures) == 1, [note.detail for note in wizard.notes]
        note = failures[0]
        # 1. The token: the kind the system made decides, not the hard coded one.
        assert note.remedy is Remedy.REMOUNT_WRITABLE, note.remedy
        # 2. The structured cause, rather than a null remedy.
        assert note.cause is not None, note.detail
        assert note.cause.reason == "path-read-only"
        assert note.cause.remediation.remedy is Remedy.REMOUNT_WRITABLE
        assert note.cause.detail["access"] == str(cause_module.AccessKind.READ_ONLY)
        # The path named is on the volume that refused.
        assert str(volume) in note.cause.detail["path"]
        # 3. The sentence, free to disagree with the token.
        assert "mounted read only" in note.detail
        assert "no permission grant can change that" in note.detail
        assert "Full Disk Access" not in note.detail
        assert "Grant this interpreter" not in note.detail
        assert not config.state_path("taxonomy_active", cfg).exists()


def test_the_read_only_refusal_and_the_permission_refusal_do_not_share_an_act(
        tmp_path, monkeypatch):
    """EROFS and EACCES through the same branch differ in token and sentence."""
    _require_hdiutil()
    sealed_root = tmp_path / "sealed" / "library"
    (sealed_root / "Music").mkdir(parents=True)

    def note_for(root: Path) -> doctor.Finding:
        monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
        cfg = config.from_dict(document_for(root))
        wizard = seeded(cfg)
        return next(note for note in wizard.notes if note.status is FAIL)
    with _sealed(sealed_root, mode=0o500):
        permission = note_for(sealed_root)
    with read_only_volume(_library_on) as volume:
        read_only = note_for(volume / "library")
    assert permission.remedy is Remedy.GRANT_PATH_ACCESS, permission.detail
    assert read_only.remedy is Remedy.REMOUNT_WRITABLE, read_only.detail
    assert permission.remedy is not read_only.remedy
    assert "Full Disk Access" in permission.detail
    assert "Full Disk Access" not in read_only.detail


def test_the_driver_path_to_the_write_probe_is_driven_on_a_real_read_only_volume():
    """The write probe's only route on a real read only volume keeps the attached path."""
    _require_hdiutil()

    def a_database_on(volume: Path) -> None:
        connection = sqlite3.connect(str(volume / "library.db"))
        connection.execute("CREATE TABLE t (a)")
        connection.commit()
        connection.close()
    with read_only_volume(a_database_on) as volume:
        database = volume / "library.db"
        refused: sqlite3.Error | None = None
        try:
            connection = sqlite3.connect(str(database))
            connection.execute("INSERT INTO t VALUES (1)")
            connection.commit()
            connection.close()
        except sqlite3.Error as error:
            refused = error
        assert refused is not None, (
            "the write onto a read only volume succeeded, so the arrangement is "
            "not the one this test names")
        assert getattr(refused, "sqlite_errorname", "") == "SQLITE_READONLY", (
            f"the driver answered {getattr(refused, 'sqlite_errorname', None)}, "
            f"which routes to the READ probe and not to the one under test")
        # The connection site attaches the path and the classifier reads it.
        cause_module.name_the_database(refused, database)
        refusal = cause_module.access_refusal(refused)
        assert refusal is not None, (
            "a driver level refusal on a read only volume reached the user as an "
            "unanticipated failure")
        assert refusal.kind is cause_module.AccessKind.READ_ONLY, (
            "the medium refused every writer and the user was told to grant this "
            "account an access that cannot change it")
        assert refusal.path == str(database)
        assert refusal.remedy is Remedy.REMOUNT_WRITABLE


# ── taxonomy.schema: the copy against the shipped schema (U132) ─────────────


def _schema_finding(cfg: config.Config) -> doctor.Finding:
    return finding_on(cfg, "taxonomy.schema")


def test_a_version_2_copy_without_favorites_is_named_with_both_versions(configured):
    write_active(configured, live_shaped())
    finding = checked(_schema_finding(configured), INFO)
    assert "schema_version 2" in finding.detail
    assert "'default' template states 5" in finding.detail
    assert "lacks the class(es) favorites" in finding.detail
    assert "lacks the bucket(s) soul" in finding.detail
    assert "crate taxonomy upgrade raises schema_version to 5 and adds favorites" in finding.detail
    assert "soul is held" in finding.detail and "'Soul'" in finding.detail
    # Reported, never repaired.
    assert config.state_path("taxonomy_active", configured).read_text(encoding="utf-8") == live_shaped()


def test_a_current_copy_with_every_entry_is_ok(configured):
    seed_taxonomy(configured)
    finding = checked(_schema_finding(configured), OK)
    assert "schema_version 5" in finding.detail


def test_a_copy_that_does_not_parse_is_left_to_taxonomy_active(configured):
    write_active(configured, "schema_version = 2\n[tree\n")
    finding = checked(_schema_finding(configured), INFO)
    assert finding.detail.startswith("not compared")
    assert finding_on(configured, "taxonomy.active").status is FAIL


def test_the_schema_is_not_compared_when_the_library_disk_is_absent(configured):
    seed_taxonomy(configured)
    gone = probes(**UNMOUNTED)
    finding = checked(find(doctor.run(configured, probes=gone), "taxonomy.schema"), INFO)
    assert "schema_version" not in finding.detail


def test_a_library_with_no_copy_routes_by_the_shipped_template_and_is_current(configured):
    assert not config.state_path("taxonomy_active", configured).exists()
    finding = checked(_schema_finding(configured), OK)
    assert "no active taxonomy copy" in finding.detail
    assert "'default' template, which is current" in finding.detail


def test_a_shipped_template_that_cannot_be_read_is_named_and_not_the_copy(configured, monkeypatch):
    seed_taxonomy(configured)

    def unreadable(_name):
        raise OSError("the package data is missing")
    monkeypatch.setattr(taxonomy, "shipped_template_text", unreadable)
    finding = checked(_schema_finding(configured), INFO)
    assert "shipped template 'default' could not be read" in finding.detail
    assert "taxonomy.template" in finding.detail
    assert "taxonomy.active" not in finding.detail


def test_a_shipped_template_that_does_not_load_is_a_defect_and_not_the_copy(
        configured, monkeypatch):
    seed_taxonomy(configured)
    shipped = taxonomy.shipped_template_text("default")
    monkeypatch.setattr(
        taxonomy, "shipped_template_text", lambda _n: shipped.replace('id = "rnb"', 'id = "R and B"', 1)
    )
    finding = checked(_schema_finding(configured), FAIL, Remedy.REPORT_DEFECT)
    assert "shipped" in finding.detail


def test_the_bandcamp_session_check_names_the_verbs_that_spend_it(configured):
    """U176: the Bandcamp session is never required, yet names the verbs that refuse without it."""
    inputs = doctor._Inputs(configured, None, probes(credential_recorded=lambda _name: False))
    finding = checked(doctor._check_credential("credential.bandcamp", inputs), INFO)
    assert "crate acquire bandcamp and crate acquire bandcamp-fetch" in finding.detail
    assert "no verb" not in finding.detail
    other = doctor._check_credential("credential.recognition", inputs)
    assert other.status is FAIL or "no verb" in other.detail


def test_the_discogs_token_is_reported_never_failed_and_says_how_to_record_it(configured):
    """U244: the Discogs token is INFO naming the tagging verbs and the login step."""
    inputs = doctor._Inputs(configured, None, probes(credential_recorded=lambda _name: False))
    finding = checked(doctor._check_credential("credential.discogs", inputs), INFO)
    assert "crate tag folder, crate tag retag, crate tag suggest" in finding.detail
    assert "crate login discogs-token --from-file PATH" in finding.detail
    assert "no verb" not in finding.detail
    recorded = doctor._Inputs(configured, None, probes(credential_recorded=lambda _name: True))
    assert doctor._check_credential("credential.discogs", recorded).status is OK


def test_the_cyanite_key_is_reported_never_failed_and_names_the_trial(configured):
    """U245: the Cyanite key is INFO naming the trial, and setup never offers it."""
    inputs = doctor._Inputs(configured, None, probes(credential_recorded=lambda _name: False))
    finding = checked(doctor._check_credential("credential.cyanite", inputs), INFO)
    assert "scripts/cyanite_trial.py" in finding.detail
    assert "crate login" in finding.detail
    recorded = doctor._Inputs(configured, None, probes(credential_recorded=lambda _name: True))
    assert doctor._check_credential("credential.cyanite", recorded).status is OK
    assert not doctor.offered("credential.cyanite", profiles.resolve("full"))


def test_setup_offers_the_discogs_token_where_a_tagging_verb_is_switched_on():
    full = profiles.resolve("full")
    assert doctor.offered("credential.discogs", full)
    assert not doctor.requires_check("credential.discogs", full)
    assert not doctor.offered("credential.bandcamp", full)
    spenders = set(doctor.OFFERED_WHEN_SPENT["credential.discogs"])
    assert spenders <= {entry.name for entry in registry.entries()}, "each is a real verb"
    assert {
        entry.name for entry in registry.entries() if entry.name in spenders
    } == spenders == {"tag.folder", "tag.retag", "tag.suggest"}


# ═══ U159: install.release, whether a newer release is published ════════════

_REPO_URL = "https://github.com/philgutowski/cratekit"


def _release_finding(origin, tags=None, *, read=None):
    seen = []

    def release_tags(url):
        seen.append(url)
        return tags if read is None else read(url)
    inputs = doctor._Inputs(
        None, None, probes(install_origin=lambda: origin, release_tags=release_tags))
    return doctor._check_release(inputs), seen


def _vcs(version="0.2.0", extras=()):
    return doctor.InstallOrigin(kind="vcs", version=version, url=_REPO_URL, extras=extras)


def test_a_newer_release_warns_with_the_one_pipx_command_keeping_the_extras():
    finding, seen = _release_finding(
        _vcs("0.2.0", ("analysis", "vocals")), ("v0.1.0", "v0.2.0", "v0.3.0"))
    assert seen == [_REPO_URL]
    assert finding.status is INFO, "a copy behind a release still works"
    assert "v0.3.0" in finding.detail and "0.2.0" in finding.detail
    assert (
        f'pipx install --force "cratekit[analysis,vocals] @ git+{_REPO_URL}@v0.3.0"'
        in finding.detail)


def test_a_newer_release_without_extras_names_plain_cratekit():
    finding, _ = _release_finding(_vcs("0.2.0"), ("v0.2.1",))
    assert f'pipx install --force "cratekit @ git+{_REPO_URL}@v0.2.1"' in finding.detail


@pytest.mark.parametrize(
    ("version", "tags", "said"),
    [
        pytest.param("0.2.0", ("v0.2.0",), "latest release", id="equal"),
        pytest.param("0.2.0", ("v0.1.9", "v0.2.0"), "latest release", id="equal-beside-older"),
        pytest.param("0.2.0", ("v0.1.0",), "latest release", id="newer"),
        pytest.param("0.1.0", (), "no release has been published", id="no-tags"),
        pytest.param(
            "0.2.0", ("v0.2.0", "nightly", "v9", "v10.0.0-rc1", "release-11.0.0", "v1.0"), "v0.2.0",
            id="tags-that-are-not-versions-are-ignored"),
    ])
def test_a_copy_no_published_release_is_newer_than_passes_and_says_why(version, tags, said):
    finding, _ = _release_finding(_vcs(version), tags)
    assert finding.status is OK
    assert said in finding.detail


def test_a_failed_read_says_it_could_not_read_and_never_passes():
    finding, _ = _release_finding(_vcs("0.1.0"), read=lambda _url: None)
    assert finding.status is not OK, "a check that could not look reported the copy as current"
    assert finding.status is INFO
    assert "could not be read" in finding.detail
    assert "unknown" in finding.detail


@pytest.mark.parametrize(("kind", "said"), [("editable", "editable checkout"), ("folder", "a folder")])
def test_a_folder_or_editable_install_says_the_check_does_not_apply(kind, said):
    finding, seen = _release_finding(
        doctor.InstallOrigin(kind=kind, version="0.1.0", url="file:///somewhere"), ("v9.0.0",))
    assert seen == [], "a folder install has no release to read"
    assert finding.status is INFO
    assert said in finding.detail and "does not apply" in finding.detail
    assert f"git+{_REPO_URL}@" in finding.detail, "it says how to move to a release install"


@pytest.mark.parametrize("kind", ["index", "unknown"])
def test_an_install_not_from_the_repository_does_not_apply(kind):
    finding, seen = _release_finding(doctor.InstallOrigin(kind=kind), ("v9.0.0",))
    assert seen == []
    assert finding.status is INFO
    assert "does not apply" in finding.detail


def test_the_check_never_fails_setup_on_any_answer():
    """INFO or OK for every shape, because a release behind is no reason to refuse."""
    for origin, read in (
        (_vcs("0.1.0"), lambda _u: ("v0.9.0",)),
        (_vcs("0.1.0"), lambda _u: None),
        (_vcs("not-a-version"), lambda _u: ("v0.1.0",)),
        (doctor.InstallOrigin(kind="editable"), lambda _u: None),
    ):
        finding, _ = _release_finding(origin, read=read)
        assert not finding.failed


def _distribution(tmp_path, direct_url, requires=()):
    """A real dist-info directory, read through importlib.metadata as installed."""
    info = made(tmp_path / "cratekit-0.2.0.dist-info")
    lines = ["Metadata-Version: 2.1", "Name: cratekit", "Version: 0.2.0"]
    lines += [f"Requires-Dist: {r}" for r in requires]
    (info / "METADATA").write_text("\n".join(lines) + "\n")
    if direct_url is not None:
        (info / "direct_url.json").write_text(direct_url)
    return importlib_metadata.PathDistribution(info)


@pytest.mark.parametrize(
    ("record", "kind"),
    [
        (
            '{"url": "https://github.com/philgutowski/cratekit", '
            '"vcs_info": {"vcs": "git", "requested_revision": "v0.2.0", "commit_id": "abc"}}',
            "vcs",
        ),
        ('{"url": "file:///src/cratekit", "dir_info": {"editable": true}}', "editable"),
        ('{"url": "file:///src/cratekit", "dir_info": {}}', "folder"),
        ('{"url": "file:///x.tar.gz", "archive_info": {}}', "folder"),
        (None, "index"),
        ("not json", "unknown"),
    ])
def test_the_install_origin_is_read_off_the_pep_610_record(tmp_path, monkeypatch, record, kind):
    dist = _distribution(tmp_path, record)
    monkeypatch.setattr(importlib_metadata, "distribution", lambda name: dist)
    origin = doctor_model._install_origin()
    assert origin.kind == kind
    if kind != "unknown":
        assert origin.version == "0.2.0"
    if kind == "vcs":
        assert origin.url == _REPO_URL


def test_the_installed_extras_are_the_ones_whose_requirements_are_present(tmp_path, monkeypatch):
    dist = _distribution(
        tmp_path,
        '{"url": "https://github.com/philgutowski/cratekit", "vcs_info": {"vcs": "git"}}',
        requires=(
            "platformdirs>=4.0",
            'librosa>=0.10; extra == "analysis"',
            'numpy>=1.24; extra == "analysis"',
            'torch>=2.2; extra == "vocals"',
            'cratekit[analysis,vocals]; extra == "all"',
        ))
    present = {"cratekit", "librosa", "numpy", "platformdirs"}

    def distribution(name):
        if name == "cratekit":
            return dist
        if name in present:
            return dist
        raise importlib_metadata.PackageNotFoundError(name)
    monkeypatch.setattr(importlib_metadata, "distribution", distribution)
    assert doctor_model._install_origin().extras == ("analysis",), (
        "vocals is missing torch and all is an alias, so only analysis is kept")


def test_the_release_read_parses_ls_remote_and_refuses_on_failure(monkeypatch):
    calls = []

    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs))
        out = "abc\trefs/tags/v0.1.0\ndef\trefs/tags/v0.2.0\n"
        return subprocess.CompletedProcess(argv, 0, out, "")
    monkeypatch.setattr(subprocess, "run", fake_run)
    assert doctor_model._release_tags(_REPO_URL) == ("v0.1.0", "v0.2.0")
    argv, kwargs = calls[0]
    assert argv[:3] == ["git", "ls-remote", "--tags"]
    assert kwargs["timeout"] == doctor_model.RELEASE_READ_TIMEOUT
    assert kwargs["env"]["GIT_TERMINAL_PROMPT"] == "0"

    def refused(argv, **kwargs):
        return subprocess.CompletedProcess(argv, 128, "", "fatal: could not read Username")
    monkeypatch.setattr(subprocess, "run", refused)
    assert doctor_model._release_tags(_REPO_URL) is None

    def timed_out(argv, **kwargs):
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])
    monkeypatch.setattr(subprocess, "run", timed_out)
    assert doctor_model._release_tags(_REPO_URL) is None


def test_an_unparseable_installed_version_is_unknown_never_a_downgrade():
    finding, _ = _release_finding(_vcs("0.2.0.dev1"), ("v0.1.0",))
    assert finding.status is INFO
    assert "unknown" in finding.detail
    assert "pipx install" not in finding.detail, "it told a newer copy to downgrade"


# ═══ U185: DEADCA7 beside the library ═══════════════════════════════════════


#: The green machine's clock, which every DEADCA7 push below is dated against.
GREEN_NOW = doctor_machines.green().now


def _deadca7(tmp_path, *, pushed_at: datetime | None = None, home: bool = True):
    """DEADCA7's support folder, and one backup entry written at ``pushed_at``."""
    support = tmp_path / "deadca7"
    if not home:
        return support
    backups = made(support / doctor_backup.DEADCA7_BACKUPS, parents=True)
    (backups / ".DS_Store").write_bytes(b"")
    if pushed_at is not None:
        entry = planted(backups / "master-20261030.db", b"a copy")
        os.utime(entry, (pushed_at.timestamp(), pushed_at.timestamp()))
    return support


def _deadca7_check(configured, **seams) -> doctor.Finding:
    """``deadca7.push`` on the green machine with ``seams``: a note, whatever it says."""
    finding = find(report_on(configured, **seams), "deadca7.push")
    assert finding.status is INFO, finding
    return finding


def _push_check(configured, support) -> doctor.Finding:
    return _deadca7_check(configured, deadca7_home=lambda: support)


def test_with_no_deadca7_support_folder_doctor_says_not_installed_and_does_not_fail(
        configured, tmp_path):
    finding = _push_check(configured, _deadca7(tmp_path, home=False))
    assert "not installed" in finding.detail
    # A machine with no home for it at all answers the same, and never fails.
    assert "not installed" in _push_check(configured, None).detail


def test_installed_with_no_push_says_so(configured, tmp_path):
    finding = _push_check(configured, _deadca7(tmp_path))
    assert "installed here and has recorded no push" in finding.detail


def test_a_push_newer_than_the_last_database_backup_warns_and_names_the_backup(
        configured, tmp_path):
    backed_up(configured, DATABASE, GREEN_NOW - timedelta(days=3))
    finding = _push_check(configured, _deadca7(tmp_path, pushed_at=GREEN_NOW - timedelta(days=1)))
    assert finding.detail.startswith("warning: DEADCA7 last pushed")
    assert "after this product's last database backup" in finding.detail
    assert "crate backup run" in finding.detail


def test_a_push_older_than_the_last_database_backup_is_held_by_it(configured, tmp_path):
    backed_up(configured, DATABASE, GREEN_NOW - timedelta(days=1))
    finding = _push_check(configured, _deadca7(tmp_path, pushed_at=GREEN_NOW - timedelta(days=3)))
    assert "before this product's last database backup, which holds it" in finding.detail
    assert "warning" not in finding.detail


def test_a_push_with_no_database_backup_recorded_warns(configured, tmp_path):
    finding = _push_check(configured, _deadca7(tmp_path, pushed_at=GREEN_NOW - timedelta(days=1)))
    assert finding.detail.startswith("warning:")
    assert "no database backup is recorded here" in finding.detail


def test_a_backup_folder_that_cannot_be_read_is_said_as_unread_and_does_not_fail(
        configured, tmp_path):
    support = _deadca7(tmp_path)
    (support / doctor_backup.DEADCA7_BACKUPS / "gone").symlink_to(tmp_path / "nowhere")
    finding = _push_check(configured, support)
    assert "cannot be said: its backup folder could not be read" in finding.detail


# ═══ U224: DEADCA7 installed and never pushed is not DEADCA7 absent ═════════


def _installed_places(tmp_path, *present: str) -> tuple[Path, ...]:
    """The system, user and state places the installed probe names, ``present`` made."""
    places = {
        "system": tmp_path / "Applications" / doctor_model.DEADCA7_BUNDLE,
        "user": tmp_path / "home" / "Applications" / doctor_model.DEADCA7_BUNDLE,
        "state": tmp_path / "home" / "Library" / "Application Support" / doctor_model.DEADCA7_STATE,
    }
    for name in present:
        places[name].mkdir(parents=True)
    return tuple(places.values())


def _installed_check(configured, support, installed) -> doctor.Finding:
    return _deadca7_check(
        configured, deadca7_home=lambda: support, deadca7_installed=lambda: installed)


def test_sitting_68s_mac_the_bundle_and_no_support_folder_reads_installed_with_no_push(
        configured, tmp_path):
    """DEADCA7.app in /Applications with no support folder reads installed."""
    places = _installed_places(tmp_path, "system")
    finding = _installed_check(configured, _deadca7(tmp_path, home=False), places)
    assert "not installed" not in finding.detail, finding.detail
    assert finding.detail.startswith(
        "DEADCA7 is installed here and has recorded no push into rekordbox's database")
    assert str(places[0]) in finding.detail, "it did not name what it found"
    assert "unconfirmed until a push is read" in finding.detail
    assert str(tmp_path / "deadca7" / doctor_backup.DEADCA7_BACKUPS) in finding.detail


@pytest.mark.parametrize(
    ("present", "named"), [("user", 1), ("state", 2)],
    ids=["the-accounts-own-applications-folder", "the-state-folder-alone"])
def test_one_installed_place_alone_reads_installed_with_no_push(
        configured, tmp_path, present, named):
    places = _installed_places(tmp_path, present)
    finding = _installed_check(configured, _deadca7(tmp_path, home=False), places)
    assert "installed here and has recorded no push" in finding.detail
    assert str(places[named]) in finding.detail


def test_nothing_present_still_reads_not_installed(configured, tmp_path):
    finding = _installed_check(
        configured, _deadca7(tmp_path, home=False), _installed_places(tmp_path))
    assert finding.detail == (
        "DEADCA7 is not installed here, so nothing else writes the library beside rekordbox")


def test_a_file_where_the_bundle_would_be_is_not_an_install(configured, tmp_path):
    places = _installed_places(tmp_path)
    places[0].parent.mkdir(parents=True)
    places[0].write_bytes(b"")
    finding = _installed_check(configured, _deadca7(tmp_path, home=False), places)
    assert "not installed" in finding.detail


def test_a_push_is_read_as_today_whatever_the_install_signals_say(configured, tmp_path):
    support = _deadca7(tmp_path, pushed_at=GREEN_NOW - timedelta(days=1))
    finding = _installed_check(configured, support, _installed_places(tmp_path, "system"))
    assert finding.detail.startswith("warning: DEADCA7 last pushed into rekordbox's database at")
    assert "unconfirmed" not in finding.detail


def test_installed_with_an_empty_backup_folder_says_the_location_is_unconfirmed(
        configured, tmp_path):
    finding = _installed_check(configured, _deadca7(tmp_path), ())
    assert "installed here and has recorded no push" in finding.detail
    assert "holds no entry" in finding.detail
    assert "unconfirmed until a push is read" in finding.detail


def test_a_support_folder_with_no_backup_folder_reads_installed_with_no_push(configured, tmp_path):
    support = made(tmp_path / "deadca7")
    finding = _installed_check(configured, support, ())
    assert "installed here and has recorded no push" in finding.detail
    assert "does not exist" in finding.detail


def test_an_install_signal_that_cannot_be_read_is_unread_never_not_installed(
        configured, tmp_path, monkeypatch):
    places = _installed_places(tmp_path)
    _refuse_stat_under(monkeypatch, tmp_path / "home")
    finding = _installed_check(configured, _deadca7(tmp_path, home=False), places)
    assert "not installed" not in finding.detail, finding.detail
    assert finding.detail.startswith("whether DEADCA7 is installed here cannot be said")
    assert str(places[2]) in finding.detail
    assert "PermissionError" in finding.detail


def test_a_support_folder_that_cannot_be_read_is_unread_never_not_installed(
        configured, tmp_path, monkeypatch):
    support = _deadca7(tmp_path)
    _refuse_stat_under(monkeypatch, support)
    finding = _installed_check(configured, support, _installed_places(tmp_path))
    assert "not installed" not in finding.detail, finding.detail
    assert finding.detail.startswith("whether DEADCA7 is installed here cannot be said")
    assert str(support) in finding.detail


def test_installed_with_its_support_folder_unread_says_its_push_cannot_be_said(
        configured, tmp_path, monkeypatch):
    support = _deadca7(tmp_path)
    places = _installed_places(tmp_path, "system")
    _refuse_stat_under(monkeypatch, support)
    finding = _installed_check(configured, support, places)
    assert finding.detail.startswith("DEADCA7 is installed here")
    assert "cannot be said" in finding.detail
    assert "recorded no push" not in finding.detail, "an unread folder read as no push"


def test_a_backup_folder_whose_stat_is_refused_is_unread_never_no_push(
        configured, tmp_path, monkeypatch):
    support = _deadca7(tmp_path)
    _refuse_stat_under(monkeypatch, support / doctor_backup.DEADCA7_BACKUPS)
    finding = _installed_check(configured, support, ())
    assert "cannot be said: its backup folder could not be read" in finding.detail
    assert "recorded no push" not in finding.detail


@pytest.mark.parametrize("probe", ["deadca7_home", "deadca7_installed"])
def test_a_probe_that_raises_reads_unread_rather_than_not_installed(configured, tmp_path, probe):
    def broken():
        raise OSError(5, "Input/output error")
    seams = {
        "deadca7_home": lambda: _deadca7(tmp_path, home=False),
        "deadca7_installed": lambda: _installed_places(tmp_path),
        probe: broken,
    }
    finding = _deadca7_check(configured, **seams)
    assert "not installed" not in finding.detail, finding.detail
    assert finding.detail.startswith("whether DEADCA7 is installed here cannot be said")
    assert "OSError" in finding.detail


def test_a_probe_that_raises_beside_a_present_bundle_still_reads_installed(configured, tmp_path):
    def broken():
        raise OSError(5, "Input/output error")
    places = _installed_places(tmp_path, "system")
    finding = _deadca7_check(configured, deadca7_home=broken, deadca7_installed=lambda: places)
    assert finding.detail.startswith("DEADCA7 is installed here")
    assert "cannot be said" in finding.detail
    assert "recorded no push" not in finding.detail


def test_the_installed_probe_names_both_bundles_and_the_shipped_state_folder(monkeypatch, tmp_path):
    monkeypatch.setattr(pathlib.Path, "home", classmethod(lambda cls: tmp_path))
    assert doctor_model._deadca7_installed() == (
        Path("/Applications/DEADCA7.app"),
        tmp_path / "Applications" / "DEADCA7.app",
        tmp_path / "Library" / "Application Support" / "deadcatalog",
    )

    def homeless(cls):
        raise RuntimeError("no home")
    monkeypatch.setattr(pathlib.Path, "home", classmethod(homeless))
    assert doctor_model._deadca7_installed() == (Path("/Applications/DEADCA7.app"),)


def test_a_real_probes_value_asks_the_installed_probe(configured, tmp_path, monkeypatch):
    """The seam's default is wired: a regression to nothing would re-create the bug green."""
    home = tmp_path / "home"
    (home / "Library" / "Application Support" / doctor_model.DEADCA7_STATE).mkdir(parents=True)
    monkeypatch.setattr(pathlib.Path, "home", classmethod(lambda cls: home))
    machine = dataclasses.replace(
        doctor_machines.green(), deadca7_home=lambda: home / "nowhere",
        deadca7_installed=RealProbes().deadca7_installed)
    finding = find(doctor.run(configured, probes=machine), "deadca7.push")
    assert "installed here and has recorded no push" in finding.detail, finding.detail


def test_an_install_place_reached_through_a_file_is_absent_not_unread(configured, tmp_path):
    """``Applications`` a file: the stat raises NotADirectoryError, which is not there."""
    (tmp_path / "Applications").write_bytes(b"")
    places = (tmp_path / "Applications" / doctor_model.DEADCA7_BUNDLE,)
    finding = _installed_check(configured, _deadca7(tmp_path, home=False), places)
    assert finding.detail == (
        "DEADCA7 is not installed here, so nothing else writes the library beside rekordbox")


def test_with_its_support_folder_here_the_install_signals_are_not_asked(configured, tmp_path):
    asked = []

    def installed():
        asked.append(True)
        raise OSError(5, "Input/output error")
    report = report_on(
        configured, deadca7_home=lambda: _deadca7(tmp_path), deadca7_installed=installed)
    finding = find(report, "deadca7.push")
    assert "installed here and has recorded no push" in finding.detail, finding.detail
    assert asked == [], "the support folder alone says installed; nothing else need be read"


def test_installed_with_no_home_to_resolve_says_where_its_backups_land_is_unconfirmed(
        configured, tmp_path):
    places = _installed_places(tmp_path, "system")
    finding = _installed_check(configured, None, places)
    assert finding.detail.startswith("DEADCA7 is installed here and has recorded no push")
    assert finding.detail.endswith(
        "Where it backs rekordbox's database up before a push is unconfirmed until a push is read")


def _refuse_stat_under(monkeypatch, under: Path) -> None:
    """Refuse ``os.stat`` at or under ``under``, as a closed folder would."""
    real = os.stat

    def refused(path, *args, **kwargs):
        if Path(path) == under or under in Path(path).parents:
            raise PermissionError(13, "Permission denied", str(path))
        return real(path, *args, **kwargs)
    monkeypatch.setattr(os, "stat", refused)


def test_a_push_beside_a_backup_recorded_ahead_of_now_is_not_called_held(configured, tmp_path):
    backed_up(configured, DATABASE, GREEN_NOW + timedelta(days=10))
    finding = _push_check(configured, _deadca7(tmp_path, pushed_at=GREEN_NOW - timedelta(days=1)))
    assert "cannot be said, since that backup is recorded ahead of now" in finding.detail
    assert "which holds it" not in finding.detail


# ═══ U181: install.extras, whether the vocal model can score in this copy ═══

_NO_EXTRA = ("extra", "the 'vocals' extra is not installed here; reinstall it")


def _extras_finding(missing, origin=None, **overrides):
    origin = origin or _vcs("0.3.0", ("analysis",))
    inputs = doctor._Inputs(
        None, None,
        probes(vocal_requirement=lambda: missing, install_origin=lambda: origin, **overrides))
    return doctor._check_install_extras(inputs)


def test_a_copy_without_the_vocals_extra_says_so_and_prints_the_reinstall_command():
    finding = _extras_finding(_NO_EXTRA)
    assert finding.key == "install.extras"
    assert finding.status is INFO, "it runs inside setup and must not refuse"
    assert "vocals extra is absent" in finding.detail
    assert "carry no voxlevel" in finding.detail
    assert (
        f'pipx install --force "cratekit[analysis,vocals] @ git+{_REPO_URL}@v0.3.0"'
        in finding.detail
    ), "the reinstall keeps the extra this copy carries and adds vocals, at its own tag"


def test_a_copy_whose_vocal_model_can_score_is_ok():
    finding = checked(_extras_finding(None), OK)
    assert "pipx" not in finding.detail


def test_the_row_reads_the_vocals_modules_own_probe_with_the_loader_bound_or_not(monkeypatch):
    """Unbound with no torch reports the row and the command; bound is ok."""
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", None)
    monkeypatch.setattr(
        vocals, "requirement", lambda: ("extra", "the 'vocals' extra is not installed here"))
    inputs = doctor._Inputs(None, None, doctor.Probes(install_origin=lambda: _vcs("0.3.0")))
    unbound = checked(doctor._check_install_extras(inputs), INFO)
    assert f'"cratekit[vocals] @ git+{_REPO_URL}@v0.3.0"' in unbound.detail
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", lambda: object())
    assert doctor._check_install_extras(inputs).status is OK


def test_missing_model_files_are_named_and_no_reinstall_is_offered_for_them():
    """A reinstall does not place the checkpoint, so the row does not say it would."""
    finding = _extras_finding(("files", "the vocal model checkpoint is not at the path"))
    assert finding.status is INFO
    assert "checkpoint is not at the path" in finding.detail
    assert "Reinstall" not in finding.detail and "pipx" not in finding.detail


def test_a_copy_not_installed_from_a_release_gets_the_vocals_modules_own_command(monkeypatch):
    monkeypatch.setattr(vocals, "install", lambda: "the vocals module's own command")
    finding = _extras_finding(_NO_EXTRA, origin=doctor.InstallOrigin(kind="editable"))
    assert "Reinstall with: the vocals module's own command" in finding.detail


def test_the_extras_row_never_fails_setup():
    for missing in (_NO_EXTRA, ("files", "the label table is not at the path"), None):
        assert not _extras_finding(missing).failed


@pytest.mark.parametrize(
    ("scored", "command"),
    [(True, 'pipx install --force "cratekit[analysis,vocals]'), (False, '"cratekit[analysis]')],
    ids=["scored-adds-vocals", "never-scored-adds-nothing"])
def test_an_upgrade_keeps_the_extras_and_adds_vocals_only_for_a_scored_library(scored, command):
    """A copy that lost the extra would otherwise upgrade without it again."""
    inputs = doctor._Inputs(
        None,
        None,
        probes(
            install_origin=lambda: _vcs("0.2.0", ("analysis",)),
            release_tags=lambda _url: ("v0.3.0",), vocals_scored=lambda _cfg: scored))
    finding = doctor._check_release(inputs)
    assert f'{command} @ git+{_REPO_URL}@v0.3.0"' in finding.detail


def test_a_library_has_scored_when_a_vocal_calibration_is_recorded(configured):
    """The shipped probe: the calibration a fit writes only from scored files."""
    assert doctor_model._vocals_scored(None) is False
    assert doctor_model._vocals_scored(configured) is False
    path = config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, configured)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"threshold": 12.0}', encoding="utf-8")
    assert doctor_model._vocals_scored(configured) is True


def test_a_git_install_of_a_branch_head_names_no_tag_that_does_not_exist(monkeypatch):
    """``@v0.3.1.dev3+g...`` is no tag, so the command is the vocals module's own."""
    monkeypatch.setattr(vocals, "install", lambda: "the vocals module's own command")
    origin = _vcs("0.3.1.dev3+gabc1234", ("analysis",))
    assert doctor_state.vocals_install_command(origin) == "the vocals module's own command"
    assert "@v0.3.0" in doctor_state.vocals_install_command(_vcs("0.3.0", ("analysis",)))
