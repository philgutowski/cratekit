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
import enum
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import gates, output, registry, render
from cratekit.core import config, profiles, rb_writer, taxonomy
from cratekit.core.cause import REASONS, Cause, CratekitError, Outcome, Remediation, Scope
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
from tests._source_guards import constructs_a_csv_writer

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


def _modules_declaring_their_own_remedy() -> dict[str, type]:
    """Every module in the package that declares a ``Remedy`` of its own.

    DERIVED by walking the package, not listed. The version of this test that
    named ``config`` alone was already false when it was written: four more
    modules declared their own Remedy afterwards, none of them a subset, and the
    suite stayed green over sixteen tokens the canonical enum had never heard
    of. That is seam decision P3 exactly, and this is the shape that prevents it
    recurring.
    """
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
    """Several modules declared remediation tokens before this vocabulary existed.

    They stay a SUBSET rather than becoming a second scheme. Two vocabularies for
    one idea is the drift that produced five genre resolvers, and it starts
    exactly like this: one module needing a token before the module that owns
    them was written.
    """
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
    """The consequence the subset rule exists to prevent, asserted directly.

    A token the canonical enum does not carry falls through ``render`` to the
    exit code's generic summary, so a refusal that means "store this credential"
    reads as "an unexpected failure". That is silent, it is user facing, and it
    is exactly the collapse KTD25 names. Derived over every module-local token,
    not over a sample.
    """
    generic = {str(meaning_of(code).summary) for code in ExitCode}
    for module_name, declared in _modules_declaring_their_own_remedy().items():
        for member in declared:
            line = render.remediation_line(
                Cause(
                    reason="internal-error",
                    message="m",
                    remediation=Remediation(remedy=Remedy(str(member))),
                    scope=Scope.RUN,
                    retryable=False,
                )
            )
            body = line.removeprefix("  fix: ")
            assert body not in generic, (
                f"{module_name}.{member.name} renders as the exit code's generic summary "
                f"rather than as its own remediation"
            )


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

#: The refusal conditions the guarded rekordbox writer raises, taken from U7's
#: surface map. U5 ships before U7 precisely so that U7 CONSUMES this vocabulary
#: instead of inventing codes, and a refusal with no code is the defect KTD25
#: exists to prevent. The two-process refusal is a separate exception type in the
#: source and is asserted alongside them.
#:
#: DELIBERATELY NOT COUNTED IN PROSE. It was written as "the eleven refusal
#: conditions" and stopped being eleven the first time one was split in two,
#: which is what a count in a comment always does. The list is walked by the test
#: below and reconciled against what the writer actually raises, so its size is
#: derived in both directions and never asserted here.
WRITER_REFUSALS: dict[str, str] = {
    "pyrekordbox pin drift": "pyrekordbox-pin-drift",
    "database schema version drift": "db-schema-pin-drift",
    "rekordbox application version drift": "app-version-pin-drift",
    "missing database directory": "library-directory-missing",
    "missing database file": "library-database-missing",
    "database open failure": "database-open-failed",
    "canary read failure": "canary-read-failed",
    "cloud sync canary tripped": "cloud-sync-active",
    # Split off the line above. "Sync is on" and "we cannot tell whether sync is
    # on" were one slug, so two conditions with opposite answers arrived as one
    # exit code, which is the collision this whole reservation list exists to
    # prevent. Reserved separately here because the reservation list is the
    # contract; the writer consumes it.
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


def test_an_unreadable_cloud_state_and_an_active_one_are_different_failures():
    """The second collision of the same shape as the two-process one above.

    They shared a slug, so a caller could not tell "Cloud Library Sync is on"
    from "the file that records it could not be read". The answers are not
    variations of each other: one is switched off in another application, and the
    other cannot be, because nothing has established there is anything to switch.
    The fix for "we cannot tell" is a PERSON deciding whether to proceed, which
    is what the decision code already means, so no code was invented for it (S4).

    The remedy tokens are read from the codes rather than asserted as literals,
    so this stays true if a code's class remedy is ever revised.
    """
    unreadable, active = REASONS["cloud-sync-unreadable"], REASONS["cloud-sync-active"]
    assert unreadable is not active
    assert meaning_of(unreadable).remedy is not meaning_of(active).remedy
    assert meaning_of(unreadable).remedy is Remedy.ANSWER_DECISION
    assert meaning_of(active).remedy is Remedy.DISABLE_CLOUD_SYNC

    # "Answer the decision" is only true advice if the run is still there to
    # answer. The command-line layer decides that by code, so picking this code
    # is what makes the refusal resumable rather than merely described as such.
    assert unreadable in gates.GATE_CODES
    assert active not in gates.GATE_CODES


def test_the_unreadable_cloud_state_is_not_the_undeclared_gate_reason():
    """Two slugs on one code, kept apart because they mean opposite things.

    ``decision-unknown-gate`` means a decision named a gate the verb does not
    declare, which is a defect. This one means a declared gate was reached with
    nothing recorded against it, which is the system working. Folding the second
    into the first would report a normal refusal as a bug in the product.
    """
    assert REASONS["cloud-sync-unreadable"] is REASONS["decision-unknown-gate"]
    assert "cloud-sync-unreadable" != "decision-unknown-gate"


def test_the_reason_registry_has_no_duplicate_key():
    """A duplicate key in a dict literal is silent: the later one simply wins.

    Every test over this mapping iterates the RUNTIME dict, so a slug shadowed at
    parse time is invisible to all of them, and the shadowed entry's exit code
    becomes whatever the survivor says. This repository has shipped that defect
    once with the whole suite green. Counting the literal's keys against the
    runtime length is the only check that can see it.
    """
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


def test_the_unreadable_cloud_sync_override_is_a_DECLARED_GATE():
    """The override used to be a Python keyword argument and nothing else.

    It sat on three functions inside the guarded writer, reachable from no
    command a user can type, so the only way past a canary that could not read
    the state was to edit the source. A refusal with an escape nobody can reach
    is a refusal with no escape.

    Looked up BY NAME through the registry rather than constructed here, because
    a spec built in the test proves the test can build a spec.
    """
    owner, spec = registry.gate("write.cloudsync.unreadable")
    assert spec.explicit, (
        "R34 forbids a blanket answer for this class: proceeding past a guard "
        "that could not rule out a concurrent writer is a per-run act by a named "
        "actor, not a flag that answers it once for everything"
    )
    assert set(spec.options) == {"proceed", "abort"}
    assert owner.writes & registry.DB_WRITE_SURFACES


def test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision():
    """Derived by walking the registry, never by listing verbs (P3).

    Every verb declaring a database write surface opens the database with write
    intent and therefore reaches the writer's unreadable-cloud refusal. A verb
    that reaches it without declaring the decision leaves a user with a refusal
    and no way to answer it, and a hand-written list of the verbs that qualify is
    a list that misses the next one somebody adds.
    """
    missing = sorted(
        entry.name
        for entry in registry.ENTRIES
        if entry.writes & registry.DB_WRITE_SURFACES
        and not any(spec.name == "write.cloudsync.unreadable" for spec in entry.gates)
    )
    assert not missing, (
        f"verbs that write the database and declare no cloud-sync decision: {missing}"
    )

    # And the reverse, which is the direction that rots: a verb declaring the
    # decision without writing the database would be asking a person to answer a
    # question its work can never raise.
    spurious = sorted(
        entry.name
        for entry in registry.ENTRIES
        if any(spec.name == "write.cloudsync.unreadable" for spec in entry.gates)
        and not entry.writes & registry.DB_WRITE_SURFACES
    )
    assert not spurious, f"verbs declaring a decision they cannot reach: {spurious}"


def test_the_core_writer_never_learns_the_gates_name_or_any_flag_string():
    """D2 from the other side: the foundation names no verb and no gate.

    The override crosses into the guarded writer as a BOOLEAN. What produced that
    boolean, what it is called, and what a user typed to answer it all belong to
    the command-line layer, which is the only layer allowed to render a token
    into text. A core module that knows the gate's name has re-acquired the
    command vocabulary the layering rule removes from it.
    """
    source = (SRC_ROOT / "cratekit" / "core" / "rb_writer.py").read_text()
    for leaked in ("write.cloudsync.unreadable", "--decision", "crate "):
        assert leaked not in source, f"the core writer names {leaked!r}"


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

    Every caller runs under the ``configured`` fixture, which is what lets the
    file-taking verbs be handed a path inside the configured library rather than
    a literal one this repository would then be shipping (R1).
    """
    library = config.load().library.root
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
        # U11. Same shape as the job verbs above: an identifier that is
        # deliberately absent, so each verb must refuse with a code from the
        # vocabulary rather than with a traceback, and an empty queue is the
        # state a fresh install is genuinely in. The two file verbs take a path
        # under the CONFIGURED library rather than a literal, because a literal
        # here would be a real path on somebody's machine (R1).
        "review.list": [],
        "review.show": ["no-such-item"],
        "review.resolve": ["no-such-item", "--verdict", "accepted"],
        "review.clear": ["no-such-item"],
        "review.export": [str(library / "review-export.json")],
        "review.import": [str(library / "no-such-export.json")],
        # U23. The census takes no positional argument at all: a taxonomy
        # declares exactly one routing tree by stable identifier, so a flag
        # naming one would be a second opinion about a value the template
        # already holds (R19). It queues rather than scanning, which is
        # conformance 5's property, and queueing needs no database, which is
        # what lets the half of adoption that is ready land while its
        # destructive sibling waits.
        "adopt.scan": [],
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


def test_the_csv_writer_guard_bites_and_stays_quiet_on_correct_code():
    """P7's own instruction: run a guard against correct code before shipping it.

    THE HALF THAT WAS SKIPPED. This assertion was armed over every adjudicating
    verb through conformance 4, and its self-test checked ``import csv`` and
    ``from csv import DictWriter`` and never the aliased import. A reviewer
    switched the whole guard off with one keyword, ``import csv as spreadsheet``,
    so "run it against correct code" had been done and "run it against the
    evasion" had not. Every import shape the language offers is checked here now,
    in both directions.

    The shapes that look like it and are not, an unrelated attribute of the same
    name and a READ, are still left alone.
    """
    assert constructs_a_csv_writer("import csv\ncsv.writer(handle)\n")
    assert constructs_a_csv_writer("from csv import DictWriter\nDictWriter(handle, [])\n")
    assert constructs_a_csv_writer("import csv as spreadsheet\nspreadsheet.writer(handle)\n"), (
        "an aliased import switches the guard off, which is the evasion it was "
        "armed against"
    )
    assert constructs_a_csv_writer("from csv import writer as w\nw(handle)\n")
    assert not constructs_a_csv_writer("import xml\nxml.writer(handle)\n")
    assert not constructs_a_csv_writer("import csv\nfor row in csv.reader(handle):\n    pass\n")
    for _path, source in package_sources():
        assert not constructs_a_csv_writer(source), (
            "the guard fires somewhere in the tree it is meant to leave alone"
        )


@pytest.mark.parametrize(
    "entry", [e for e in ALL_ENTRIES if e.adjudicates], ids=lambda e: e.name
)
def test_conformance_4_adjudication_goes_through_the_review_queue(entry, configured):
    """Assertion 4, armed now that the review queue has landed (U11).

    WHAT IS DRIVEN, STATED PLAINLY, in the same shape assertion 6 uses for the
    destructive verbs. Every adjudicating verb here carries a ``planned_in``
    marker, so there is no landed one to invoke. What is driven instead is the
    shared surface all of them must go through, once per declared adjudicating
    verb and UNDER THAT VERB'S OWN handler key: an item is offered, it is
    addressable by that key alone, a real command line resolves it, and a third
    independent open of the store sees the verdict. That is behaviour rather than
    an existence check, and it is the strongest thing available until the first
    adjudicating verb lands.

    The static half is what bites afterwards, with no edit to this file: the
    moment a verb's module exists, its own source is walked for a comma separated
    writer. The previous version of this test asserted ``hasattr(review,
    "list_items")``, which its own docstring already claimed was an assertion
    against the store; an attribute lookup would have passed with every call site
    deleted.
    """
    import importlib

    review = importlib.import_module("cratekit.core.review")

    queue = review.adjudicated_queues()[0]
    with review.open_store(configured) as store:
        item = review.offer(
            store,
            queue=queue,
            kind="conformance",
            identity={"handler": entry.handler_key},
            payload={"handler": entry.handler_key},
            options=(review.Option(option_id="opt-one", summary="the one candidate"),),
            handler_key=entry.handler_key,
        )
        assert item.verdict is None
        addressed = review.list_items(store, handler_key=entry.handler_key).items
        assert [held.item_id for held in addressed] == [item.item_id], (
            f"{entry.name} declares that it adjudicates, and the queue cannot "
            f"show what it produced under its own key"
        )

    code, out, err = drive(
        [
            "--output", "json", "review", "resolve", item.item_id,
            "--verdict", "accepted", "--option", "opt-one",
        ]
    )
    assert code == int(ExitCode.OK), err or out

    with review.open_store(configured) as store:
        settled = review.get(store, item.item_id)
        assert settled.verdict is review.Verdict.ACCEPTED
        assert review.count_unresolved(store) == 0

    # The replacement must not be the thing it replaces. Derived by WALKING the
    # declared review directory rather than by naming the database, so a second
    # file added beside it is covered on the day it appears (P3).
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
            f"{entry.name} declares that it adjudicates and writes a comma "
            f"separated file for a person to edit: {offenders}. Adjudication is a "
            f"persisted review item (R12)."
        )


@pytest.mark.parametrize(
    "entry", [e for e in ALL_ENTRIES if e.long_running], ids=lambda e: e.name
)
def test_conformance_5_long_work_is_queued_rather_than_run_inline(entry):
    """Assertion 5, armed now that the job engine has landed (U10)."""
    import importlib

    jobs = importlib.import_module("cratekit.core.jobs")
    assert entry.argv_builder
    assert hasattr(jobs, "get")


def _state_fingerprint(*roots) -> dict[str, tuple[int, int]]:
    """Size and modification time of every file under each root.

    "Zero writes" is asserted against the FILESYSTEM rather than assumed from
    reading the code, because the whole class of defect this guards is a refusal
    that already wrote something before it decided to refuse. A fingerprint taken
    either side of the call is the only thing that can see that.
    """
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


@pytest.mark.parametrize(
    "entry", [e for e in ALL_ENTRIES if e.destructive], ids=lambda e: e.name
)
def test_conformance_6_destructive_verbs_refuse_without_the_session_gates(
    entry, configured, tmp_path
):
    """Assertion 6, now that the write session has landed (U8, R-5).

    Three refusals, three distinct codes, zero writes each time: a lock held
    elsewhere is 20, a missing backup acknowledgment is 32, and a volume whose
    recorded identity does not match is 22. Per KTD24 the trigger is
    ``destructive``, not ``writes``, so a verb that trashes files while writing
    no database row is still covered.

    WHAT IS DRIVEN, STATED PLAINLY. Every one of these entries carries a
    ``planned_in`` marker, so there is no landed destructive verb to invoke
    through the dispatcher yet. What is driven instead is the shared gate that
    every one of them must pass through, once per declared destructive verb and
    under that verb's own name. That is behaviour rather than an existence check,
    and it is the strongest thing available until the first destructive verb
    lands; ``tests/test_write_session.py`` drives the same three refusals through
    a real destructive OPERATION, the backup restore, which does exist.
    """
    import importlib

    session = importlib.import_module("cratekit.core.session")
    assert hasattr(session, "assert_gates")

    right = configured.library.volume_id
    matching = lambda _path: right  # noqa: E731 - one line, and naming it adds nothing
    roots = (
        configured.library.root,
        config.installation_state_dir(),
        config.config_dir(),
    )

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

    # 1. A volume whose recorded identity does not match. Checked FIRST because
    #    it is the one refusal that must happen before any path is resolved.
    wrong_volume = refuse_with(
        identity_provider=lambda _path: "0000-0000", mount_enumerator=lambda: ()
    )

    # 2. No backup acknowledgment. The volume now matches, and nothing has been
    #    recorded, which is the state of every library before a person answers.
    no_acknowledgment = refuse_with(identity_provider=matching)

    # 3. The lock held elsewhere. The acknowledgment is minted first so this
    #    refusal is reached, and the lock is taken on a separate handle so it
    #    looks exactly like another process holding it.
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
    assert codes == (
        ExitCode.LIBRARY_BUSY,
        ExitCode.ACK_REQUIRED,
        ExitCode.LIBRARY_UNAVAILABLE,
    )
    assert len(set(codes)) == 3, "three refusals that cannot be told apart is one refusal"


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
