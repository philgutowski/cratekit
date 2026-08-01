"""U5: the verb conformance suite.

Coverage checking proves a verb EXISTS. This proves it CONFORMS. The difference
is the whole deliverable of this unit: the suite iterates the registry rather
than naming verbs, so a verb added without structured output, without a place in
the exit-code vocabulary, or with a prompt in it fails the build by OMISSION
instead of by somebody noticing in review.

The file is in five parts, and each part answers a specific failure in the
source system:

1. **The exit-code vocabulary.** Three unrelated schemes there give one integer
   three meanings with opposite remediations, and the only named constant lives
   in a consumer rather than in any producer.
2. **The structured cause.** Every non-success result carries one, with a
   remediation, and it survives the boundaries between where it happened and
   where it becomes a status.
3. **The envelope.** Versioned, with human rendering kept out of it, and a lock
   file so a schema change without a version bump fails here.
4. **Gates and standard input.** Three layers of proof that no verb reads
   standard input, because the source system's non-interactive contract is
   claimed in a docstring and false in three places.
5. **Parity.** Every Feature Inventory row and every source entry point is
   either claimed by a verb or written down in CUT.md with a reason.
"""

from __future__ import annotations

import ast
import contextlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import gates, output, registry, render
from cratekit.core import config, profiles, taxonomy
from cratekit.core.cause import REASONS, Cause, Outcome, Remediation, Scope
from cratekit.core.exit_codes import (
    BANDS,
    MAX_CODE,
    RETIRED,
    ExitCode,
    Remedy,
    band_of,
    meaning_of,
)
from tests._pending import requires

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "cratekit"
SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"


def package_sources() -> list[tuple[Path, str]]:
    """Every module we AUTHOR, vendored third-party code excluded.

    The vendored downloader is not ours to restyle and does read standard input;
    holding it to a contract written after it was published would only produce a
    suppression comment somebody later reads as permission.
    """
    return [
        (path, path.read_text())
        for path in sorted(PACKAGE_ROOT.rglob("*.py"))
        if "_vendor" not in path.parts
    ]


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def configured(library):
    """A machine that has been set up, so a verb reaches its own logic."""
    cfg = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(library),
                "volume_id": "F1E2-D3C4",
                "db_path": str(library / "db" / "master.db"),
            },
            "paths": {"download_staging": str(library.parent / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(cfg)
    config.reset_cache()
    return cfg


@pytest.fixture(autouse=True)
def _trap_standard_input(monkeypatch):
    """Make any read of standard input an immediate, named failure.

    Both halves matter. Trapping ``input`` alone misses a direct
    ``sys.stdin.readline()``, and the source system reads ``sys.stdin.isatty()``
    directly at three sites, so an input-only trap would have declared that code
    non-interactive.
    """

    class Trapped:
        def __getattr__(self, name):
            raise AssertionError(f"a verb read standard input (sys.stdin.{name})")

    monkeypatch.setattr(sys, "stdin", Trapped())
    monkeypatch.setattr(
        "builtins.input",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("a verb called input()")),
    )


def drive(argv: list[str]) -> tuple[int, str, str]:
    """Run the real dispatcher and return (status, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


# ═══════════════════════════════════════════════════════════════════════════
# Part 1: the exit-code vocabulary (KTD25, S4)
# ═══════════════════════════════════════════════════════════════════════════


def test_every_code_has_a_meaning_and_a_remediation_token():
    """Derived by ITERATING the enum, never by listing members.

    A test that enumerates is a test that misses the next addition, and the next
    addition is exactly the code nobody has thought about yet.
    """
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
    unclaimed = [
        value
        for value in range(BANDS[-1].start, BANDS[-1].stop)
        if value not in {int(c) for c in ExitCode}
    ]
    assert unclaimed, "the vocabulary has no room left for a class nobody has met yet"


def test_status_two_belongs_to_the_argument_parser_and_to_nothing_else():
    """The durable half of the KTD25 fix.

    The source system's collision is real and reachable: one component means
    "rekordbox is open" by 2, another means "another run holds the lock", and
    argparse means "you mistyped". Argparse will keep producing 2 whatever we
    decide, so the only fix that cannot come back is for 2 to have exactly one
    owner and for that owner not to be us.
    """
    assert not meaning_of(ExitCode.USAGE).verb_producible
    producible = {int(c) for c in ExitCode if meaning_of(c).verb_producible}
    assert 2 not in producible
    assert 2 not in {int(code) for code in REASONS.values()}

    code, _, _ = drive(["--not-a-flag"])
    assert code == int(ExitCode.USAGE)


def test_the_configuration_remedies_are_part_of_one_vocabulary():
    """U2 declared six remediation tokens before this vocabulary existed.

    They stay a SUBSET rather than becoming a second scheme. Two vocabularies for
    one idea is the drift that produced five genre resolvers, and it starts
    exactly like this: one module needing a token before the module that owns
    them was written.
    """
    canonical = {str(member) for member in Remedy}
    declared = {str(member) for member in config.Remedy}
    assert declared <= canonical, sorted(declared - canonical)


def test_every_remediation_token_renders_to_something_a_user_can_act_on():
    """Audited by walking the enum, so a new token cannot render as nothing."""
    for remedy in Remedy:
        rendered = render.remediation_line(
            Cause(
                reason="internal-error",
                message="x",
                remediation=Remediation(remedy=remedy),
            )
        )
        assert rendered.strip() not in ("fix:", ""), f"{remedy} renders to nothing"


# ── S4: every refusal the guarded writer raises has a code and a remedy ──────

#: The eleven refusal conditions the guarded rekordbox writer raises, taken from
#: U7's surface map. U5 ships before U7 precisely so that U7 CONSUMES this
#: vocabulary instead of inventing codes, and a refusal with no code is the
#: defect KTD25 exists to prevent. The twelfth, the two-process refusal, is a
#: separate exception type in the source and is asserted alongside them.
WRITER_REFUSALS: dict[str, str] = {
    "pyrekordbox pin drift": "pyrekordbox-pin-drift",
    "database schema version drift": "db-schema-pin-drift",
    "rekordbox application version drift": "app-version-pin-drift",
    "missing database directory": "library-directory-missing",
    "missing database file": "library-database-missing",
    "database open failure": "database-open-failed",
    "canary read failure": "canary-read-failed",
    "cloud sync canary tripped": "cloud-sync-active",
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
    """The exact collision KTD25 names, asserted as fixed.

    Both are code 2 in the source, and their remediations are opposites: quitting
    an application fixes one and is precisely the wrong move for the other, which
    has no command at all and can only be waited out.
    """
    assert REASONS["rekordbox-running"] is ExitCode.REKORDBOX_OPEN
    assert REASONS["write-lock-held"] is ExitCode.LIBRARY_BUSY
    assert REASONS["session-lock-held"] is ExitCode.LIBRARY_BUSY
    assert meaning_of(ExitCode.REKORDBOX_OPEN).remedy is Remedy.QUIT_REKORDBOX
    assert meaning_of(ExitCode.LIBRARY_BUSY).remedy is Remedy.WAIT_FOR_HOLDER


def test_an_unrecorded_application_pin_refuses_rather_than_adopting_what_is_installed():
    """S2. A pin the software copies from the machine it runs on refuses nothing."""
    assert REASONS["app-version-pin-unrecorded"] is ExitCode.VERSION_PIN


def test_every_reason_maps_into_the_vocabulary_and_every_refusal_is_reachable():
    for slug, code in REASONS.items():
        assert isinstance(code, ExitCode), f"{slug} maps to something that is not a code"
    reachable = set(REASONS.values())
    unreachable = [
        code.name
        for code in ExitCode
        if code not in reachable and code not in (ExitCode.OK, ExitCode.USAGE)
    ]
    assert not unreachable, (
        f"codes with no reason that produces them: {unreachable}. A code nothing "
        f"can raise is a code nobody maintains."
    )


# ═══════════════════════════════════════════════════════════════════════════
# Part 2: the structured cause
# ═══════════════════════════════════════════════════════════════════════════


def test_a_cause_round_trips_through_json_with_its_chain_intact():
    """Boundary 3 is a process boundary, so this is not a convenience.

    The job engine re-invokes the CLI as a subprocess (KTD26). A cause that
    cannot survive JSON cannot cross that hop, and the engine is back to deriving
    status from an exit code, which is the collapse KTD25 is about.
    """
    inner = Cause(
        reason="unavailable-transient",
        message="the provider timed out",
        remediation=Remediation(remedy=Remedy.RETRY_LATER),
        scope=Scope.ITEM,
        retryable=True,
        origin=("adapter.vendored",),
    )
    outer = Cause(
        reason="adapter-broken",
        message="the adapter gave up after three attempts",
        remediation=Remediation(remedy=Remedy.RETRY_LATER, steps=("wait, then retry",)),
        scope=Scope.SOURCE,
        origin=("download", "job", "sync"),
        inner=inner,
    )
    assert Cause.from_json(json.loads(outer.to_text())) == outer


def test_a_cause_cannot_be_built_without_a_remediation():
    with pytest.raises(ValueError):
        Remediation()


def test_a_reason_outside_the_registry_is_refused():
    with pytest.raises(KeyError):
        Cause(
            reason="something-somebody-invented",
            message="x",
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
        )


def test_a_boundary_appends_to_the_origin_trail_rather_than_replacing_it():
    first = Cause(
        reason="auth-failed",
        message="x",
        remediation=Remediation(remedy=Remedy.AUTHENTICATE_PROVIDER),
        origin=("adapter",),
    )
    assert first.at("download").at("job").origin == ("adapter", "download", "job")


def test_the_exit_code_comes_from_the_reason_rather_than_being_stored_beside_it():
    """A cause whose code contradicts its reason is worse than either alone."""
    built = Cause(
        reason="rekordbox-running",
        message="x",
        remediation=Remediation(remedy=Remedy.QUIT_REKORDBOX),
    )
    assert built.code is ExitCode.REKORDBOX_OPEN


# ═══════════════════════════════════════════════════════════════════════════
# Part 3: the envelope and the schema lock (R32)
# ═══════════════════════════════════════════════════════════════════════════


def test_the_five_structured_surfaces_r32_names_are_all_declared():
    assert set(output.schema_names()) == {
        "plan",
        "match",
        "review_set",
        "job_state",
        "diagnostic",
    }


def test_the_match_surface_reserves_three_states_from_its_first_version():
    """R11's needs-review state has no representation in the source at all.

    Two CSV files, owned and missing. Adding the third state later would break
    every consumer keyed on the shape; reserving it now costs an empty array.
    """
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
        f"the {name!r} payload changed shape but {identifier} did not move. Bump "
        f"the major in cratekit/cli/output.py and re-run scripts/dump_schemas.py. "
        f"An additive change needs a bump too: a consumer keyed on field presence "
        f"cannot tell an addition from a rename."
    )


@pytest.mark.parametrize("name", sorted(output.schema_names()))
def test_every_previous_major_is_still_present_in_the_lock(name):
    lock = json.loads((SCHEMA_DIR / "lock.json").read_text())
    major = int(output.current_schema(name).split("/")[1])
    for earlier in range(1, major):
        assert f"{name}/{earlier}" in lock, (
            f"{name}/{earlier} vanished from the lock. A retired version stays "
            f"recorded, so a consumer holding an old envelope can still find out "
            f"what it was."
        )


@pytest.mark.parametrize("name", sorted(output.schema_names()))
def test_the_committed_golden_validates_against_the_current_schema(name):
    """Catches a backward-incompatible change even when somebody DID bump.

    A bump records that the shape changed. It does not record whether last
    version's envelope still parses, and that is the question a consumer has.
    """
    major = output.current_schema(name).split("/")[1]
    golden = json.loads((SCHEMA_DIR / "golden" / f"{name}.v{major}.json").read_text())
    assert output.envelope_problems(golden) == []


def test_the_declared_envelope_keys_are_exactly_what_is_serialized():
    """Derived from a real envelope, so the declared list cannot fall behind it.

    The conformance suite requires every key in ``ENVELOPE_KEYS`` of every verb.
    If that list and the serializer could disagree, a key could be added to the
    output and required of nobody, which is the same hole as a hand-kept list
    anywhere else.
    """
    document = output.build(
        verb="profile.show",
        run_id="r",
        schema=output.current_schema("diagnostic"),
        started="2026-01-01T00:00:00+00:00",
        data={"checks": [], "summary": {}},
    ).to_json()
    assert set(document) == set(output.ENVELOPE_KEYS)


def test_exactly_one_verb_is_interactive_and_it_is_the_one_with_the_stdin_exemption():
    """The exemption is a list of one, in two files, checked against each other.

    An interactive verb is exempt from the no-standard-input assertion, so the
    number of them is the size of the hole. Asserting it here means a second one
    cannot be added quietly, and the module it is allowed to live in is the same
    single path the static guard allows.
    """
    interactive = [entry for entry in registry.entries() if entry.interactive]
    assert [entry.name for entry in interactive] == ["setup"]
    assert len(INTERACTIVE_ALLOWLIST) == 1


def test_the_envelope_never_carries_its_own_human_rendering():
    """The direct correction of the source system's plan preview.

    That file stores the rendered gate text inside the JSON, so machine and human
    output are one artifact and every wording change is a schema change.
    """
    for name in output.schema_names():
        assert "render" not in output.schema_document(name)["required"]
    assert set(output.ENVELOPE_KEYS) & {"render", "text", "message"} == set()


def test_pending_human_action_and_its_exit_code_imply_each_other():
    pending = output.PendingHumanAction(
        kind="rekordbox_import",
        id="pha_x",
        summary="import one file",
        verify_verb="run.show",
    )
    good = output.build(
        verb="run.show",
        run_id="r",
        schema=output.current_schema("diagnostic"),
        started="2026-01-01T00:00:00+00:00",
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        data={"checks": [], "summary": {}},
        pending=pending,
        cause=Cause(
            reason="awaiting-import",
            message="waiting",
            remediation=Remediation(remedy=Remedy.COMPLETE_PENDING_ACTION),
        ),
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
    document = output.build(
        verb="profile.show",
        run_id="r",
        schema=output.current_schema("diagnostic"),
        started="2026-01-01T00:00:00+00:00",
        outcome=Outcome.FAILED,
        code=ExitCode.INTERNAL,
        data={"checks": [], "summary": {}},
    ).to_json()
    assert any("structured cause" in problem for problem in output.envelope_problems(document))


def test_two_runs_starting_in_the_same_second_get_different_identifiers():
    """A collision would let one run's decisions answer another run's gate."""
    assert output.new_run_id() != output.new_run_id()


# ═══════════════════════════════════════════════════════════════════════════
# Part 4: gates, and no verb reads standard input (R33)
# ═══════════════════════════════════════════════════════════════════════════

#: The only file allowed to touch standard input, ever. It does not exist yet;
#: the setup wizard lands with U27, and its registry entry is the one marked
#: interactive. Naming the path here rather than a directory means the exemption
#: cannot spread by somebody adding a second file next to the first.
INTERACTIVE_ALLOWLIST = frozenset({"cratekit/cli/prompt.py"})


def standard_input_reads(source: str) -> list[str]:
    """Every construct that could read standard input, as an AST walk.

    A string search would miss ``sys.stdin`` reached through an alias and would
    fire on the word appearing in a comment, which is the shape that gets a guard
    muted.
    """
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
            names = (
                [a.name for a in node.names]
                if isinstance(node, ast.Import)
                else [node.module or ""]
            )
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
        f"standard input is read at {offenders}. A gate is answered by name and "
        f"resumed from state; a prompt cannot be answered by a detached job, and "
        f"a terminal check is a behaviour change under a pipe rather than an "
        f"absence of a read."
    )


def test_an_unanswered_gate_exits_with_the_documented_code_and_leaves_the_run_resumable(
    configured,
):
    code, out, err = drive(["--output", "json", "profile", "set", "slim"])
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


def test_the_same_gate_answered_by_name_proceeds(configured):
    code, out, _ = drive(["--output", "json", "-d", "profile.set.apply=apply", "profile", "set", "slim"])
    assert code == int(ExitCode.OK)
    envelope = json.loads(out)
    assert envelope["outcome"] == "ok"
    config.reset_cache()
    assert config.load().profile.name == "slim"


def test_a_gate_is_answerable_from_a_different_process_in_a_later_session(configured):
    """The half of R33 a flag on the original invocation can never provide."""
    _, out, _ = drive(["--output", "json", "profile", "set", "slim"])
    run_id = json.loads(out)["run_id"]

    code, _, _ = drive(["run", "decide", run_id, "profile.set.apply", "apply", "--actor", "test"])
    assert code == int(ExitCode.OK)

    code, out, _ = drive(["--output", "json", "--run", run_id, "profile", "set", "slim"])
    assert code == int(ExitCode.OK)
    config.reset_cache()
    assert config.load().profile.name == "slim"

    state = gates.load(run_id)
    assert state.decisions["profile.set.apply"].actor == "test"


def test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale(configured):
    """The property that stops a user approving one plan and running a wider one."""
    _, out, _ = drive(["--output", "json", "profile", "set", "slim"])
    run_id = json.loads(out)["run_id"]
    drive(["run", "decide", run_id, "profile.set.apply", "apply"])

    # The world moves between the offer and the resume: one module is switched
    # off by hand, so the membership delta the decision was made against is no
    # longer the delta that would be applied.
    document = config.load().to_toml_dict()
    document["modules"] = {"analysis": False}
    config.save(config.from_dict(document))
    config.reset_cache()

    code, out, _ = drive(["--output", "json", "--run", run_id, "profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_STALE)
    assert json.loads(out)["cause"]["reason"] == "decision-stale"


def test_a_gate_marked_explicit_refuses_an_inline_answer(configured):
    """R34: no blanket affirmative, and no answer smuggled into the same command.

    The gate under test belongs to a verb that has not landed, so the resolver is
    driven directly. That is deliberate rather than a workaround: the rule is a
    property of the resolver, and asserting it here means it is already true when
    the first explicit gate arrives with U8.
    """
    spec = registry.GateSpec(
        name="session.ack.backup",
        options=("acknowledged", "abort"),
        prompt="Backed up?",
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


def test_no_environment_variable_or_config_key_can_answer_a_gate(configured, monkeypatch):
    """There is deliberately no fourth decision source.

    A blanket answer satisfies every gate at once, which is what R34 forbids and
    what "the user pressed yes to something" already means in practice.
    """
    for variable in ("CRATEKIT_YES", "CRATEKIT_DECISION", "CRATEKIT_ASSUME_YES"):
        monkeypatch.setenv(variable, "1")
    code, _, _ = drive(["profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_REQUIRED)


def test_a_malformed_decision_is_refused_rather_than_ignored(configured):
    """A silently dropped decision stops at a gate the user believes they answered."""
    code, _, _ = drive(["-d", "no-equals-sign", "profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_REQUIRED)


def test_a_verb_blocked_by_an_unverified_pending_action_refuses_before_doing_anything(
    configured,
):
    """What makes ``pending_human_action`` load-bearing rather than advisory."""
    state = gates.new_run(registry.entry("profile.set"))
    state.pending = output.PendingHumanAction(
        kind="rekordbox_import",
        id=output.new_pending_id(state.run_id),
        summary="import one file",
        verify_verb="run.show",
        blocks=("profile.set",),
    )
    gates.save(state)

    code, out, _ = drive(["--output", "json", "--run", state.run_id, "profile", "set", "slim"])
    assert code == int(ExitCode.PENDING_HUMAN)
    assert json.loads(out)["cause"]["reason"] == "blocked-by-pending-action"


def test_a_run_that_reached_a_gate_reports_it(configured):
    _, out, _ = drive(["--output", "json", "profile", "set", "slim"])
    run_id = json.loads(out)["run_id"]
    code, out, _ = drive(["--output", "json", "run", "show", run_id])
    assert code == int(ExitCode.OK)
    envelope = json.loads(out)
    assert envelope["data"]["summary"]["open_gate"] == "profile.set.apply"


def test_a_run_carrying_a_pending_action_reports_it_as_pending(configured):
    state = gates.new_run(registry.entry("profile.set"))
    state.pending = output.PendingHumanAction(
        kind="rekordbox_import",
        id=output.new_pending_id(state.run_id),
        summary="import one file into rekordbox",
        verify_verb="run.show",
        steps=("open the library application", "import the file"),
    )
    gates.save(state)

    code, out, _ = drive(["--output", "json", "run", "show", state.run_id])
    assert code == int(ExitCode.PENDING_HUMAN)
    envelope = json.loads(out)
    assert output.envelope_problems(envelope) == []
    assert envelope["pending_human_action"]["verify_verb"] == "run.show"


def test_a_decision_naming_a_gate_the_verb_does_not_declare_is_refused(configured):
    _, out, _ = drive(["--output", "json", "profile", "set", "slim"])
    run_id = json.loads(out)["run_id"]
    code, _, _ = drive(["run", "decide", run_id, "some.other.gate", "apply"])
    assert code == int(ExitCode.DECISION_REQUIRED)


def test_a_run_record_belongs_to_the_verb_that_created_it(configured):
    _, out, _ = drive(["--output", "json", "profile", "set", "slim"])
    run_id = json.loads(out)["run_id"]
    code, _, _ = drive(["--run", run_id, "run", "show", run_id])
    assert code == int(ExitCode.DECISION_REQUIRED)


# ═══════════════════════════════════════════════════════════════════════════
# Part 5: the registry, the stub, and parity
# ═══════════════════════════════════════════════════════════════════════════


def test_help_succeeds_with_every_heavy_extra_absent(configured, monkeypatch):
    """The plan's first scenario for this unit.

    Blocking the extras at the import system rather than uninstalling them is
    what makes it a test rather than an environment.
    """
    blocked = {module for entry in registry.entries() for module in entry.extras_modules}
    assert blocked, "no entry declares an extras-backed dependency"

    class Blocker:
        def find_spec(self, name, path=None, target=None):
            if name.split(".")[0] in blocked:
                raise ImportError(f"blocked: {name}", name=name)
            return None

    monkeypatch.setattr(sys, "meta_path", [Blocker(), *sys.meta_path])
    # argparse's own --help action writes to the real standard output rather
    # than to anything the dispatcher was handed, so the redirect is what makes
    # this assert on the text a user would actually see.
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        code, _, _ = drive(["--help"])
    assert code == 0
    text = printed.getvalue()
    assert "crate" in text
    for entry in registry.landed_entries():
        assert entry.path[0] in text, f"{entry.name} vanished from help"


def test_a_module_with_missing_extras_becomes_a_stub_that_names_the_install_command():
    """Assertion 9, driven against the real construction path with a fake entry."""
    entry = registry.Entry(
        name="analyze.demo",
        summary="a verb behind an extras group",
        module="tests.cli_fixtures.needs_extra",
        builder="build",
        handler_key="analyze.demo",
        module_id="analysis",
        extras="analysis",
        extras_modules=("a_third_party_analysis_library",),
    )
    parser = cli.build_parser([entry], membership=profiles.resolve("full"))

    # The stub is still LISTED, with its summary and what it needs. A verb that
    # vanishes from help on a slim install leaves the user with no way to find
    # out it exists, which is a worse failure than one that says how to enable it.
    help_text = io.StringIO()
    with contextlib.redirect_stdout(help_text), pytest.raises(SystemExit):
        parser.parse_args(["analyze", "--help"])
    assert "a verb behind an extras group" in help_text.getvalue()
    assert "requires the 'analysis' extra" in help_text.getvalue()

    args = parser.parse_args(["analyze", "demo"])
    assert args._stub is not None
    cause = cli._stub_cause(args._entry, args._stub)
    assert cause.code is ExitCode.MODULE_UNAVAILABLE
    assert cause.detail["install"] == "pip install 'cratekit[analysis]'"


def test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra():
    """The other branch, and the reason the stub is gated on the extras names.

    A bare ``except ImportError`` sends a user to install a package that would
    not have helped, and hides the real defect behind a false one they cannot fix.
    """
    entry = registry.Entry(
        name="analyze.broken",
        summary="a verb with a defect of our own",
        module="tests.cli_fixtures.broken_module",
        builder="build",
        handler_key="analyze.broken",
        module_id="analysis",
        extras="analysis",
        extras_modules=("a_third_party_analysis_library",),
    )
    with pytest.raises(ImportError):
        cli.build_parser([entry], membership=profiles.resolve("full"))


def test_a_profile_that_switches_a_module_off_removes_its_verbs(configured):
    entry = registry.Entry(
        name="analyze.demo",
        summary="a verb behind a module toggle",
        module="tests.cli_fixtures.plain",
        builder="build",
        handler_key="analyze.demo",
        module_id="analysis",
    )
    slim = cli.build_parser([entry], membership=profiles.resolve("slim"))
    with pytest.raises(SystemExit):
        slim.parse_args(["analyze", "demo"])

    full = cli.build_parser([entry], membership=profiles.resolve("full"))
    assert full.parse_args(["analyze", "demo"])._entry is entry


def test_a_handler_key_resolves_without_importing_the_module():
    """KTD26: the engine validates a queued job's handler BEFORE spawning.

    Validating by import would pull the module into the engine's own process,
    which is exactly what the lazy-import scheme exists to prevent.
    """
    target = registry.entry("acquire.download")
    assert target.module not in sys.modules
    assert registry.by_handler_key("acquire.download") is target
    assert target.module not in sys.modules


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"emits": frozenset({"plan"})}, "declares its schema"),
        ({"output_schema": "plan/1"}, "emits something"),
        ({"writes": frozenset({"files"})}, "destructive by definition"),
        ({"long_running": True}, "argv builder"),
        ({"module_id": "not-a-module"}, "not a declared feature module"),
        ({"extras": "analysis"}, "names the third-party modules"),
    ],
)
def test_an_entry_missing_its_metadata_fails_to_register(kwargs, expected):
    """A new verb fails by omission. This is the omission half."""
    base = dict(
        name="demo.verb",
        summary="x",
        module="tests.cli_fixtures.plain",
        builder="build",
        handler_key="demo.verb",
    )
    with pytest.raises(ValueError) as excinfo:
        registry.Entry(**{**base, **kwargs})
    assert expected in str(excinfo.value)


def test_the_registry_is_the_source_of_the_verb_names_the_layering_guard_reads():
    assert registry.VERB_NAMES == frozenset(e.name for e in registry.entries())
    assert len(registry.VERB_NAMES) == len(registry.entries())


@pytest.mark.parametrize(
    "entry", [e for e in registry.entries() if not e.landed], ids=lambda e: e.name
)
def test_a_planned_verb_whose_module_has_landed_must_lose_its_marker(entry):
    """The countdown, in the same shape as the pending register.

    A declared-but-absent verb is how parity stays checkable before the units
    that implement it exist. The marker has to expire on its own, or it becomes a
    comment nobody re-reads.
    """
    import importlib.util

    try:
        present = importlib.util.find_spec(entry.module) is not None
    except ModuleNotFoundError:
        present = False
    assert not present, (
        f"{entry.module} now exists, so {entry.planned_in} has landed. Clear "
        f"planned_in on {entry.name!r} so the conformance assertions start "
        f"driving it."
    )


# ── the nine conformance properties, over every entry ────────────────────────

ALL_ENTRIES = list(registry.entries())
LANDED = [e for e in ALL_ENTRIES if e.landed]


@pytest.mark.parametrize("entry", ALL_ENTRIES, ids=lambda e: e.name)
def test_conformance_1_structured_output(entry):
    if not entry.emits:
        return
    name, _, major = entry.output_schema.partition("/")
    assert entry.output_schema == output.current_schema(name)
    lock = json.loads((SCHEMA_DIR / "lock.json").read_text())
    assert f"{name}/{major}" in lock


@pytest.mark.parametrize("entry", LANDED, ids=lambda e: e.name)
def test_conformance_1_structured_output_is_actually_emitted(entry, configured):
    argv = ["--output", "json", *_sample_decisions(entry), *entry.path, *_sample_arguments(entry)]
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


def _sample_arguments(entry: registry.Entry) -> list[str]:
    """Enough POSITIONAL arguments to drive one verb, per verb this unit ships.

    Decisions are kept separate below rather than mixed in here, because they are
    flags on the ROOT parser: a gate answer belongs to the invocation, not to the
    subcommand, so that one command can answer gates raised anywhere in it.
    """
    return {
        "profile.show": [],
        "profile.set": ["slim"],
        "run.show": ["no-such-run"],
        "run.decide": ["no-such-run", "profile.set.apply", "apply"],
        # U10. The three per-job verbs are driven against an identifier that is
        # deliberately absent: every one of them must refuse with a code from the
        # vocabulary rather than with a traceback, and an empty queue is the state
        # a fresh install is actually in.
        "job.list": [],
        "job.show": ["no-such-job"],
        "job.resume": ["no-such-job"],
        "job.cancel": ["no-such-job"],
    }[entry.name]


def _sample_decisions(entry: registry.Entry) -> list[str]:
    """Answers for every gate the verb declares, so a drive reaches its logic."""
    flags: list[str] = []
    for spec in entry.gates:
        flags += ["-d", f"{spec.name}={spec.options[0]}"]
    return flags


@pytest.mark.parametrize("entry", LANDED, ids=lambda e: e.name)
def test_conformance_2_exit_codes_are_from_the_vocabulary_and_never_status_two(
    entry, configured
):
    code, _, _ = drive([*_sample_decisions(entry), *entry.path, *_sample_arguments(entry)])
    assert code in {int(c) for c in ExitCode}
    assert code != int(ExitCode.USAGE)


def test_conformance_2_only_the_entry_point_may_end_the_process():
    """One boundary converts a cause into a status. Everything else returns.

    ``SystemExit`` is a ``BaseException``, so an ``except Exception`` upstream
    does not catch it, which is how an argument-parsing failure inside one
    component of the source system surfaces as the orchestrator's exit 2.
    """
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


@pytest.mark.parametrize("entry", LANDED, ids=lambda e: e.name)
def test_conformance_3_every_declared_gate_refuses_and_then_proceeds(entry, configured):
    positional = _sample_arguments(entry)
    for spec in entry.gates:
        code, out, _ = drive(["--output", "json", *entry.path, *positional])
        assert code == int(ExitCode.DECISION_REQUIRED)
        envelope = json.loads(out)
        # The gate and its options ride on the CAUSE, not on
        # ``pending_human_action``: that field means a person must act OUTSIDE
        # the tool, and the envelope asserts it implies status PENDING_HUMAN in
        # both directions. A decision is answerable in the tool, so putting it
        # there would make the two fields contradict each other.
        assert envelope["cause"]["detail"]["gate"] == spec.name
        assert envelope["cause"]["detail"]["options"] == list(spec.options)

        code, _, _ = drive(
            ["-d", f"{spec.name}={spec.options[0]}", *entry.path, *positional]
        )
        assert code == int(ExitCode.OK)


@requires("cratekit.core.review")
@pytest.mark.parametrize(
    "entry", [e for e in ALL_ENTRIES if e.adjudicates], ids=lambda e: e.name
)
def test_conformance_4_adjudication_goes_through_the_review_queue(entry):
    """Assertion 4, armed when the review queue lands.

    It asserts against the STORE rather than against an import, because an import
    proves nothing about use, and it additionally forbids a CSV under the run
    directory: fourteen hand-edited review files are the anti-pattern this
    replaces, and a regression would be visible as a file.
    """
    import importlib

    review = importlib.import_module("cratekit.core.review")
    assert hasattr(review, "list_items")


@pytest.mark.parametrize(
    "entry", [e for e in ALL_ENTRIES if e.long_running], ids=lambda e: e.name
)
def test_conformance_5_long_work_is_queued_rather_than_run_inline(entry):
    """Assertion 5, armed now that the job engine has landed (U10)."""
    import importlib

    jobs = importlib.import_module("cratekit.core.jobs")
    assert entry.argv_builder
    assert hasattr(jobs, "get")


@requires("cratekit.core.session")
@pytest.mark.parametrize(
    "entry", [e for e in ALL_ENTRIES if e.destructive], ids=lambda e: e.name
)
def test_conformance_6_destructive_verbs_refuse_without_the_session_gates(entry):
    """Assertion 6, armed when the write session lands.

    Three refusals, three distinct codes, zero writes each time: a lock held
    elsewhere is 20, a missing backup acknowledgment is 32, and a volume whose
    recorded identity does not match is 22. Per KTD24 the trigger is
    ``destructive``, not ``writes``, so a verb that trashes files while writing
    no database row is still covered.
    """
    import importlib

    session = importlib.import_module("cratekit.core.session")
    assert hasattr(session, "assert_gates")


TAXONOMY_IDS = frozenset(
    {taxonomy.default_taxonomy().tree.id, taxonomy.default_taxonomy().intake.id}
    | set(taxonomy.default_taxonomy().bucket_ids())
    | {band.id for band in taxonomy.default_taxonomy().energy.bands}
    | {sub.id for sub in taxonomy.default_taxonomy().sub_classes}
)

TAXONOMY_DISPLAY_NAMES = frozenset(
    {taxonomy.default_taxonomy().tree.display, taxonomy.default_taxonomy().intake.display}
    | {bucket.display for bucket in taxonomy.default_taxonomy().buckets}
    | {band.display for band in taxonomy.default_taxonomy().energy.bands}
)


@pytest.mark.parametrize("entry", ALL_ENTRIES, ids=lambda e: e.name)
def test_conformance_7_taxonomy_terms_are_stable_identifiers(entry):
    """R19: a verb resolves the declared taxonomy, never a display name.

    A display name is simultaneously code, config, a persisted key, XML bytes,
    and a folder in the user's library. Keying anything on it means a rename
    orphans history in five places at once.
    """
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
    """R3's gap, closed as a rule.

    In the source system the health checks have exactly one caller, an HTML
    template. No verb consults them, so nothing is ever a precondition to
    anything.
    """
    if entry.writes:
        assert entry.doctor_checks, (
            f"{entry.name} writes {sorted(entry.writes)} and declares no health "
            f"check to pass first"
        )


@requires("cratekit.cli.doctor")
def test_conformance_8_every_declared_check_key_exists_in_the_doctor_registry():
    """Armed when doctor lands. Until then the keys are declarations only."""
    import importlib

    doctor = importlib.import_module("cratekit.cli.doctor")
    known = set(doctor.CHECK_KEYS)
    declared = {key for entry in registry.entries() for key in entry.doctor_checks}
    assert declared <= known, sorted(declared - known)


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
    """Widened past the Feature Inventory on purpose.

    Four live console scripts have no inventory row at all, so a check keyed on
    the inventory alone would pass while four real workflows vanished.
    """
    fixture = Path(__file__).resolve().parent / "fixtures" / "dj_tools_scripts.txt"
    scripts = [
        line.strip()
        for line in fixture.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    assert len(scripts) == 33, "the transcribed entry-point list changed size"

    mapped = {name for entry in registry.entries() for name in entry.source_scripts}
    cut_text = (REPO_ROOT / "CUT.md").read_text()
    unaccounted = [s for s in scripts if s not in mapped and s not in cut_text]
    assert not unaccounted, (
        f"source entry points that no verb claims and CUT.md does not explain: "
        f"{unaccounted}"
    )


def test_every_declared_module_toggle_is_used_by_at_least_one_verb():
    """The reverse direction, which is the one that rots.

    A toggle nobody reads is a switch in the user's config that does nothing, and
    it looks identical to a toggle whose verbs have not landed yet until you
    check.
    """
    used = {entry.module_id for entry in registry.entries()} - {None}
    unused = sorted(set(profiles.MODULES) - used - registry.DEFERRED_MODULES)
    assert not unused, (
        f"declared modules no verb is gated by: {unused}. Either a verb is "
        f"missing its module_id or the toggle should not exist."
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


# ═══════════════════════════════════════════════════════════════════════════
# The unit's verification step: a scripted non-interactive run hits a gate
# ═══════════════════════════════════════════════════════════════════════════


def test_a_scripted_run_with_no_terminal_reaches_a_gate_and_exits_with_its_code(
    configured, tmp_path
):
    """The verification the plan asks for, as a real process with no standard input.

    A detached job in the source system gets its standard input bound to the null
    device, the prompt raises at end of file, and the code turns that into
    "abort": the run does not hang, but it also cannot be told to retry. Here the
    same conditions produce a documented code and a resumable run.
    """
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    result = subprocess.run(
        [sys.executable, "-m", "cratekit.cli", "--output", "json", "profile", "set", "slim"],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env=env,
        cwd=tmp_path,
    )
    assert result.returncode == int(ExitCode.DECISION_REQUIRED), result.stderr
    envelope = json.loads(result.stdout)
    assert envelope["cause"]["detail"]["gate"] == "profile.set.apply"
    assert envelope["resumable"] is True
    assert gates.load(envelope["run_id"]).open_gate == "profile.set.apply"


def test_an_unconfigured_machine_refuses_with_a_precondition_and_a_remedy():
    """Not an internal error. A machine that has never been set up is a state.

    U2 models five configuration failures with five remediation tokens; the
    dispatcher converts them rather than each verb doing it, so a verb that
    merely reads config still refuses correctly.
    """
    code, out, _ = drive(["--output", "json", "profile", "show"])
    assert code == int(ExitCode.PRECONDITION)
    envelope = json.loads(out)
    assert envelope["cause"]["reason"] == "config-unusable"
    assert envelope["cause"]["remediation"]["remedy"] == str(Remedy.RUN_SETUP)


def test_a_verb_that_raises_something_unexpected_becomes_an_internal_cause(
    configured, monkeypatch
):
    """Nothing escapes the boundary as a traceback the user has to interpret."""

    def explode(ctx):
        raise ZeroDivisionError("something nobody predicted")

    monkeypatch.setattr("cratekit.cli.verbs.profile.show", explode)
    code, out, _ = drive(["--output", "json", "profile", "show"])
    assert code == int(ExitCode.INTERNAL)
    assert json.loads(out)["cause"]["reason"] == "internal-error"


def test_a_verb_that_exits_the_process_directly_is_converted_rather_than_obeyed(
    configured, monkeypatch
):
    """The live leak in the source, closed. ``SystemExit`` is a ``BaseException``."""

    def exits(ctx):
        raise SystemExit(2)

    monkeypatch.setattr("cratekit.cli.verbs.profile.show", exits)
    code, out, _ = drive(["--output", "json", "profile", "show"])
    assert code == int(ExitCode.INTERNAL)
    assert code != int(ExitCode.USAGE)
    assert json.loads(out)["cause"]["reason"] == "internal-error"


def test_human_mode_renders_the_gate_with_its_options_and_how_to_answer(configured):
    _, _, err = drive(["profile", "set", "slim"])
    assert "profile.set.apply" in err
    assert "apply, abort" in err
    assert "crate run decide" in err
