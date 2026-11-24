"""U5: the verb conformance suite. Coverage proves a verb exists; this proves it conforms,
iterating the registry so a verb without structured output or an exit code, or with a prompt,
fails by omission."""

from __future__ import annotations

import argparse
import ast
import contextlib
import enum
import io
import json
import os
import re
import subprocess
import sys
import uuid
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

import pytest

from cratekit import cli
from cratekit.cli import gates, output, registry, render
from cratekit.core import config, profiles, rb_writer, taxonomy
from cratekit.core.cause import REASONS, Cause, CratekitError, Outcome, Remediation, Scope
from cratekit.core.exit_codes import BANDS, MAX_CODE, RETIRED, ExitCode, Remedy, band_of, meaning_of
from cratekit.modules import extras
from tests import _import_probe, outbound_fakes
from tests import doctor_machines as machines
from tests._source_guards import constructs_a_csv_writer
from tests.test_config import valid_data

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "cratekit"
SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"


def package_sources() -> list[tuple[Path, str]]:
    """Every module we author; the vendored downloader is not ours to restyle."""
    return [
        (path, path.read_text())
        for path in sorted(PACKAGE_ROOT.rglob("*.py"))
        if "_vendor" not in path.parts
    ]


# Fixtures
@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def configured(library, monkeypatch):
    """A set up machine on the R-13 disposable database, so a verb reaches its own
    logic; volume identity and the two process refusal are satisfied."""
    from cratekit.core import preflight, rb_writer
    from tests.test_rb_writer_db import _build_disposable_database
    db_path = library / "db" / "master.db"
    supplied = rb_writer.integration_db_path()
    if supplied is not None:
        import shutil

        db_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(supplied, db_path)
        for suffix in rb_writer.db_sidecar_suffixes():
            sidecar = supplied.with_name(supplied.name + suffix)
            if sidecar.exists():
                shutil.copy2(sidecar, db_path.with_name(db_path.name + suffix))
    else:
        _build_disposable_database(db_path)

    cfg = config.from_dict(valid_data(library, profile={"name": "full"}))
    assert cfg.library.db_path == db_path
    config.save(cfg)
    config.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    # A person is present (U49), so gated verbs are driven through their gate and
    # ``record_acknowledgment`` does not depend on how pytest was launched. The
    # refusing direction is tested in tests/test_session_cli.py.
    from cratekit.core import session as core_session
    monkeypatch.setattr(core_session, "has_controlling_terminal", lambda: True)
    return cfg


@pytest.fixture(autouse=True)
def _trap_standard_input(monkeypatch):
    """Any read of ``input`` or ``sys.stdin`` is an immediate, named failure."""

    class Trapped:
        def __getattr__(self, name):
            raise AssertionError(f"a verb read standard input (sys.stdin.{name})")

    monkeypatch.setattr(sys, "stdin", Trapped())
    refusal = AssertionError("a verb called input()")
    monkeypatch.setattr("builtins.input", lambda *a, **k: (_ for _ in ()).throw(refusal))


def drive(argv: list[str]) -> tuple[int, str, str]:
    """Run the real dispatcher and return (status, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


# Part 1: the exit-code vocabulary (KTD25, S4)
def test_every_code_has_a_meaning_and_a_remediation_token():
    """Iterates the enum rather than listing members, so a new code is covered."""
    for code in ExitCode:
        meaning = meaning_of(code)
        assert meaning.summary, f"{code.name} has no summary"
        assert isinstance(meaning.remedy, Remedy), f"{code.name} has no remediation token"


def test_no_two_codes_share_a_value_and_none_reaches_the_shell_range():
    values = [int(code) for code in ExitCode]
    assert len(values) == len(set(values)), "two names share one exit code"
    for code in ExitCode:
        assert 0 <= int(code) < MAX_CODE, (
            f"{code.name}={int(code)} collides with the shell's own conventions "
            f"(126, 127, and 128 plus a signal number)"
        )
        band_of(code)


def test_a_retired_value_is_never_reissued():
    live = {int(code) for code in ExitCode}
    reused = sorted(live & set(RETIRED))
    assert not reused, (
        f"exit codes {reused} were retired and have been reissued. A stored cause "
        f"and a shell script both outlive the release that wrote them."
    )


def test_the_bands_do_not_overlap_and_leave_growth_room():
    for earlier, later in zip(BANDS, BANDS[1:]):
        assert earlier.stop <= later.start, "two bands overlap"
    assert BANDS[-1].stop == MAX_CODE
    live = {int(c) for c in ExitCode}
    unclaimed = [value for value in range(BANDS[-1].start, BANDS[-1].stop) if value not in live]
    assert unclaimed, "the vocabulary has no room left for a class nobody has met yet"


def test_status_two_belongs_to_the_argument_parser_and_to_nothing_else():
    """Status 2 belongs to argparse alone (KTD25), which produces it for a mistyped command."""
    assert not meaning_of(ExitCode.USAGE).verb_producible
    producible = {int(c) for c in ExitCode if meaning_of(c).verb_producible}
    assert 2 not in producible
    assert 2 not in {int(code) for code in REASONS.values()}

    code, _, _ = drive(["--not-a-flag"])
    assert code == int(ExitCode.USAGE)


def _modules_declaring_their_own_remedy() -> dict[str, type]:
    """Every module declaring a ``Remedy`` of its own, found by walking the package (P3)."""
    import importlib
    import pkgutil

    import cratekit
    found: dict[str, type] = {}
    for info in pkgutil.walk_packages(cratekit.__path__, "cratekit."):
        if "._vendor" in info.name:
            continue
        try:
            module = importlib.import_module(info.name)
        except Exception:  # noqa: BLE001 - a missing heavy extra is not a failure here
            continue
        declared = vars(module).get("Remedy")
        if (
            isinstance(declared, type)
            and issubclass(declared, enum.Enum)
            and declared.__module__ == info.name
            and info.name != "cratekit.core.exit_codes"
        ):
            found[info.name] = declared
    return found


def test_every_module_declaring_its_own_remedies_stays_inside_one_vocabulary():
    """Module local remediation tokens stay a subset of the canonical vocabulary,
    rather than becoming a second scheme for one idea."""
    modules = _modules_declaring_their_own_remedy()
    assert modules, "no module-local Remedy was found; the walk is broken, not the tree"
    canonical = {str(member) for member in Remedy}
    strays = {
        name: sorted({str(m) for m in declared} - canonical)
        for name, declared in modules.items()
        if not {str(m) for m in declared} <= canonical
    }
    assert not strays, (
        "these modules declare remediation tokens the canonical vocabulary has never heard of, "
        f"so the CLI cannot render them: {strays}"
    )


def test_every_module_local_remedy_renders_to_something_a_user_can_act_on():
    """Every module local token renders to its own remedy, not the code's generic summary."""
    generic = {str(meaning_of(code).summary) for code in ExitCode}
    for module_name, declared in _modules_declaring_their_own_remedy().items():
        for member in declared:
            remediation = Remediation(remedy=Remedy(str(member)))
            cause = Cause(
                reason="internal-error", message="m", remediation=remediation, scope=Scope.RUN,
                retryable=False,
            )
            body = render.remediation_line(cause).removeprefix("  fix: ")
            assert body not in generic, (
                f"{module_name}.{member.name} renders as the exit code's generic summary "
                f"rather than as its own remediation"
            )


def test_every_remediation_token_renders_to_something_a_user_can_act_on():
    """Audited by walking the enum, so a new token cannot render as nothing."""
    for remedy in Remedy:
        cause = Cause(reason="internal-error", message="x", remediation=Remediation(remedy=remedy))
        rendered = render.remediation_line(cause)
        assert rendered.strip() not in ("fix:", ""), f"{remedy} renders to nothing"


@pytest.mark.parametrize(
    "remedy, forbidden",
    [
        (Remedy.AUTHENTICATE_PROVIDER, "  fix: crate login"),
        (
            Remedy.REAUTHENTICATE_PROVIDER,
            "  fix: the provider rejected the stored credential; log in again",
        ),
    ],
)
def test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs(
    remedy, forbidden
):
    """U97, R-411: both provider session tokens name three acts, not a dead end login,
    pinned as literal text since a renderer compared to itself proves nothing."""
    cause = Cause(
        reason="credential-missing", message="no streaming provider session is usable",
        remediation=Remediation(remedy=remedy), scope=Scope.RUN,
    )
    line = render.remediation_line(cause)
    assert line != forbidden
    body = line.removeprefix("  fix: ")
    assert "crate login cannot mint" in body
    assert "vendored downloader's own login command" in body
    assert "crate login provider-session --from-file" in body
    assert "erase the plaintext file" in body
    assert "docs/adapters.md" in body


def test_the_document_the_provider_session_remedy_names_ships_and_carries_the_command():
    """The document the remedy names ships, since ``docs/`` is in no wheel."""
    adapters = REPO_ROOT / "docs" / "adapters.md"
    assert adapters.is_file(), "the remedy points at a document this repository does not ship"
    assert "crate login provider-session --from-file" in adapters.read_text(encoding="utf-8")


# ── S4: every refusal the guarded writer raises has a code and a remedy ──────
#: The refusals the guarded rekordbox writer raises, from U7's surface map, so U7
#: consumes this vocabulary. Reconciled against the writer by the test below.
WRITER_REFUSALS: dict[str, str] = {
    "pyrekordbox pin drift": "pyrekordbox-pin-drift",
    "database schema version drift": "db-schema-pin-drift",
    "rekordbox application version drift": "app-version-pin-drift",
    "missing database directory": "library-directory-missing",
    "missing database file": "library-database-missing",
    "database open failure": "database-open-failed",
    "canary read failure": "canary-read-failed",
    "cloud sync canary tripped": "cloud-sync-active",
    # "Sync is on" and "we cannot tell whether sync is on" have opposite answers,
    # so each is reserved separately.
    "cloud sync state unreadable": "cloud-sync-unreadable",
    "additive whitelist violation": "whitelist-violation",
    "missing tag-category template": "mytag-category-template-missing",
    "write lock contention": "write-lock-held",
}


@pytest.mark.parametrize("condition, slug", sorted(WRITER_REFUSALS.items()))
def test_every_guarded_writer_refusal_has_a_reserved_code(condition, slug):
    assert slug in REASONS, (
        f"the guarded writer refuses on {condition} and this vocabulary has no "
        f"slug for it. U7 consumes what is reserved here; a refusal it cannot "
        f"name collapses to a bare status one hop downstream."
    )
    code = REASONS[slug]
    assert code is not ExitCode.OK
    assert meaning_of(code).remedy is not None


def test_the_two_process_refusal_and_the_lock_contention_are_different_codes():
    """The two process refusal and lock contention differ, since their remedies are
    opposite: quit an application, or wait (KTD25)."""
    assert REASONS["rekordbox-running"] is ExitCode.REKORDBOX_OPEN
    assert REASONS["write-lock-held"] is ExitCode.LIBRARY_BUSY
    assert REASONS["session-lock-held"] is ExitCode.LIBRARY_BUSY
    assert meaning_of(ExitCode.REKORDBOX_OPEN).remedy is Remedy.QUIT_REKORDBOX
    assert meaning_of(ExitCode.LIBRARY_BUSY).remedy is Remedy.WAIT_FOR_HOLDER


def test_an_unrecorded_application_pin_refuses_rather_than_adopting_what_is_installed():
    """S2. A pin the software copies from the machine it runs on refuses nothing."""
    assert REASONS["app-version-pin-unrecorded"] is ExitCode.VERSION_PIN


def test_an_unreadable_cloud_state_and_an_active_one_are_different_failures():
    """An unreadable cloud state and an active one are different failures (S4): one
    is switched off elsewhere, the other needs a person to decide."""
    unreadable, active = REASONS["cloud-sync-unreadable"], REASONS["cloud-sync-active"]
    assert unreadable is not active
    assert meaning_of(unreadable).remedy is not meaning_of(active).remedy
    assert meaning_of(unreadable).remedy is Remedy.ANSWER_DECISION
    assert meaning_of(active).remedy is Remedy.DISABLE_CLOUD_SYNC

    # Answering the decision needs the run still there, and the command line layer
    # decides that by code, so this code makes the refusal resumable.
    assert unreadable in gates.GATE_CODES
    assert active not in gates.GATE_CODES


def test_the_unreadable_cloud_state_is_not_the_undeclared_gate_reason():
    """The unreadable cloud state is not ``decision-unknown-gate``, which is a
    defect, while a declared gate with nothing recorded is the system working."""
    assert REASONS["cloud-sync-unreadable"] is REASONS["decision-unknown-gate"]
    assert "cloud-sync-unreadable" != "decision-unknown-gate"


def test_the_reason_registry_has_no_duplicate_key():
    """No duplicate key in the reason registry literal, where a later one silently wins."""
    import inspect

    from cratekit.core import cause as cause_module
    literal = None
    for node in ast.walk(ast.parse(inspect.getsource(cause_module))):
        target = None
        if isinstance(node, ast.AnnAssign):
            target = getattr(node.target, "id", None)
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = getattr(node.targets[0], "id", None)
        if target == "REASONS":
            literal = node.value
    assert literal is not None, "REASONS is no longer a module-level assignment"

    # ``MappingProxyType({...})``: the mapping is the call's first argument.
    mapping = literal.args[0] if isinstance(literal, ast.Call) else literal
    keys = [key.value for key in mapping.keys]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    assert not duplicates, f"duplicate reason slugs shadowed at parse time: {duplicates}"
    assert len(keys) == len(REASONS), (
        f"the literal declares {len(keys)} keys and the runtime mapping has "
        f"{len(REASONS)}; the difference is entries one of the others shadows"
    )


def test_every_reason_maps_into_the_vocabulary_and_every_refusal_is_reachable():
    for slug, code in REASONS.items():
        assert isinstance(code, ExitCode), f"{slug} maps to something that is not a code"
    reachable = {*REASONS.values(), ExitCode.OK, ExitCode.USAGE}
    unreachable = [code.name for code in ExitCode if code not in reachable]
    assert not unreachable, (
        f"codes with no reason that produces them: {unreachable}. A code nothing "
        f"can raise is a code nobody maintains."
    )


# Part 2: the structured cause
def test_a_cause_round_trips_through_json_with_its_chain_intact():
    """A cause survives JSON, since the job engine re-invokes the CLI as a
    subprocess (KTD26) and would otherwise fall back to exit codes."""
    inner = Cause(
        reason="unavailable-transient", message="the provider timed out",
        remediation=Remediation(remedy=Remedy.RETRY_LATER), scope=Scope.ITEM, retryable=True,
        origin=("adapter.vendored",),
    )
    outer = Cause(
        reason="adapter-broken", message="the adapter gave up after three attempts",
        remediation=Remediation(remedy=Remedy.RETRY_LATER, steps=("wait, then retry",)),
        scope=Scope.SOURCE, origin=("download", "job", "sync"), inner=inner,
    )
    assert Cause.from_json(json.loads(outer.to_text())) == outer


def test_a_cause_cannot_be_built_without_a_remediation():
    with pytest.raises(ValueError):
        Remediation()


def test_a_reason_outside_the_registry_is_refused():
    remediation = Remediation(remedy=Remedy.REPORT_DEFECT)
    with pytest.raises(KeyError):
        Cause(reason="something-somebody-invented", message="x", remediation=remediation)


def test_a_boundary_appends_to_the_origin_trail_rather_than_replacing_it():
    remediation = Remediation(remedy=Remedy.AUTHENTICATE_PROVIDER)
    first = Cause(reason="auth-failed", message="x", remediation=remediation, origin=("adapter",))
    assert first.at("download").at("job").origin == ("adapter", "download", "job")


def test_the_exit_code_comes_from_the_reason_rather_than_being_stored_beside_it():
    """A cause whose code contradicts its reason is worse than either alone."""
    remediation = Remediation(remedy=Remedy.QUIT_REKORDBOX)
    built = Cause(reason="rekordbox-running", message="x", remediation=remediation)
    assert built.code is ExitCode.REKORDBOX_OPEN


# Part 3: the envelope and the schema lock (R32)
def test_the_five_structured_surfaces_r32_names_are_all_declared():
    assert set(output.schema_names()) == {"plan", "match", "review_set", "job_state", "diagnostic"}


def test_the_match_surface_reserves_three_states_from_its_first_version():
    """The match surface reserves R11's needs review state from its first version,
    since adding it later would break every consumer keyed on the shape."""
    document = output.schema_document("match")
    assert set(document["required"]) == {"matched", "needs_review", "missing"}


@pytest.mark.parametrize("name", sorted(output.schema_names()))
def test_a_schema_change_without_a_version_bump_fails(name):
    lock = json.loads((SCHEMA_DIR / "lock.json").read_text())
    identifier = output.current_schema(name)
    assert identifier in lock, (
        f"{identifier} has no lock entry. A new major is recorded in "
        f"tests/schemas/lock.json by running scripts/dump_schemas.py, and the "
        f"previous entry stays so no version is silently retired."
    )
    assert output.schema_fingerprint(name) == lock[identifier], (
        f"the {name!r} payload changed shape but {identifier} did not move. Bump the major in "
        f"cratekit/cli/output.py and re-run scripts/dump_schemas.py. An additive change needs a "
        f"bump too: a consumer keyed on field presence cannot tell an addition from a rename."
    )


@pytest.mark.parametrize("name", sorted(output.schema_names()))
def test_every_previous_major_is_still_present_in_the_lock(name):
    lock = json.loads((SCHEMA_DIR / "lock.json").read_text())
    major = int(output.current_schema(name).split("/")[1])
    for earlier in range(1, major):
        assert f"{name}/{earlier}" in lock, (
            f"{name}/{earlier} vanished from the lock. A retired version stays recorded, so a "
            f"consumer holding an old envelope can still find out what it was."
        )


@pytest.mark.parametrize("name", sorted(output.schema_names()))
def test_the_committed_golden_validates_against_the_current_schema(name):
    """The golden still validates, since a version bump does not say whether last
    version's envelope parses."""
    major = output.current_schema(name).split("/")[1]
    golden = json.loads((SCHEMA_DIR / "golden" / f"{name}.v{major}.json").read_text())
    assert output.envelope_problems(golden) == []


def _diagnostic(**fields) -> output.Envelope:
    """A diagnostic envelope built by the real builder, for run ``r`` of ``profile.show``."""
    return output.build(
        **{"verb": "profile.show", **fields}, run_id="r",
        schema=output.current_schema("diagnostic"), started="2026-01-01T00:00:00+00:00",
        data={"checks": [], "summary": {}},
    )


def test_the_declared_envelope_keys_are_exactly_what_is_serialized():
    """Derived from a real envelope, so the declared keys every verb must carry
    cannot fall behind the serializer."""
    document = _diagnostic().to_json()
    assert set(document) == set(output.ENVELOPE_KEYS)


def test_exactly_two_verbs_are_interactive_and_one_file_holds_the_stdin_exemption():
    """The stdin exemption is two verbs and one file, checked against each other (U107)."""
    interactive = [entry for entry in registry.entries() if entry.interactive]
    assert [entry.name for entry in interactive] == ["setup", "label.sync"]
    assert len(INTERACTIVE_ALLOWLIST) == 1


def test_the_envelope_never_carries_its_own_human_rendering():
    """Human rendering stays out of the JSON, or every wording change becomes a schema change."""
    for name in output.schema_names():
        assert "render" not in output.schema_document(name)["required"]
    assert set(output.ENVELOPE_KEYS) & {"render", "text", "message"} == set()


def test_pending_human_action_and_its_exit_code_imply_each_other():
    pending = output.PendingHumanAction(
        kind="rekordbox_import", id="pha_x", summary="import one file", verify_verb="run.show"
    )
    remediation = Remediation(remedy=Remedy.COMPLETE_PENDING_ACTION)
    good = _diagnostic(
        verb="run.show", outcome=Outcome.PENDING, code=ExitCode.PENDING_HUMAN, pending=pending,
        cause=Cause(reason="awaiting-import", message="waiting", remediation=remediation),
    )
    assert output.envelope_problems(good.to_json()) == []
    # One direction: pending action, wrong code.
    document = good.to_json()
    document["exit_code"] = int(ExitCode.OK)
    document["outcome"] = str(Outcome.OK)
    document["cause"] = None
    assert output.envelope_problems(document)
    # The other: the code with no pending action to explain it.
    document = good.to_json()
    document["pending_human_action"] = None
    assert output.envelope_problems(document)


def test_a_pending_action_must_name_the_verb_that_proves_it_done():
    """The field that separates a state from a printed instruction."""
    with pytest.raises(ValueError):
        output.PendingHumanAction(kind="rekordbox_import", id="x", summary="y", verify_verb="")


def test_every_non_success_outcome_carries_a_cause():
    document = _diagnostic(outcome=Outcome.FAILED, code=ExitCode.INTERNAL).to_json()
    assert any("structured cause" in problem for problem in output.envelope_problems(document))


def test_two_runs_starting_in_the_same_second_get_different_identifiers():
    """A collision would let one run's decisions answer another run's gate."""
    assert output.new_run_id() != output.new_run_id()


def test_two_thousand_identifiers_minted_inside_one_second_are_all_distinct():
    """U235, R-22: two thousand ids minted at one frozen instant are all distinct."""
    instant = datetime(2026, 11, 7, 16, 48, 26, tzinfo=timezone.utc)
    minted = [output.new_run_id(instant) for _ in range(2000)]
    assert len(set(minted)) == len(minted)
    assert {one[:20] for one in minted} == {"2026-11-07T16:48:26Z"}


def test_a_run_identifier_carries_sixty_four_bits_of_random_tail():
    """The tail is sixteen hex characters, a literal, as ``snapshot.new_stamp`` carries."""
    instant = datetime(2026, 11, 7, 16, 48, 26, tzinfo=timezone.utc)
    minted = output.new_run_id(instant)
    assert re.fullmatch(r"2026-11-07T16:48:26Z-[0-9a-f]{16}", minted), minted


# Part 4: gates, and no verb reads standard input (R33)
#: The only file allowed to touch standard input. Naming a path rather than a
#: directory keeps the exemption from spreading to a neighbouring file.
INTERACTIVE_ALLOWLIST = frozenset({"cratekit/cli/prompt.py"})


def standard_input_reads(source: str) -> list[str]:
    """Every construct that could read standard input, as an AST walk, not a search."""
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"input", "raw_input"}:
                found.append(f"{node.func.id}()")
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Attribute):
            if node.value.attr == "stdin":
                found.append(f"sys.stdin.{node.attr}")
        if isinstance(node, ast.Attribute) and node.attr == "stdin":
            if isinstance(node.value, ast.Name) and node.value.id == "sys":
                found.append("sys.stdin")
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imported = isinstance(node, ast.Import)
            names = [a.name for a in node.names] if imported else [node.module or ""]
            if any(name.split(".")[0] == "getpass" for name in names):
                found.append("getpass")
    return found


def test_the_standard_input_guard_bites_on_each_shape():
    assert standard_input_reads("answer = input('go? ')\n")
    assert standard_input_reads("import sys\nline = sys.stdin.readline()\n")
    assert standard_input_reads("import sys\nif sys.stdin.isatty():\n    pass\n")
    assert standard_input_reads("import getpass\n")
    assert standard_input_reads("x = 1\n") == []


def test_no_module_we_author_reads_standard_input():
    offenders: dict[str, list[str]] = {}
    for path, source in package_sources():
        relative = path.relative_to(SRC_ROOT).as_posix()
        if relative in INTERACTIVE_ALLOWLIST:
            continue
        found = standard_input_reads(source)
        if found:
            offenders[relative] = found
    assert not offenders, (
        f"standard input is read at {offenders}. A gate is answered by name and resumed from "
        f"state; a prompt cannot be answered by a detached job, and a terminal check is a "
        f"behaviour change under a pipe rather than an absence of a read."
    )


_TO_SLIM = ["--output", "json", "profile", "set", "slim"]


def _stopped_at_the_profile_gate() -> str:
    """The run id of a ``profile set slim`` that stopped at its gate."""
    _, out, _ = drive(_TO_SLIM)
    return json.loads(out)["run_id"]


def test_an_unanswered_gate_exits_with_the_documented_code_and_leaves_the_run_resumable(configured):
    code, out, err = drive(_TO_SLIM)
    assert code == int(ExitCode.DECISION_REQUIRED)
    envelope = json.loads(out)
    assert output.envelope_problems(envelope) == []
    assert envelope["resumable"] is True
    assert envelope["cause"]["reason"] == "decision-required"
    assert envelope["cause"]["detail"]["gate"] == "profile.set.apply"
    assert envelope["cause"]["detail"]["options"] == ["apply", "abort"]
    # Resumable means the state is on disk, not that the message said so.
    state = gates.load(envelope["run_id"])
    assert state.open_gate == "profile.set.apply"
    assert state.verb == "profile.set"
    assert "profile.set.apply" in state.offers


def test_the_profile_gate_shows_the_delta_the_digest_was_taken_over(configured):
    """R-693: the profile gate shows the delta its digest covers, in json and on screen."""
    code, out, _ = drive(_TO_SLIM)
    assert code == int(ExitCode.DECISION_REQUIRED)
    shown = json.loads(out)["cause"]["detail"]["shown"]
    code, out, _ = drive(["--output", "json", "-d", "profile.set.apply=abort", *_TO_SLIM[2:]])
    assert code == int(ExitCode.OK)
    declined = json.loads(out)["data"]
    assert shown["items"] == declined["items"]
    assert shown["items"], "full to slim turns modules off, so the delta cannot be empty"
    assert shown["digest"] == declined["digest"]
    assert shown["count"] == len(declined["items"])
    assert (shown["enabling"], shown["disabling"]) == (
        declined["totals"]["enabling"],
        declined["totals"]["disabling"],
    )
    assert shown["profile"] == "slim"
    code, out, err = drive(["profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_REQUIRED)
    screen = out + err
    assert f"  digest: {shown['digest']}" in screen
    assert "  profile: slim" in screen
    first = shown["items"][0]
    assert f"    module={first['module']}, change={first['change']}" in screen


def test_the_same_gate_answered_by_name_proceeds(configured):
    code, out, _ = drive(["--output", "json", "-d", "profile.set.apply=apply", "profile", "set", "slim"])
    assert code == int(ExitCode.OK)
    envelope = json.loads(out)
    assert envelope["outcome"] == "ok"
    config.reset_cache()
    assert config.load().profile.name == "slim"


def test_a_gate_is_answerable_from_a_different_process_in_a_later_session(configured):
    """The half of R33 a flag on the original invocation can never provide."""
    run_id = _stopped_at_the_profile_gate()
    code, _, _ = drive(["run", "decide", run_id, "profile.set.apply", "apply", "--actor", "test"])
    assert code == int(ExitCode.OK)
    code, out, _ = drive(["--output", "json", "--run", run_id, "profile", "set", "slim"])
    assert code == int(ExitCode.OK)
    config.reset_cache()
    assert config.load().profile.name == "slim"
    assert gates.load(run_id).decisions["profile.set.apply"].actor == "test"


def test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments(configured):
    """U168: one command answers the gate and continues the run, arguments and all."""
    run_id = _stopped_at_the_profile_gate()
    assert gates.load(run_id).argv == ("profile", "set", "slim")
    code, out, _ = drive(
        ["--output", "json", "run", "decide", run_id, "profile.set.apply", "apply", "--continue"]
    )
    assert code == int(ExitCode.OK), out
    envelope = json.loads(out)
    assert envelope["verb"] == "profile.set" and envelope["run_id"] == run_id
    config.reset_cache()
    assert config.load().profile.name == "slim"


def test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded(configured):
    """U168: what --continue gives back is the run's first command line, never a later one."""
    run_id = _stopped_at_the_profile_gate()
    drive(["--output", "json", "--run", run_id, "profile", "set", "full"])
    assert gates.load(run_id).argv == ("profile", "set", "slim")


def test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale(configured):
    """The property that stops a user approving one plan and running a wider one."""
    run_id = _stopped_at_the_profile_gate()
    drive(["run", "decide", run_id, "profile.set.apply", "apply"])
    # The world moves between offer and resume: one module is switched off by hand,
    # so the delta the decision was made against is no longer the one applied.
    document = config.load().to_toml_dict()
    document["modules"] = {"analysis": False}
    config.save(config.from_dict(document))
    config.reset_cache()
    code, out, _ = drive(["--output", "json", "--run", run_id, "profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_STALE)
    assert json.loads(out)["cause"]["reason"] == "decision-stale"


def test_a_gate_marked_explicit_refuses_an_inline_answer(configured):
    """R34: an explicit gate refuses an answer given in the same command, in the resolver."""
    spec = registry.GateSpec(
        name="session.ack.backup", options=("acknowledged", "abort"), prompt="Backed up?",
        explicit=True,
    )
    state = gates.RunState(run_id="r", verb="session.ack", created="now")
    resolver = gates.Gates(state=state, supplied={"session.ack.backup": "acknowledged"})
    with pytest.raises(gates.DecisionRequired):
        resolver.require(spec)
    # Recorded deliberately, with the actor, it passes.
    gates.record(state, spec, "acknowledged", actor="a-person")
    assert gates.Gates(state=state).require(spec) == "acknowledged"
    assert state.decisions[spec.name].actor == "a-person"


def test_the_unreadable_cloud_sync_override_is_a_DECLARED_GATE():
    """The unreadable cloud sync override is a declared gate a user can answer,
    looked up through the registry."""
    owner, spec = registry.gate("write.cloudsync.unreadable")
    assert spec.explicit, (
        "R34 forbids a blanket answer for this class: proceeding past a guard "
        "that could not rule out a concurrent writer is a per-run act by a named "
        "actor, not a flag that answers it once for everything"
    )
    assert set(spec.options) == {"proceed", "abort"}
    assert owner.writes & registry.DB_WRITE_SURFACES


def test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision():
    """Every verb declaring a database write surface declares the cloud sync decision (P3)."""
    writing = {e.name for e in registry.ENTRIES if e.writes & registry.DB_WRITE_SURFACES}
    asking = {
        entry.name
        for entry in registry.ENTRIES
        if any(spec.name == "write.cloudsync.unreadable" for spec in entry.gates)
    }
    missing = sorted(writing - asking)
    assert not missing, (
        f"verbs that write the database and declare no cloud-sync decision: {missing}"
    )
    # And the reverse: a verb declaring the decision without writing the database
    # asks a question its work can never raise.
    spurious = sorted(asking - writing)
    assert not spurious, f"verbs declaring a decision they cannot reach: {spurious}"


def test_the_core_writer_never_learns_the_gates_name_or_any_flag_string():
    """D2: the core writer and its parts (R-1890) name no verb, gate or flag; the
    override crosses in as a boolean."""
    from tests._split_modules import source_of
    source = source_of("cratekit.core.rb_writer")
    for leaked in ("write.cloudsync.unreadable", "--decision", "crate "):
        assert leaked not in source, f"the core writer names {leaked!r}"


def test_no_environment_variable_or_config_key_can_answer_a_gate(configured, monkeypatch):
    """No environment variable or config key answers a gate, since a blanket
    answer satisfies every gate at once, which R34 forbids."""
    for variable in ("CRATEKIT_YES", "CRATEKIT_DECISION", "CRATEKIT_ASSUME_YES"):
        monkeypatch.setenv(variable, "1")
    code, _, _ = drive(["profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_REQUIRED)


def test_a_malformed_decision_is_refused_rather_than_ignored(configured):
    """A silently dropped decision stops at a gate the user believes they answered."""
    code, _, _ = drive(["-d", "no-equals-sign", "profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_REQUIRED)


def _pending_profile_run(**fields) -> gates.RunState:
    """A saved ``profile.set`` run carrying a pending import, with ``fields`` on the action."""
    state = gates.new_run(registry.entry("profile.set"))
    state.pending = output.PendingHumanAction(
        kind="rekordbox_import", id=output.new_pending_id(state.run_id), verify_verb="run.show",
        **fields,
    )
    gates.save(state)
    return state


def test_a_verb_blocked_by_an_unverified_pending_action_refuses_before_doing_anything(configured):
    """What makes ``pending_human_action`` load-bearing rather than advisory."""
    state = _pending_profile_run(summary="import one file", blocks=("profile.set",))
    code, out, _ = drive(["--output", "json", "--run", state.run_id, "profile", "set", "slim"])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert json.loads(out)["cause"]["reason"] == "blocked-by-pending-action"


def test_a_run_that_reached_a_gate_reports_it(configured):
    code, out, _ = drive(["--output", "json", "run", "show", _stopped_at_the_profile_gate()])
    assert code == int(ExitCode.OK)
    assert json.loads(out)["data"]["summary"]["open_gate"] == "profile.set.apply"


def test_a_run_carrying_a_pending_action_reports_it_as_pending(configured):
    state = _pending_profile_run(
        summary="import one file into rekordbox",
        steps=("open the library application", "import the file"),
    )
    code, out, _ = drive(["--output", "json", "run", "show", state.run_id])
    assert code == int(ExitCode.PENDING_HUMAN)
    envelope = json.loads(out)
    assert output.envelope_problems(envelope) == []
    assert envelope["pending_human_action"]["verify_verb"] == "run.show"


def test_a_decision_naming_a_gate_the_verb_does_not_declare_is_refused(configured):
    run_id = _stopped_at_the_profile_gate()
    code, _, _ = drive(["run", "decide", run_id, "some.other.gate", "apply"])
    assert code == int(ExitCode.DECISION_REQUIRED)


def test_a_run_record_belongs_to_the_verb_that_created_it(configured):
    run_id = _stopped_at_the_profile_gate()
    code, _, _ = drive(["--run", run_id, "run", "show", run_id])
    assert code == int(ExitCode.DECISION_REQUIRED)


# Part 5: the registry, the stub, and parity
def test_help_succeeds_with_every_heavy_extra_absent(configured, monkeypatch):
    """Help succeeds with every heavy extra absent, blocked at the import system so
    this is a test rather than an environment."""
    blocked = {module for entry in registry.entries() for module in entry.extras_modules}
    assert blocked, "no entry declares an extras-backed dependency"

    class Blocker:
        def find_spec(self, name, path=None, target=None):
            if name.split(".")[0] in blocked:
                raise ImportError(f"blocked: {name}", name=name)
            return None

    monkeypatch.setattr(sys, "meta_path", [Blocker(), *sys.meta_path])
    # argparse's --help writes to the real stdout, so the redirect captures what a user would see.
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        code, _, _ = drive(["--help"])
    assert code == 0
    text = printed.getvalue()
    assert "crate" in text
    for entry in registry.landed_entries():
        assert entry.path[0] in text, f"{entry.name} vanished from help"


def _analysis_entry(verb: str, summary: str, module: str, **fields) -> registry.Entry:
    """A fake ``analyze`` verb in the analysis module, built from ``tests/cli_fixtures``."""
    return registry.Entry(
        name=f"analyze.{verb}", summary=summary, module=f"tests.cli_fixtures.{module}",
        builder="build", handler_key=f"analyze.{verb}", module_id="analysis", **fields,
    )


_BEHIND_AN_EXTRA = {"extras": "analysis", "extras_modules": ("a_third_party_analysis_library",)}


def test_a_module_with_missing_extras_becomes_a_stub_that_names_the_install_command():
    """Assertion 9, driven against the real construction path with a fake entry."""
    summary = "a verb behind an extras group"
    entry = _analysis_entry("demo", summary, "needs_extra", **_BEHIND_AN_EXTRA)
    parser = cli.build_parser([entry], membership=profiles.resolve("full"))
    # The stub is still listed with what it needs, so a slim install can find out the verb exists.
    help_text = io.StringIO()
    with contextlib.redirect_stdout(help_text), pytest.raises(SystemExit):
        parser.parse_args(["analyze", "--help"])
    assert "a verb behind an extras group" in help_text.getvalue()
    assert "requires the 'analysis' extra" in help_text.getvalue()
    args = parser.parse_args(["analyze", "demo"])
    assert args._stub is not None
    cause = cli._stub_cause(args._entry, args._stub)
    assert cause.code is ExitCode.MODULE_UNAVAILABLE
    assert cause.detail["install"] == extras.install_command("analysis")


def test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra():
    """A defect in our own module raises as itself, not as a missing extra, which
    would send a user to install a package that cannot help."""
    entry = _analysis_entry(
        "broken", "a verb with a defect of our own", "broken_module", **_BEHIND_AN_EXTRA
    )
    # Since U248 the defect raises when its verb is chosen, so one broken module
    # stops no other command; the eager parser still raises it at construction.
    parser = cli.build_parser([entry], membership=profiles.resolve("full"))
    with pytest.raises(ImportError) as raised:
        parser.parse_args(["analyze", "broken"])
    assert raised.value.name == "cratekit.this_module_does_not_exist"
    with pytest.raises(ImportError):
        cli.build_parser([entry], membership=profiles.resolve("full"), eager=True)


def test_a_profile_that_switches_a_module_off_removes_its_verbs(configured):
    entry = _analysis_entry("demo", "a verb behind a module toggle", "plain")
    slim = cli.build_parser([entry], membership=profiles.resolve("slim"))
    with pytest.raises(SystemExit):
        slim.parse_args(["analyze", "demo"])
    full = cli.build_parser([entry], membership=profiles.resolve("full"))
    assert full.parse_args(["analyze", "demo"])._entry is entry


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"emits": frozenset({"plan"})}, "declares its schema"),
        ({"output_schema": "plan/1"}, "emits something"),
        ({"writes": frozenset({"files"})}, "destructive by definition"),
        ({"long_running": True}, "argv builder"),
        ({"module_id": "not-a-module"}, "not a declared feature module"),
        ({"extras": "analysis"}, "names the third-party modules"),
        (
            {"module_id": "vocals", "extras": "analysis", "extras_modules": ("x",)},
            "is not this verb's own module",
        ),
        (
            {"module_id": "setbuilder", "extras": "setbuilder", "extras_modules": ("x",)},
            "has no extras group",
        ),
    ],
)
def test_an_entry_missing_its_metadata_fails_to_register(kwargs, expected):
    """A new verb fails by omission. This is the omission half."""
    base = dict(
        name="demo.verb", summary="x", module="tests.cli_fixtures.plain", builder="build",
        handler_key="demo.verb",
    )
    with pytest.raises(ValueError) as excinfo:
        registry.Entry(**{**base, **kwargs})
    assert expected in str(excinfo.value)


def test_the_registry_is_the_source_of_the_verb_names_the_layering_guard_reads():
    assert registry.VERB_NAMES == frozenset(e.name for e in registry.entries())
    assert len(registry.VERB_NAMES) == len(registry.entries())


def test_the_table_is_every_part_in_order_and_each_file_is_under_the_bar():
    """U328: the table is split so no file passes U290's 1,500 lines. A ``registry_*`` module
    nobody stars into ``ENTRIES`` would drop its verbs silently, and help follows the order."""
    files = sorted(Path(registry.__file__).parent.glob("registry*.py"))
    assert files[0].name == "registry.py"
    parts = [vars(sys.modules[f"cratekit.cli.{path.stem}"]) for path in files[1:]]
    held = {name: rows for part in parts for name, rows in part.items() if name.endswith("_VERBS")}
    order = ("STATE_VERBS", "PIPELINE_VERBS", "SYNC_VERBS", "MODULE_VERBS", "LATER_VERBS")
    assert sorted(held) == sorted(order) and len(parts) == len(order) and all(held.values())
    assert registry.ENTRIES == tuple(entry for name in order for entry in held[name])
    over = {path.name: n for path in files if (n := len(path.read_text().splitlines())) > 1500}
    assert not over, f"over 1,500 lines, so the next verb's block opens a new part: {over}"


def test_a_planned_verb_whose_module_has_landed_must_lose_its_marker():
    """A planned verb whose module has landed loses its ``planned_in`` marker, walked
    so an empty set is a valid population (P3)."""
    import importlib.util
    leftover = []
    for entry in registry.entries():
        if entry.landed:
            continue
        try:
            present = importlib.util.find_spec(entry.module) is not None
        except ModuleNotFoundError:
            present = False
        if present:
            leftover.append(
                f"{entry.module} now exists, so {entry.planned_in} has landed. Clear planned_in on "
                f"{entry.name!r} so the conformance assertions start driving it."
            )
    assert not leftover, leftover


#: Planned verbs whose module ``tests/_pending.PENDING`` also owes, written out
#: so a change to either register is made where a reviewer reads. Empty since U27.
EXPECTED_COMPARED: frozenset[str] = frozenset()


def test_a_planned_verb_and_the_pending_register_name_the_same_unit():
    """``Entry.planned_in`` and ``tests/_pending.PENDING`` name the same unit.

    They drifted once. Compared over the intersection; the anti vacuity guard reads the list the
    comparison reads."""
    from tests import _pending  # noqa: PLC0415
    compared = [
        entry
        for entry in registry.entries()
        if not entry.landed and entry.module in _pending.PENDING
    ]
    # Empty since U27, and falsifiable both ways: registering a planned verb's
    # module fires this, and emptying the register raises in ``_pending.requires``.
    assert {entry.name for entry in compared} == EXPECTED_COMPARED, (
        f"the set of planned verbs the register also owes has moved; it is now "
        f"{sorted(entry.name for entry in compared)} and this file says it is "
        f"{sorted(EXPECTED_COMPARED)}. Update the expectation in the same commit "
        f"as the register, or the comparison below stops covering the new one."
    )
    disagreements = {
        entry.name: (entry.planned_in, _pending.PENDING[entry.module][0])
        for entry in compared
        if entry.planned_in != _pending.PENDING[entry.module][0]
    }
    assert not disagreements, (
        f"planned_in and tests/_pending.PENDING name different units for the same "
        f"module: {disagreements}. The register is what scripts/board.py reads, so "
        f"it wins; repoint the marker."
    )


# ── the nine conformance properties, over every entry ────────────────────────
ALL_ENTRIES = list(registry.entries())
LANDED = [e for e in ALL_ENTRIES if e.landed]


def test_a_handler_key_resolves_without_importing_the_module():
    """KTD26: a handler key resolves without importing its module, measured in a
    fresh interpreter that imported only the registry, as the supervisor has."""
    result = _import_probe.run_probe(
        """
        import json, sys
        from cratekit.cli import registry

        leaked = {}
        walked = 0
        for entry in registry.entries():
            if not entry.landed:
                continue
            walked += 1
            before = set(sys.modules)
            assert registry.by_handler_key(entry.handler_key) is entry
            added = sorted(m for m in set(sys.modules) - before if m.startswith("cratekit"))
            if added:
                leaked[entry.handler_key] = added
        print(json.dumps({"leaked": leaked, "walked": walked}))
        """
    )
    _import_probe.assert_no_leak(result, what="resolving a handler key")


@pytest.mark.parametrize("entry", ALL_ENTRIES, ids=lambda e: e.name)
def test_conformance_1_structured_output(entry):
    if not entry.emits:
        return
    name, _, major = entry.output_schema.partition("/")
    assert entry.output_schema == output.current_schema(name)
    lock = json.loads((SCHEMA_DIR / "lock.json").read_text())
    assert f"{name}/{major}" in lock


@pytest.mark.parametrize("entry", LANDED, ids=lambda e: e.name)
def test_conformance_1_structured_output_is_actually_emitted(entry, configured, monkeypatch):
    argv = ["--output", "json", *_sample_decisions(entry), *entry.path, *_sample_arguments(entry, monkeypatch)]
    code, out, _ = drive(argv)
    envelope = json.loads(out)
    assert output.envelope_problems(envelope) == [], envelope
    assert envelope["exit_code"] == code, (
        "the envelope's exit code and the process status must be the same "
        "number, or a caller reading one of them has no idea what the other says"
    )
    assert envelope["verb"] == entry.name
    # Exactly one JSON object on standard output and nothing else.
    assert out.strip().startswith("{") and out.strip().endswith("}")
    assert out.strip().count("\n") == 0


def _written(path: Path, text: str) -> Path:
    """One small file at ``path``, for a sample that needs a file of a given shape."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _sample_arguments(entry: registry.Entry, monkeypatch=None) -> list[str]:
    """Enough positional arguments to drive one verb; decisions stay root parser flags. File
    verbs get a path under the ``configured`` library (R1); ``monkeypatch`` serves a lazy sample
    (U129)."""
    library = config.load().library.root
    sample = {
        "profile.show": [],
        "profile.set": ["slim"],
        "run.show": ["no-such-run"],
        "run.decide": ["no-such-run", "profile.set.apply", "apply"],
        # U170. Lazy: a run open at its gate for a month gives the confirm a plan; the rest is in
        # tests/test_run_retire.py.
        "run.retire": _run_retire_over_one_old_gate,
        # U10. An absent identifier refuses from the vocabulary; an empty queue is a fresh install.
        "job.list": [],
        "job.show": ["no-such-job"],
        "job.resume": ["no-such-job"],
        "job.cancel": ["no-such-job"],
        # U11. Absent identifiers, as above; the file verbs take a path under the library (R1).
        "review.list": [],
        "review.show": ["no-such-item"],
        "review.resolve": ["no-such-item", "--verdict", "accepted"],
        "review.clear": ["no-such-item"],
        "review.export": [str(library / "review-export.json")],
        "review.import": [str(library / "no-such-export.json")],
        # U36. Read only, it opens the database only for a native tree, so it exits OK.
        "converge": [],
        # U24. An empty store is not a failure; revoking is driven from the deletion suite.
        "tombstone.list": [],
        # U24. It refuses at its confirm gate; conformance 3 drives the two act OK path.
        "delete.review": [],
        # U16. An absent path, refused from the vocabulary; tests/test_match_states.py.
        "match.run": [str(library / "no-such-list.txt")],
        # U42. Download freezes an absent list unread and audit reads an empty music folder: OK.
        "acquire.download": [str(library / "no-such-list.txt")],
        "acquire.audit": [],
        # U80. An absent list, refused before any walk, so nothing reaches the searcher.
        "acquire.fallback": [str(library / "no-such-list.txt")],
        # U81. The same absent list, refused before any walk, queue or download.
        "acquire.fallback-fetch": [str(library / "no-such-list.txt")],
        # U176. No session in the isolated keychain: both refuse auth-failed, before Bandcamp.
        "acquire.bandcamp": [],
        "acquire.bandcamp-fetch": [],
        # U23. The census takes no positional (R19) and queues without a database.
        # U49. The session verbs take no positional or actor flag (R34); ``session ack --as
        # session`` (U184) is in tests/test_session_ack_by_session.py, the rest in
        # tests/test_session_cli.py.
        "session.ack": [],
        "session.release": [],
        "adopt.scan": [],
        # U27. No positional (R19): its explicit gate is asked over an empty plan, abortable.
        "adopt.apply": [],
        # R-758. It reads the backup acknowledgment before its gate (R-733); the plan is empty.
        "adopt.move": [],
        # U119. Lazy: the tree cut over, the source made, so NO_OP; tests/test_genre_favorites.py.
        "favorites.refresh": _routing_tree_cut_over_with_a_source,
        # U120. Lazy: the source made and no hearts job, so NO_OP; tests/test_favorites_backfill.py.
        "favorites.backfill": _a_source_playlist,
        # U145. No quarter playlist, so it asks nothing (UNREACHABLE_GATES); test_favorites_split.
        "favorites.split": _a_source_playlist,
        # U180. The source alone and in order, so NO_OP (UNREACHABLE_GATES); test_favorites_order.
        "favorites.order": _a_source_playlist_in_a_folder,
        # U61. The favourites export reaches the confirm gate; tests/test_sync_all.py.
        "sync.all": ["--export", str(outbound_fakes.write_export(library / "outbound"))],
        # U152, U181. Lazy fakes: the gate is asked, nothing queued, NO_OP; tests/test_sync_land.py.
        "sync.land": _a_pass_with_no_vocal_model_and_nothing_new,
        # U293. The pass ends on its own first refusal, which the night records; test_sync_night.
        "sync.night": [],
        # U295. conftest reads the platform as Linux, so each refuses before launchd; test_schedule.
        "schedule.install": [],
        "schedule.show": [],
        "schedule.remove": [],
        # U179. The plan step refuses for want of a Bandcamp session; tests/test_sync_bandcamp.py.
        "sync.bandcamp": [],
        # U20. An empty intake exits OK; rebuild names an actor, or the product answers for one.
        "route.inbox": [],
        "route.unplaced": [],
        "route.resort": [],
        "route.pending": [],
        "rebuild": ["--actor", "a-person"],
        # U27. The wizard answers everything from the recorded file and reaches no prompt.
        "setup": [],
        "doctor": [],
        "status": [],
        # A credential is never an argument, so this drives the refusal naming both ways.
        "login": ["provider-session"],
        # U37. Identify refuses a missing recording before any paid call; set (U129) is lazy.
        "intake.set": _intake_set_reaching_account_gate,
        "intake.identify": [str(library / "no-such-set.mp3")],
        "intake.playlist": ["https://example.invalid/playlist"],
        # U69. An absent identifier, refused from the vocabulary.
        "intake.missing": ["--job", "no-such-job"],
        # U121. Lazy: one finished set job whose track is missing, so NO_OP.
        "intake.inspiration": _finished_set_job_on_a_native_tree,
        # R-770. A real file, lazy, since the verb is gated and on the bridge asks nothing.
        "intake.file": lambda: [str(_a_file_in_the_library())],
        # U154. No batch folder, so an empty plan, OK and no gate (UNREACHABLE_GATES).
        "intake.shelve": ["--report", "--all"],
        # U72. A folder with no audio, refused before the gate.
        "intake.land": [str(library / "Music"), "--export", str(library / "no-such.xml")],
        # R-501. An absent export, refused from the vocabulary.
        "intake.imported": ["--export", str(library / "no-such.xml")],
        # U82. A pass never run: the gate over an empty plan, NO_OP; lazy (R-235), since its
        # file under the library would trip the cutover precheck. tests/test_sync_mark.py.
        "sync.mark": lambda: [
            "--xml",
            str(outbound_fakes.write_export(library / "landed").rename(
                library / "landed" / "no-such-pass_synced_inboxed.xml"
            )),
        ],
        # R-838. No mark record, so an empty plan and NO_OP; tests/test_sync_unmark.py.
        "sync.unmark": ["--pass", "no-such-pass_synced"],
        "tag.folder": [str(library / "Music")],
        # U40. An empty folder opens no database, so no cloud sync decision (R-246).
        "tag.retag": [str(library / "Music")],
        # U43. An absent anchor refuses; the OK path is in tests/test_setbuilder_cli.py.
        "setbuild": [str(library / "Music" / "no-such-anchor.aiff")],
        # U44. OK: the path is queued unread; the refusal is in tests/test_master_cli.py.
        "master": [str(library / "Music" / "no-such-recording.wav")],
        # U45. Queued off the configured destinations; tests/test_backup_cli.py refuses.
        "backup.run": [],
        "name.apply": [],
        # U102. The confirm gate over an empty queue; unflagged, tests/intake/test_repair.py.
        "repair.paths": ["--apply"],
        # U25. Run and restamp queue, so they still emit a job_state envelope.
        "analyze.run": [str(library / "Music")],
        "analyze.calibrate": [],
        "analyze.validate": [],
        "analyze.restamp": [str(library / "Music")],
        "analyze.vocals": [str(library / "Music")],
        "metadata.mytags-vocals": [],
        # U26. An empty registry; ``sync labels`` is retired (U109); tests/test_label_workers.py.
        "label.registry": [],
        "sync.labels": [],
        "label.import": ["no-such-label"],
        "label.harvest": ["https://example.invalid/playlist"],
        # U75. An empty review queue accepts nothing, before the catalogue is resolved.
        "label.approved": [],
        # R-798. It lists what the genre gate holds.
        "label.held": [],
        # R-815. An empty review queue queues no job and says which zero, before any provider.
        "label.judge": [],
        # R-840. An empty review queue repairs none, before any provider.
        "label.artists": [],
        # U108. ``--go`` reaches the one gate; with no saved answer a yes downloads nothing.
        "label.sync": ["--go"],
        # R-835. A label nobody follows: still gated, NO_OP; tests/test_label_playlists.py.
        "label.playlists": ["no-such-label"],
        # R-836. The same for the prune. tests/test_prune.py.
        "label.prune": ["no-such-label"],
        # U123. The same for the heard merge. tests/test_label_heard.py.
        "label.heard": ["no-such-label", "2023", "2026-10-09"],
        # R-835. The same, with the intake file the mark needs, lazy as ``sync.mark``.
        "label.mark": lambda: [
            "no-such-label",
            "--xml",
            str(outbound_fakes.write_export(library / "label-landed").rename(
                library / "label-landed" / "no-such-batch_inboxed.xml"
            )),
        ],
        # R-837. An empty list reaches the gate, NO_OP; lazy, as it writes. test_export_set.
        "export.set": lambda: [
            str(_written(library / "set-lists" / "empty-set.list.json", '{"list": 1, "tracks": []}'))
        ],
        # R-837. A set never made archives nothing, still gated, with its intake file.
        "export.archive": lambda: [
            "no-such-set",
            "--xml",
            str(_written(library / "set-landed" / "no-such-set_inboxed.xml", "<DJ_PLAYLISTS/>")),
        ],
        # U27. An absent export under the library (R1) refuses; tests/modules/test_reports.py.
        "audit.coverage": [str(library / "no-such-export.xml")],
        "audit.duplicates": [str(library / "no-such-export.xml")],
        "report.library": [str(library / "no-such-export.xml")],
        "report.intake-aging": [str(library / "no-such-export.xml")],
        # U27. An empty session log restores nothing, so OK with no backup acknowledgment.
        "restore.list": [],
        "restore.run": [],
        # U96. It refuses here, the behaviour under test, and declares no gate.
        "restore.bare-metal": ["--target", str(library / "replacement"), "--accept-replacement"],
        # U33, U51. A real export (R1), since an absent one refuses before the gate.
        "export.playlist": [
            "crate-export", "--export", str(outbound_fakes.write_export(library / "outbound"))
        ],
        "sync.favorites": ["--export", str(outbound_fakes.write_export(library / "outbound"))],
        # R-836. Never exported: an empty plan, still gated, NO_OP. tests/test_prune.py.
        "export.prune": [
            "crate-export", "--export", str(outbound_fakes.write_export(library / "outbound"))
        ],
        # U28. A target under the library, or it would write the real agent skills folder.
        "skills.install": ["--into", str(library / "agent-skills")],
        # R-235. Lazy, since each changes library state: a cutover the precheck passes, a revert.
        "tree.cutover": lambda: _ready_to_cut_over(),
        "tree.revert": lambda: _already_cut_over(),
        # R-745. A new name per drive, since the verb never replaces a file.
        "export.collection": lambda: [
            str(library / "exports" / f"collection-{uuid.uuid4().hex}.xml")
        ],
        # R-797. The author's threshold and the configured database.
        "report.genres": [],
        # Stale row genres: it reads the configured collection.
        "tag.rows": [],
        # R-923. The seeded rows made whole first, so an empty plan, gated, a no op apply.
        "repair.rows": lambda: _rows_whole(),
        # A32. Every row given the ContentLink value first, so the plan writes nothing.
        "repair.link": lambda: _link_rows(),
        # U132. The taxonomy copy lacks the genre Favorites class, so the plan adds it.
        "taxonomy.upgrade": lambda: _taxonomy_behind(),
        # U194. The template as the copy and a word answered; tests/test_taxonomy_word.py.
        "taxonomy.alias": lambda: _shipped_copy(["Latin Electronic", "Afro House"]),
        "taxonomy.folder": lambda: _shipped_copy(["Latin Electronic"]),
        # R-799. It reads every tagging record, none on this fixture.
        "tag.remap": [],
        # U114. No row lacks a genre, so an empty plan, gated, a no op apply.
        "tag.suggest": [],
        # U339. A row no library holds is listed gone, gated, a no op. tests/test_tag_set.py.
        "tag.set": ["Deep House", "--row", "no-such-row"],
        # U340. A row the collection lacks is left, gated, a no op. tests/test_tag_second.py.
        "tag.second": ["Deep House", "--row", "999999"],
        # U292. It reads the collection and writes nothing; tests/test_tag_backlog.py.
        "tag.backlog": [],
        # U294. An empty backlog: NO_OP after the acknowledgment and the gate.
        "tag.campaign": [],
        # U172. The library root holds no audio, so NO_OP; tests/test_tag_guess.py.
        "tag.guess": [str(library)],
        # U111. The intake tree native, so INBOX plans empty and still asks.
        "inbox.rotate": _intake_cut_over,
        # U134. Lazy: the tree cut over, one account pass run, no INBOX playlist, so NO_OP.
        "inbox.refill": _finished_account_playlist_pass_on_a_native_tree,
        # U166. Lazy: the tree cut over and no Analyze playlist, so NO_OP.
        "inbox.analyzed": _intake_cut_over,
        # U167. The check reads a copy of the fixture's database; tests/test_analyze_check.py.
        "analyze.check": [],
        # U327. Lazy: cut over, since the bridge refuses; no Analyze playlist, so an empty
        # scope, gated, NO_OP. It reads the acknowledgment first. tests/test_analyze_adopt.py.
        "analyze.adopt": _intake_cut_over,
        # U112. Its database area reads the acknowledgment first; both areas still ask.
        "organize": [],
        # U130. No pair marked: an empty plan, both gates ask, NO_OP; tests/test_sync_pair.py.
        "sync.pair": [],
        # U149. No year folder: NO_OP (UNREACHABLE_GATES). tests/test_sync_twins.py.
        "sync.twins": _an_account_with_no_year_folder,
        # U221. One twin holding one track: approving empties the hold, writing no database.
        "sync.release": _a_twin_holding_one_track,
        # U242. No playlist: empty plans, gate asked, nothing written. tests/test_u242_taken.py.
        "sync.taken": _an_account_with_no_year_folder,
        "sync.strip": _an_account_with_no_year_folder,
        # U287. Nothing downloaded, so the account is never asked; tests/test_sync_removed.py.
        "sync.removed": _an_account_with_no_year_folder,
    }[entry.name]
    if not callable(sample):
        return sample
    import inspect
    if monkeypatch is not None and "monkeypatch" in inspect.signature(sample).parameters:
        return sample(monkeypatch)
    return sample()


def _run_retire_over_one_old_gate() -> list[str]:
    """One ``profile.set`` run stopped at its gate thirty days ago, for ``run retire`` to ask over."""
    import os
    from datetime import datetime, timedelta, timezone
    then = datetime.now(timezone.utc) - timedelta(days=30)
    state = gates.new_run(registry.entry("profile.set"))
    state.created = output.timestamp(then)
    state.open_gate = "profile.set.apply"
    path = gates.save(state)
    os.utime(path, (then.timestamp(), then.timestamp()))
    return []


def _intake_set_reaching_account_gate(monkeypatch) -> list[str]:
    """A named local recording, so U129's account gate fires before recognition;
    tests/test_u129_set_account_playlist.py drives the writing path."""
    from cratekit.core import secrets
    from cratekit.intake import acrcloud
    from cratekit.label import catalogue
    from tests import outbound_fakes
    from tests.intake.test_recognition import FakeCarver, hit
    from tests.label_fakes import FakeCatalogue, catalogue_factory
    from tests.test_intake_missing_search import Hit
    from tests.test_outbound_workers import bind as bind_account
    secrets.set(str(secrets.Credential.IDENTIFY_KEY), "k-conformance")
    secrets.set(str(secrets.Credential.IDENTIFY_SIGNING_KEY), "s-conformance")

    class _Repeating:
        """One hit for every chunk, across every conformance drive of this verb."""

        def __init__(self) -> None:
            self.requests = []

        def __call__(self, request):
            import json

            from cratekit.intake.acrcloud import Response
            self.requests.append(request)
            body = hit("Aurora Bloom", "Sun Path")
            return Response(status=200, body=json.dumps(body).encode())

    monkeypatch.setattr(acrcloud, "http_transport", _Repeating())
    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: FakeCarver(25.0))
    fake = FakeCatalogue(
        searches={("Aurora Bloom", "Sun Path"): [Hit("tid-1", "Aurora Bloom", "Sun Path")]}
    )
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    bind_account(monkeypatch, outbound_fakes.StrictAccount())

    path = Path(config.load().library.root) / "Music" / "conformance-set.mp3"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"ID3")
    return [str(path), "--dj", "Probe", "--set-name", "Friday Night", "--set-date", "2026-05"]


def test_intake_set_sample_leaves_account_and_catalogue_seams_real(configured, monkeypatch):
    """The intake.set sample leaks no fake into later tests on this worker, since
    ``account.forget`` clears only the opened handle."""
    from cratekit.label import catalogue
    from cratekit.modules.outbound import account
    real_account = account.resolve
    real_catalogue = catalogue.resolve
    with monkeypatch.context() as nested:
        argv = _intake_set_reaching_account_gate(nested)
        entry = registry.entry("intake.set")
        code, _, _ = drive([*entry.path, *argv])
        assert code == int(ExitCode.DECISION_REQUIRED), (
            "the named local sample must reach the account gate before recognition"
        )
        assert account.resolve is not real_account
        assert catalogue.resolve is not real_catalogue
    seams = (("account", account, real_account), ("catalogue", catalogue, real_catalogue))
    for name, seam, real in seams:
        assert seam.resolve is real, (
            f"closing the intake.set sample's monkeypatch context did not restore "
            f"{name}.resolve; later tests on this worker would miss the guard"
        )


def _an_account_with_no_year_folder(monkeypatch) -> list[str]:
    """An account with no year folder and no playlist, bound through ``monkeypatch``."""
    from cratekit.label import catalogue
    from tests import outbound_fakes
    from tests.label_fakes import FakeCatalogue, catalogue_factory
    from tests.test_outbound_workers import bind as bind_account
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(FakeCatalogue(account=[])))
    bind_account(monkeypatch, outbound_fakes.FakeAccount())
    return []


def _a_twin_holding_one_track() -> list[str]:
    """One custom playlist twin's pair holding one track, for ``sync release`` to let go."""
    from cratekit.core import config
    from cratekit.modules.outbound import pairs
    store = pairs.PairStore(config.load())
    store.mark("acc-twin", "901", name="DOWNLOADED Twin", twin=True, on_hold={"t1": "A - B"})
    return ["acc-twin"]


def _a_pass_with_no_vocal_model_and_nothing_new(monkeypatch) -> list[str]:
    """No vocal model, and a ``sync all`` that queued nothing, bound through ``monkeypatch``."""
    from cratekit.analysis import vocals
    from cratekit.cli import tail
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", None)
    absent = "the 'vocals' extra is not installed here"
    monkeypatch.setattr(vocals, "missing_requirement", lambda: absent)
    real = tail.dispatch

    def nothing_new(argv):
        if list(argv[:2]) == ["sync", "all"]:
            return int(ExitCode.OK), {
                "outcome": "no_op",
                "data": {"summary": {"run_id": "conformance-pass", "queued": 0}},
                "warnings": [],
            }
        return real(argv)

    monkeypatch.setattr(tail, "dispatch", nothing_new)
    return []


def _with_the_source_playlist(make) -> list[str]:
    """The playlist every favourite is in, made by ``make(handle, source)`` when it is not
    already held. Answers no arguments."""
    from cratekit.core import rb_writer
    cfg = config.load()
    source = taxonomy.default_taxonomy().sub_class("favorites").signal_playlist
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        held = [row for row in handle.get_playlist(Name=source) if not rb_writer.is_folder(row)]
        if not held:
            make(handle, source)
            handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    return []


def _a_source_playlist() -> list[str]:
    """The playlist every favourite is in, present and empty."""
    return _with_the_source_playlist(lambda handle, source: handle.create_playlist(source))


def _a_source_playlist_in_a_folder() -> list[str]:
    """The playlist every favourite is in, alone in a Favorites folder."""

    def in_a_folder(handle, source):
        handle.create_playlist(source, parent=handle.create_playlist_folder("Favorites"))

    return _with_the_source_playlist(in_a_folder)


def _run_to_the_end(job) -> None:
    """Drive a queued job's resume command and require it to succeed."""
    from cratekit.cli import jobs as cli_jobs
    from cratekit.core import jobs
    from tests.cli_drive import drive as drive_json
    code, resumed = drive_json(cli_jobs.argv_for(job))
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed


def _finished_account_playlist_pass_on_a_native_tree() -> list[str]:
    """The intake tree native and one finished account playlist job; answers ``--pass``."""
    from cratekit.acquire import match
    from cratekit.core import jobs
    from cratekit.intake import cli as intake_cli
    from cratekit.intake import missing_cli
    from cratekit.sync import playlists
    _intake_cut_over()
    run_id = "2026-10-03T101500Z-cd34"
    track = {"artist": "Probe", "title": "One", "origin": match.TIDAL, "ref": "tid-one"}
    with jobs.open_store() as store:
        job = intake_cli.queue_playlist(
            store, config.load(), handler_key="intake.playlist", reference="pl-a",
            tracks={"tid-one": track}, run_id=run_id, source_id=playlists.SOURCE_ID,
            name="Sunset Warmup",
        )
    _run_to_the_end(job)
    return ["--pass", missing_cli.synced_name(run_id)]


def _finished_set_job_on_a_native_tree() -> list[str]:
    """The intake tree native, and one set job run to the end. Answers ``--job`` and its id."""
    from cratekit.acquire import match
    from cratekit.core import jobs
    from cratekit.intake import cli as intake_cli
    _intake_cut_over()
    tracks = {
        "rc_one": {"artist": "Probe", "title": "One", "origin": match.TEXT, "spelled": "Probe - One"}
    }
    page = {"title": "Probe - A Set", "uploader": "Probe", "upload_date": "20260503"}
    payload = {
        intake_cli.SOURCE: "https://example.invalid/a-set", intake_cli.TRACKS: tracks,
        intake_cli.CALLS: 1, intake_cli.UNREACHED: 0, intake_cli.PARTS: 1, intake_cli.PAGE: page,
    }
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key="intake.set", payload=payload, cfg=config.load(),
            item_ids=tuple(tracks),
        )
    _run_to_the_end(job)
    return ["--job", job.job_id]


def _record_native(cfg, tree, on) -> None:
    """Record ``tree`` of the shipped taxonomy database native since ``on``, under one root."""
    from cratekit.core import tree_registry
    from tests import cutover_fixtures
    record = tree_registry.TreeRecord(
        tree_id=tree.id, mode=tree_registry.Mode.DATABASE, cutover_on=on,
        root_id=cutover_fixtures.one_root(cfg, tree.display),
        source=tree_registry.DerivationSource.TAXONOMY,
    )
    tree_registry.write(cfg, tree_registry.read(cfg).with_record(record))


def _routing_tree_cut_over_with_a_source() -> list[str]:
    """The routing tree database native and the favourites source present. Answers no arguments."""
    from datetime import date

    from cratekit.core import rb_writer
    cfg = config.load()
    declared = taxonomy.default_taxonomy()
    _record_native(cfg, declared.tree, date(2026, 10, 9))
    source = declared.sub_class("favorites").signal_playlist
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        held = [row for row in handle.get_playlist(Name=source) if not rb_writer.is_folder(row)]
        playlist = held[0] if held else handle.create_playlist(source)
        # One track, since an emptied source refuses before the gate, in no genre
        # folder, so the plan writes nothing.
        if not list(handle.get_playlist_songs(PlaylistID=str(playlist.ID))):
            handle.add_to_playlist(playlist, "1")
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    return []


def _intake_cut_over() -> list[str]:
    """Record the configured library's intake tree database native. Answers no arguments."""
    from datetime import date
    _record_native(config.load(), taxonomy.default_taxonomy().intake, date(2026, 10, 3))
    return []


def _routing_tree() -> tuple[str, str]:
    """The routing tree this fixture's library declares: identifier, display name."""
    from cratekit.core import active_taxonomy
    declared = active_taxonomy.load(config.load())
    return declared.tree.id, declared.tree.display


def _a_file_in_the_library() -> Path:
    """One empty file with an audio suffix under the configured library, which
    ``intake file`` reads for tags and finds none."""
    path = Path(config.load().library.root) / "Music" / "conformance-single.flac"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    return path


def _ready_to_cut_over() -> list[str]:
    from tests import cutover_fixtures
    tree_id, display = _routing_tree()
    export, _root = cutover_fixtures.ready(config.load(), display)
    return [tree_id, "--export", str(export)]


def _update_every_content_row(sets: str, values: tuple) -> None:
    """One ``UPDATE`` of every content row of the configured database, committed."""
    import sqlite3

    from cratekit.core import rb_writer
    connection = sqlite3.connect(config.load().library.db_path)
    try:
        connection.execute(f"UPDATE {rb_writer.CONTENT_TABLE} SET {sets}", values)
        connection.commit()
    finally:
        connection.close()


def _rows_whole() -> list[str]:
    """Every content row given rekordbox's defaults, as rekordbox would have made it."""
    from cratekit.core import rb_writer
    defaults = rb_writer.CONTENT_ROW_DEFAULTS
    sets = ", ".join(f"{column} = ?" for column in defaults)
    _update_every_content_row(sets, tuple(defaults.values()))
    return []


def _link_rows() -> list[str]:
    """Every content row made whole with rekordbox's probe values, so ``repair link``
    plans nothing."""
    from cratekit.core import rb_writer
    from tests.test_repair_link import HOUSE
    _rows_whole()
    link, isrc = rb_writer.CONTENT_LINK_COLUMN, rb_writer.ISRC_COLUMN
    _update_every_content_row(f"{link} = ?, {isrc} = ''", (HOUSE,))
    return ["--set", f"1:{link}={HOUSE}", "--set", f"1:{isrc}="]


def _taxonomy_behind() -> list[str]:
    """The library's taxonomy copy made without the genre Favorites class."""
    from cratekit.core import taxonomy
    text = taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)
    head, _, tail = text.partition('[[sub_class]]\nid = "favorites"')
    assert tail, "the shipped template no longer declares the favorites class"
    _, _, rest = tail.partition("\n[")
    path = config.state_path("taxonomy_active", config.load())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(head + "[" + rest, encoding="utf-8")
    return []


def _shipped_copy(argv: list[str]) -> list[str]:
    """The library's taxonomy copy written as the shipped template, and ``argv``."""
    from cratekit.core import taxonomy
    path = config.state_path("taxonomy_active", config.load())
    path.parent.mkdir(parents=True, exist_ok=True)
    text = taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)
    path.write_text(text, encoding="utf-8")
    return argv


def _already_cut_over() -> list[str]:
    from datetime import date

    from cratekit.core import tree_registry
    tree_id, _display = _routing_tree()
    cfg = config.load()
    if not tree_registry.read(cfg).is_database_native(tree_id):
        tree_registry.record_cutover(
            cfg, tree_id, root_id="a-root", on=date(2026, 9, 27),
            source=tree_registry.DerivationSource.TAXONOMY,
        )
    return [tree_id]


def _sample_decisions(entry: registry.Entry) -> list[str]:
    """Answers for every gate the verb declares, so a drive reaches its logic."""
    return [flag for spec in entry.gates for flag in ("-d", f"{spec.name}={spec.options[0]}")]


@pytest.mark.parametrize("entry", LANDED, ids=lambda e: e.name)
def test_conformance_2_exit_codes_are_from_the_vocabulary_and_never_status_two(
    entry, configured, monkeypatch
):
    code, _, _ = drive([*_sample_decisions(entry), *entry.path, *_sample_arguments(entry, monkeypatch)])
    assert code in {int(c) for c in ExitCode}
    assert code != int(ExitCode.USAGE)


def test_conformance_2_only_the_entry_point_may_end_the_process():
    """Only the entry point ends the process; one boundary converts a cause into a
    status, since ``SystemExit`` escapes an ``except Exception`` upstream."""
    offenders: list[str] = []
    for path, source in package_sources():
        relative = path.relative_to(SRC_ROOT).as_posix()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "exit" and isinstance(node.func.value, ast.Name):
                    if node.func.value.id in {"sys", "os"}:
                        offenders.append(f"{relative}:{node.lineno}")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {"exit", "quit"}:
                    offenders.append(f"{relative}:{node.lineno}")
    assert not offenders, f"process exits outside the dispatcher: {offenders}"


def test_conformance_2_no_module_builds_an_exit_code_from_a_bare_integer():
    """A code constructed from a literal is a code nothing keeps in sync."""
    offenders: list[str] = []
    for path, source in package_sources():
        relative = path.relative_to(SRC_ROOT).as_posix()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == "ExitCode" and node.args:
                    if isinstance(node.args[0], ast.Constant):
                        offenders.append(f"{relative}:{node.lineno}")
    assert not offenders, f"ExitCode built from a literal: {offenders}"


#: Gates that cannot be reached in a test environment, each with the reason. A
#: listed gate that is reached fails below and says to delete the entry.
UNREACHABLE_GATES: Mapping[str, str] = MappingProxyType(
    {
        "sync.removed.confirm": (
            "asked only by a plan that offers a row, which needs a pass swept, landed into a "
            "native intake tree and read again on the account with a track taken off, and the "
            "conformance fixture downloaded nothing, so the sample asks the account nothing and "
            "ends NO_OP with no gate, by U288's brief. The gate, its explicit two act answer, the "
            "removal and its refusals are driven in tests/test_sync_removed.py."
        ),
        "sync.removed.retire": (
            "asked only by sync removed --retire over a synced playlist the account no longer "
            "lists whose id answered not found, and the conformance sample passes no flag and "
            "downloaded nothing, so it asks the account nothing and ends NO_OP with no gate "
            "(U320). The gate, its explicit two act answer, the retirement and its abort are "
            "driven in tests/test_sync_removed_gone.py."
        ),
        "rebuild.accept": (
            "asked only by rebuild --tree naming a tree no rebuild can reproduce, the intake tree "
            "above all, that a restore marked unconverged, and the conformance fixture has no "
            "native tree, so the sample queues nothing and asks nothing (U219). That path never "
            "queues, so the queued resume contract has nothing to hold it to. The gate, its "
            "explicit two act answer and the disposition it records are driven in "
            "tests/test_resort_scope.py over a restore the real detection marked."
        ),
        "export.set.rename": (
            "asked only by export set --rename JOB, which names a succeeded set job, and the "
            "conformance fixture's queue holds none, so the sample takes the tracklist path, which "
            "asks export.set.confirm instead. One drive reaches one path. The rename gate, its "
            "explicit two act answer and its refusals are driven in "
            "tests/test_export_set_rename.py over a set job and an INSPIRATION playlist."
        ),
        "favorites.split.approve": (
            "asked only over a library that still holds a quarter playlist beside All Favorites, "
            "and approving one writes: the quarter is retired, which the conformance fixture "
            "refuses for its unpinned rekordbox, since a pin is never adopted on a user's behalf "
            "(S2). A library with no quarter asks nothing, by U145's brief, so the sample is that "
            "library and the verb ends NO_OP with no gate. The gate, its explicit two act answer, "
            "the split and its refusals are driven in tests/test_favorites_split.py."
        ),
        "favorites.order.approve": (
            "asked only over a Favorites folder that is not in order, and approving one writes the "
            "positions of its playlists, which the conformance fixture refuses for its unpinned "
            "rekordbox, since a pin is never adopted on a user's behalf (S2). A folder already in "
            "order asks nothing, by U180's brief, so the sample is that folder and the verb ends "
            "NO_OP with no gate. The gate, its explicit two act answer, the write and its refusals "
            "are driven in tests/test_favorites_order.py."
        ),
        "intake.file.native": (
            "asked only on a library whose intake tree is recorded database native, for the reason "
            "intake.land.native gives below: the conformance fixture's intake tree is on the xml "
            "bridge, where the same verb shows its plan and asks nothing, and the medium is the "
            "tree's mode, not an argument. The gate, its explicit two act answer and its refusals "
            "are driven in tests/test_intake_writers_native.py on a library whose intake tree has "
            "cut over."
        ),
        "intake.land.native": (
            "asked only on a library whose intake tree is recorded database native, and the "
            "conformance fixture's intake tree is on the xml bridge, where the same verb asks "
            "intake.land.confirm instead. One drive reaches one medium, and the medium is the "
            "tree's mode, not an argument, so no argument list reaches both. The native gate, its "
            "explicit two act answer and its refusals are driven in "
            "tests/test_intake_land_native.py on a library whose intake tree has cut over."
        ),
        "intake.shelve.native": (
            "asked only over a plan that moves a batch, and approving one writes a path on the "
            "collection, which the conformance fixture refuses for its unpinned rekordbox, since a "
            "pin is never adopted on a user's behalf (S2). The sample is --report, which plans "
            "against a read only copy and asks nothing by design (U154). The gate, its explicit "
            "two act answer, the write and its refusals are driven in tests/test_intake_shelve.py "
            "on a library whose batch has landed."
        ),
        "label.playlists.crawl": (
            "asked only by a full build of a FOLLOWED label whose listing estimates more provider "
            "calls than playlists_cli.FULL_BUILD_CALLS, and the conformance sample names a label "
            "nobody follows, which is a plan of nothing decided before a catalogue is resolved and "
            "asks label.playlists.confirm instead (U191). The crawl gate, its explicit two act "
            "answer, a decline and a stale answer over a grown listing are driven in "
            "tests/test_label_playlists_releases.py."
        ),
        "sync.twins.approve": (
            "asked only over an account holding a downloaded custom playlist in a year folder that "
            "has no twin, and approving one writes a folder and a playlist in rekordbox, which the "
            "conformance fixture refuses for its unpinned rekordbox, since a pin is never adopted "
            "on a user's behalf (S2). An account with nothing to backfill asks nothing, by U149's "
            "brief, so the sample is that account and the verb ends NO_OP with no gate. The gate, "
            "its explicit two act answer, the write and its refusals are driven in "
            "tests/test_sync_twins.py."
        ),
        "write.cloudsync.unreadable": (
            "raised by the guarded writer only when rekordbox's Cloud Library Sync state cannot be "
            "READ, which is a property of the machine rather than of the verb. A test environment "
            "has no rekordbox installation to have an unreadable sync state, so no drive can "
            "provoke it and requiring it would refuse every correct verb that declares it. Closes "
            "with the disposable database fixture R-13 names, which is the first environment able "
            "to produce the state."
        ),
    }
)


def _assert_gate_reach(entry: registry.Entry, reached: list[str]) -> None:
    """Every gate the entry declares fired, except the ones named unreachable,
    since only a drive that counts what fired holds a handler to its declaration."""
    declared = {spec.name for spec in entry.gates}
    exempt = declared & set(UNREACHABLE_GATES)
    silent = sorted(declared - exempt - set(reached))
    assert not silent, (
        f"{entry.name} declares {silent} and its handler never reached them. A declared gate that "
        f"cannot fire is a decision the registry promises and the verb does not ask, and for a "
        f"destructive verb that is the concurrent-writer question going unasked with the suite "
        f"green. Either reach it, drop the declaration, or name it in UNREACHABLE_GATES with the "
        f"reason no drive can provoke it."
    )
    surprising = sorted(set(reached) & exempt)
    assert not surprising, (
        f"{entry.name} reached {surprising}, which UNREACHABLE_GATES says no "
        f"drive can provoke. The exemption is stale: delete the entry so every "
        f"verb declaring that gate is held to reaching it."
    )


#: Verbs that read the backup acknowledgment before their gate (R-733). Named,
#: so other gated verbs reaching their gates without one stays under test.
ACKNOWLEDGED_BEFORE_THE_GATE = {
    name: f"tests/{module}.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate"
    for name, module in {
        "inbox.analyzed": "test_inbox_analyzed",
        "inbox.refill": "test_inbox_refill",
        "adopt.move": "test_adopt_move",
        "inbox.rotate": "test_inbox_rotate",
        "tag.rows": "test_tag_rows",
        "analyze.adopt": "test_analyze_adopt",
        "repair.rows": "test_repair_rows",
        "repair.link": "test_repair_link",
        "favorites.refresh": "test_genre_favorites",
        "favorites.backfill": "test_favorites_backfill",
        "favorites.split": "test_favorites_split",
        "favorites.order": "test_favorites_order",
        "tag.suggest": "test_tag_suggest",
        "tag.set": "test_tag_set",
        "tag.campaign": "test_tag_campaign",
        "intake.inspiration": "test_set_inspiration_playlist",
        # U112. Only its database area is refused without one; the account area
        # is still asked, which its own suite drives.
        "organize": "test_organize",
        "sync.pair": "test_sync_pair",
        "sync.twins": "test_sync_twins",
    }.items()
}


def _acknowledge_where_the_verb_reads_it_first(entry: registry.Entry, cfg) -> None:
    if entry.name not in ACKNOWLEDGED_BEFORE_THE_GATE:
        return
    from cratekit.core import session
    session.record_acknowledgment(cfg, terminal=lambda: True)


def test_every_verb_acknowledged_for_conformance_is_refused_without_one_elsewhere():
    """Each acknowledged verb names the test that drives it without an
    acknowledgment, and that test exists."""
    root = Path(__file__).resolve().parent.parent
    for name, node_id in ACKNOWLEDGED_BEFORE_THE_GATE.items():
        assert registry.entry(name).landed, name
        path, _, function = node_id.partition("::")
        tree = ast.parse((root / path).read_text(encoding="utf-8"))
        defined = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        assert function in defined, f"{name} names {node_id}, which does not exist"


def _conformance_3(entry: registry.Entry, positional: list[str]) -> list[str]:
    """Drive one gated verb to OK the way R34 says it is reached.

    Returns the gates it refused at, asserting they are exactly the entry's minus
    :data:`UNREACHABLE_GATES`, which holds a handler to its declared gates."""
    declared = {spec.name: spec for spec in entry.gates}
    answered: list[str] = []
    reached: list[str] = []
    run_id: str | None = None

    # One drive per gate plus the one that succeeds; refusing more often than it has
    # gates means an undeclared refusal, which falling out of the loop makes visible.
    for _ in range(len(declared) + 1):
        resume = ["--run", run_id] if run_id is not None else []
        argv = ["--output", "json", *answered, *resume, *entry.path, *positional]
        code, out, err = drive(argv)
        if code == int(ExitCode.OK):
            _assert_gate_reach(entry, reached)
            return reached
        assert code == int(ExitCode.DECISION_REQUIRED), err or out
        envelope = json.loads(out)
        # The gate rides on the cause, not on ``pending_human_action``, which means a
        # person must act outside the tool and implies PENDING_HUMAN.
        detail = envelope["cause"]["detail"]
        assert detail["gate"] in declared, (
            f"{entry.name} refused at {detail['gate']!r}, which it does not declare; a gate "
            f"outside the registry is invisible to every conformance assertion"
        )
        spec = declared[detail["gate"]]
        assert detail["options"] == list(spec.options)
        assert detail["explicit"] is spec.explicit
        assert envelope["resumable"] is True
        reached.append(spec.name)
        if not spec.explicit:
            # One act: an ordinary gate is answerable inline, and flags accumulate so a
            # later gate is reached with the first still answered.
            answered += ["-d", f"{spec.name}={spec.options[0]}"]
            continue
        # Two acts (R34): the inline answer is refused again, since an explicit gate is
        # satisfied only by a separate act recorded with its actor.
        run_id = envelope["run_id"]
        inline = ["-d", f"{spec.name}={spec.options[0]}"]
        code, _, _ = drive([*answered, *inline, "--run", run_id, *entry.path, *positional])
        assert code == int(ExitCode.DECISION_REQUIRED), (
            f"{spec.name} is explicit, and an inline answer satisfied it. R34's whole content is "
            f"that this class of decision cannot be typed onto the command that was already running"
        )
        assert spec.name not in gates.load(run_id).decisions, (
            "the refused inline answer was recorded anyway, so the second act "
            "would find the gate already answered by the first"
        )
        answer = ["run", "decide", run_id, spec.name, spec.options[0], "--actor", "a-person"]
        code, _, err = drive(answer)
        assert code == int(ExitCode.OK), err
        assert gates.load(run_id).decisions[spec.name].actor == "a-person", (
            "an explicit decision names who asserted it, or the record cannot "
            "tell a person's answer from the process asking itself"
        )

    raise AssertionError(f"{entry.name} still refuses after every gate it declares was answered")


@pytest.mark.parametrize("entry", LANDED, ids=lambda e: e.name)
def test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds(entry, configured, monkeypatch):
    """Assertion 3: a gate refuses, and OK comes only after R34's acts."""
    if not entry.gates:
        return
    _acknowledge_where_the_verb_reads_it_first(entry, configured)
    _conformance_3(entry, _sample_arguments(entry, monkeypatch))


def _swap_in(monkeypatch, promoted: registry.Entry) -> None:
    """Put a modified entry in front of the dispatcher, ``_BY_NAME`` included."""
    entries = tuple(promoted if e.name == promoted.name else e for e in registry.ENTRIES)
    monkeypatch.setattr(registry, "ENTRIES", entries)
    monkeypatch.setattr(registry, "_BY_NAME", {**dict(registry._BY_NAME), promoted.name: promoted})


def test_conformance_3_admits_an_explicitly_gated_verb(configured, monkeypatch):
    """Assertion 3 admits an explicitly gated verb (``profile.set`` promoted)."""
    base = registry.entry("profile.set")
    promoted = replace(base, gates=(replace(base.gates[0], explicit=True),))
    _swap_in(monkeypatch, promoted)
    assert _conformance_3(promoted, ["slim"]) == ["profile.set.apply"]
    config.reset_cache()
    assert config.load().profile.name == "slim", (
        "the verb reported OK without doing its work, so the two acts bought a "
        "status rather than a profile change"
    )


#: A second gate for a one gate verb, explicit, as entries with their own
#: confirmation plus the shared cloud sync decision carry.
_SECOND_GATE = registry.GateSpec(
    name="profile.set.second", options=("go", "abort"),
    prompt="A second decision on the same verb?", explicit=True,
)


def _require_every_gate(ctx):
    """A handler that reaches all of its entry's gates, in declaration order."""
    for spec in ctx.entry.gates:
        ctx.gate.require(spec)
    return ctx.envelope(data={"checks": [], "summary": {}})


@pytest.mark.parametrize(
    "explicit_first", [False, True], ids=["plain-then-explicit", "explicit-then-explicit"]
)
def test_conformance_3_admits_a_verb_carrying_two_gates(explicit_first, configured, monkeypatch):
    """Assertion 3 admits a verb carrying two gates, in both orderings; only the
    handler is synthetic."""
    base = registry.entry("profile.set")
    first = replace(base.gates[0], explicit=explicit_first)
    promoted = replace(base, gates=(first, _SECOND_GATE))
    _swap_in(monkeypatch, promoted)
    monkeypatch.setattr("cratekit.cli.verbs.profile.apply_profile", _require_every_gate)
    assert _conformance_3(promoted, ["slim"]) == [first.name, _SECOND_GATE.name], (
        "the verb reached OK without both of its gates refusing first, so one of "
        "them was answered by something other than a decision"
    )


def test_the_csv_writer_guard_bites_and_stays_quiet_on_correct_code():
    """The csv writer guard fires on every import shape, aliased ones included,
    and stays quiet on an unrelated attribute of that name and on a read (P7)."""
    assert constructs_a_csv_writer("import csv\ncsv.writer(handle)\n")
    assert constructs_a_csv_writer("from csv import DictWriter\nDictWriter(handle, [])\n")
    assert constructs_a_csv_writer("import csv as spreadsheet\nspreadsheet.writer(handle)\n"), (
        "an aliased import switches the guard off, which is the evasion it was armed against"
    )
    assert constructs_a_csv_writer("from csv import writer as w\nw(handle)\n")
    assert not constructs_a_csv_writer("import xml\nxml.writer(handle)\n")
    assert not constructs_a_csv_writer("import csv\nfor row in csv.reader(handle):\n    pass\n")
    for _path, source in package_sources():
        assert not constructs_a_csv_writer(source), (
            "the guard fires somewhere in the tree it is meant to leave alone"
        )


@pytest.mark.parametrize("entry", [e for e in ALL_ENTRIES if e.adjudicates], ids=lambda e: e.name)
def test_conformance_4_adjudication_goes_through_the_review_queue(entry, configured):
    """Assertion 4 (U11): adjudication goes through the review queue.

    This drives the shared surface, not the verb, a gap a residual records. The static half walks
    each landed verb's source for a comma separated writer."""
    import importlib
    review = importlib.import_module("cratekit.core.review")
    queue = review.adjudicated_queues()[0]
    keyed = {"handler": entry.handler_key}
    with review.open_store(configured) as store:
        item = review.offer(
            store, queue=queue, kind="conformance", identity=keyed, payload=keyed,
            options=(review.Option(option_id="opt-one", summary="the one candidate"),),
            handler_key=entry.handler_key,
        )
        assert item.verdict is None
        addressed = review.list_items(store, handler_key=entry.handler_key).items
        assert [held.item_id for held in addressed] == [item.item_id], (
            f"{entry.name} declares that it adjudicates, and the queue cannot "
            f"show what it produced under its own key"
        )

    verdict = ["--verdict", "accepted", "--option", "opt-one"]
    code, out, err = drive(["--output", "json", "review", "resolve", item.item_id, *verdict])
    assert code == int(ExitCode.OK), err or out
    with review.open_store(configured) as store:
        settled = review.get(store, item.item_id)
        assert settled.verdict is review.Verdict.ACCEPTED
        assert review.count_unresolved(store) == 0
    # The replacement must not be what it replaces; the review directory is walked,
    # so a second file beside the database is covered (P3).
    for current, _directories, files in os.walk(config.state_path("review_queue", configured)):
        for name in files:
            assert not name.endswith(".csv"), (
                f"the review queue itself wrote {name}, which is the hand edited "
                f"file this whole surface replaces"
            )
    path = SRC_ROOT / Path(*entry.module.split(".")).with_suffix(".py")
    if path.is_file():
        offenders = constructs_a_csv_writer(path.read_text())
        assert not offenders, (
            f"{entry.name} declares that it adjudicates and writes a comma separated file for a "
            f"person to edit: {offenders}. Adjudication is a persisted review item (R12)."
        )


@pytest.mark.parametrize("entry", [e for e in ALL_ENTRIES if e.long_running], ids=lambda e: e.name)
def test_conformance_5_long_work_is_queued_rather_than_run_inline(entry):
    """Assertion 5, armed now that the job engine has landed (U10)."""
    import importlib
    jobs = importlib.import_module("cratekit.core.jobs")
    assert entry.argv_builder
    assert hasattr(jobs, "get")


def _state_fingerprint(*roots) -> dict[str, tuple[int, int]]:
    """Size and modification time of every file under each root, for zero writes."""
    found: dict[str, tuple[int, int]] = {}
    for root in roots:
        base = Path(root)
        if not base.is_dir():
            continue
        for current, _directories, files in os.walk(base):
            for name in files:
                path = Path(current) / name
                try:
                    stat = path.stat()
                except OSError:  # pragma: no cover - a file that vanished mid-walk
                    continue
                found[str(path)] = (stat.st_size, stat.st_mtime_ns)
    return found


@pytest.mark.parametrize("entry", [e for e in ALL_ENTRIES if e.destructive], ids=lambda e: e.name)
def test_conformance_6_destructive_verbs_refuse_without_the_session_gates(
    entry, configured, tmp_path
):
    """Assertion 6 (U8): destructive verbs refuse without the session gates.

    Three refusals, three codes, zero writes each. The trigger is ``destructive``, not ``writes``
    (KTD24). This drives the shared gate, a gap a residual records."""
    import importlib
    session = importlib.import_module("cratekit.core.session")
    assert hasattr(session, "assert_gates")
    right = configured.library.volume_id
    matching = lambda _path: right  # noqa: E731 - one line, and naming it adds nothing
    roots = (configured.library.root, config.installation_state_dir(), config.config_dir())

    def refuse_with(**gate_arguments) -> ExitCode:
        before = _state_fingerprint(*roots)
        with pytest.raises(CratekitError) as excinfo:
            with session.assert_gates(configured, workflow=entry.name, **gate_arguments):
                raise AssertionError("the gates admitted a session they should have refused")
        assert _state_fingerprint(*roots) == before, (
            f"{entry.name} wrote to the state tree on a refused path; a refusal "
            f"that leaves a trace is a refusal that has already done something"
        )
        return excinfo.value.cause.code

    # 1. A mismatched volume, first, since it must refuse before any path resolves.
    wrong_volume = refuse_with(
        identity_provider=lambda _path: "0000-0000", mount_enumerator=lambda: ()
    )
    # 2. No backup acknowledgment: the volume matches and nothing is recorded.
    no_acknowledgment = refuse_with(identity_provider=matching)
    # 3. The lock held elsewhere: the acknowledgment is minted first, and the lock
    #    is taken on a separate handle, as another process would hold it.
    session.record_acknowledgment(configured, terminal=lambda: True)
    lock = session.lock_path(configured)
    lock.parent.mkdir(parents=True, exist_ok=True)
    contender = open(lock, "a+")
    try:
        rb_writer._acquire_exclusive(contender)
        held = refuse_with(identity_provider=matching)
    finally:
        contender.close()
    codes = (held, no_acknowledgment, wrong_volume)
    assert codes == (ExitCode.LIBRARY_BUSY, ExitCode.ACK_REQUIRED, ExitCode.LIBRARY_UNAVAILABLE)
    assert len(set(codes)) == 3, "three refusals that cannot be told apart is one refusal"


_SHIPPED = taxonomy.default_taxonomy()
_TREES = (_SHIPPED.tree, _SHIPPED.intake, _SHIPPED.intake_old, _SHIPPED.inspiration)
TAXONOMY_IDS = frozenset(
    {tree.id for tree in _TREES}
    | set(_SHIPPED.bucket_ids())
    | {band.id for band in _SHIPPED.energy.bands}
    | {sub.id for sub in _SHIPPED.sub_classes}
)
TAXONOMY_DISPLAY_NAMES = frozenset(
    {tree.display for tree in _TREES}
    | {bucket.display for bucket in _SHIPPED.buckets}
    | {band.display for band in _SHIPPED.energy.bands}
)


@pytest.mark.parametrize("entry", ALL_ENTRIES, ids=lambda e: e.name)
def test_conformance_7_taxonomy_terms_are_stable_identifiers(entry):
    """R19: a verb resolves the declared taxonomy, never a display name, since a
    display name is a persisted key in five places and a rename orphans them."""
    for term in entry.taxonomy_terms:
        assert term in TAXONOMY_IDS, (
            f"{entry.name} names {term!r}, which is not a stable taxonomy id in "
            f"the shipped template"
        )
        assert term not in TAXONOMY_DISPLAY_NAMES


def test_conformance_7_no_verb_module_hardcodes_a_taxonomy_display_name():
    offenders: list[str] = []
    for entry in LANDED:
        path = SRC_ROOT / Path(*entry.module.split(".")).with_suffix(".py")
        if not path.is_file():
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Constant) and node.value in TAXONOMY_DISPLAY_NAMES:
                offenders.append(f"{entry.name}: {node.value!r}")
    assert not offenders, offenders


@pytest.mark.parametrize("entry", ALL_ENTRIES, ids=lambda e: e.name)
def test_conformance_8_anything_that_writes_declares_a_doctor_precondition(entry):
    """R3: anything that writes declares a doctor precondition, so health checks
    gate the work rather than only feeding a report."""
    if entry.writes:
        assert entry.doctor_checks, (
            f"{entry.name} writes {sorted(entry.writes)} and declares no health check to pass first"
        )


def test_conformance_8_every_declared_check_key_exists_in_the_doctor_registry(configured):
    """Every declared check key exists in the doctor registry (U27); behaviour is below."""
    import importlib
    doctor = importlib.import_module("cratekit.cli.doctor")
    known = set(doctor.CHECK_KEYS)
    declared = {key for entry in registry.entries() for key in entry.doctor_checks}
    assert declared <= known, sorted(declared - known)


def test_conformance_8_every_declared_precondition_can_pass_and_can_refuse(configured):
    """Every declared precondition passes on a healthy machine, refuses on a broken one.

    No constant answer passes both. If a new precondition cannot fail on ``machines.hostile()``,
    extend ``hostile()`` rather than relaxing this."""
    import importlib
    doctor = importlib.import_module("cratekit.cli.doctor")
    declared = {key for entry in registry.entries() for key in entry.doctor_checks}
    assert declared, "no verb declares a precondition; the walk is broken, not the tree"
    # The fixture is set up, not healthy: it records no rekordbox pin, since a pin
    # is never adopted for a user (S2). The healthy run adds one here only.
    document = dict(configured.to_toml_dict())
    pin = {"pinned_app_version": machines.INSTALLED_APP_VERSION, "validated_on": "2026-08-01"}
    cfg = config.from_dict({**document, "rekordbox": pin})
    healthy = {f.key: f for f in doctor.run(cfg, probes=machines.green()).findings}
    broken = {f.key: f for f in doctor.run(cfg, probes=machines.hostile()).findings}
    assert _precondition_problems(declared, healthy, broken) == []


def _precondition_problems(declared, healthy, broken) -> list[str]:
    """Every way two reports fail to show a precondition that did work, as a function."""
    from cratekit.cli.doctor import Status
    problems: list[str] = []
    for key in sorted(declared):
        if key not in healthy or key not in broken:
            problems.append(f"{key} was not answered on both machines")
            continue
        for finding in (healthy[key], broken[key]):
            if not finding.title.strip():
                problems.append(f"{key} answered with no title")
            if len(finding.detail.strip()) <= 20:
                problems.append(
                    f"{key} answered with nothing that says what was observed: {finding.detail!r}"
                )
        if healthy[key].status is Status.FAIL:
            problems.append(
                f"{key} refuses on a machine where nothing is broken, so it fires "
                f"on a correct install: {healthy[key].detail}"
            )
        if broken[key].status is not Status.FAIL:
            problems.append(
                f"{key} is declared as a precondition by "
                f"{sorted(e.name for e in registry.entries() if key in e.doctor_checks)} "
                f"and does not refuse on a machine where it is broken, so no verb "
                f"declaring it is gated on anything: {broken[key].detail}"
            )
        elif broken[key].remedy is None:
            problems.append(f"{key} refuses with no remedy")
    return problems


def test_conformance_8_rejects_a_doctor_that_answers_without_working():
    """The guard rejects three stub doctors that answer every key without working."""
    from cratekit.cli.doctor import Finding, Status
    declared = {key for entry in registry.entries() for key in entry.doctor_checks}

    def stub(status: Status, detail: str = "", title: str = "") -> dict:
        return {k: Finding(key=k, title=title, status=status, detail=detail) for k in declared}

    empty = stub(Status.OK)
    assert _precondition_problems(declared, empty, empty), "an empty answer passed"
    always_green = stub(Status.OK, detail="everything is fine on this machine", title="t")
    assert _precondition_problems(declared, always_green, always_green), (
        "a check that can never refuse passed"
    )
    always_red = stub(Status.FAIL, detail="everything is broken on this machine", title="t")
    assert _precondition_problems(declared, always_red, always_red), (
        "a check that fires on a correct install passed"
    )


# ── parity ───────────────────────────────────────────────────────────────────
def test_every_feature_row_maps_to_a_verb_at_its_stated_disposition():
    claimed: dict[int, list[registry.Entry]] = {}
    for entry in registry.entries():
        for row in entry.feature_rows:
            claimed.setdefault(row, []).append(entry)
    missing: list[str] = []
    wrongly_claimed: list[str] = []
    misgated: list[str] = []
    for feature in registry.FEATURES:
        owners = claimed.get(feature.row, [])
        if feature.disposition in {"cut", "defer"}:
            if owners:
                wrongly_claimed.append(
                    f"row {feature.row} ({feature.title}) is {feature.disposition} "
                    f"but claimed by {[o.name for o in owners]}"
                )
            continue
        if not owners:
            missing.append(f"row {feature.row} ({feature.title}) has no verb")
            continue
        if feature.disposition == "core" and all(o.module_id for o in owners):
            misgated.append(
                f"row {feature.row} is Core but every verb for it is behind a module toggle"
            )
        if feature.disposition == "module" and feature.row not in registry.POLICY_ROWS:
            if not any(o.module_id for o in owners):
                misgated.append(
                    f"row {feature.row} is a Module row but no verb for it is gated "
                    f"by a module toggle, so a slim install gets it anyway (R5)"
                )
    assert not missing and not wrongly_claimed and not misgated, "\n".join(
        missing + wrongly_claimed + misgated
    )


def test_every_source_entry_point_is_either_mapped_or_written_down_as_cut():
    """Every source entry point is mapped or written down as cut, wider than the
    inventory, since some live console scripts have no inventory row."""
    fixture = Path(__file__).resolve().parent / "fixtures" / "dj_tools_scripts.txt"
    lines = fixture.read_text().splitlines()
    scripts = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    # 37 since U105 (R-193). The pin catches a list that shrinks.
    assert len(scripts) == 37, "the transcribed entry-point list changed size"
    mapped = {name for entry in registry.entries() for name in entry.source_scripts}
    cut_text = (REPO_ROOT / "CUT.md").read_text()
    unaccounted = [s for s in scripts if s not in mapped and s not in cut_text]
    assert not unaccounted, (
        f"source entry points that no verb claims and CUT.md does not explain: {unaccounted}"
    )


def test_every_declared_module_toggle_is_used_by_at_least_one_verb():
    """Every declared toggle gates some verb, since a toggle nobody reads is a
    config switch that does nothing."""
    used = {entry.module_id for entry in registry.entries()} - {None}
    unused = sorted(set(profiles.MODULES) - used - registry.DEFERRED_MODULES)
    assert not unused, (
        f"declared modules no verb is gated by: {unused}. Either a verb is "
        f"missing its module_id or the toggle should not exist."
    )


def _verb_paths(
    parser: argparse.ArgumentParser, prefix: tuple[str, ...] = ()
) -> set[tuple[str, ...]]:
    """Every command path a built parser answers to, walked through its subparsers."""
    found: set[tuple[str, ...]] = set()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for word, child in action.choices.items():
                found.add((*prefix, word))
                found |= _verb_paths(child, (*prefix, word))
    return found


#: Every toggle that gates at least one LANDED verb, derived from the registry so
#: a toggle whose first verb lands joins the parametrisation on its own.
_TOGGLES_WITH_LANDED_VERBS = sorted(
    {entry.module_id for entry in registry.landed_entries()} - {None} - profiles.ALWAYS_AVAILABLE
)


@pytest.fixture(scope="module")
def slim_verb_paths():
    return _verb_paths(cli.build_parser(membership=profiles.resolve("slim")))


def test_every_live_toggle_is_driven_by_the_toggle_test_below():
    """Every live toggle gates a landed verb, which stops the derived
    parametrisation below silently shrinking."""
    waiting = {entry.module_id for entry in registry.entries() if not entry.landed}
    live = set(profiles.MODULES) - registry.DEFERRED_MODULES - waiting
    assert live <= set(_TOGGLES_WITH_LANDED_VERBS), sorted(live - set(_TOGGLES_WITH_LANDED_VERBS))


@pytest.mark.parametrize("module", _TOGGLES_WITH_LANDED_VERBS)
def test_a_module_toggle_alone_switches_its_landed_verbs_on_and_off(module, slim_verb_paths):
    """R-4: a module toggle alone switches its landed verbs on and off.

    Driven through the real resolver and parser; a gated verb reachable with its module off is a
    Module row shipping as core (R5)."""
    verbs = [entry.path for entry in registry.landed_entries() if entry.module_id == module]
    added = _verb_paths(cli.build_parser(membership=profiles.resolve("slim", {module: True})))
    removed = _verb_paths(cli.build_parser(membership=profiles.resolve("full", {module: False})))
    for path in verbs:
        assert path not in slim_verb_paths, f"{path} is on in the slim profile"
        assert path in added, f"turning {module} on did not reach {path}"
        assert path not in removed, f"turning {module} off left {path} reachable"


def test_a_verb_carrying_a_resume_argv_builder_declares_that_it_queues():
    """A verb carrying a resume argv builder declares ``long_running``.

    ``tests/test_queued_resume_contract.py`` derives its population from both flags. The floor
    sits on the measured count (U61)."""
    carriers = [entry for entry in registry.ENTRIES if entry.argv_builder]
    assert len(carriers) >= 19, (
        f"only {len(carriers)} entries declare a resume argv builder, which is "
        f"below the 19 measured when U61 last moved this floor; either the "
        f"registry shrank or this guard has stopped deriving anything"
    )
    mislabelled = sorted(entry.name for entry in carriers if not entry.long_running)
    assert not mislabelled, (
        f"these verbs declare a resume argv builder and do not declare long_running: "
        f"{mislabelled}. Either the builder is dead code, or the verb queues and has just dropped "
        f"out of every derived guard in tests/test_queued_resume_contract.py"
    )


#: Long running entries whose shell legitimately files no job under its own key,
#: with the reason: queueing is not what they do, rather than not done yet.
QUEUES_BY_ROLE_NOT_BY_ENQUEUE: Mapping[str, str] = MappingProxyType(
    {
        "job.resume": (
            "the resume verb spawns the child that drives an existing job and never files one of "
            "its own"
        ),
    }
)


def _enqueue_calls(tree: ast.AST) -> int:
    found = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        callee = node.func
        if isinstance(callee, ast.Attribute) and callee.attr == "enqueue":
            found += 1
        elif isinstance(callee, ast.Name) and callee.id == "enqueue":
            found += 1
    return found


def test_a_verb_declaring_the_queueing_contract_has_a_shell_that_queues():
    """R-149, U60: a verb declaring the queueing contract has a shell that queues.

    Parsed rather than searched, since prose naming ``enqueue`` is no call."""
    queued = [e for e in registry.ENTRIES if e.landed and e.long_running]
    assert queued, "no landed verb queues, so this guard derives nothing"
    stale = sorted(set(QUEUES_BY_ROLE_NOT_BY_ENQUEUE) - {e.name for e in queued})
    assert not stale, f"exemptions naming no landed long-running verb: {stale}"
    inline = []
    for entry in queued:
        if entry.name in QUEUES_BY_ROLE_NOT_BY_ENQUEUE:
            continue
        path = SRC_ROOT / Path(*entry.module.split(".")).with_suffix(".py")
        if not _enqueue_calls(ast.parse(path.read_text())):
            inline.append(entry.name)
    assert not inline, (
        f"these verbs declare long_running and an argv builder and their shell "
        f"never calls enqueue: {inline}. Either the verb does its work inline and "
        f"the entry should stop claiming a queue, or the shell should queue"
    )


def test_no_verb_claims_a_module_the_profile_layer_does_not_declare():
    known = set(profiles.MODULES) | profiles.ALWAYS_AVAILABLE
    claimed = {entry.module_id for entry in registry.entries()} - {None}
    assert claimed <= known, sorted(claimed - known)


def test_library_adoption_is_available_in_every_profile():
    """R5 names it explicitly: opt-in modules, except adoption."""
    adopt = registry.entry("adopt.scan")
    for name in profiles.PROFILE_NAMES:
        assert adopt.available_to(profiles.resolve(name))


# The unit's verification step: a scripted non-interactive run hits a gate
def test_a_scripted_run_with_no_terminal_reaches_a_gate_and_exits_with_its_code(
    configured, tmp_path
):
    """A scripted run with no standard input reaches a gate, exits with a documented
    code and leaves a resumable run, rather than aborting at end of file."""
    result = subprocess.run(
        [sys.executable, "-m", "cratekit.cli", *_TO_SLIM], capture_output=True, text=True,
        stdin=subprocess.DEVNULL, env=dict(os.environ, PYTHONPATH=str(SRC_ROOT)), cwd=tmp_path,
    )
    assert result.returncode == int(ExitCode.DECISION_REQUIRED), result.stderr
    envelope = json.loads(result.stdout)
    assert envelope["cause"]["detail"]["gate"] == "profile.set.apply"
    assert envelope["resumable"] is True
    assert gates.load(envelope["run_id"]).open_gate == "profile.set.apply"


def test_an_unconfigured_machine_refuses_with_a_precondition_and_a_remedy():
    """An unconfigured machine is a state, not an internal error."""
    code, out, _ = drive(["--output", "json", "profile", "show"])
    assert code == int(ExitCode.PRECONDITION)
    envelope = json.loads(out)
    assert envelope["cause"]["reason"] == "config-unusable"
    assert envelope["cause"]["remediation"]["remedy"] == str(Remedy.RUN_SETUP)


@pytest.mark.parametrize(
    "raised",
    [ZeroDivisionError("something nobody predicted"), SystemExit(2)],
    ids=["something-unexpected", "exits-the-process-directly"],
)
def test_a_verb_that_raises_or_exits_becomes_an_internal_cause(configured, monkeypatch, raised):
    """Nothing escapes the boundary as a traceback the user has to interpret, and a direct
    ``SystemExit``, a ``BaseException``, is converted rather than obeyed."""

    def explode(ctx):
        raise raised

    monkeypatch.setattr("cratekit.cli.verbs.profile.show", explode)
    code, out, _ = drive(["--output", "json", "profile", "show"])
    assert code == int(ExitCode.INTERNAL)
    assert code != int(ExitCode.USAGE)
    assert json.loads(out)["cause"]["reason"] == "internal-error"


def test_human_mode_renders_the_gate_with_its_options_and_how_to_answer(configured):
    _, _, err = drive(["profile", "set", "slim"])
    assert "profile.set.apply" in err
    assert "apply, abort" in err
    assert "crate run decide" in err


def _context_spec(*, explicit: bool) -> registry.GateSpec:
    """One gate to ask, built here because the property is the resolver's."""
    return registry.GateSpec(
        name="context.probe", options=("proceed", "abort"), prompt="Proceed?", explicit=explicit
    )


def _probe_state() -> gates.RunState:
    return gates.RunState(run_id="r", verb="probe", created="now")


def test_a_gate_refusal_carries_what_the_verb_consulted(configured):
    """U49: a gate refusal carries the facts the verb consulted, as a backup age."""
    resolver = gates.Gates(state=_probe_state())
    ages = {"ages": [{"portion": "database", "state": "never-recorded"}]}
    with pytest.raises(gates.DecisionRequired) as raised:
        resolver.require(_context_spec(explicit=False), context=ages)
    shown = raised.value.cause.detail["shown"]
    assert shown["ages"] == [{"portion": "database", "state": "never-recorded"}]


def test_a_gate_refusal_with_no_context_carries_no_shown_key_at_all(configured):
    """A gate refusal with no context carries no ``shown`` key at all, so "shows
    nothing" stays distinct from "looked and found nothing"."""
    with pytest.raises(gates.DecisionRequired) as raised:
        gates.Gates(state=_probe_state()).require(_context_spec(explicit=False))
    detail = raised.value.cause.detail
    assert "shown" not in detail
    assert set(detail) == {"gate", "options", "prompt", "explicit", "run_id"}


def test_the_explicit_inline_refusal_carries_the_context_too(configured):
    """The explicit inline refusal carries the context too, since it is the one a
    person meets when trying to shortcut the acknowledgment (R34)."""
    spec = _context_spec(explicit=True)
    resolver = gates.Gates(state=_probe_state(), supplied={spec.name: "proceed"})
    with pytest.raises(gates.DecisionRequired) as raised:
        resolver.require(spec, context={"holder": {"host": "elsewhere", "pid": 41}})
    assert raised.value.cause.detail["shown"]["holder"]["host"] == "elsewhere"


def test_human_mode_renders_what_the_verb_showed_and_is_unchanged_without_it(configured):
    """Human mode renders what the verb showed, so a terminal user is not left with
    a bare question; a refusal carrying nothing prints as it did before."""
    spec = _context_spec(explicit=False)
    ages = {"ages": [{"portion": "database", "state": "never-recorded"}]}
    carried = render.render_gate(gates.DecisionRequired(spec, "r", ages).cause)
    assert "portion=database" in carried
    assert "state=never-recorded" in carried
    bare = render.render_gate(gates.DecisionRequired(spec, "r").cause)
    assert "portion" not in bare
    assert bare.splitlines() == [
        "Proceed?",
        "",
        "  gate:    context.probe",
        "  options: proceed, abort",
        "",
        "  answer:  crate run decide r context.probe <option>",
        "  then:    add --continue to answer and carry on the run in one command",
        "  or:      rerun with -d context.probe=<option>",
    ]


def _reaches_no_gate(ctx):
    """A handler that declares gates and asks none of them."""
    return ctx.envelope(data={"checks": [], "summary": {}})


def _reaches_only_the_first_gate(ctx):
    ctx.gate.require(ctx.entry.gates[0])
    return ctx.envelope(data={"checks": [], "summary": {}})


_APPLY_PROFILE = "cratekit.cli.verbs.profile.apply_profile"


@pytest.mark.parametrize(
    "handler", [_reaches_no_gate, _reaches_only_the_first_gate], ids=["no-gate", "only-the-first"]
)
def test_conformance_3_fails_a_verb_that_declares_a_gate_and_never_asks_it(
    configured, monkeypatch, handler
):
    """Assertion 3 fails a verb that declares a gate and never asks it, in both
    shapes, since nothing else holds a handler to its declared gates."""
    base = registry.entry("profile.set")
    promoted = replace(base, gates=(base.gates[0], _SECOND_GATE))
    _swap_in(monkeypatch, promoted)
    monkeypatch.setattr(_APPLY_PROFILE, handler)
    with pytest.raises(AssertionError, match="never reached them"):
        _conformance_3(promoted, ["slim"])


def test_the_unreachable_exemption_covers_one_named_gate_and_expires_on_its_own(
    configured, monkeypatch
):
    """The exemption covers one named gate with a reason, and expires on its own."""
    base = registry.entry("profile.set")
    with_exempt = replace(base, gates=(base.gates[0], registry.CLOUD_SYNC_UNREADABLE_GATE))
    _swap_in(monkeypatch, with_exempt)
    monkeypatch.setattr(_APPLY_PROFILE, _reaches_only_the_first_gate)
    assert _conformance_3(with_exempt, ["slim"]) == ["profile.set.apply"], (
        "the cloud-sync gate cannot be provoked in this environment, so a verb "
        "that declares it and reaches its own gate is correct"
    )
    # The stale half: reaching an exempt gate must say the exemption is over.
    monkeypatch.setattr(_APPLY_PROFILE, _require_every_gate)
    with pytest.raises(AssertionError, match="exemption is stale"):
        _conformance_3(with_exempt, ["slim"])


#: Exact membership: adding a gate is a red suite, as with ``EXPECTED_PENDING``.
EXPECTED_UNREACHABLE_GATES = frozenset(
    {
        "write.cloudsync.unreadable", "intake.land.native", "intake.file.native",
        "export.set.rename", "favorites.split.approve", "favorites.order.approve",
        "intake.shelve.native", "label.playlists.crawl", "sync.twins.approve", "rebuild.accept",
        "sync.removed.confirm", "sync.removed.retire",
    }
)


def test_the_unreachable_exemption_set_is_exactly_the_intended_one():
    """The exempt gates are exactly the intended set; another is a decision, and
    each is driven in its own suite."""
    assert set(UNREACHABLE_GATES) == EXPECTED_UNREACHABLE_GATES, (
        f"the exemption set is {sorted(UNREACHABLE_GATES)} and this file declares "
        f"{sorted(EXPECTED_UNREACHABLE_GATES)}. Every entry here is a gate no verb has to reach, "
        f"which is the assertion switched off for that gate across every entry that declares it."
    )


def test_every_unreachable_gate_is_real_and_carries_a_reason():
    """An exemption naming a gate nobody declares is an exemption nobody can audit."""
    for name, reason in UNREACHABLE_GATES.items():
        registry.gate(name)  # raises KeyError if no entry declares it
        assert len(reason) > 80, (
            f"{name} is exempted from assertion 3 with a reason too thin to "
            f"judge; say what makes it unprovokable and what would change that"
        )


def test_the_reports_shell_reads_each_engine_from_its_own_module_on_first_use():
    """The reports module is toggleable, so the shell imports no engine at load
    (U303) and resolves each one, under its old attribute name, on first read."""
    import importlib

    from cratekit.cli import reports as reports_cli
    for attribute, module in (
        ("aging", "aging"), ("coverage", "coverage"), ("duplicates", "duplicates"),
        ("export", "export"), ("library_report", "library"),
    ):
        expected = importlib.import_module(f"cratekit.modules.reports.{module}")
        assert getattr(reports_cli, attribute) is expected, attribute
    with pytest.raises(AttributeError):
        reports_cli.no_such_engine  # noqa: B018
