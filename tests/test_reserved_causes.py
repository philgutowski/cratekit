"""U38: the reserved exit-code table, and the two ways a module can bypass it.

S4 says every structured refusal cause has a reserved code and a remediation.
``cratekit.cli.exit_codes`` is that reservation. This file is what makes it a
CONSTRAINT rather than a lookup table nobody is obliged to consult, and it hunts
the five defects a registry-shaped thing in this repository has actually shipped:

1. **A duplicate key that Python resolves silently.** The reservations are a
   TUPLE and the mapping is built from it, so the count can see a repeat that a
   dict literal would have collapsed at parse time. Asserted against the
   distinct CAUSES, deliberately not against the distinct codes: several causes
   share a code on purpose and the closed reason registry makes the same
   argument at length.
2. **One symbol meaning two things.** Two keys in this table are also canonical
   remediation tokens, so each must reserve ITS OWN token, and any slug this
   table shares with ``core.cause.REASONS`` must reserve the identical code.
3. **A reserved range nothing enforces.** The range is 10 through 59 and a test
   fails on anything outside it, on the process band below, on the growth band
   above, and on any code no verb may return.
4. **A table that can be bypassed.** Two source guards, both bound through the
   import graph, forbid a second table anywhere else in the package and forbid a
   bare integer becoming a process status. Each ships fixtures proving it bites
   the evasion, including an aliased import, AND stays silent on correct code
   written in every import shape this repository allows (P7).
5. **A set that quantifies and enumerates.** The completeness check DERIVES the
   causes by walking the package for the exceptions that carry one, so a module
   landing later with an unreserved cause fails here rather than shipping a
   refusal nothing downstream can recover (P3).
"""

from __future__ import annotations

import enum
import importlib
import pkgutil
import typing
from pathlib import Path

import pytest

import cratekit
from cratekit.cli import exit_codes as reserved_codes
from cratekit.cli import render
from cratekit.core.cause import REASONS, Cause, CratekitError, Remediation
from cratekit.core.exit_codes import BANDS, MAX_CODE, ExitCode, Remedy, band_of, meaning_of
from tests._source_guards import process_status_literals, reserved_code_tables

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "src" / "cratekit"

#: The only two files in the package that may map a refusal cause to a code.
#: One is the reservation itself; the other is the closed reason registry that
#: predates it. A test below asserts the two AGREE wherever they overlap, which
#: is the alternative to pretending only one of them exists.
TABLE_OWNERS = frozenset({"cli/exit_codes.py", "core/cause.py"})

CAUSES = frozenset(reserved_codes.RESERVED_CAUSES)


def package_sources() -> list[tuple[str, str]]:
    """Every module this repository authors, as (path relative to the package, source).

    Vendored third-party code is excluded for the same reason the conformance
    suite excludes it: it is not ours to restyle, and holding it to a contract
    written after it was published produces a suppression comment somebody later
    reads as permission.
    """
    return [
        (path.relative_to(PACKAGE_ROOT).as_posix(), path.read_text())
        for path in sorted(PACKAGE_ROOT.rglob("*.py"))
        if "_vendor" not in path.parts
    ]


# ═══════════════════════════════════════════════════════════════════════════
# The table's own integrity
# ═══════════════════════════════════════════════════════════════════════════


def test_no_reservation_was_collapsed_by_a_duplicate_key():
    """The defect U19's merge had to disprove, asserted rather than reviewed.

    A duplicate key in a dict literal is resolved silently by whichever line
    comes last, and every test that iterates the runtime mapping is blind to it
    because the collapse already happened at parse time. Declaring the
    reservations as a TUPLE is what makes the count meaningful: the tuple keeps
    both entries, so the length of the index can disagree with it.

    The distinct CODES are deliberately not counted. Several causes share a code
    on purpose, exactly as the closed reason registry puts six slugs on one code
    and argues for it, so a count of distinct codes would be asserting a
    coincidence and would fail the next time two refusals correctly agree.
    """
    causes = [reservation.cause for reservation in reserved_codes.RESERVATIONS]
    duplicates = sorted({cause for cause in causes if causes.count(cause) > 1})
    assert not duplicates, f"reserved more than once: {duplicates}"
    assert len(reserved_codes.RESERVATIONS) == len(set(causes))
    assert len(reserved_codes.RESERVATIONS) == len(reserved_codes.RESERVED_CAUSES)


def test_the_index_refuses_a_duplicate_at_import_rather_than_only_in_a_test():
    """A duplicate that only the suite catches still ships to anyone who runs the code."""
    doubled = (
        reserved_codes.RESERVATIONS[0],
        reserved_codes.RESERVATIONS[0],
    )
    with pytest.raises(ValueError) as excinfo:
        reserved_codes._index(doubled)
    assert reserved_codes.RESERVATIONS[0].cause in str(excinfo.value)


def test_every_reservation_carries_a_remediation():
    """A refusal with nothing to do about it is the bare status this replaces."""
    for reservation in reserved_codes.RESERVATIONS:
        remediation = reservation.remediation()
        assert remediation.remedy is not None or remediation.steps
        assert reservation.note, f"{reservation.cause} says nothing about why this code"


def test_a_reservation_with_no_remediation_cannot_be_constructed():
    with pytest.raises(ValueError):
        reserved_codes.Reservation(
            cause="invented", code=ExitCode.PRECONDITION, note="no remediation at all"
        )


# ═══════════════════════════════════════════════════════════════════════════
# The reserved range, enforced rather than described
# ═══════════════════════════════════════════════════════════════════════════


def test_every_reserved_code_sits_inside_the_reserved_range():
    """10 through 59, and a test that fails on anything else.

    A range nothing enforces is a comment, and the next unit picks a code inside
    it. Below 10 is the process band: 0 is success, 1 is a defect, and 2 belongs
    to the argument parser, which is the one property the whole KTD25 fix rests
    on. At or above MAX_CODE is the shell's own territory, where 126 means not
    executable, 127 means not found, 128 plus a signal number covers 129 to 165,
    and anything past a byte truncates to something it did not mean.
    """
    low, high = reserved_codes.RESERVED_RANGE
    assert (low, high) == (10, 60)
    assert high <= MAX_CODE
    for reservation in reserved_codes.RESERVATIONS:
        value = int(reservation.code)
        assert isinstance(reservation.code, ExitCode), (
            f"{reservation.cause} reserves a bare integer rather than a member of "
            f"the one vocabulary"
        )
        assert low <= value < high, f"{reservation.cause} reserves {value}"
        assert value not in (0, 1, 2)
        assert band_of(reservation.code).name in reserved_codes.RESERVED_BANDS
        assert meaning_of(reservation.code).verb_producible


def test_the_growth_band_stays_free_of_reservations():
    """60 through 63 is the room a class nobody has met yet claims.

    Reserving inside it is how the room quietly disappears, so the range check
    excludes it and this asserts the consequence directly.
    """
    growth = BANDS[-1]
    assert growth.name == "unclaimed"
    taken = [
        reservation.cause
        for reservation in reserved_codes.RESERVATIONS
        if growth.start <= int(reservation.code) < growth.stop
    ]
    assert not taken, f"these reservations took the growth room: {taken}"


@pytest.mark.parametrize("value", [0, 1, 2, 60, 64, 126, 127, 130, 255])
def test_a_code_outside_the_range_cannot_be_reserved(value):
    """The range enforced at import, driven with the exact integers it excludes.

    ``ExitCode`` has no member for most of these, which is itself the answer: a
    reservation can only name a member, and the ones it CAN name that fall
    outside the range are refused by the index.
    """
    member = next((code for code in ExitCode if int(code) == value), None)
    if member is None:
        assert value >= MAX_CODE or value not in {int(c) for c in ExitCode}
        return
    candidate = reserved_codes.Reservation(
        cause="invented",
        code=member,
        note="outside the range on purpose",
        steps=("nothing",),
    )
    with pytest.raises(ValueError):
        reserved_codes._index((candidate,))


# ═══════════════════════════════════════════════════════════════════════════
# One symbol, one meaning
# ═══════════════════════════════════════════════════════════════════════════


def test_where_this_table_and_the_closed_reason_registry_overlap_they_agree():
    """Two tables giving one slug two codes is worse than one table giving it none.

    The overlap is not avoided, it is asserted. Today it is one slug and one is
    enough to prove the check works; the set is derived, so a slug that appears
    in both later is checked without anyone remembering to add it.
    """
    shared = sorted(CAUSES & set(REASONS))
    assert shared, "the overlap vanished; this check has stopped checking anything"
    for slug in shared:
        assert reserved_codes.code_for(slug) is REASONS[slug], (
            f"{slug!r} exits with {reserved_codes.code_for(slug).name} here and "
            f"{REASONS[slug].name} in the closed reason registry, so one refusal "
            f"has two meanings depending on which table a caller read"
        )


def test_a_reserved_cause_that_is_also_a_remedy_token_reserves_that_token():
    """The sharp edge of one flat key space, closed.

    ``core.backup_facts`` models an unreadable fact file as a choice of REMEDY
    rather than a choice of cause, so two keys in this table are remediation
    tokens. ``upgrade-cratekit`` is also what ``core.config`` says about a file
    from a newer build, and a key that meant "upgrade" in one reading and
    something else in another would be the exact defect a registry exists to
    prevent.
    """
    tokens = {str(member): member for member in Remedy}
    overlapping = sorted(CAUSES & set(tokens))
    assert overlapping, "no key is a remediation token; this check has gone stale"
    for slug in overlapping:
        reservation = reserved_codes.reserved(slug)
        assert reservation.remedy is tokens[slug], (
            f"{slug!r} is a remediation token and reserves {reservation.remedy!r}, "
            f"so the same symbol says two different things"
        )


# ═══════════════════════════════════════════════════════════════════════════
# What an unreserved cause does, and what a reserved one renders to
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unreserved_cause_fails_and_names_itself():
    """Never a default code. A default is indistinguishable from a real answer."""
    with pytest.raises(reserved_codes.UnreservedCause) as excinfo:
        reserved_codes.code_for("a-cause-nobody-reserved")
    assert "a-cause-nobody-reserved" in str(excinfo.value)
    assert isinstance(excinfo.value, KeyError)


def test_every_reserved_cause_renders_to_something_a_user_can_act_on():
    """The consequence the reservation exists for, asserted at the output boundary.

    A remediation that renders to the exit code's generic summary tells a person
    "an unexpected failure" when the table knew exactly what to say. That is the
    same collapse the module-local remediation audit already found live once, so
    it is checked here over every reservation rather than over a sample.
    """
    generic = {str(meaning_of(code).summary) for code in ExitCode}
    for reservation in reserved_codes.RESERVATIONS:
        line = render.remediation_line(
            Cause(
                reason="internal-error",
                message="driven through the real renderer",
                remediation=reservation.remediation(),
            )
        )
        body = line.removeprefix("  fix: ").strip()
        assert body, f"{reservation.cause} renders to nothing"
        assert body not in generic, (
            f"{reservation.cause} renders as the exit code's generic summary "
            f"rather than as its own remediation"
        )


def test_a_reservation_builds_the_remediation_a_cause_carries():
    """The table hands out the type the boundary actually builds, not a lookalike."""
    reservation = reserved_codes.reserved("rekordbox-running")
    remediation = reserved_codes.remediation_for("rekordbox-running")
    assert isinstance(remediation, Remediation)
    assert remediation.remedy is Remedy.QUIT_REKORDBOX
    assert reservation.code is ExitCode.REKORDBOX_OPEN
    # The one path a refusal actually takes: reason from the closed registry,
    # remediation from this table, and the two agree on the status.
    error = CratekitError(
        Cause(
            reason="rekordbox-running",
            message="the application is running",
            remediation=remediation,
        )
    )
    assert error.cause.code is reservation.code


# ═══════════════════════════════════════════════════════════════════════════
# Completeness, derived by walking (P3)
# ═══════════════════════════════════════════════════════════════════════════


def structured_refusal_causes() -> dict[str, frozenset[str]]:
    """Every structured refusal cause in the package, as module -> cause slugs.

    DERIVED, and the derivation is the specification of what this table owes.

    A ``CratekitError`` already carries a ``Cause`` whose reason comes from the
    closed registry, so its code is reserved by construction and it is not the
    gap. The gap is every OTHER exception in the package that carries a
    structured discriminator, because there is nothing downstream that turns one
    of those into a status. Those are found by their shape: an exception defined
    in this package, not a ``CratekitError``, whose constructor takes a parameter
    annotated with an enum this package defines.

    That shape deliberately excludes ``core.config`` and ``core.secrets``, whose
    structured cause is the exception TYPE rather than an enum member. Their
    conversion is already declared at the command-line boundary and they already
    arrive carrying their own remediation token, so reserving them here would be
    the second opinion this table exists to prevent.
    """
    found: dict[str, frozenset[str]] = {}
    for info in pkgutil.walk_packages(cratekit.__path__, "cratekit."):
        if "._vendor" in info.name:
            continue
        try:
            module = importlib.import_module(info.name)
        except Exception:  # noqa: BLE001 - a missing heavy extra is not a failure here
            continue
        for value in vars(module).values():
            if not (isinstance(value, type) and issubclass(value, Exception)):
                continue
            if value.__module__ != info.name or issubclass(value, CratekitError):
                continue
            try:
                hints = typing.get_type_hints(value.__init__)
            except Exception:  # noqa: BLE001 - an unresolvable annotation is not a cause
                continue
            for hint in hints.values():
                if not (isinstance(hint, type) and issubclass(hint, enum.Enum)):
                    continue
                if not hint.__module__.startswith("cratekit."):
                    continue
                if hint.__module__ == "cratekit.core.exit_codes":
                    continue
                slugs = frozenset(str(member.value) for member in hint)
                found[f"{info.name}.{value.__name__}"] = slugs
    return found


def test_every_structured_refusal_cause_in_the_package_is_reserved():
    """S4, quantified over a set this test derives rather than lists.

    A module landing later with a cause nobody reserved fails HERE, which is the
    scenario the brief asks for, rather than shipping a refusal that arrives at
    the shell as a bare integer. The reverse direction is asserted too: a
    reservation nothing raises is a dead entry, and dead entries are what a
    reader trusts by mistake.
    """
    derived = structured_refusal_causes()
    assert derived, "the walk found no structured refusal cause; it is broken, not the tree"
    raised = frozenset().union(*derived.values())

    unreserved = sorted(raised - CAUSES)
    assert not unreserved, (
        f"these structured refusal causes have no reserved exit code, so each one "
        f"reaches the process boundary as a bare status with its remediation "
        f"discarded: {unreserved}. They are raised by {sorted(derived)}"
    )
    orphaned = sorted(CAUSES - raised)
    assert not orphaned, (
        f"these causes are reserved and nothing in the package raises them: "
        f"{orphaned}. A reservation with no producer is read as a contract and is "
        f"not one"
    )


def test_the_three_surfaces_the_waiting_guard_names_are_covered():
    """The unit's own brief, named explicitly beside the derivation.

    The derived check above would pass if the walk quietly stopped finding one of
    these, and a walk that finds nothing is exactly how P3's own lesson recurs.
    """
    derived = structured_refusal_causes()
    for producer in (
        "cratekit.modules.tools.backup.BackupRefused",
        "cratekit.modules.tools.mastering.MasteringRefused",
        "cratekit.core.backup_facts.BackupFactsUnreadable",
        "cratekit.core.binaries.BinaryNotFound",
    ):
        assert producer in derived, f"the walk no longer sees {producer}"
        assert derived[producer] <= CAUSES


# ═══════════════════════════════════════════════════════════════════════════
# The guards, driven against the evasion AND against correct code (P7)
# ═══════════════════════════════════════════════════════════════════════════

CORRECT_READS_THE_TABLE = """
from cratekit.cli.exit_codes import code_for

def status(cause):
    return int(code_for(cause))
"""

CORRECT_USES_THE_VOCABULARY = """
from cratekit.core.exit_codes import ExitCode

DEFAULT = ExitCode.PRECONDITION

def classify(kind):
    return ExitCode.LIBRARY_UNAVAILABLE if kind == "volume" else DEFAULT
"""

CORRECT_SENTENCES_KEYED_BY_CAUSE = """
ADVICE = {
    "rclone-missing": "install the program that talks to the remote",
    "rekordbox-running": "quit the application and let its agent settle",
}
"""

CORRECT_EXITS_THROUGH_THE_ENVELOPE = """
import sys

from cratekit.cli.exit_codes import code_for

def main(envelope, cause):
    sys.exit(int(code_for(cause)))

def clean():
    sys.exit(0)
"""

CORRECT_SOMEBODY_ELSE_HAS_AN_EXIT = """
class Runner:
    def exit(self, code):
        return code

def drive(runner):
    runner.exit(21)
"""

CORRECT_ALIASED_IMPORT_USED_ORDINARILY = """
import cratekit.core.exit_codes as ec

def classify(broken):
    return ec.ExitCode.LIBRARY_UNREADABLE if broken else ec.ExitCode.OK
"""

CORRECT_A_MAPPING_THIS_TABLE_DOES_NOT_OWN = """
from cratekit.core.exit_codes import ExitCode

PORTION_CODES = {
    "files": ExitCode.LIBRARY_UNAVAILABLE,
    "settings": ExitCode.PRECONDITION,
}
"""

EVASION_BARE_INTEGER_TABLE = """
CODES = {
    "rclone-missing": 30,
    "rekordbox-running": 21,
}
"""

EVASION_ALIASED_MODULE_IMPORT = """
import cratekit.core.exit_codes as ec

CODES = {"rekordbox-running": ec.ExitCode.REKORDBOX_OPEN}
"""

EVASION_ALIASED_CLASS_IMPORT = """
from cratekit.core.exit_codes import ExitCode as EC

CODES = {"database-absent": EC.LIBRARY_UNAVAILABLE}
"""

EVASION_FROM_THE_PACKAGE = """
from cratekit.core import exit_codes

CODES = {"encoder-missing": exit_codes.ExitCode.PRECONDITION}
"""

EVASION_ALIASED_SYS_EXIT = """
import sys as system

def refuse():
    system.exit(21)
"""

EVASION_RAISES_A_STATUS = """
def refuse():
    raise SystemExit(30)
"""


@pytest.mark.parametrize(
    "source",
    [
        CORRECT_READS_THE_TABLE,
        CORRECT_USES_THE_VOCABULARY,
        CORRECT_SENTENCES_KEYED_BY_CAUSE,
        CORRECT_EXITS_THROUGH_THE_ENVELOPE,
        CORRECT_SOMEBODY_ELSE_HAS_AN_EXIT,
        CORRECT_ALIASED_IMPORT_USED_ORDINARILY,
        CORRECT_A_MAPPING_THIS_TABLE_DOES_NOT_OWN,
    ],
)
def test_the_second_table_guard_stays_silent_on_correct_code(source):
    """P7. A guard that fires on correct code is a guard somebody switches off.

    Both halves of P7 are here. The aliased import is the shape that DEFEATED an
    armed guard in this repository once, so it is driven as an evasion below and
    as ordinary correct code here: recognizing the alias must not turn every
    aliased module into a suspect. The mapping this table does not own is the
    other half: a module keying its own data on its own slugs is not a second
    reservation and reporting it would be the false positive that gets the guard
    suppressed.
    """
    assert reserved_code_tables(source, CAUSES) == []


@pytest.mark.parametrize(
    "source",
    [
        EVASION_BARE_INTEGER_TABLE,
        EVASION_ALIASED_MODULE_IMPORT,
        EVASION_ALIASED_CLASS_IMPORT,
        EVASION_FROM_THE_PACKAGE,
    ],
)
def test_the_second_table_guard_bites_every_shape_of_second_opinion(source):
    """Including the two aliased shapes, which is what defeated the armed guards once."""
    assert reserved_code_tables(source, CAUSES)


@pytest.mark.parametrize(
    "source",
    [
        CORRECT_READS_THE_TABLE,
        CORRECT_EXITS_THROUGH_THE_ENVELOPE,
        CORRECT_SOMEBODY_ELSE_HAS_AN_EXIT,
        CORRECT_USES_THE_VOCABULARY,
    ],
)
def test_the_bare_status_guard_stays_silent_on_correct_code(source):
    assert process_status_literals(source) == []


@pytest.mark.parametrize("source", [EVASION_ALIASED_SYS_EXIT, EVASION_RAISES_A_STATUS])
def test_the_bare_status_guard_bites_a_module_that_returns_a_raw_literal(source):
    assert process_status_literals(source)


def test_no_module_in_the_package_keeps_a_second_reservation_table():
    """The guards, over the real tree.

    Exactly two files may map a refusal cause to a code, and both are named
    above. Anywhere else is a second opinion that will eventually disagree with
    the first, which is the argument this repository has already made about its
    duplicate taxonomy resolvers.
    """
    offenders = {
        relative: reserved_code_tables(source, CAUSES)
        for relative, source in package_sources()
        if relative not in TABLE_OWNERS and reserved_code_tables(source, CAUSES)
    }
    assert not offenders, f"a second reservation table: {offenders}"


def test_no_module_in_the_package_turns_a_bare_integer_into_a_status():
    offenders = {
        relative: process_status_literals(source)
        for relative, source in package_sources()
        if process_status_literals(source)
    }
    assert not offenders, (
        f"these bypass the vocabulary entirely and exit with an integer nobody "
        f"reserved: {offenders}"
    )
