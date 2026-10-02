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

import argparse
import ast
import contextlib
import enum
import io
import json
import os
import subprocess
import sys
import uuid
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

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
from cratekit.modules import extras
from tests import _import_probe, outbound_fakes
from tests import doctor_machines as machines
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
def configured(library, monkeypatch):
    """A machine that has been set up, so a verb reaches its own logic.

    The disposable database is the R-13 substitute: a supplied
    ``CRATEKIT_TEST_DB`` snapshot wins, otherwise a synthetic file is built.
    The battery runs either way. Volume identity and the two-process refusal
    are satisfied here because ``delete.review`` asserts both before it can
    return OK, and a fixture that claims to be set up must be a machine the
    destructive session will actually admit.
    """
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

    cfg = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(library),
                "volume_id": "F1E2-D3C4",
                "db_path": str(db_path),
            },
            "paths": {"download_staging": str(library.parent / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(cfg)
    config.reset_cache()
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    # A PERSON IS SITTING HERE, asserted rather than inherited, and U49 is what
    # made it necessary. ``session.ack`` is the first landed verb that reaches
    # ``core.session.record_acknowledgment``, which refuses when no controlling
    # terminal opens, and conformance 3 drives every gated verb THROUGH its gate
    # to OK. Whether ``os.ctermid()`` opens under pytest depends on how the suite
    # was launched, so leaving it unpatched makes this file pass or fail on a
    # property of the machine rather than of the product. The patch lives here
    # and not in ``tests/conftest.py`` on purpose: here it is visible as a
    # property of the conformance drive, there it would silently cover every
    # future terminal-gated verb. The REFUSING direction is driven in
    # tests/test_session_cli.py, where it is the thing under test rather than a
    # precondition.
    from cratekit.core import session as core_session

    monkeypatch.setattr(core_session, "has_controlling_terminal", lambda: True)
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
    """U97, closing R-411, over BOTH tokens that send a person to get a session.

    ``AUTHENTICATE_PROVIDER`` was the single command ``crate login``, which
    records a value somebody already holds and refuses without one, so a first
    run person who followed the product's own remedy reached a second refusal.
    ``REAUTHENTICATE_PROVIDER`` said "log in again", the same dead end reached
    from the other direction and the likelier one, since every session minted
    before 2026-09-01 is a device flow session the adapter now refuses.

    Asserted against literal text rather than against ``render.remedy_text``,
    which is the token's own renderer: comparing a renderer to itself is X
    equals X and would pass over the exact wording this closes. Each act is
    pinned separately, because the erase is the one a reader drops and the one
    R4's promise depends on.
    """
    line = render.remediation_line(
        Cause(
            reason="credential-missing",
            message="no streaming provider session is usable",
            remediation=Remediation(remedy=remedy),
            scope=Scope.RUN,
        )
    )
    assert line != forbidden
    body = line.removeprefix("  fix: ")
    assert "crate login cannot mint" in body
    assert "vendored downloader's own login command" in body
    assert "crate login provider-session --from-file" in body
    assert "erase the plaintext file" in body
    assert "docs/adapters.md" in body


def test_the_document_the_provider_session_remedy_names_ships_and_carries_the_command():
    """A remedy that points at a document is only as good as the document.

    A renamed file, or a section that stops carrying the recording command,
    leaves a first run person at a dead end with nothing red. The pointer is
    worded as the PROJECT'S document and not as a local path on purpose:
    ``docs/`` is in no wheel, measured by building one, so an installed person
    told to open a path would find nothing there.
    """
    adapters = REPO_ROOT / "docs" / "adapters.md"
    assert adapters.is_file(), "the remedy points at a document this repository does not ship"
    assert "crate login provider-session --from-file" in adapters.read_text(encoding="utf-8")


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


def test_the_profile_gate_shows_the_delta_the_digest_was_taken_over(configured):
    """The gate carried the question and not one module (R-693). Its ``shown``
    now holds the declined run's items, each module turning on or off, the
    digest they were taken over, the profile and the totals, in the json
    envelope and on the screen a person answers from."""
    code, out, _ = drive(["--output", "json", "profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_REQUIRED)
    shown = json.loads(out)["cause"]["detail"]["shown"]
    code, out, _ = drive(
        ["--output", "json", "-d", "profile.set.apply=abort", "profile", "set", "slim"]
    )
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

    The resolver is driven directly, because the rule is a property of the
    RESOLVER rather than of any verb that happens to declare an explicit gate.
    An earlier version of this docstring justified that differently, saying the
    gate belonged to a verb that had not landed and that asserting the rule here
    made it true before the first explicit gate arrived with U8. Both clauses
    are now false and one always was: ``write.cloudsync.unreadable`` is explicit
    and sits on a landed entry, and U49 landed ``session.ack`` itself. The test
    is unchanged because its reason never depended on either.
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
    assert cause.detail["install"] == extras.install_command("analysis")


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


def test_a_planned_verb_whose_module_has_landed_must_lose_its_marker():
    """The countdown, in the same shape as the pending register.

    A declared-but-absent verb is how parity stays checkable before the units
    that implement it exist. The marker has to expire on its own, or it becomes a
    comment nobody re-reads. Walked rather than parametrized so an empty set,
    which is the state after the last planned verb lands, is still a valid
    derived population (P3) rather than a collection error.
    """
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
                f"{entry.module} now exists, so {entry.planned_in} has landed. "
                f"Clear planned_in on {entry.name!r} so the conformance "
                f"assertions start driving it."
            )
    assert not leftover, leftover


#: The planned verbs whose module ``tests/_pending.PENDING`` also owes, written
#: out for the reason ``EXPECTED_PENDING`` is: a change to either register must be
#: made in a second place a reviewer reads. Empty since U27 landed
#: ``cratekit.session.restore_cli``, the last one.
EXPECTED_COMPARED: frozenset[str] = frozenset()


def test_a_planned_verb_and_the_pending_register_name_the_same_unit():
    """Two registers hold "who lands this module" and neither read the other.

    ``registry.Entry.planned_in`` and ``tests/_pending.PENDING`` both answer that
    question, for the same modules, and they drifted: the two ``restore.*`` verbs
    carried ``planned_in="U32"`` while the register had already moved
    ``cratekit.session.restore_cli`` to U27 precisely because U32 could not land
    it. Nothing compared them. ``board.py`` reads the register and never reads
    ``planned_in``, and the countdown above only asks whether the module EXISTS,
    never who owes it, so the marker stayed pointing at a unit that was closing.
    An obligation attributed to a closed unit is owned by nobody, which is the
    exact failure the register entry's own text says it was written to prevent.

    Asked over the intersection rather than over either register whole: a planned
    verb whose module nothing in the register mentions is a separate question, and
    the register legitimately holds keys that are not verb modules at all.

    THE ANTI-VACUITY GUARD MEASURES THE SET THAT IS ACTUALLY COMPARED, and the
    first version of it did not. It rebuilt the intersection in a second
    comprehension and asked its question of that, which is a re-derivation of the
    predicate rather than a measurement of the comparison. Found by mutation:
    neutering the filter on the comparison alone killed NOTHING, because the guard
    went on building a populated list of its own and stayed green over a
    comparison that now compared nothing. One list is built once and both
    statements read it.
    """
    from tests import _pending  # noqa: PLC0415

    compared = [
        entry
        for entry in registry.entries()
        if not entry.landed and entry.module in _pending.PENDING
    ]
    # First, WHAT is compared, written out rather than derived, because the whole
    # point of this guard is that a change to either register has to be made in a
    # second place a reviewer reads. It is EMPTY, and that is a true state rather
    # than a hole: U27 landed ``cratekit.session.restore_cli``, which was the last
    # planned verb module the register owed, so there is nothing left to compare.
    #
    # IT IS STILL FALSIFIABLE IN BOTH DIRECTIONS, which is what an anti-vacuity
    # guard is for. A unit that declares a verb and registers its module here
    # fires this assertion on the day it lands, and whoever does that restores the
    # comparison by naming it. Emptying the register side never reaches this file
    # at all: ``_pending.requires`` raises at import for a key that is gone, which
    # is a collection error rather than a green run.
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
    """KTD26: the engine validates a queued job's handler BEFORE spawning.

    Validating by import would pull the feature module into the supervisor's own
    process, which is exactly what the lazy-import scheme exists to prevent.

    MEASURED IN A CLEAN INTERPRETER, and this is the third shape of this test.
    It named ``acquire.download`` as its single subject until U42, chosen because
    its module did not exist, so ``not in sys.modules`` held for a reason that had
    nothing to do with the property; the day the module landed, an earlier drive
    in the same session imported it and the assertion failed on a lookup that had
    imported nothing.

    It was then restated in-process as a DIFFERENCE across every landed verb, and
    a mutation table proved that version empty. Inserting a real
    ``importlib.import_module`` into ``by_handler_key`` killed ZERO tests, subset
    and promoted full suite alike, because by the time the suite reaches this
    file the feature modules are already in ``sys.modules`` and importing a
    cached module adds nothing to measure. A difference is only a measurement
    where the thing could have differed.

    So the property is measured where it is actually claimed: a fresh interpreter
    that has imported the registry and NOTHING else, the state the supervisor is
    genuinely in when it validates a queued job's handler. One subprocess covers
    every landed verb, so no hand-picked subject remains to expire.
    """
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
    sample = {
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
        # U36. Driven with no argument at all, which is the whole point: this
        # verb is read only and answers on a library where nothing has cut over,
        # which is every library until the first cutover and which is also the
        # only shape this fixture can build. It opens the rekordbox database
        # only when a tree is actually database-native, so it exits OK here with
        # no database on the machine.
        "converge": [],
        # U24. A plain listing with no arguments, which is the state a fresh
        # install is genuinely in: no version has been deleted, so no version is
        # suppressed, and the verb must still emit a well-formed review set and
        # exit OK rather than treating an empty store as a failure. Revoking is
        # driven from the deletion suite, where a real tombstone exists to lift.
        "tombstone.list": [],
        # U24. No positional argument: the confirm gate is the only input, and
        # the first run on this fixture baselines an empty removal set rather
        # than presenting history. The drive here is the refuse-at-the-gate
        # half; the two-act OK path is conformance 3.
        "delete.review": [],
        # U16. Same convention as the two file verbs above and for the same
        # reason: a path under the CONFIGURED library rather than a literal, and
        # one that is deliberately absent, so the verb must refuse with a code
        # from the vocabulary rather than with a traceback. The happy path over a
        # real list and a real library is driven in tests/test_match_states.py,
        # which is where the fixtures for it live.
        "match.run": [str(library / "no-such-list.txt")],
        # U42. Download takes a list under the CONFIGURED library, for the R1
        # reason every file verb here gives, and it is deliberately absent. It
        # still exits OK, and the difference from match.run beside it is the
        # point: this verb QUEUES, and queueing freezes the path without reading
        # it, so an absent list is refused by the worker that reads it rather
        # than by the shell that files it. Audit takes no positional at all: an
        # empty music directory is the state this fixture is genuinely in, and
        # the verb must still emit a well-formed review set and exit OK rather
        # than treating nothing to report as a failure.
        "acquire.download": [str(library / "no-such-list.txt")],
        "acquire.audit": [],
        # U80. A list under the CONFIGURED library that is absent, so the verb
        # refuses from the vocabulary before a library walk or a search, and no
        # contract run can ever reach the shipped searcher's subprocess.
        "acquire.fallback": [str(library / "no-such-list.txt")],
        # U81. The same absent list, refused from the vocabulary before any
        # library walk, queue or download.
        "acquire.fallback-fetch": [str(library / "no-such-list.txt")],
        # U23. The census takes no positional argument at all: a taxonomy
        # declares exactly one routing tree by stable identifier, so a flag
        # naming one would be a second opinion about a value the template
        # already holds (R19). It queues rather than scanning, which is
        # conformance 5's property, and queueing needs no database, which is
        # what lets the half of adoption that is ready land while its
        # destructive sibling waits.
        # U49. Neither session verb takes a positional argument, and neither may
        # take a flag: R34 forbids a caller naming the actor or asserting the
        # answer, so the whole input is the recorded gate decision. Both are
        # driven on a fixture whose library has no backup fact file and no lock,
        # which is the state of every install before its first backup, and both
        # must still ask their question rather than treating an empty world as a
        # reason not to. WHICH MODE THIS MEASURES: the drives below reach these
        # verbs through the derived populations, and the explicit gates mean
        # ``_sample_decisions``'s inline answer is refused rather than accepted,
        # so conformance 1 and 2 see the REFUSAL and conformance 3 is the only
        # property here that reaches the acting half. The two-act OK path and
        # every refusal shape live in tests/test_session_cli.py.
        "session.ack": [],
        "session.release": [],
        "adopt.scan": [],
        # U27. The apply takes no positional argument either, and for the same
        # R19 reason: the tree comes off the declared taxonomy. It asks its
        # explicit approval gate against the digest of the plan it rebuilt, which
        # on this fixture is the EMPTY plan, because no unit in this build lands
        # the collection reader that would give the census rows. An empty plan is
        # still a plan a person can abort, so the gate fires, and the two-act OK
        # path is conformance 3. Queueing needs no database and opens no
        # destructive session, which is what lets the verb exit OK on a machine
        # that has never acknowledged a backup.
        "adopt.apply": [],
        # R-758. No argument, as its sibling takes none. It reads the backup
        # acknowledgment BEFORE it asks its gate (R-733), so it is the one verb
        # here that needs the acknowledgment this fixture records to reach its
        # own logic at all. The tree on this fixture has not cut over, so the
        # plan is the empty one over a tree nobody read, which still asks.
        "adopt.move": [],
        # U61. The composer takes the favourites source's export, the same
        # document ``sync.favorites`` is driven with below, so its confirm gate
        # is reachable and conformance 3 can drive it. The registry on this
        # fixture is empty, so the labels source refuses for itself and the
        # pass still reaches OK once favourites is confirmed. The composition
        # itself is driven in tests/test_sync_all.py.
        "sync.all": [
            "--export",
            str(outbound_fakes.write_export(library / "outbound")),
        ],
        # U20. Inbox, unplaced and pending take no positional argument: an empty
        # intake folder and an empty ledger are the state a fresh install is
        # genuinely in, and each verb must still emit a well-formed plan and
        # exit OK. Resort and rebuild are long-running, so they queue and
        # report a job. Rebuild carries a typed actor because an empty one is
        # the product answering for the user. No tree flag, because a library that
        # has never flipped a tree has nothing native and the verb still
        # queues.
        "route.inbox": [],
        "route.unplaced": [],
        "route.resort": [],
        "route.pending": [],
        "rebuild": ["--actor", "a-person"],
        # U27. The wizard and the two reports take no positional argument at all:
        # every answer the wizard needs is already recorded by the ``configured``
        # fixture, so a drive here resolves each one from the file and reaches no
        # prompt, which is the property that makes the ONE interactive verb
        # scriptable rather than a hole in the non-interactive contract.
        "setup": [],
        "doctor": [],
        "status": [],
        # Named without a source on purpose. The value is never a command-line
        # argument, so the drive exercises the refusal that names both ways of
        # supplying one rather than a success that would have had to put a
        # credential in the process listing.
        "login": ["provider-session"],
        # U37. Identify is driven against a missing recording so it must refuse
        # with a vocabulary code before any paid call (no recognition keys on
        # a fresh install). Set and playlist queue a job, so the source string
        # is frozen and never fetched. File and tag take a path under the
        # configured library. Repair and name.apply take no positional: an
        # empty library is the state a fresh install is genuinely in.
        "intake.set": ["https://example.invalid/mix"],
        "intake.identify": [str(library / "no-such-set.mp3")],
        "intake.playlist": ["https://example.invalid/playlist"],
        # U69. The job verbs' convention: an identifier deliberately absent,
        # so the verb must refuse from the vocabulary rather than trace back.
        "intake.missing": ["--job", "no-such-job"],
        # R-770. A FILE THAT IS THERE, since the verb declares a gate now and
        # conformance 3 holds a gated verb to ending OK. On the conformance
        # fixture the intake tree is on the xml bridge and no export is named,
        # so the verb shows its plan, writes nothing and asks nothing. LAZY,
        # because it puts a file under the library.
        "intake.file": lambda: [str(_a_file_in_the_library())],
        # U72. A folder under the CONFIGURED library that holds no audio, so
        # the verb refuses from the vocabulary before its gate is reached.
        "intake.land": [str(library / "Music"), "--export", str(library / "no-such.xml")],
        # R-501. An export that is not there, which the verb refuses from the
        # vocabulary whether or not any run is waiting on one.
        "intake.imported": ["--export", str(library / "no-such.xml")],
        # U82. A real export document under the CONFIGURED library, named as an
        # intake file of a pass this fixture never ran. No playlist job spells
        # that name, so the plan is empty, the explicit gate is still asked,
        # and the verb ends NO_OP without listing the account or asking for a
        # credential this fixture does not have. The
        # marking path is driven in tests/test_sync_mark.py.
        #
        # LAZY SINCE R-235, the first sample here that another sample's drive
        # can see. Every value in this mapping is built on every call, whichever
        # verb is being driven, and this one leaves an intake file under the
        # library, which is exactly what the cutover precheck refuses over.
        "sync.mark": lambda: [
            "--xml",
            str(
                outbound_fakes.write_export(library / "landed").rename(
                    library / "landed" / "no-such-pass_synced_inboxed.xml"
                )
            ),
        ],
        # R-838. A pass the mark record holds nothing for, so the plan is
        # empty, the explicit gate is still asked, and the verb ends NO_OP
        # without listing the account or asking for a credential. The
        # unmarking path is driven in tests/test_sync_unmark.py.
        "sync.unmark": ["--pass", "no-such-pass_synced"],
        "tag.folder": [str(library / "Music")],
        # U40. Same convention as tag.folder: a folder under the CONFIGURED
        # library. It is empty here, so the selection is empty and the confirm
        # gate is asked against the digest of a plan with nothing in it, which is
        # still a plan a person can abort. This verb opens no database on any
        # path, which is why it declares no database write surface and no cloud
        # sync decision: the entry claimed db_metadata until R-246 narrowed it to
        # files, after the row relink that has no caller in src.
        "tag.retag": [str(library / "Music")],
        # U43. The anchor is a path under the CONFIGURED library, for the R1
        # reason every file verb above gives, and it is deliberately absent, so
        # the verb must refuse with a code from the vocabulary rather than with a
        # traceback. An absent anchor and an empty index are the same state here
        # and the same refusal: this fixture's library holds no audio at all, so
        # nothing could be indexed even if the file were there. The OK path over
        # a library that does hold the anchor is driven in
        # tests/test_setbuilder_cli.py, where the audio fixtures live.
        "setbuild": [str(library / "Music" / "no-such-anchor.aiff")],
        # U44. A recording under the CONFIGURED library, for the R1 reason every
        # file verb above gives, and deliberately absent. Unlike setbuild beside
        # it, this one exits OK rather than refusing, and the difference is the
        # point: the verb QUEUES, and queueing freezes the path without reading
        # it. A stat in the handler would refuse here on a fixture that has no
        # ffmpeg either, on a machine where the work would have run fine once
        # claimed. The cost, that a mistyped path is reported queued rather than
        # refused, is filed as a residual. The refusal over an absent recording
        # is driven in tests/test_master_cli.py, on the work path where a person
        # meets it.
        "master": [str(library / "Music" / "no-such-recording.wav")],
        # U45. No positional argument at all: the whole plan comes off the
        # configured destinations, so a flag naming one would be a second opinion
        # about a value the wizard already recorded. It exits OK on this fixture,
        # which has no rclone binary and no backup remote, and that is the point
        # rather than an accident: the verb QUEUES, and queueing resolves no
        # binary, reads no process table and stats no volume. A plan built in this
        # handler would refuse here on a machine where the work would have run
        # fine once claimed, and the entry's two doctor checks are what tell a
        # person about rclone and the volume before they type the verb. The
        # refusals over a missing rclone and over a failed transfer are driven in
        # tests/test_backup_cli.py, on the work path where a person meets them.
        "backup.run": [],
        "name.apply": [],
        # U102. Driven with the flag, because that is the path the confirm gate
        # is on and conformance 3 holds the verb to reaching every gate it
        # declares. The review queue is empty here, so the gate is asked against
        # the digest of a plan with nothing in it, which is still a plan a person
        # can abort, and the collection is never read. Without the flag the verb
        # scans and offers and asks nothing, which tests/intake/test_repair.py
        # and tests/intake/test_repair_apply.py drive.
        "repair.paths": ["--apply"],
        # U25. Folder verbs take a path under the configured library. Calibrate
        # and validate accept no folder, which is the state with no labelled
        # set yet. Run and restamp queue, so they must still emit a job_state
        # envelope over an empty folder rather than a traceback.
        "analyze.run": [str(library / "Music")],
        "analyze.calibrate": [],
        "analyze.validate": [],
        "analyze.restamp": [str(library / "Music")],
        "analyze.vocals": [str(library / "Music")],
        "metadata.mytags-vocals": [],
        # U26. Registry list is the empty-install state. Import of a name that
        # is not registered must refuse with a vocabulary code. Harvest of an
        # unreachable playlist must refuse rather than invent labels.
        #
        # U52 CHANGED WHAT THE SWEEP DOES ON THIS FIXTURE, and the comment is
        # updated rather than the assertion. It used to queue an increment here.
        # Its job items are now the registered favourite labels, and this fixture
        # registers none, so it refuses ``label-registry-empty`` rather than
        # filing a job with nothing to claim, which ``jobs.drive`` would later
        # transition straight to SUCCEEDED over work nothing did. That is still a
        # code from the vocabulary and still not USAGE, which is all this
        # conformance asks. The queueing path over a registry that holds labels,
        # and the refusal over one that does not, are both driven in
        # tests/test_label_workers.py, where a registry can be populated.
        "label.registry": [],
        "sync.labels": [],
        "label.import": ["no-such-label"],
        "label.harvest": ["https://example.invalid/playlist"],
        # U75. No argument is required: over a configured machine with an
        # empty review queue the verb reports nothing accepted and stops
        # before the catalogue is resolved.
        "label.approved": [],
        # R-798. No argument lists what the genre gate holds.
        "label.held": [],
        # R-815. No argument judges every pending label release, and over an
        # empty review queue that is nothing: the verb queues no job and says
        # which zero it is, before any provider is resolved.
        "label.judge": [],
        # R-840. No argument repairs every open label release whose artist
        # reads an address, and over an empty review queue that is none: the
        # verb says so before any provider is resolved.
        "label.artists": [],
        # U27. The four report verbs each take a collection export, and each is
        # handed a path under the CONFIGURED library that is deliberately absent,
        # for the same reason the file verbs above are: a literal here would be a
        # real path on somebody's machine (R1), and an absent one makes every one
        # of them refuse with a code from the vocabulary rather than with a
        # traceback. There is no configured export location to default to, so an
        # absent file is the state every fresh install is genuinely in. The happy
        # path over a real export is driven in tests/modules/test_reports.py,
        # which is where the export fixtures live.
        "audit.coverage": [str(library / "no-such-export.xml")],
        "audit.duplicates": [str(library / "no-such-export.xml")],
        "report.library": [str(library / "no-such-export.xml")],
        "report.intake-aging": [str(library / "no-such-export.xml")],
        # U27. Both restore verbs are driven with no positional argument at all,
        # and the omission is the state a fresh install is genuinely in rather
        # than a convenience. The listing answers over an empty session log. The
        # run means "the newest session whose capture is spendable", of which
        # there are none here, so it asks its explicit confirmation gate against
        # the digest of an offer with no halves in it and then reports that there
        # was nothing to restore. That path opens NO destructive session, which is
        # what lets the verb exit OK on a machine that has never acknowledged a
        # backup: the session is opened only by the code that touches the volume.
        "restore.list": [],
        "restore.run": [],
        # U96. The recovery names a target and accepts the replacement, and in
        # this sandbox it REFUSES, which is the behaviour under test rather than
        # a shortfall of the drive: the configured library is present, and the
        # engine refuses a bare-metal recovery whenever the recorded volume can
        # be read. It declares no gate, so nothing requires it to exit OK here,
        # and the machine on which it does is one whose library is gone.
        "restore.bare-metal": [
            "--target",
            str(library / "replacement"),
            "--accept-replacement",
        ],
        # U33. Export takes the playlist identifier and queues after its
        # own confirm gate. Favourites sync takes no positional: the
        # confirm is the remote half, separate from any local colour write.
        #
        # U51 GAVE BOTH A REAL EXPORT, and unlike the report verbs above it is
        # NOT an absent path. The difference is what each verb has to reach.
        # A report refuses on an unreadable export and that refusal is the whole
        # behaviour under test here. These two decide their JOB ITEMS from the
        # document, so an absent one refuses before the confirm gate is reached,
        # and assertion 3 exists to prove the gate IS reached. The document is
        # written under the configured library, so no literal path from anybody's
        # machine enters the repository (R1).
        "export.playlist": [
            "crate-export",
            "--export",
            str(outbound_fakes.write_export(library / "outbound")),
        ],
        "sync.favorites": [
            "--export",
            str(outbound_fakes.write_export(library / "outbound")),
        ],
        # U28. Driven with an explicit target under the configured library rather
        # than with no argument at all, and the difference matters: the default
        # target is the agent skills directory under the REAL home directory of
        # whoever runs the suite, so a bare drive would write twelve directories
        # into a person's actual configuration while claiming to be a test. The
        # flag exists so the destination is always somebody's choice.
        "skills.install": ["--into", str(library / "agent-skills")],
        # R-235. The cutover is driven over a library the precheck PASSES, with
        # exactly one root for the routing tree, because conformance 3 holds the
        # verb to reaching its approval and to ending OK once it is given, and
        # an unready library refuses before the question. The revert is driven
        # over a tree already recorded native, since a tree on the bridge has
        # nothing to revert and is answered without the question. Both are LAZY:
        # each changes the library's own state, and built eagerly they would
        # change it under every other verb's drive.
        "tree.cutover": lambda: _ready_to_cut_over(),
        "tree.revert": lambda: _already_cut_over(),
        # R-745. A NEW NAME PER DRIVE, because the verb never replaces a file
        # and a conformance that drives it twice would otherwise be asserting
        # about the refusal the second time round.
        "export.collection": lambda: [
            str(library / "exports" / f"collection-{uuid.uuid4().hex}.xml")
        ],
        # R-797. No argument: the threshold is the author's number and the
        # database is the configured one.
        "report.genres": [],
        # The residual on stale row genres. No argument: it reads the whole
        # collection of the configured database.
        "tag.rows": [],
        # R-799. No argument: it reads every tagging record this installation
        # committed, which on the fixture's machine is none.
        "tag.remap": [],
    }[entry.name]
    return sample() if callable(sample) else sample


def _routing_tree() -> tuple[str, str]:
    """The routing tree this fixture's library declares: identifier, display name."""
    from cratekit.core import active_taxonomy

    declared = active_taxonomy.load(config.load())
    return declared.tree.id, declared.tree.display


def _a_file_in_the_library() -> Path:
    """One file with an audio suffix under the configured library, made on demand.

    Empty, which is enough: ``intake file`` with no export on a bridge tree
    reads its tags for the plan and an empty container carries none.
    """
    path = Path(config.load().library.root) / "Music" / "conformance-single.flac"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    return path


def _ready_to_cut_over() -> list[str]:
    from tests import cutover_fixtures

    tree_id, display = _routing_tree()
    export, _root = cutover_fixtures.ready(config.load(), display)
    return [tree_id, "--export", str(export)]


def _already_cut_over() -> list[str]:
    from datetime import date

    from cratekit.core import tree_registry

    tree_id, _display = _routing_tree()
    cfg = config.load()
    if not tree_registry.read(cfg).is_database_native(tree_id):
        tree_registry.record_cutover(
            cfg,
            tree_id,
            root_id="a-root",
            on=date(2026, 9, 27),
            source=tree_registry.DerivationSource.TAXONOMY,
        )
    return [tree_id]


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


#: Gates that CANNOT be reached in a test environment, each with the reason.
#:
#: This map exists because the honest alternative is worse in both directions. A
#: rule requiring every declared gate to fire would fail every correct verb
#: declaring the cloud-sync decision, and a rule requiring none would let a verb
#: ship with a gate its handler no longer reaches. So the exemption is NAMED,
#: per gate, with what makes it unreachable, and everything not in here must
#: fire.
#:
#: An entry here is a claim that can expire. If a listed gate is ever reached,
#: the assertion below fails and says to delete the entry, because a gate that
#: fires is a gate the suite can hold a verb to.
UNREACHABLE_GATES: Mapping[str, str] = MappingProxyType(
    {
        "intake.file.native": (
            "asked only on a library whose intake tree is recorded database "
            "native, for the reason intake.land.native gives below: the "
            "conformance fixture's intake tree is on the xml bridge, where the "
            "same verb shows its plan and asks nothing, and the medium is the "
            "tree's mode, not an argument. The gate, its explicit two act answer "
            "and its refusals are driven in tests/test_intake_writers_native.py "
            "on a library whose intake tree has cut over."
        ),
        "intake.land.native": (
            "asked only on a library whose intake tree is recorded database "
            "native, and the conformance fixture's intake tree is on the xml "
            "bridge, where the same verb asks intake.land.confirm instead. One "
            "drive reaches one medium, and the medium is the tree's mode, not an "
            "argument, so no argument list reaches both. The native gate, its "
            "explicit two act answer and its refusals are driven in "
            "tests/test_intake_land_native.py on a library whose intake tree has "
            "cut over."
        ),
        "write.cloudsync.unreadable": (
            "raised by the guarded writer only when rekordbox's Cloud Library "
            "Sync state cannot be READ, which is a property of the machine "
            "rather than of the verb. A test environment has no rekordbox "
            "installation to have an unreadable sync state, so no drive can "
            "provoke it and requiring it would refuse every correct verb that "
            "declares it. Closes with the disposable database fixture R-13 "
            "names, which is the first environment able to produce the state."
        ),
    }
)


def _assert_gate_reach(entry: registry.Entry, reached: list[str]) -> None:
    """Every gate the entry declares fired, except the ones named unreachable.

    The half that a returned list nobody compared cannot provide. A declaration
    is a promise to the person reading the registry that this verb asks this
    question, and the only thing that can hold a handler to it is a drive that
    counts what actually fired.
    """
    declared = {spec.name for spec in entry.gates}
    exempt = declared & set(UNREACHABLE_GATES)
    expected = declared - exempt

    silent = sorted(expected - set(reached))
    assert not silent, (
        f"{entry.name} declares {silent} and its handler never reached them. A "
        f"declared gate that cannot fire is a decision the registry promises and "
        f"the verb does not ask, and for a destructive verb that is the "
        f"concurrent-writer question going unasked with the suite green. Either "
        f"reach it, drop the declaration, or name it in UNREACHABLE_GATES with "
        f"the reason no drive can provoke it."
    )

    surprising = sorted(set(reached) & exempt)
    assert not surprising, (
        f"{entry.name} reached {surprising}, which UNREACHABLE_GATES says no "
        f"drive can provoke. The exemption is stale: delete the entry so every "
        f"verb declaring that gate is held to reaching it."
    )


#: Verbs that read the backup acknowledgment BEFORE they ask their gate (R-733),
#: so a machine that never acknowledged one refuses them ahead of the gate
#: conformance 3 holds them to reaching. NAMED RATHER THAN GIVEN TO EVERY VERB
#: THROUGH THE FIXTURE: the other gated verbs reach their gates on a machine
#: with no acknowledgment, and that is a property worth keeping under test.
#: That each of these refuses without one is driven in its own suite, which
#: the guard below holds this table to.
ACKNOWLEDGED_BEFORE_THE_GATE = {
    "adopt.move": (
        "tests/test_adopt_move.py::"
        "test_with_no_acknowledgment_the_verb_refuses_before_the_gate"
    ),
    "tag.rows": (
        "tests/test_tag_rows.py::"
        "test_with_no_acknowledgment_the_verb_refuses_before_the_gate"
    ),
}


def _acknowledge_where_the_verb_reads_it_first(entry: registry.Entry, cfg) -> None:
    if entry.name not in ACKNOWLEDGED_BEFORE_THE_GATE:
        return
    from cratekit.core import session

    session.record_acknowledgment(cfg, terminal=lambda: True)


def test_every_verb_acknowledged_for_conformance_is_refused_without_one_elsewhere():
    """The table is an exemption from one machine state, so each entry names
    the test that drives the verb in that state, and the test has to exist."""
    root = Path(__file__).resolve().parent.parent
    for name, node_id in ACKNOWLEDGED_BEFORE_THE_GATE.items():
        assert registry.entry(name).landed, name
        path, _, function = node_id.partition("::")
        tree = ast.parse((root / path).read_text(encoding="utf-8"))
        defined = {
            node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
        }
        assert function in defined, f"{name} names {node_id}, which does not exist"


def _conformance_3(entry: registry.Entry, positional: list[str]) -> list[str]:
    """Drive one gated verb to OK the way R34 says it is reached, and say how.

    Returns the gates it actually refused at, in the order it refused at them,
    having first asserted that the set of them is exactly what the entry declares
    minus :data:`UNREACHABLE_GATES`.

    THAT EQUALITY IS THE POINT, and an earlier version of this function dropped
    it. Returning the reached list and leaving the caller to ignore it made a
    verb that declares two gates and reaches neither pass, and made a verb whose
    handler stopped reaching a declared gate pass. A destructive database verb
    could have shipped with its concurrent-writer decision unreachable and the
    suite would have been green, because no other assertion anywhere holds a
    handler to the gates its entry declares.

    The narrowing that replaced it was real but far too wide: it covered every
    gate when the justification covered one. A gate that cannot be provoked is
    named in the map above with the reason, and every other declared gate must
    fire.
    """
    declared = {spec.name: spec for spec in entry.gates}
    answered: list[str] = []
    reached: list[str] = []
    run_id: str | None = None

    # One drive per gate, plus the one that succeeds. A verb that refuses more
    # often than it has gates is refusing at something it did not declare, and
    # falling out of the loop rather than spinning is what makes that visible.
    for _ in range(len(declared) + 1):
        resume = ["--run", run_id] if run_id is not None else []
        argv = ["--output", "json", *answered, *resume, *entry.path, *positional]
        code, out, err = drive(argv)
        if code == int(ExitCode.OK):
            _assert_gate_reach(entry, reached)
            return reached
        assert code == int(ExitCode.DECISION_REQUIRED), err or out

        envelope = json.loads(out)
        # The gate and its options ride on the CAUSE, not on
        # ``pending_human_action``: that field means a person must act OUTSIDE
        # the tool, and the envelope asserts it implies status PENDING_HUMAN in
        # both directions. A decision is answerable in the tool, so putting it
        # there would make the two fields contradict each other.
        detail = envelope["cause"]["detail"]
        assert detail["gate"] in declared, (
            f"{entry.name} refused at {detail['gate']!r}, which it does not "
            f"declare; a gate outside the registry is invisible to every "
            f"conformance assertion"
        )
        spec = declared[detail["gate"]]
        assert detail["options"] == list(spec.options)
        assert detail["explicit"] is spec.explicit
        assert envelope["resumable"] is True
        reached.append(spec.name)

        if not spec.explicit:
            # ONE ACT. An ordinary gate is answerable in the invocation that
            # discovered it, and the flags accumulate rather than replacing each
            # other so a second gate further in is reached with the first still
            # answered.
            answered += ["-d", f"{spec.name}={spec.options[0]}"]
            continue

        # TWO ACTS (R34). The inline answer is refused AGAIN, because an
        # explicit gate is satisfiable only by a deliberate, separate act
        # recorded with its actor. Asserting OK here instead, which is what this
        # function did for four waves, asserts that an explicit gate must NOT be
        # honoured, and every verb declaring one was unlandable by construction.
        run_id = envelope["run_id"]
        inline = ["-d", f"{spec.name}={spec.options[0]}"]
        code, _, _ = drive([*answered, *inline, "--run", run_id, *entry.path, *positional])
        assert code == int(ExitCode.DECISION_REQUIRED), (
            f"{spec.name} is explicit, and an inline answer satisfied it. R34's "
            f"whole content is that this class of decision cannot be typed onto "
            f"the command that was already running"
        )
        assert spec.name not in gates.load(run_id).decisions, (
            "the refused inline answer was recorded anyway, so the second act "
            "would find the gate already answered by the first"
        )

        code, _, err = drive(
            ["run", "decide", run_id, spec.name, spec.options[0], "--actor", "a-person"]
        )
        assert code == int(ExitCode.OK), err
        assert gates.load(run_id).decisions[spec.name].actor == "a-person", (
            "an explicit decision names who asserted it, or the record cannot "
            "tell a person's answer from the process asking itself"
        )

    raise AssertionError(
        f"{entry.name} still refuses after every gate it declares was answered"
    )


@pytest.mark.parametrize("entry", LANDED, ids=lambda e: e.name)
def test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds(entry, configured):
    """Assertion 3, rewritten: a gate refuses, and OK comes only after R34's acts.

    WHAT WAS WRONG. The previous version drove every gate the same way: refuse,
    then hand the answer back on ``-d`` in a fresh invocation, then assert OK.
    For an ordinary gate that is the contract. For an EXPLICIT one it is the
    opposite of the contract. ``Gates.require`` refuses an inline answer whenever
    nothing is recorded against the run, and ``cli.run`` mints a new run whenever
    ``--run`` is absent, so an explicitly gated verb refuses the second drive too,
    every time, by design. Asserting OK there asserted that R34 must be violated.

    Nothing caught it because no landed entry declares an explicit gate. Fifteen
    declare one and all fifteen are planned, so the branch was never driven, and
    four units in one wave independently concluded their verb "cannot land" and
    parked the obligation somewhere else. The test below drives the branch against
    a synthetic entry so it is proved before the first real one arrives.
    """
    if not entry.gates:
        return
    _acknowledge_where_the_verb_reads_it_first(entry, configured)
    _conformance_3(entry, _sample_arguments(entry))


def _swap_in(monkeypatch, promoted: registry.Entry) -> None:
    """Put a modified entry in front of the dispatcher, everywhere it is looked up.

    ``_BY_NAME`` is patched alongside ``ENTRIES`` because ``run decide`` resolves
    the owning entry BY NAME to find the gate it is answering, so a swap that
    reached only the parser would leave the second act looking at the unmodified
    spec and quietly prove nothing.
    """
    monkeypatch.setattr(
        registry,
        "ENTRIES",
        tuple(promoted if e.name == promoted.name else e for e in registry.ENTRIES),
    )
    monkeypatch.setattr(
        registry, "_BY_NAME", {**dict(registry._BY_NAME), promoted.name: promoted}
    )


def test_conformance_3_admits_an_explicitly_gated_verb(configured, monkeypatch):
    """The branch above, driven, before any landed verb declares an explicit gate.

    Fifteen planned entries declare one and none has landed, so assertion 3's
    explicit half would otherwise ship untested and be discovered by the unit
    that lands the first one. That is precisely how the defect it replaces
    survived four waves.

    The synthetic entry is the REAL ``profile.set`` with its one gate promoted to
    explicit, rather than a verb invented here. A verb invented for the test
    proves the test can invent a verb; promoting a real one means the dispatcher,
    the run record, ``run decide`` and the resume path are all the shipped ones,
    and the single difference is the flag under examination.
    """
    base = registry.entry("profile.set")
    promoted = replace(base, gates=(replace(base.gates[0], explicit=True),))
    _swap_in(monkeypatch, promoted)

    assert _conformance_3(promoted, ["slim"]) == ["profile.set.apply"]
    config.reset_cache()
    assert config.load().profile.name == "slim", (
        "the verb reported OK without doing its work, so the two acts bought a "
        "status rather than a profile change"
    )


#: A second gate to hang on a one-gate verb, so the two-gate shape is driven
#: rather than assumed. Explicit, because that is the shape four registry entries
#: carry: their own confirmation plus the shared cloud-sync decision.
_SECOND_GATE = registry.GateSpec(
    name="profile.set.second",
    options=("go", "abort"),
    prompt="A second decision on the same verb?",
    explicit=True,
)


def _require_every_gate(ctx):
    """A handler that reaches all of its entry's gates, in declaration order."""
    for spec in ctx.entry.gates:
        ctx.gate.require(spec)
    return ctx.envelope(data={"checks": [], "summary": {}})


@pytest.mark.parametrize(
    "explicit_first", [False, True], ids=["plain-then-explicit", "explicit-then-explicit"]
)
def test_conformance_3_admits_a_verb_carrying_two_gates(
    explicit_first, configured, monkeypatch
):
    """The OTHER half of what assertion 3 could not express, driven both ways.

    The previous version drove once per DECLARED gate and answered only that one
    gate, on a fresh run every time. A verb with two gates therefore refused on
    whichever gate the current drive had not answered, so it exited
    DECISION_REQUIRED for both iterations and could never pass, with no explicit
    flag involved at all. Four registry entries carry two gates, ``restore.run``,
    ``name.apply``, ``route.inbox`` and ``adopt.apply``, and every one of them was
    unlandable for this reason on top of the R34 one.

    ``_conformance_3`` answers gates CUMULATIVELY instead, which is what makes one
    loop cover both shapes: an ordinary gate accumulates a flag and the next drive
    reaches past it, an explicit one takes its two acts and the run carries the
    answer forward under ``--run``. Both orderings are driven because they are not
    the same path. Plain-then-explicit has to carry an inline answer across the
    switch to a resumed run, and explicit-then-explicit has to record two separate
    decisions against one run without the first being re-asked.

    The handler is the one piece that cannot be borrowed, because no landed verb
    declares two gates and a verb that declares them without reaching them proves
    nothing. Everything else on the path is shipped: the parser, the dispatcher,
    the run record, ``run decide``, and the resume.
    """
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
    destructive verbs. What is driven is the shared surface every adjudicating
    verb goes through, once per declared adjudicating verb and UNDER THAT VERB'S
    OWN handler key: an item is offered, it is addressable by that key alone, a
    real command line resolves it, and a third independent open of the store sees
    the verdict. That is behaviour rather than an existence check.

    IT IS NOT A DRIVE OF THE VERB. This was written when no adjudicating verb had
    landed. They have all landed since, and none is invoked here: the item is
    offered by this test, so a verb that decides without offering anything to
    the queue passes. The residual finding "Conformance 4 and 6 drive the shared
    surface and not the landed verbs" records that gap.

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
    """Assertion 6, now that the write session has landed (U8, and the residual
    finding "Four conformance assertions are written in full and gated on units
    that have not landed").

    Three refusals, three distinct codes, zero writes each time: a lock held
    elsewhere is 20, a missing backup acknowledgment is 32, and a volume whose
    recorded identity does not match is 22. Per KTD24 the trigger is
    ``destructive``, not ``writes``, so a verb that trashes files while writing
    no database row is still covered.

    WHAT IS DRIVEN, STATED PLAINLY. What is driven is the shared gate every
    destructive verb must pass through, once per declared destructive verb and
    under that verb's own name. That is behaviour rather than an existence check.

    IT IS NOT A DRIVE OF THE VERB. This was written when every one of these
    entries carried a ``planned_in`` marker. Most have landed since, and none is
    invoked here through the dispatcher, so a verb that writes before it enters
    its session passes. ``tests/test_write_session.py`` drives the same three
    refusals through the backup restore, and ``tests/test_adopt_apply_cli.py``
    through ``apply_outstanding``, both below the dispatcher. The residual
    finding "Conformance 4 and 6 drive the shared surface and not the landed
    verbs" records that gap.
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


def test_conformance_8_every_declared_check_key_exists_in_the_doctor_registry(configured):
    """ARMED by U27, and the static half is all this one is.

    A verb may not declare a precondition nobody wrote, or it satisfies assertion
    8 above with a non-empty tuple while depending on nothing at all. That is a
    table lookup and it is honest about being one; the behaviour is asserted by
    the test below, which is a different property and was not one until the
    review said so.
    """
    import importlib

    doctor = importlib.import_module("cratekit.cli.doctor")
    known = set(doctor.CHECK_KEYS)
    declared = {key for entry in registry.entries() for key in entry.doctor_checks}
    assert declared <= known, sorted(declared - known)


def test_conformance_8_every_declared_precondition_can_pass_and_can_refuse(configured):
    """The behaviour half, written so a doctor that does no work cannot pass it.

    WHAT THIS REPLACED WAS A TAUTOLOGY. ``CHECK_KEYS`` is derived from ``CHECKS``,
    ``run`` is one finding per check, and every check returns its own key, so
    "every declared key comes back with an answer" is identically the existence
    check on the line above it, computed the expensive way. A stub doctor
    emitting one empty ``Finding`` per key satisfied both halves while observing
    nothing at all, and the same property was already asserted in
    ``tests/test_doctor.py``.

    So the assertion is now a COMPARISON BETWEEN TWO RUNS over the same
    configuration, on two machines that differ only in their seams:

    * on a machine where nothing is broken, no declared precondition refuses, or
      the check fires on a correct install and gets worked around (P7);
    * on a machine where each of those preconditions IS broken, every one of them
      refuses. That is this module's own sentence, "a check that cannot fail is
      not a check", applied to the exact set of keys some verb has declared it
      depends on.

    Neither half can be satisfied by a constant. A check that always answers OK
    fails the second, one that always refuses fails the first, and one that
    answers with an empty finding fails the shape assertion under both.

    TWO LIMITS, RECORDED RATHER THAN HIDDEN, because both are the kind of thing a
    later reader would otherwise discover as a surprise:

    * It covers the keys some verb DECLARES, which is 9 of the doctor's 23. The
      other 14 are asserted one at a time in ``tests/test_doctor.py``, and
      nothing here forces a new check to be reachable or refusable until a verb
      depends on it.
    * ``machines.hostile()`` is ``machines.green()`` with seams overridden, so it
      breaks the machine and not the configuration. A future precondition whose
      correct answer on that machine is INFO rather than FAIL, a check about
      something no seam describes, will fail this test. THE FIX IS TO EXTEND
      ``hostile()`` so that precondition is genuinely broken there, not to relax
      the assertion: "this check cannot refuse" is the finding, and softening the
      guard is how it stops being one.
    """
    import importlib

    doctor = importlib.import_module("cratekit.cli.doctor")
    declared = {key for entry in registry.entries() for key in entry.doctor_checks}
    assert declared, "no verb declares a precondition; the walk is broken, not the tree"

    # The shared fixture is a machine that has been SET UP, which is deliberately
    # not the same as one that is healthy: it records no rekordbox pin, because
    # a pin is never adopted on a user's behalf (S2). The healthy run needs one,
    # so it is added here rather than in the fixture, where it would quietly make
    # every other conformance drive assert against a state a fresh install is not
    # in.
    document = dict(configured.to_toml_dict())
    document["rekordbox"] = {
        "pinned_app_version": machines.INSTALLED_APP_VERSION,
        "validated_on": "2026-08-01",
    }
    cfg = config.from_dict(document)

    healthy = {f.key: f for f in doctor.run(cfg, probes=machines.green()).findings}
    broken = {f.key: f for f in doctor.run(cfg, probes=machines.hostile()).findings}

    assert _precondition_problems(declared, healthy, broken) == []


def _precondition_problems(declared, healthy, broken) -> list[str]:
    """Every way two reports fail to show a precondition that did work.

    A function rather than a loop inside the assertion so the guard itself can be
    driven against the evasion it exists to reject, which is the half of a guard
    that keeps getting skipped: running it against correct code proves it does
    not fire, and proves nothing about what it catches.
    """
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
                    f"{key} answered with nothing that says what was observed: "
                    f"{finding.detail!r}"
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
    """The evasion, run against the guard.

    A doctor emitting one empty ``Finding`` per key satisfied the assertion this
    replaced: the keys all came back, the report had the right length, and
    nothing had been observed. Three stubs here, one per way of answering without
    working, and the guard has to reject all three.
    """
    from cratekit.cli.doctor import Finding, Status

    declared = {key for entry in registry.entries() for key in entry.doctor_checks}

    def stub(status: Status, detail: str = "", title: str = "") -> dict:
        return {
            key: Finding(key=key, title=title, status=status, detail=detail)
            for key in declared
        }

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
    # 37 since U105, which transcribed ``master_set.sh``, the mastering
    # verb's predecessor, into the second block (R-193). 36 since 2026-09-18.
    # It was 33, and 33 was wrong: three console scripts
    # in the source system's table were never transcribed, so this count pinned
    # an incomplete list and made the omission look deliberate. The pin still
    # earns its place, because a list that shrinks is the failure it catches.
    assert len(scripts) == 37, "the transcribed entry-point list changed size"

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
    {entry.module_id for entry in registry.landed_entries()}
    - {None}
    - profiles.ALWAYS_AVAILABLE
)


@pytest.fixture(scope="module")
def slim_verb_paths():
    return _verb_paths(cli.build_parser(membership=profiles.resolve("slim")))


def test_every_live_toggle_is_driven_by_the_toggle_test_below():
    """The parametrisation below is derived, so this is what stops it shrinking.

    A toggle that is neither deferred nor waiting on a planned verb must gate a
    landed one, or the round trip below silently stops covering it.
    """
    waiting = {entry.module_id for entry in registry.entries() if not entry.landed}
    live = set(profiles.MODULES) - registry.DEFERRED_MODULES - waiting
    assert live <= set(_TOGGLES_WITH_LANDED_VERBS), sorted(
        live - set(_TOGGLES_WITH_LANDED_VERBS)
    )


@pytest.mark.parametrize("module", _TOGGLES_WITH_LANDED_VERBS)
def test_a_module_toggle_alone_switches_its_landed_verbs_on_and_off(module, slim_verb_paths):
    """R-4's closing condition, driven rather than declared.

    Nine toggles were added by U5 before any verb stood behind them. Each one is
    exercised here through the real resolver and the real parser, in both
    directions an explicit toggle can move: added to slim, and subtracted from
    full. A gated verb that stays reachable with its module off is a Module row
    shipping as core, which is exactly what R5 forbids.

    It sees only verbs that already name a module. A verb declared core by
    mistake carries no ``module_id`` and never enters this set; the Feature
    Inventory parity check above is what holds that direction.
    """
    verbs = [entry.path for entry in registry.landed_entries() if entry.module_id == module]
    added = _verb_paths(cli.build_parser(membership=profiles.resolve("slim", {module: True})))
    removed = _verb_paths(
        cli.build_parser(membership=profiles.resolve("full", {module: False}))
    )
    for path in verbs:
        assert path not in slim_verb_paths, f"{path} is on in the slim profile"
        assert path in added, f"turning {module} on did not reach {path}"
        assert path not in removed, f"turning {module} off left {path} reachable"


def test_a_verb_carrying_a_resume_argv_builder_declares_that_it_queues():
    """THE DIRECTION THAT REMOVES ANOTHER FILE'S COVERAGE, found 2026-08-26.

    ``tests/test_queued_resume_contract.py`` derives its guarded set from
    ``long_running`` AND ``argv_builder``, which is what makes every guard there
    cover a verb nobody thought to list. It also means dropping ``long_running``
    from an entry silently removes that verb from all of them: that suite goes
    green with three fewer tests and nothing says so. A U40 mutation removing
    exactly that flag killed nothing and only shrank the collected count.

    IT LIVES HERE RATHER THAN BESIDE THE GUARDS IT PROTECTS, and the reason is
    NOT the one this docstring first gave. The first version claimed this file's
    parametrisations key on ``landed`` so the collected count would be unmoved and
    the death countable. That was wrong and the third mutation round measured it
    wrong: ``test_conformance_5_long_work_is_queued_rather_than_run_inline`` at
    ``:1913`` parametrises over exactly this flag, so removing it still drops a
    case and the count still moves, from 532 to 531.

    THE HONEST STATEMENT IS THAT NO CLEAN MEASUREMENT EXISTS for a registry flag
    a parametrisation keys on. Wherever the guard lives, removing the flag removes
    parametrised cases somewhere, and ``mutate.py`` will report drift rather than a
    zero, which is correct of it and cannot be designed around. What moving the
    guard here actually bought is smaller and real: the drift went from three
    cases to one, and the row now NAMES this test among its kills instead of
    reporting nothing at all. It belongs here regardless, because it is a registry
    invariant and that is what this file holds.

    ``Entry.__post_init__`` already refuses the other direction, a long-running
    verb with no builder. This is the implication that has no home there, because
    the type cannot argue about intent: an ``argv_builder`` exists for exactly one
    purpose, turning a frozen payload back into a command line for the child the
    job driver spawns, so a verb declaring one and not declaring ``long_running``
    is either mislabelled or carrying a builder nothing will ever call.

    Measured over the registry on 2026-08-26: 21 entries declare ``long_running``
    and every one declares a builder, so the implication holds in the tree today
    and this is what stops it drifting.

    Measured again on 2026-09-10 by U60: 20, because ``delete.review`` stopped
    declaring BOTH halves in one commit. The floor below now sits exactly on the
    count, so the next verb to stop queueing has to move it on purpose.

    Measured again on 2026-09-10 by U61: 19, because ``sync.all`` stopped
    declaring both halves in one commit. It composes other verbs' queueing paths
    and queues nothing under its own key, so it has nothing to resume.
    """
    carriers = [entry for entry in registry.ENTRIES if entry.argv_builder]
    assert len(carriers) >= 19, (
        f"only {len(carriers)} entries declare a resume argv builder, which is "
        f"below the 19 measured when U61 last moved this floor; either the "
        f"registry shrank or this guard has stopped deriving anything"
    )
    mislabelled = sorted(entry.name for entry in carriers if not entry.long_running)
    assert not mislabelled, (
        f"these verbs declare a resume argv builder and do not declare "
        f"long_running: {mislabelled}. Either the builder is dead code, or the "
        f"verb queues and has just dropped out of every derived guard in "
        f"tests/test_queued_resume_contract.py"
    )


#: Long-running entries whose shell legitimately files no job under its own key,
#: with the reason. Not a list of verbs that are allowed to lie: a verb goes here
#: only when queueing is not what it DOES, as opposed to what it has not done yet.
QUEUES_BY_ROLE_NOT_BY_ENQUEUE: Mapping[str, str] = MappingProxyType(
    {
        "job.resume": (
            "the resume verb spawns the child that drives an existing job and "
            "never files one of its own"
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
    """R-149's class, the direction no other guard here can see. U60, 2026-09-10.

    ``long_running`` plus an ``argv_builder`` says a job driver re-invokes this
    verb as a subprocess. Every guard in ``tests/test_queued_resume_contract.py``
    and ``tests/test_handlers.py`` trusts that sentence and derives its population
    from it, so an entry that declares it over a shell doing the work inline puts
    a verb into every one of those populations with nothing behind it: a builder
    nothing calls, and an unbound handler key that tells a person the work is
    queued when it is not. ``delete.review`` sat in that state from U24 until U60.

    PARSED RATHER THAN SEARCHED, for the reason
    ``tests/test_handlers.py::_drive_calls`` gives: prose that names ``enqueue``
    is not a call to it. A call anywhere in the verb's module is the bar, not a
    call on the handler's own path, because several shells enqueue from a helper.
    """
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


def _context_spec(*, explicit: bool) -> registry.GateSpec:
    """One gate to ask, built here because the property is the resolver's."""
    return registry.GateSpec(
        name="context.probe",
        options=("proceed", "abort"),
        prompt="Proceed?",
        explicit=explicit,
    )


def test_a_gate_refusal_carries_what_the_verb_consulted(configured):
    """U49: the question arrives with the facts it was asked over.

    A gate's prompt is fixed at declaration and cannot name a backup age or a
    lock holder, so a verb that has to put one in front of a person carries it
    on the refusal. Driven through the real resolver against a real
    ``GateSpec``, because a hand built ``DecisionRequired`` would prove this
    file can build one.
    """
    state = gates.RunState(run_id="r", verb="probe", created="now")
    resolver = gates.Gates(state=state)
    with pytest.raises(gates.DecisionRequired) as raised:
        resolver.require(
            _context_spec(explicit=False),
            context={"ages": [{"portion": "database", "state": "never-recorded"}]},
        )
    shown = raised.value.cause.detail["shown"]
    assert shown["ages"] == [{"portion": "database", "state": "never-recorded"}]


def test_a_gate_refusal_with_no_context_carries_no_shown_key_at_all(configured):
    """ABSENT AND EMPTY STAY DIFFERENT, and this is the row that holds them apart.

    Every gate in the product predates the context argument and passes nothing.
    A default that materialised an empty ``shown`` would make "this verb shows
    nothing here" indistinguishable from "this verb looked and found nothing",
    which is the collapse ``backup_facts`` refuses one layer down, and it would
    turn an optional carry into a field every refusal now claims to answer.
    """
    state = gates.RunState(run_id="r", verb="probe", created="now")
    with pytest.raises(gates.DecisionRequired) as raised:
        gates.Gates(state=state).require(_context_spec(explicit=False))
    detail = raised.value.cause.detail
    assert "shown" not in detail
    assert set(detail) == {"gate", "options", "prompt", "explicit", "run_id"}


def test_the_explicit_inline_refusal_carries_the_context_too(configured):
    """BOTH RAISE SITES, or what a person sees depends on whether they typed a flag.

    ``require`` refuses twice: once because nothing answered the gate, and once
    because an explicit gate was answered inline, which R34 forbids. That second
    refusal is the one a person hits when they try to shortcut the acknowledgment,
    so it is exactly the refusal that has to name what they were about to assert.
    """
    spec = _context_spec(explicit=True)
    state = gates.RunState(run_id="r", verb="probe", created="now")
    resolver = gates.Gates(state=state, supplied={spec.name: "proceed"})
    with pytest.raises(gates.DecisionRequired) as raised:
        resolver.require(spec, context={"holder": {"host": "elsewhere", "pid": 41}})
    assert raised.value.cause.detail["shown"]["holder"]["host"] == "elsewhere"


def test_human_mode_renders_what_the_verb_showed_and_is_unchanged_without_it(configured):
    """The carried context reaches a PERSON, not only a JSON consumer.

    ``render_gate`` reads a fixed set of keys off the cause, so a context that
    stopped at the envelope would satisfy ``--output json`` and leave somebody
    at a terminal answering a bare question. The second half of this test is the
    control: a refusal carrying nothing prints exactly what it printed before
    the context existed, which is what makes this addition additive.
    """
    spec = _context_spec(explicit=False)
    carried = render.render_gate(
        gates.DecisionRequired(
            spec, "r", {"ages": [{"portion": "database", "state": "never-recorded"}]}
        ).cause
    )
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
        "  or:      rerun with -d context.probe=<option>",
    ]


def _reaches_no_gate(ctx):
    """A handler that declares gates and asks none of them."""
    return ctx.envelope(data={"checks": [], "summary": {}})


def _reaches_only_the_first_gate(ctx):
    ctx.gate.require(ctx.entry.gates[0])
    return ctx.envelope(data={"checks": [], "summary": {}})


def test_conformance_3_fails_a_verb_that_declares_a_gate_and_never_asks_it(
    configured, monkeypatch
):
    """THE NEGATIVE CONTROL THE PREVIOUS VERSION DID NOT HAVE.

    ``_conformance_3`` returned the gates it reached and every caller threw the
    value away, so nothing compared reached against declared. Both shapes below
    passed against unmutated product source, and neither is exotic: the second is
    one refactor away, where a writer's check moves behind a path the verb no
    longer takes. A destructive database verb would then ship with its
    concurrent-writer decision unreachable and every assertion in this file
    green, because no other test in the suite holds a handler to the gates its
    registry entry declares.

    Driven rather than argued, in both shapes, and both are asserted to FAIL now.
    """
    base = registry.entry("profile.set")
    promoted = replace(base, gates=(base.gates[0], _SECOND_GATE))
    _swap_in(monkeypatch, promoted)

    monkeypatch.setattr("cratekit.cli.verbs.profile.apply_profile", _reaches_no_gate)
    with pytest.raises(AssertionError, match="never reached them"):
        _conformance_3(promoted, ["slim"])

    monkeypatch.setattr(
        "cratekit.cli.verbs.profile.apply_profile", _reaches_only_the_first_gate
    )
    with pytest.raises(AssertionError, match="never reached them"):
        _conformance_3(promoted, ["slim"])


def test_the_unreachable_exemption_covers_one_named_gate_and_expires_on_its_own(
    configured, monkeypatch
):
    """The exemption is per gate WITH a reason, not a hole the whole rule falls in.

    Both directions are driven. A verb declaring the exempt gate and not reaching
    it passes, which is the case the narrowing exists for and the case a
    universal rule would have refused. A verb declaring a gate that is NOT exempt
    and not reaching it fails, which is what the universal exemption gave away.

    And the entry expires. If the exempt gate is ever reached, the assertion says
    to delete it, because a gate that can fire is a gate the suite can hold every
    verb to. That is the countdown shape this repository already uses for a
    pending module, applied to a pending environment.
    """
    base = registry.entry("profile.set")
    with_exempt = replace(
        base, gates=(base.gates[0], registry.CLOUD_SYNC_UNREADABLE_GATE)
    )
    _swap_in(monkeypatch, with_exempt)
    monkeypatch.setattr(
        "cratekit.cli.verbs.profile.apply_profile", _reaches_only_the_first_gate
    )
    assert _conformance_3(with_exempt, ["slim"]) == ["profile.set.apply"], (
        "the cloud-sync gate cannot be provoked in this environment, so a verb "
        "that declares it and reaches its own gate is correct"
    )

    # The stale half: reaching an exempt gate must say the exemption is over.
    monkeypatch.setattr(
        "cratekit.cli.verbs.profile.apply_profile", _require_every_gate
    )
    with pytest.raises(AssertionError, match="exemption is stale"):
        _conformance_3(with_exempt, ["slim"])


#: EXACT MEMBERSHIP, because the three checks below are each satisfiable by a
#: plausible-looking addition. `registry.gate` only asks that SOME entry among
#: sixty-three declares the name, and the reason check is a length test rather
#: than a truth test, so a gate a landed verb declares and does not reach can be
#: exempted with one entry and an eighty-one character sentence. Verified: it
#: passed silently with all three guards green.
#:
#: Adding a gate here is now a red suite, which is the point. It is the same
#: shape `EXPECTED_PENDING` uses: the duplication IS the mechanism, because the
#: second place is a line a reviewer reads in a diff.
EXPECTED_UNREACHABLE_GATES = frozenset(
    {"write.cloudsync.unreadable", "intake.land.native", "intake.file.native"}
)


def test_the_unreachable_exemption_set_is_exactly_the_intended_one():
    """Three gates are exempt. A fourth one is a decision, not a diff.

    The second, ``intake.land.native``, joined with R-746: one verb, two media,
    one drive per fixture, and the conformance fixture's intake tree is on the
    bridge. Its own suite holds the verb to reaching it on a native tree. The
    third, ``intake.file.native``, joined with R-770 for the same reason: it
    is the second verb that writes the intake tree, on the same two media.

    Note what this pin does NOT prove, so nobody reads more into a green run than
    is there: the map is still a named exemption, not a drive of the unreadable
    state. Landed verbs that declare `write.cloudsync.unreadable` now go through
    assertion 3, and the exemption is what lets them reach OK without firing
    that gate. Its self-expiry is still proved by the synthetic tests above.
    """
    assert set(UNREACHABLE_GATES) == EXPECTED_UNREACHABLE_GATES, (
        f"the exemption set is {sorted(UNREACHABLE_GATES)} and this file "
        f"declares {sorted(EXPECTED_UNREACHABLE_GATES)}. Every entry here is a "
        f"gate no verb has to reach, which is the assertion switched off for "
        f"that gate across every entry that declares it."
    )


def test_every_unreachable_gate_is_real_and_carries_a_reason():
    """An exemption naming a gate nobody declares is an exemption nobody can audit."""
    for name, reason in UNREACHABLE_GATES.items():
        registry.gate(name)  # raises KeyError if no entry declares it
        assert len(reason) > 80, (
            f"{name} is exempted from assertion 3 with a reason too thin to "
            f"judge; say what makes it unprovokable and what would change that"
        )
