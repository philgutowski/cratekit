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
from tests import doctor_machines

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
    """R-1's own sentence, made true.

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
    git_dir = doctor._git_dir(root)
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
    """The half no mount state can answer: the right disk, and no permission."""
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

    R-7 is entirely about providers that trash on delete, and four of them read
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

    hardened = probes(
        rclone_remotes=lambda _r: {"archive": {"type": "onedrive", "hard_delete": "true"}}
    )
    assert find(doctor.run(cfg, probes=hardened), "backup.remote").status is doctor.Status.OK

    trashing = probes(
        rclone_remotes=lambda _r: {"archive": {"type": "onedrive", "hard_delete": "false"}}
    )
    assert find(doctor.run(cfg, probes=trashing), "backup.remote").failed


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
    assert "no shipped template is named" in checks["setup.taxonomy"]["detail"]


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
    assert preflight.identity_source(existing) == preflight.containing_mount(existing)
    # Still no mount slot, and any depth of ordinary missing directory: it would
    # be created on the volume its parent is already on.
    for gap in ("one", "one/two", "one/two/three/four"):
        assert preflight.identity_source(tmp_path / gap) == preflight.containing_mount(
            tmp_path
        ), gap
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


def test_a_check_whose_probe_raises_becomes_a_failed_check_not_a_lost_report(configured):
    """BLOCKING. ``run`` documented "never raise" and nothing made it true.

    Three of these checks reach the outside world through calls that raise on an
    ordinary broken machine rather than returning a value, and one raising took
    the ENTIRE report down: every other answer, on the machine the module's own
    opening argument says the report exists for.
    """

    def blind():
        raise PermissionError(13, "this account may not enumerate processes")

    report = doctor.run(configured, probes=probes(process_lister=blind))

    # Every check still answered, in order.
    assert [f.key for f in report.findings] == list(doctor.CHECK_KEYS)
    broken = find(report, "rekordbox.closed")
    assert broken.status is doctor.Status.FAIL, "unknown was reported as healthy"
    assert "did not complete" in broken.detail
    assert "PermissionError" in broken.detail
    assert broken.remedy is Remedy.REPORT_DEFECT
    # And the answers either side of it are the real ones rather than casualties.
    assert find(report, "interpreter.version").status is doctor.Status.OK
    assert find(report, "library.identity").status is doctor.Status.OK


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
    assert "exists and could not be read" in unreadable.detail
    assert unreadable.remedy is not Remedy.RUN_SETUP
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
        # Two removable-media mounters and the conventional hand-mounted spot.
        "linux": (("/media", 1), ("/media", 2), ("/run/media", 2), ("/mnt", 1)),
    }
    # And no other platform has one, which is a REFUSAL TO GUESS rather than a
    # claim that no volume mounts there. Windows resolves an identity provider
    # and has no row, so the derive refuses nothing on it: recorded as a residual
    # rather than fixed by inventing a shape nobody here can drive.
    assert "win32" not in preflight._VOLUME_MOUNT_LOCATIONS
