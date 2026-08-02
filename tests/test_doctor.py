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
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.acquire import adapter as adapter_contract
from cratekit.cli import doctor, prompt, registry, render
from cratekit.cli import setup as setup_verb
from cratekit.cli.doctor import Probes as RealProbes
from cratekit.cli.verbs import login as login_verb
from cratekit.core import backup_facts, binaries, config, profiles, secrets, session
from cratekit.core.cause import CratekitError, Outcome
from cratekit.core.exit_codes import ExitCode, Remedy

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

#: A synthetic volume identity. Shaped like a real one and belonging to nobody,
#: because R1 forbids a shipped artifact from carrying a real library string.
VOLUME = "F1E2-D3C4"


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

    Built from the class captured at IMPORT time, so a test that replaces
    ``doctor.Probes`` to feed a synthetic machine through the real dispatcher does
    not thereby replace the thing this function calls to build one.
    """
    defaults = dict(
        now=datetime(2026, 8, 2, tzinfo=timezone.utc),
        python_version=(3, 12, 4),
        requires_python=">=3.12,<3.14",
        find_binary=lambda name: f"/opt/probe/bin/{name}",
        identity_provider=lambda _path: VOLUME,
        mount_enumerator=lambda: (),
        process_lister=lambda: (),
        keychain_available=lambda: True,
        credential_recorded=lambda _name: True,
        installed_app_version=lambda _cfg: "7.0.1",
        binding_pin_problem=lambda _cfg: None,
        rclone_remotes=lambda _rclone: {},
        checkout_root=lambda: None,
    )
    defaults.update(overrides)
    return RealProbes(**defaults)


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


def test_the_check_table_and_the_keys_are_one_declaration():
    """The keys are DERIVED from the table, so the two cannot disagree."""
    assert doctor.CHECK_KEYS == tuple(check.key for check in doctor.CHECKS)


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
        name = "tidal_dl_ng"

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
        ((3, 12, 1), "", True),
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


def test_a_remote_whose_provider_trashes_on_delete_is_reported(configured):
    """R-7, closed. The source system passed a provider flag from inside the
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


def test_the_commit_hook_check_says_nothing_on_an_installed_package(library):
    """R-1 is a developer check. Reporting a missing developer tool to somebody
    who is not a developer is noise, and noise is what stops the report being read.
    """
    installed = find(
        doctor.run(config.from_dict(document_for(library)), probes=probes()),
        "repo.commit_hook",
    )
    assert installed.status is doctor.Status.INFO

    bare = library / "checkout"
    (bare / ".git" / "hooks").mkdir(parents=True)
    missing = find(
        doctor.run(
            config.from_dict(document_for(library)),
            probes=probes(checkout_root=lambda: bare),
        ),
        "repo.commit_hook",
    )
    assert missing.status is doctor.Status.FAIL
    assert "pre-commit install" in missing.detail

    (bare / ".git" / "hooks" / "pre-commit").write_text("# generated by pre-commit\n")
    present = find(
        doctor.run(
            config.from_dict(document_for(library)),
            probes=probes(checkout_root=lambda: bare),
        ),
        "repo.commit_hook",
    )
    assert present.status is doctor.Status.OK


def test_a_worktree_finds_the_hook_in_the_common_git_directory(tmp_path):
    """A worktree's ``.git`` is a FILE naming a directory that names the COMMON
    one, where hooks actually live. Following only the first pointer reports every
    worktree as unhooked while the hook is installed and running, which is a guard
    that fires on correct setups (P7).
    """
    common = tmp_path / "main" / ".git"
    (common / "hooks").mkdir(parents=True)
    (common / "hooks" / "pre-commit").write_text("# generated by pre-commit\n")
    per_tree = common / "worktrees" / "w1"
    per_tree.mkdir(parents=True)
    (per_tree / "commondir").write_text("../..\n")

    worktree = tmp_path / "w1"
    worktree.mkdir()
    (worktree / ".git").write_text(f"gitdir: {per_tree}\n")

    assert doctor._git_dir(worktree) == common.resolve()
    assert doctor._git_dir(tmp_path / "main") == common


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
    kept = setup_verb._resolve_volume_id(wizard, str(configured.library.root), None)
    assert kept == VOLUME

    overridden = setup_verb._resolve_volume_id(
        wizard, str(configured.library.root), "1111-2222"
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
    setup_verb._seed_taxonomy(wizard, configured)
    path = config.state_path("taxonomy_active", configured)
    assert path.is_file()

    path.write_text("# edited by hand\n" + path.read_text())
    setup_verb._seed_taxonomy(wizard, configured)
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


def test_only_the_wizard_is_declared_interactive_and_it_reads_no_standard_input():
    """The exemption is one FILE, and the wizard is not it.

    The registry marks setup interactive; the static allowlist names
    ``cli/prompt.py``. Those are two different things on purpose, and asserting
    both here is what stops the second one drifting into "the setup module may
    prompt", which would put a read of standard input in a module the wizard's
    own helpers keep growing.
    """
    interactive = [entry.name for entry in registry.entries() if entry.interactive]
    assert interactive == ["setup"]
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
