"""U27: the setup wizard, the doctor, and the two reports beside them.

The suite is in six parts, and each one answers a specific way this unit could be
green and wrong:

1. **The check table is complete and ordered.** Every run answers every declared
   key, in the declared order, with the interpreter first. A report whose length
   depends on the machine is a report nobody can diff, and a check silently
   absent is a precondition nobody is checking.
2. **The three derived families really are derived.** Credentials, binaries and
   the acquisition contract are all expanded from somebody else's declaration.
   Each is asserted against its source, because "derived" that is 90 percent
   complete is worse than an honest list: it invites trust (P4).
3. **The five scenarios in the brief**, driven against synthetic machines through
   the real checks rather than through a copy of them.
4. **The wizard**, including the three things it must refuse to do: overwrite a
   configuration it cannot understand, re-derive a volume identity it already
   recorded, and adopt a version pin nobody agreed to.
5. **``crate login``**, which must never accept a credential as an argument.
6. **The guards this unit arms**, checked against the EVASION as well as against
   correct code, because running a guard only against correct code is the half
   that keeps getting skipped.
"""

from __future__ import annotations

import ast
import errno
import json
import os
import subprocess
import sys
import tomllib
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.acquire import adapter as adapter_contract
from cratekit.cli import doctor, prompt, registry, render
from cratekit.cli import jobs as jobs_cli
from cratekit.cli import setup as setup_verb
from cratekit.cli.doctor import Probes as RealProbes
from cratekit.cli.verbs import login as login_verb
from cratekit.core import backup_facts, binaries, config, jobs, profiles, secrets, session, taxonomy
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from tests import doctor_machines
from tests._hardware import filesystem_kind, hdiutil_available, read_only_volume
from tests.test_active_taxonomy import shipped_without, write_active
from tests.test_session_log_unlisted import _refuse_listing

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

#: A synthetic volume identity, from the shared machine description so the two
#: suites cannot describe two different disks. R1 forbids a shipped artifact from
#: carrying a real library string, which is why it is invented rather than read.
VOLUME = doctor_machines.VOLUME


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


def document_for(root: Path, **library_overrides) -> dict:
    """The smallest configuration that validates, against a synthetic library."""
    library = {
        "root": str(root),
        "volume_id": VOLUME,
        "db_path": str(root / "db" / "master.db"),
    }
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
    """No test in this file may reach a real terminal, however pytest was invoked.

    The wizard is the one verb that prompts, so a drive of it that fell through to
    the real standard input would BLOCK rather than fail, and it would do so only
    under ``pytest -s``, where capture is off. A test that hangs on one person's
    machine and passes on the build's is the worst shape a test can have, so the
    stream is replaced here rather than relied on being replaced by the runner.
    """

    class Trapped:
        def __getattr__(self, name):
            raise AssertionError(f"a test in this file read standard input (sys.stdin.{name})")

    monkeypatch.setattr(sys, "stdin", Trapped())
    monkeypatch.setattr(
        "builtins.input",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("a test called input()")),
    )


@pytest.fixture
def library(tmp_path, monkeypatch):
    """A synthetic library root, and the environment pointed at it.

    The override is re-set over the one the suite-wide fixture installs, because
    an override RELOCATES ``library.root`` on every load: leaving the suite's own
    temporary directory in place would silently move every config this file
    builds onto a different path than the one it is asserting about (P2).
    """
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def configured(library):
    cfg = config.from_dict(document_for(library))
    config.save(cfg)
    config.reset_cache()
    return config.load()


def probes(**overrides) -> doctor.Probes:
    """A machine on which every check passes, minus whatever a test breaks.

    Written as a green baseline rather than as a bare ``Probes()`` so a test
    naming one broken seam is asserting about that seam alone. A test that
    started from the real machine would pass or fail on whatever happens to be
    installed on it.

    The baseline itself moved to ``tests/doctor_machines.py`` when the verb
    conformance suite needed the same one: two copies of a machine description
    are two machines, and the property conformance 8 asserts is a comparison
    BETWEEN two runs, so the green one it compares against has to be this green
    one. The module holds the class captured at import time for the reason this
    function did, which is that a test replacing ``doctor.Probes`` to drive a
    synthetic machine through the real dispatcher must not thereby replace the
    thing that builds one.
    """
    return doctor_machines.green(**overrides)


def seed_taxonomy(cfg: config.Config) -> None:
    path = config.state_path("taxonomy_active", cfg)
    config.atomic_write_bytes(setup_verb.template_text("default").encode("utf-8"), path)


def find(report: doctor.Report, key: str) -> doctor.Finding:
    return next(finding for finding in report.findings if finding.key == key)


def drive(argv: list[str]) -> tuple[int, str, str]:
    import io

    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


# ═══════════════════════════════════════════════════════════════════════════
# 1. The check table
# ═══════════════════════════════════════════════════════════════════════════


def test_every_run_answers_every_declared_check_in_the_declared_order(configured):
    """Not "the failures are reported": every key, every run, same order.

    A report whose contents depend on which branch a machine took cannot be
    diffed between two runs or two machines, and a check that quietly stops
    appearing is a precondition that quietly stops being one.
    """
    report = doctor.run(configured, probes=probes())
    assert tuple(f.key for f in report.findings) == doctor.CHECK_KEYS
    assert len(set(doctor.CHECK_KEYS)) == len(doctor.CHECK_KEYS), "a key is declared twice"


def test_the_interpreter_is_checked_before_anything_else():
    """The brief says so, and the reason is that nothing below it means anything.

    On an interpreter the vendored tree has never run on, a green report about
    binaries and credentials is a report about a machine that cannot run the
    product at all.
    """
    assert doctor.CHECK_KEYS[0] == "interpreter.version"


def test_every_check_key_and_its_place_in_the_run_order_is_written_out():
    """The whole table, spelled out, because the previous version could not fail.

    It asserted ``CHECK_KEYS == tuple(check.key for check in CHECKS)`` and
    ``doctor.py`` DEFINES ``CHECK_KEYS`` as exactly that expression, so the
    assertion was the implementation restated and its own docstring conceded it.
    Round two removed this shape from ``tests/test_cli_contract.py`` and left
    this instance.

    The three families stay derived from the declarations doctor derives them
    FROM, rather than from ``CHECKS``, which is the whole difference: a binary
    added to ``core/binaries`` is still checked here with no edit, and dropping,
    renaming or reordering a check is a failure a reviewer reads.
    """
    assert doctor.CHECK_KEYS == (
        "interpreter.version",
        "config.present",
        "library.mounted",
        "library.identity",
        "library.db_containment",
        "library.trash",
        "taxonomy.active",
        "taxonomy.schema",
        "rekordbox.closed",
        "rekordbox.pins",
        "library.paths_resolved",
        "keychain.reachable",
        "credential.bandcamp",
        "credential.catalogue",
        "credential.provider",
        "credential.recognition",
        *(f"binary.{name}" for name in doctor.BINARY_NAMES),
        "adapter.contract",
        *(f"backup.age.{portion}" for portion in backup_facts.PORTIONS),
        "backup.acknowledgment",
        "backup.full_comparison",
        "backup.remote",
        "deadca7.push",
        "session.unresolved",
        "runs.open-gates",
        "provider.isrc-cache",
        "tree.registry",
        "repo.commit_hook",
        "install.extras",
        "install.release",
    )
    assert doctor.BINARY_NAMES == (
        *binaries.INSTALLABLE_BINARIES,
        *sorted(binaries.PLATFORM_BINARIES),
    )


def test_doctor_never_raises_when_there_is_no_configuration_at_all(tmp_path, monkeypatch):
    """The first machine doctor meets is the one with nothing on it.

    Everything downstream of configuration reports as unchecked rather than as a
    failure, because the failure is already reported once and repeating it twenty
    times buries it.
    """
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "empty"))
    config.reset_cache()
    report = doctor.run(probes=probes())

    assert tuple(f.key for f in report.findings) == doctor.CHECK_KEYS
    present = find(report, "config.present")
    assert present.status is doctor.Status.FAIL
    assert present.remedy is Remedy.RUN_SETUP
    assert find(report, "library.mounted").status is doctor.Status.INFO
    assert "not checked" in find(report, "library.mounted").detail


def test_a_configuration_from_a_newer_build_keeps_its_own_remedy(tmp_path, monkeypatch):
    """Five ways a config can be unusable, five remediations, and doctor carries
    the one that arrived rather than the class default.

    ``getattr(error, "remedy", something)`` would have handed back a permissive
    answer for a field whose whole point is that these five differ.
    """
    directory = tmp_path / "cfg"
    directory.mkdir()
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(directory))
    (directory / config.CONFIG_FILENAME).write_text(
        f"schema_version = {config.CURRENT_SCHEMA_VERSION + 5}\n"
    )
    config.reset_cache()

    present = find(doctor.run(probes=probes()), "config.present")
    assert present.status is doctor.Status.FAIL
    assert present.remedy is Remedy.UPGRADE_CRATEKIT


# ═══════════════════════════════════════════════════════════════════════════
# 2. The derived families
# ═══════════════════════════════════════════════════════════════════════════


def test_every_stored_credential_is_covered_by_exactly_one_check():
    """P4. A derivation that misses one member is a list wearing a derivation's
    clothes, and the member it misses is the credential nobody notices is unchecked.
    """
    covered = [
        name
        for names in doctor.CREDENTIALS_BY_CHECK.values()
        for name in names
    ]
    assert sorted(str(n) for n in covered) == sorted(str(n) for n in secrets.Credential)
    assert len(covered) == len(set(covered)), "one credential is claimed by two checks"


def test_every_credential_check_the_registry_declares_has_a_group_and_a_remedy():
    declared = {
        key
        for entry in registry.entries()
        for key in entry.doctor_checks
        if key.startswith("credential.")
    }
    assert declared <= set(doctor.CREDENTIALS_BY_CHECK)
    for key in doctor.CREDENTIALS_BY_CHECK:
        assert f"binary.{key}" not in doctor.CHECK_KEYS
        assert isinstance(Remedy(str(doctor._CREDENTIAL_REMEDY[key])), Remedy)


def test_every_binary_the_resolver_knows_about_is_probed():
    """The source system's doctor hand-listed six binaries. This one cannot.

    Both halves of ``core/binaries``' own tables are expanded, so a binary added
    there is checked here the day it is added rather than the day somebody
    remembers (P3).
    """
    probed = {key[len("binary.") :] for key in doctor.CHECK_KEYS if key.startswith("binary.")}
    assert probed == set(binaries.INSTALLABLE_BINARIES) | set(binaries.PLATFORM_BINARIES)


def test_the_acquisition_contract_is_read_off_the_protocol():
    """Derived, so a member added to the protocol is checked without an edit.

    Asserted against the protocol itself rather than against a copy: the point of
    the check is that a substitute adapter is measured against the WHOLE contract,
    and a hand-listed pair of names stops being the whole contract the moment the
    protocol grows a third member.
    """
    assert doctor.contract_members() == ("acquire", "name")

    class Grown(adapter_contract.AcquisitionAdapter):
        capabilities: tuple[str, ...]

        def reset(self) -> None: ...

    assert set(doctor.contract_members(Grown)) >= {"capabilities", "reset"}


def test_every_backup_portion_gets_its_own_answer():
    """One aggregate timestamp reports a half-protected library as protected.

    The normal state of a library backed up without quitting rekordbox is "files
    current, database stale", which is the one thing the warning exists to say.
    """
    reported = {key for key in doctor.CHECK_KEYS if key.startswith("backup.age.")}
    assert reported == {f"backup.age.{portion}" for portion in backup_facts.PORTIONS}


# ═══════════════════════════════════════════════════════════════════════════
# 3. The five scenarios in the brief
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unmounted_volume_and_a_moved_volume_produce_different_messages(
    tmp_path, monkeypatch
):
    """The brief's second scenario, and the reason ``preflight`` has five outcomes.

    "The volume is wrong" sends a user to unplug a drive that was never the
    problem. One of these says the disk is not attached; the other says it IS
    attached, somewhere else, and nothing needs plugging in.
    """
    absent = tmp_path / "not-mounted"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(absent))
    unmounted = doctor.run(
        config.from_dict(document_for(absent)),
        probes=probes(identity_provider=lambda _p: "0000-0000", mount_enumerator=lambda: ()),
    )

    elsewhere_root = tmp_path / "configured"
    (elsewhere_root / "Music").mkdir(parents=True)
    actually_at = tmp_path / "actually-here"
    actually_at.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(elsewhere_root))
    moved = doctor.run(
        config.from_dict(document_for(elsewhere_root)),
        probes=probes(
            identity_provider=lambda path: VOLUME if path == actually_at else "0000-0000",
            mount_enumerator=lambda: (actually_at,),
        ),
    )

    first = find(unmounted, "library.mounted")
    second = find(moved, "library.mounted")
    assert first.status is doctor.Status.FAIL and second.status is doctor.Status.FAIL
    assert first.detail != second.detail
    assert "not mounted anywhere" in first.detail
    assert "different mount point" in second.detail and str(actually_at) in second.detail


def test_a_foreign_volume_at_the_configured_root_is_its_own_answer(library):
    """The restored clone: right layout, right filenames, wrong disk.

    A directory check answers yes on a clone, which is why identity is asked for
    at all, and why this is not folded into "not mounted".
    """
    report = doctor.run(
        config.from_dict(document_for(library)),
        probes=probes(identity_provider=lambda _p: "9999-9999"),
    )
    identity = find(report, "library.identity")
    assert identity.status is doctor.Status.FAIL
    assert "9999-9999" in identity.detail and VOLUME in identity.detail
    assert identity.remedy is Remedy.MOUNT_LIBRARY_VOLUME


def test_a_module_enabled_without_its_credential_is_reported_with_the_fix(library):
    """The brief's third scenario, and it is derived rather than decided.

    Recognition is gated by the ``identify`` module. Switching that module off
    makes the same missing credential a note; switching it on makes it a failure.
    Nothing in the doctor module knows which module that is: it asks the registry
    which verbs declare the check and whether the profile switches any of them on.
    """
    missing = probes(credential_recorded=lambda name: name != str(secrets.Credential.IDENTIFY_KEY))

    on = doctor.run(config.from_dict(document_for(library)), probes=missing)
    finding = find(on, "credential.recognition")
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.SET_CREDENTIAL
    assert render.remedy_text(finding.remedy), "the fix must render to something"

    document = document_for(library)
    document["profile"] = {"name": "slim"}
    off = doctor.run(config.from_dict(document), probes=missing)
    assert find(off, "credential.recognition").status is doctor.Status.INFO


def _break_the_presence_index(monkeypatch) -> Path:
    """Leave a credential recorded and the index unreadable. Returns its path.

    Driven through the REAL ``secrets.exists`` rather than a probe that raises,
    because the finding being closed is that the reader answered False and the
    report believed it. A seam handed a prepared exception would pass over a
    reader that still answers False.
    """
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
    library, monkeypatch
):
    """Item 4 of the five-places residual finding, and the second half of its
    closing condition: doctor says which
    it saw.

    "Not recorded, record it" over a credential the keychain is holding is the
    loop R-116 measured, and the remedy never completes because recording it
    again does not move the index. The report now names the file and sends the
    person to the permission instead.
    """
    index = _break_the_presence_index(monkeypatch)
    machine = probes(credential_recorded=secrets.exists)

    report = doctor.run(config.from_dict(document_for(library)), probes=machine)
    finding = find(report, "credential.provider")

    assert finding.status is doctor.Status.FAIL
    assert str(index) in finding.detail
    assert "not recorded" not in finding.detail
    assert finding.remedy is not Remedy.AUTHENTICATE_PROVIDER
    assert finding.remedy is Remedy.GRANT_PATH_ACCESS
    assert render.remedy_text(finding.remedy), "the fix must render to something"


def test_an_unreadable_credential_index_costs_one_check_and_not_the_report(
    library, monkeypatch
):
    """Every other check still answers, which is doctor's standing contract: a
    report whose length depends on the machine is a report a consumer cannot diff.
    """
    _break_the_presence_index(monkeypatch)
    machine = probes(credential_recorded=secrets.exists)

    keys = {f.key for f in doctor.run(config.from_dict(document_for(library)), probes=machine).findings}
    green = {f.key for f in doctor.run(config.from_dict(document_for(library)), probes=probes()).findings}
    assert keys == green


def test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying(
    configured, monkeypatch
):
    """``_capture_credentials`` runs AFTER the configuration is saved, so a raise
    here loses the whole report over a file already on disk. That is the shape
    the same residual's third item spent four rounds closing, and the presence
    question is a new way
    into it.
    """
    index = _break_the_presence_index(monkeypatch)
    wizard = setup_verb._Wizard({}, Scripted(["yes", "yes", "yes"], ["k3y", "s1gn", "s3cret"]))

    setup_verb._capture_credentials(wizard, configured)

    offered = [note for note in wizard.notes if note.key.startswith("setup.credential.")]
    assert offered, "no credential was reported, so nothing here was exercised"
    broken = [note for note in offered if note.status is doctor.Status.FAIL]
    assert broken, "an unanswerable presence question was not reported at all"
    assert all(str(index) in note.detail for note in broken)
    assert all(note.remedy is Remedy.GRANT_PATH_ACCESS for note in broken)


def test_the_wizard_notes_an_index_that_refuses_the_write_rather_than_dying(
    configured, monkeypatch
):
    """The other way into the wizard, and it was open after the first leg closed.

    ``secrets.set`` notes the name in the presence index after the keychain write,
    through the same reader, so an unusable index refuses on the WRITE as well as
    on the probe. ``secrets.CredentialError`` is not a ``CratekitError``, so the
    handler already beside it does not catch this, and the window is a person
    typing a secret.

    DAMAGED WHILE THE SECRET IS BEING TYPED, which is the only arrangement that
    reaches the write leg at all: an index that is already unusable refuses at the
    probe one line above and the write is never attempted. Writing it that way
    passed against the build this test was written to fail, and the window it
    models is the real one, since a person at a password prompt is as long as
    windows in this product get.
    """
    index = config.state_path("credential_index")
    answers = ["yes", "yes", "yes"]
    held = ["k3y", "s1gn", "s3cret"]

    def read_secret(_question):
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text("{not json at all")
        return held.pop(0) if held else _eof()

    scripted = prompt.Prompter(
        read_line=lambda: (answers.pop(0) + "\n") if answers else _eof(),
        read_secret=read_secret,
        write=lambda _text: None,
    )
    wizard = setup_verb._Wizard({}, scripted)

    setup_verb._capture_credentials(wizard, configured)

    offered = [note for note in wizard.notes if note.key.startswith("setup.credential.")]
    assert offered, "no credential was reported, so nothing here was exercised"
    assert all(note.status is doctor.Status.FAIL for note in offered)
    assert all(str(index) in note.detail for note in offered)
    assert all(note.remedy is Remedy.REPAIR_CREDENTIAL_STORE for note in offered)
    # And no typed value reaches the report, which is the standing rule for every
    # note this function writes and is worth re-asserting on a new branch of it.
    rendered = json.dumps([note.to_json() for note in wizard.notes])
    for value in ("k3y", "s1gn", "s3cret"):
        assert value not in rendered


def test_a_missing_binary_is_reported_with_where_it_comes_from(library):
    """The brief's fourth scenario. Reported BEFORE any spend, which is what a
    precondition means: the alternative is discovering it part way through a
    download whose identification calls have already been paid for.
    """
    report = doctor.run(
        config.from_dict(document_for(library)),
        probes=probes(find_binary=lambda name: None if name == "ffmpeg" else f"/bin/{name}"),
    )
    finding = find(report, "binary.ffmpeg")
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.INSTALL_BINARY
    assert binaries.env_var("ffmpeg") in finding.detail


def test_a_binary_no_enabled_verb_needs_is_a_note_rather_than_a_failure(library):
    """P7 in the report itself. rclone is only reachable through the backup
    module, so on an install without it a missing rclone is worth knowing and is
    not a problem, and painting it red teaches people to ignore red.
    """
    document = document_for(library)
    document["profile"] = {"name": "slim"}
    report = doctor.run(
        config.from_dict(document),
        probes=probes(find_binary=lambda name: None if name == "rclone" else f"/bin/{name}"),
    )
    assert find(report, "binary.rclone").status is doctor.Status.INFO
    assert "no verb this profile switches on" in find(report, "binary.rclone").detail


def test_doctor_verifies_the_configured_adapter_against_the_contract(library):
    """The brief's fifth scenario. R9's whole promise is that the downloader is
    replaceable, and a substitute that does not satisfy the protocol is a
    substitution that fails at the first download rather than at configuration.
    """
    document = document_for(library)
    document["acquisition"] = {"adapter": "streamrip"}
    ok = doctor.run(config.from_dict(document), probes=probes())
    assert find(ok, "adapter.contract").status is doctor.Status.OK
    assert "streamrip" in find(ok, "adapter.contract").detail

    document["acquisition"] = {"adapter": "not-a-real-adapter"}
    unknown = doctor.run(config.from_dict(document), probes=probes())
    finding = find(unknown, "adapter.contract")
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.CHOOSE_KNOWN_ADAPTER


def test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check(library):
    """U197. The check refuses a configured name the resolved class does not call
    itself, so the retired key would read as a mismatch unless it is folded where
    the file is read. Folded, the check passes and names the current key."""
    document = document_for(library)
    document["acquisition"] = {"adapter": "tidal_dl_ng"}
    finding = find(doctor.run(config.from_dict(document), probes=probes()), "adapter.contract")
    assert finding.status is doctor.Status.OK, finding.detail
    assert "'vendored'" in finding.detail
    assert "tidal_dl_ng" not in finding.detail


def test_an_adapter_whose_name_disagrees_with_the_configuration_is_refused(
    library, monkeypatch
):
    """The identity every result is reported under has to be the one selected.

    Two names for one adapter means a run reports work against an adapter nobody
    chose, and the mismatch is invisible in every other check.
    """

    class Impostor:
        name = "something-else"

        def acquire(self, requests):  # pragma: no cover - never called
            raise NotImplementedError

    monkeypatch.setattr("cratekit.acquire.load", lambda _name: Impostor)
    finding = find(
        doctor.run(config.from_dict(document_for(library)), probes=probes()),
        "adapter.contract",
    )
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.SWITCH_ADAPTER


def test_an_adapter_missing_a_contract_member_is_refused(library, monkeypatch):
    class Partial:
        name = "vendored"

    monkeypatch.setattr("cratekit.acquire.load", lambda _name: Partial)
    finding = find(
        doctor.run(config.from_dict(document_for(library)), probes=probes()),
        "adapter.contract",
    )
    assert finding.status is doctor.Status.FAIL
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
        # A specifier that yields NO clause compares nothing, so it answers
        # nothing. Returning True for these was the initialisation showing
        # through: ``verdict`` started at True and a loop that ran no comparison
        # handed it straight back, which made "this bound says nothing" and "this
        # version satisfies it" the same answer.
        ((3, 12, 1), "", None),
        ((3, 12, 1), "   ", None),
        ((3, 12, 1), ",,", None),
        # And a bound that DOES compare still answers, including when only one of
        # several clauses is meaningful.
        ((3, 12, 1), ">=3.12,", True),
    ],
)
def test_the_interpreter_specifier_parser_answers_or_says_it_cannot(
    version, specifier, expected
):
    """Three answers, not two. A specifier shape this parser does not know
    returns None, and the caller reports "not asserted" rather than a pass:
    guessing at a shape is how a bound stops being a bound.
    """
    assert doctor.satisfies(version, specifier) is expected


def test_a_specifier_that_compares_nothing_is_not_a_pass():
    """The evasion, run against the initialisation that permitted it.

    ``verdict = True`` at the top of the loop meant any specifier the parser
    walked without executing a comparison returned True. It is degenerate for a
    real build backend, which is exactly why nothing caught it, and it is the
    same shape as every other defect in this unit's review: a positive claim
    reached by falling through rather than by observing anything.
    """
    for specifier in ("", "   ", ",", " , ", "\t"):
        assert doctor.satisfies((3, 12, 5), specifier) is None, specifier


def test_an_unsupported_interpreter_fails_and_an_unreadable_bound_does_not(library):
    outside = doctor.run(
        config.from_dict(document_for(library)),
        probes=probes(python_version=(3, 14, 0)),
    )
    finding = find(outside, "interpreter.version")
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.UNSUPPORTED_PLATFORM

    unknown = doctor.run(
        config.from_dict(document_for(library)), probes=probes(requires_python=None)
    )
    assert find(unknown, "interpreter.version").status is doctor.Status.INFO


def test_the_declared_bound_is_read_from_packaging_rather_than_repeated():
    """KTD19's bound lives in one place, and this is not it.

    A constant in the doctor module would be a second copy of one decision, and
    the copy that drifts is always the one nobody is looking at.
    """
    declared = (REPO_ROOT / "pyproject.toml").read_text()
    source = (SRC_ROOT / "cratekit" / "cli" / "doctor.py").read_text()
    for bound in (">=3.12", "<3.14"):
        assert bound in declared
        assert bound not in source


# ── the pins, the processes, the sessions ────────────────────────────────────


def test_an_unrecorded_application_pin_fails_and_names_the_installed_version(library):
    """S2. An unset pin refuses every database write, and doctor says so on every
    run rather than leaving the user to meet it at the write.
    """
    document = document_for(library)
    document["rekordbox"] = {}
    finding = find(
        doctor.run(config.from_dict(document), probes=probes()), "rekordbox.pins"
    )
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.RECORD_REKORDBOX_PIN
    assert "7.0.1" in finding.detail


def test_a_drifted_application_pin_is_a_different_answer_from_an_unset_one(library):
    finding = find(
        doctor.run(
            config.from_dict(document_for(library)),
            probes=probes(installed_app_version=lambda _cfg: "8.0.0"),
        ),
        "rekordbox.pins",
    )
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.REVALIDATE_PINS
    assert "frozen by design" in finding.detail


def test_a_pin_that_was_never_confirmed_against_a_write_is_reported(library):
    document = document_for(library)
    document["rekordbox"] = {"pinned_app_version": "7.0.1"}
    finding = find(
        doctor.run(config.from_dict(document), probes=probes()), "rekordbox.pins"
    )
    assert finding.status is doctor.Status.INFO
    assert "a number somebody typed" in finding.detail


def test_a_running_rekordbox_agent_is_reported_even_with_the_window_closed(library):
    finding = find(
        doctor.run(
            config.from_dict(document_for(library)),
            probes=probes(process_lister=lambda: ("rekordboxAgent.exe",)),
        ),
        "rekordbox.closed",
    )
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.QUIT_REKORDBOX
    assert "rekordboxAgent" in finding.detail


def test_a_committed_unverified_session_is_reported_before_the_next_write(configured):
    """The refusal a user would otherwise meet at their next write, surfaced early.

    The session log SURVIVES a rollback, so the condemning record outlives the
    restore that answers it; doctor is where it stays visible in between.
    """
    record = session.SessionRecord(
        session_id="s-1",
        workflow="route.inbox",
        started="2026-08-02T00:00:00+00:00",
        state=session.SessionState.COMMITTED_UNVERIFIED,
    )
    session.write_record(record, configured)

    finding = find(doctor.run(configured, probes=probes()), "session.unresolved")
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.RESTORE_FROM_SNAPSHOT
    assert "s-1" in finding.detail


def test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it(configured):
    """R-598. Listed bare, a record a hard kill left reads as a run in progress.

    The live record beside it is the control: the clause is about the dead
    holder, not about being open.
    """
    import subprocess
    import sys

    finished = subprocess.Popen([sys.executable, "-c", "pass"])
    finished.wait()
    here = session.current_holder()
    gone = session.Holder(host=here.host, boot=here.boot, pid=finished.pid, started="1.000")
    orphan = session.open_session(configured, workflow="w", session_id="s-dead", holder=gone)
    live = session.open_session(configured, workflow="w", session_id="s-live", holder=here)

    finding = find(doctor.run(configured, probes=probes()), "session.unresolved")
    assert finding.status is doctor.Status.INFO
    assert f"{orphan.session_id} (open, its process is gone, crate session release" in (
        finding.detail
    )
    assert f"{live.session_id} (open)" in finding.detail


def test_an_unreadable_session_record_is_reported_rather_than_dropped(configured):
    """A gate reading its own state through a tolerant reader fails OPEN.

    ``scan_log`` returns both halves for exactly this reason, and doctor reports
    the half that will refuse rather than the half it can read.
    """
    log = session.log_dir(configured)
    log.mkdir(parents=True, exist_ok=True)
    (log / "wrecked.json").write_text("{not json")

    finding = find(doctor.run(configured, probes=probes()), "session.unresolved")
    assert finding.status is doctor.Status.FAIL
    assert "wrecked.json" in finding.detail


def test_a_backup_recorded_in_the_future_is_refused_rather_than_treated_as_fresh(
    configured,
):
    """A negative age reads as the freshest possible value to any comparison, so
    a skewed clock silently satisfies every freshness check it should fail.
    """
    backup_facts.record(
        configured,
        backup_facts.Portion.FILES,
        completed_at=datetime(2026, 9, 1, tzinfo=timezone.utc),
        destination="somewhere",
    )
    finding = find(doctor.run(configured, probes=probes()), "backup.age.files")
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.REPAIR_BACKUP_FACTS


def test_a_recorded_backup_reports_its_age_and_its_destination(configured):
    backup_facts.record(
        configured,
        backup_facts.Portion.DATABASE,
        completed_at=datetime(2026, 8, 2, tzinfo=timezone.utc) - timedelta(days=9),
        destination="a-remote:bucket",
    )
    finding = find(doctor.run(configured, probes=probes()), "backup.age.database")
    assert finding.status is doctor.Status.INFO
    assert "9 days ago" in finding.detail and "a-remote:bucket" in finding.detail


#: U184. One clock for the acknowledgment tests, so "valid" and "expired" are
#: measured against the instant doctor reads rather than the wall clock.
ACK_NOW = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)


def _acknowledged(cfg: config.Config, at: datetime) -> session.Acknowledgment:
    """An acknowledgment minted at ``at`` by the session rule, over young backups."""
    for portion in backup_facts.Portion:
        backup_facts.record(
            cfg, portion, completed_at=at - timedelta(days=1), destination="probe"
        )
    return session.record_acknowledgment(cfg, now=at, decided_by=session.SESSION_ACTOR)


def test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages(configured):
    """U184: the third fact a destructive verb consults, after the two it was minted over."""
    minted = _acknowledged(configured, ACK_NOW - timedelta(hours=2, minutes=30))

    report = doctor.run(configured, probes=probes(now=ACK_NOW))

    finding = find(report, "backup.acknowledgment")
    assert finding.status is doctor.Status.INFO
    expires = minted.expires_at.replace(microsecond=0).isoformat()
    assert finding.detail == (
        f"valid until {expires}, 9h 30m from now, minted by the session-ages rule"
    )
    keys = [one.key for one in report.findings]
    ages = [keys.index(f"backup.age.{portion}") for portion in backup_facts.PORTIONS]
    assert keys.index("backup.acknowledgment") == max(ages) + 1


def test_doctor_names_when_an_acknowledgment_lapsed(configured):
    minted = _acknowledged(configured, ACK_NOW - timedelta(hours=13))

    finding = find(doctor.run(configured, probes=probes(now=ACK_NOW)), "backup.acknowledgment")

    assert finding.status is doctor.Status.INFO
    expires = minted.expires_at.replace(microsecond=0).isoformat()
    assert finding.detail.startswith(f"expired at {expires};"), finding.detail
    assert "crate session ack" in finding.detail


def test_doctor_says_when_no_acknowledgment_is_on_record(configured):
    finding = find(doctor.run(configured, probes=probes()), "backup.acknowledgment")

    assert finding.status is doctor.Status.INFO
    assert finding.detail.startswith("none on record"), finding.detail


def test_an_acknowledgment_that_cannot_be_understood_is_a_failure(configured):
    path = session.ack_path(configured)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{ not json")

    finding = find(doctor.run(configured, probes=probes()), "backup.acknowledgment")

    assert finding.status is doctor.Status.FAIL
    assert "not readable as JSON" in finding.detail
    assert finding.remedy is Remedy.REPORT_DEFECT


def test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read(configured, tmp_path):
    """The record lives on the library volume, so a missing volume is not "none"."""
    _acknowledged(configured, ACK_NOW)
    configured.library.root.rename(tmp_path / "detached")

    finding = find(doctor.run(configured, probes=probes(now=ACK_NOW)), "backup.acknowledgment")

    assert finding.status is doctor.Status.INFO
    assert "not asserted" in finding.detail
    assert "none on record" not in finding.detail


def test_a_remote_whose_provider_trashes_on_delete_is_reported(configured):
    """The residual finding "Backup pruning reclaims space only if the remote is
    configured to", closed. The source system passed a provider flag from inside the
    prune, which is the one-provider assumption this port removed; without the
    per-remote option a pruned archive keeps counting against the quota, which is
    the whole point of pruning.
    """
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:"}
    cfg = config.from_dict(document)

    trashing = probes(rclone_remotes=lambda _r: {"archive": {"type": "drive"}})
    finding = find(doctor.run(cfg, probes=trashing), "backup.remote")
    assert finding.status is doctor.Status.FAIL
    assert "use_trash" in finding.detail

    disabled = probes(
        rclone_remotes=lambda _r: {"archive": {"type": "drive", "use_trash": "false"}}
    )
    assert find(doctor.run(cfg, probes=disabled), "backup.remote").status is doctor.Status.OK


def test_a_backup_module_with_no_destination_is_a_note_rather_than_a_failure(library):
    """The full preset switches backup on for everybody. Failing here would paint
    a correct install red on the day it is set up (P7).
    """
    finding = find(
        doctor.run(config.from_dict(document_for(library)), probes=probes()), "backup.remote"
    )
    assert finding.status is doctor.Status.INFO


#: What pre-commit's own installer writes, reduced to the lines that decide
#: whether the hook dispatches: the tool's hook implementation, the stage it was
#: installed for, and the configuration it reads.
INSTALLED_HOOK = (
    "#!/usr/bin/env bash\n"
    "# File generated by pre-commit: https://pre-commit.com\n"
    "ARGS=(hook-impl --config=.pre-commit-config.yaml --hook-type=pre-commit)\n"
    'exec pre-commit "${ARGS[@]}"\n'
)


def hooked_checkout(root: Path, body: str = INSTALLED_HOOK, *, config_file: bool = True):
    """A synthetic checkout with a git directory, a hook, and its configuration."""
    (root / ".git" / "hooks").mkdir(parents=True, exist_ok=True)
    (root / ".git" / "hooks" / "pre-commit").write_text(body)
    if config_file:
        (root / ".pre-commit-config.yaml").write_text("repos: []\n")
    return root


def hook_finding(library, checkout) -> doctor.Finding:
    return find(
        doctor.run(
            config.from_dict(document_for(library)),
            probes=probes(checkout_root=lambda: checkout),
        ),
        "repo.commit_hook",
    )


def test_the_commit_hook_check_says_nothing_on_an_installed_package(library):
    """The commit hook finding is a developer check. Reporting a missing developer tool to somebody
    who is not a developer is noise, and noise is what stops the report being read.
    """
    installed = find(
        doctor.run(config.from_dict(document_for(library)), probes=probes()),
        "repo.commit_hook",
    )
    assert installed.status is doctor.Status.INFO

    bare = library / "checkout"
    (bare / ".git" / "hooks").mkdir(parents=True)
    missing = hook_finding(library, bare)
    assert missing.status is doctor.Status.FAIL
    assert "pre-commit install" in missing.detail

    present = hook_finding(library, hooked_checkout(bare))
    assert present.status is doctor.Status.OK


@pytest.mark.parametrize(
    "body, config_file, because",
    [
        # The EVASION the substring test admitted: a hook whose entire content is
        # a mention of the word. It runs nothing.
        ("#!/bin/sh\n# pre-commit\nexit 0\n", True, "hook-impl"),
        # A hook installed for a different stage, copied into this file.
        (
            "ARGS=(hook-impl --config=.pre-commit-config.yaml --hook-type=pre-push)\n",
            True,
            "--hook-type=pre-commit",
        ),
        # A hook that dispatches to ANOTHER repository's configuration, so these
        # commits are scanned by somebody else's rules or by none.
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
    ],
)
def test_a_hook_that_does_not_dispatch_to_this_repository_is_refused(
    library, tmp_path, body, config_file, because
):
    """The sentence of the residual finding "The commit hook is off by default on a
    fresh clone", made true.

    The check CLAIMED it refused when the hook "does not dispatch to this
    repository's pre-commit configuration" and tested ``"pre-commit" in body``,
    which is satisfied by a comment. Each row here is a hook that passes that
    substring and runs no scan over this repository's commits.
    """
    checkout = hooked_checkout(tmp_path / "checkout", body, config_file=config_file)
    finding = hook_finding(library, checkout)
    assert finding.status is doctor.Status.FAIL, finding.detail
    assert because in finding.detail


def test_the_repositorys_own_installed_hook_passes_the_check(library):
    """The other half of every guard: it must also pass on correct code.

    Run against this checkout's REAL hook when there is one, because a guard
    tightened until only its fixtures pass it is a guard that fires on the
    correct setup, and those get worked around rather than fixed (P7).
    """
    root = doctor._checkout_root()
    if root is None:  # pragma: no cover - an installed wheel has no checkout
        return
    git_dir, unreadable, _remedy = doctor._git_dir(root)
    assert unreadable is None, unreadable
    hook = git_dir / "hooks" / "pre-commit" if git_dir else None
    if hook is None or not hook.is_file():  # pragma: no cover - a clone with no hook
        return
    assert doctor._hook_dispatch_problem(hook.read_text(), root) is None


def test_a_worktree_finds_the_hook_in_the_common_git_directory(tmp_path):
    """A worktree's ``.git`` is a FILE naming a directory that names the COMMON
    one, where hooks actually live. Following only the first pointer reports every
    worktree as unhooked while the hook is installed and running, which is a guard
    that fires on correct setups (P7).
    """
    common = tmp_path / "main" / ".git"
    (common / "hooks").mkdir(parents=True)
    (common / "hooks" / "pre-commit").write_text(INSTALLED_HOOK)
    per_tree = common / "worktrees" / "w1"
    per_tree.mkdir(parents=True)
    (per_tree / "commondir").write_text("../..\n")

    worktree = tmp_path / "w1"
    worktree.mkdir()
    (worktree / ".git").write_text(f"gitdir: {per_tree}\n")

    assert doctor._git_dir(worktree) == (common.resolve(), None, None)
    assert doctor._git_dir(tmp_path / "main") == (common, None, None)


#: The shape of this repository's own configuration that decides the answer: one
#: hook on the default stage and one on the commit-msg stage.
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
    "        stages: [commit-msg]\n"
)

#: What pre-commit's installer writes for the second type: the same template,
#: bound to the other stage.
INSTALLED_COMMIT_MSG_HOOK = INSTALLED_HOOK.replace(
    "--hook-type=pre-commit", "--hook-type=commit-msg"
)

TWO_STAGE_COMMAND = "pre-commit install --hook-type pre-commit --hook-type commit-msg"


def two_stage_checkout(root: Path, *, commit_msg: str | None = INSTALLED_COMMIT_MSG_HOOK):
    """A synthetic checkout configured for two stages, with the pre-commit hook installed."""
    hooked_checkout(root)
    (root / ".pre-commit-config.yaml").write_text(TWO_STAGE_CONFIG)
    if commit_msg is not None:
        (root / ".git" / "hooks" / "commit-msg").write_text(commit_msg)
    return root


def test_a_configured_commit_msg_stage_with_no_hook_is_refused(library, tmp_path):
    """The widened half of the residual finding "The commit hook is off by default
    on a fresh clone".

    `pre-commit install` alone writes the pre-commit hook and nothing else, so a
    clone set up from a one-line instruction has the scan and silently lacks the
    closing check on the commit-msg stage. The check looked at one file and said
    green over that clone.
    """
    finding = hook_finding(library, two_stage_checkout(tmp_path / "checkout", commit_msg=None))
    assert finding.status is doctor.Status.FAIL, finding.detail
    assert "no commit-msg hook" in finding.detail
    assert TWO_STAGE_COMMAND in finding.detail


def test_every_configured_hook_type_installed_passes_the_check(library, tmp_path):
    """The other half of every guard: the correct setup is green, and says why."""
    finding = hook_finding(library, two_stage_checkout(tmp_path / "checkout"))
    assert finding.status is doctor.Status.OK, finding.detail
    assert "commit-msg" in finding.detail


def test_a_commit_msg_hook_installed_for_another_stage_is_refused(library, tmp_path):
    """A pre-commit hook copied into the commit-msg slot runs the scan, not the closing check."""
    checkout = two_stage_checkout(tmp_path / "checkout", commit_msg=INSTALLED_HOOK)
    finding = hook_finding(library, checkout)
    assert finding.status is doctor.Status.FAIL, finding.detail
    assert "--hook-type=commit-msg" in finding.detail
    assert TWO_STAGE_COMMAND in finding.detail


def test_a_fresh_clone_is_told_the_whole_install_line(library, tmp_path):
    """R-1's own scenario, a clone with no hook at all, gets the line that installs both."""
    checkout = tmp_path / "checkout"
    (checkout / ".git" / "hooks").mkdir(parents=True)
    (checkout / ".pre-commit-config.yaml").write_text(TWO_STAGE_CONFIG)
    finding = hook_finding(library, checkout)
    assert finding.status is doctor.Status.FAIL, finding.detail
    assert "no pre-commit hook" in finding.detail
    assert TWO_STAGE_COMMAND in finding.detail


def test_a_commit_msg_hook_that_cannot_be_read_is_unknown_not_missing(library, tmp_path):
    """The split the pre-commit hook already makes, carried to every other type."""
    checkout = two_stage_checkout(tmp_path / "checkout")
    other = checkout / ".git" / "hooks" / "commit-msg"
    other.chmod(0o000)
    try:
        finding = hook_finding(library, checkout)
    finally:
        other.chmod(0o644)
    assert finding.status is doctor.Status.FAIL, finding.detail
    assert "unknown rather than no" in finding.detail
    assert "no commit-msg hook" not in finding.detail
    assert finding.remedy is Remedy.GRANT_PATH_ACCESS


def test_a_configuration_that_does_not_parse_is_not_read_as_one_hook_type(library, tmp_path):
    """Falling back to the floor would report green over the gap this check closes."""
    checkout = two_stage_checkout(tmp_path / "checkout", commit_msg=None)
    (checkout / ".pre-commit-config.yaml").write_text("repos: [\n")
    finding = hook_finding(library, checkout)
    assert finding.status is doctor.Status.FAIL, finding.detail
    assert "not valid YAML" in finding.detail


def test_a_configuration_that_cannot_be_read_is_unknown_and_asks_for_access(
    library, tmp_path
):
    """The hook names a file that is there; this account cannot open it. That is a
    permission to grant, and the stages it configures are unknown rather than none.
    """
    checkout = two_stage_checkout(tmp_path / "checkout", commit_msg=None)
    config_file = checkout / ".pre-commit-config.yaml"
    config_file.chmod(0o000)
    try:
        finding = hook_finding(library, checkout)
    finally:
        config_file.chmod(0o644)
    assert finding.status is doctor.Status.FAIL, finding.detail
    assert "could not be read" in finding.detail
    assert "unknown rather than no" in finding.detail
    assert finding.remedy is Remedy.GRANT_PATH_ACCESS


def test_a_clone_with_no_configuration_is_told_the_floor(library, tmp_path):
    """No configuration to read means the line names the one type that is always needed,
    rather than a bare installer call with nothing after it.
    """
    checkout = tmp_path / "checkout"
    (checkout / ".git" / "hooks").mkdir(parents=True)
    finding = hook_finding(library, checkout)
    assert finding.status is doctor.Status.FAIL, finding.detail
    assert "Run `pre-commit install --hook-type pre-commit` in" in finding.detail


def test_no_yaml_reader_is_unknown_rather_than_one_hook_type(library, tmp_path, monkeypatch):
    """PyYAML arrives with the dev extra, not the runtime, so its absence is reachable."""
    monkeypatch.setitem(sys.modules, "yaml", None)
    finding = hook_finding(library, two_stage_checkout(tmp_path / "checkout"))
    assert finding.status is doctor.Status.FAIL, finding.detail
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
        f"        stages: {stages}\n"
    )


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
    ],
)
def test_the_hook_types_a_configuration_needs(tmp_path, text, expected):
    config_file = tmp_path / ".pre-commit-config.yaml"
    config_file.write_text(text)
    assert doctor._configured_hook_types(config_file) == (expected, None, None)


@pytest.mark.parametrize(
    "text, because",
    [
        (_stage_config("[on-commit]"), "'on-commit'"),
        (_stage_config("[{stage: commit}]"), "installs no hook for"),
        ("- just\n- a list\n", "is not a pre-commit configuration"),
    ],
)
def test_a_configuration_this_cannot_understand_is_a_sentence(tmp_path, text, because):
    """An unknown stage is not a stage that needs nothing."""
    config_file = tmp_path / ".pre-commit-config.yaml"
    config_file.write_text(text)
    types, problem, _remedy = doctor._configured_hook_types(config_file)
    assert types == ()
    assert problem is not None and because in problem


def test_this_repositorys_own_configuration_needs_both_hook_types():
    """Pinned against the tree rather than a fixture authored beside the reader."""
    root = doctor._checkout_root()
    if root is None:  # pragma: no cover - an installed wheel has no checkout
        return
    types, problem, _remedy = doctor._configured_hook_types(root / ".pre-commit-config.yaml")
    assert problem is None, problem
    assert types == ("pre-commit", "commit-msg")


def test_a_commit_msg_hook_on_another_configuration_is_refused(library, tmp_path):
    """The types were read from the pre-commit hook's configuration, so a hook for
    one of them dispatching to any other file runs a stage that configuration does
    not describe, and its closing check never runs.
    """
    checkout = two_stage_checkout(
        tmp_path / "checkout",
        commit_msg=INSTALLED_COMMIT_MSG_HOOK.replace(
            ".pre-commit-config.yaml", "tools/other.yaml"
        ),
    )
    (checkout / "tools").mkdir()
    (checkout / "tools" / "other.yaml").write_text("repos: []\n")
    finding = hook_finding(library, checkout)
    assert finding.status is doctor.Status.FAIL, finding.detail
    assert "dispatches to tools/other.yaml, not .pre-commit-config.yaml" in finding.detail


def test_the_install_line_names_a_configuration_that_is_not_the_default(library, tmp_path):
    """The installer rewrites every hook to the configuration it is given, and with
    none that is the default. Advice that omits it breaks a hook that was working.
    """
    checkout = tmp_path / "checkout"
    (checkout / "tools").mkdir(parents=True)
    (checkout / "tools" / "hooks.yaml").write_text(TWO_STAGE_CONFIG)
    hooked_checkout(
        checkout,
        INSTALLED_HOOK.replace(".pre-commit-config.yaml", "tools/hooks.yaml"),
        config_file=False,
    )
    finding = hook_finding(library, checkout)
    assert finding.status is doctor.Status.FAIL, finding.detail
    assert (
        "pre-commit install --config tools/hooks.yaml "
        "--hook-type pre-commit --hook-type commit-msg"
    ) in finding.detail


# ═══════════════════════════════════════════════════════════════════════════
# 4. The wizard
# ═══════════════════════════════════════════════════════════════════════════


class Scripted(prompt.Prompter):
    """A prompter with its answers queued, driving the REAL ask and confirm."""

    def __new__(cls, answers, secrets_=()):
        queued = list(answers)
        held = list(secrets_)
        return prompt.Prompter(
            read_line=lambda: (queued.pop(0) + "\n") if queued else _eof(),
            read_secret=lambda _q: held.pop(0) if held else _eof(),
            write=lambda _text: None,
        )


def _eof():
    raise EOFError("nothing left in the script")


def silent() -> prompt.Prompter:
    """A machine where nothing can be asked, which is every scripted run."""
    return prompt.Prompter(read_line=_eof, read_secret=lambda _q: _eof(), write=lambda _t: None)


def test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor(
    tmp_path, monkeypatch
):
    """The brief's first scenario, end to end through the real dispatcher.

    Every answer is supplied as a flag, which is the property that makes the ONE
    interactive verb scriptable: a verb that can only be driven by typing at it
    cannot be exercised end to end by anything except a person.
    """
    root = tmp_path / "fresh"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setattr(doctor, "Probes", lambda: probes())

    code, out, err = drive(
        [
            "--output", "json", "setup",
            "--library-root", str(root),
            "--db-path", str(root / "db" / "master.db"),
            "--volume-id", VOLUME,
            "--staging", str(tmp_path / "staging"),
            "--profile", "slim",
            "--taxonomy", "default",
        ]
    )
    envelope = json.loads(out)
    written = config.load()
    assert written.library.volume_id == VOLUME
    assert written.profile.name == "slim"
    assert config.state_path("taxonomy_active", written).is_file()

    # The pin is the one thing a clean machine cannot have, and it is the one
    # thing setup may not adopt on the user's behalf (S2).
    failing = [c["key"] for c in envelope["data"]["checks"] if c["status"] == "fail"]
    assert failing == ["rekordbox.pins"], (envelope["data"]["checks"], err)
    assert code == int(ExitCode.PRECONDITION)

    document = json.loads(json.dumps(document_for(root)))
    document["profile"] = {"name": "slim"}
    assert config.validate(document) == []
    assert doctor.run(config.from_dict(document), probes=probes()).ok


def state_fingerprint(*roots) -> dict[str, tuple[int, int]]:
    """Size and modification time of every file under each root.

    "It wrote nothing" is asserted against the FILESYSTEM rather than inferred
    from reading the code, for the same reason the destructive-session assertion
    does it: the class of defect being guarded is a read-only path that already
    wrote something before anybody noticed.
    """
    import os

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
    """A diagnostic that changes the thing it is diagnosing is not a diagnostic.

    It also has to be safe to run on a library whose volume is WRONG, which is
    precisely the moment a write would land somewhere nobody intended, so the
    probe here is the foreign-volume one.

    Asserted about ``run`` rather than about the whole invocation on purpose: the
    dispatcher persists a run record for every verb it dispatches, which is the
    shell's own state and is not this module's to avoid.
    """
    seed_taxonomy(configured)
    roots = (
        configured.library.root,
        config.installation_state_dir(),
        config.config_dir(),
    )
    before = state_fingerprint(*roots)
    report = doctor.run(configured, probes=probes(identity_provider=lambda _p: "9999"))
    assert not report.ok
    assert state_fingerprint(*roots) == before


def test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to(
    configured, monkeypatch
):
    """The property that makes re-running the wizard cheap rather than dangerous.

    Every answer resolves from what is already recorded, so nothing is prompted;
    the file is rewritten with the same content, and the volume identity, the
    profile and the taxonomy choice all survive untouched. A wizard that asked
    everything again is a wizard people stop re-running, and then the checks it
    performs at the end never run either.
    """
    seed_taxonomy(configured)
    monkeypatch.setattr(doctor, "Probes", lambda: probes())
    before = config.load().to_toml_dict()

    code, out, err = drive(["--output", "json", "setup"])
    assert code == int(ExitCode.OK), err
    envelope = json.loads(out)
    assert envelope["data"]["summary"]["answered"] == []
    assert envelope["data"]["summary"]["provenance"] == "existing"

    config.reset_cache()
    assert config.load().to_toml_dict() == before


def test_the_wizard_reports_no_check_key_twice(configured, monkeypatch):
    """One report, one row per thing. Two credentials share one check key, so a
    note keyed on the check would emit that key twice and a consumer keying on it
    would keep whichever arrived last.
    """
    seed_taxonomy(configured)
    monkeypatch.setattr(doctor, "Probes", lambda: probes(credential_recorded=lambda _n: False))
    _code, out, _err = drive(["--output", "json", "setup"])
    keys = [check["key"] for check in json.loads(out)["data"]["checks"]]
    assert len(keys) == len(set(keys)), sorted(k for k in keys if keys.count(k) > 1)


def test_the_wizard_never_puts_a_credential_value_in_its_own_report(configured):
    """The report is written to standard output and read by other processes.

    Only the NAME of a credential ever appears in it. A value that reached the
    envelope would be in every log and every job record that captured the run.
    """
    wizard = setup_verb._Wizard({}, Scripted(["yes", "yes", "yes"], ["s3cret", "k3y", "s1gn"]))
    setup_verb._capture_credentials(wizard, configured)
    rendered = json.dumps([note.to_json() for note in wizard.notes])
    for value in ("s3cret", "k3y", "s1gn"):
        assert value not in rendered


def test_the_wizard_refuses_to_overwrite_a_configuration_it_cannot_understand(
    tmp_path, monkeypatch
):
    """The reader that cannot tell a wrong document from an empty one, refused.

    Treating an unreadable config as an absent one and writing a fresh document
    over it destroys every answer the user gave. Only a genuinely MISSING file
    starts from empty.
    """
    directory = tmp_path / "cfg"
    directory.mkdir()
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(directory))
    path = directory / config.CONFIG_FILENAME
    path.write_text("this is not toml = = =\n")
    config.reset_cache()

    with pytest.raises(CratekitError) as excinfo:
        setup_verb.existing_document()
    assert excinfo.value.cause.remediation.remedy is Remedy.REPAIR_CONFIG_FILE
    assert path.read_text() == "this is not toml = = =\n", "the original was rewritten"


def test_the_wizard_completes_an_incomplete_configuration_rather_than_refusing(
    tmp_path, monkeypatch
):
    """The one unusable state setup is FOR. A config missing a required key parses
    fine and fails validation, and answering the missing key is the whole job.
    """
    directory = tmp_path / "cfg"
    directory.mkdir()
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(directory))
    (directory / config.CONFIG_FILENAME).write_text(
        f'schema_version = {config.CURRENT_SCHEMA_VERSION}\n'
        f'[library]\nroot = "{tmp_path / "kept"}"\n'
    )
    config.reset_cache()

    document, provenance = setup_verb.existing_document()
    assert provenance == "incomplete"
    assert document["library"]["root"] == str(tmp_path / "kept")


def test_the_wizard_never_re_derives_a_volume_identity_it_already_recorded(configured):
    """R38's clone protection, arriving through the thing meant to provide it.

    A wizard that re-read the identity on every run would record whatever disk
    happened to be mounted, so a restored clone would be adopted as the library by
    the act of running setup again.
    """
    wizard = setup_verb._Wizard(dict(configured.to_toml_dict()), silent())
    kept = setup_verb._resolve_volume_id(
        wizard, str(configured.library.root), None, probes()
    )
    assert kept == VOLUME

    overridden = setup_verb._resolve_volume_id(
        wizard, str(configured.library.root), "1111-2222", probes()
    )
    assert overridden == "1111-2222", "an explicit answer is the only thing that replaces it"


def test_the_wizard_proposes_the_installed_pin_and_records_it_only_on_a_yes(
    configured, monkeypatch
):
    """S2 as behaviour. A pin the software copies from whatever is installed
    refuses nothing, forever, which is the entire property the pin provides.
    """
    monkeypatch.setattr(
        setup_verb.rb_writer, "read_installed_app_version", lambda **_k: "9.9.9"
    )
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
    # Never written here: it means "confirmed against a real write", and this verb
    # has not made one.
    assert "validated_on" not in document["rekordbox"]


def _no_backup_flags():
    from types import SimpleNamespace

    return SimpleNamespace(
        backup_dest=None, backup_archive_root=None, backup_db_dest_root=None, backup_remote=None
    )


def test_the_wizard_asks_for_the_backup_destinations_when_the_module_is_on(configured):
    """The brief's fourth scenario (R-345). ``BackupConfig`` said every field was
    wizard supplied and the wizard never asked, so the values were typed by hand
    and the first dry run ran against bare folder names. On a full profile with
    nothing recorded the set is offered, a yes asks all three, and the remote is
    derived from the answers rather than asked a fourth time.
    """
    document = dict(configured.to_toml_dict())
    assert "backup" not in document
    wizard = setup_verb._Wizard(
        document, Scripted(["yes", "gdrive:mirror", "gdrive:archive", "gdrive:db"])
    )
    setup_verb._resolve_backup(wizard, document, _no_backup_flags(), probes())
    assert document["backup"] == {
        "dest": "gdrive:mirror",
        "archive_root": "gdrive:archive",
        "db_dest_root": "gdrive:db",
        "remote": "gdrive",
    }
    assert [line for line in wizard.asked if line.startswith("backup.")] == [
        "backup.dest (answered)",
        "backup.archive_root (answered)",
        "backup.db_dest_root (answered)",
    ]
    assert config.validate(document) == []


def test_the_wizard_records_nothing_for_backup_when_the_offer_goes_unanswered(configured):
    """Offered the way the pin is offered, so a scripted run on a full profile
    stays a run that asks nothing and refuses nothing. The note says what was
    not recorded and names the flags, and doctor reports the unset remote.
    """
    document = dict(configured.to_toml_dict())
    wizard = setup_verb._Wizard(document, silent())
    setup_verb._resolve_backup(wizard, document, _no_backup_flags(), probes())
    assert "backup" not in document
    assert wizard.asked == []
    note = next(n for n in wizard.notes if n.key == "setup.backup")
    assert note.status is doctor.Status.INFO
    assert "backup.dest" in note.detail and "not recorded" in note.detail
    assert "--backup-dest" in note.detail


def test_the_wizard_asks_nothing_about_backup_when_the_module_is_off(configured):
    """Slim has no backup module, so there is no destination to ask for."""
    document = dict(configured.to_toml_dict())
    document["profile"] = {"name": "slim"}
    written: list[str] = []
    wizard = setup_verb._Wizard(
        document,
        prompt.Prompter(read_line=lambda: "yes\n", read_secret=lambda _q: "", write=written.append),
    )
    setup_verb._resolve_backup(wizard, document, _no_backup_flags(), probes())
    assert written == []
    assert "backup" not in document
    note = next(n for n in wizard.notes if n.key == "setup.backup")
    assert "off in this profile" in note.detail


def test_backup_flags_are_recorded_even_when_the_module_is_off(configured):
    """A flag is an answer whatever the profile says. Refusing it would send a
    person to switch the module on and come back, and validation judges the
    shape either way."""
    from types import SimpleNamespace

    document = dict(configured.to_toml_dict())
    document["profile"] = {"name": "slim"}
    wizard = setup_verb._Wizard(document, silent())
    setup_verb._resolve_backup(
        wizard,
        document,
        SimpleNamespace(
            backup_dest="gdrive:mirror",
            backup_archive_root="gdrive:archive",
            backup_db_dest_root="gdrive:db",
            backup_remote=None,
        ),
        probes(),
    )
    assert document["backup"] == {
        "dest": "gdrive:mirror",
        "archive_root": "gdrive:archive",
        "db_dest_root": "gdrive:db",
        "remote": "gdrive",
    }
    assert len([line for line in wizard.asked if "command line" in line]) == 3
    assert any("off in this profile" in n.detail for n in wizard.notes if n.key == "setup.backup")


def test_a_declined_offer_still_records_the_flags_that_were_given(configured):
    """Partial flags on a full profile: the two given land, the offer is about
    the one still missing, a no leaves that one unset, and the remote is
    derived from what did land."""
    from types import SimpleNamespace

    document = dict(configured.to_toml_dict())
    wizard = setup_verb._Wizard(document, Scripted(["no"]))
    setup_verb._resolve_backup(
        wizard,
        document,
        SimpleNamespace(
            backup_dest="gdrive:mirror",
            backup_archive_root="gdrive:archive",
            backup_db_dest_root=None,
            backup_remote=None,
        ),
        probes(),
    )
    assert document["backup"] == {
        "dest": "gdrive:mirror",
        "archive_root": "gdrive:archive",
        "remote": "gdrive",
    }
    note = next(n for n in wizard.notes if n.key == "setup.backup")
    assert "backup.db_dest_root not recorded" in note.detail
    assert "backup.dest" not in note.detail.split(" not recorded")[0]


def test_a_mistyped_module_name_is_still_a_named_problem_not_a_traceback(
    configured, monkeypatch
):
    """The wizard reads membership off the document before validate runs, and
    ``profiles.resolve`` raises on a module it does not know. A hand edit such
    as ``bakcup = true`` has to stay validate's to report as a named problem
    under config-unusable, the way it was before the wizard asked about backup,
    rather than escape as an internal error the dispatcher files as a defect."""
    seed_taxonomy(configured)
    monkeypatch.setattr(doctor, "Probes", lambda: probes())
    path = config.config_path()
    path.write_text(path.read_text() + "\n[modules]\nbakcup = true\n")
    config.reset_cache()

    code, out, err = drive(["--output", "json", "setup"])

    envelope = json.loads(out)
    assert envelope["cause"]["reason"] == "config-unusable", envelope["cause"]
    problems = envelope["cause"]["detail"]["problems"]
    assert any("modules.bakcup is not a known module" in p for p in problems), problems


def test_the_wizard_keeps_recorded_backup_destinations_without_asking(configured):
    """A re-run changes nothing it was not asked to change: three recorded
    destinations and a spelled remote reach no prompt and are left as spelled."""
    document = dict(configured.to_toml_dict())
    document["backup"] = {
        "remote": "gdrive:",
        "dest": "gdrive:mirror",
        "archive_root": "gdrive:archive",
        "db_dest_root": "gdrive:db",
    }
    before = json.loads(json.dumps(document))
    written: list[str] = []
    wizard = setup_verb._Wizard(
        document,
        prompt.Prompter(read_line=lambda: "yes\n", read_secret=lambda _q: "", write=written.append),
    )
    setup_verb._resolve_backup(wizard, document, _no_backup_flags(), probes())
    assert written == []
    assert wizard.asked == []
    assert document == before


def test_the_backup_flags_are_recorded_without_a_question(configured, monkeypatch):
    """Every answer is also a flag, through the real dispatcher: the three
    destinations land in the file, the remote is derived into it, and nothing
    was prompted."""
    seed_taxonomy(configured)
    # The closing doctor looks the derived remote up in rclone's configuration,
    # so the green machine knows one by that name.
    monkeypatch.setattr(
        doctor,
        "Probes",
        lambda: probes(rclone_remotes=lambda _rclone: {"gdrive": {"type": "sftp"}}),
    )

    code, out, err = drive(
        [
            "--output", "json", "setup",
            "--backup-dest", "gdrive:mirror",
            "--backup-archive-root", "gdrive:archive",
            "--backup-db-dest-root", "gdrive:db",
        ]
    )
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
    configured, monkeypatch, how
):
    """The producer of R-345 through the wizard, both ways in. The answer goes
    through the same ``validate`` call as every other answer, so a bare folder
    name is refused with the key named rather than written and handed to rclone
    as a local path on the next backup."""
    seed_taxonomy(configured)
    monkeypatch.setattr(doctor, "Probes", lambda: probes())
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
    document["backup"] = {
        "remote": spelled,
        "dest": "gdrive:mirror",
        "archive_root": "gdrive:archive",
        "db_dest_root": "gdrive:db",
    }
    return document


def test_a_spelled_remote_rclone_lacks_is_replaced_by_the_destinations_remote(configured):
    """R-662's producer at the wizard: the file spells a remote nothing can write
    to and the destinations agree on another. rclone's configuration was READ
    and lacks the spelled name, so a re-run repairs it and says so."""
    document = _spelled_remote_document(configured)
    wizard = setup_verb._Wizard(document, silent())
    setup_verb._resolve_backup(
        wizard,
        document,
        _no_backup_flags(),
        probes(rclone_remotes=lambda _rclone: {"gdrive": {"type": "sftp"}}),
    )
    assert document["backup"]["remote"] == "gdrive"
    note = next(n for n in wizard.notes if n.key == "setup.backup.remote")
    assert "'remote'" in note.detail and "replaced with 'gdrive'" in note.detail
    assert config.validate(document) == []


@pytest.mark.parametrize(
    "machine",
    [
        pytest.param(
            {"rclone_remotes": lambda _r: {"remote": {}, "gdrive": {}}}, id="rclone-knows-it"
        ),
        pytest.param({"rclone_remotes": lambda _r: None}, id="rclone-unreadable"),
        # An empty dump lacks every name, so the destinations may be the typo.
        pytest.param({"rclone_remotes": lambda _r: {}}, id="rclone-knows-neither"),
        pytest.param({"find_binary": lambda _name: None}, id="rclone-absent"),
    ],
)
def test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it(configured, machine):
    """R-345's rule stands where rclone knows the spelled remote, and where
    rclone could not be asked, since a machine that could not say is not one
    that said no. Nothing is replaced and validation still refuses."""
    document = _spelled_remote_document(configured)
    wizard = setup_verb._Wizard(document, silent())
    setup_verb._resolve_backup(wizard, document, _no_backup_flags(), probes(**machine))
    assert document["backup"]["remote"] == "remote"
    assert not any(n.key == "setup.backup.remote" for n in wizard.notes)
    problems = config.validate(document)
    assert len(problems) == 1 and "backup.remote names 'remote'" in problems[0], problems


def test_no_disagreement_is_read_where_there_is_nothing_to_compare(configured):
    """A blank spelled remote is unset, and destinations naming several remotes
    give no one name to compare against. Neither is a disagreement, so neither
    reaches the repair or adds a second problem naming an arbitrary remote
    beside the several-remotes one validation already reports."""
    blank = _spelled_remote_document(configured, spelled="  ")
    assert config.backup_remote_disagreement(blank) is None

    several = _spelled_remote_document(configured)
    several["backup"]["archive_root"] = "dropbox:archive"
    assert config.backup_remote_disagreement(several) is None
    problems = config.validate(several)
    assert len(problems) == 1 and "name several" in problems[0], problems


def test_the_backup_remote_flag_replaces_a_spelled_remote_rclone_knows(configured):
    """The explicit answer: a flag replaces the recorded value whatever rclone
    says, which is the repair the refusal's fix line now names."""
    from types import SimpleNamespace

    document = _spelled_remote_document(configured)
    wizard = setup_verb._Wizard(document, silent())
    setup_verb._resolve_backup(
        wizard,
        document,
        SimpleNamespace(
            backup_dest=None,
            backup_archive_root=None,
            backup_db_dest_root=None,
            backup_remote="gdrive",
        ),
        probes(rclone_remotes=lambda _r: {"remote": {}, "gdrive": {}}),
    )
    assert document["backup"]["remote"] == "gdrive"
    assert "backup.remote (from the command line)" in wizard.asked
    assert config.validate(document) == []


def _spell_the_backup_remote(name: str) -> None:
    path = config.config_path()
    path.write_text(path.read_text() + f'\n[backup]\nremote = "{name}"\n')
    config.reset_cache()


_GDRIVE_DESTINATIONS = [
    "--backup-dest", "gdrive:mirror",
    "--backup-archive-root", "gdrive:archive",
    "--backup-db-dest-root", "gdrive:db",
]


def test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it(
    configured, monkeypatch
):
    """Sitting 5 through the real dispatcher. The file spells ``remote``, rclone
    knows a remote by that name so nothing is guessed, and the destinations on
    the command line name ``gdrive``. The refusal's fix line used to be
    ``crate setup``, the command that had just refused; it names the flag now,
    and running what it names writes the file."""
    seed_taxonomy(configured)
    _spell_the_backup_remote("remote")
    monkeypatch.setattr(
        doctor,
        "Probes",
        lambda: probes(
            rclone_remotes=lambda _r: {"remote": {"type": "sftp"}, "gdrive": {"type": "sftp"}}
        ),
    )

    code, _out, err = drive(["setup", *_GDRIVE_DESTINATIONS])

    assert code != int(ExitCode.OK), err
    assert "config-unusable" in err
    assert "fix: re-run crate setup with --backup-remote gdrive" in err, err
    assert "fix: crate setup\n" not in err
    assert "Setup's --backup-remote replaces the spelled one" in err

    code, out, err = drive(["--output", "json", "setup", "--backup-remote", "gdrive"])

    assert code == int(ExitCode.OK), err
    assert "backup.remote (from the command line)" in json.loads(out)["data"]["summary"][
        "answered"
    ]
    config.reset_cache()
    assert config.load().backup.remote == "gdrive"
    assert tomllib.loads(config.config_path().read_text())["backup"]["remote"] == "gdrive"


def test_the_setup_token_stays_when_the_disagreement_is_not_the_only_problem(configured):
    """Beside other problems the fix is still more answers, so the run-setup
    token is kept and the flag leads the steps rather than replacing them."""
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
    """The other half of R-662 end to end: the spelled name is not among
    rclone's, so the destinations given on the command line settle it with no
    fourth flag and no hand move of the file."""
    seed_taxonomy(configured)
    _spell_the_backup_remote("remote")
    monkeypatch.setattr(
        doctor,
        "Probes",
        lambda: probes(rclone_remotes=lambda _r: {"gdrive": {"type": "sftp"}}),
    )

    code, out, err = drive(["--output", "json", "setup", *_GDRIVE_DESTINATIONS])

    assert code == int(ExitCode.OK), err
    checks = json.loads(out)["data"]["checks"]
    assert any(c["key"] == "setup.backup.remote" for c in checks), checks
    config.reset_cache()
    assert config.load().backup.remote == "gdrive"


def test_the_wizard_refuses_a_required_answer_it_cannot_obtain(tmp_path, monkeypatch):
    """A value nobody supplied and nothing could derive is a refusal naming the
    key, never a guess written into a configuration file.
    """
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "cfg"))
    config.reset_cache()
    wizard = setup_verb._Wizard({}, silent())
    with pytest.raises(CratekitError) as excinfo:
        wizard.resolve("library.root", flag=None, question="Where is the library")
    assert excinfo.value.cause.remediation.remedy is Remedy.RUN_SETUP
    assert "library.root" in excinfo.value.cause.message


def test_a_derived_default_is_taken_when_nothing_can_be_asked(tmp_path):
    wizard = setup_verb._Wizard({}, silent())
    answer = wizard.resolve(
        "paths.download_staging",
        flag=None,
        question="Where",
        default=str(tmp_path / "staging"),
    )
    assert answer == str(tmp_path / "staging")
    assert any("nothing could be asked" in line for line in wizard.asked)


def test_a_closed_question_refuses_a_default_outside_its_own_option_set():
    """A default a user cannot accept by pressing return is not a default."""
    wizard = setup_verb._Wizard({}, silent())
    with pytest.raises(ValueError, match="not one of them"):
        wizard.resolve(
            "profile.name",
            flag=None,
            question="Which preset",
            default="enormous",
            choices=profiles.PROFILE_NAMES,
        )


def test_the_active_taxonomy_is_copied_once_and_never_overwritten(configured):
    """S6. The library's own copy is what makes it self-describing, and a second
    run must not replace a template the user edited.
    """
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, configured, probes())
    path = config.state_path("taxonomy_active", configured)
    assert path.is_file()

    path.write_text("# edited by hand\n" + path.read_text())
    setup_verb._seed_taxonomy(wizard, configured, probes())
    assert path.read_text().startswith("# edited by hand")


def test_the_wizard_offers_every_credential_the_profile_needs_and_records_it(configured):
    """What is offered is the same registry question doctor asks, so a module
    switched on above is a credential offered here with no edit.
    """
    values = ["one", "two", "three"]
    wizard = setup_verb._Wizard({}, Scripted(["yes", "yes", "yes"], values))
    setup_verb._capture_credentials(wizard, configured)

    assert secrets.exists(str(secrets.Credential.PROVIDER_SESSION))
    assert secrets.exists(str(secrets.Credential.IDENTIFY_KEY))
    assert all(note.status is doctor.Status.OK for note in wizard.notes)


def test_an_unanswered_credential_offer_leaves_it_outstanding_rather_than_empty(
    configured,
):
    """Nobody answered and no is the same consequence, which is exactly why these
    are the questions allowed to go unanswered.
    """
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._capture_credentials(wizard, configured)
    assert not secrets.recorded()
    assert all(note.status is doctor.Status.INFO for note in wizard.notes)


def test_only_the_wizard_and_the_label_sync_are_interactive_and_neither_reads_stdin():
    """The exemption is one FILE, and neither interactive verb is it.

    The registry marks setup and label.sync interactive; the static allowlist
    names ``cli/prompt.py``. Those are two different things on purpose, and
    asserting both here is what stops the second one drifting into "the setup
    module may prompt", which would put a read of standard input in a module
    the wizard's own helpers keep growing. U107's verb is held to the same
    rule in ``tests/test_label_sync.py``.
    """
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
                else [node.module or ""]
            )
            assert all(name.split(".")[0] != "getpass" for name in names)


# ═══════════════════════════════════════════════════════════════════════════
# 5. crate login
# ═══════════════════════════════════════════════════════════════════════════


def test_a_credential_offer_accepted_and_left_empty_is_the_same_note_as_a_no(configured):
    """R-347. The provider session is a blob only login produces, so a person who
    says yes and then has nothing to type has told the wizard the same fact as a
    no, and it used to fail the whole run.
    """
    wizard = setup_verb._Wizard({}, Scripted(["yes", "yes", "yes"], ["", "  ", ""]))
    setup_verb._capture_credentials(wizard, configured)

    offered = [note for note in wizard.notes if note.key.startswith("setup.credential.")]
    assert offered, "no credential was offered, so nothing here was exercised"
    assert all(note.status is doctor.Status.INFO for note in offered)
    assert not secrets.recorded()


def test_a_credential_offer_that_could_not_be_read_still_fails(configured):
    """The other half. An empty answer is a person; a dead stream is not."""
    wizard = setup_verb._Wizard({}, Scripted(["yes", "yes", "yes"]))
    setup_verb._capture_credentials(wizard, configured)

    offered = [note for note in wizard.notes if note.key.startswith("setup.credential.")]
    assert offered
    assert all(note.status is doctor.Status.FAIL for note in offered)


def test_an_empty_credential_leaves_the_exit_code_to_doctor(tmp_path, monkeypatch):
    """R-347 end to end. With the offer accepted and left empty, the only failing
    check is the one doctor itself reports on a clean machine, the unset pin.
    """
    root = tmp_path / "fresh"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setattr(doctor, "Probes", lambda: probes())
    scripted = Scripted(["no", "yes", "yes", "yes"], ["", "", ""])
    monkeypatch.setattr(setup_verb.prompt, "Prompter", lambda: scripted)

    code, out, err = drive(
        [
            "--output", "json", "setup",
            "--library-root", str(root),
            "--db-path", str(root / "db" / "master.db"),
            "--volume-id", VOLUME,
            "--staging", str(tmp_path / "staging"),
            "--profile", "slim",
            "--taxonomy", "default",
        ]
    )
    checks = json.loads(out)["data"]["checks"]
    credential = [c for c in checks if c["key"].startswith("setup.credential.")]
    assert credential and all(c["status"] == "info" for c in credential), (checks, err)
    failing = [c["key"] for c in checks if c["status"] == "fail"]
    assert failing == ["rekordbox.pins"], (checks, err)
    assert code == int(ExitCode.PRECONDITION)


def test_an_identity_typed_as_diskutil_prints_it_passes_the_mount_check(library):
    """R-344 through setup. The uppercase UUID is recorded as given, the platform
    reports it lowercase, and the taxonomy the sitting could not write is written.
    """
    reported = "0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"
    wizard = setup_verb._Wizard({}, silent())
    recorded = setup_verb._resolve_volume_id(wizard, str(library), reported.upper(), probes())
    cfg = config.from_dict(document_for(library, volume_id=recorded))
    machine = probes(identity_provider=lambda _path: reported)

    status = setup_verb.preflight.resolve_mount_state(
        cfg.library.root,
        cfg.library.volume_id,
        identity_provider=machine.identity_provider,
        mount_enumerator=machine.mount_enumerator,
    )
    assert status.state is setup_verb.preflight.MountState.OK

    setup_verb._seed_taxonomy(wizard, cfg, machine)
    assert not [note for note in wizard.notes if note.status is doctor.Status.FAIL]
    assert config.state_path("taxonomy_active", cfg).is_file()


def test_a_question_reaches_a_real_pipe_before_its_answer_is_read():
    """R-346. Every other test injects the writer, which is why none could see it.

    A real interpreter, real pipes, and no ``PYTHONUNBUFFERED``: the question must
    arrive on standard error while the child is still blocked waiting for the
    answer. Unflushed, it sat in the buffer and a terminal showed nothing.
    """
    import select
    import subprocess
    import time

    environment = {k: v for k, v in os.environ.items() if k != "PYTHONUNBUFFERED"}
    script = (
        "import sys\n"
        "from cratekit.cli import prompt\n"
        "sys.stdout.write(prompt.Prompter().ask('Which crate'))\n"
    )
    child = subprocess.Popen(
        [sys.executable, "-c", script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment,
    )
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
    """An argument is visible in the process listing to every local account for
    as long as the process runs, and in the shell history afterwards.
    """
    import argparse

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
    holder = tmp_path / "token.txt"
    holder.write_text("  a-real-looking-token\n")

    code, out, err = drive(
        ["--output", "json", "login", "provider-session", "--from-file", str(holder)]
    )
    assert code == int(ExitCode.OK), err
    assert secrets.get("provider-session") == "a-real-looking-token"
    assert json.loads(out)["data"]["summary"]["credential"] == "provider-session"


def test_login_refuses_a_file_holding_nothing(configured, tmp_path):
    """An empty credential reads back as absent on some backends and as present on
    others, so storing one makes the presence question unanswerable and doctor
    starts giving an answer it cannot support.
    """
    holder = tmp_path / "empty.txt"
    holder.write_text("   \n")
    code, out, _ = drive(
        ["--output", "json", "login", "provider-session", "--from-file", str(holder)]
    )
    assert code == int(ExitCode.PRECONDITION)
    assert not secrets.recorded()


def test_login_reads_the_environment_fallback_through_the_store_that_owns_it(
    configured, monkeypatch
):
    """One rule about when the environment may supply a credential, in one place.

    A second reader here would be a second rule, and the fallback would be on for
    one caller and off for another with nothing in the configuration to explain it.
    """
    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    monkeypatch.setenv(secrets.ENV_CREDENTIAL_PREFIX + "IDENTIFY_KEY", "from-the-environment")
    code, _, err = drive(["login", "identify-key"])
    assert code == int(ExitCode.OK), err

    monkeypatch.delenv(secrets.ENV_ALLOW_ENV_CREDENTIALS)
    assert secrets.environment_value("identify-key") is None


# ═══════════════════════════════════════════════════════════════════════════
# 6. The reports, and the rendering
# ═══════════════════════════════════════════════════════════════════════════


def test_doctor_exits_with_a_precondition_status_and_keeps_its_report(configured, monkeypatch):
    """A doctor that fails by throwing its checks away is useless in exactly the
    case it exists for, which is why this verb builds its own envelope.
    """
    monkeypatch.setattr(doctor, "Probes", lambda: probes(keychain_available=lambda: False))
    code, out, err = drive(["--output", "json", "doctor"])
    envelope = json.loads(out)
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "doctor-check-failed"
    assert len(envelope["data"]["checks"]) == len(doctor.CHECK_KEYS)
    assert "keychain.reachable" in envelope["cause"]["detail"]["failing"]
    assert "keychain.reachable" in err, "the failure has to reach a person too"


def test_a_green_doctor_exits_zero(configured, monkeypatch):
    seed_taxonomy(configured)
    monkeypatch.setattr(doctor, "Probes", lambda: probes())
    code, out, err = drive(["--output", "json", "doctor"])
    assert code == int(ExitCode.OK), err
    assert json.loads(out)["outcome"] == str(Outcome.OK)


def test_status_reports_open_runs_sessions_and_trees(configured):
    from cratekit.cli import gates

    state = gates.new_run(registry.entry("profile.set"))
    state.open_gate = "profile.set.apply"
    gates.save(state)

    record = session.SessionRecord(
        session_id="s-2",
        workflow="sync.labels",
        started="2026-08-02T00:00:00+00:00",
        sources={"labels": str(session.SourceState.REFUSED)},
    )
    session.write_record(record, configured)

    code, out, err = drive(["--output", "json", "status"])
    assert code == int(ExitCode.OK), err
    data = json.loads(out)["data"]
    keys = {check["key"] for check in data["checks"]}
    assert f"run.{state.run_id}" in keys
    assert "source.labels" in keys
    assert data["summary"]["open_runs"] == 1


def test_status_names_a_session_log_it_cannot_list_and_still_reports_the_rest(
    configured, monkeypatch
):
    """R-1255, review round one: a log nobody could list is said, not read as no source.

    The status reports runs, sources and trees, and only the sources are in
    the log, so the log is one failing finding of its own and the report goes
    on; a source refused in it is not lost behind an empty read.
    """
    record = session.SessionRecord(
        session_id="s-2",
        workflow="sync.labels",
        started="2026-08-02T00:00:00+00:00",
        sources={"labels": str(session.SourceState.REFUSED)},
    )
    session.write_record(record, configured)
    log = Path(session.log_dir(configured))
    _refuse_listing(monkeypatch, log)

    code, out, err = drive(["--output", "json", "status"])

    assert code == int(ExitCode.OK), err
    checks = {check["key"]: check for check in json.loads(out)["data"]["checks"]}
    assert "source.labels" not in checks
    named = checks["source.session-log"]
    assert named["status"] == "fail"
    assert f"the session log directory {log} exists and cannot be listed" in named["detail"]


def test_the_human_rendering_shows_the_checks_rather_than_only_a_status(
    configured, monkeypatch
):
    """A doctor whose human output says only "failed" sends the reader to parse
    JSON to find out what failed.
    """
    monkeypatch.setattr(doctor, "Probes", lambda: probes(keychain_available=lambda: False))
    _code, _out, err = drive(["doctor"])
    assert "keychain.reachable" in err
    assert render.remedy_text(Remedy.INSTALL_KEYCHAIN_BACKEND) in err


def test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb(
    configured, monkeypatch
):
    """U97, closing R-411, and driven through the DEFAULT human output on purpose.

    The token was always right and the rendering was not, so a test that read
    the JSON envelope would compare a token to itself and pass over the wording
    a person actually reads. This one goes through the dispatcher the way the
    process does and asserts the check table's own ``fix:`` line.

    The bare verb is pinned NEGATIVELY as a whole line rather than as a
    substring, because the procedure that replaces it contains ``crate login``
    inside a longer command, and a substring check would forbid the fix.
    """
    monkeypatch.setattr(
        doctor,
        "Probes",
        lambda: probes(
            credential_recorded=lambda name: name != str(secrets.Credential.PROVIDER_SESSION)
        ),
    )
    _code, _out, err = drive(["doctor"])

    assert "credential.provider" in err
    assert "fix: crate login\n" not in err
    assert "crate login provider-session --from-file" in err
    assert "erase the plaintext file" in err
    assert "docs/adapters.md" in err


def test_the_cause_steps_are_not_printed_twice_beside_the_check_table():
    """The table already lists every failure with its own fix, so repeating the
    cause's steps above it prints one list twice.
    """
    report = doctor.Report(
        (
            doctor.Finding(
                key="binary.ffmpeg",
                title="external binary ffmpeg",
                status=doctor.Status.FAIL,
                detail="not found",
                remedy=Remedy.INSTALL_BINARY,
            ),
        )
    )
    from cratekit.cli import output

    envelope = output.build(
        verb="doctor",
        run_id="r",
        schema=output.current_schema("diagnostic"),
        started="2026-08-02T00:00:00+00:00",
        outcome=Outcome.FAILED,
        code=ExitCode.PRECONDITION,
        data=report.payload(),
        cause=doctor.failure_cause(report),
    )
    text = render.render(envelope)
    assert text.count("binary.ffmpeg") == 1
    assert "[FAIL]" in text


def test_a_check_table_is_rendered_only_for_the_diagnostic_surface():
    """Gated on the schema rather than on a ``checks`` key, so a later surface
    that happens to carry one is not rendered in a shape built for another.
    """
    from cratekit.cli import output

    plan = output.build(
        verb="profile.set",
        run_id="r",
        schema=output.current_schema("plan"),
        started="2026-08-02T00:00:00+00:00",
        data={"digest": "d", "items": [], "totals": {}, "chunk": None},
    )
    assert render.render_checks(plan) == []


# ═══════════════════════════════════════════════════════════════════════════
# 7. The prompt module, and the guard it is exempt from
# ═══════════════════════════════════════════════════════════════════════════


def test_a_prompt_that_cannot_be_answered_is_a_typed_refusal(monkeypatch):
    """Anything the reader raises becomes one type, so the wizard can treat a
    required answer differently from an optional one instead of dying with a
    traceback from whatever replaced the stream.
    """
    for boom in (EOFError("closed"), OSError("descriptor gone"), AssertionError("trapped")):

        def reader(exc=boom):
            raise exc

        asking = prompt.Prompter(read_line=reader, write=lambda _t: None)
        with pytest.raises(prompt.PromptUnavailable):
            asking.ask("anything")


def test_a_prompt_never_writes_to_standard_output(capsys):
    """R32: standard output carries exactly one JSON envelope and nothing else.

    A question printed there would sit in front of that object and the failure
    would look like a schema problem rather than like a prompt.
    """
    asking = prompt.Prompter(read_line=lambda: "yes\n")
    assert asking.confirm("proceed") is True
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "proceed" in captured.err


def test_an_answer_outside_a_closed_set_is_re_asked_and_then_abandoned():
    queued = ["nonsense", "rubbish", "drivel"]
    asking = prompt.Prompter(
        read_line=lambda: queued.pop(0) + "\n", write=lambda _t: None
    )
    with pytest.raises(prompt.PromptUnavailable):
        asking.choose("which", ["a", "b"], default="a")
    assert queued == [], "the bounded retry is what stops a pipe spinning forever"


def test_no_mapping_in_this_unit_has_a_key_written_twice():
    """The shape this repository has already shipped once with a green suite.

    Every other test over a mapping iterates the RUNTIME object and is blind to an
    entry collapsed at parse time: two branches append two rows, one key is
    written twice, and the later value silently wins. The only check that can see
    it counts the elements in the LITERAL and compares them against the runtime
    length, so this walks the syntax tree of every module this unit ships.
    """
    for name in ("doctor.py", "setup.py", "prompt.py", "render.py"):
        source = (SRC_ROOT / "cratekit" / "cli" / name).read_text()
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
    """Driven over EVERY mount outcome, because the shape that got this wrong was
    a chain of branches with a fall-through at the end.

    ``resolve_mount_state`` fills in ``observed_identity`` for an unmounted volume
    and for one mounted elsewhere alike, since it observed SOMETHING at the
    configured path in both cases. A final "and otherwise it matched" therefore
    reported a green identity beside a red mount for a volume sitting on another
    mount point, and for one that is not attached at all. Only two outcomes mean
    the identities were equal, and this asserts exactly those two.
    """
    from cratekit.core import preflight

    matched = {preflight.MountState.OK, preflight.MountState.LIBRARY_PATH_MISSING}
    for state in preflight.MountState:
        verdict, remedy = doctor._IDENTITY_VERDICT[state]
        assert (verdict is doctor.Status.OK) == (state in matched), state
        assert (remedy is None) == (verdict is not doctor.Status.FAIL), state


def test_a_volume_mounted_elsewhere_is_one_problem_reported_once(tmp_path, monkeypatch):
    """The mount is wrong and the identity is fine, so exactly one of the two
    findings carries a fix. Reporting it twice attaches the wrong remedy to one
    of the copies, which is how a user ends up unplugging a healthy drive.
    """
    root = tmp_path / "configured"
    (root / "Music").mkdir(parents=True)
    elsewhere = tmp_path / "actually-here"
    elsewhere.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))

    report = doctor.run(
        config.from_dict(document_for(root)),
        probes=probes(
            identity_provider=lambda path: VOLUME if path == elsewhere else "0000-0000",
            mount_enumerator=lambda: (elsewhere,),
        ),
    )
    assert find(report, "library.mounted").status is doctor.Status.FAIL
    identity = find(report, "library.identity")
    assert identity.status is doctor.Status.INFO
    assert identity.remedy is None
    assert VOLUME in identity.detail


def test_an_unmounted_volume_never_reports_a_matching_identity(tmp_path, monkeypatch):
    absent = tmp_path / "not-mounted"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(absent))
    report = doctor.run(
        config.from_dict(document_for(absent)),
        probes=probes(identity_provider=lambda _p: "0000-0000", mount_enumerator=lambda: ()),
    )
    identity = find(report, "library.identity")
    assert identity.status is not doctor.Status.OK
    assert "matches" not in identity.detail


def test_every_mount_outcome_has_a_sentence_of_its_own():
    """A mapping over a closed enum has to be total, or one state renders as a
    ``KeyError`` in the middle of the report that was supposed to explain it.
    """
    from cratekit.core import preflight

    assert set(doctor._MOUNT_DETAIL) == set(preflight.MountState)
    assert len({str(v) for v in doctor._MOUNT_DETAIL.values()}) == len(preflight.MountState)


def test_a_seam_default_is_a_plain_function_and_never_a_bound_method():
    """The landmine under a dataclass whose fields hold callables.

    ``slots=True`` deletes the class attribute, so a function default stays a
    plain function and is called with the arguments it declares. Drop ``slots``
    and every one of them becomes a descriptor: the first argument silently
    becomes the instance, ``installed_app_version(cfg)`` passes the Probes object
    where the config belongs, and no test that injects its own seam would ever
    see it.
    """
    import types

    # The two seams the review added answer through the module that owns the
    # rule, rather than through a copy of it here. Asserted by identity, because
    # a second reader of the same environment variables is a second rule that
    # will eventually disagree with the first.
    assert RealProbes().environment_credential is secrets.environment_value
    assert RealProbes().binary_override_problem is binaries.override_problem

    for holder in (RealProbes(), prompt.Prompter()):
        for field_name in holder.__dataclass_fields__:
            value = getattr(holder, field_name)
            assert not isinstance(value, types.MethodType), (
                f"{type(holder).__name__}.{field_name} arrived bound to its own "
                f"instance, so its first argument is now the holder"
            )


def test_the_interactive_allowlist_still_holds_exactly_one_file():
    """The size of the hole, asserted from this unit's side as well.

    ``tests/test_cli_contract.py`` owns the allowlist. This unit is the one that
    filled it, so it is the one that would notice a second file being added to
    make some later wizard helper convenient.
    """
    from tests.test_cli_contract import INTERACTIVE_ALLOWLIST

    assert INTERACTIVE_ALLOWLIST == frozenset({"cratekit/cli/prompt.py"})
    assert (SRC_ROOT / "cratekit" / "cli" / "prompt.py").is_file()


# ═══════════════════════════════════════════════════════════════════════════
# 8. What the review found: a positive claim reached by falling through
# ═══════════════════════════════════════════════════════════════════════════
#
# Every defect in this section has one shape. Something reported OK by arriving
# at the end of a function rather than by observing the thing it claims, and each
# one is asserted here against the machine that produced the false green as well
# as against the machine where the answer really is yes.


class _Volumes:
    """A synthetic directory this platform mounts volumes into, and what is IN it.

    Two facts rather than one, and the second is the correction. The table alone
    says where a volume WOULD appear; on its own it cannot tell a mount point
    with a volume in it from the empty directory an ejected volume leaves behind,
    and those are the two states the derive has to answer differently. So the
    fixture carries the mount table and the mount seam together, and a test says
    which of the two it is building by calling ``attach`` or ``eject``.

    ``__truediv__`` so a test still spells a path under it the obvious way.
    """

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
        """The LEFTOVER: the directory is there and nothing is mounted in it.

        The first of the three broken states ``core/preflight``'s opening
        paragraphs name, and the one a rule about missing directories cannot see.
        """
        mount = (self.path / name).resolve()
        mount.mkdir(parents=True, exist_ok=True)
        self.mounted.discard(mount)
        return mount


@pytest.fixture
def volumes_directory(tmp_path, monkeypatch):
    """A synthetic directory that this platform mounts volumes into.

    ``preflight`` declares those per platform, the way it declares identity
    providers, because whether a volume will appear at a path is not something
    the filesystem can be asked. Injecting the table and the mount seam is what
    lets the suite drive every answer on any platform without touching the real
    one, and without needing to mount anything.

    RESOLVED, because the paths it is compared against are resolved. An
    unresolved row silently matched nothing on a machine whose temporary
    directory is reached through a symlink, which turned the whole guard into a
    no-op with no symptom.
    """
    from cratekit.core import preflight

    volumes = (tmp_path / "Volumes").resolve()
    volumes.mkdir()
    synthetic = _Volumes(volumes)
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((volumes, 1),))
    monkeypatch.setattr(
        preflight, "is_mount_point", lambda path: Path(path).resolve() in synthetic.mounted
    )
    return synthetic


def test_the_wizard_will_not_read_an_identity_from_a_volume_that_is_not_there(
    volumes_directory,
):
    """BLOCKING. The reproduction: derive with the drive unplugged.

    ``containing_mount`` climbs to the deepest EXISTING ancestor, so an absent
    library root does not fail the read, it succeeds against the boot disk. That
    identity was then recorded as the library's, and doctor reported four greens
    over it: mounted, identity, taxonomy and containment, all true of the boot
    disk. Every destructive verb's identity precondition passes there too, which
    is R38 pointed at the wrong disk.
    """
    absent = volumes_directory / "not-attached"
    boot = "BOOT-DISK-IDENTITY"
    wizard = setup_verb._Wizard({}, silent())

    with pytest.raises(CratekitError) as excinfo:
        setup_verb._resolve_volume_id(
            wizard, str(absent), None, probes(identity_provider=lambda _p: boot)
        )

    assert excinfo.value.cause.remediation.remedy is Remedy.MOUNT_LIBRARY_VOLUME
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert boot not in str(excinfo.value.cause.message), "the wrong identity was still read"
    assert "--volume-id" in excinfo.value.cause.message


def test_an_identity_is_derived_when_the_root_really_is_on_the_volume(tmp_path):
    """The other half. A guard that also refuses the correct case is not shipped."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    wizard = setup_verb._Wizard({}, silent())

    derived = setup_verb._resolve_volume_id(
        wizard, str(root), None, probes(identity_provider=lambda _p: VOLUME)
    )
    assert derived == VOLUME
    assert any("read from the mounted volume" in line for line in wizard.asked)


def test_setup_refuses_end_to_end_rather_than_recording_the_boot_disk(
    tmp_path, monkeypatch, volumes_directory
):
    """The same reproduction through the real dispatcher, with nothing written.

    A refusal that still saved the document would be the defect with an error
    message attached: the next run would read the recorded identity back and keep
    it, because an identity already recorded is never re-derived.
    """
    absent = volumes_directory / "not-attached"
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(absent))
    monkeypatch.setattr(doctor, "Probes", lambda: probes(identity_provider=lambda _p: "BOOT"))

    code, _out, _err = drive(
        [
            "--output", "json", "setup",
            "--library-root", str(absent),
            "--db-path", str(absent / "db" / "master.db"),
            "--staging", str(tmp_path / "staging"),
            "--profile", "slim",
            "--taxonomy", "default",
        ]
    )
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE)
    with pytest.raises(config.ConfigMissing):
        config.reset_cache()
        config.load()


def test_setup_writes_nothing_beside_the_library_until_the_volume_is_asserted(
    tmp_path, monkeypatch
):
    """BLOCKING. The wizard wrote library state first and checked last.

    Two permanent costs, and neither is visible in the report the run printed. On
    macOS an occupied ``/Volumes/NAME`` sends the real volume to
    ``/Volumes/NAME 1`` on its next attach, so the directory this created IS the
    leftover mount point ``core/preflight`` names as the first of the three
    states it exists to tell apart. And the copied template is COUPLED state on a
    filesystem no snapshot of that library captures and no rollback reverts.
    """
    root = tmp_path / "Volumes" / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    # The recorded identity is supplied, so BLOCKING 1 is not in play: what is
    # under test is the write, against a disk that is not the recorded one.
    monkeypatch.setattr(doctor, "Probes", lambda: probes(identity_provider=lambda _p: "0000"))

    code, out, _err = drive(
        [
            "--output", "json", "setup",
            "--library-root", str(root),
            "--volume-id", VOLUME,
            "--db-path", str(root / "db" / "master.db"),
            "--staging", str(tmp_path / "staging"),
            "--profile", "slim",
            "--taxonomy", "default",
        ]
    )

    assert code == int(ExitCode.PRECONDITION)
    assert not (root / config.from_dict(document_for(root)).library.state_dirname).exists(), (
        "setup created its own state directory on a volume it had not asserted"
    )
    assert not config.state_path("taxonomy_active", config.load()).exists()
    checks = {c["key"]: c for c in json.loads(out)["data"]["checks"]}
    assert checks["setup.taxonomy"]["status"] == "fail"
    assert checks["setup.taxonomy"]["remedy"] == str(Remedy.MOUNT_LIBRARY_VOLUME)


def test_the_wizard_still_writes_on_a_platform_that_reports_no_volume_identity(
    configured,
):
    """The correct case on the platform the guard could most easily lock out.

    ``preflight.null_volume_identity`` is what every platform with no adapter
    resolves to and it answers None for every volume, so a guard demanding
    MountState.OK would refuse to write the active taxonomy on that platform
    forever, with nothing wrong. The configured root existing is the signal that
    is actually available there, and it is the one used.
    """
    from cratekit.core import preflight

    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(
        wizard, configured, probes(identity_provider=preflight.null_volume_identity)
    )
    assert config.state_path("taxonomy_active", configured).is_file()
    assert all(note.status is not doctor.Status.FAIL for note in wizard.notes)


def test_the_wizard_writes_the_active_template_once_the_volume_is_the_recorded_one(
    tmp_path, monkeypatch
):
    """The correct case still writes, or the guard is just a refusal to work."""
    root = tmp_path / "Volumes" / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setattr(doctor, "Probes", lambda: probes())

    drive(
        [
            "--output", "json", "setup",
            "--library-root", str(root),
            "--volume-id", VOLUME,
            "--db-path", str(root / "db" / "master.db"),
            "--staging", str(tmp_path / "staging"),
            "--profile", "slim",
            "--taxonomy", "default",
        ]
    )
    assert config.state_path("taxonomy_active", config.load()).is_file()


# ── session.unresolved: an empty scan is not an answer ───────────────────────


def test_an_unresolved_session_is_never_reported_clean_because_its_disk_is_gone(
    configured, tmp_path
):
    """BLOCKING. The library holds a condemning record and doctor said none.

    ``scan_log`` returns two empty tuples for a directory that does not exist and
    for one it cannot read, which is the same pair it returns for a library that
    has never opened a session. Turning that into "0 recorded sessions, none of
    them open" is a positive claim about a disk nobody looked at, and it is the
    exact shape the identity check was already fixed for.
    """
    record = session.SessionRecord(
        session_id="s-9",
        workflow="route.inbox",
        started="2026-08-02T00:00:00+00:00",
        state=session.SessionState.COMMITTED_UNVERIFIED,
    )
    session.write_record(record, configured)
    mounted = find(doctor.run(configured, probes=probes()), "session.unresolved")
    assert mounted.status is doctor.Status.FAIL
    assert mounted.remedy is Remedy.RESTORE_FROM_SNAPSHOT

    # THE VOLUME GOES AWAY, taking the log with it. The reproduction exactly: the
    # record still exists, on a disk that is no longer at the configured path, so
    # the scan finds no files and the old branch turned that into "0 recorded
    # sessions, none of them open" over a library that cannot be vouched for.
    configured.library.root.rename(tmp_path / "detached")
    for machine in (
        probes(),  # the identity still matches further up: the ROOT is missing
        probes(identity_provider=lambda _p: "0000-0000", mount_enumerator=lambda: ()),
    ):
        finding = find(doctor.run(configured, probes=machine), "session.unresolved")
        assert finding.status is not doctor.Status.OK, finding.detail
        assert "not asserted" in finding.detail
        assert "none of them open" not in finding.detail


def test_an_unreadable_session_log_directory_is_not_an_empty_one(configured):
    """The half no mount state can answer: the right disk, and no permission.

    BLOCKING, AND THE ASSERTIONS ARE THE FIX. This test passed with the handler
    in ``_log_directory_unreadable`` deleted, because the exception then reached
    ``answer``'s blanket rescue, whose detail interpolates the ``PermissionError``
    and whose message CONTAINS THE PATH, so "status is FAIL" and "the path is in
    the detail" were both satisfied by the rescue. A guard covered by another
    guard is a guard nothing covers, and round four found this exact shape ten
    lines up in the same function, fixed that one, and left this one.

    So the answer has to be THIS check's answer: the sentence it writes, and not
    the sentence the rescue writes.
    """
    log = session.log_dir(configured)
    log.mkdir(parents=True, exist_ok=True)
    (log / "s-1.json").write_text("{}")
    log.chmod(0o000)
    try:
        finding = find(doctor.run(configured, probes=probes()), "session.unresolved")
    finally:
        log.chmod(0o700)
    assert finding.status is doctor.Status.FAIL
    assert str(log) in finding.detail
    assert "did not complete" not in finding.detail, "the blanket rescue answered"
    assert "cannot be listed by this account" in finding.detail
    assert "An unreadable log is not an empty one" in finding.detail


def test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check(configured, monkeypatch):
    """R-1255: the test above on a container that runs as root, which no mode bars.

    The listing is refused for the one path, as an account the log is closed
    to is refused. The scan answers that log as the one unread entry too, so
    the check under it would still FAIL with "1 session record(s) cannot be
    read" if this probe answered nothing; the sentence is the probe's own.
    """
    log = Path(session.log_dir(configured))
    log.mkdir(parents=True, exist_ok=True)
    (log / "s-1.json").write_text("{}")
    _refuse_listing(monkeypatch, log)

    finding = find(doctor.run(configured, probes=probes()), "session.unresolved")

    assert finding.status is doctor.Status.FAIL
    assert (
        f"the session log directory {log} exists and cannot be listed by this account"
        in finding.detail
    )
    assert "session record(s) in the log cannot be read" not in finding.detail


def test_a_library_with_no_sessions_still_reports_a_clean_log(configured):
    """And the OK says what it established, rather than what it failed to find."""
    finding = find(doctor.run(configured, probes=probes()), "session.unresolved")
    assert finding.status is doctor.Status.OK
    assert "on the recorded library volume was read" in finding.detail
    assert "0 recorded session(s), none of them open" in finding.detail


#: What each mount outcome permits, WRITTEN OUT rather than derived from the
#: thing under test. Duplicating the tables is the entire point: a mutation to
#: either one has to be made in two places, and the second place is a test a
#: reviewer reads. The version of this that only asserted the SHAPE of the tables
#: survived setting MOUNTED_ELSEWHERE to yes in both of them, which says doctor
#: may read and the wizard may write library state at the configured root while
#: the recorded volume is attached somewhere else, and that is the leftover
#: mount-point hazard the module exists to prevent.
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
    [("_STATE_READABLE", EXPECTED_READABLE), ("_STATE_WRITABLE", EXPECTED_WRITABLE)],
)
def test_every_mount_outcome_permits_exactly_what_it_is_declared_to(table, expected):
    """Every row of both tables, spelled out, per table.

    The weaker form of this asserted that the two tables were total and that
    their conditional rows matched, which a mutation setting one state to yes in
    BOTH tables passes: the shape is preserved and the meaning is inverted. Row
    values are what carry the meaning, so row values are what is asserted.
    """
    from cratekit.core import preflight

    mapping = getattr(preflight, table)
    assert set(mapping) == set(preflight.MountState), "the table is not total"
    assert {state.value: verdict.value for state, verdict in mapping.items()} == expected


def test_the_two_tables_differ_in_three_rows_and_every_one_is_a_read_signal_removed():
    """THREE rows, not one, and each is a place a read answer stood in for a write.

    ``library_path_missing`` is the visible one: the identity MATCHED and only the
    directory is absent, which is nothing to read and exactly when creating it is
    correct. The other two are the conditional rows, and they were the same
    defect one leg further down: "is anything there" answers a read, while a
    write needs to know whether CREATING the root lands on the volume this run is
    talking about. Sharing the read's condition refused a first run on every
    platform with no identity adapter, which is every platform that is not macOS
    or Windows.
    """
    from cratekit.core import preflight

    readable = preflight._STATE_READABLE
    writable = preflight._STATE_WRITABLE
    differ = {state for state in readable if readable[state] != writable[state]}
    assert differ == {
        preflight.MountState.LIBRARY_PATH_MISSING,
        preflight.MountState.IDENTITY_UNAVAILABLE,
        preflight.MountState.IDENTITY_NOT_RECORDED,
    }


@pytest.mark.parametrize(
    "state",
    ["IDENTITY_UNAVAILABLE", "IDENTITY_NOT_RECORDED"],
)
def test_a_platform_with_no_identity_adapter_may_create_a_library_it_cannot_read_yet(
    tmp_path, state
):
    """The guard must not fire on the correct case, and a first run IS the case.

    ``null_volume_identity`` is what every platform without an adapter resolves
    to, and it answers None for every volume, mounted or not. There is nothing to
    READ at a root that does not exist yet, and creating it is exactly what setup
    is for, so the two questions answer differently for the same machine.
    """
    from cratekit.core import preflight

    present = tmp_path / "library"
    present.mkdir()
    not_yet = tmp_path / "not-created-yet"

    for root, readable, writable in ((present, True, True), (not_yet, False, True)):
        status = preflight.MountStatus(
            state=getattr(preflight.MountState, state), configured_root=root
        )
        assert preflight.library_state_is_readable(status) is readable
        assert preflight.library_state_may_be_written(status) is writable


def test_a_first_run_on_a_platform_with_no_identity_adapter_writes_its_template(
    configured, tmp_path
):
    """Driven through the product's own seam, at the shape a first run is in.

    Root not yet created, no identity adapter: the wizard used to report
    "this run could not establish that the volume there is the one recorded for
    this library (identity_unavailable...)" and write nothing, which is a refusal
    aimed at every Linux and BSD install.
    """
    from cratekit.core import preflight

    configured.library.root.rename(tmp_path / "moved-away")
    wizard = setup_verb._Wizard({}, silent())

    setup_verb._seed_taxonomy(
        wizard, configured, probes(identity_provider=preflight.null_volume_identity)
    )

    assert config.state_path("taxonomy_active", configured).is_file()
    assert all(note.status is not doctor.Status.FAIL for note in wizard.notes), [
        note.detail for note in wizard.notes
    ]


def test_a_renamed_library_folder_on_the_right_volume_is_written_not_refused(
    configured, tmp_path, monkeypatch
):
    """Reachable with no flags at all: set up, rename the folder, run setup.

    The identity still matches, because the volume is the same one; only the
    directory is gone. The first version of this guard called that "the volume
    recorded for this library is not the one mounted there" while printing
    "recorded F1E2-D3C4, observed F1E2-D3C4" in the same sentence, and refused
    the one write that was correct.
    """
    configured.library.root.rename(tmp_path / "renamed-by-hand")
    wizard = setup_verb._Wizard({}, silent())

    setup_verb._seed_taxonomy(wizard, configured, probes())

    assert config.state_path("taxonomy_active", configured).is_file()
    assert all(note.status is not doctor.Status.FAIL for note in wizard.notes), [
        note.detail for note in wizard.notes
    ]


def test_a_refusal_to_write_never_contradicts_its_own_parenthetical(configured):
    """The refusal that remains has to describe the state it printed.

    A wrong volume is still a refusal, and the sentence has to be one the
    observed and recorded identities beside it can support.
    """
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(
        wizard, configured, probes(identity_provider=lambda _p: "0000-0000")
    )
    note = wizard.notes[0]
    assert note.status is doctor.Status.FAIL
    assert "could not establish" in note.detail
    assert "0000-0000" in note.detail and VOLUME in note.detail
    assert not config.state_path("taxonomy_active", configured).exists()


# ── taxonomy.active: two claims, neither of them checked ─────────────────────


def test_a_configured_template_that_ships_nowhere_is_refused(configured):
    """The check said "template X is active" while comparing nothing to X.

    ``config.validate`` accepts any bare token, so a transposed letter reached
    the file and doctor reported it green with a bucket count read from whatever
    copy happened to be beside the database.
    """
    seed_taxonomy(configured)
    document = document_for(configured.library.root)
    document["taxonomy"] = {"template": "no-such-template"}
    finding = find(
        doctor.run(config.from_dict(document), probes=probes()), "taxonomy.active"
    )
    assert finding.status is doctor.Status.FAIL
    assert "no-such-template" in finding.detail
    assert finding.remedy is Remedy.RUN_SETUP


def test_the_active_template_is_not_reported_at_all_when_its_disk_is_absent(configured):
    """FAIL here would send the user to setup, and setup would then copy a
    template onto whatever filesystem is at that path, which is the write this
    unit had to be stopped from making.
    """
    seed_taxonomy(configured)
    gone = probes(identity_provider=lambda _p: "0000-0000", mount_enumerator=lambda: ())
    finding = find(doctor.run(configured, probes=gone), "taxonomy.active")
    assert finding.status is doctor.Status.INFO
    assert finding.remedy is None


def test_an_active_template_on_the_recorded_volume_reports_what_it_verified(configured):
    seed_taxonomy(configured)
    finding = find(doctor.run(configured, probes=probes()), "taxonomy.active")
    assert finding.status is doctor.Status.OK
    assert "on the recorded library volume" in finding.detail
    assert "'default'" in finding.detail


# ── taxonomy.active: a stale copy told from an edited one (R-689) ────────────
#
# Setup records a digest of the shipped text it copied, beside the copy. Doctor
# reads the record and answers with three digests: the recorded one, the copy's
# and the shipped text's. The one INFO is a copy that still matches the record
# while the shipped text has moved on, which is the tenth sitting's library:
# set up before ``[long_tracks]`` shipped, never edited, and since R-685 missing
# the section from every verb with nothing saying why.


def _seed_with_origin(cfg: config.Config) -> Path:
    """What setup leaves: the copy and the record, through the wizard's own code."""
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, cfg, probes())
    return config.state_path("taxonomy_origin", cfg)


def _taxonomy_finding(cfg: config.Config) -> doctor.Finding:
    return find(doctor.run(cfg, probes=probes()), "taxonomy.active")


def test_setup_records_which_shipped_text_the_copy_was_made_from(configured):
    origin = _seed_with_origin(configured)
    assert origin.is_file()
    assert origin.parent == config.state_path("taxonomy_active", configured).parent
    record = tomllib.loads(origin.read_text(encoding="utf-8"))
    shipped = setup_verb.template_text("default")
    assert record == {
        "template": "default",
        "sha256": taxonomy.template_digest(shipped),
    }
    assert config.state_path("taxonomy_active", configured).read_text(encoding="utf-8") == shipped


def test_setup_writes_no_record_for_a_copy_it_left_alone(configured):
    """It cannot know which shipped text an existing copy came from, so a record
    would say "unedited" over a copy nothing established that about."""
    seed_taxonomy(configured)
    origin = _seed_with_origin(configured)
    assert not origin.exists()


def test_a_copy_setup_made_that_the_shipped_template_has_since_outgrown_is_info(configured):
    """The tenth sitting's library. The record says the copy is the one setup
    made, the copy still matches it, and the shipped text has moved on."""
    older = shipped_without("long_tracks")
    write_active(configured, older)
    origin = config.state_path("taxonomy_origin", configured)
    origin.write_text(taxonomy.origin_record_text("default", older), encoding="utf-8")
    finding = _taxonomy_finding(configured)
    assert finding.status is doctor.Status.INFO
    assert finding.remedy is None
    assert "unedited" in finding.detail
    assert "[long_tracks]" in finding.detail
    assert "does not rewrite the copy" in finding.detail
    # Reported, never repaired: the copy is exactly what it was.
    assert config.state_path("taxonomy_active", configured).read_text(encoding="utf-8") == older


def test_a_copy_the_person_edited_is_theirs_whatever_the_shipped_template_did(configured):
    older = shipped_without("long_tracks")
    write_active(configured, older)
    origin = config.state_path("taxonomy_origin", configured)
    origin.write_text(taxonomy.origin_record_text("default", older), encoding="utf-8")
    active = config.state_path("taxonomy_active", configured)
    active.write_text("# mine\n" + older, encoding="utf-8")
    finding = _taxonomy_finding(configured)
    assert finding.status is doctor.Status.OK
    assert "edited since setup copied the shipped 'default'" in finding.detail
    assert "long_tracks" not in finding.detail


def test_a_copy_setup_made_from_the_text_that_still_ships_is_ok_and_says_so(configured):
    _seed_with_origin(configured)
    finding = _taxonomy_finding(configured)
    assert finding.status is doctor.Status.OK
    assert "unedited since setup copied the shipped 'default', which has not changed" in (
        finding.detail
    )


def test_a_copy_with_no_record_says_the_origin_is_unrecorded(configured):
    """Every library set up before the record existed. Matching the shipped text
    as it ships now is said; differing from it is said as undecidable, since
    the two histories look the same from here."""
    seed_taxonomy(configured)
    matching = _taxonomy_finding(configured)
    assert matching.status is doctor.Status.OK
    assert "nothing records which shipped text" in matching.detail
    assert "matches the shipped 'default' as it ships now" in matching.detail

    write_active(configured, shipped_without("long_tracks"))
    differing = _taxonomy_finding(configured)
    assert differing.status is doctor.Status.OK
    assert "nothing records which shipped text" in differing.detail
    assert "cannot be told" in differing.detail
    assert "long_tracks" not in differing.detail


def test_a_record_that_cannot_be_used_is_said_rather_than_read_as_no_record(configured):
    origin = _seed_with_origin(configured)
    origin.write_text('template = "default"\nsha256 = "short"\n', encoding="utf-8")
    finding = _taxonomy_finding(configured)
    assert finding.status is doctor.Status.INFO
    assert "is not usable" in finding.detail
    assert "cannot be told" in finding.detail


def test_a_record_this_account_cannot_read_is_said_rather_than_read_as_no_record(configured):
    origin = _seed_with_origin(configured)
    origin.chmod(0)
    try:
        finding = _taxonomy_finding(configured)
    finally:
        origin.chmod(0o644)
    assert finding.status is doctor.Status.INFO
    assert "could not be read" in finding.detail
    assert finding.remedy is None


def test_a_shipped_template_that_dropped_a_section_the_copy_still_has_is_named_too(configured):
    """The difference runs both ways. A shipped template that removed or renamed
    a section leaves nothing gained, and the detail must not then claim the
    change is inside sections both declare."""
    older = shipped_without("long_tracks") + "\n[retired_section]\nkept = true\n"
    write_active(configured, older)
    origin = config.state_path("taxonomy_origin", configured)
    origin.write_text(taxonomy.origin_record_text("default", older), encoding="utf-8")
    finding = _taxonomy_finding(configured)
    assert finding.status is doctor.Status.INFO
    assert "it now declares [long_tracks], which the copy does not" in finding.detail
    assert "it no longer declares [retired_section], which the copy still does" in (
        finding.detail
    )


def test_a_shipped_change_inside_a_section_both_declare_is_said_as_such(configured):
    shipped = setup_verb.template_text("default")
    bucket = taxonomy.load_taxonomy(shipped).buckets[0]
    older = shipped.replace(f'display = "{bucket.display}"', 'display = "Older Name"', 1)
    assert older != shipped
    write_active(configured, older)
    origin = config.state_path("taxonomy_origin", configured)
    origin.write_text(taxonomy.origin_record_text("default", older), encoding="utf-8")
    finding = _taxonomy_finding(configured)
    assert finding.status is doctor.Status.INFO
    assert "the difference is inside sections both declare" in finding.detail
    assert "[" not in finding.detail.split("has changed since:")[1].split(".")[0]


def test_a_record_naming_a_template_other_than_the_configured_one_is_info(configured):
    """The record carries the fact the name check alone cannot see: the copy came
    from one shipped template and the configuration now names another."""
    origin = _seed_with_origin(configured)
    record = origin.read_text(encoding="utf-8").replace('template = "default"', 'template = "club"')
    origin.write_text(record, encoding="utf-8")
    finding = _taxonomy_finding(configured)
    assert finding.status is doctor.Status.INFO
    assert "made from the shipped 'club'" in finding.detail
    assert "taxonomy.template now names 'default'" in finding.detail
    assert "leaves an existing copy alone" in finding.detail


def test_a_packaged_text_that_cannot_be_read_is_a_damaged_install_and_compares_nothing(
    configured, monkeypatch
):
    _seed_with_origin(configured)

    def unreadable(name: str) -> taxonomy.Fingerprint:
        raise OSError(errno.EIO, "packaged text", name)

    monkeypatch.setattr(taxonomy, "shipped_template_fingerprint", unreadable)
    finding = _taxonomy_finding(configured)
    assert finding.status is doctor.Status.INFO
    assert "could not be read" in finding.detail
    assert "damaged or partial install" in finding.detail


def test_a_record_that_cannot_be_written_does_not_uncopy_the_template(configured, monkeypatch):
    """The copy is there and every verb routes by it. The note says the record is
    missing and names no remedy, since a second run leaves the copy alone."""
    real = config.atomic_write_bytes
    active = config.state_path("taxonomy_active", configured)

    def refuse_second(data: bytes, path: Path, *args, **kwargs):
        if path != active:
            raise OSError(errno.EROFS, "read only", str(path))
        return real(data, path, *args, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", refuse_second)
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, configured, probes())
    assert active.is_file()
    assert not config.state_path("taxonomy_origin", configured).exists()
    notes = [n for n in wizard.notes if n.key == "setup.taxonomy"]
    assert [n.status for n in notes] == [doctor.Status.INFO]
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
    """The remedy has to be true. A recorded value outside the closed set was
    returned by ``resolve`` ahead of the guard, so every re-run produced the same
    refusal and the only escape was to hand-edit the TOML this verb abolishes.
    """
    document = dict(configured.to_toml_dict())
    document["taxonomy"] = {"template": "defualt"}
    wizard = setup_verb._Wizard(document, silent())

    answer = wizard.resolve(
        "taxonomy.template",
        flag=None,
        question="Which taxonomy template",
        default="default",
        choices=setup_verb.template_names(),
    )
    assert answer == "default"
    assert any("is not one of" in note.detail for note in wizard.notes)


def test_the_taxonomy_flag_is_a_closed_set_like_the_profile_beside_it(capsys):
    """argparse refuses the typo before anything can persist it.

    Executed against the build without the choices: ``--taxonomy defualt`` exited
    30, wrote the misspelling into config.toml, and then every re-run with no
    flag at all read it back and failed the same way forever.
    """
    code, _out, _err = drive(["setup", "--taxonomy", "defualt"])
    assert code == int(ExitCode.USAGE)
    # argparse owns this message and writes it to the process's own stream, which
    # is the one thing in the product that is allowed to (KTD25 reserves status 2
    # for it alone).
    assert "invalid choice: 'defualt'" in capsys.readouterr().err


def test_a_template_name_shaped_like_a_path_is_a_configuration_problem(library):
    """What the foundation CAN assert about a name it may not resolve.

    Membership is the taxonomy module's question and that module sits above
    config, so validation asserts the shape instead: the name is composed into a
    packaged resource path, and a separator in it would read some other file.
    """
    document = document_for(library)
    document["taxonomy"] = {"template": "../../etc/passwd"}
    assert any(config.TAXONOMY_TEMPLATE_KEY in p for p in config.validate(document))
    assert config.validate(document_for(library)) == []


# ── backup.remote: every provider nobody had gotten around to adding ─────────


@pytest.mark.parametrize("kind", ["onedrive", "box", "pcloud", "dropbox"])
def test_a_provider_with_a_recycle_bin_is_no_longer_green_by_default(configured, kind):
    """The one-row table reported OK for every type that was not in it.

    The residual finding "Backup pruning reclaims space only if the remote is
    configured to" is entirely about providers that trash on delete, and four of them read
    green over the exact condition the check exists to find, because the branch
    said "no row, therefore fine".
    """
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:"}
    cfg = config.from_dict(document)
    finding = find(
        doctor.run(cfg, probes=probes(rclone_remotes=lambda _r: {"archive": {"type": kind}})),
        "backup.remote",
    )
    assert finding.status is not doctor.Status.OK, finding.detail


def test_a_provider_whose_no_trash_option_is_set_the_other_way_round_is_read_correctly(
    configured,
):
    """Drive's option must be false and OneDrive's must be true. One shared "is
    it false" test read one of the two backwards in both directions.
    """
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:"}
    cfg = config.from_dict(document)

    business = {"type": "onedrive", "drive_type": "business"}
    hardened = probes(rclone_remotes=lambda _r: {"archive": {**business, "hard_delete": "true"}})
    assert find(doctor.run(cfg, probes=hardened), "backup.remote").status is doctor.Status.OK

    trashing = probes(rclone_remotes=lambda _r: {"archive": {**business, "hard_delete": "false"}})
    assert find(doctor.run(cfg, probes=trashing), "backup.remote").failed


@pytest.mark.parametrize("drive_type", ["personal", None])
@pytest.mark.parametrize("hard_delete", ["true", "false"])
def test_a_onedrive_remote_where_hard_delete_does_nothing_is_a_note(
    configured, drive_type, hard_delete
):
    """rclone honours hard_delete on business drives and document libraries only.

    Its own backend help says a personal account does not support the permanent
    delete call. Reading the option alone reported that remote green on a setting
    that changes nothing, and red on one that nothing could change. An unset
    drive_type is the same answer, because which kind of drive it is was not read.
    """
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:"}
    cfg = config.from_dict(document)
    settings = {"type": "onedrive", "hard_delete": hard_delete}
    if drive_type is not None:
        settings["drive_type"] = drive_type
    finding = find(
        doctor.run(cfg, probes=probes(rclone_remotes=lambda _r: {"archive": settings})),
        "backup.remote",
    )
    assert finding.status is doctor.Status.INFO, finding.detail
    assert f"drive_type is {drive_type or 'unset'}" in finding.detail


@pytest.mark.parametrize("extra", [{}, {"permanent_delete": "true"}])
def test_dropbox_is_not_told_to_set_an_option_rclone_does_not_have(configured, extra):
    """rclone's Dropbox backend has no per-remote delete option at all.

    The row used to name ``permanent_delete``, so every Dropbox remote failed
    with a fix nothing could apply, and one where somebody wrote that key by
    hand went green while every prune still went to Dropbox's deleted files.
    """
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:"}
    cfg = config.from_dict(document)
    finding = find(
        doctor.run(
            cfg,
            probes=probes(rclone_remotes=lambda _r: {"archive": {"type": "dropbox", **extra}}),
        ),
        "backup.remote",
    )
    assert finding.status is doctor.Status.INFO, finding.detail
    assert "permanent_delete" not in finding.detail
    assert "no per-remote option" in finding.detail


def test_a_remote_type_with_no_row_says_so_rather_than_passing(configured):
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:"}
    cfg = config.from_dict(document)
    finding = find(
        doctor.run(
            cfg, probes=probes(rclone_remotes=lambda _r: {"archive": {"type": "s3"}})
        ),
        "backup.remote",
    )
    assert finding.status is doctor.Status.INFO
    assert "no row" in finding.detail


def test_a_remote_where_a_delete_is_a_delete_is_the_one_that_reports_green(configured):
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:"}
    cfg = config.from_dict(document)
    finding = find(
        doctor.run(
            cfg, probes=probes(rclone_remotes=lambda _r: {"archive": {"type": "local"}})
        ),
        "backup.remote",
    )
    assert finding.status is doctor.Status.OK


def test_the_remote_path_form_resolves_to_the_remote_it_names(configured):
    """``remote:path`` is rclone's own spelling. Stripping the trailing colon
    left the path attached, so a correct destination failed as an unknown remote.
    """
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:library/archive"}
    cfg = config.from_dict(document)
    finding = find(
        doctor.run(
            cfg,
            probes=probes(rclone_remotes=lambda _r: {"archive": {"type": "drive", "use_trash": "false"}}),
        ),
        "backup.remote",
    )
    assert finding.status is doctor.Status.OK


def test_an_unknown_remote_is_not_sent_to_a_verb_that_cannot_fix_it(configured):
    """The wizard has no question, no flag and no code path for backup.remote."""
    document = document_for(configured.library.root)
    document["backup"] = {"remote": "archive:"}
    cfg = config.from_dict(document)
    finding = find(
        doctor.run(cfg, probes=probes(rclone_remotes=lambda _r: {"other": {"type": "local"}})),
        "backup.remote",
    )
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.FIX_CONFIG_VALUES
    assert not any(
        "backup" in argument for entry in registry.entries() if entry.name == "setup"
        for argument in entry.doctor_checks
    )


# ── a broken override, a headless machine, and the metadata bound ────────────


def test_a_set_but_broken_binary_override_gets_the_remedy_that_exists_for_it(
    configured, tmp_path, monkeypatch
):
    """``binaries.Remedy.FIX_BINARY_OVERRIDE`` existed, ``render`` carried its
    sentence, and no check ever emitted it. Reported as "not found on PATH,
    install it", a user installs a binary they already have and the override
    keeps winning, because ``find`` deliberately does not fall through.
    """
    broken = tmp_path / "not-executable"
    broken.write_text("")
    monkeypatch.setenv(binaries.env_var("ffmpeg"), str(broken))

    # The REAL rule, from the module that owns it, against a real variable. The
    # green machine answers this seam with None like every other, so a test that
    # let it stand would be asserting about the fake.
    machine = probes(
        find_binary=lambda _n: None, binary_override_problem=binaries.override_problem
    )
    finding = find(doctor.run(configured, probes=machine), "binary.ffmpeg")
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.FIX_BINARY_OVERRIDE
    assert str(broken) in finding.detail


def test_a_binary_that_is_simply_absent_still_says_install_it(configured):
    finding = find(
        doctor.run(configured, probes=probes(find_binary=lambda _n: None)), "binary.ffmpeg"
    )
    assert finding.remedy is Remedy.INSTALL_BINARY


def test_a_headless_machine_that_opted_into_the_environment_fallback_is_not_red(
    configured, monkeypatch
):
    """The check names the fallback as the alternative and never asked whether it
    was in use, so a machine set up the documented way reported a failing keychain
    beside two green credentials and exited PRECONDITION on the whole run.
    """
    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    for credential in secrets.Credential:
        monkeypatch.setenv(
            f"CRATEKIT_CREDENTIAL_{str(credential).upper().replace('-', '_')}", "value"
        )
    seed_taxonomy(configured)

    machine = probes(
        keychain_available=lambda: False,
        environment_credential=secrets.environment_value,
    )
    report = doctor.run(configured, probes=machine)
    keychain = find(report, "keychain.reachable")
    assert keychain.status is doctor.Status.INFO
    assert not report.failures, [f.key for f in report.failures]


def test_a_machine_with_no_keychain_and_no_fallback_is_still_red(configured):
    finding = find(
        doctor.run(configured, probes=probes(keychain_available=lambda: False)),
        "keychain.reachable",
    )
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.INSTALL_KEYCHAIN_BACKEND


def test_a_fallback_supplying_only_some_of_what_is_needed_is_still_red(
    configured, monkeypatch
):
    """Half a credential set is not a working machine, and saying so is the
    difference between a note and a report that hides a missing value.
    """
    monkeypatch.setenv(secrets.ENV_ALLOW_ENV_CREDENTIALS, "1")
    monkeypatch.setenv("CRATEKIT_CREDENTIAL_PROVIDER_SESSION", "value")

    machine = probes(
        keychain_available=lambda: False,
        environment_credential=secrets.environment_value,
    )
    finding = find(doctor.run(configured, probes=machine), "keychain.reachable")
    assert finding.status is doctor.Status.FAIL
    assert "identify-key" in finding.detail


# ── the containment report, which nothing in this file asserted at all ───────


def test_a_database_outside_the_library_root_is_reported_on_every_run(
    library, tmp_path, monkeypatch
):
    """The four-wave obligation ``tests/_pending.py`` held against this unit.

    Refusing at load makes the consequence visible at setup, when the database
    can still be moved, and does nothing at all about the install where somebody
    accepted it eighteen months ago and has forgotten that their snapshots are
    copies across two filesystems rather than one atomic commit.
    """
    document = document_for(library)
    document["library"]["db_path"] = str(tmp_path / "elsewhere" / "master.db")
    document["library"]["db_outside_root_acknowledged_on"] = "2026-08-01"
    finding = find(
        doctor.run(config.from_dict(document), probes=probes()), "library.db_containment"
    )

    assert finding.status is doctor.Status.INFO
    assert str(tmp_path / "elsewhere" / "master.db") in finding.detail
    assert str(library) in finding.detail
    assert "2026-08-01" in finding.detail
    assert "two filesystems" in finding.detail


def test_a_contained_database_says_the_snapshot_commits_with_a_rename(configured):
    finding = find(doctor.run(configured, probes=probes()), "library.db_containment")
    assert finding.status is doctor.Status.OK
    assert "under library.root" in finding.detail


# ── the Trash on the library volume, which deletion refuses without ──────────


def test_a_volume_whose_trash_accepts_a_move_reads_green(configured):
    finding = find(doctor.run(configured, probes=probes()), "library.trash")
    assert finding.status is doctor.Status.OK
    assert str(configured.library.root) in finding.detail
    assert finding.remedy is None


def test_a_volume_with_no_usable_trash_refuses_because_a_verb_depends_on_it(configured):
    """R35 sends a confirmed deletion to the Trash and never to an unlink.

    Without this check a person meets that refusal in the middle of a deletion,
    after the review and after the confirm gate, against a plan already digested.
    The remedy is NOT run-doctor, which is what ``trash.assert_usable`` refuses
    with: that token sends somebody here, and answering with it here is a loop.
    """
    finding = find(
        doctor.run(configured, probes=doctor_machines.hostile()), "library.trash"
    )
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.GRANT_PATH_ACCESS
    assert "not writable" in finding.detail
    assert "never unlinks it" in finding.detail


def test_a_volume_with_no_trash_directory_yet_is_not_a_failure(configured):
    """The false red the cross-model review found, driven both ways.

    ``trash.probe`` creates the per-volume Trash on first use because the desktop
    does, and the deletion pass takes that default. Doctor asks with
    ``create=False`` so its answer cannot be produced by its own asking, which
    means a volume nobody has deleted from answers "not a directory" here and
    works perfectly when a deletion actually runs. Reporting that as red told a
    person deletion would refuse on a machine where it would succeed, which is the
    one thing a precondition must never do.
    """
    finding = find(
        doctor.run(configured, probes=probes(trash_probe=doctor_machines._absent_trash)),
        "library.trash",
    )
    assert finding.status is doctor.Status.OK
    assert finding.remedy is None
    assert "creates it on first use" in finding.detail


def test_the_two_probe_answers_that_made_the_false_red_are_really_different(tmp_path):
    """The asymmetry itself, measured on the real probe rather than on a seam.

    This is the evidence the finding rested on, kept as a test so the seam above
    cannot drift away from what the module it stands in for actually does.
    """
    from cratekit.deletion import trash

    volume = tmp_path / "volume"
    (volume / "Music").mkdir(parents=True)
    home = tmp_path / "home"
    common = {"home": home, "uid": 501, "platform": "linux"}

    asked = trash.probe(volume, create=False, **common)
    made = trash.probe(volume, create=True, **common)

    assert not asked.usable and asked.absent, "doctor's question"
    assert made.usable, "the deletion pass's question, on the same volume"


def test_a_broken_trash_is_informational_when_no_verb_this_profile_needs_it(library):
    """The deletion module off means nothing on this machine trashes a file.

    Reporting red for a capability nothing uses is how a person learns to ignore
    red, which is the argument the INFO status carries everywhere else here.
    """
    document = document_for(library)
    document["profile"] = {"name": "slim"}
    cfg = config.from_dict(document)
    finding = find(
        doctor.run(cfg, probes=probes(trash_probe=doctor_machines._no_trash)),
        "library.trash",
    )
    assert finding.status is doctor.Status.INFO
    assert "nothing depends on it today" in finding.detail
    assert finding.remedy is None


def test_the_trash_check_cannot_pass_by_having_run(tmp_path, monkeypatch):
    """The seam binds ``create=False``, and the BINDING is what is driven.

    THE VERSION THIS REPLACES MEASURED NOTHING, and the author's own mutation
    table is what said so: flipping the seam to ``create=True`` killed zero
    tests. It watched a temporary directory for a new folder, and on this
    platform ``layout_for`` resolves that directory's volume root to ``/``, so
    the create it was watching for was refused by the filesystem rather than by
    the argument. The test passed for a reason that had nothing to do with the
    property.

    So the call is captured instead. ``trash.probe`` creates the per-volume Trash
    by default, because the desktop does too, and a health check taking that
    default would make the directory it is asking about exist and then report the
    pass it had itself produced.
    """
    from cratekit.deletion import trash

    seen: list[dict] = []

    def recording(path, **kwargs):
        seen.append(dict(kwargs, path=path))
        return trash.TrashStatus(None, False, "not probed for real")

    monkeypatch.setattr(doctor.trash, "probe", recording)
    volume = tmp_path / "volume"
    (volume / "Music").mkdir(parents=True)

    doctor._probe_trash(volume)

    assert len(seen) == 1
    assert seen[0]["create"] is False, (
        "the doctor probe took the creating default, so the check can pass by "
        "having run"
    )
    assert seen[0]["path"] == volume


def test_a_trash_probe_the_operating_system_refuses_is_a_failure_with_the_right_act(
    configured,
):
    """An unanswerable question is not a pass, and the act follows the refusal.

    The classification runs at ``Finding`` construction, so a permission error
    reaches the report as grant-path-access and a read-only volume as
    remount-writable, rather than as one hardcoded sentence for both.
    """

    def refuses(path):
        # WITH A FILENAME, because ``access_refusal`` will not claim a refusal it
        # cannot name a path for: a sentence with no path is one a user can do
        # nothing with. Every real refusal on this route carries one, since the
        # probe stats and opens named directories.
        raise PermissionError(errno.EACCES, "Operation not permitted", str(path))

    finding = find(
        doctor.run(configured, probes=probes(trash_probe=refuses)), "library.trash"
    )
    assert finding.status is doctor.Status.FAIL
    assert "could not be established" in finding.detail
    assert finding.remedy is not None
    assert finding.remedy is not Remedy.REPORT_DEFECT


def test_an_unanswerable_trash_probe_is_informational_when_no_verb_needs_it(library):
    """The gate on the refusal branch, which the fix round left unmeasured.

    Forcing that branch to FAIL regardless of the profile killed nothing in the
    author's own table, because the only test of it ran on the full profile where
    the answer is FAIL either way. A machine with the deletion module switched off
    has nothing that moves a file to the Trash, so an unanswerable question about
    it is worth knowing and is not a fault, which is the rule every neighbouring
    check in this file applies.
    """

    def refuses(path):
        raise PermissionError(errno.EACCES, "Operation not permitted", str(path))

    document = document_for(library)
    document["profile"] = {"name": "slim"}
    finding = find(
        doctor.run(config.from_dict(document), probes=probes(trash_probe=refuses)),
        "library.trash",
    )
    assert finding.status is doctor.Status.INFO
    assert finding.remedy is None
    assert "could not be established" in finding.detail


def test_the_trash_check_is_unchecked_when_there_is_no_configuration(tmp_path, monkeypatch):
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "empty"))
    config.reset_cache()
    finding = find(doctor.run(probes=probes()), "library.trash")
    assert finding.status is doctor.Status.INFO
    assert "no usable configuration" in finding.detail


# ═══════════════════════════════════════════════════════════════════════════
# 9. What the second review found: a truth teller that could refuse to run
# ═══════════════════════════════════════════════════════════════════════════
#
# The pass that removed the false greens added three ways to be unavailable and
# two claims nobody checked. A doctor that cannot start on a broken machine is
# worse than one that reports the wrong thing about it, because the broken
# machine is the one it exists for.


class _StubResources:
    """``importlib.resources`` with its package root pointed somewhere else.

    A stand-in for a partial install: the package imports, and the packaged data
    beside it is missing or unreadable. Injected rather than simulated by
    deleting real files, because the real ones are the ones this suite runs on.
    """

    def __init__(self, root: Path) -> None:
        self.root = root

    def files(self, _package: str) -> Path:
        return self.root


@pytest.fixture
def stripped_install(monkeypatch, tmp_path):
    """A cratekit whose templates directory does not exist."""
    from cratekit.core import taxonomy as taxonomy_module

    monkeypatch.setattr(taxonomy_module, "resources", _StubResources(tmp_path / "pkg"))
    return tmp_path


@pytest.fixture
def unreadable_install(monkeypatch, tmp_path):
    """A cratekit whose templates directory exists and cannot be listed."""
    from cratekit.core import taxonomy as taxonomy_module

    templates = tmp_path / "pkg" / "templates"
    templates.mkdir(parents=True)
    (templates / "taxonomy.default.toml").write_text("")
    templates.chmod(0o000)
    monkeypatch.setattr(taxonomy_module, "resources", _StubResources(tmp_path / "pkg"))
    yield tmp_path
    templates.chmod(0o700)


@pytest.mark.parametrize("install", ["stripped_install", "unreadable_install"])
def test_the_whole_command_line_survives_an_install_with_no_readable_templates(
    install, request, configured, monkeypatch
):
    """BLOCKING. The command tree builds EVERY landed verb's parser on EVERY run.

    Putting ``choices=shipped_template_names()`` on the wizard's flag therefore
    walked packaged data before anything dispatched, so a missing or unreadable
    templates directory took ``crate doctor`` and ``crate --help`` down with an
    unhandled OSError. Doctor exists for the broken machine and a partial install
    is a broken machine; it has to be able to report on one, and this was a
    strict regression against the build before the fix.
    """
    request.getfixturevalue(install)
    monkeypatch.setattr(doctor, "Probes", lambda: probes())

    assert drive(["--help"])[0] == int(ExitCode.OK)

    code, out, err = drive(["--output", "json", "doctor"])
    assert code == int(ExitCode.PRECONDITION), err
    checks = {c["key"]: c for c in json.loads(out)["data"]["checks"]}
    # It reports, and what it reports is the truth about this install: the
    # packaged data could not be READ. Saying instead that no template ships
    # under the configured name is a claim about a directory nobody could open,
    # and it carried run-setup, which cannot repair packaged data.
    assert checks["taxonomy.active"]["status"] == "fail"
    assert "could not be listed" in checks["taxonomy.active"]["detail"]
    assert "not established" in checks["taxonomy.active"]["detail"]
    assert checks["taxonomy.active"]["remedy"] != "run-setup"


def test_a_missing_templates_directory_is_an_empty_answer_not_an_exception(
    stripped_install,
):
    from cratekit.core import taxonomy as taxonomy_module

    assert taxonomy_module.shipped_template_names() == ()


def test_an_install_with_no_templates_offers_no_closed_set_rather_than_an_empty_one(
    stripped_install, tmp_path, monkeypatch
):
    """An empty ``choices`` rejects every value including the correct one.

    So the flag carries no closed set when nothing ships, and the wizard reports
    the missing template as a finding instead of arguing with the user about a
    name that would have been right on a whole install.
    """
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setattr(doctor, "Probes", lambda: probes())

    code, out, err = drive(
        [
            "--output", "json", "setup",
            "--library-root", str(root),
            "--volume-id", VOLUME,
            "--db-path", str(root / "db" / "master.db"),
            "--staging", str(tmp_path / "staging"),
            "--profile", "slim",
            "--taxonomy", "default",
        ]
    )
    assert code != int(ExitCode.USAGE), err
    checks = {c["key"]: c for c in json.loads(out)["data"]["checks"]}
    assert checks["setup.taxonomy"]["status"] == "fail"
    # A DIRECTORY THAT IS NOT THERE IS A DAMAGED INSTALL, not a name the user
    # typed wrongly, and the wizard used to say the second for both. The finding
    # here is the first, and it agrees with what doctor says about the same
    # install two lines further down the same report.
    assert "could not be listed" in checks["setup.taxonomy"]["detail"]
    assert "damaged or partial install" in checks["setup.taxonomy"]["detail"]
    assert checks["setup.taxonomy"]["remedy"] == str(Remedy.REPORT_DEFECT)


def test_a_shipped_name_configuration_would_reject_is_never_offered(
    monkeypatch, tmp_path
):
    """Two layers, one question, one answer, one layer further down.

    Anything between the prefix and the suffix is a candidate on disk, so
    ``taxonomy.deep.house.toml`` yields ``deep.house``, which validation refuses
    because the name is composed into a packaged resource path. Offering it as a
    closed-set choice and then refusing it is the defect the shared walk exists
    to prevent, reappearing one layer down.
    """
    from cratekit.core import taxonomy as taxonomy_module

    templates = tmp_path / "pkg" / "templates"
    templates.mkdir(parents=True)
    for name in ("taxonomy.default.toml", "taxonomy.deep.house.toml", "taxonomy..toml"):
        (templates / name).write_text("")
    monkeypatch.setattr(taxonomy_module, "resources", _StubResources(tmp_path / "pkg"))

    assert taxonomy_module.shipped_template_names() == ("default",)


def test_every_name_the_wheel_actually_ships_is_one_configuration_accepts(library):
    """The real packaged set, against the real validator."""
    from cratekit.core import taxonomy as taxonomy_module

    shipped = taxonomy_module.shipped_template_names()
    assert shipped, "the wheel ships no taxonomy template"
    for name in shipped:
        document = document_for(library)
        document["taxonomy"] = {"template": name}
        assert config.validate(document) == [], name


# ── the derive guard that over-fired ────────────────────────────────────────


def test_a_library_folder_not_yet_created_under_a_real_mount_is_not_refused():
    """BLOCKING. The first run this guard was most likely to meet, refused.

    ``Path(root).is_dir()`` was too strong by exactly one case: a library folder
    that does not exist yet, directly under a mount point that is attached and
    readable. The identity read there comes from the right volume, and the
    refusal told the user to attach a drive that was already attached, with the
    only escape being a flag whose value nothing in the product prints.

    The filesystem root is used as the mount, because it is a mount point on
    every platform this runs on and needs no privileges to arrange.
    """
    from cratekit.core import preflight

    wizard = setup_verb._Wizard({}, silent())
    not_yet_created = Path("/") / "cratekit-library-that-does-not-exist"
    assert not not_yet_created.exists()
    assert preflight.deepest_existing(not_yet_created) == Path("/")

    derived = setup_verb._resolve_volume_id(
        wizard, str(not_yet_created), None, probes(identity_provider=lambda _p: VOLUME)
    )
    assert derived == VOLUME


@pytest.mark.parametrize(
    "gap", ["library", "Music/library", "Music/a/b/library"], ids=["one", "two", "four"]
)
def test_a_library_nested_under_an_attached_volume_derives_at_any_depth(
    volumes_directory, gap
):
    """BLOCKING. The rule counted levels, and depth was never the hazard.

    Driven on one attached volume in one run, ``<mount>/library`` was accepted
    and ``<mount>/Music/library`` was refused with "attach the library volume and
    run setup again", which is false: the volume is attached, the identity read
    comes from it, and nothing in the product prints the identity a first-run
    user would need for the only escape it offered.
    """
    attached = volumes_directory.attach("DISK_THAT_IS_ATTACHED")
    (attached / "Music" / "a" / "b").mkdir(parents=True, exist_ok=True)
    root = attached / gap
    assert not root.exists()

    wizard = setup_verb._Wizard({}, silent())
    derived = setup_verb._resolve_volume_id(
        wizard, str(root), None, probes(identity_provider=lambda _p: VOLUME)
    )
    assert derived == VOLUME


def test_the_derive_still_refuses_when_the_mount_point_is_empty(volumes_directory):
    """And the case that cost a library is still refused.

    ``/Volumes/NAME/Music`` with the drive unplugged: ``/Volumes/NAME`` is where
    a volume mounts and nothing is mounted there, so the identity a walk finds
    now belongs to whatever filesystem is above it.
    """
    from cratekit.core import preflight

    root = volumes_directory / "EP_LIBRARY" / "Music"
    assert preflight.deepest_existing(root) == volumes_directory.resolve()
    assert preflight.identity_source(root) is None

    wizard = setup_verb._Wizard({}, silent())
    with pytest.raises(CratekitError) as excinfo:
        setup_verb._resolve_volume_id(
            wizard, str(root), None, probes(identity_provider=lambda _p: "BOOT")
        )
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert "no volume is mounted there right now" in excinfo.value.cause.message
    assert str(volumes_directory / "EP_LIBRARY") in excinfo.value.cause.message


@pytest.mark.parametrize(
    "gap", ["", "library", "Music/library", "Music/a/b/library"],
    ids=["at-the-mount-point", "one", "two", "four"],
)
def test_an_ejected_volume_leaves_a_mount_POINT_behind_and_the_derive_refuses_it(
    volumes_directory, gap
):
    """BLOCKING, and it is the FIRST defect arriving through the second fix for it.

    The rule before this one refused a gap a volume would fill, which reads
    absence as the hazard. An ejected volume routinely leaves its mount point
    behind as an empty directory on the boot disk: ``core/preflight``'s own
    opening paragraphs name that as the first of the three broken states the
    module exists to tell apart.

    With ``<mount>/NAME`` sitting there, nothing is missing, so nothing was
    refused, and ``identity_source`` walked straight past it to the boot disk and
    handed back its identity to be recorded as the library's. That is verbatim
    the defect the guard was written for, reachable through the fix for it.
    """
    from cratekit.core import preflight

    leftover = volumes_directory.eject("EP_LIBRARY")
    (leftover / "Music" / "a" / "b").mkdir(parents=True, exist_ok=True)
    root = leftover / gap if gap else leftover
    boot = preflight.containing_mount(root)

    # The shape: the directory IS there, and it is not a mount.
    assert leftover.is_dir()
    assert boot != leftover

    assert preflight.identity_source(root) is None, "the boot disk was offered"
    assert preflight.root_can_be_created(root) is False

    wizard = setup_verb._Wizard({}, silent())
    with pytest.raises(CratekitError) as excinfo:
        setup_verb._resolve_volume_id(
            wizard, str(root), None, probes(identity_provider=lambda _p: "BOOT-DISK")
        )
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE


def test_the_identity_source_refuses_an_empty_mount_slot_and_nothing_else(
    tmp_path, volumes_directory
):
    """The rule itself, over every shape that matters.

    NEITHER DEPTH NOR ABSENCE IS ONE OF THEM, and each was a defect in turn: a
    rule counting levels refused a library two directories under an attached
    volume, and a rule about the missing directory accepted a mount point an
    ejected volume left behind.
    """
    from cratekit.core import preflight

    existing = tmp_path / "library"
    existing.mkdir()
    # No mount slot on the way down. It exists: the identity is the volume it
    # is on.
    #
    # WHAT IS ASSERTED IS THE PROPERTY, NOT THE CALL. This read
    # ``identity_source(x) == containing_mount(...)`` and ``identity_source``'s
    # accept leg IS ``return containing_mount(resolved)``, so the assertion was
    # the implementation restated and pinned only "it did not refuse". A literal
    # path is not portable, since the mount holding a temporary directory is
    # ``/`` on one machine and a tmpfs on another, so the three facts that make
    # an answer usable are stated instead: it is an answer, it is a real mount
    # point, and it holds the path asked about. A mutation returning the path
    # itself, its parent, or a fixed string fails all three.
    source = preflight.identity_source(existing)
    assert source is not None
    assert os.path.ismount(source), "an identity may only be read from a mount"
    assert source == existing or source in existing.parents
    # Still no mount slot, and any depth of ordinary missing directory: it would
    # be created on the volume its parent is already on.
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
    """Linux declares ``<media>/<label>`` AND ``<media>/<user>/<label>``.

    So one real path matches two rows, and only one of them is where the volume
    actually is. A rule consulting a single slot has to pick which, and both
    choices are wrong for one of the two mounters: the deepest match refuses a
    healthy volume mounted at the shallow row with an ordinary subdirectory under
    it, and the shallowest refuses a healthy per-user mount. Every slot is asked,
    and one mounted slot is enough.
    """
    from cratekit.core import preflight

    media = (tmp_path / "media").resolve()
    mount = media / "phil" / "EP_LIBRARY"
    mount.mkdir(parents=True)
    monkeypatch.setattr(
        preflight, "volume_mount_locations", lambda: ((media, 1), (media, 2))
    )
    monkeypatch.setattr(preflight, "is_mount_point", lambda path: Path(path) == mount)

    assert preflight.mount_location_ancestors(mount / "library") == (
        mount,
        media / "phil",
    )
    # The shallow slot is an ordinary directory the automounter made, and the
    # deep one is the volume. Accepted.
    assert preflight.identity_source(mount / "library") is not None
    # And the mirror image: the volume at the SHALLOW slot, with an ordinary
    # subdirectory below it that matches the deep row.
    monkeypatch.setattr(preflight, "is_mount_point", lambda path: Path(path) == media / "phil")
    assert preflight.identity_source(media / "phil" / "sub" / "library") is not None


# ── an OK detail may claim only what the run established ────────────────────


def test_no_ok_detail_claims_a_volume_the_run_never_identified(configured):
    """BLOCKING. Two greens asserting a disk nobody looked at.

    Both are reached through the leg of the reachability rule whose entire
    meaning is that the identity could not be ASKED, and on a machine with no
    identity adapter they appeared on the same report as ``library.identity``
    failing with "reports no volume identity". The pre-fix details claimed
    nothing at all, so this was a claim ADDED by the round that exists to remove
    exactly those.
    """
    from cratekit.core import preflight

    seed_taxonomy(configured)
    report = doctor.run(
        configured, probes=probes(identity_provider=preflight.null_volume_identity)
    )

    assert find(report, "library.identity").status is doctor.Status.FAIL
    for key in ("taxonomy.active", "session.unresolved"):
        finding = find(report, key)
        assert finding.status is doctor.Status.OK, finding.detail
        assert "recorded library volume" not in finding.detail, finding.detail
        assert "could not be compared" in finding.detail


def test_the_strong_claim_survives_where_the_identity_really_was_compared(configured):
    seed_taxonomy(configured)
    report = doctor.run(configured, probes=probes())
    for key in ("taxonomy.active", "session.unresolved"):
        assert "on the recorded library volume" in find(report, key).detail


# ── the credential store and its index never disagree ───────────────────────


def _refuse_the_index_lock(monkeypatch):
    """Make the presence index unlockable, the way a read-only state root does."""
    import os as os_module

    real_open = os_module.open

    def refuse(path, *args, **kwargs):
        if str(path).endswith("credential_index.lock"):
            raise PermissionError("no")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(os_module, "open", refuse)


def test_a_refused_index_lock_leaves_the_keychain_untouched_on_a_record(
    monkeypatch,
):
    """BLOCKING. The lock's own refusal reintroduced the lie it was added to fix.

    Taken AFTER the keychain write, an unobtainable lock refused a write that had
    already happened: the keychain held the value, the index did not name it,
    ``exists`` answered False, and doctor sent the user to record a credential
    the machine already had. The lock is taken first now, so a refusal means
    nothing changed anywhere.
    """
    _refuse_the_index_lock(monkeypatch)

    with pytest.raises(secrets.CredentialIndexUnusable) as excinfo:
        secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")

    assert "NOTHING WAS CHANGED" in str(excinfo.value)
    assert not secrets.exists(secrets.Credential.IDENTIFY_KEY)
    with pytest.raises(secrets.CredentialMissing):
        secrets.get(secrets.Credential.IDENTIFY_KEY)


def test_a_refused_index_lock_leaves_the_keychain_untouched_on_a_delete(monkeypatch):
    """The other direction, which was the one that made doctor report green.

    The keychain entry was removed first and the index write then failed, so
    ``exists`` answered TRUE for a credential that was gone and doctor reported a
    green credential over nothing.
    """
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")
    _refuse_the_index_lock(monkeypatch)

    with pytest.raises(secrets.CredentialIndexUnusable):
        secrets.delete(secrets.Credential.IDENTIFY_KEY)

    assert secrets.exists(secrets.Credential.IDENTIFY_KEY)
    assert secrets.get(secrets.Credential.IDENTIFY_KEY) == "value-from-the-user"


def test_a_delete_that_fails_between_the_two_stores_never_reports_green(monkeypatch):
    """The index entry goes first, so the surviving disagreement is the safe one.

    Index absent with a keychain entry still there reads as work to do, and
    re-recording is idempotent. The reverse reads as work already done, over a
    credential that is gone.
    """
    secrets.set(secrets.Credential.IDENTIFY_KEY, "value-from-the-user")

    import keyring

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
def test_a_hook_whose_configuration_name_needed_quoting_still_passes(
    library, tmp_path, filename
):
    """``pre_commit`` builds that line with ``shlex.join``, which QUOTES.

    A greedy match over non-space characters therefore stopped at the space and
    reported "the configuration it names, my, does not exist", so doctor exited
    30 for a developer whose hook was installed and working. Built here with the
    real ``shlex.join`` rather than with a hand-written string, because the
    hand-written string is what agreed with the regex.
    """
    import shlex

    checkout = tmp_path / "checkout"
    (checkout / ".git" / "hooks").mkdir(parents=True)
    (checkout / filename).write_text("repos: []\n")
    args = shlex.join(
        ["hook-impl", f"--config={filename}", "--hook-type=pre-commit"]
    )
    (checkout / ".git" / "hooks" / "pre-commit").write_text(
        f"#!/usr/bin/env bash\nARGS=({args})\nexec pre-commit \"${{ARGS[@]}}\"\n"
    )

    finding = hook_finding(library, checkout)
    assert finding.status is doctor.Status.OK, finding.detail
    assert filename in finding.detail, "the detail names a file it did not check"


def test_the_hook_ok_names_the_configuration_it_actually_resolved(library, tmp_path):
    """It interpolated the DEFAULT name whatever the hook said."""
    checkout = hooked_checkout(
        tmp_path / "checkout",
        "ARGS=(hook-impl --config=tools/hooks.yaml --hook-type=pre-commit)\n",
        config_file=False,
    )
    (checkout / "tools").mkdir()
    (checkout / "tools" / "hooks.yaml").write_text("repos: []\n")

    finding = hook_finding(library, checkout)
    assert finding.status is doctor.Status.OK, finding.detail
    assert "tools/hooks.yaml" in finding.detail
    assert ".pre-commit-config.yaml" not in finding.detail


# ── two partial tables over one key space ───────────────────────────────────


def test_the_two_remote_tables_never_answer_for_the_same_type():
    """Every other table in this module is total over a closed enum and asserted.

    These two are partial by necessity, since rclone's provider list is not ours
    to close, so what can be asserted instead is that they do not overlap: one
    type answering in both is one type with two answers, and which one wins is
    the order the branches happen to be written in.
    """
    overlap = set(doctor._REMOTE_TRASH_POLICY) & doctor._NON_TRASHING_REMOTE_TYPES
    assert not overlap, overlap
    for kind, policy in doctor._REMOTE_TRASH_POLICY.items():
        assert policy.option is None or policy.disabled in ("true", "false"), kind
        # A gate on an option that does not exist is a gate on nothing.
        assert policy.applies_when is None or policy.option is not None, kind


# ── the write refusals, driven rather than read off the table ────────────────


def test_the_wizard_refuses_to_write_when_the_volume_is_not_mounted_at_all(
    configured, tmp_path
):
    """NOT_MOUNTED, behaviourally. The table said never and nothing drove it.

    Mutation testing found this: ``foreign_volume`` was covered by a real drive
    and these two were covered only by the structural assertion, so a table row
    flipped to yes would have been caught for one state and not for the others.
    The state needs three things at once, an absent root, an identity that does
    not match, and the recorded volume nowhere in the mount table, which is why
    it is worth building rather than assuming.
    """
    from cratekit.core import preflight

    configured.library.root.rename(tmp_path / "detached")
    machine = probes(
        identity_provider=lambda _p: "0000-0000", mount_enumerator=lambda: ()
    )
    status = preflight.resolve_mount_state(
        configured.library.root,
        configured.library.volume_id,
        identity_provider=machine.identity_provider,
        mount_enumerator=machine.mount_enumerator,
    )
    assert status.state is preflight.MountState.NOT_MOUNTED

    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, configured, machine)

    assert wizard.notes[0].status is doctor.Status.FAIL
    assert wizard.notes[0].remedy is Remedy.MOUNT_LIBRARY_VOLUME
    assert not config.state_path("taxonomy_active", configured).exists()
    assert not configured.library.root.exists(), "the refusal created the root anyway"


def test_the_wizard_refuses_to_write_when_the_volume_is_mounted_somewhere_else(
    configured, tmp_path
):
    """MOUNTED_ELSEWHERE, behaviourally, and this is the leftover mount point.

    The drive IS attached, at another path, so the configured root is a directory
    on some other filesystem. Writing there is what creates a directory at a
    mount point, which on macOS sends the real volume to ``<name> 1`` on its next
    attach, permanently.
    """
    from cratekit.core import preflight

    elsewhere = tmp_path / "actually-here"
    elsewhere.mkdir()
    machine = probes(
        identity_provider=lambda path: VOLUME if path == elsewhere else "0000-0000",
        mount_enumerator=lambda: (elsewhere,),
    )
    status = preflight.resolve_mount_state(
        configured.library.root,
        configured.library.volume_id,
        identity_provider=machine.identity_provider,
        mount_enumerator=machine.mount_enumerator,
    )
    assert status.state is preflight.MountState.MOUNTED_ELSEWHERE

    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, configured, machine)

    assert wizard.notes[0].status is doctor.Status.FAIL
    assert not config.state_path("taxonomy_active", configured).exists()
    assert not (configured.library.root / configured.library.state_dirname).exists()


def test_the_zip_backed_shape_of_a_missing_packaged_directory_is_also_caught(
    monkeypatch, tmp_path
):
    """"Never raises" has to be true of every backend, not of the common one.

    ``importlib.resources`` does not promise one exception family. A filesystem
    traversable raises FileNotFoundError or NotADirectoryError, both OSError; a
    zip-backed one raises ``ValueError("Can't listdir a file")``, which is not.
    Catching one family and documenting the other is the overclaim this unit
    keeps shipping, so the guard is driven against a traversable that raises the
    one that is not an OSError.
    """
    from cratekit.core import taxonomy as taxonomy_module

    class ZipBacked:
        name = "templates"

        def __truediv__(self, _other):
            return self

        def iterdir(self):
            raise ValueError("Can't listdir a file")

    class _Zip:
        def files(self, _package):
            return ZipBacked()

    monkeypatch.setattr(taxonomy_module, "resources", _Zip())
    assert taxonomy_module.shipped_template_names() == ()
    assert drive(["--help"])[0] == int(ExitCode.OK)


def test_the_presence_index_has_no_locking_helper_left_to_deadlock_on():
    """Dead code that is also a footgun.

    ``set`` and ``delete`` hold the lock across their whole operation now, so the
    two wrappers that took it themselves have no callers, and calling either from
    inside a held cycle self-deadlocks: ``flock`` is per open file description,
    and a second acquisition blocks against the first. The non-locking halves
    stay, and their docstrings say who holds the lock for them.
    """
    assert not hasattr(secrets, "_index_add")
    assert not hasattr(secrets, "_index_remove")
    assert hasattr(secrets, "_record_name") and hasattr(secrets, "_forget_name")


# ── a check that cannot answer says so, and the report survives it ───────────


def test_a_check_whose_probe_raises_becomes_a_failed_check_not_a_lost_report(
    configured, tmp_path
):
    """BLOCKING. ``run`` documented "never raise" and nothing made it true.

    Three of these checks reach the outside world through calls that raise on an
    ordinary broken machine rather than returning a value, and one raising took
    the ENTIRE report down: every other answer, on the machine the module's own
    opening argument says the report exists for.

    THE REMEDY THIS ASSERTS CHANGED IN ROUND SIX, and the test's purpose did not.
    What it exists for is that an unstructured break becomes a FAILED CHECK
    rather than a lost report, and both legs below still assert exactly that. What
    it used to assert beside it was that a permission the operating system refused
    carries report-defect, which pinned the defect this unit was sent back for
    three rounds running: doctor told the user their own filesystem permission was
    a Cratekit bug, on the same page where the wizard told them it was not.

    THE REFUSAL IS REAL IN ROUND SEVEN. It was a hand-built
    ``PermissionError(13)`` with no filename on it, and the sentence the product
    then rendered told the reader to grant access to "the path named below" with
    nothing below it. A refusal with no path is now not claimed as one, which is
    what made this leg fail until it drove a real directory with mode 0o000.
    """
    sealed = tmp_path / "sealed"
    sealed.mkdir()
    inside = sealed / "inside"
    inside.write_text("x")
    sealed.chmod(0o000)

    def blind():
        inside.read_text()

    try:
        report = doctor.run(configured, probes=probes(process_lister=blind))
    finally:
        sealed.chmod(0o700)

    # Every check still answered, in order.
    assert [f.key for f in report.findings] == list(doctor.CHECK_KEYS)
    broken = find(report, "rekordbox.closed")
    assert broken.status is doctor.Status.FAIL, "unknown was reported as healthy"
    assert "did not complete" in broken.detail
    assert "PermissionError" in broken.detail
    assert broken.remedy is Remedy.GRANT_PATH_ACCESS
    assert "rather than a defect in this program" in broken.detail
    assert str(inside) in broken.detail, "a permission with no path to grant is unactionable"
    # And the answers either side of it are the real ones rather than casualties.
    assert find(report, "interpreter.version").status is doctor.Status.OK
    assert find(report, "library.identity").status is doctor.Status.OK

    # THE DEFECT LEG IS STILL A DEFECT. Classifying the permission out of the
    # blanket must not classify everything out of it: a probe that simply fell
    # over is an unanticipated failure and report-defect is the honest answer.
    def fell_over():
        raise RuntimeError("psutil returned a shape this reader has never seen")

    ordinary = find(
        doctor.run(configured, probes=probes(process_lister=fell_over)),
        "rekordbox.closed",
    )
    assert ordinary.status is doctor.Status.FAIL
    assert ordinary.remedy is Remedy.REPORT_DEFECT


def test_the_rescue_reports_a_broken_check_as_FAIL_rather_than_as_a_note(configured):
    """The half that carries the weight, and the easy thing to get wrong.

    INFO means "worth knowing, nothing to do now", and a check that did not
    complete has not established that there is nothing to do. A rescue that
    filed one under INFO would leave ``report.ok`` true and doctor exiting 0 over
    a question nobody answered, which is this unit's own defining defect wearing
    a handler.
    """

    def explode(_inputs):
        raise RuntimeError("the probe fell over")

    finding = doctor.answer(doctor.Check("made.up", explode), object())
    assert finding.status is doctor.Status.FAIL
    assert doctor.Report((finding,)).ok is False


def test_a_library_root_this_account_cannot_traverse_is_reported_not_raised(
    tmp_path, monkeypatch
):
    """The realistic shape of the above, and it needs no injected seam at all.

    ``Path.exists`` and ``Path.is_dir`` re-raise a permission error rather than
    answering False, so a library root under a directory this account cannot
    traverse arrives inside ``resolve_mount_state`` as an exception. Driven
    against a real unreadable directory rather than a stub.
    """
    sealed = tmp_path / "sealed"
    root = sealed / "library"
    root.mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(document_for(root))
    assert cfg.library.root == root, "the environment override moved the root"

    sealed.chmod(0o000)
    try:
        report = doctor.run(cfg, probes=probes())
    finally:
        sealed.chmod(0o755)

    assert [f.key for f in report.findings] == list(doctor.CHECK_KEYS)
    assert report.ok is False
    mounted = find(report, "library.mounted")
    assert mounted.status is doctor.Status.FAIL
    assert "did not complete" in mounted.detail

    # AND NOT ONE FAILING CHECK IN THE WHOLE REPORT CALLS IT A DEFECT. This is
    # the measurement that matters, taken on a REAL directory with mode 0o000
    # rather than on a fixture raising a synthetic error: four checks at once
    # came out of this arrangement saying "this is a defect; report it" over one
    # permission, and the wizard's own note in the same envelope said the
    # opposite. One report may not answer one condition two ways.
    for finding in report.failures:
        assert finding.remedy is not Remedy.REPORT_DEFECT, finding.key
    assert find(report, "library.identity").remedy is Remedy.GRANT_PATH_ACCESS
    assert find(report, "taxonomy.active").remedy is Remedy.GRANT_PATH_ACCESS


def test_a_session_log_this_account_cannot_traverse_is_not_an_empty_one(
    configured, tmp_path
):
    """"There are no sessions" is a claim, and this could not look.

    The guard reached the untraversable directory through ``Path.exists``, which
    raises rather than answering, so the whole report was lost. Answering False
    instead would be worse: it reads as a library that has never opened a
    session, and the next destructive run refuses on records this said were not
    there.

    THIS ASSERTS THE CHECK'S OWN ANSWER, not the rescue's, and the distinction is
    why the test is written this way. ``doctor.answer`` turns any exception into
    a failed check, so a version of this test that only asked for FAIL passed
    with the handler removed: the blanket rescue was answering for it. Found by
    mutation, on a guard added in this same round. What the user needs is the
    sentence naming the directory and the remedy that goes with it, so that is
    what is asserted.
    """
    directory = session.log_dir(configured)
    directory.mkdir(parents=True, exist_ok=True)
    directory.parent.chmod(0o000)
    try:
        report = doctor.run(configured, probes=probes())
    finally:
        directory.parent.chmod(0o755)

    finding = find(report, "session.unresolved")
    assert finding.status is doctor.Status.FAIL
    assert "none of them open" not in finding.detail
    assert "cannot be listed by this account" in finding.detail
    assert str(directory) in finding.detail
    assert "did not complete" not in finding.detail, "the blanket rescue answered"
    assert finding.remedy is Remedy.REPORT_DEFECT


# ── present and unreadable is not the same answer as absent ──────────────────


def test_a_commit_hook_that_exists_and_cannot_be_read_is_not_a_missing_hook(
    configured, tmp_path
):
    """One handler over both said "no pre-commit hook at X" for a file at X.

    And it sent the user to ``pre-commit install``, which rewrites a file it may
    not be able to open either. Git runs the hook regardless of whether this
    check can read it, so whether the scan happens is genuinely unknown.
    """
    root = tmp_path / "checkout"
    (root / ".git" / "hooks").mkdir(parents=True)
    hook = root / ".git" / "hooks" / "pre-commit"
    hook.write_text("exec pre-commit hook-impl --hook-type=pre-commit\n")
    (root / ".pre-commit-config.yaml").write_text("repos: []\n")

    hook.chmod(0o000)
    try:
        unreadable = find(
            doctor.run(configured, probes=probes(checkout_root=lambda: root)),
            "repo.commit_hook",
        )
    finally:
        hook.chmod(0o644)
    hook.unlink()
    absent = find(
        doctor.run(configured, probes=probes(checkout_root=lambda: root)),
        "repo.commit_hook",
    )

    assert unreadable.status is absent.status is doctor.Status.FAIL
    assert unreadable.detail != absent.detail, "one sentence for two conditions"
    assert "could not be read" in unreadable.detail
    assert "unknown rather than no" in unreadable.detail
    # The hook was refused by the operating system, so the act is to grant access
    # rather than to file a defect about somebody else's file permissions.
    assert unreadable.remedy is Remedy.GRANT_PATH_ACCESS
    assert "did not complete" not in unreadable.detail, "the blanket rescue answered"
    # The same claim the taxonomy check had to drop: an untraversable hooks
    # directory raises this too, and nothing beneath it was observed.
    assert "exists at" not in unreadable.detail
    assert "no pre-commit hook" in absent.detail


def test_an_active_template_that_exists_and_cannot_be_read_is_not_a_missing_one(
    configured
):
    """Same shape, and this one looped.

    "No active taxonomy template at X" carried run-setup, and setup leaves an
    existing copy alone, so the user re-runs it forever against a file that is
    there and unreadable.
    """
    seed_taxonomy(configured)
    path = config.state_path("taxonomy_active", configured)

    path.chmod(0o000)
    try:
        unreadable = find(doctor.run(configured, probes=probes()), "taxonomy.active")
    finally:
        path.chmod(0o644)
    path.unlink()
    absent = find(doctor.run(configured, probes=probes()), "taxonomy.active")

    assert unreadable.status is absent.status is doctor.Status.FAIL
    assert "could not be read" in unreadable.detail
    assert unreadable.remedy is not Remedy.RUN_SETUP
    # AND THE ACT IS THE ONE THE USER CAN PERFORM. The sentence names a
    # permission as one of the two shapes this handler catches, and the token
    # beside it said "report a defect" for both. This file was refused by the
    # operating system, so the answer is to grant access to it.
    assert unreadable.remedy is Remedy.GRANT_PATH_ACCESS
    assert "did not complete" not in unreadable.detail, "the blanket rescue answered"
    # AND IT DOES NOT CLAIM THE FILE IS THERE. The same handler catches the
    # permission error an untraversable PARENT raises, and nothing under such a
    # parent was observed at all, so "exists and could not be read" was a second
    # claim about something nobody looked at.
    assert "exists and could not be read" not in unreadable.detail
    assert "whether the file is even there is unknown" in unreadable.detail.lower()
    assert "no active taxonomy template" in absent.detail
    assert absent.remedy is Remedy.RUN_SETUP


def test_an_unlistable_packaged_directory_is_not_a_shipped_set_of_none(
    configured, unreadable_install
):
    """BLOCKING. The empty tuple was serving as two different answers.

    The walk swallows an unreadable packaged directory so that building the
    command tree cannot die on a partial install, which is right. Reading the
    resulting emptiness as a fact about the SHIPPED SET is not: doctor told a
    user with a damaged install that their configuration named a template nothing
    ships, and sent them to re-run setup, which cannot repair packaged data.
    """
    from cratekit.core import taxonomy as taxonomy_module

    names, problem = taxonomy_module.shipped_templates()
    assert names == ()
    assert problem is not None and "could not be listed" in problem
    # The parser-facing half is unchanged, because a parser only ever wanted a
    # list of choices and an exception there takes every verb down.
    assert taxonomy_module.shipped_template_names() == ()

    finding = find(doctor.run(configured, probes=probes()), "taxonomy.active")
    assert finding.status is doctor.Status.FAIL
    assert "no template ships under that name" not in finding.detail
    assert "not established" in finding.detail
    assert finding.remedy is not Remedy.RUN_SETUP


def test_a_readable_packaged_directory_reports_no_problem_at_all(configured):
    """The other direction, because a problem that is always set is not a signal."""
    from cratekit.core import taxonomy as taxonomy_module

    names, problem = taxonomy_module.shipped_templates()
    assert problem is None
    assert "default" in names
    seed_taxonomy(configured)
    assert find(doctor.run(configured, probes=probes()), "taxonomy.active").status is (
        doctor.Status.OK
    )


# ── the write leg of the reachability rule, driven in BOTH directions ────────


def test_a_first_run_into_an_empty_mount_slot_may_not_write_library_state(
    volumes_directory
):
    """``IF_ROOT_CAN_BE_CREATED`` had no refusing case anywhere in the suite.

    Only its permitting case was driven, so the condition could have been the
    constant True and the whole table would still have passed. The refusal is the
    half that matters: a first run with the drive unplugged must not create the
    library root, because on macOS a directory at an empty mount point sends the
    real volume to ``<name> 1`` on its next attach, permanently.
    """
    from cratekit.core import preflight

    for root in (
        volumes_directory / "NOT_ATTACHED" / "library",       # absent slot
        volumes_directory.eject("EJECTED") / "library",       # leftover slot
    ):
        assert preflight.root_can_be_created(root) is False
        for state in (
            preflight.MountState.IDENTITY_UNAVAILABLE,
            preflight.MountState.IDENTITY_NOT_RECORDED,
        ):
            status = preflight.MountStatus(state=state, configured_root=root)
            assert preflight.library_state_may_be_written(status) is False
            assert preflight.library_state_is_readable(status) is False

    attached = volumes_directory.attach("ATTACHED")
    assert preflight.root_can_be_created(attached / "library") is True


def test_the_mount_location_table_is_resolved_so_a_symlink_cannot_disarm_it(monkeypatch):
    """A guard that silently matches nothing is a guard that is not there.

    Every path this is compared against is resolved, so one unresolved row makes
    ``relative_to`` raise and the whole rule fall through to "nothing to refuse",
    with no symptom. It is exactly what happened on a machine whose temporary
    directory is reached through a symlink.
    """
    from cratekit.core import preflight

    monkeypatch.setattr(
        preflight, "_VOLUME_MOUNT_LOCATIONS", {sys.platform: (("/tmp", 1),)}
    )
    rows = preflight.volume_mount_locations()
    assert rows == ((Path("/tmp").resolve(), 1),)
    assert all(row[0] == row[0].resolve() for row in rows)


def test_where_each_platform_mounts_a_volume_is_declared_row_by_row():
    """The table itself, spelled out, because every other test replaces it.

    Found by mutation: the shipped rows could be changed to an absurd directory
    at an absurd depth with the whole suite still green, because the fixture that
    drives this rule injects its own table on every test that touches it. That is
    the shape of a tuning constant nothing covers, and the answer is the one the
    reachability tables already use: write the declaration out in a test, so a
    change has to be made in two places and the second is one a reviewer reads.

    It is a claim about operating systems rather than about this code, so what it
    pins is that somebody edited it deliberately.
    """
    from cratekit.core import preflight

    assert dict(preflight._VOLUME_MOUNT_LOCATIONS) == {
        # An external volume mounts one level under this directory.
        "darwin": (("/Volumes", 1),),
        # The removable-media mounters, and NOT ``/mnt``. Every row is a claim
        # that an empty directory there is evidence of an absent volume, which
        # holds for a location a mounter creates and removes around a mount and
        # is false for the spot the hierarchy standard reserves for mounting by
        # hand. With ``/mnt`` present, an ordinary Linux library at
        # ``/mnt/<name>/music`` could never have its active template written, on a
        # platform that records no identity to protect in the first place.
        "linux": (("/media", 1), ("/media", 2), ("/run/media", 2)),
    }
    assert ("/mnt", 1) not in preflight._VOLUME_MOUNT_LOCATIONS["linux"]
    # And no other platform has one, which is a REFUSAL TO GUESS rather than a
    # claim that no volume mounts there. Windows resolves an identity provider
    # and has no row, so the derive refuses nothing on it: recorded as a residual
    # rather than fixed by inventing a shape nobody here can drive.
    assert "win32" not in preflight._VOLUME_MOUNT_LOCATIONS


# ═══════════════════════════════════════════════════════════════════════════
# 9. Round five: the guard that answers about something it did not observe
# ═══════════════════════════════════════════════════════════════════════════
#
# One defect, five shapes, four rounds. A rule that decides identity from
# something that is not identity, or a check that answers about something it
# never looked at. Everything below drives BOTH directions, because the two
# previous corrections in this file were each a refusal that also refused a
# correct install.


def _case_insensitive(directory: Path) -> bool:
    """Whether ``directory`` lives on a filesystem that folds case.

    Asked of the real directory rather than of ``sys.platform``, because the
    answer is a property of the VOLUME: the default macOS boot volume folds case
    and a macOS volume formatted case-sensitively does not, and both run this
    suite. The tests below assert the right thing for whichever they got, so
    neither leg is ever skipped into silence.
    """
    probe = directory / "CaseProbe"
    probe.mkdir()
    return (directory / "caseprobe").is_dir()


def test_a_differently_cased_spelling_of_the_mount_directory_does_not_disarm_the_rule(
    tmp_path,
):
    """BLOCKING. The whole guard turned off by a shell that lower-cased a path.

    ``Path.relative_to`` compares path PARTS, which is case sensitive, and the
    default macOS boot volume is case INSENSITIVE. So ``/volumes/NAME/Music`` and
    ``/Volumes/NAME/Music`` name one directory to every filesystem call and two
    different things to the rule: the canonical spelling refused with the drive
    detached and the lower-cased one recorded the BOOT DISK'S UUID as the
    library's identity, for the life of that library, and every destructive
    verb's precondition then passed against the disk holding the operating
    system.

    Both directions are asserted, on whichever filesystem this ran on, because
    making the comparison blindly case insensitive would be the mirror defect: on
    a case-sensitive volume the two spellings really are two directories, and
    conflating them would refuse a path that has nothing to do with any mount.
    """
    from cratekit.core import preflight

    volumes = (tmp_path / "Volumes").resolve()
    volumes.mkdir()
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

    # And a genuinely different directory is never conflated with the row, on
    # either kind of filesystem.
    other = tmp_path / "VolumesElsewhere"
    other.mkdir()
    assert preflight._is_a_volume_mount_location(other / "EP", rows) is False


def test_two_spellings_of_one_directory_are_one_directory_however_they_differ(tmp_path):
    """The property underneath the case test, driven on every filesystem.

    Case folding is one way two strings name one directory and a symlink is
    another, and both were invisible to a comparison over path parts. The
    filesystem answers with ``(st_dev, st_ino)``, so this pins the comparison
    itself rather than one platform's spelling of it.
    """
    from cratekit.core import preflight

    real = tmp_path / "Volumes"
    real.mkdir()
    link = tmp_path / "linked-volumes"
    link.symlink_to(real, target_is_directory=True)

    assert preflight._names_one_path(real, real) is True
    assert preflight._names_one_path(link, real) is True
    assert preflight._is_a_volume_mount_location(link / "EP", ((real, 1),)) is True

    apart = tmp_path / "other"
    apart.mkdir()
    assert preflight._names_one_path(apart, real) is False
    # Neither side exists, so nothing can be compared. False is the ACCEPTING
    # direction here and it is what the parts comparison answered too.
    assert preflight._names_one_path(tmp_path / "a", tmp_path / "b") is False

    # AND IT IS THE FILESYSTEM'S ANSWER RATHER THAN A NAME COMPARISON, which is
    # what makes it right on a case-SENSITIVE volume as well as on a folding one.
    # Two directories the filesystem calls different stay different here whatever
    # their names spell, which no amount of lower-casing could promise.
    for left, right in ((real, real), (link, real), (apart, real), (real, apart)):
        assert preflight._names_one_path(left, right) is os.path.samefile(left, right)


def test_a_symlinked_mount_point_pointing_out_of_the_mount_directory_still_refuses(
    volumes_directory, tmp_path
):
    """The case-folding consequence, reached by a second route.

    ``mount_location_ancestors`` resolved the path before asking about slots, so
    a symlink standing in the mount directory and aimed at an ordinary directory
    elsewhere produced no slot at all, the walk fell through to the boot disk,
    and its identity was handed back to be recorded as the library's. The symlink
    is not harmless scenery either: it occupies the mount point permanently, so a
    volume of that name attaches at ``<name> 1`` instead, forever.
    """
    from cratekit.core import preflight

    elsewhere = tmp_path / "elsewhere"
    (elsewhere / "library").mkdir(parents=True)
    (volumes_directory.path / "SYMVOL").symlink_to(elsewhere, target_is_directory=True)

    root = volumes_directory / "SYMVOL" / "library"
    assert preflight.mount_location_ancestors(root) == (volumes_directory / "SYMVOL",)
    assert preflight.identity_source(root) is None
    assert preflight.root_can_be_created(root) is False

    wizard = setup_verb._Wizard({}, silent())
    with pytest.raises(CratekitError) as excinfo:
        setup_verb._resolve_volume_id(
            wizard, str(root), None, probes(identity_provider=lambda _p: "BOOT-DISK")
        )
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE


def test_a_symlinked_mount_point_that_names_a_real_mount_is_still_a_mounted_volume(
    volumes_directory, tmp_path
):
    """The other half, and it is the ordinary macOS install.

    Every current macOS puts the BOOT volume's own entry in the mount directory
    as a symlink to ``/``, and a library under it really is on the mounted boot
    volume. ``os.path.ismount``
    answers False for a symlink by contract, so refusing on that alone would
    paint a correct setup red, which is the shape of guard people work around
    rather than fix (P7).
    """
    from cratekit.core import preflight

    attached = volumes_directory.attach("REAL")
    (attached / "Music").mkdir(parents=True)
    (volumes_directory.path / "ALIAS").symlink_to(attached, target_is_directory=True)

    alias_root = volumes_directory / "ALIAS" / "Music"
    assert preflight.slot_holds_a_volume(volumes_directory / "ALIAS") is True
    assert preflight.identity_source(alias_root) is not None
    assert preflight.root_can_be_created(alias_root) is True


def test_a_declared_mount_directory_absent_from_this_machine_still_names_itself(
    tmp_path, monkeypatch
):
    """ZERO DEATH. The equality shortcut in ``_names_one_path`` killed nothing.

    ``samefile`` compares two inodes, so it has to stat both sides, and a
    declared mount directory that is not on this machine has no inode. Without
    the shortcut in front of it the function answered "that is not the mount
    directory" about the mount directory's own spelling. ``/run/media`` is the
    udisks2 location and plenty of Linux installs do not have it, so a first run
    naming ``--library-root /run/media/<user>/<label>/Music`` with the drive
    detached found no slot to ask about at all, fell through to the boot disk and
    recorded its identity as the library's, permanently.

    Two DIFFERENT spellings of an absent directory answering False is the
    accepting direction and is deliberate. One directory answering False about
    itself is not.
    """
    from cratekit.core import preflight

    absent = tmp_path.resolve() / "run" / "media"
    assert not absent.exists()
    assert preflight._names_one_path(absent, absent) is True

    root = absent / "phil" / "EP_LIBRARY" / "Music"
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((absent, 2),))
    monkeypatch.setattr(preflight, "is_mount_point", lambda _path: False)
    assert preflight.mount_location_ancestors(root) == (absent / "phil" / "EP_LIBRARY",)
    assert preflight.identity_source(root) is None


def test_the_walk_up_to_an_ancestor_never_clamps_at_the_filesystem_root(tmp_path):
    """ZERO DEATH. The break that stops the walk running off the top killed nothing.

    ``Path('/').parent`` is ``Path('/')``, so without the break the walk stops
    moving and keeps counting, and the ancestor it ends on is the same path for
    every depth that overruns. One directory then answers to two different
    declared depths, which is the identity-that-is-not-unique defect in
    miniature: a match is supposed to mean "the declared directory is exactly
    this many levels up", and a clamped walk makes it mean "or fewer".
    """
    from cratekit.core import preflight

    anchor = Path(tmp_path.anchor)
    # Zero levels up from the mount directory IS the mount directory. One level
    # up from it is off the top of the filesystem, and that is not a match.
    assert preflight._is_a_volume_mount_location(anchor, ((anchor, 0),)) is True
    assert preflight._is_a_volume_mount_location(anchor, ((anchor, 1),)) is False
    assert preflight._is_a_volume_mount_location(anchor / "Volumes", ((anchor, 1),)) is True


def test_a_library_reached_through_a_symlinked_parent_still_finds_its_slot(
    volumes_directory, tmp_path
):
    """ZERO DEATH. Walking the RESOLVED chain killed nothing on its own.

    The sibling above covers the spelling GIVEN, where a symlink standing in the
    mount directory points out of it. This is the other direction and it is the
    ordinary convenience layout: a shortcut in the home directory aimed at the
    external volume, with the library named through the shortcut. Nothing on the
    given chain crosses a declared row, so the resolved chain is the only thing
    that finds the slot, and without it the drive being detached is invisible and
    the boot disk's identity is what gets recorded.
    """
    from cratekit.core import preflight

    shortcut = tmp_path / "EP_LIBRARY"
    shortcut.symlink_to(volumes_directory.path / "EXT", target_is_directory=True)
    root = shortcut / "Music"

    assert preflight.mount_location_ancestors(root) == (volumes_directory / "EXT",)
    assert preflight.identity_source(root) is None

    wizard = setup_verb._Wizard({}, silent())
    with pytest.raises(CratekitError) as excinfo:
        setup_verb._resolve_volume_id(
            wizard, str(root), None, probes(identity_provider=lambda _p: "BOOT-DISK")
        )
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE


def test_identity_source_asks_whether_the_slot_holds_a_volume_not_whether_it_is_one(
    tmp_path, monkeypatch
):
    """ZERO DEATH, and the reason is the guard-covered-by-a-guard shape again.

    ``identity_source`` asks :func:`slot_holds_a_volume` rather than
    :func:`is_mount_point`, and swapping it back killed nothing because the
    synthetic fixture answers ``is_mount_point`` by RESOLVING first, so the
    fixture was already doing the work the real seam does not. Only the real
    ``os.path.ismount`` shows the difference: it answers False for a symlink by
    contract, and every current macOS puts the boot volume's own entry in the
    mount directory as a symlink to ``/``. Asking the narrower question refuses
    that install, which is a guard firing on a correct setup (P7).
    """
    from cratekit.core import preflight

    volumes = (tmp_path / "Volumes").resolve()
    volumes.mkdir()
    (volumes / "ALIAS").symlink_to(Path(tmp_path.anchor), target_is_directory=True)
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((volumes, 1),))

    # The real seam, deliberately left alone.
    assert preflight.is_mount_point(volumes / "ALIAS") is False
    assert preflight.identity_source(volumes / "ALIAS" / "Music") is not None


def test_is_mount_point_is_the_one_fact_the_rule_turns_on_and_it_is_pinned(
    tmp_path, monkeypatch
):
    """BLOCKING. The seam the whole round-four rule stands on covered nothing.

    The full suite passed with the body replaced by ``return True`` AND with it
    replaced by ``return False``, because every test that drives the rule injects
    its own answer through the fixture and the no-slot cases short circuit before
    it is reached. ``return True`` accepts an ejected volume's leftover mount
    point, which is verbatim the defect round four exists to close.

    So the same remedy the mount-location TABLE already gets is applied to the
    SEAM beside it: what it delegates to is asserted, and the real function is
    driven against a directory that IS a mount point on this machine and one that
    is not. The filesystem root is a mount point on every platform this runs on,
    including Windows, where a drive root answers True.
    """
    from cratekit.core import preflight

    ordinary = tmp_path / "not-a-mount"
    ordinary.mkdir()

    # The real function, both directions. ``return True`` dies on the second
    # line and ``return False`` dies on the first.
    assert preflight.is_mount_point(Path(tmp_path.anchor)) is True
    assert preflight.is_mount_point(ordinary) is False
    # And absent or unstattable is False, which is the safe direction: the
    # caller's refusal is what stops an identity being read off the wrong disk.
    assert preflight.is_mount_point(tmp_path / "never-existed") is False

    # It is ``os.path.ismount`` and not a reimplementation of it, so a platform
    # that grows a new mount shape is answered by the standard library rather
    # than by a copy here.
    monkeypatch.setattr(os.path, "ismount", lambda path: str(path) == "sentinel")
    assert preflight.is_mount_point(Path("sentinel")) is True
    assert preflight.is_mount_point(Path(tmp_path.anchor)) is False


def test_a_linux_library_on_an_ordinary_directory_is_not_refused_forever(
    tmp_path, monkeypatch
):
    """OVER RESTRICTION. ``/mnt/<name>`` as a row produced a run-setup loop.

    Linux has no identity adapter, so every mount outcome there is
    ``IDENTITY_UNAVAILABLE`` and the write leg always goes through
    ``root_can_be_created``. With ``/mnt`` declared as a place a volume mounts, a
    library at ``/mnt/<name>/music`` on an ordinary root filesystem could never
    have its active template written: the wizard refused, doctor read for the
    template, found nothing, and answered ``taxonomy.active`` FAIL with
    run-setup. The user re-runs setup forever, which is the exact loop round four
    closed one function away in ``doctor.py``.

    ``--volume-id`` does not rescue it, because ``_seed_taxonomy`` asks the WRITE
    table rather than the identity, so the arrangement is driven with an identity
    already recorded.
    """
    from cratekit.core import preflight

    mnt = (tmp_path / "mnt").resolve()
    root = mnt / "data" / "music"
    root.mkdir(parents=True)
    media = (tmp_path / "media").resolve()
    (media / "phil" / "EP_LIBRARY").mkdir(parents=True)
    # The SHIPPED linux rows, rebased under the temporary directory, so this is
    # the table that ships rather than one invented for the test.
    rebased = tuple(
        ((tmp_path / directory.lstrip("/")).resolve(), depth)
        for directory, depth in preflight._VOLUME_MOUNT_LOCATIONS["linux"]
    )
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: rebased)
    monkeypatch.setattr(preflight, "is_mount_point", lambda path: False)

    assert preflight.mount_location_ancestors(root) == ()
    assert preflight.identity_source(root) is not None
    assert preflight.root_can_be_created(root) is True
    status = preflight.MountStatus(
        state=preflight.MountState.IDENTITY_UNAVAILABLE, configured_root=root
    )
    assert preflight.library_state_may_be_written(status) is True
    assert preflight.library_state_is_readable(status) is True

    # AND THE REFUSAL THAT MATTERS SURVIVES. A drive the automounter would put at
    # ``<media>/<user>/<label>`` is still refused while nothing is mounted there,
    # which is the arrangement the rule exists for.
    detached = media / "phil" / "EP_LIBRARY" / "Music"
    assert preflight.mount_location_ancestors(detached) != ()
    assert preflight.identity_source(detached) is None
    assert preflight.root_can_be_created(detached) is False


def test_the_wizard_writes_the_active_template_on_a_linux_style_ordinary_directory(
    tmp_path, monkeypatch
):
    """The loop, closed end to end rather than at the table.

    A refusal nobody can act on is worse than one nobody sees, and this one had
    no exit at all: the template is what makes a library self-describing, and
    doctor fails without it.
    """
    from cratekit.core import preflight

    root = (tmp_path / "mnt" / "data" / "music").resolve()
    (root / "Music").mkdir(parents=True)
    rebased = tuple(
        ((tmp_path / directory.lstrip("/")).resolve(), depth)
        for directory, depth in preflight._VOLUME_MOUNT_LOCATIONS["linux"]
    )
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: rebased)
    monkeypatch.setattr(preflight, "is_mount_point", lambda path: False)
    # A platform with no identity adapter, which is every platform that is not
    # macOS or Windows.
    monkeypatch.setattr(
        doctor, "Probes", lambda: probes(identity_provider=preflight.null_volume_identity)
    )

    code, out, err = drive(
        [
            "--output", "json", "setup",
            "--library-root", str(root),
            "--volume-id", VOLUME,
            "--db-path", str(root / "db" / "master.db"),
            "--staging", str(tmp_path / "staging"),
            "--profile", "slim",
            "--taxonomy", "default",
        ]
    )
    assert code != int(ExitCode.USAGE), err
    checks = {c["key"]: c for c in json.loads(out)["data"]["checks"]}
    assert checks["setup.taxonomy"]["status"] == "ok", checks["setup.taxonomy"]["detail"]
    config.reset_cache()
    assert config.state_path("taxonomy_active", config.load()).is_file()


def test_a_library_on_the_boot_disk_itself_is_not_refused(tmp_path):
    """The plainest legitimate arrangement, and every round has had to keep it.

    A library in a home directory crosses no declared mount location, so there is
    no slot to ask about, and the identity of whatever holds it is the identity
    it will keep. Accepted whether or not the directory exists yet, at any depth.
    """
    from cratekit.core import preflight

    here = tmp_path / "Music"
    here.mkdir()
    assert preflight.identity_source(here) is not None
    assert preflight.root_can_be_created(here) is True
    # A FIRST RUN: the root is not there yet and will be created on the volume
    # its parent is already on. "The root must exist" was correction one, and it
    # refused every first run.
    assert preflight.root_can_be_created(tmp_path / "not" / "yet" / "here") is True


def test_a_platform_with_no_declared_row_refuses_nothing(tmp_path, monkeypatch):
    """An empty table is "nothing to refuse", not "refuse everything".

    Inventing a location for a platform nobody has described would refuse
    ordinary paths on it. The gap for Windows specifically is item 1 of the residual
    finding "Five places where "I could not look" is still not said out loud".
    """
    from cratekit.core import preflight

    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ())
    monkeypatch.setattr(preflight, "is_mount_point", lambda path: False)
    assert preflight.mount_location_ancestors(tmp_path / "anything") == ()
    assert preflight.identity_source(tmp_path / "anything") is not None


# ── an unreadable .git marker is not a marker that names nothing ─────────────


def test_a_git_marker_that_cannot_be_read_is_not_a_marker_that_names_nothing(
    configured, tmp_path
):
    """BLOCKING, and doctor exited 0 over it.

    ``_git_dir`` returned None for an unreadable marker and for a marker that
    parsed and named no directory alike, and the caller rendered both as the
    second: INFO, no remedy, ``report.ok`` still True. Round four made exactly
    this split for the hook FILE two screens down and left the MARKER that leads
    to it, in the same check, in the same round.
    """
    root = tmp_path / "checkout"
    root.mkdir()
    marker = root / ".git"
    marker.write_text("gitdir: /somewhere/else\n")

    marker.chmod(0o000)
    try:
        pointed, unreadable, remedy = doctor._git_dir(root)
        report = doctor.run(configured, probes=probes(checkout_root=lambda: root))
    finally:
        marker.chmod(0o644)

    assert pointed is None
    assert unreadable is not None and str(marker) in unreadable
    finding = find(report, "repo.commit_hook")
    assert finding.status is doctor.Status.FAIL, finding.detail
    # AND THE ACT IS THE ONE THE USER CAN PERFORM. The marker was refused by the
    # operating system, which is a permission to grant and not a defect in this
    # program; report-defect over it is the same misclassification this whole
    # round is about, wearing a different check's name.
    assert remedy is Remedy.GRANT_PATH_ACCESS
    assert finding.remedy is Remedy.GRANT_PATH_ACCESS
    assert "unknown rather than no" in finding.detail
    assert "names no git directory" not in finding.detail
    assert report.ok is False, "doctor exited 0 over an unanswered commit scan"

    # AND THE QUIET ANSWER SURVIVES. A marker that WAS read and named nothing is
    # still INFO with no remedy: nothing is broken, there is simply no git
    # directory to look in.
    marker.write_text("this is not a gitdir pointer\n")
    named_nothing = find(
        doctor.run(configured, probes=probes(checkout_root=lambda: root)),
        "repo.commit_hook",
    )
    assert doctor._git_dir(root) == (None, None, None)

    # AND A MARKER THAT IS PRESENT AND IS NOT TEXT. ``UnicodeDecodeError`` is a
    # ``ValueError`` rather than an ``OSError``, so it escaped the handler beside
    # it and left the whole check as one that did not complete. Its own leg
    # killed no test until this line, which is the same shape as the split above.
    marker.write_bytes(b"gitdir: \xff\xfe/somewhere\n")
    pointed, not_text, not_text_remedy = doctor._git_dir(root)
    assert pointed is None
    assert not_text is not None and "not readable text" in not_text
    # The bytes were READ and then would not decode, so nothing was refused and
    # this leg keeps report-defect. The two legs of one handler answer two
    # different questions and must not borrow each other's act.
    assert not_text_remedy is Remedy.REPORT_DEFECT
    assert named_nothing.status is doctor.Status.INFO
    assert "names no git directory" in named_nothing.detail


def test_a_commondir_that_cannot_be_read_is_reported_rather_than_swallowed(
    configured, tmp_path
):
    """The second None in the same function, and it had a pragma over it.

    A worktree's per-tree directory names the COMMON one through ``commondir``,
    and a ``commondir`` this account cannot open left the caller reporting a
    worktree as having no git directory at all.
    """
    common = tmp_path / "main" / ".git"
    (common / "hooks").mkdir(parents=True)
    per_tree = common / "worktrees" / "w1"
    per_tree.mkdir(parents=True)
    commondir = per_tree / "commondir"
    commondir.write_text("../..\n")
    worktree = tmp_path / "w1"
    worktree.mkdir()
    (worktree / ".git").write_text(f"gitdir: {per_tree}\n")

    commondir.chmod(0o000)
    try:
        pointed, unreadable, remedy = doctor._git_dir(worktree)
        finding = find(
            doctor.run(configured, probes=probes(checkout_root=lambda: worktree)),
            "repo.commit_hook",
        )
    finally:
        commondir.chmod(0o644)

    assert pointed is None
    assert unreadable is not None and "commondir" in unreadable
    assert finding.status is doctor.Status.FAIL
    assert remedy is Remedy.GRANT_PATH_ACCESS
    assert finding.remedy is Remedy.GRANT_PATH_ACCESS


def test_a_commondir_that_is_present_and_is_not_text_is_reported_too(
    configured, tmp_path
):
    """THE OTHER MEMBER OF THE SAME TUPLE, and it was pinned by nothing.

    ``except (OSError, UnicodeDecodeError)`` has two members precisely because a
    ``UnicodeDecodeError`` is a ``ValueError`` and would otherwise escape the
    check entirely. Only the permission leg was ever driven, so dropping the
    second member killed no test and the claim that both were covered was false
    for this one. A ``commondir`` written by a damaged checkout, or by a tool
    that wrote a different encoding, is present and does not decode.
    """
    common = tmp_path / "main" / ".git"
    (common / "hooks").mkdir(parents=True)
    per_tree = common / "worktrees" / "w1"
    per_tree.mkdir(parents=True)
    (per_tree / "commondir").write_bytes(b"..\xff\xfe/..\n")
    worktree = tmp_path / "w1"
    worktree.mkdir()
    (worktree / ".git").write_text(f"gitdir: {per_tree}\n")

    pointed, unreadable, remedy = doctor._git_dir(worktree)
    finding = find(
        doctor.run(configured, probes=probes(checkout_root=lambda: worktree)),
        "repo.commit_hook",
    )

    assert pointed is None
    assert unreadable is not None and "commondir" in unreadable
    assert finding.status is doctor.Status.FAIL
    # Nothing was refused, so this half is a damaged checkout and keeps
    # report-defect. It is the leg the permission test above cannot reach.
    assert remedy is Remedy.REPORT_DEFECT
    assert finding.remedy is Remedy.REPORT_DEFECT
    assert "did not complete" not in finding.detail, "the blanket rescue answered"


# ── the wizard reports a damaged install as a damaged install ────────────────


def test_the_wizard_tells_an_unlistable_template_directory_from_an_absent_name(
    configured, unreadable_install
):
    """BLOCKING. The fourth handler of the collapse round four fixed three of.

    ``except (FileNotFoundError, OSError)`` is ONE clause over BOTH conditions,
    and the redundancy is the fingerprint: ``FileNotFoundError`` IS an
    ``OSError``. With the packaged directory unreadable, one ``crate setup``
    envelope carried "no shipped template is named 'default'; shipped: " from the
    wizard and "the packaged template directory could not be listed ... a damaged
    or partial install rather than a configuration error" from doctor, in the
    same report. The first contradicted the second, sent the user to change a
    configuration value that was correct, and printed an empty shipped set as a
    fact.
    """
    cfg = configured
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, cfg, probes())

    note = next(n for n in wizard.notes if n.key == "setup.taxonomy")
    assert note.status is doctor.Status.FAIL
    assert "could not be listed" in note.detail
    assert "damaged or partial install" in note.detail
    assert note.remedy is Remedy.REPORT_DEFECT
    assert "no shipped template is named" not in note.detail
    assert "shipped: " not in note.detail, "an empty set was printed as a fact"

    # And it AGREES with what doctor says about the same install, which is the
    # property the two answers failed on.
    doctor_finding = find(doctor.run(cfg, probes=probes()), "taxonomy.active")
    assert doctor_finding.remedy is note.remedy


def test_the_wizard_still_names_a_template_that_simply_does_not_ship(configured):
    """The other half. A listable set that does not hold the name is a config error.

    Splitting a handler is only right if both branches keep their own answer, and
    this is the one the user really can fix by choosing another value.
    """
    document = configured.to_toml_dict()
    document.setdefault("taxonomy", {})["template"] = "no-such-template"
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, config.from_dict(document), probes())

    note = next(n for n in wizard.notes if n.key == "setup.taxonomy")
    assert note.status is doctor.Status.FAIL
    assert "no shipped template is named 'no-such-template'" in note.detail
    assert "default" in note.detail, "the shipped set is named"
    assert note.remedy is Remedy.FIX_CONFIG_VALUES


def test_a_template_that_ships_and_will_not_open_is_a_damaged_install_too(
    configured, monkeypatch
):
    """The third condition the one handler was hiding.

    The name IS in the listed set and the packaged bytes will not open, so this
    is neither a wrong value nor an absent template. Re-running setup cannot
    repair a wheel, and that is the sentence the user gets.
    """
    def refuse(_name):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(setup_verb, "template_text", refuse)
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, configured, probes())

    note = next(n for n in wizard.notes if n.key == "setup.taxonomy")
    assert note.status is doctor.Status.FAIL
    assert "ships and its packaged text could not be read" in note.detail
    assert "damaged or partial install" in note.detail
    assert note.remedy is Remedy.REPORT_DEFECT

    # AND PACKAGED BYTES THAT ARE NOT TEXT, which is the same damaged install
    # arriving as a ``ValueError`` rather than an ``OSError``. Dropping
    # ``UnicodeDecodeError`` from the handler killed no test until this line, and
    # what it costs is the whole verb: the wizard would exit through the
    # dispatcher's blanket as an internal defect.
    def mojibake(_name):
        raise UnicodeDecodeError("utf-8", b"\xff\xfe", 0, 1, "invalid start byte")

    monkeypatch.setattr(setup_verb, "template_text", mojibake)
    second = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(second, configured, probes())

    note = next(n for n in second.notes if n.key == "setup.taxonomy")
    assert note.status is doctor.Status.FAIL
    assert "ships and its packaged text could not be read" in note.detail
    assert note.remedy is Remedy.REPORT_DEFECT


def test_the_status_verb_survives_a_state_directory_that_cannot_be_walked(monkeypatch):
    """ZERO DEATH, and item 1 of the residual finding "Two rescues that are kept
    without being covered" argued it could not be anything else.

    The argument was about the TRIGGER and it stands: measured on this
    interpreter, ``Path.glob`` swallows a ``PermissionError`` inside its own
    scandir walk and answers empty for a run directory somebody replaced with a
    plain file, so no arrangement of a real filesystem reaches the handler. What
    the argument does not excuse is leaving the CONTRACT unstated. The contract
    is that a walk which refuses costs the report its run records and not the
    whole ``crate status`` verb, and that is assertable at the seam whether or
    not CPython ever raises there.
    """

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
                    remedy=Remedy.MOUNT_LIBRARY_VOLUME, steps=("attach the drive",)
                ),
                scope=Scope.RUN,
                origin=("tests",),
            )
        )

    return doctor.Check(key, run)


def test_a_structured_refusal_keeps_its_reason_remedy_steps_and_reserved_code():
    """The blanket rescue flattened a refusal into "report this defect".

    Measured: status FAIL, remedy report-defect, detail "this check did not
    complete", and the process left under PRECONDITION rather than under the
    reserved 22. The reason slug, the remediation steps and the code were all
    gone, and the user was told to file a defect about their own unmounted drive.
    The rescue is deliberately not per check, which is exactly why it mattered:
    every check written here inherits it.
    """
    inputs = doctor._Inputs(None, None, probes())
    finding = doctor.answer(_refusing_check(), inputs)

    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.MOUNT_LIBRARY_VOLUME
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
    """The other half, and it is the one the rescue was written for.

    Splitting the handler must not stop the report surviving a check that simply
    broke, which is the property the whole module's opening argument turns on.
    """
    def explode(_inputs):
        raise RuntimeError("psutil said no")

    inputs = doctor._Inputs(None, None, probes())
    finding = doctor.answer(doctor.Check("library.mounted", explode), inputs)

    assert finding.status is doctor.Status.FAIL
    assert finding.cause is None
    assert "did not complete" in finding.detail
    assert finding.remedy is Remedy.REPORT_DEFECT
    assert doctor.failure_cause(doctor.Report((finding,))).reason == "doctor-check-failed"


def test_a_report_with_no_structured_refusal_still_exits_precondition(configured):
    """The ordinary failing report keeps the code it has always had.

    Reading the exit code off the cause rather than writing PRECONDITION into the
    envelope must not change what an ordinary broken machine reports.
    """
    report = doctor.run(configured, probes=probes(find_binary=lambda _n: None))
    assert report.ok is False
    cause = doctor.failure_cause(report)
    assert cause.reason == "doctor-check-failed"
    assert cause.code is ExitCode.PRECONDITION


def test_doctor_leaves_under_the_code_a_refusing_check_reserved(monkeypatch, configured):
    """End to end through the real dispatcher, because the code is the contract."""
    monkeypatch.setattr(doctor, "CHECKS", (_refusing_check(),))
    code, out, _err = drive(["--output", "json", "doctor"])
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE)
    assert json.loads(out)["cause"]["reason"] == "library-volume-unmounted"


def test_the_rescue_still_lets_the_three_control_exceptions_through():
    """KeyboardInterrupt, SystemExit and GeneratorExit are not check failures.

    They are how a process is being stopped, and swallowing one turns a Ctrl-C
    into a green check.
    """
    inputs = doctor._Inputs(None, None, probes())
    for kind in (KeyboardInterrupt, SystemExit, GeneratorExit):
        def raiser(_inputs, _kind=kind):
            raise _kind()

        with pytest.raises(kind):
            doctor.answer(doctor.Check("library.mounted", raiser), inputs)
    # And a MemoryError IS caught, because the report is worth more than the
    # check that ran out of room.
    def hungry(_inputs):
        raise MemoryError()

    assert doctor.answer(doctor.Check("k", hungry), inputs).status is doctor.Status.FAIL


# ── an ancestor this account cannot traverse ────────────────────────────────


@pytest.fixture
def sealed_ancestor(tmp_path):
    """A library root under a directory this account cannot traverse.

    The routine first-run state on the platform this ships for first: on macOS
    an interpreter without Full Disk Access is refused exactly this way for
    anything under Documents, Desktop, Downloads or an external volume, and
    ``Path.exists`` re-raises the permission error rather than answering False.
    """
    sealed = tmp_path / "sealed"
    sealed.mkdir()
    (sealed / "lib").mkdir()
    sealed.chmod(0o000)
    yield sealed / "lib"
    sealed.chmod(0o700)


def test_the_wizard_refuses_an_unreachable_ancestor_rather_than_filing_a_defect(
    sealed_ancestor,
):
    """Item 3 of the residual finding "Five places where "I could not look" is
    still not said out loud", and what it recorded was not what happens.

    It said the wizard "exits with a traceback" and deferred it because a
    traceback is loud rather than wrong. Driven end to end there is no traceback:
    the dispatcher's blanket catches it and renders "setup: failed (INTERNAL) /
    internal-error: PermissionError / fix: this is a defect; report it". So the
    product classified the user's own filesystem permission as a Cratekit defect
    and sent them to file a bug report, in the one verb whose entire job is
    getting a fresh clone to a first write.
    """
    wizard = setup_verb._Wizard({}, silent())
    with pytest.raises(CratekitError) as excinfo:
        setup_verb._resolve_volume_id(
            wizard, str(sealed_ancestor), None, probes(identity_provider=lambda _p: "X")
        )

    cause = excinfo.value.cause
    assert cause.reason == "library-root-unreachable"
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert str(sealed_ancestor) in cause.message
    assert "Full Disk Access" in cause.message
    assert render.remedy_text(Remedy.GRANT_PATH_ACCESS)


def test_setup_end_to_end_names_the_path_instead_of_asking_for_a_bug_report(
    sealed_ancestor, tmp_path, monkeypatch
):
    """Through the real dispatcher, which is where the defect was visible."""
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(sealed_ancestor))
    monkeypatch.setattr(doctor, "Probes", lambda: probes())

    code, out, err = drive(
        [
            "--output", "json", "setup",
            "--library-root", str(sealed_ancestor),
            "--db-path", str(sealed_ancestor / "db" / "master.db"),
            "--staging", str(tmp_path / "staging"),
            "--profile", "slim",
            "--taxonomy", "default",
        ]
    )
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), err
    envelope = json.loads(out)
    assert envelope["cause"]["reason"] == "library-root-unreachable"
    assert envelope["cause"]["reason"] != "internal-error"
    assert "report it" not in envelope["cause"]["remediation"].get("remedy", "")
    # THE SLUG ITSELF, because it is what persists. Nothing pinned the token's
    # spelling, so a typo in the enum travelled into every stored cause and every
    # machine consumer branching on it while the whole suite stayed green.
    assert envelope["cause"]["remediation"]["remedy"] == "grant-path-access"


def test_the_taxonomy_seed_reports_an_unreachable_root_rather_than_raising(
    sealed_ancestor, monkeypatch
):
    """The second place the wizard reaches preflight, and it is reached only when
    ``--volume-id`` supplied the identity the derive would otherwise have refused
    over. It NOTES rather than raises, because the configuration is already saved
    by the time it runs and the report is what the user reads.
    """
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(sealed_ancestor))
    cfg = config.from_dict(document_for(sealed_ancestor))
    assert Path(cfg.library.root) == sealed_ancestor
    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, cfg, probes())

    note = next(n for n in wizard.notes if n.key == "setup.taxonomy")
    assert note.status is doctor.Status.FAIL
    assert note.remedy is Remedy.GRANT_PATH_ACCESS
    assert "Full Disk Access" in note.detail
    assert str(sealed_ancestor) in note.detail


def test_the_seed_reports_a_state_directory_it_could_not_look_into(library):
    """THE HOLE THE FIRST FIX MOVED. The mount question was handled at the top of
    ``_seed_taxonomy`` and the same exception shape was left unhandled at the
    bottom of it, ten lines on.

    ``Path.exists`` re-raises a permission error rather than answering False, so
    a ``.cratekit`` directory this account cannot traverse escaped the whole verb
    and the dispatcher rendered the user's own filesystem permission as
    "internal-error ... this is a defect; report it". The library root here is
    perfectly reachable, which is what makes it a second condition rather than
    the same one: everything above this line succeeds.
    """
    cfg = config.from_dict(document_for(library))
    state = config.state_path("taxonomy_active", cfg).parent
    state.mkdir(parents=True, exist_ok=True)
    wizard = setup_verb._Wizard({}, silent())
    state.chmod(0o000)
    try:
        setup_verb._seed_taxonomy(wizard, cfg, probes())
    finally:
        state.chmod(0o700)

    note = next(n for n in wizard.notes if n.key == "setup.taxonomy")
    assert note.status is doctor.Status.FAIL
    assert note.remedy is Remedy.GRANT_PATH_ACCESS
    assert "could not be examined" in note.detail
    assert "Full Disk Access" in note.detail


def test_the_seed_reports_a_write_it_was_refused_rather_than_filing_a_defect(library):
    """The other half of the same tail, and a DIFFERENT act from the one above.

    A library volume mounted read only, or a state directory owned by another
    account, is reached and stat-ed perfectly well and refuses the write. That
    escaped as an internal defect too. It must not borrow the sentence above,
    which asserts a directory could not be opened: this one was opened.

    THE SENTENCE NOW NAMES THE KIND THAT HAPPENED RATHER THAN BOTH. It used to
    hedge, "a directory this account may not write in or a volume mounted read
    only", and then close with the act for the first of those two whichever one
    had actually occurred. This arrangement is the first: a directory mode, on a
    writable volume. So the read only act must NOT appear, and the sibling test
    below drives a real read only volume and asserts the reverse.
    """
    cfg = config.from_dict(document_for(library))
    state = config.state_path("taxonomy_active", cfg).parent
    state.mkdir(parents=True, exist_ok=True)
    wizard = setup_verb._Wizard({}, silent())
    # Readable, listable, and not writable.
    state.chmod(0o500)
    try:
        setup_verb._seed_taxonomy(wizard, cfg, probes())
    finally:
        state.chmod(0o700)

    note = next(n for n in wizard.notes if n.key == "setup.taxonomy")
    assert note.status is doctor.Status.FAIL
    assert note.remedy is Remedy.GRANT_PATH_ACCESS
    assert "could not be written" in note.detail
    assert "Full Disk Access" in note.detail
    # The act for the OTHER kind is absent, because the other kind did not occur.
    assert "mounted read only" not in note.detail
    assert "chflags nouchg" not in note.detail
    # And it does not claim the path could not be looked at, because it was.
    assert "could not be examined" not in note.detail
    assert not config.state_path("taxonomy_active", cfg).exists()


def test_the_grant_path_access_advice_claims_neither_act_over_the_other(library):
    """One token, two conditions, so the one-line advice may assert neither.

    It read "this account cannot open a directory on the way to the path named
    below", which is false for the read-only-volume half: that directory opens
    fine. The specific act is named in each finding's own detail.
    """
    advice = render.remedy_text(Remedy.GRANT_PATH_ACCESS)
    assert advice
    assert "cannot reach or write" in advice
    assert "on the way to" not in advice


def test_doctor_still_answers_every_check_over_an_unreachable_root(
    sealed_ancestor, monkeypatch
):
    """The behaviour that was already right, pinned so the wizard's fix matches it.

    Doctor survives this and answers all of its checks, with the mount question
    reported as a check that did not complete rather than as a green one.
    """
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(sealed_ancestor))
    report = doctor.run(config.from_dict(document_for(sealed_ancestor)), probes=probes())

    assert tuple(f.key for f in report.findings) == doctor.CHECK_KEYS
    mounted = find(report, "library.mounted")
    assert mounted.status is doctor.Status.FAIL
    assert "did not complete" in mounted.detail


# ── one classification, made once, for a permission the user can grant ───────
#
# Round six. The same defect was fixed three times, at six sites, and found again
# three times, so it is no longer fixed per site: ``cause.permission_denied``
# answers it, ``cause.access_remedy`` chooses the act, and the two blankets that
# exist for what nobody guarded, the dispatcher and doctor's check runner, both
# ask. The tests below drive REAL directories with mode 0o000 rather than
# fixtures raising a synthetic error, because a fixture raising ``PermissionError``
# is what pinned the wrong answer for three rounds.


@pytest.mark.parametrize("arrangement", ["configuration-directory", "library-root"])
def test_both_verbs_answer_a_real_permission_with_an_act_the_user_can_perform(
    tmp_path, monkeypatch, arrangement
):
    """THE WHOLE VERB, through the real dispatcher, against a real 0o000 directory.

    TWO ARRANGEMENTS, AND ONLY ONE OF THEM USED TO RUN. The docstring named both
    and the body sealed only the configuration directory: the library root was
    created fresh under ``tmp_path`` and nothing ever refused it, so the row
    called "the whole verb" covered exactly one sealed location and asserted one
    slug that the other arrangement does not produce. Both are driven now, and
    what is asserted per arrangement is what that arrangement is entitled to.

    A library root behind a sealed ancestor is answered by the verbs THEMSELVES,
    under their own slug, because a refusal that knows which path it was about
    keeps the better name for it. A configuration directory behind one is
    answered by NOBODY, because ``config.load`` stats the file before it reads it
    and a stat is not a ``ConfigError``.

    What is asserted in both is the thing a user reads. Not a slug, not an
    exception type: whether the product told them to file a bug about their own
    filesystem, and whether it named the path they have to act on.
    """
    sealed = tmp_path / "sealed"
    (sealed / "cfg").mkdir(parents=True)
    library = (sealed / "lib") if arrangement == "library-root" else (tmp_path / "library")
    if arrangement == "library-root":
        library.mkdir()
        monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "cfg"))
    else:
        monkeypatch.setenv(config.ENV_CONFIG_DIR, str(sealed / "cfg"))
    config.reset_cache()
    monkeypatch.setattr(doctor, "Probes", lambda: probes())

    argv = [
        "--output", "json", "setup",
        "--library-root", str(library),
        "--db-path", str(library / "db" / "master.db"),
        "--staging", str(tmp_path / "staging"),
        "--profile", "slim",
        "--taxonomy", "default",
    ]
    if arrangement == "configuration-directory":
        # The identity is supplied, so the run reaches the configuration file.
        # Withholding it in the other arrangement is what makes the wizard DERIVE
        # an identity, which is the act that meets the sealed ancestor.
        argv += ["--volume-id", VOLUME]

    sealed.chmod(0o000)
    try:
        doctor_code, doctor_out, doctor_err = drive(["--output", "json", "doctor"])
        setup_code, setup_out, setup_err = drive(argv)
    finally:
        sealed.chmod(0o755)
        config.reset_cache()

    surfaces = [(setup_code, setup_out, setup_err)]
    if arrangement == "configuration-directory":
        # Doctor reports on the CONFIGURATION it could not load. With the config
        # readable and only the library sealed, it reports a library finding and
        # exits on the FAIL band rather than refusing, which the check-table
        # tests already cover; this row is about a refusal.
        surfaces.append((doctor_code, doctor_out, doctor_err))

    for code, out, err in surfaces:
        envelope = json.loads(out)
        cause = envelope["cause"]
        # The ACT is the same in both, and it is what the user performs.
        assert cause["remediation"]["remedy"] == "grant-path-access", err
        assert "report it" not in err
        assert "report-defect" not in out
        # The path is the entire actionable content: "permission denied" with
        # nothing to grant access TO is a sentence nobody can act on.
        assert str(sealed) in cause["message"]
        assert cause["detail"]["path"] is not None
        # THE SLUG AND THE CODE DIFFER BY ARRANGEMENT, and both are right. A
        # refusal that knows the path was the LIBRARY says so on the library's
        # band; one raised where nobody knew which path it was says so on the
        # installation's, and only that one is written by the classification.
        if arrangement == "library-root":
            assert cause["reason"] == "library-root-unreachable"
            assert code == int(ExitCode.LIBRARY_UNAVAILABLE)
        else:
            assert cause["reason"] == "path-permission-denied"
            assert code == int(ExitCode.PRECONDITION)
            assert f"The path is {cause['detail']['path']}." in cause["message"]


def test_the_help_screen_survives_a_configuration_directory_it_cannot_open(
    tmp_path, monkeypatch, capsys
):
    """A CLAIM THE CODE DID NOT KEEP, in the first thing every invocation runs.

    ``_membership`` says a "missing or unreadable config resolves to the full
    preset rather than raising", and it caught ``ConfigError`` only. A stat under
    a directory the operating system will not open raises ``PermissionError``,
    which is neither, and the call sits OUTSIDE the dispatcher's try, in the
    parser construction. So ``crate --help`` exited with a traceback on a machine
    whose configuration directory is sealed, which is the one moment a new user
    has nothing to diagnose with.
    """
    sealed = tmp_path / "sealed"
    (sealed / "cfg").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(sealed / "cfg"))
    config.reset_cache()

    sealed.chmod(0o000)
    try:
        code, _out, _err = drive(["--help"])
    finally:
        sealed.chmod(0o755)
        config.reset_cache()

    # The parser prints its own help to the real stream and exits, which the
    # dispatcher converts to a status; what is asserted is that it got there at
    # all rather than dying on the way in.
    assert code == int(ExitCode.OK)
    assert "usage: crate" in capsys.readouterr().out


def test_a_mount_slot_this_account_cannot_stat_is_not_an_empty_mount_slot(tmp_path):
    """BLOCKING, and instance seven of absence read as evidence of absence.

    ``os.path.ismount`` swallows every ``OSError`` and answers False, so with the
    volume ATTACHED under a directory this account cannot traverse the caller was
    told "no volume is mounted there right now" and sent to plug in a drive that
    was already plugged in. Nothing established that. A refusal may not assert a
    physical fact it could not observe.

    Both shapes are driven, because the two stats ``ismount`` makes fail in
    different arrangements: a slot behind a sealed parent cannot be stat-ed at
    all, and a slot that is itself unreadable cannot have its own parent resolved
    through it.
    """
    from cratekit.core import preflight

    behind_a_seal = tmp_path / "sealed"
    (behind_a_seal / "EXT").mkdir(parents=True)
    itself = tmp_path / "EXT2"
    itself.mkdir()

    behind_a_seal.chmod(0o000)
    itself.chmod(0o000)
    try:
        with pytest.raises(PermissionError):
            preflight.is_mount_point(behind_a_seal / "EXT")
        with pytest.raises(PermissionError):
            preflight.is_mount_point(itself)
    finally:
        behind_a_seal.chmod(0o755)
        itself.chmod(0o755)

    # AND THE REAL ANSWERS ARE UNCHANGED. Absent is still False, because nothing
    # is there and nothing is mounted there, and the answer still comes from the
    # standard library rather than from a reimplementation of its rules.
    assert preflight.is_mount_point(tmp_path / "never-existed") is False
    assert preflight.is_mount_point(itself) is False
    assert preflight.is_mount_point(Path(tmp_path.anchor)) is True


def test_the_wizard_does_not_claim_an_unmounted_volume_it_could_not_observe(
    tmp_path, monkeypatch
):
    """The refusal that named a cause it had not established, end to end.

    Measured before the fix, with the volume attached and mounted: ``ismount``
    under EPERM answered False, ``identity_source`` answered None, and the wizard
    printed "no volume is mounted there right now. Attach the library volume and
    run setup again". It now refuses under the reason that IS established, which
    is that a directory on the way could not be opened, and the two sentences are
    different sentences on purpose.
    """
    from cratekit.core import preflight

    volumes = (tmp_path / "Volumes").resolve()
    volumes.mkdir()
    slot = volumes / "EXT"
    root = slot / "Music"
    root.mkdir(parents=True)
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((volumes, 1),))
    wizard = setup_verb._Wizard({}, silent())

    slot.chmod(0o000)
    try:
        with pytest.raises(CratekitError) as excinfo:
            setup_verb._resolve_volume_id(
                wizard, str(root), None, probes(identity_provider=lambda _p: "X")
            )
    finally:
        slot.chmod(0o755)

    cause = excinfo.value.cause
    assert cause.reason == "library-root-unreachable"
    assert cause.reason != "library-volume-unmounted"
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert "no volume is mounted there right now" not in cause.message
    assert "Attach the library volume" not in cause.message
    assert str(root) in cause.message


def test_one_pair_of_paths_does_not_get_two_answers_decided_by_permission(
    tmp_path, monkeypatch
):
    """The comparison underneath the mount rule, and permission was deciding it.

    ``samefile`` stats both sides, and one handler over every ``OSError`` turned
    "this account may not look" into "compared, and different". So two case
    spellings of ONE directory on a case insensitive volume answered True when
    stat-able and False when not: the same pair, two answers, decided by a
    permission rather than by identity, and the False is the accepting direction
    that lets an identity be read off the wrong disk.
    """
    from cratekit.core import preflight

    sealed = tmp_path / "sealed"
    (sealed / "Volumes").mkdir(parents=True)
    declared = sealed / "Volumes"
    ordinary = tmp_path / "elsewhere"
    ordinary.mkdir()
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: ((declared, 1),))

    # Stat-able: a real comparison, and a real answer.
    assert preflight._names_one_path(declared, declared) is True
    assert preflight._names_one_path(ordinary, declared) is False

    sealed.chmod(0o000)
    try:
        # The identical pair, and the answer may not silently become "different".
        with pytest.raises(PermissionError):
            preflight._names_one_path(ordinary, declared)
        # And the rule built on it refuses rather than finding no slot at all,
        # which is what fell through to the boot disk.
        with pytest.raises(PermissionError):
            preflight.mount_location_ancestors(ordinary / "EP" / "Music")
    finally:
        sealed.chmod(0o755)

    # Absent on both sides is still a real answer and still False: nothing was
    # refused, the two spellings simply are not one path.
    assert preflight._names_one_path(tmp_path / "a", tmp_path / "b") is False


def test_the_database_probe_survives_a_recorded_path_it_cannot_stat(
    tmp_path, monkeypatch
):
    """BLOCKING, and it killed the whole verb before it asked anything.

    ``try/except`` covered the settings READER and stopped there, so the stat
    below it ran unguarded, and ``Path.exists`` re raises under EPERM rather than
    answering False. On an ordinary first run where rekordbox's OWN settings name
    a database on an external drive or under Documents, ``crate setup`` exited
    INTERNAL with "this is a defect; report it" before the first question. The
    path is not one the user supplied, so there was nothing to route around.

    AND IT IS STILL PROPOSED. Dropping the proposal would apply "could not look
    means it is not there" to the one machine where the proposal is most likely
    to be right: rekordbox is using that database and only this interpreter is
    refused. It is a default to a question, never a value written unasked.
    """
    root = tmp_path / "library"
    locked = root / "db"
    locked.mkdir(parents=True)
    (root / "Music").mkdir()
    (locked / "master.db").write_bytes(b"")
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "cfg"))
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    config.reset_cache()
    monkeypatch.setattr(
        setup_verb.rb_writer,
        "read_rekordbox_settings",
        lambda: {"db_path": str(locked / "master.db")},
    )
    monkeypatch.setattr(doctor, "Probes", lambda: probes())

    locked.chmod(0o000)
    try:
        assert setup_verb._probe_db_path() == str(locked / "master.db")
        code, out, err = drive(
            [
                "--output", "json", "setup",
                "--library-root", str(root),
                "--volume-id", VOLUME,
                "--staging", str(tmp_path / "staging"),
                "--profile", "slim",
                "--taxonomy", "default",
            ]
        )
    finally:
        locked.chmod(0o755)
        config.reset_cache()

    envelope = json.loads(out)
    assert code != int(ExitCode.INTERNAL), err
    assert envelope.get("cause", {}).get("reason") != "internal-error"
    assert "report-defect" not in out
    # THE VERB COMPLETED: a configuration was written and the proposal was taken
    # as the default, which is the whole thing that could not happen before.
    assert config.load().library.db_path == locked / "master.db"


def test_an_unreadable_backup_fact_file_is_a_permission_not_a_corruption(configured):
    """It told the user to repair or reset the record of their last backup.

    Over a file that may be perfectly intact. "Exists but could not be read" also
    claims the file is there, and an untraversable parent raises exactly this
    without anything under it having been observed. Two conditions, two acts:
    a corruption is repaired, a permission is granted.
    """
    path = backup_facts.path_for(configured)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"schema_version": 1, "portions": {}}')

    path.chmod(0o000)
    try:
        report = doctor.run(configured, probes=probes())
    finally:
        path.chmod(0o644)

    for portion in backup_facts.PORTIONS:
        finding = find(report, f"backup.age.{portion}")
        assert finding.status is doctor.Status.FAIL
        assert finding.remedy is Remedy.GRANT_PATH_ACCESS
        assert "repair or reset" not in (render.remedy_text(finding.remedy) or "")
        assert "exists but could not be read" not in finding.detail

    # AND A REAL CORRUPTION STILL ASKS FOR A REPAIR. Classifying the permission
    # out of this handler must not classify everything out of it.
    path.write_text("this is not JSON at all")
    damaged = find(doctor.run(configured, probes=probes()), "backup.age.files")
    assert damaged.status is doctor.Status.FAIL
    assert damaged.remedy is Remedy.REPAIR_BACKUP_FACTS


def test_an_active_template_that_is_present_and_is_not_text_is_reported(configured):
    """The second undriven ``UnicodeDecodeError`` leg, at ``taxonomy.active``.

    A ``UnicodeDecodeError`` is a ``ValueError`` rather than an ``OSError``, so
    the member exists precisely to stop a template that is present and does not
    decode escaping the check. Dropping it killed no test: only the permission
    half of the clause was ever driven.
    """
    path = config.state_path("taxonomy_active", configured)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"trees:\n  - name: \xff\xfe\n")

    finding = find(doctor.run(configured, probes=probes()), "taxonomy.active")

    assert finding.status is doctor.Status.FAIL
    assert "could not be read" in finding.detail
    assert "did not complete" not in finding.detail, "the blanket rescue answered"
    # Nothing was refused by the operating system, so this one IS a repair.
    assert finding.remedy is Remedy.REPORT_DEFECT


def test_a_commit_hook_that_is_present_and_is_not_text_is_reported(configured, tmp_path):
    """The third undriven leg, at ``repo.commit_hook``, and the same shape.

    The equivalent member in the wizard's own template read kills a test, so the
    setup half was covered and the doctor half was not, in a pair of handlers
    written to be the same handler.
    """
    root = tmp_path / "checkout"
    (root / ".git" / "hooks").mkdir(parents=True)
    (root / ".pre-commit-config.yaml").write_text("repos: []\n")
    (root / ".git" / "hooks" / "pre-commit").write_bytes(b"#!/bin/sh\n\xff\xfe\n")

    finding = find(
        doctor.run(configured, probes=probes(checkout_root=lambda: root)),
        "repo.commit_hook",
    )

    assert finding.status is doctor.Status.FAIL
    assert "could not be read" in finding.detail
    assert "did not complete" not in finding.detail, "the blanket rescue answered"
    assert finding.remedy is Remedy.REPORT_DEFECT


def test_the_classification_reads_the_declared_cause_and_not_the_context(tmp_path):
    """One decision, and the boundary of it is the point.

    A wrapper that says ``raise X from exc`` is stating that its failure IS that
    failure, so a permission underneath may not be hidden by it. An IMPLICIT
    context is merely "this happened while handling that", which is exactly what
    a handler that catches a permission and then raises a real defect produces,
    and reading it would classify that defect as a permission the user can grant.
    """
    from cratekit.core import cause as cause_module

    denied = PermissionError(13, "refused")
    assert cause_module.permission_denied(denied) is denied
    assert cause_module.permission_denied(RuntimeError("fell over")) is None
    assert cause_module.permission_denied(None) is None
    # AND THE ERRNO IS READ AS WELL AS THE CLASS. CPython picks the subclass from
    # the errno only when the constructor is given one, so a base ``OSError``
    # built with a message and stamped with its number afterwards, which is how a
    # third-party reader re-raises one, is EACCES and is not a
    # ``PermissionError``. Reading the class alone would call it a defect.
    import errno as errno_module

    rebuilt = OSError("the operating system refused this account")
    rebuilt.errno = errno_module.EACCES
    assert type(rebuilt) is OSError
    assert cause_module.permission_denied(rebuilt) is rebuilt

    other = OSError("no such file")
    other.errno = errno_module.ENOENT
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

    # ``access_remedy`` chooses an ACT, so it asks the question that requires a
    # path. ``permission_denied`` above answers a narrower one for the callers
    # deciding whether to re-raise, and they tell nobody anything.
    named = PermissionError(13, "refused", str(tmp_path / "sealed" / "inside"))
    assert (
        cause_module.access_remedy(named, otherwise=Remedy.REPORT_DEFECT)
        is Remedy.GRANT_PATH_ACCESS
    )
    assert (
        cause_module.access_remedy(RuntimeError("x"), otherwise=Remedy.REPORT_DEFECT)
        is Remedy.REPORT_DEFECT
    )
    assert (
        cause_module.access_remedy(denied, otherwise=Remedy.REPORT_DEFECT)
        is Remedy.REPORT_DEFECT
    ), "a refusal naming no path has no path to grant access to"


# ═══════════════════════════════════════════════════════════════════════════
# Round seven: the classification lives where a refusal is CONSTRUCTED
# ═══════════════════════════════════════════════════════════════════════════
#
# Round six put the decision in two blankets, the dispatcher and doctor's check
# runner, and argued it from a property that measurement contradicts: an AST walk
# over the package finds nineteen ``except OSError`` sites that raise a
# structured refusal, and eighteen of them never reach either blanket, because a
# blanket only ever sees what nobody caught. Three of the eighteen hard coded the
# wrong answer. So the decision moved to ``cause.classified``, which every
# structured refusal in the package passes through, and the tests below drive it
# from the OUTSIDE: real permissions, a real read only volume, a real locked
# file, and the driver level error this program's own state store raises.


def _sealed(path: Path):
    """A real 0o000 file, restored however the test ends."""
    import contextlib

    @contextlib.contextmanager
    def arranged():
        before = path.stat().st_mode
        path.chmod(0o000)
        try:
            yield path
        finally:
            path.chmod(before & 0o777)

    return arranged()


def test_a_sealed_state_database_answers_with_its_path_and_an_act(tmp_path, monkeypatch):
    """F1. THE CLASSIFICATION WAS BLIND TO EVERYTHING ARRIVING THROUGH A C EXTENSION.

    ``sqlite3.OperationalError`` is not an ``OSError``. It carries no errno, no
    filename and no ``__cause__``, so an errno-shaped rule answers None for it,
    and this program keeps its own job queue in SQLite. Driven end to end, a
    ``chmod 000`` on ``queue.db`` with every directory left traversable produced
    exit 1, ``internal-error``, ``report-defect`` and "this is a defect; report
    it" over a file the user had every ability to fix.

    The connection site is the only place that knows WHICH file the driver meant,
    so it records it; the classification then measures the path rather than
    assuming, and answers with a remedy and the path to apply it to.
    """
    cfg_dir = tmp_path / "cfg"
    cfg_dir.mkdir()
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(cfg_dir))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "state"))
    config.reset_cache()
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    config.save(config.from_dict(document_for(root)))
    config.reset_cache()

    # One clean run, which is what creates the queue.
    code, _out, _err = drive(["--output", "json", "job", "list"])
    assert code == 0, "the arrangement itself must be green before it is broken"
    queue = jobs.queue_path()
    assert queue.exists()

    with _sealed(queue):
        code, out, err = drive(["--output", "json", "job", "list"])

    envelope = json.loads(out)
    cause = envelope["cause"]
    assert cause["reason"] == "path-permission-denied", cause
    assert cause["remediation"]["remedy"] == "grant-path-access"
    assert cause["detail"]["path"] == str(queue)
    assert str(queue) in cause["message"]
    assert code == int(ExitCode.PRECONDITION)
    assert "report it" not in err
    assert "report-defect" not in out


def test_a_refusal_that_names_no_path_does_not_claim_one(tmp_path, monkeypatch):
    """F2. OVER CLASSIFICATION, AND THE SENTENCE IT PRODUCED HAD NOTHING IN IT.

    The kernel refuses several things that are not paths at all: a bind to a
    privileged port and a signal to another account's process both raise
    ``PermissionError`` with ``filename`` set to None. The old rule said "yes, a
    permission" for those, and the line the user then read was "this account
    cannot reach or write the path named below; grant this interpreter access to
    it, on macOS through Full Disk Access" with no path below it, over an act
    Full Disk Access has nothing to do with.

    A guard that misfires on ordinary code is not a lesser failure than one that
    misses. The classification now requires a path before it asserts one, and
    what has no path stays the honest "this program did not anticipate it".
    """
    cfg_dir = tmp_path / "cfg"
    cfg_dir.mkdir()
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(cfg_dir))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "state"))
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    config.reset_cache()
    config.save(config.from_dict(document_for(root)))
    config.reset_cache()

    def refused(_ctx):
        # A REAL kernel refusal with no path in it: signalling another account's
        # process. Nothing is sent; signal 0 asks permission and nothing else.
        # NOT GUARDED WITH A SKIP, because a skip is a guard switched off with no
        # record of when it comes back. An account that CAN signal pid 1 is root,
        # on which the whole 0o000 suite is meaningless anyway, and this fails
        # loudly there instead of passing quietly.
        os.kill(1, 0)
        raise AssertionError("this account signalled pid 1, so the arrangement is void")

    monkeypatch.setattr(jobs_cli, "list_jobs", refused)
    code, out, err = drive(["--output", "json", "job", "list"])

    envelope = json.loads(out)
    cause = envelope["cause"]
    assert cause["reason"] == "internal-error", cause
    assert cause["remediation"]["remedy"] == "report-defect"
    assert "path named below" not in err
    assert "the arrangement is void" not in cause["message"]
    assert code == int(ExitCode.INTERNAL)
    # And the sentence is not produced at all, rather than produced empty.
    assert render.access_note(PermissionError(1, "Operation not permitted")) is None


def test_a_read_only_volume_is_not_sent_to_full_disk_access(tmp_path):
    """F8. EROFS WAS NOT CLASSIFIED, SO THE ADVICE WAS EITHER A DEFECT OR WRONG.

    A read only volume refuses every writer on the machine. No permission grant
    changes that, so "grant this interpreter access, on macOS through Full Disk
    Access" is an instruction that cannot succeed, and ``internal-error`` with
    "report it" beside it is worse. A DJ's library on a read only disk image or a
    write protected card is ordinary.

    The refusal here is REAL. Every current macOS mounts its system volume read
    only, so a write to it is the kernel's own EROFS rather than a constructed
    one, and the test says so rather than asserting it.
    """
    from cratekit.core import cause as cause_module

    refused: OSError | None = None
    try:
        os.mkdir("/cratekit-u27-read-only-probe")
    except OSError as exc:
        refused = exc
    else:  # pragma: no cover - only on a machine with a writable root volume
        os.rmdir("/cratekit-u27-read-only-probe")
        raise AssertionError("this machine's root volume is writable, so it proves nothing")
    assert refused.errno == errno.EROFS, (
        f"this machine's root volume answered {refused.errno} rather than EROFS, "
        f"so the arrangement is not a read only volume"
    )

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

    # And it travels: a refusal built anywhere in the package under an EROFS is
    # answered with the act for a read only volume rather than with the act for a
    # permission, even where the site itself named the permission.
    try:
        try:
            os.mkdir("/cratekit-u27-read-only-probe")
        except OSError as inner:
            raise refuse(
                "library-root-unreachable",
                "the library root could not be created",
                remedy=Remedy.GRANT_PATH_ACCESS,
            ) from inner
    except CratekitError as err:
        assert err.cause.remediation.remedy is Remedy.REMOUNT_WRITABLE
        assert err.declared_cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS


def test_a_locked_file_is_routed_to_the_lock_and_names_the_destination(tmp_path, monkeypatch):
    """F5. THE COMMONEST NON PERMISSION EPERM ON macOS, ANSWERED TWO WAYS WRONG.

    Finder's "Locked" checkbox writes the ``uchg`` flag, and a write to a file
    carrying it fails EPERM for the file's own owner. Full Disk Access will never
    make that write succeed; ``chflags nouchg`` will.

    AND THE PATH IT NAMED DID NOT EXIST. Every state file is written by renaming
    a temporary one over the destination, and ``os.replace`` reports the SOURCE
    in ``filename``. So the product named ``cfg/tmpXXXX.tmp`` at the user, a file
    that is gone by the time they read about it, while the file they actually
    have to unlock went unmentioned. The destination is in ``filename2`` and is
    what is read first now.
    """
    import subprocess

    from cratekit.core import cause as cause_module

    cfg_dir = tmp_path / "cfg"
    cfg_dir.mkdir()
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(cfg_dir))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "state"))
    config.reset_cache()
    destination = config.config_path()
    destination.write_text('schema_version = 1\n[library]\nroot = "/tmp/x"\n')
    locked = subprocess.run(["chflags", "uchg", str(destination)], check=False)
    assert locked.returncode == 0, "this platform has no per-file lock flag to drive"

    try:
        code, out, err = drive(
            [
                "--output", "json", "setup",
                "--library-root", str(tmp_path / "library"),
                "--db-path", str(tmp_path / "library" / "db" / "master.db"),
                "--volume-id", VOLUME,
                "--staging", str(tmp_path / "staging"),
                "--profile", "slim",
                "--taxonomy", "default",
            ]
        )
    finally:
        subprocess.run(["chflags", "nouchg", str(destination)], check=False)
        config.reset_cache()

    envelope = json.loads(out)
    cause = envelope["cause"]
    assert cause["reason"] == "path-locked", cause
    assert cause["remediation"]["remedy"] == "unlock-path"
    assert cause["detail"]["path"] == str(destination), "the temporary file was named again"
    assert ".tmp" not in cause["detail"]["path"]
    assert "chflags nouchg" in err
    assert "Full Disk Access" not in err
    assert code == int(ExitCode.PRECONDITION)

    # AND THE DESTINATION RULE IS NOT ONLY THE LOCK'S. A rename into a directory
    # this account cannot write refuses the same way with no lock anywhere in it,
    # and ``filename`` is still the temporary file. Driven separately because the
    # locked leg above finds its path through the flag rather than through the
    # ordering, so the ordering was covered by nothing.
    source = tmp_path / "source"
    source.mkdir()
    staged = source / "tmpABCD.tmp"
    staged.write_text("x")
    unwritable = tmp_path / "unwritable"
    unwritable.mkdir()
    landing = unwritable / "config.toml"
    unwritable.chmod(0o500)
    try:
        try:
            os.replace(staged, landing)
        except OSError as exc:
            renamed = cause_module.access_refusal(exc)
    finally:
        unwritable.chmod(0o700)
    assert renamed is not None
    assert renamed.path == str(landing), "the temporary file was named instead"
    assert ".tmp" not in renamed.path


def test_the_session_reader_does_not_read_absence_out_of_a_refusal(tmp_path, monkeypatch):
    """F3, site one, and recurring defect one: ABSENCE READ AS EVIDENCE OF ABSENCE.

    One handler over every ``OSError`` answered "no session is recorded with the
    identifier 'x'" for a record this account was not allowed to open, under
    ``internal-error`` with ``report-defect`` beside it. Two wrong claims in one
    raise: a read that never happened reported as a fact about what is there, and
    a permission reported as a defect in this program.
    """
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "cfg"))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "state"))
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    config.reset_cache()
    cfg = config.from_dict(document_for(root))

    path = session.log_path("session-abc", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}")

    with _sealed(path):
        with pytest.raises(CratekitError) as excinfo:
            session.read_record("session-abc", cfg)

    cause = excinfo.value.cause
    assert cause.reason == "path-permission-denied"
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert cause.detail["path"] == str(path)
    assert "no session is recorded" not in cause.message
    assert "was not established" in cause.message

    # AND ABSENCE IS STILL ABSENCE. Splitting the handler must not cost the
    # answer that was right: a record that genuinely is not there still says so.
    path.unlink()
    with pytest.raises(CratekitError) as absent:
        session.read_record("session-abc", cfg)
    assert "no session is recorded" in absent.value.cause.message


def test_the_acknowledgment_reader_does_not_claim_the_file_exists(tmp_path, monkeypatch):
    """F3, site two. "Exists and could not be read" was not established either.

    Absent is caught above by its own class, so everything reaching that handler
    is a read that did not happen, and an untraversable PARENT fails exactly that
    way while establishing nothing about what is under it. ``backup_facts`` says
    this in so many words one module over; this site said the opposite.
    """
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "cfg"))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "state"))
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    config.reset_cache()
    cfg = config.from_dict(document_for(root))

    ack = session.ack_path(cfg)
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text("{}")

    with _sealed(ack):
        with pytest.raises(CratekitError) as excinfo:
            session.read_acknowledgment(cfg)

    cause = excinfo.value.cause
    assert cause.reason == "path-permission-denied"
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert "exists and could not be read" not in cause.message
    assert "whether it is even there was not established" in cause.message


def test_an_unreadable_capture_manifest_is_not_a_defect_report(tmp_path):
    """F3, site three. The same hard coded ``report-defect``, one module over.

    Nothing about the SENTENCE here was wrong. What was wrong is that the act
    beside it was "report a defect" whatever the operating system said, and the
    ``raise ... from exc`` at the site is what lets the refusal constructor
    overrule it.
    """
    from cratekit.core import snapshot

    capture = tmp_path / "capture"
    capture.mkdir()
    manifest = capture / snapshot.MANIFEST_NAME
    manifest.write_text("{}")

    with _sealed(manifest):
        with pytest.raises(CratekitError) as excinfo:
            snapshot.read_manifest(capture)

    cause = excinfo.value.cause
    assert cause.reason == "path-permission-denied"
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert cause.detail["path"] == str(manifest)
    # The site's own reading is kept, because it is still worth reading.
    assert cause.detail["declared_reason"] == "internal-error"


def test_the_wizard_does_not_call_an_intact_configuration_corrupt(tmp_path, monkeypatch):
    """F4. "REPAIR OR RECREATE IT" OVER A FILE THAT IS BYTE FOR BYTE INTACT.

    A configuration this account cannot read is not a configuration to repair,
    and telling its owner to recreate it sends them to rewrite work they still
    have. The third edge of the residual finding "Three edges of the permission
    classification, stated rather than closed", the one that says the
    classification stops at the configuration reader, scopes the
    ``core/config.py`` half to another unit; this half is this unit's own file
    and was left standing beside it.
    """
    cfg_dir = tmp_path / "cfg"
    cfg_dir.mkdir()
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(cfg_dir))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "state"))
    config.reset_cache()
    document = config.config_path()
    document.write_text('schema_version = 1\n[library]\nroot = "/tmp/x"\n')
    intact = document.read_bytes()

    with _sealed(document):
        code, out, err = drive(
            [
                "--output", "json", "setup",
                "--library-root", str(tmp_path / "library"),
                "--db-path", str(tmp_path / "library" / "db" / "master.db"),
                "--volume-id", VOLUME,
                "--staging", str(tmp_path / "staging"),
                "--profile", "slim",
                "--taxonomy", "default",
            ]
        )
    config.reset_cache()

    envelope = json.loads(out)
    cause = envelope["cause"]
    assert cause["remediation"]["remedy"] != "repair-config-file", cause
    assert cause["remediation"]["remedy"] == "grant-path-access"
    assert cause["reason"] == "path-permission-denied"
    assert code == int(ExitCode.PRECONDITION)
    assert "repair or recreate" not in err
    assert document.read_bytes() == intact, "the file it called unrepairable was never touched"


def test_the_wizards_second_read_does_not_call_an_intact_configuration_corrupt(
    tmp_path, monkeypatch
):
    """F4 at the site, not at the boundary. ``cli/setup.py`` reads the file TWICE.

    An incomplete configuration is loaded, found invalid, and then re-opened raw
    so the answers it does hold are kept. Its own comment says the second open is
    what happens when "a file removed, a permission taken away, or a truncation"
    lands between the two, and its handler answered ``repair-config-file`` for
    every one of them. The permission leg tells a user to repair or recreate a
    document that is byte for byte intact.

    THE REFUSAL IS THE KERNEL'S. Only the TIMING is arranged: the real
    ``config.load`` runs against a real file and the file is sealed after it
    returns, which is exactly the window the handler exists for. What
    ``existing_document`` then meets is a real 0o000 file through a real
    ``Path.open``.
    """
    cfg_dir = tmp_path / "cfg"
    cfg_dir.mkdir()
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(cfg_dir))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "state"))
    config.reset_cache()
    document = config.config_path()
    document.write_text("schema_version = 1\n")
    intact = document.read_bytes()

    real_load = config.load

    def load_then_seal():
        try:
            return real_load()
        finally:
            document.chmod(0o000)

    monkeypatch.setattr(setup_verb.config, "load", load_then_seal)
    try:
        with pytest.raises(CratekitError) as excinfo:
            setup_verb.existing_document()
    finally:
        document.chmod(0o600)
        config.reset_cache()

    cause = excinfo.value.cause
    assert cause.remediation.remedy is not Remedy.REPAIR_CONFIG_FILE
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert cause.reason == "path-permission-denied"
    assert cause.detail["path"] == str(document)
    assert cause.detail["declared_reason"] == "config-unusable"
    assert document.read_bytes() == intact, "the file it called unrepairable was never touched"


def test_doctors_configuration_check_does_not_call_an_intact_file_corrupt(tmp_path, monkeypatch):
    """F4 in the REPORT. ``config.present`` read the remedy off the error class.

    ``ConfigError.remedy`` is a declared class attribute, which is right for
    every way a configuration can genuinely be unusable and wrong for the one way
    that is not the file's fault at all. A document with mode 0o000 is byte for
    byte intact and the report told its owner to repair or recreate it, on the
    same page the wizard tells them it is a permission.
    """
    cfg_dir = tmp_path / "cfg"
    cfg_dir.mkdir()
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(cfg_dir))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "state"))
    config.reset_cache()
    document = config.config_path()
    document.write_text('schema_version = 1\n[library]\nroot = "/tmp/x"\n')

    with _sealed(document):
        finding = find(doctor.run(probes=probes()), "config.present")
    config.reset_cache()

    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is not Remedy.REPAIR_CONFIG_FILE
    assert finding.remedy is Remedy.GRANT_PATH_ACCESS
    assert str(document) in finding.detail
    assert "repair or recreate" not in (render.remedy_text(finding.remedy) or "")


def test_a_verb_that_lets_a_config_error_escape_is_classified_too(tmp_path, monkeypatch):
    """F4 at the LAST hop. Six verbs call ``config.load()`` and catch nothing.

    The dispatcher converts a ``ConfigError`` that reaches it, reading the
    remedy off the error class exactly as the report did. ``ConfigError`` is not
    a ``CratekitError``, so the refusal constructor never sees it and this is the
    one place the classification can be applied to that family.
    """
    cfg_dir = tmp_path / "cfg"
    cfg_dir.mkdir()
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(cfg_dir))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "state"))
    config.reset_cache()
    document = config.config_path()
    document.write_text('schema_version = 1\n[library]\nroot = "/tmp/x"\n')

    with _sealed(document):
        code, out, err = drive(["--output", "json", "review", "list"])
    config.reset_cache()

    cause = json.loads(out)["cause"]
    assert cause["remediation"]["remedy"] == "grant-path-access", cause
    assert cause["reason"] == "path-permission-denied"
    assert cause["detail"]["path"] == str(document)
    assert cause["detail"]["declared_reason"] == "config-unusable"
    assert code == int(ExitCode.PRECONDITION)
    assert "repair or recreate" not in err


def test_the_access_sentence_names_the_path_it_is_about(tmp_path):
    """F6, guard one: the path clause killed nothing and is the actionable half.

    ``access_note``'s own docstring calls the path "the entire actionable
    content", and deleting the clause that carries it killed no test, because the
    only assertion near it was satisfied by the raw ``{exc}`` text that happens to
    repeat the path. This asserts the clause itself.
    """
    sealed = tmp_path / "sealed"
    sealed.mkdir()
    inside = sealed / "inside"
    inside.write_text("x")

    with _sealed(sealed):
        try:
            inside.read_text()
        except OSError as exc:
            note = render.access_note(exc)

    assert note.startswith(f"The path is {inside}. ")
    assert "rather than a defect in this program" in note


def test_the_cause_walk_terminates_on_a_chain_that_names_itself(tmp_path):
    """F6, guard two: the cycle guard killed nothing, and without it nothing dies.

    ``__cause__`` is assignable, so two exceptions can name each other, and the
    walk over the chain is then infinite. A defect that HANGS is the worst shape
    one can take: the process does not fail, it stops responding, and no failing
    assertion is ever reached. It is driven in a subprocess with a deadline for
    exactly that reason, because a test that hangs cannot report anything either.
    """
    import subprocess

    script = (
        "from cratekit.core import cause\n"
        "a = OSError('one')\n"
        "b = OSError('two')\n"
        "a.__cause__ = b\n"
        "b.__cause__ = a\n"
        "assert cause.permission_denied(a) is None\n"
        "assert cause.access_refusal(a) is None\n"
        "print('terminated')\n"
    )
    done = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=60
    )
    assert done.returncode == 0, done.stderr
    assert "terminated" in done.stdout


def test_is_mount_point_answers_an_unrepresentable_path(tmp_path):
    """F7. The sibling ninety lines below catches this and this one did not.

    ``os.path.ismount`` answers False for a path with an embedded null;
    ``os.lstat`` raises ``ValueError`` for one. So the confirming stat added in
    round six turned an answer into an exception for an input the standard
    library already handles, in the one function three mount rules go through.
    """
    from cratekit.core import preflight

    assert os.path.ismount("a\x00b") is False
    assert preflight.is_mount_point(Path("a\x00b")) is False
    assert preflight.slot_holds_a_volume(Path("a\x00b")) is False


# ── the handler sweep: every rescue answers something, or says why it cannot ──
#
# A verifier's mutation sweep found twenty-one handlers in ``cli/doctor.py`` and
# ``cli/setup.py`` that killed no test when deleted, one of them absorbed by the
# blanket rescue and the other twenty driven by nothing at all. A handler nothing
# exercises is a claim nobody has checked, which is the class this whole round is
# about. Each one below is driven; the two that cannot be are argued in the
# source beside them rather than here.


def test_the_declared_interpreter_bound_is_none_when_it_cannot_be_read(monkeypatch):
    """Two ways to have no bound, and both are "nothing was asserted".

    Reported as its own answer rather than as a pass, because a check that cannot
    fail is not a check. It happens for real when the package is imported
    straight from a checkout with no distribution installed.
    """
    monkeypatch.setattr(doctor.registry, "DISTRIBUTION", "cratekit-no-such-distribution")
    assert doctor._declared_python_bound() is None

    monkeypatch.setattr(doctor.metadata, "metadata", lambda _name: {})
    assert doctor._declared_python_bound() is None

    finding = find(
        doctor.run(None, probes=probes(requires_python=None)), "interpreter.version"
    )
    assert finding.status is doctor.Status.INFO
    assert "nothing was asserted about it" in finding.detail


def test_the_binding_pin_problem_is_whatever_the_writers_own_assertion_says(monkeypatch):
    """Asked through the guarded writer rather than by comparing versions here.

    Two ways it answers, and they are different sentences: the writer refusing
    under its own structured cause, and the binding not being importable at all.
    A single handler would have reported the second as the first, which sends a
    user to revalidate a pin against a module that is not installed.
    """
    def refuse(_cfg):
        raise CratekitError(
            Cause(
                reason="pyrekordbox-pin-drift",
                message="pyrekordbox 0.4.0 is not the pinned 0.3.0",
                remediation=Remediation(remedy=Remedy.REVALIDATE_PINS),
                scope=Scope.RUN,
                origin=("tests",),
            )
        )

    monkeypatch.setattr(doctor.rb_writer, "assert_binding_version", refuse)
    assert doctor._binding_pin_problem(None) == "pyrekordbox 0.4.0 is not the pinned 0.3.0"

    def uninstalled(_cfg):
        raise ImportError("No module named 'pyrekordbox'")

    monkeypatch.setattr(doctor.rb_writer, "assert_binding_version", uninstalled)
    answer = doctor._binding_pin_problem(None)
    assert answer is not None and "could not be imported" in answer

    monkeypatch.setattr(doctor.rb_writer, "assert_binding_version", lambda _cfg: None)
    assert doctor._binding_pin_problem(None) is None


def test_the_rclone_dump_answers_none_for_every_way_it_can_fail(monkeypatch, tmp_path):
    """Five failure shapes, one answer, and it is not an empty set of remotes.

    "rclone told us there are no remotes" and "rclone could not be asked" have
    opposite consequences for the backup check, which reports the second as a
    note and the first as a failure naming the remote.
    """
    from types import SimpleNamespace

    # The binary is not there at all.
    assert doctor._rclone_remotes(str(tmp_path / "no-such-rclone")) is None

    def timed_out(*_a, **_k):
        raise doctor.subprocess.TimeoutExpired(cmd="rclone", timeout=10)

    monkeypatch.setattr(doctor.subprocess, "run", timed_out)
    assert doctor._rclone_remotes("rclone") is None

    monkeypatch.setattr(
        doctor.subprocess, "run", lambda *_a, **_k: SimpleNamespace(returncode=1, stdout="")
    )
    assert doctor._rclone_remotes("rclone") is None

    monkeypatch.setattr(
        doctor.subprocess,
        "run",
        lambda *_a, **_k: SimpleNamespace(returncode=0, stdout="not json at all"),
    )
    assert doctor._rclone_remotes("rclone") is None

    monkeypatch.setattr(
        doctor.subprocess,
        "run",
        lambda *_a, **_k: SimpleNamespace(returncode=0, stdout="[1, 2]"),
    )
    assert doctor._rclone_remotes("rclone") is None

    # And the answer when it works, so none of the above is passing by accident.
    monkeypatch.setattr(
        doctor.subprocess,
        "run",
        lambda *_a, **_k: SimpleNamespace(
            returncode=0, stdout='{"gdrive": {"type": "drive", "use_trash": "false"}}'
        ),
    )
    assert doctor._rclone_remotes("rclone") == {
        "gdrive": {"type": "drive", "use_trash": "false"}
    }


def test_an_active_template_that_does_not_validate_is_its_own_answer(configured):
    """Present, readable, and not a usable declaration of a tree.

    A different answer from absent and from unreadable, and the only one of the
    three that running setup can actually repair.
    """
    path = config.state_path("taxonomy_active", configured)
    config.atomic_write_bytes(b"schema_version = 99\n", path)
    finding = find(doctor.run(configured, probes=probes()), "taxonomy.active")

    assert finding.status is doctor.Status.FAIL
    assert "is not usable" in finding.detail
    assert finding.remedy is Remedy.RUN_SETUP


def test_a_registered_adapter_whose_tool_is_not_installed_says_so(configured, monkeypatch):
    """R9's whole point is that acquisition survives one tool breaking.

    A registered name whose module will not import is a different failure from an
    unknown name, and the remedies are opposite: install the tool, or choose
    another adapter.
    """
    def uninstalled(_name):
        raise ImportError("No module named 'yt_dlp'")

    monkeypatch.setattr(doctor.acquire, "load", uninstalled)
    finding = find(doctor.run(configured, probes=probes()), "adapter.contract")

    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.INSTALL_ADAPTER
    assert "is not installed here" in finding.detail


def test_unreadable_backup_facts_are_reported_per_portion(configured, monkeypatch):
    """Never collapsed into "no backup recorded".

    A library with a perfectly good backup and one damaged fact file would
    otherwise report as never backed up, and repairing a small file has nothing
    to do with running a backup.
    """
    def refuse(_cfg, *, now):
        raise backup_facts.BackupFactsUnreadable(
            "the backup facts file is not readable JSON",
            path=Path("/nowhere/backup.json"),
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )

    monkeypatch.setattr(doctor.backup_facts, "ages", refuse)
    report = doctor.run(configured, probes=probes())
    for portion in backup_facts.PORTIONS:
        finding = find(report, f"backup.age.{portion}")
        assert finding.status is doctor.Status.FAIL
        assert finding.remedy is Remedy.REPAIR_BACKUP_FACTS
        assert "not readable JSON" in finding.detail


def test_a_hook_line_with_an_unbalanced_quote_falls_back_to_the_default_config():
    """``shlex.split`` raises on a line it cannot tokenise, and that is not a defect.

    A line this cannot read is a line it must not draw a conclusion from, so it
    keeps looking and ends at pre-commit's own default, which is what an absent
    ``--config`` means anyway.
    """
    assert (
        doctor._hook_config_name('exec pre-commit hook-impl --config="unbalanced')
        == doctor._HOOK_CONFIG_DEFAULT
    )
    # And a quoted path WITH a space is read, which is why shlex is used at all.
    assert (
        doctor._hook_config_name("exec pre-commit hook-impl --config='my config.yaml'")
        == "my config.yaml"
    )


def test_a_run_record_that_will_not_load_is_reported_rather_than_skipped(configured):
    """``crate status`` reads the records the dispatcher persists.

    A record that will not parse is a run whose open gate nobody can see, and
    skipping it silently is how a waiting run disappears from the one surface
    that exists to list them.
    """
    from cratekit.cli import gates

    directory = gates.run_dir()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "r-broken.json").write_text("{ this is not json")

    findings = doctor._run_findings()
    broken = next(f for f in findings if f.key == "run.r-broken")
    assert broken.status is doctor.Status.FAIL
    assert broken.remedy is Remedy.REPORT_DEFECT


def test_a_tree_registry_that_will_not_load_is_never_read_as_no_record(configured):
    """No record means "every tree is still on the bridge", which sends a byte
    write at a tree the database already owns. So an unreadable registry is its
    own answer, carrying the remedy the registry module chose rather than one
    invented here.
    """
    from cratekit.core import tree_registry

    path = tree_registry.path_for(configured)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"{ not json")

    findings = doctor._tree_findings(configured)
    assert [f.key for f in findings] == ["tree.registry"]
    assert findings[0].status is doctor.Status.FAIL
    assert findings[0].remedy is Remedy.RUN_DOCTOR


def test_setup_refuses_a_config_that_stopped_being_readable_between_the_two_reads(
    monkeypatch, tmp_path
):
    """``existing_document`` reads the file TWICE, so the two reads can disagree.

    The first is ``config.load``, which classified it as merely incomplete; the
    second is the raw read that keeps the answers it does hold. Anything that
    changed in between, a file removed, a permission taken away, a truncation,
    lands here, and the one thing it may not do is treat the document as empty
    and write over it.
    """
    missing = tmp_path / "vanished.toml"

    def incomplete():
        raise config.ConfigInvalid("library.root is missing")

    monkeypatch.setattr(config, "load", incomplete)
    monkeypatch.setattr(config, "config_path", lambda: missing)

    with pytest.raises(CratekitError) as excinfo:
        setup_verb.existing_document()
    assert "will not overwrite a configuration it cannot read" in excinfo.value.cause.message
    assert excinfo.value.cause.remediation.remedy is Remedy.REPAIR_CONFIG_FILE


def test_setup_refuses_when_the_migration_ladder_refuses(monkeypatch, tmp_path):
    """The incomplete document is MIGRATED before it is completed.

    Nothing exercises the ladder today because it is empty at version 1, which is
    exactly why the refusal has to be written and driven now: the first migration
    lands in a unit that has no reason to look here.
    """
    path = tmp_path / "config.toml"
    path.write_text("schema_version = 1\n")

    def incomplete():
        raise config.ConfigInvalid("library.root is missing")

    def refuse(_raw):
        raise config.ConfigTooNew("written by a newer Cratekit")

    monkeypatch.setattr(config, "load", incomplete)
    monkeypatch.setattr(config, "config_path", lambda: path)
    monkeypatch.setattr(config, "migrate", refuse)

    with pytest.raises(CratekitError) as excinfo:
        setup_verb.existing_document()
    assert "will not overwrite this configuration" in excinfo.value.cause.message
    assert excinfo.value.cause.remediation.remedy is Remedy.UPGRADE_CRATEKIT


def test_the_database_probe_is_a_proposal_and_never_a_failure(monkeypatch, tmp_path):
    """It reads another application's private format through a third-party reader.

    Its failure modes are not a closed set this module gets to enumerate, and a
    wizard that died because a settings file was an unexpected shape would be
    refusing over a value it was only ever going to OFFER as a default.
    """
    def unexpected():
        raise RuntimeError("the settings file is in a shape this reader has never seen")

    monkeypatch.setattr(setup_verb.rb_writer, "read_rekordbox_settings", unexpected)
    assert setup_verb._probe_db_path() is None

    # A recorded path that is not on this machine is not proposed either: a
    # default nobody can use is worse than no default.
    monkeypatch.setattr(
        setup_verb.rb_writer,
        "read_rekordbox_settings",
        lambda: {"db_path": str(tmp_path / "absent" / "master.db")},
    )
    assert setup_verb._probe_db_path() is None

    real = tmp_path / "master.db"
    real.write_bytes(b"")
    monkeypatch.setattr(
        setup_verb.rb_writer, "read_rekordbox_settings", lambda: {"db_path": str(real)}
    )
    assert setup_verb._probe_db_path() == str(real)


def test_a_credential_that_cannot_be_read_and_one_that_cannot_be_stored_differ(
    configured, monkeypatch
):
    """Two handlers, two remedies, and neither may borrow the other's.

    Nothing could be READ carries "store the credential"; the store REFUSING
    carries whatever the secrets module's own failure types say, because no
    backend, no entry and a rejected entry need opposite acts, and the second
    note here proves the remedy TRAVELS rather than being substituted.
    """
    wizard = setup_verb._Wizard({}, silent())
    wizard.optional = lambda *_a, **_k: True  # the user said yes to every offer
    monkeypatch.setattr(doctor, "requires_check", lambda _key, _m: True)
    monkeypatch.setattr(secrets, "exists", lambda _name: False)

    setup_verb._capture_credentials(wizard, configured)
    unreadable = [n for n in wizard.notes if n.key.startswith("setup.credential.")]
    assert unreadable, "no credential was offered at all"
    for note in unreadable:
        assert note.status is doctor.Status.FAIL
        assert "was offered and nothing could be read" in note.detail
        assert note.remedy is Remedy.SET_CREDENTIAL

    def rejected(_name, _value):
        raise secrets.CredentialBackendUnavailable("no keychain backend resolves here")

    stored = setup_verb._Wizard({}, Scripted([], secrets_=["a-value"] * 8))
    stored.optional = lambda *_a, **_k: True
    monkeypatch.setattr(secrets, "set", rejected)
    setup_verb._capture_credentials(stored, configured)

    refused = [n for n in stored.notes if n.key.startswith("setup.credential.")]
    assert refused
    for note in refused:
        assert note.status is doctor.Status.FAIL
        assert "could not be recorded" in note.detail
        assert note.remedy is Remedy.INSTALL_KEYCHAIN_BACKEND


def test_a_hook_config_path_that_cannot_be_resolved_is_a_refusal_not_a_crash(tmp_path):
    """The handler was written for a shape a hook file cannot produce.

    ``Path.resolve`` does not raise for an absent path, so ``except OSError``
    caught nothing a real hook could cause. What a real hook CAN name is a path
    through a symlink loop, and CPython reports that as ``RuntimeError``, which
    went straight past the handler and out to the blanket rescue as "this check
    did not complete". Same shape as the guard-covered-by-a-guard defect, one
    exception family over.
    """
    root = tmp_path / "checkout"
    (root / ".git" / "hooks").mkdir(parents=True)
    (root / "loop").symlink_to(root / "loop-b")
    (root / "loop-b").symlink_to(root / "loop")
    body = "exec pre-commit hook-impl --hook-type=pre-commit --config=loop/config.yaml\n"

    problem = doctor._hook_dispatch_problem(body, root)
    assert problem is not None
    assert "cannot be resolved" in problem

    (root / ".git" / "hooks" / "pre-commit").write_text(body)
    finding = find(
        doctor.run(None, probes=probes(checkout_root=lambda: root)), "repo.commit_hook"
    )
    assert finding.status is doctor.Status.FAIL
    assert "did not complete" not in finding.detail, "the blanket rescue answered"
    assert "cannot be resolved" in finding.detail


def test_a_slot_holds_a_volume_when_a_symlink_in_it_names_a_real_mount(tmp_path):
    """The symlink leg, driven against the REAL mount seam rather than a fixture's.

    FOUND BY MUTATION, and it is the guard-covered-by-a-guard shape again one
    layer down: the synthetic-volumes fixture answers ``is_mount_point`` with
    ``Path(path).resolve() in mounted``, so the fixture was already resolving and
    dropping this leg killed nothing. What the leg exists for is only visible
    against the real function, which answers False for a symlink by contract.

    Both directions, because refusing here would refuse the ordinary macOS
    install: the boot volume has its own entry in the mount directory, as a
    symlink to ``/``.
    """
    from cratekit.core import preflight

    mount = Path(tmp_path.anchor)
    to_a_mount = tmp_path / "alias-to-a-real-mount"
    to_a_mount.symlink_to(mount, target_is_directory=True)
    ordinary = tmp_path / "ordinary"
    ordinary.mkdir()
    to_a_directory = tmp_path / "alias-to-an-ordinary-directory"
    to_a_directory.symlink_to(ordinary, target_is_directory=True)

    # The seam itself is unchanged: a symlink is never a mount point.
    assert preflight.is_mount_point(to_a_mount) is False
    assert preflight.is_mount_point(to_a_directory) is False

    # The QUESTION the rule asks is whether a volume is behind the slot.
    assert preflight.slot_holds_a_volume(mount) is True
    assert preflight.slot_holds_a_volume(to_a_mount) is True
    assert preflight.slot_holds_a_volume(to_a_directory) is False
    assert preflight.slot_holds_a_volume(ordinary) is False


def test_setup_leaves_under_the_code_a_refusing_check_reserved(monkeypatch, tmp_path):
    """The wizard ends on doctor's verdict, so it inherits doctor's exit code.

    Writing PRECONDITION into this envelope would drop a reserved code exactly as
    it did one module over, and the wizard is the verb a first run meets, so the
    code it leaves under is the first thing a script wrapping it branches on.
    """
    root = tmp_path / "fresh"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setattr(doctor, "Probes", lambda: probes())
    monkeypatch.setattr(doctor, "CHECKS", (_refusing_check(),))

    code, out, err = drive(
        [
            "--output", "json", "setup",
            "--library-root", str(root),
            "--volume-id", VOLUME,
            "--db-path", str(root / "db" / "master.db"),
            "--staging", str(tmp_path / "staging"),
            "--profile", "slim",
            "--taxonomy", "default",
        ]
    )
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), err
    assert json.loads(out)["cause"]["reason"] == "library-volume-unmounted"


# ═══════════════════════════════════════════════════════════════════════════
# Round eight: the channel a refusal travels when nothing is RAISED
# ═══════════════════════════════════════════════════════════════════════════
#
# Round seven put the classification at the constructor every ``CratekitError``
# passes through, which covers every site that raises. It does not cover the
# sites that REPORT: a check, and every branch of the wizard, answers by building
# a ``doctor.Finding`` and returning, so the exception is caught and never
# re-raised and ``cause.classified`` never sees it. The gap was not evenly
# spread. It sat on the one site in the wizard that WRITES to the library volume,
# which is where EROFS actually arises, and that site hard coded "grant this
# interpreter access" for a volume no grant can change.


def test_a_finding_that_carries_a_refusal_is_classified_where_it_is_built(tmp_path):
    """The channel, at the object that owns it, rather than at one call site.

    The previous four rounds each fixed this class of miss at the site that
    happened to be found, and it recurred at the next site. A ``Finding`` is the
    only way a check or the wizard reports, so this is the whole channel: hand it
    the exception and the act follows the kind, whatever the site wrote.

    THREE KINDS, ONE OF THEM ON A REAL READ ONLY VOLUME. Each is driven from a
    real refusal by the operating system rather than from a constructed
    exception, and each site is given the WRONG token on purpose, because a test
    that passes the right token cannot tell a classification from an assignment.
    """
    sealed = tmp_path / "sealed.toml"
    sealed.write_text("x = 1\n", encoding="utf-8")
    sealed.chmod(0o000)
    try:
        try:
            sealed.open("rb")
        except OSError as exc:
            refused = exc
        else:
            raise AssertionError("a 0o000 file opened, so the arrangement is void")

        finding = doctor.Finding(
            key="setup.taxonomy",
            title="active taxonomy template",
            status=doctor.Status.FAIL,
            detail="the template could not be read",
            # The site's own reading, deliberately the token for a different act.
            remedy=Remedy.REMOUNT_WRITABLE,
            error=refused,
        )
    finally:
        sealed.chmod(0o600)

    assert finding.remedy is Remedy.GRANT_PATH_ACCESS
    assert finding.cause is not None, "a failing refusal must reach the envelope as one"
    assert finding.cause.reason == "path-permission-denied"
    assert finding.cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert finding.cause.detail["path"] == str(sealed)
    assert finding.cause.detail["check"] == "setup.taxonomy"

    # A real read only volume, which is this machine's own system volume.
    try:
        os.mkdir("/cratekit-u27-finding-probe")
    except OSError as exc:
        read_only = exc
    else:  # pragma: no cover - only on a machine with a writable root volume
        os.rmdir("/cratekit-u27-finding-probe")
        raise AssertionError("this machine's root volume is writable, so it proves nothing")
    assert read_only.errno == errno.EROFS

    on_a_read_only_volume = doctor.Finding(
        key="setup.taxonomy",
        title="active taxonomy template",
        status=doctor.Status.FAIL,
        detail="the template could not be written",
        remedy=Remedy.GRANT_PATH_ACCESS,
        error=read_only,
    )
    assert on_a_read_only_volume.remedy is Remedy.REMOUNT_WRITABLE
    assert on_a_read_only_volume.cause.reason == "path-read-only"

    # And a finding about something the operating system did not refuse is left
    # exactly as its site built it, because there is no kind to follow.
    ordinary = doctor.Finding(
        key="taxonomy.active",
        title="active taxonomy template",
        status=doctor.Status.FAIL,
        detail="the file is not valid TOML",
        remedy=Remedy.REPORT_DEFECT,
        error=ValueError("not a refusal"),
    )
    assert ordinary.remedy is Remedy.REPORT_DEFECT
    assert ordinary.cause is None

    # A finding carrying no exception at all is the ordinary case and is inert.
    assert (
        doctor.Finding(
            key="k", title="t", status=doctor.Status.FAIL, detail="d", remedy=Remedy.RUN_DOCTOR
        ).remedy
        is Remedy.RUN_DOCTOR
    )


def test_the_seed_on_a_read_only_library_volume_is_not_sent_to_full_disk_access(monkeypatch):
    """F1. THE ONE SITE IN THE WIZARD THAT WRITES, WHICH IS WHERE EROFS ARISES.

    ``_seed_taxonomy`` is the only thing ``crate setup`` puts on the library
    volume, so it is the only place in the verb a read only volume can be met,
    and it hard coded ``grant-path-access`` and closed its sentence with "Give
    this interpreter write access to that directory". Full Disk Access cannot
    make a write to a read only volume succeed. The sentence even named the read
    only case, as one of two possibilities, and then gave the advice for the
    other one.

    THE VOLUME IS REAL. Every current macOS mounts its system volume read only,
    so a library root at ``/`` refuses the state directory with the kernel's own
    EROFS, and the test asserts that rather than assuming it.
    """
    # Over the suite-wide override, which RELOCATES ``library.root`` on every
    # load: without this the configuration built below would name a writable
    # temporary directory and the test would assert about the wrong disk (P2).
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, "/")
    # The one test that aims a write outside the temporary root on purpose, at a
    # volume the kernel refuses, so the R-926 guard is widened for it alone.
    monkeypatch.setattr(config, "_TEST_WRITE_ROOT", Path("/"))
    cfg = config.from_dict(document_for(Path("/")))
    state = config.state_path("taxonomy_active", cfg)
    assert state.parent.parent == Path("/.cratekit"), state

    try:
        os.mkdir("/cratekit-u27-seed-probe")
    except OSError as exc:
        assert exc.errno == errno.EROFS, (
            f"this machine's root volume answered {exc.errno} rather than EROFS, "
            f"so the arrangement is not a read only volume"
        )
    else:  # pragma: no cover - only on a machine with a writable root volume
        os.rmdir("/cratekit-u27-seed-probe")
        raise AssertionError("this machine's root volume is writable, so it proves nothing")

    wizard = setup_verb._Wizard({}, silent())
    setup_verb._seed_taxonomy(wizard, cfg, probes())

    note = next(n for n in wizard.notes if n.key == "setup.taxonomy")
    assert note.status is doctor.Status.FAIL
    assert note.remedy is Remedy.REMOUNT_WRITABLE, "a read only volume is not a grant"
    assert "Full Disk Access" not in note.detail
    assert "mounted read only" in note.detail
    assert "/.cratekit" in note.detail

    # The one-line fix a person reads is the act for THIS kind.
    assert "Full Disk Access" not in render.remedy_text(note.remedy)

    # And the envelope carries it: before this the wizard's report reached the
    # boundary as "N checks are failing" with a null remedy, because a note built
    # a Finding and ``failure_cause`` had no cause to read.
    cause = doctor.failure_cause(doctor.Report(tuple(wizard.notes)), origin="cli.setup")
    assert cause.reason == "path-read-only"
    assert cause.remediation.remedy is Remedy.REMOUNT_WRITABLE
    assert cause.detail["access"] == "read-only"
    assert not state.exists()


def test_a_path_no_filesystem_can_represent_is_answered_rather_than_raised():
    """F3. A GUARD ROUND SEVEN WROTE TWICE, IN THE MODULE IT DID NOT WRITE IT IN.

    ``os.lstat`` and ``os.open`` reject a path with an embedded null before any
    syscall is made, and they reject it with ``ValueError`` rather than with an
    ``OSError``. Both are reached from ``access_refusal``, which is read INSIDE
    the dispatcher's own ``except CratekitError`` handler: an exception escaping
    there replaces a refusal the user could act on with a traceback. Round seven
    guarded exactly this input twice in ``core/preflight`` and left it in the
    module it rewrote.

    LATENT RATHER THAN LIVE, AND SAID SO. No real syscall produces an ``OSError``
    carrying a null in ``filename``, and ``sqlite3.connect`` raises the
    ``ValueError`` before any ``sqlite3.Error`` exists, so the last assertion
    below is the only one built from a constructed exception and it is here
    because the guard is cheap and the failure mode is the worst shape there is.
    """
    from cratekit.core import cause as cause_module

    unrepresentable = "/tmp/cratekit-u27\0probe"

    # The two real functions really do raise, so the guards are not decorative.
    with pytest.raises(ValueError):
        os.lstat(unrepresentable)
    with pytest.raises(ValueError):
        os.open(unrepresentable, os.O_RDONLY)

    # And the two seams answer instead, exactly as ``os.path.ismount`` does.
    assert os.path.ismount(unrepresentable) is False
    assert cause_module._immutable(unrepresentable) is False
    assert cause_module._probe_readable(unrepresentable) is None
    assert cause_module._probe_writable(unrepresentable) is None

    # Constructed, because no syscall can carry one: the classification answers
    # rather than raising through the handler that is reading it.
    assert cause_module.access_refusal(
        PermissionError(errno.EACCES, "Permission denied", unrepresentable)
    ) == cause_module.AccessRefusal(
        kind=cause_module.AccessKind.PERMISSION, path=unrepresentable
    )


def test_the_write_probe_classifies_every_way_a_write_is_refused(tmp_path):
    """What the WRITE CAPABLE handle buys, pinned, because nothing pinned it.

    Measured 2026-08-14: forcing every probe to read only killed ZERO tests out
    of 5044 collected. So the one behaviour that makes ``_probe_writable``
    different from ``_probe_readable``, and the reason the reports allowlist
    guard still names it, was not asserted anywhere. That is the worst state for
    a decision to be taken in, because every candidate resolution changes this
    behaviour and the suite would have stayed green through all of them.

    These are the cases a write can be refused while a READ still succeeds, which
    is exactly the set a read only probe cannot answer. The read only volume is
    the one no file mode can imitate and it has its own test above; here it is
    the file mode, the immutable flag and an ACL, driven rather than constructed.

    THIS TEST PINS BEHAVIOUR AND TAKES NO SIDE ON R-80. If the write capable
    handle is later replaced, this is the test that has to keep passing, and a
    replacement that cannot hold all three rows is a replacement that changed
    what the user is told.
    """
    import subprocess

    from cratekit.core.cause import AccessKind, _probe_readable, _probe_writable

    # 1. Readable and not writable by MODE. The commonest shape.
    mode = tmp_path / "mode.db"
    mode.write_bytes(b"x")
    mode.chmod(0o444)
    assert _probe_readable(str(mode)) is None, "the read probe cannot see this"
    refused = _probe_writable(str(mode))
    assert refused is not None and refused.kind is AccessKind.PERMISSION
    assert refused.path == str(mode)

    # 2. The immutable flag, which is what Finder's Locked checkbox writes. It
    #    answers EPERM rather than EACCES and routes to a different act.
    locked = tmp_path / "locked.db"
    locked.write_bytes(b"x")
    if subprocess.run(["chflags", "uchg", str(locked)]).returncode == 0:
        try:
            assert _probe_readable(str(locked)) is None
            found = _probe_writable(str(locked))
            assert found is not None and found.kind is AccessKind.LOCKED
        finally:
            subprocess.run(["chflags", "nouchg", str(locked)], check=False)

    # 3. An ACL denying write while the mode still allows it, so the mode bits
    #    and the answer disagree. Skipped where chmod cannot set one.
    acl = tmp_path / "acl.db"
    acl.write_bytes(b"x")
    denied = subprocess.run(
        ["chmod", "+a", "everyone deny write,append", str(acl)],
        capture_output=True,
    )
    if denied.returncode == 0:
        assert oct(acl.stat().st_mode)[-3:] == "644", "the mode still says writable"
        assert _probe_readable(str(acl)) is None
        found = _probe_writable(str(acl))
        assert found is not None and found.kind is AccessKind.PERMISSION

    # And the negative row, so the three above are not passing on a probe that
    # refuses everything.
    ordinary = tmp_path / "ordinary.db"
    ordinary.write_bytes(b"x")
    assert _probe_writable(str(ordinary)) is None


def test_the_write_probe_names_the_medium_rather_than_the_account():
    """The fourth way a write is refused, and the one no file mode can imitate.

    R-80 was resolved by replacing the write capable handle with three metadata
    readings, and a mutation table then measured the read only branch of those
    three at ZERO deaths: dropping it left every test green while a read only
    volume started reporting as a permission. That is the one answer of the three
    a user cannot act on if it is wrong, because no amount of Full Disk Access
    makes a read only volume writable.

    The arrangement is REAL and is not built here. Every current macOS mounts its
    system volume read only, so ``/usr/bin/true`` sits on a medium that refuses
    every writer on the machine, and the test asserts that rather than assuming
    it. The file is also mode 555 and owned by root, which is what makes the row
    bite: with the read only branch removed the probe still refuses the write and
    refuses it as a PERMISSION, sending the user to grant an access that would
    change nothing.
    """
    from cratekit.core.cause import AccessKind, _probe_readable, _probe_writable

    on_the_system_volume = "/usr/bin/true"
    assert os.path.exists(on_the_system_volume), (
        "this machine has no /usr/bin/true, so the arrangement is not the one "
        "this test names"
    )
    assert os.statvfs(on_the_system_volume).f_flag & os.ST_RDONLY, (
        "this machine's system volume is writable, so it proves nothing"
    )
    assert _probe_readable(on_the_system_volume) is None, "the read probe can see it"

    refused = _probe_writable(on_the_system_volume)
    assert refused is not None
    assert refused.kind is AccessKind.READ_ONLY, (
        "a medium that refuses every writer was reported as this account's "
        "permission, which is an act the user can take and that cannot work"
    )
    assert refused.remedy is Remedy.REMOUNT_WRITABLE
    assert refused.path == on_the_system_volume


def test_the_write_probe_answers_for_a_path_it_cannot_reach_at_all(tmp_path):
    """The read probe delegation, which is the only thing that answers here.

    R-80's replacement asks the read probe first and returns its classification
    when a read is itself refused. Every metadata reading below that line needs
    to reach the path, and a parent directory denying traversal refuses all three
    of them: ``os.statvfs``, ``os.lstat`` and ``os.access`` all answer EACCES, so
    without the delegation the probe returns None and the refusal reaches the
    user as an unanticipated failure.

    LATENT RATHER THAN LIVE, AND SAID SO. The one caller reaches this function
    only after ``sqlite3`` opened the database and then refused a write, so the
    parent was traversable a moment earlier and something changed it in between.
    That is a race rather than an ordinary arrangement. It is pinned because the
    delegation costs one branch, because a mutation table measured its removal at
    zero deaths, and because the failure it prevents is the worst shape there is:
    a real refusal reported as a defect in this program.
    """
    from cratekit.core.cause import AccessKind, _probe_writable

    sealed = tmp_path / "sealed"
    sealed.mkdir()
    target = sealed / "library.db"
    target.write_bytes(b"x")
    sealed.chmod(0o000)
    try:
        assert (os.statvfs(str(sealed)).f_flag & os.ST_RDONLY) == 0, (
            "this temporary directory is on a read only volume, so the read only "
            "branch would answer before the delegation does"
        )
        refused = _probe_writable(str(target))
    finally:
        sealed.chmod(0o755)

    assert refused is not None, (
        "a path this account cannot reach was answered with silence, which "
        "reaches the user as an unanticipated failure rather than as an act"
    )
    assert refused.kind is AccessKind.PERMISSION
    assert refused.path == str(target)


def test_a_two_path_refusal_names_the_side_the_operating_system_refused(tmp_path):
    """F4. DESTINATION FIRST IS RIGHT FOR A RENAME AND WRONG FOR A LINK.

    ``os.replace`` sets ``filename`` to the source and ``filename2`` to the
    destination, and the guarded writer writes every file by renaming a temporary
    one over it, so reading ``filename`` alone named a ``.tmp`` that no longer
    exists. ``os.link`` fills the same two fields in the same order and the
    refusal is on the OTHER side: with a source this account cannot reach,
    destination-first names the one path there is nothing to do about.

    So which side was refused is MEASURED, the same way a driver level error is,
    and the destination keeps precedence: it is asked first and the source is
    named only when the destination is not itself refused and the source is.
    Neither ``os.link`` nor ``os.symlink`` appears anywhere in ``src/cratekit``
    today, which is what makes this latent rather than live.
    """
    from cratekit.core import cause as cause_module

    sealed_dir = tmp_path / "sealed"
    sealed_dir.mkdir()
    source = sealed_dir / "source.bin"
    source.write_bytes(b"x")
    destination = tmp_path / "destination.bin"
    sealed_dir.chmod(0o000)
    try:
        try:
            os.link(source, destination)
        except OSError as exc:
            refused = exc
        else:
            raise AssertionError("a link out of a 0o000 directory succeeded")

        assert refused.filename == str(source), "the arrangement is not the one described"
        assert refused.filename2 == str(destination)

        refusal = cause_module.access_refusal(refused)
        assert refusal is not None
        assert refusal.path == str(source), "the refusal named the path the account can write"
        assert refusal.kind is cause_module.AccessKind.PERMISSION
    finally:
        sealed_dir.chmod(0o700)

    # THE RENAME CASE IS UNCHANGED, which is what the precedence is for: a
    # destination this account cannot write in, named ahead of the temporary file.
    unwritable = tmp_path / "unwritable"
    unwritable.mkdir()
    target = unwritable / "config.toml"
    target.write_bytes(b"y")
    temporary = tmp_path / "tmpXXXX.tmp"
    temporary.write_bytes(b"z")
    target.chmod(0o000)
    unwritable.chmod(0o500)
    try:
        try:
            os.replace(temporary, target)
        except OSError as exc:
            renamed = exc
        else:
            raise AssertionError("a rename into a 0o500 directory succeeded")
        found = cause_module.access_refusal(renamed)
        assert found is not None
        assert found.path == str(target), "the user was sent to a temporary file again"
    finally:
        unwritable.chmod(0o700)
        target.chmod(0o600)


def test_a_copy_that_gave_up_on_one_member_is_classified_by_its_paths(tmp_path):
    """F5. THE ONE REFUSAL IN THE PACKAGE THAT ARRIVES AS RENDERED TEXT.

    ``shutil.copytree`` does not raise the refusal it met. It collects every
    member it could not copy and raises one ``shutil.Error`` at the end whose
    single argument is a list of ``(source, destination, why)`` triples, and
    ``why`` has already been rendered to a string. Measured on this platform that
    exception IS an ``OSError`` subclass, contrary to the shape one would guess
    from its behaviour, and it carries ``errno``, ``filename`` and ``filename2``
    all None and no ``__cause__``, so every errno rule in the module answered
    None for it.

    ``core/snapshot`` copies each declared capture source with exactly this call
    and does not guard it, so a sealed member of a declared source reached the
    dispatcher's blanket as "this is a defect; report it". The paths survive the
    rendering even though the errno does not, so the paths are what is measured.
    """
    import shutil

    from cratekit.core import cause as cause_module

    tree = tmp_path / "source"
    (tree / "inner").mkdir(parents=True)
    member = tree / "inner" / "member.bin"
    member.write_bytes(b"z")
    member.chmod(0o000)
    try:
        try:
            shutil.copytree(tree, tmp_path / "captured")
        except shutil.Error as exc:
            gave_up = exc
        else:
            raise AssertionError("a 0o000 member copied, so the arrangement is void")

        # The shape the classification has to work from, stated rather than assumed.
        assert isinstance(gave_up, OSError)
        assert gave_up.errno is None
        assert gave_up.filename is None
        assert gave_up.__cause__ is None

        refusal = cause_module.access_refusal(gave_up)
        assert refusal is not None, "a sealed member was read as an unanticipated failure"
        assert refusal.path == str(member)
        assert refusal.kind is cause_module.AccessKind.PERMISSION
        assert refusal.remedy is Remedy.GRANT_PATH_ACCESS

        # And it travels the whole way: the dispatcher's blanket is what an
        # unguarded copy actually reaches.
        from cratekit import cli as cli_module

        blanket = cli_module._unhandled_cause(gave_up)
        assert blanket.reason == "path-permission-denied"
        assert blanket.remediation.remedy is Remedy.GRANT_PATH_ACCESS
        assert str(member) in blanket.message
    finally:
        member.chmod(0o600)


# ═══════════════════════════════════════════════════════════════════════════
# Round eight, verified independently: the two answers a double cannot give
# ═══════════════════════════════════════════════════════════════════════════
#
# Everything above answers the mount question through ``Probes``, which is the
# right seam for driving twenty three checks over seven mount states without a
# second disk. It cannot answer two things, and both are load bearing here:
#
# * whether the DISTINCTION between an unmounted volume and a moved one survives
#   contact with a real volume identity, the kernel's own mount table, and a real
#   detach. A stubbed identity provider agrees with itself by construction.
# * whether a volume that refuses writes at the MOUNT, with EROFS, reaches the
#   user as "remount it" rather than as "grant this interpreter access". A chmod
#   cannot stand in: it produces EACCES, which is the other kind, and it is the
#   kind whose advice is correct. Only a read only mount refuses the file's owner
#   and every other account on the machine alike.
#
# These FAIL rather than skip when hdiutil is missing, because a skipped hardware
# proof is indistinguishable from a passing one in every summary anybody reads.


def _require_hdiutil() -> None:
    if not hdiutil_available():
        pytest.fail(
            "hdiutil is required to prove these two answers against real mounts "
            "and it is missing here. It ships with macOS, which is the platform "
            "this unit targets first. This fails rather than skips because a "
            "skipped hardware proof reads as a passing one."
        )


def _library_on(volume: Path) -> None:
    """What ``read_only_volume`` writes while the image is still writable."""
    (volume / "library" / "Music").mkdir(parents=True)


def test_an_unmounted_volume_and_a_moved_volume_are_told_apart_on_a_real_volume(tmp_path):
    """The brief's second scenario, driven with nothing about the disk stubbed.

    Four outcomes off ONE real volume, using the platform's own identity call and
    the kernel's own mount table:

    * the configured root is a directory on the mounted volume: OK;
    * the volume is mounted and the configured root is not a directory on it:
      LIBRARY_PATH_MISSING, the library moved WITHIN the volume;
    * the configured root's mount point does not exist and the volume is attached
      somewhere else: MOUNTED_ELSEWHERE, found at the place it actually is;
    * the same configured root after the volume is DETACHED: NOT_MOUNTED.

    The last two are the pair the brief singles out and the pair one "the volume
    is wrong" sentence conflates. One is fixed by plugging a drive in and the
    other by editing a path, so a report that cannot tell them apart sends a user
    to unplug a drive that was never the problem.

    The identity is REAL: ``macos_volume_identity`` reads it through
    ``getattrlist(2)`` off the mounted image, and it outlives the detach in this
    test's own variable, which is the entire property that makes it an identity
    rather than a coincidence.
    """
    _require_hdiutil()

    from cratekit.core import preflight

    identity_of = preflight.macos_volume_identity
    gone_root = tmp_path / "no-such-mount-point" / "library"

    with read_only_volume(_library_on) as volume:
        # The mount TABLE, never a behaviour probe: the macOS FAT driver allows
        # symlinks, so probing behaviour to identify a filesystem is measured
        # wrong on this platform and the habit is what this asks instead.
        assert filesystem_kind(volume) == "hfs", filesystem_kind(volume)

        recorded = identity_of(volume)
        assert recorded, (
            "the fixture volume reports no identity through getattrlist, so this "
            "test would be asserting about IDENTITY_UNAVAILABLE rather than about "
            "the distinction it names"
        )

        on_it = preflight.resolve_mount_state(
            volume / "library", recorded, identity_provider=identity_of
        )
        moved_within = preflight.resolve_mount_state(
            volume / "not-that-folder", recorded, identity_provider=identity_of
        )
        elsewhere = preflight.resolve_mount_state(
            gone_root,
            recorded,
            identity_provider=identity_of,
            mount_enumerator=preflight.local_mount_points,
        )

    # Detached here, which is an unplugged drive arranged the only way that is
    # not a simulation of one.
    unmounted = preflight.resolve_mount_state(
        gone_root,
        recorded,
        identity_provider=identity_of,
        mount_enumerator=preflight.local_mount_points,
    )

    assert on_it.state is preflight.MountState.OK, on_it
    assert moved_within.state is preflight.MountState.LIBRARY_PATH_MISSING, moved_within
    assert elsewhere.state is preflight.MountState.MOUNTED_ELSEWHERE, elsewhere
    assert unmounted.state is preflight.MountState.NOT_MOUNTED, unmounted

    # The moved answer says WHERE, which is the whole difference in what the user
    # does next. The unmounted answer has no such place to name.
    assert elsewhere.found_at is not None
    assert unmounted.found_at is None

    # The two sentences a user reads over the same configured root are different
    # sentences carrying different acts.
    moved_detail = doctor._MOUNT_DETAIL[elsewhere.state]
    absent_detail = doctor._MOUNT_DETAIL[unmounted.state]
    assert moved_detail != absent_detail
    assert "Nothing needs plugging in" in moved_detail
    assert "Attach it" in absent_detail

    # And both refuse a library state read, so nothing downstream reports on a
    # template it read off a disk nobody looked at.
    assert not preflight.library_state_is_readable(elsewhere)
    assert not preflight.library_state_is_readable(unmounted)


def test_a_real_read_only_volume_reaches_the_user_as_remount_not_as_a_permission(
    monkeypatch,
):
    """The wizard's write onto the library volume, refused at the MOUNT.

    THIS IS THE SITE ROUND EIGHT WAS ABOUT. Every branch of the wizard used to
    close with "Give this interpreter write access to that directory", hard
    coded, and the branch that says it is the branch that writes to the library
    volume, which is where EROFS actually arises. No permission grant changes a
    read only mount, so that advice is not a lesser answer: it is an act the user
    can carry out in full and be no better off for.

    All three channels are asserted, because round eight is the round that
    discovered they can disagree: the remedy TOKEN a machine consumer reads, the
    structured cause the envelope carries, and the sentence a person reads. The
    negative assertions are the load bearing ones.
    """
    _require_hdiutil()

    from cratekit.core.cause import AccessKind

    with read_only_volume(_library_on) as volume:
        root = volume / "library"
        monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
        cfg = config.from_dict(document_for(root))

        wizard = setup_verb._Wizard({}, silent())
        setup_verb._seed_taxonomy(wizard, cfg, probes())

        failures = [note for note in wizard.notes if note.status is doctor.Status.FAIL]
        assert len(failures) == 1, [note.detail for note in wizard.notes]
        note = failures[0]

        # 1. The token. GRANT_PATH_ACCESS is what the branch hard codes; the kind
        #    the operating system made is what decides.
        assert note.remedy is Remedy.REMOUNT_WRITABLE, note.remedy

        # 2. The structured cause, so a failing check does not reach the envelope
        #    as "N checks are failing" with a null remedy.
        assert note.cause is not None, note.detail
        assert note.cause.reason == "path-read-only"
        assert note.cause.remediation.remedy is Remedy.REMOUNT_WRITABLE
        assert note.cause.detail["access"] == str(AccessKind.READ_ONLY)
        # The path named is ON the volume that refused, which is the actionable
        # content. WHICH file on it is a separate and separately recorded question.
        assert str(volume) in note.cause.detail["path"]

        # 3. The sentence. This is the assertion that would have caught the
        #    defect, because the wording and the token are free to disagree.
        assert "mounted read only" in note.detail
        assert "no permission grant can change that" in note.detail
        assert "Full Disk Access" not in note.detail
        assert "Grant this interpreter" not in note.detail

        # And nothing was written, which is the other half of a refusal: the tool
        # did not half create the library's own state on a volume it cannot write.
        assert not config.state_path("taxonomy_active", cfg).exists()


def test_the_read_only_refusal_and_the_permission_refusal_do_not_share_an_act(
    tmp_path, monkeypatch
):
    """The pair, because a single kind assertion cannot fail the way this failed.

    The defect was ONE wording for every kind, so a test that only ever meets one
    kind passes straight over it. EROFS comes from a real read only mount and
    EACCES from a directory this account may not write, through the same wizard
    branch, and the two answers have to differ in the token and in the closing
    sentence both.
    """
    _require_hdiutil()

    sealed_root = tmp_path / "sealed" / "library"
    (sealed_root / "Music").mkdir(parents=True)

    def note_for(root: Path) -> doctor.Finding:
        monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
        cfg = config.from_dict(document_for(root))
        wizard = setup_verb._Wizard({}, silent())
        setup_verb._seed_taxonomy(wizard, cfg, probes())
        return next(note for note in wizard.notes if note.status is doctor.Status.FAIL)

    sealed_root.chmod(0o500)
    try:
        permission = note_for(sealed_root)
    finally:
        sealed_root.chmod(0o700)

    with read_only_volume(_library_on) as volume:
        read_only = note_for(volume / "library")

    assert permission.remedy is Remedy.GRANT_PATH_ACCESS, permission.detail
    assert read_only.remedy is Remedy.REMOUNT_WRITABLE, read_only.detail
    assert permission.remedy is not read_only.remedy
    assert "Full Disk Access" in permission.detail
    assert "Full Disk Access" not in read_only.detail


def test_the_driver_path_to_the_write_probe_is_driven_on_a_real_read_only_volume():
    """The whole producer chain for the write probe, on real hardware.

    The three metadata readings that replaced R-80's write capable handle are
    pinned individually above. This drives the chain that reaches them, which
    nothing did: a real ``sqlite3`` database on a real read only mount, a real
    write attempt, the driver's own ``SQLITE_READONLY``, and the classification
    that comes back out of ``access_refusal``.

    IT IS THE ONLY WAY THIS FUNCTION IS REACHED IN THE PRODUCT. ``_probe_writable``
    has one caller and that caller is a driver level error, so a test that calls
    the probe directly proves the answer and not the route. The route is what
    round eight's whole vocabulary rests on: the driver carries no errno, no
    filename and no cause, and if the path attribute does not survive the hop
    then every one of these classifications answers None no matter how right the
    probe is.
    """
    _require_hdiutil()

    import sqlite3

    from cratekit.core.cause import AccessKind, access_refusal, name_the_database

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
            "not the one this test names"
        )
        assert getattr(refused, "sqlite_errorname", "") == "SQLITE_READONLY", (
            f"the driver answered {getattr(refused, 'sqlite_errorname', None)}, "
            f"which routes to the READ probe and not to the one under test"
        )

        # The hop the whole vocabulary rests on: the connection site is the only
        # place that knows the path, so it attaches it and the classifier reads it.
        name_the_database(refused, database)
        refusal = access_refusal(refused)

        assert refusal is not None, (
            "a driver level refusal on a read only volume reached the user as an "
            "unanticipated failure"
        )
        assert refusal.kind is AccessKind.READ_ONLY, (
            "the medium refused every writer and the user was told to grant this "
            "account an access that cannot change it"
        )
        assert refusal.path == str(database)
        assert refusal.remedy is Remedy.REMOUNT_WRITABLE


# ── taxonomy.schema: the copy against the shipped schema (U132) ─────────────
#
# The live library's copy stated schema_version 2 with no genre Favorites class
# after one shipped, and doctor said only that it parsed. These name the gap,
# what the upgrade would add, and the hand edit for what it holds.


def _schema_finding(cfg: config.Config) -> doctor.Finding:
    return find(doctor.run(cfg, probes=probes()), "taxonomy.schema")


def test_a_version_2_copy_without_favorites_is_named_with_both_versions(configured):
    from tests.test_taxonomy_upgrade import live_shaped

    write_active(configured, live_shaped())
    finding = _schema_finding(configured)
    assert finding.status is doctor.Status.INFO
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
    finding = _schema_finding(configured)
    assert finding.status is doctor.Status.OK
    assert "schema_version 5" in finding.detail


def test_a_copy_that_does_not_parse_is_left_to_taxonomy_active(configured):
    write_active(configured, "schema_version = 2\n[tree\n")
    finding = _schema_finding(configured)
    assert finding.status is doctor.Status.INFO
    assert finding.detail.startswith("not compared")
    assert find(doctor.run(configured, probes=probes()), "taxonomy.active").status is doctor.Status.FAIL


def test_the_schema_is_not_compared_when_the_library_disk_is_absent(configured):
    seed_taxonomy(configured)
    gone = probes(identity_provider=lambda _p: "0000-0000", mount_enumerator=lambda: ())
    finding = find(doctor.run(configured, probes=gone), "taxonomy.schema")
    assert finding.status is doctor.Status.INFO
    assert "schema_version" not in finding.detail


def test_a_library_with_no_copy_routes_by_the_shipped_template_and_is_current(configured):
    assert not config.state_path("taxonomy_active", configured).exists()
    finding = _schema_finding(configured)
    assert finding.status is doctor.Status.OK
    assert "no active taxonomy copy" in finding.detail
    assert "'default' template, which is current" in finding.detail


def test_a_shipped_template_that_cannot_be_read_is_named_and_not_the_copy(
    configured, monkeypatch
):
    seed_taxonomy(configured)

    def unreadable(_name):
        raise OSError("the package data is missing")

    monkeypatch.setattr(taxonomy, "shipped_template_text", unreadable)
    finding = _schema_finding(configured)
    assert finding.status is doctor.Status.INFO
    assert "shipped template 'default' could not be read" in finding.detail
    assert "taxonomy.template" in finding.detail
    assert "taxonomy.active" not in finding.detail


def test_a_shipped_template_that_does_not_load_is_a_defect_and_not_the_copy(
    configured, monkeypatch
):
    seed_taxonomy(configured)
    shipped = taxonomy.shipped_template_text("default")
    monkeypatch.setattr(
        taxonomy, "shipped_template_text", lambda _n: shipped.replace('id = "rnb"', 'id = "R and B"', 1)
    )
    finding = _schema_finding(configured)
    assert finding.status is doctor.Status.FAIL
    assert finding.remedy is Remedy.REPORT_DEFECT
    assert "shipped" in finding.detail



def test_the_bandcamp_session_check_names_the_verbs_that_spend_it(configured):
    """U176, review round two. No verb declares the Bandcamp session, so it is
    never required, and the finding must not say no verb needs it: the two
    Bandcamp verbs do, and refuse without it."""
    inputs = doctor._Inputs(configured, None, probes(credential_recorded=lambda _name: False))
    finding = doctor._check_credential("credential.bandcamp", inputs)
    assert finding.status is doctor.Status.INFO
    assert "crate acquire bandcamp and crate acquire bandcamp-fetch" in finding.detail
    assert "no verb" not in finding.detail
    other = doctor._check_credential("credential.recognition", inputs)
    assert other.status is doctor.Status.FAIL or "no verb" in other.detail


# ---------------------------------------------------------------------------
# U159: install.release, whether a newer release than this copy is published
# ---------------------------------------------------------------------------

_REPO_URL = "https://github.com/philgutowski/cratekit"


def _release_finding(origin, tags=None, *, read=None):
    seen = []

    def release_tags(url):
        seen.append(url)
        return tags if read is None else read(url)

    inputs = doctor._Inputs(
        None, None, probes(install_origin=lambda: origin, release_tags=release_tags)
    )
    return doctor._check_release(inputs), seen


def _vcs(version="0.2.0", extras=()):
    return doctor.InstallOrigin(kind="vcs", version=version, url=_REPO_URL, extras=extras)


def test_a_newer_release_warns_with_the_one_pipx_command_keeping_the_extras():
    finding, seen = _release_finding(
        _vcs("0.2.0", ("analysis", "vocals")), ("v0.1.0", "v0.2.0", "v0.3.0")
    )
    assert seen == [_REPO_URL]
    assert finding.status is doctor.Status.INFO, "a copy behind a release still works"
    assert "v0.3.0" in finding.detail and "0.2.0" in finding.detail
    assert (
        f'pipx install --force "cratekit[analysis,vocals] @ git+{_REPO_URL}@v0.3.0"'
        in finding.detail
    )


def test_a_newer_release_without_extras_names_plain_cratekit():
    finding, _ = _release_finding(_vcs("0.2.0"), ("v0.2.1",))
    assert f'pipx install --force "cratekit @ git+{_REPO_URL}@v0.2.1"' in finding.detail


@pytest.mark.parametrize("tags", [("v0.2.0",), ("v0.1.9", "v0.2.0"), ("v0.1.0",)])
def test_an_equal_or_newer_installed_version_passes(tags):
    finding, _ = _release_finding(_vcs("0.2.0"), tags)
    assert finding.status is doctor.Status.OK
    assert "latest release" in finding.detail


def test_no_tags_passes_and_says_none_is_published():
    finding, _ = _release_finding(_vcs("0.1.0"), ())
    assert finding.status is doctor.Status.OK
    assert "no release has been published" in finding.detail


def test_a_failed_read_says_it_could_not_read_and_never_passes():
    finding, _ = _release_finding(_vcs("0.1.0"), read=lambda _url: None)
    assert finding.status is not doctor.Status.OK, (
        "a check that could not look reported the copy as current"
    )
    assert finding.status is doctor.Status.INFO
    assert "could not be read" in finding.detail
    assert "unknown" in finding.detail


def test_tags_that_are_not_versions_are_ignored():
    finding, _ = _release_finding(
        _vcs("0.2.0"), ("v0.2.0", "nightly", "v9", "v10.0.0-rc1", "release-11.0.0", "v1.0")
    )
    assert finding.status is doctor.Status.OK
    assert "v0.2.0" in finding.detail


@pytest.mark.parametrize(("kind", "said"), [("editable", "editable checkout"), ("folder", "a folder")])
def test_a_folder_or_editable_install_says_the_check_does_not_apply(kind, said):
    finding, seen = _release_finding(
        doctor.InstallOrigin(kind=kind, version="0.1.0", url="file:///somewhere"), ("v9.0.0",)
    )
    assert seen == [], "a folder install has no release to read"
    assert finding.status is doctor.Status.INFO
    assert said in finding.detail and "does not apply" in finding.detail
    assert f"git+{_REPO_URL}@" in finding.detail, "it says how to move to a release install"


@pytest.mark.parametrize("kind", ["index", "unknown"])
def test_an_install_not_from_the_repository_does_not_apply(kind):
    finding, seen = _release_finding(doctor.InstallOrigin(kind=kind), ("v9.0.0",))
    assert seen == []
    assert finding.status is doctor.Status.INFO
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
    info = tmp_path / "cratekit-0.2.0.dist-info"
    info.mkdir()
    lines = ["Metadata-Version: 2.1", "Name: cratekit", "Version: 0.2.0"]
    lines += [f"Requires-Dist: {r}" for r in requires]
    (info / "METADATA").write_text("\n".join(lines) + "\n")
    if direct_url is not None:
        (info / "direct_url.json").write_text(direct_url)
    from importlib import metadata

    return metadata.PathDistribution(info)


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
    ],
)
def test_the_install_origin_is_read_off_the_pep_610_record(tmp_path, monkeypatch, record, kind):
    dist = _distribution(tmp_path, record)
    monkeypatch.setattr(doctor.metadata, "distribution", lambda name: dist)
    origin = doctor._install_origin()
    assert origin.kind == kind
    if kind != "unknown":
        assert origin.version == "0.2.0"
    if kind == "vcs":
        assert origin.url == _REPO_URL


def test_the_installed_extras_are_the_ones_whose_requirements_are_present(tmp_path, monkeypatch):
    from importlib import metadata

    dist = _distribution(
        tmp_path,
        '{"url": "https://github.com/philgutowski/cratekit", "vcs_info": {"vcs": "git"}}',
        requires=(
            "platformdirs>=4.0",
            'librosa>=0.10; extra == "analysis"',
            'numpy>=1.24; extra == "analysis"',
            'torch>=2.2; extra == "vocals"',
            'cratekit[analysis,vocals]; extra == "all"',
        ),
    )
    present = {"cratekit", "librosa", "numpy", "platformdirs"}

    def distribution(name):
        if name == "cratekit":
            return dist
        if name in present:
            return dist
        raise metadata.PackageNotFoundError(name)

    monkeypatch.setattr(doctor.metadata, "distribution", distribution)
    assert doctor._install_origin().extras == ("analysis",), (
        "vocals is missing torch and all is an alias, so only analysis is kept"
    )


def test_the_release_read_parses_ls_remote_and_refuses_on_failure(monkeypatch):
    calls = []

    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs))
        out = "abc\trefs/tags/v0.1.0\ndef\trefs/tags/v0.2.0\n"
        return subprocess.CompletedProcess(argv, 0, out, "")

    monkeypatch.setattr(doctor.subprocess, "run", fake_run)
    assert doctor._release_tags(_REPO_URL) == ("v0.1.0", "v0.2.0")
    argv, kwargs = calls[0]
    assert argv[:3] == ["git", "ls-remote", "--tags"]
    assert kwargs["timeout"] == doctor.RELEASE_READ_TIMEOUT
    assert kwargs["env"]["GIT_TERMINAL_PROMPT"] == "0"

    def refused(argv, **kwargs):
        return subprocess.CompletedProcess(argv, 128, "", "fatal: could not read Username")

    monkeypatch.setattr(doctor.subprocess, "run", refused)
    assert doctor._release_tags(_REPO_URL) is None

    def timed_out(argv, **kwargs):
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])

    monkeypatch.setattr(doctor.subprocess, "run", timed_out)
    assert doctor._release_tags(_REPO_URL) is None


def test_an_unparseable_installed_version_is_unknown_never_a_downgrade():
    finding, _ = _release_finding(_vcs("0.2.0.dev1"), ("v0.1.0",))
    assert finding.status is doctor.Status.INFO
    assert "unknown" in finding.detail
    assert "pipx install" not in finding.detail, "it told a newer copy to downgrade"


# ═══════════════════════════════════════════════════════════════════════════
# U185. DEADCA7 beside the library
# ═══════════════════════════════════════════════════════════════════════════


def _deadca7(tmp_path, *, pushed_at: datetime | None = None, home: bool = True):
    """DEADCA7's support folder, and one backup entry written at ``pushed_at``."""
    support = tmp_path / "deadca7"
    if not home:
        return support
    backups = support / doctor.DEADCA7_BACKUPS
    backups.mkdir(parents=True)
    (backups / ".DS_Store").write_bytes(b"")
    if pushed_at is not None:
        entry = backups / "master-20261030.db"
        entry.write_bytes(b"a copy")
        os.utime(entry, (pushed_at.timestamp(), pushed_at.timestamp()))
    return support


def _push_check(configured, support) -> doctor.Finding:
    report = doctor.run(configured, probes=probes(deadca7_home=lambda: support))
    finding = find(report, "deadca7.push")
    assert finding.status is doctor.Status.INFO, finding
    return finding


def test_with_no_deadca7_support_folder_doctor_says_not_installed_and_does_not_fail(
    configured, tmp_path
):
    finding = _push_check(configured, _deadca7(tmp_path, home=False))
    assert "not installed" in finding.detail
    # A machine with no home for it at all answers the same, and never fails.
    assert "not installed" in _push_check(configured, None).detail


def test_installed_with_no_push_says_so(configured, tmp_path):
    finding = _push_check(configured, _deadca7(tmp_path))
    assert "installed here and has recorded no push" in finding.detail


def test_a_push_newer_than_the_last_database_backup_warns_and_names_the_backup(
    configured, tmp_path
):
    now = doctor_machines.green().now
    backup_facts.record(
        configured,
        backup_facts.Portion.DATABASE,
        completed_at=now - timedelta(days=3),
        destination="remote:backups",
    )
    finding = _push_check(configured, _deadca7(tmp_path, pushed_at=now - timedelta(days=1)))
    assert finding.detail.startswith("warning: DEADCA7 last pushed")
    assert "after this product's last database backup" in finding.detail
    assert "crate backup run" in finding.detail


def test_a_push_older_than_the_last_database_backup_is_held_by_it(configured, tmp_path):
    now = doctor_machines.green().now
    backup_facts.record(
        configured,
        backup_facts.Portion.DATABASE,
        completed_at=now - timedelta(days=1),
        destination="remote:backups",
    )
    finding = _push_check(configured, _deadca7(tmp_path, pushed_at=now - timedelta(days=3)))
    assert "before this product's last database backup, which holds it" in finding.detail
    assert "warning" not in finding.detail


def test_a_push_with_no_database_backup_recorded_warns(configured, tmp_path):
    now = doctor_machines.green().now
    finding = _push_check(configured, _deadca7(tmp_path, pushed_at=now - timedelta(days=1)))
    assert finding.detail.startswith("warning:")
    assert "no database backup is recorded here" in finding.detail


def test_a_backup_folder_that_cannot_be_read_is_said_as_unread_and_does_not_fail(
    configured, tmp_path
):
    support = _deadca7(tmp_path)
    (support / doctor.DEADCA7_BACKUPS / "gone").symlink_to(tmp_path / "nowhere")
    finding = _push_check(configured, support)
    assert "cannot be said: its backup folder could not be read" in finding.detail


def test_a_push_beside_a_backup_recorded_ahead_of_now_is_not_called_held(configured, tmp_path):
    now = doctor_machines.green().now
    backup_facts.record(
        configured,
        backup_facts.Portion.DATABASE,
        completed_at=now + timedelta(days=10),
        destination="remote:backups",
    )
    finding = _push_check(configured, _deadca7(tmp_path, pushed_at=now - timedelta(days=1)))
    assert "cannot be said, since that backup is recorded ahead of now" in finding.detail
    assert "which holds it" not in finding.detail


# ---------------------------------------------------------------------------
# U181: install.extras, whether the vocal model can score in this copy
# ---------------------------------------------------------------------------

_NO_EXTRA = ("extra", "the 'vocals' extra is not installed here; reinstall it")


def _extras_finding(missing, origin=None, **overrides):
    origin = origin or _vcs("0.3.0", ("analysis",))
    inputs = doctor._Inputs(
        None,
        None,
        probes(vocal_requirement=lambda: missing, install_origin=lambda: origin, **overrides),
    )
    return doctor._check_install_extras(inputs)


def test_a_copy_without_the_vocals_extra_says_so_and_prints_the_reinstall_command():
    """Sitting 51's copy: installed with analysis and not vocals, from the release."""
    finding = _extras_finding(_NO_EXTRA)
    assert finding.key == "install.extras"
    assert finding.status is doctor.Status.INFO, "it runs inside setup and must not refuse"
    assert "vocals extra is absent" in finding.detail
    assert "carry no voxlevel" in finding.detail
    assert (
        f'pipx install --force "cratekit[analysis,vocals] @ git+{_REPO_URL}@v0.3.0"'
        in finding.detail
    ), "the reinstall keeps the extra this copy carries and adds vocals, at its own tag"


def test_a_copy_whose_vocal_model_can_score_is_ok():
    finding = _extras_finding(None)
    assert finding.status is doctor.Status.OK
    assert "pipx" not in finding.detail


def test_the_row_reads_the_vocals_modules_own_probe_with_the_loader_bound_or_not(
    monkeypatch,
):
    """The scenario's two halves through the shipped seam: unbound on a machine
    with no torch reports the row and the command, bound is ok."""
    from cratekit.analysis import vocals

    monkeypatch.setattr(vocals, "_VOCAL_LOADER", None)
    monkeypatch.setattr(
        vocals, "requirement", lambda: ("extra", "the 'vocals' extra is not installed here")
    )
    inputs = doctor._Inputs(None, None, doctor.Probes(install_origin=lambda: _vcs("0.3.0")))
    unbound = doctor._check_install_extras(inputs)
    assert unbound.status is doctor.Status.INFO
    assert f'"cratekit[vocals] @ git+{_REPO_URL}@v0.3.0"' in unbound.detail

    monkeypatch.setattr(vocals, "_VOCAL_LOADER", lambda: object())
    assert doctor._check_install_extras(inputs).status is doctor.Status.OK


def test_missing_model_files_are_named_and_no_reinstall_is_offered_for_them():
    """A reinstall does not place the checkpoint, so the row does not say it would."""
    finding = _extras_finding(("files", "the vocal model checkpoint is not at the path"))
    assert finding.status is doctor.Status.INFO
    assert "checkpoint is not at the path" in finding.detail
    assert "Reinstall" not in finding.detail and "pipx" not in finding.detail


def test_a_copy_not_installed_from_a_release_gets_the_vocals_modules_own_command(
    monkeypatch,
):
    from cratekit.analysis import vocals

    monkeypatch.setattr(vocals, "install", lambda: "the vocals module's own command")
    finding = _extras_finding(_NO_EXTRA, origin=doctor.InstallOrigin(kind="editable"))
    assert "Reinstall with: the vocals module's own command" in finding.detail


def test_the_extras_row_never_fails_setup():
    for missing in (_NO_EXTRA, ("files", "the label table is not at the path"), None):
        assert not _extras_finding(missing).failed


def test_an_upgrade_adds_vocals_when_the_library_has_scored_a_track():
    """A copy that lost the extra would otherwise upgrade without it again."""
    inputs = doctor._Inputs(
        None,
        None,
        probes(
            install_origin=lambda: _vcs("0.2.0", ("analysis",)),
            release_tags=lambda _url: ("v0.3.0",),
            vocals_scored=lambda _cfg: True,
        ),
    )
    finding = doctor._check_release(inputs)
    assert (
        f'pipx install --force "cratekit[analysis,vocals] @ git+{_REPO_URL}@v0.3.0"'
        in finding.detail
    )


def test_an_upgrade_keeps_the_extras_and_adds_nothing_for_a_library_never_scored():
    inputs = doctor._Inputs(
        None,
        None,
        probes(
            install_origin=lambda: _vcs("0.2.0", ("analysis",)),
            release_tags=lambda _url: ("v0.3.0",),
            vocals_scored=lambda _cfg: False,
        ),
    )
    finding = doctor._check_release(inputs)
    assert f'"cratekit[analysis] @ git+{_REPO_URL}@v0.3.0"' in finding.detail


def test_a_library_has_scored_when_a_vocal_calibration_is_recorded(configured):
    """The shipped probe: the calibration a fit writes only from scored files."""
    from cratekit.write import metadata_cli

    assert doctor._vocals_scored(None) is False
    assert doctor._vocals_scored(configured) is False
    path = config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, configured)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"threshold": 12.0}', encoding="utf-8")
    assert doctor._vocals_scored(configured) is True


def test_a_git_install_of_a_branch_head_names_no_tag_that_does_not_exist(monkeypatch):
    """Review round one: ``@v0.3.1.dev3+g...`` is no tag, so the command is the
    vocals module's own rather than a release reinstall pipx would refuse."""
    from cratekit.analysis import vocals

    monkeypatch.setattr(vocals, "install", lambda: "the vocals module's own command")
    origin = _vcs("0.3.1.dev3+gabc1234", ("analysis",))
    assert doctor.vocals_install_command(origin) == "the vocals module's own command"
    assert "@v0.3.0" in doctor.vocals_install_command(_vcs("0.3.0", ("analysis",)))
