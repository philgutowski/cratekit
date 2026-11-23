"""U38: the reserved exit-code table, and the two ways a module can bypass it.

S4 says every structured refusal cause has a reserved code and a remediation.
``cratekit.cli.exit_codes`` is that reservation, and this file makes it a
constraint rather than a lookup table nobody must consult. It hunts five
defects a registry in this repository has shipped:

1. A duplicate key Python resolves silently: the reservations are a tuple, so
   the count sees a repeat a dict literal would collapse.
2. One symbol meaning two things: a key that is also a remediation token
   reserves its own token, and a slug shared with ``core.cause.REASONS``
   reserves the identical code.
3. A range nothing enforces: 10 through 59, clear of the process band, the
   growth band and any code no verb may return.
4. A table that can be bypassed: two source guards, bound through the import
   graph, forbid a second table and a bare integer becoming a process status,
   each with fixtures proving it bites the evasion and stays silent on correct
   code in every import shape the repository allows (P7).
5. A set that quantifies and enumerates: the completeness check derives the
   causes by walking the package (P3).

Most of the file is the fixtures six review rounds wrote after a plausible
``modules/tools/tagger.py`` with unreserved causes, its own table and bare
exits passed the suite; the unit record has the story. The measurements are in
the residual "The tiers were bought with a number that does not exist" and the residual
"The mutation table for this unit's guards, written into the repository".
"""

from __future__ import annotations

import ast
import dataclasses
import enum
import functools
import importlib
import pkgutil
import re
import sys
import typing
from pathlib import Path
from types import MappingProxyType, ModuleType
from typing import Iterator, Mapping

import pytest

import cratekit
from cratekit.cli import exit_codes as reserved_codes
from cratekit.cli import render
from cratekit.core import backup_facts, config
from cratekit.core.cause import REASONS, Cause, CratekitError, Remediation
from cratekit.core.exit_codes import BANDS, MAX_CODE, ExitCode, Remedy, band_of, meaning_of
from tests import _source_guards as _guards
from tests._parse_memo import parsed, shares_parses, sharing_parses
from tests._pinned_reserved_populations import (
    PINNED_KEBAB_LITERALS_BY_MODULE,
    PINNED_LITERAL_HOLDERS,
    PINNED_LITERAL_HOLDERS_WITH_INTEGER,
    PINNED_NAMED_WITH_INTEGER,
    PINNED_NAMED_WITH_OWN,
    PINNED_NAMED_WITHOUT_OWN,
    PINNED_NON_RESERVED_CAUSES,
    PINNED_RESERVED_CAUSE_COUNT,
)
from tests._source_guards import (
    process_status_literals,
    reserved_code_tables,
    reserved_code_tables_in,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "src" / "cratekit"

#: Where a per module pin is edited, said by every failure that names one (U296).
_PIN_FILES = "each in its own package's file under tests/ratchets/reserved_causes/"


@pytest.fixture(autouse=True, scope="module")
def _one_parse_per_text():
    """Every test here shares one tree per text, dropped when the module ends (U312)."""
    with sharing_parses():
        yield

#: The only two files in the package that may map a refusal cause to a code: the
#: reservation and the closed reason registry. A test below asserts they agree.
TABLE_OWNERS = frozenset({"cli/exit_codes.py", "core/cause.py"})

CAUSES = frozenset(reserved_codes.RESERVED_CAUSES)

#: The range the guard measures a bare integer against, taken from the table.
RANGE = reserved_codes.RESERVED_RANGE

#: The package enums that are NOT a refusal cause vocabulary, and why. Every
#: OTHER package enum reaching an exception's constructor is one.
#:
#: By enum identity, never by parameter name: reading the role from the name let
#: a rename drop ``preflight.LibraryVolumeError`` and restore ``Scope``. A new
#: enum on an exception must be classified here by a person, with a reason;
#: ``test_every_enum_declared_not_a_cause_exists`` keeps the entries honest.
NOT_A_CAUSE: Mapping[str, str] = MappingProxyType(
    {
        "cratekit.core.cause.Scope": (
            "how wide a failure's blast radius is. Context travelling ON a "
            "refusal, not the reason for it; every cause already carries one"
        ),
        "cratekit.core.cause.Outcome": (
            "what a run DID. An envelope field, and a successful run has one"
        ),
        "cratekit.core.jobs.JobState": "where a job is in its lifecycle",
        "cratekit.core.jobs.ItemState": "where one item of a job is in its lifecycle",
        "cratekit.core.backup_facts.Portion": (
            "WHICH half of a backup, the files or the database. A subject, and "
            "both portions appear on a run that refused nothing"
        ),
        "cratekit.core.backup_facts.AgeState": (
            "whether a recorded age is usable. A reading, and its usable value "
            "is the ordinary one"
        ),
        "cratekit.core.binaries.PackageManager": (
            "WHERE a missing program is installed from, carried on the install "
            "hint that rides beside the remedy. The cause is that the program is "
            "absent; this says which command line would fix it, which is the "
            "remediation's own detail. Found by the dataclass hop, which is the "
            "identity rule doing its job: it demanded a classification for an "
            "enum a person had to look at, rather than guessing from a name"
        ),
        "cratekit.acquire.adapter.TrackOutcome": "what happened to one requested track",
        "cratekit.acquire.adapter.InvocationOutcome": "how one adapter invocation ended",
        "cratekit.acquire.download.ProviderSignal": (
            "what the provider signalled during a download, including nothing "
            "unusual at all"
        ),
        "cratekit.core.routing.Decline": (
            "why tagging would not answer. A decline is a RESULT and the module "
            "says so in its own docstring, not a refusal that ends a process"
        ),
    }
)

#: The refusals whose discriminator this table deliberately does NOT reserve, and
#: the conversion that already gives each a code and a remediation. Named, not
#: excluded by an annotation the derivation could not read.
#: ``test_every_exclusion_names_a_refusal_something_already_converts`` proves each.
CONVERTED_ELSEWHERE: Mapping[str, str] = MappingProxyType(
    {
        "cratekit.core.config.ConfigError": (
            "cratekit/cli/__init__.py catches this AT THE COMMAND-LINE BOUNDARY "
            "and builds a cause with reason config-unusable, which core.cause "
            "already reserves at PRECONDITION, carrying the module's own token "
            "through unchanged. Reserving its six tokens here would be a second "
            "opinion, and for upgrade-cratekit it would be a WRONG one: this "
            "table reserves that key at 32 for the unreadable fact file, and the "
            "configuration path exits 30. See the module docstring, which now "
            "records that collision instead of claiming it does not exist"
        ),
        "cratekit.acquire.adapter.AdapterError": (
            "the acquisition layer catches its own failures and folds them into "
            "an InvocationOutcome carrying exc.remedy, so an adapter refusal "
            "becomes a run RESULT rather than an exception at the boundary. Its "
            "nine tokens are remediation for a track, not a status for a process"
        ),
        "cratekit.core.preflight.LibraryVolumeError": (
            "cratekit/core/session.py converts every MountState through "
            "_MOUNT_REASONS into a slug core.cause.REASONS already reserves, "
            "with MOUNT_LIBRARY_VOLUME as the remedy, before a destructive "
            "session resolves a single path. Its seven states are a diagnosis "
            "of one condition the closed registry already spells four ways. "
            "This entry is the one the previous round excluded by ACCIDENT: the "
            "parameter is called status and the enum sits one field down inside "
            "a dataclass, so the walk lost a live refusal and said nothing"
        ),
    }
)


def package_sources() -> list[tuple[str, str]]:
    """Every module this repository authors, as (path relative to the package, source).

    Vendored code is excluded: it is not ours to hold to a later contract.
    """
    return [
        (path.relative_to(PACKAGE_ROOT).as_posix(), path.read_text())
        for path in sorted(PACKAGE_ROOT.rglob("*.py"))
        if "_vendor" not in path.parts
    ]


# The table's own integrity


def test_no_reservation_was_collapsed_by_a_duplicate_key():
    """A duplicate key in a dict literal collapses silently; the tuple keeps both.

    Distinct codes are not counted: several causes share a code on purpose.
    """
    causes = [reservation.cause for reservation in reserved_codes.RESERVATIONS]
    duplicates = sorted({cause for cause in causes if causes.count(cause) > 1})
    assert not duplicates, f"reserved more than once: {duplicates}"
    assert len(reserved_codes.RESERVATIONS) == len(set(causes))
    assert len(reserved_codes.RESERVATIONS) == len(reserved_codes.RESERVED_CAUSES)


def test_the_index_refuses_a_duplicate_rather_than_letting_the_later_one_win():
    """A duplicate that only the suite catches still ships to anyone who runs the code."""
    doubled = (
        reserved_codes.RESERVATIONS[0],
        reserved_codes.RESERVATIONS[0],
    )
    with pytest.raises(ValueError) as excinfo:
        reserved_codes._index(doubled)
    assert reserved_codes.RESERVATIONS[0].cause in str(excinfo.value)


def test_the_index_runs_at_import_rather_than_only_when_a_test_calls_it():
    """The published mapping is built at import, so a refused reservation cannot load."""
    tree = ast.parse((PACKAGE_ROOT / "cli" / "exit_codes.py").read_text())
    built_at_import = [
        node
        for node in tree.body
        if isinstance(node, (ast.Assign, ast.AnnAssign))
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "_index"
    ]
    assert built_at_import, (
        "RESERVED_CAUSES is no longer built by a module-level call to _index, so "
        "nothing enforces the range or the duplicate check until a test asks"
    )


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


# The reserved range, enforced rather than described


def test_every_reserved_code_sits_inside_the_reserved_range():
    """10 through 59, and a test that fails on anything else.

    Below 10 is the process band (0 success, 1 defect, 2 the argument parser,
    KTD25). At or above MAX_CODE is the shell's territory: 126, 127, 128 plus a
    signal up to SIGRTMAX 64, and truncation past a byte. The job engine reads a
    negative signal number through subprocess.returncode; the range is clear of both.
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


def test_the_growth_band_is_closed_at_both_ends_rather_than_merely_unused():
    """60 through 63 is the growth band: the range stops before it and no member sits in it."""
    growth = BANDS[-1]
    assert growth.name == "unclaimed"
    assert reserved_codes.RESERVED_RANGE[1] <= growth.start, (
        "the reserved range now reaches into the growth band, so the room is "
        "claimable by the next reservation rather than kept"
    )
    inhabited = [code.name for code in ExitCode if growth.start <= int(code) < growth.stop]
    assert not inhabited, f"the growth room has been built on: {inhabited}"
    taken = [
        reservation.cause
        for reservation in reserved_codes.RESERVATIONS
        if growth.start <= int(reservation.code) < growth.stop
    ]
    assert not taken, f"these reservations took the growth room: {taken}"


def test_the_permitted_bands_are_exactly_the_bands_the_range_spans():
    """The permitted bands are derived from the range, so widening one alone fails."""
    low, high = reserved_codes.RESERVED_RANGE
    spanned = {band.name for band in BANDS if band.start < high and band.stop > low}
    assert reserved_codes.RESERVED_BANDS == spanned, (
        f"the permitted bands are {sorted(reserved_codes.RESERVED_BANDS)} and the "
        f"range {low} to {high - 1} spans {sorted(spanned)}"
    )


def _candidate(code) -> reserved_codes.Reservation:
    return reserved_codes.Reservation(
        cause="invented", code=code, note="outside the range on purpose", steps=("nothing",)
    )


@pytest.mark.parametrize("value", [0, 1, 2])
def test_a_code_the_vocabulary_has_but_the_range_excludes_cannot_be_reserved(value):
    """``ExitCode`` has members at 0, 1 and 2 only outside 10 to 59, so those test the range.

    The assertion is on the message naming the range, not on any ValueError.
    """
    member = next(code for code in ExitCode if int(code) == value)
    with pytest.raises(ValueError) as excinfo:
        reserved_codes._index((_candidate(member),))
    assert "outside the reserved range" in str(excinfo.value)
    assert "invented" in str(excinfo.value)


@pytest.mark.parametrize("value", [3, 60, 63, 64, 126, 127, 130, 255])
def test_a_bare_integer_cannot_be_reserved_whatever_integer_it_is(value):
    """A reservation can only name an ``ExitCode`` member; a bare integer is refused by name."""
    assert value not in {int(code) for code in ExitCode}
    with pytest.raises(ValueError) as excinfo:
        reserved_codes._index((_candidate(value),))
    assert "not a member of the one status vocabulary" in str(excinfo.value)


def test_the_range_is_pinned_where_the_reservations_are_checked_against_it():
    """Named so nobody reads the two tests above as pinning the range itself."""
    assert reserved_codes.RESERVED_RANGE == (10, 60)
    assert reserved_codes.RESERVED_RANGE[1] <= MAX_CODE


# One symbol, one meaning


def test_where_this_table_and_the_closed_reason_registry_overlap_they_agree():
    """Where both tables reserve a slug they agree; the overlap is derived, not listed."""
    shared = sorted(CAUSES & set(REASONS))
    assert shared, "the overlap vanished; this check has stopped checking anything"
    for slug in shared:
        assert reserved_codes.code_for(slug) is REASONS[slug], (
            f"{slug!r} exits with {reserved_codes.code_for(slug).name} here and "
            f"{REASONS[slug].name} in the closed reason registry, so one refusal "
            f"has two meanings depending on which table a caller read"
        )


def test_the_two_tables_spell_two_conditions_twice_and_still_agree():
    """Two conditions spelled twice across the tables, invisible to the overlap check, agree on 22.

    Not renamed: a slug is persisted in a stored cause and crosses the job
    engine's process boundary, so renaming one is a breaking change.
    """
    for reserved_slug, registry_slug in (
        ("library-root-absent", "library-directory-missing"),
        ("database-absent", "library-database-missing"),
    ):
        assert reserved_codes.code_for(reserved_slug) is REASONS[registry_slug], (
            f"{reserved_slug!r} and {registry_slug!r} are two spellings of one "
            f"condition and now exit with two different statuses"
        )


def test_upgrade_cratekit_is_declared_three_times_and_this_table_reserves_one_meaning():
    """``upgrade-cratekit`` means 32 for an unreadable fact file and 30 for config, pinned."""
    declaring = sorted(
        f"{owner.__module__}.{owner.__qualname__}"
        for owner in (backup_facts.Remedy, config.Remedy, Remedy)
        if "upgrade-cratekit" in {str(member.value) for member in owner}
    )
    assert len(declaring) == 3, f"the collision changed shape: {declaring}"
    assert reserved_codes.code_for("upgrade-cratekit") is ExitCode.ACK_REQUIRED
    assert REASONS["config-unusable"] is ExitCode.PRECONDITION
    assert reserved_codes.code_for("upgrade-cratekit") is not REASONS["config-unusable"]


def test_a_reserved_cause_that_is_also_a_remedy_token_reserves_that_token():
    """A reserved cause that is also a remedy token reserves that token, in one flat key space."""
    tokens = {str(member): member for member in Remedy}
    overlapping = sorted(CAUSES & set(tokens))
    assert overlapping, "no key is a remediation token; this check has gone stale"
    for slug in overlapping:
        reservation = reserved_codes.reserved(slug)
        assert reservation.remedy is tokens[slug], (
            f"{slug!r} is a remediation token and reserves {reservation.remedy!r}, "
            f"so the same symbol says two different things"
        )


# What an unreserved cause does, and what a reserved one renders to


def test_an_unreserved_cause_fails_and_names_itself():
    """Never a default code. A default is indistinguishable from a real answer."""
    with pytest.raises(reserved_codes.UnreservedCause) as excinfo:
        reserved_codes.code_for("a-cause-nobody-reserved")
    assert "a-cause-nobody-reserved" in str(excinfo.value)
    assert isinstance(excinfo.value, KeyError)


def test_every_reserved_cause_renders_to_something_a_user_can_act_on():
    """Every reservation renders to an actionable remediation, never the generic summary."""
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
    # The path a refusal takes: reason from the registry, remediation from this table.
    error = CratekitError(
        Cause(
            reason="rekordbox-running",
            message="the application is running",
            remediation=remediation,
        )
    )
    assert error.cause.code is reservation.code


# Completeness, derived by walking (P3)


_NAMESPACES: dict[str, dict[str, object]] = {}


def _annotation_namespace(module: ModuleType | None) -> dict[str, object]:
    """Every name this module's import statements bind, TYPE_CHECKING included.

    ``get_type_hints`` raises ``NameError`` for a name imported only under
    ``if TYPE_CHECKING:``, so the imports are read from the source instead.
    """
    if module is None:
        return {}
    cached = _NAMESPACES.get(module.__name__)
    if cached is not None:
        return cached
    namespace: dict[str, object] = {}
    _NAMESPACES[module.__name__] = namespace
    source_file = getattr(module, "__file__", None)
    if source_file is None:
        return namespace
    try:
        tree = ast.parse(Path(source_file).read_text())
    except OSError:  # pragma: no cover - a module with no readable source
        return namespace
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and not node.level:
            for alias in node.names:
                try:
                    imported = importlib.import_module(node.module)
                    namespace[alias.asname or alias.name] = getattr(imported, alias.name)
                except Exception:  # noqa: BLE001 - a name that will not resolve is not a cause
                    continue
        elif isinstance(node, ast.Import):
            for alias in node.names:
                bound = alias.name if alias.asname else alias.name.split(".")[0]
                try:
                    namespace[alias.asname or bound] = importlib.import_module(bound)
                except Exception:  # noqa: BLE001 - as above
                    continue
    return namespace


def _is_a_record(hint: type) -> bool:
    """A dataclass or a ``NamedTuple``: the two ways this repository writes a record.

    A ``NamedTuple`` is recognized as a tuple subclass carrying ``_fields``.
    """
    if dataclasses.is_dataclass(hint):
        return True
    return issubclass(hint, tuple) and hasattr(hint, "_fields")


def _declared_enums(
    hint: object, owner: str, packages: tuple[str, ...], hops: int = 0
) -> Iterator[type]:
    """Every enum this repository declares that an annotation can carry.

    Recursive over unions (``Refusal | None``), and one field into a record
    (dataclass or ``NamedTuple``), since ``preflight.LibraryVolumeError`` carries a
    ``MountStatus`` holding the ``MountState`` cause. One hop only. ``ExitCode``
    alone is excluded: a status is not a cause, and excluding its whole module hid
    the canonical ``Remedy``.
    """
    if isinstance(hint, type) and issubclass(hint, enum.Enum):
        if hint is ExitCode:
            return
        if hint.__module__ == owner or hint.__module__.split(".")[0] in packages:
            yield hint
        return
    if isinstance(hint, type) and _is_a_record(hint) and hops < 1:
        if hint.__module__ == owner or hint.__module__.split(".")[0] in packages:
            fields = typing.get_type_hints(
                hint, localns=_annotation_namespace(sys.modules.get(hint.__module__))
            )
            for field in fields.values():
                yield from _declared_enums(field, hint.__module__, packages, hops + 1)
        return
    for argument in typing.get_args(hint):
        yield from _declared_enums(argument, owner, packages, hops)


def refusal_causes_in(
    module: ModuleType,
    *,
    packages: tuple[str, ...] = ("cratekit",),
    excluded: Mapping[str, str] = CONVERTED_ELSEWHERE,
) -> dict[str, frozenset[str]]:
    """The structured refusal causes ONE module declares, as producer -> slugs.

    Derived, and the derivation is what this table owes. A ``CratekitError``
    carries a registry cause and is reserved by construction. The gap is every
    other exception defined here whose constructor takes a parameter annotated
    with an enum this repository declares and ``NOT_A_CAUSE`` does not exclude.
    The role is read from the enum, by identity, never from the parameter name.

    It cannot see ``core.secrets``, whose exception TYPE is the discriminator;
    that is recorded in ``docs/residual-findings.md``.
    """
    namespace_owner = module
    found: dict[str, frozenset[str]] = {}
    for value in vars(module).values():
        if not (isinstance(value, type) and issubclass(value, Exception)):
            continue
        if getattr(value, "__module__", None) != module.__name__:
            continue
        if issubclass(value, CratekitError):
            continue
        if any(
            f"{base.__module__}.{base.__qualname__}" in excluded
            for base in value.__mro__
        ):
            continue
        initializer = value.__init__
        owner = sys.modules.get(getattr(initializer, "__module__", ""), namespace_owner)
        slugs: set[str] = set()
        try:
            hints = typing.get_type_hints(initializer, localns=_annotation_namespace(owner))
            for name, hint in hints.items():
                if name == "return":
                    continue
                for declared in _declared_enums(hint, value.__module__, packages):
                    if f"{declared.__module__}.{declared.__qualname__}" in NOT_A_CAUSE:
                        continue
                    slugs.update(str(member.value) for member in declared)
        except Exception as exc:  # noqa: BLE001 - re-raised, never swallowed
            raise AssertionError(
                f"{module.__name__}.{value.__name__} has an annotation this walk "
                f"cannot resolve ({type(exc).__name__}: {exc}). Swallowing it "
                f"would make the exception invisible to the completeness check "
                f"rather than failing, which is how a refusal ships with no "
                f"reserved code and nobody finds out"
            ) from exc
        if slugs:
            found[f"{module.__name__}.{value.__name__}"] = frozenset(slugs)
    return found


def imported_package_modules() -> tuple[list[ModuleType], dict[str, str]]:
    """Every module in the package, imported, and the ones that would not import.

    The failures are returned, not skipped, so coverage never depends silently
    on which extras are installed (P3).
    """
    modules: list[ModuleType] = []
    unimportable: dict[str, str] = {}
    for info in pkgutil.walk_packages(cratekit.__path__, "cratekit."):
        if "._vendor" in info.name:
            continue
        try:
            modules.append(importlib.import_module(info.name))
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            unimportable[info.name] = f"{type(exc).__name__}: {exc}"
    return modules, unimportable


def structured_refusal_causes() -> dict[str, frozenset[str]]:
    """Every structured refusal cause in the package, as producer -> cause slugs."""
    modules, unimportable = imported_package_modules()
    # Duplicated on purpose by the standalone import test; this one stops a caller
    # of the derivation reading a short answer as complete. See the residual
    # "One check in this unit is unreachable".
    assert not unimportable, (
        f"the walk could not import these, so whatever refusal causes they "
        f"declare are invisible to the completeness check: {unimportable}"
    )
    found: dict[str, frozenset[str]] = {}
    for module in modules:
        found.update(refusal_causes_in(module))
    return found


def test_every_module_in_the_package_imports_so_the_walk_can_see_it():
    """Coverage that depends on an installed extra is coverage nobody can measure."""
    _, unimportable = imported_package_modules()
    assert not unimportable, f"these are invisible to the derivation: {unimportable}"


def test_every_structured_refusal_cause_in_the_package_is_reserved():
    """S4 over a derived set: an unreserved cause fails here, and so does a dead reservation."""
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
    """The brief's three surfaces, named beside the derivation so a walk that loses one fails."""
    derived = structured_refusal_causes()
    for producer in (
        "cratekit.modules.tools.backup.BackupRefused",
        "cratekit.modules.tools.mastering.MasteringRefused",
        "cratekit.core.backup_facts.BackupFactsUnreadable",
        "cratekit.core.binaries.BinaryNotFound",
    ):
        assert producer in derived, f"the walk no longer sees {producer}"
        assert derived[producer] <= CAUSES


def _local_function_names(tree: ast.AST) -> set[str]:
    """Every function and method this source defines, to tell a helper from a builtin."""
    return {
        node.name
        for node in _guards._walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _handler_uses_what_it_bound(handler: ast.ExceptHandler, helpers: set[str]) -> bool:
    """Whether THIS handler uses the exception it bound, rather than discarding it.

    Scoped to the handler: scoped to the file, any ``exc.anything`` elsewhere
    vouched for it. Two uses count: an attribute read off the bound name, or
    handing it to a function this file defines (``acquire/download.py``).
    ``str(exc)`` reads nothing and stays a swallow.
    """
    bound = handler.name
    for node in _guards._walk(handler):
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == bound
        ):
            return True
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        called = (
            function.id
            if isinstance(function, ast.Name)
            else function.attr
            if isinstance(function, ast.Attribute)
            else None
        )
        if called not in helpers:
            continue
        given = list(node.args) + [keyword.value for keyword in node.keywords]
        if any(isinstance(argument, ast.Name) and argument.id == bound for argument in given):
            return True
    return False


def converting_handlers(tree: ast.AST) -> list[ast.ExceptHandler]:
    """Every handler in one source that binds an exception AND uses it."""
    helpers = _local_function_names(tree)
    return [
        node
        for node in _guards._walk(tree)
        if isinstance(node, ast.ExceptHandler)
        and node.name is not None
        and node.type is not None
        and _handler_uses_what_it_bound(node, helpers)
    ]


def _converted_exception_types() -> set[type]:
    return set(_converted_exception_types_once())


@functools.cache
def _converted_exception_types_once() -> frozenset[type]:
    """Exception classes this package catches and then inspects, resolved for real.

    Each clause is resolved against its module's globals, so it answers for the
    class, never for a spelling like ``Exception`` or a local ``ConfigError``.
    "Inspects" is ``_handler_uses_what_it_bound``, per handler.

    It cannot prove a conversion is lossless, as the residual
    "The conversion proof shows that a conversion exists, not that it keeps anything"
    records; the historical example is item 2 of the residual
    "Five accepted findings from the U38 reviews", closed by U48.
    """
    found: set[type] = set()
    modules, _ = imported_package_modules()
    for module in modules:
        source_file = getattr(module, "__file__", None)
        if source_file is None or "_vendor" in source_file:
            continue
        tree = parsed(Path(source_file).read_text())
        for node in converting_handlers(tree):
            caught = node.type.elts if isinstance(node.type, ast.Tuple) else [node.type]
            for entry in caught:
                resolved = _resolve_in(module, ast.unparse(entry))
                if isinstance(resolved, type) and issubclass(resolved, BaseException):
                    found.add(resolved)
    return frozenset(found)


A_HANDLER_THAT_READS_AN_ATTRIBUTE = """
def load(path):
    try:
        return read(path)
    except ConfigError as exc:
        return Refusal(remedy=exc.remedy)
"""

A_HANDLER_THAT_HANDS_IT_TO_A_HELPER = """
def _fold(run, exc):
    return Outcome(detail=str(exc), remedy=exc.remedy)


def acquire(run):
    try:
        return fetch(run)
    except AdapterBroken as exc:
        return _fold(run, exc)
"""

A_HANDLER_THAT_DISCARDS_IT = """
def _fold(exc):
    return Outcome(remedy=exc.remedy)


def load(path):
    try:
        return read(path)
    except ConfigError as exc:
        logger.debug("no usable configuration: %s", exc)
        return None
"""

A_HANDLER_THAT_ONLY_STRINGIFIES_IT = """
def load(path):
    try:
        return read(path)
    except ConfigError as exc:
        raise Refusal(str(exc)) from exc
"""


def test_the_conversion_proof_is_scoped_to_the_handler_that_bound_the_exception():
    """A handler that binds ``exc`` and discards it is a swallow, whatever helpers the file has."""
    assert converting_handlers(ast.parse(A_HANDLER_THAT_READS_AN_ATTRIBUTE))
    assert converting_handlers(ast.parse(A_HANDLER_THAT_HANDS_IT_TO_A_HELPER))
    assert converting_handlers(ast.parse(A_HANDLER_THAT_DISCARDS_IT)) == [], (
        "the handler binds the exception and throws it away, and the attribute "
        "read that vouched for it belongs to an unrelated helper"
    )
    assert converting_handlers(ast.parse(A_HANDLER_THAT_ONLY_STRINGIFIES_IT)) == [], (
        "str(exc) reads nothing off the exception, which is what separates a "
        "conversion from a swallow"
    )


def _resolve_in(module: ModuleType, dotted: str) -> object | None:
    """``preflight.LibraryVolumeError`` as the class the MODULE means by it."""
    parts = dotted.split(".")
    current: object | None = vars(module).get(parts[0])
    for part in parts[1:]:
        if current is None:
            return None
        current = getattr(current, part, None)
    return current


def test_every_exclusion_names_a_refusal_something_already_converts():
    """Each exclusion must name a class something in the package catches and inspects."""
    converted = _converted_exception_types()
    for qualname, reason in CONVERTED_ELSEWHERE.items():
        assert reason, f"{qualname} is excluded and says nothing about why"
        module_name, _, class_name = qualname.rpartition(".")
        excluded = getattr(importlib.import_module(module_name), class_name)
        family = {
            candidate for candidate in converted if issubclass(candidate, excluded)
        }
        assert family, (
            f"{qualname} is excluded from the completeness walk because something "
            f"already converts it, and nothing in this package catches that class "
            f"and inspects it. Either the conversion went away, in which case the "
            f"exclusion has to go too, or the entry was never true"
        )


def test_the_conversion_proof_answers_for_a_class_and_not_for_a_spelling():
    """The proof answers for a class: never ``Exception``, ``BaseException`` or a spelling."""
    converted = _converted_exception_types()
    assert config.ConfigError in converted
    assert Exception not in converted, (
        "the proof accepts a catch-all handler, so any module with an except "
        "Exception clause can keep any exclusion alive"
    )
    assert BaseException not in converted
    assert all(issubclass(entry, BaseException) for entry in converted)


def test_the_excluded_refusals_are_absent_from_the_derivation():
    """The exclusion actually applies, rather than being decorative."""
    derived = structured_refusal_causes()
    assert not [producer for producer in derived if producer.startswith("cratekit.core.config.")]
    assert not [producer for producer in derived if producer.startswith("cratekit.acquire.adapter.")]
    for slug in ("fix-config-values", "switch-adapter", "repair-config-file"):
        assert slug not in CAUSES, (
            f"{slug!r} is reserved here as well as carried by the module that "
            f"already converts it, which is the second opinion this table "
            f"exists to prevent"
        )


# The derivation itself, driven against modules written to defeat it (P7)
#
# These build a real module from source, so annotations, hierarchies and the
# TYPE_CHECKING fixture behave as they do in the package.

FIXTURE_PACKAGES = ("cratekit", "u38fix")


@pytest.fixture
def module_from(tmp_path):
    """Build an importable module from source, and take it back out afterwards."""
    built: list[str] = []

    def build(name: str, source: str) -> ModuleType:
        dotted = f"u38fix.{name}"
        path = tmp_path / f"{name}.py"
        path.write_text(source)
        module = ModuleType(dotted)
        module.__file__ = str(path)
        sys.modules[dotted] = module
        built.append(dotted)
        exec(compile(source, str(path), "exec"), module.__dict__)  # noqa: S102 - a fixture
        return module

    yield build
    for dotted in built:
        sys.modules.pop(dotted, None)
        _NAMESPACES.pop(dotted, None)


SEEN_OPTIONAL_DISCRIMINATOR = """
from __future__ import annotations

from enum import StrEnum


class Refusal(StrEnum):
    SOURCE_UNREADABLE = "tagger-source-unreadable"
    ART_REJECTED = "tagger-art-rejected"


class TaggingRefused(Exception):
    refusal: Refusal = Refusal.SOURCE_UNREADABLE

    def __init__(self, detail: str, *, refusal: Refusal | None = None) -> None:
        super().__init__(detail)
        if refusal is not None:
            self.refusal = refusal
"""

SEEN_DISCRIMINATOR_IMPORTED_FOR_TYPING_ONLY = """
from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cratekit.core.backup_facts import Remedy


class Unreadable(Exception):
    def __init__(self, message: str, *, remedy: Remedy) -> None:
        super().__init__(message)
        self.remedy = remedy
"""

SEEN_THE_CANONICAL_REMEDY = """
from __future__ import annotations

from cratekit.core.exit_codes import Remedy


class TaggingRefused(Exception):
    def __init__(self, detail: str, *, remedy: Remedy) -> None:
        super().__init__(detail)
        self.remedy = remedy
"""

SEEN_A_DATACLASS_EXCEPTION = """
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Refusal(StrEnum):
    ART_REJECTED = "tagger-art-rejected"


@dataclass
class TaggingRefused(Exception):
    refusal: Refusal
    detail: str = ""
"""

SEEN_A_TYPE_CALL = """
from __future__ import annotations

from enum import StrEnum


class Refusal(StrEnum):
    ART_REJECTED = "tagger-art-rejected"


def _init(self, refusal: Refusal, detail: str) -> None:
    Exception.__init__(self, detail)
    self.refusal = refusal


TaggingRefused = type("TaggingRefused", (Exception,), {"__init__": _init})
"""

SEEN_A_FACTORY = """
from __future__ import annotations

from enum import StrEnum


class Refusal(StrEnum):
    ART_REJECTED = "tagger-art-rejected"


def _refusal_type(name):
    class Refused(Exception):
        def __init__(self, refusal: Refusal, detail: str) -> None:
            super().__init__(detail)
            self.refusal = refusal

    Refused.__name__ = name
    Refused.__qualname__ = name
    return Refused


TaggingRefused = _refusal_type("TaggingRefused")
"""

SEEN_A_BASE_IN_ANOTHER_MODULE = """
from __future__ import annotations

from u38fix.upstream import UpstreamRefused


class TaggingRefused(UpstreamRefused):
    pass
"""

UPSTREAM_FOR_THE_SUBCLASS = """
from __future__ import annotations

from enum import StrEnum


class Refusal(StrEnum):
    ART_REJECTED = "tagger-art-rejected"


class UpstreamRefused(Exception):
    def __init__(self, refusal: Refusal, detail: str) -> None:
        super().__init__(detail)
        self.refusal = refusal
"""

def _context_carried_on_a_refusal(parameter: str) -> str:
    """The reviewer's false positive, spelled with any parameter name at all."""
    return (
        "from __future__ import annotations\n\n"
        "from cratekit.core.cause import Scope\n\n\n"
        "class ProbeProblem(Exception):\n"
        f"    def __init__(self, message: str, {parameter}: Scope = Scope.RUN) -> None:\n"
        "        super().__init__(message)\n"
        f"        self.{parameter} = {parameter}\n"
    )


UNSEEN_CONTEXT_RATHER_THAN_A_CAUSE = _context_carried_on_a_refusal("scope")

SEEN_A_DISCRIMINATOR_NOBODY_CALLED_REFUSAL = """
from __future__ import annotations

from enum import StrEnum


class Refusal(StrEnum):
    ART_REJECTED = "tagger-art-rejected"


class TaggingRefused(Exception):
    def __init__(self, verdict: Refusal, detail: str) -> None:
        super().__init__(detail)
        self.verdict = verdict
"""

SEEN_A_DISCRIMINATOR_ONE_FIELD_DOWN = """
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Refusal(StrEnum):
    ART_REJECTED = "tagger-art-rejected"


@dataclass(frozen=True)
class Report:
    verdict: Refusal
    examined: Path | None = None


class TaggingRefused(Exception):
    def __init__(self, status: Report, detail: str = "") -> None:
        super().__init__(detail)
        self.status = status
"""

SEEN_A_DISCRIMINATOR_ONE_FIELD_DOWN_IN_A_NAMED_TUPLE = """
from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import NamedTuple


class Refusal(StrEnum):
    ART_REJECTED = "tagger-art-rejected"


class Report(NamedTuple):
    verdict: Refusal
    examined: Path | None = None


class TaggingRefused(Exception):
    def __init__(self, status: Report, detail: str = "") -> None:
        super().__init__(detail)
        self.status = status
"""

UNSEEN_A_STATUS_IS_NOT_A_CAUSE = """
from __future__ import annotations

from cratekit.core.exit_codes import ExitCode


class Refused(Exception):
    def __init__(self, message: str, *, cause: ExitCode) -> None:
        super().__init__(message)
        self.cause = cause
"""

UNSEEN_A_CRATEKIT_ERROR = """
from __future__ import annotations

from enum import StrEnum

from cratekit.core.cause import Cause, CratekitError


class Refusal(StrEnum):
    ART_REJECTED = "tagger-art-rejected"


class Refused(CratekitError):
    def __init__(self, cause: Cause, refusal: Refusal | None = None) -> None:
        super().__init__(cause)
"""


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (SEEN_OPTIONAL_DISCRIMINATOR, {"tagger-source-unreadable", "tagger-art-rejected"}),
        # Three members since U27 appended GRANT_PATH_ACCESS; re-pinned when a unit
        # adds one, never widened.
        (
            SEEN_DISCRIMINATOR_IMPORTED_FOR_TYPING_ONLY,
            {"repair-backup-facts", "upgrade-cratekit", "grant-path-access"},
        ),
        (SEEN_A_DATACLASS_EXCEPTION, {"tagger-art-rejected"}),
        (SEEN_A_TYPE_CALL, {"tagger-art-rejected"}),
        (SEEN_A_FACTORY, {"tagger-art-rejected"}),
        (SEEN_A_DISCRIMINATOR_NOBODY_CALLED_REFUSAL, {"tagger-art-rejected"}),
        (SEEN_A_DISCRIMINATOR_ONE_FIELD_DOWN, {"tagger-art-rejected"}),
        (SEEN_A_DISCRIMINATOR_ONE_FIELD_DOWN_IN_A_NAMED_TUPLE, {"tagger-art-rejected"}),
    ],
)
def test_the_walk_sees_every_shape_a_refusal_is_actually_written_in(
    module_from, source, expected
):
    """Unions and typing-only imports, the ordinary shapes the walk once could not see."""
    module = module_from("subject", source)
    derived = refusal_causes_in(module, packages=FIXTURE_PACKAGES)
    assert derived, "the walk saw nothing"
    assert frozenset().union(*derived.values()) == expected


def test_the_hop_into_a_record_reads_a_named_tuple_and_not_only_a_dataclass(module_from):
    """A record hop reads a ``NamedTuple`` as well as a dataclass."""
    dataclass_form = module_from("record_dc", SEEN_A_DISCRIMINATOR_ONE_FIELD_DOWN)
    named_tuple_form = module_from(
        "record_nt", SEEN_A_DISCRIMINATOR_ONE_FIELD_DOWN_IN_A_NAMED_TUPLE
    )
    seen_as_dataclass = refusal_causes_in(dataclass_form, packages=FIXTURE_PACKAGES)
    seen_as_named_tuple = refusal_causes_in(named_tuple_form, packages=FIXTURE_PACKAGES)
    assert frozenset().union(*seen_as_named_tuple.values()) == frozenset(
        {"tagger-art-rejected"}
    )
    assert frozenset().union(*seen_as_named_tuple.values()) == frozenset().union(
        *seen_as_dataclass.values()
    ), "one keyword changed the answer, which is a rule a rename defeats"


def test_the_walk_sees_a_refusal_whose_base_lives_in_another_module(module_from):
    module_from("upstream", UPSTREAM_FOR_THE_SUBCLASS)
    module = module_from("child", SEEN_A_BASE_IN_ANOTHER_MODULE)
    derived = refusal_causes_in(module, packages=FIXTURE_PACKAGES)
    assert derived == {"u38fix.child.TaggingRefused": frozenset({"tagger-art-rejected"})}


def test_the_walk_demands_the_whole_vocabulary_a_module_claims(module_from):
    """A module annotating the canonical Remedy owes every token of it."""
    module = module_from("canonical", SEEN_THE_CANONICAL_REMEDY)
    derived = refusal_causes_in(module, packages=FIXTURE_PACKAGES)
    slugs = frozenset().union(*derived.values())
    assert {str(member) for member in Remedy} == set(slugs)
    assert slugs - CAUSES, "this must fail the completeness check, not pass it"


@pytest.mark.parametrize(
    "source",
    [
        UNSEEN_CONTEXT_RATHER_THAN_A_CAUSE,
        UNSEEN_A_STATUS_IS_NOT_A_CAUSE,
        UNSEEN_A_CRATEKIT_ERROR,
    ],
)
def test_the_walk_stays_silent_on_an_exception_that_reserves_nothing(module_from, source):
    """P7 for the derivation: an exception that reserves nothing draws no demand."""
    module = module_from("subject", source)
    assert refusal_causes_in(module, packages=FIXTURE_PACKAGES) == {}


@pytest.mark.parametrize("parameter", ["scope", "reason", "cause", "refusal", "remedy"])
def test_renaming_a_parameter_cannot_turn_context_into_a_cause(module_from, parameter):
    """The role lives on the enum, so renaming a parameter ``reason`` changes nothing."""
    module = module_from("context", _context_carried_on_a_refusal(parameter))
    assert refusal_causes_in(module, packages=FIXTURE_PACKAGES) == {}


@pytest.mark.parametrize("parameter", ["status", "verdict", "refusal", "problem"])
def test_renaming_a_parameter_cannot_hide_a_cause_either(module_from, parameter):
    """And the other direction: ``status`` on ``LibraryVolumeError`` cannot hide its causes."""
    source = SEEN_A_DISCRIMINATOR_NOBODY_CALLED_REFUSAL.replace("verdict", parameter)
    module = module_from("named", source)
    derived = refusal_causes_in(module, packages=FIXTURE_PACKAGES)
    assert frozenset().union(*derived.values()) == {"tagger-art-rejected"}


def test_the_live_refusal_a_name_filter_dropped_is_seen_again():
    """With the exclusion lifted the walk sees LibraryVolumeError: the exclusion is a decision."""
    from cratekit.core import preflight

    without_exclusions = refusal_causes_in(preflight, excluded={})
    producer = "cratekit.core.preflight.LibraryVolumeError"
    assert producer in without_exclusions
    assert without_exclusions[producer] == frozenset(
        str(member.value) for member in preflight.MountState
    )
    assert not without_exclusions[producer] <= CAUSES, (
        "these are unreserved, which is why losing them silently mattered"
    )
    assert refusal_causes_in(preflight) == {}


def test_every_enum_declared_not_a_cause_exists():
    """Every ``NOT_A_CAUSE`` entry names an enum that exists."""
    for qualname, reason in NOT_A_CAUSE.items():
        assert reason, f"{qualname} is declared not a cause and says nothing about why"
        module_name, _, class_name = qualname.rpartition(".")
        declared = getattr(importlib.import_module(module_name), class_name, None)
        assert isinstance(declared, type) and issubclass(declared, enum.Enum), (
            f"{qualname} is classified here and is not an enum in the package"
        )


def test_an_unresolvable_annotation_fails_rather_than_disappearing(module_from):
    """Swallowing this is what made a whole class of module invisible."""
    module = module_from(
        "broken",
        "from __future__ import annotations\n\n\n"
        "class Refused(Exception):\n"
        "    def __init__(self, refusal: NeverDefined) -> None:\n"
        "        super().__init__()\n",
    )
    with pytest.raises(AssertionError, match="cannot resolve"):
        refusal_causes_in(module, packages=FIXTURE_PACKAGES)


# The guards, driven against the evasion AND against correct code (P7)

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

# ── Correct code keyed on a cause slug and mapped to an INTEGER ─────────────
#
# A guard that fires on correct code gets its file added to the owners and
# switched off. Six reserved keys are remediation tokens, so an order, a retry
# budget and a backoff are slugs mapped to small integers and not reservations.

CORRECT_A_RETRY_FLAG_PER_CAUSE = """
RETRYABLE = {
    "rekordbox-running": False,
    "rclone-missing": True,
}
"""

CORRECT_A_BACKOFF_PER_CAUSE = """
BACKOFF_SECONDS = {
    "rekordbox-running": 5,
    "remote-not-configured": 0,
}
"""

CORRECT_A_DISPLAY_ORDER_PER_REMEDY = """
ORDER = {
    "run-setup": 1,
    "upgrade-cratekit": 2,
    "install-binary": 3,
}
"""

CORRECT_AN_ATTEMPT_BUDGET = """
ATTEMPTS = {"encoder-failed": 3}
"""

CORRECT_A_SEVERITY_RANKING = """
SEVERITY = {
    "rclone-missing": 2,
    "database-absent": 1,
    "no-snapshot-available": 1,
}
"""

CORRECT_A_COUNTER = """
COUNTS = {"rclone-missing": 0}
"""

CORRECT_A_BRANCH_THAT_WAITS = """
def wait_for(step):
    if step == "library-scan":
        seconds = 30
        return seconds
    return 0
"""

# ── Correct code whose integers sit INSIDE the reserved range ───────────────
#
# Kebab keys nobody declared as a cause, so the guard stays silent.

CORRECT_LOGGING_LEVELS = """
LEVELS = {
    "per-track": 10,
    "per-run": 20,
    "problems-only": 30,
}
"""

CORRECT_COLUMN_WIDTHS = """
COLUMNS = (
    ("track-title", 40),
    ("artist-name", 30),
    ("release-label", 24),
)
"""

CORRECT_TIMEOUTS_AND_BUDGETS = """
TIMEOUT_SECONDS = {"catalogue-lookup": 30, "artwork-fetch": 15}
ATTEMPTS = {"catalogue-lookup": 12}
RETENTION_DAYS = {"dated-archive": 30}
"""

CORRECT_A_THRESHOLD_AND_A_VERSION = """
FUZZY_THRESHOLD = {"artist-name": 55}
SCHEMA_VERSIONS = {"routing-ledger": 11}
"""

CORRECT_A_FUNCTION_RETURNING_A_WIDTH = """
def width_for(column):
    if column == "track-title":
        return 40
    return 24
"""

CORRECT_A_PROGRESS_WEIGHT_PER_STEP = """
WEIGHTS = (("library-scan", 30), ("tag-write", 55))
"""

# ── The residual, pinned rather than discovered ────────────────────────────
#
# Once a string IS a declared cause, an in-range integer beside it reads as a
# reservation. This backoff is reported, as a decision someone can find.

RESIDUAL_A_BACKOFF_ON_A_REAL_CAUSE = """
BACKOFF_SECONDS = {"rekordbox-running": 30}
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

# ── A second table for causes NOBODY has reserved ───────────────────────────
#
# Each declares its causes in its own enum, as the tree's vocabularies do,
# which makes the key a cause. The package-wide derivation route is driven
# separately below with the declaration removed.

DECLARES_ITS_CAUSES = """
from enum import StrEnum


class Refusal(StrEnum):
    SOURCE_UNREADABLE = "tagger-source-unreadable"
    ART_REJECTED = "tagger-art-rejected"
    LOOKUP_UNAVAILABLE = "tagger-lookup-unavailable"

"""

# ── HOW AN ENUM IS RECOGNIZED, in the two spellings that tell the rules apart ──
#
# Every base in ``tests/`` was ``Enum``, ``StrEnum`` or ``IntEnum``, so the
# "ends in Enum" rule was indistinguishable from that list. Each fixture here is
# silent under the other clause alone.

DECLARES_ITS_CAUSES_ON_AN_ALIASED_BASE = """
from enum import StrEnum as Vocabulary


class Refusal(Vocabulary):
    ART_REJECTED = "tagger-art-rejected"


CODES = {"tagger-art-rejected": 41}
"""

DECLARES_ITS_CAUSES_ON_A_BASE_OF_OUR_OWN = """
from cratekit.core.vocabulary import CratekitEnum


class Refusal(CratekitEnum):
    ART_REJECTED = "tagger-art-rejected"


CODES = {"tagger-art-rejected": 41}
"""

DECLARES_ITS_CAUSES_THROUGH_THE_ENUM_MODULE = """
import enum as vocabularies


class Refusal(vocabularies.StrEnum):
    ART_REJECTED = "tagger-art-rejected"


CODES = {"tagger-art-rejected": 41}
"""

CORRECT_A_PLAIN_CLASS_DECLARES_NOTHING = """
class Refusal:
    ART_REJECTED = "tagger-art-rejected"


CODES = {"tagger-art-rejected": 41}
"""

EVASION_A_NEW_MODULE_DECIDES_ITS_OWN_CODES = DECLARES_ITS_CAUSES + """
from cratekit.core.exit_codes import ExitCode

CODES = {
    "tagger-source-unreadable": ExitCode.PRECONDITION,
    "tagger-art-rejected": 30,
    "tagger-lookup-unavailable": 41,
}
"""

EVASION_A_TUPLE_OF_PAIRS = DECLARES_ITS_CAUSES + """
CODES = (
    ("tagger-source-unreadable", 30),
    ("tagger-art-rejected", 41),
)
"""

EVASION_A_COMPREHENSION_OVER_PAIRS = DECLARES_ITS_CAUSES + """
CODES = {cause: code for cause, code in (("tagger-art-rejected", 30),)}
"""

EVASION_A_COMPREHENSION_OVER_SLUGS = DECLARES_ITS_CAUSES + """
CODES = {cause: 30 for cause in ("tagger-art-rejected", "tagger-source-unreadable")}
"""

EVASION_ZIPPED_FROM_TWO_SEQUENCES = DECLARES_ITS_CAUSES + """
SLUGS = ("tagger-art-rejected", "tagger-source-unreadable")
STATUSES = (30, 41)

CODES = dict(zip(SLUGS, STATUSES))
"""

#: A ZIP THAT IS NOT A PAIR OF SEQUENCES. ``_zipped`` refuses any call not of
#: two arguments; without the refusal this source raises ``IndexError``.
CORRECT_A_ZIP_OF_ONE_SEQUENCE = DECLARES_ITS_CAUSES + """
SLUGS = ("tagger-art-rejected", "tagger-source-unreadable")

CODES = dict(zip(SLUGS))
"""

EVASION_FILLED_A_KEY_AT_A_TIME = DECLARES_ITS_CAUSES + """
CODES = {}
CODES["tagger-art-rejected"] = 30
"""

EVASION_AN_ORDERED_DICT = DECLARES_ITS_CAUSES + """
from collections import OrderedDict

CODES = OrderedDict([("tagger-art-rejected", 30)])
"""

EVASION_SETDEFAULT = DECLARES_ITS_CAUSES + """
CODES = {}

def reserve():
    CODES.setdefault("tagger-art-rejected", 30)
"""

EVASION_A_MATCH_STATEMENT = DECLARES_ITS_CAUSES + """
def status(cause):
    match cause:
        case "tagger-art-rejected":
            return 30
        case "tagger-source-unreadable":
            return 41
        case _:
            return 1
"""

EVASION_AN_IF_CHAIN = DECLARES_ITS_CAUSES + """
def status(cause):
    if cause == "tagger-art-rejected":
        return 30
    if cause == "tagger-source-unreadable":
        return 41
    return 1
"""

EVASION_A_CODE_WITH_A_CONVERSION_ROUND_IT = DECLARES_ITS_CAUSES + """
from cratekit.core.exit_codes import ExitCode

CODES = {
    "tagger-art-rejected": int(ExitCode.PRECONDITION),
    "tagger-source-unreadable": ExitCode(30),
}
"""

# ── The codes held in NAMES, which is how a careful author writes them ──────

EVASION_A_CODE_HELD_IN_A_CONSTANT = DECLARES_ITS_CAUSES + """
PRECONDITION = 30
UPSTREAM = 41

CODES = {
    "tagger-art-rejected": PRECONDITION,
    "tagger-lookup-unavailable": UPSTREAM,
}
"""

EVASION_A_CODE_HELD_ON_A_CLASS = DECLARES_ITS_CAUSES + """
class Status:
    PRECONDITION = 30


CODES = {"tagger-art-rejected": Status.PRECONDITION}
"""

EVASION_A_CODE_IN_THE_MODULES_OWN_ENUM = DECLARES_ITS_CAUSES + """
from enum import IntEnum


class Code(IntEnum):
    PRECONDITION = 30


CODES = {"tagger-art-rejected": Code.PRECONDITION}
"""

EVASION_A_CODE_REACHED_BY_ARITHMETIC = DECLARES_ITS_CAUSES + """
BASE = 30

CODES = {"tagger-art-rejected": BASE + 1}
"""

EVASION_A_CODE_ASSIGNED_THEN_RETURNED = DECLARES_ITS_CAUSES + """
def status(cause):
    if cause == "tagger-art-rejected":
        code = 41
        return code
    return 1
"""

# ── U38's own idiom, copied by the next module ─────────────────────────────
#
# cli/exit_codes.py declares a TUPLE OF DATACLASSES, not two-element pairs.

EVASION_A_TUPLE_LONGER_THAN_A_PAIR = DECLARES_ITS_CAUSES + """
TABLE = (
    ("tagger-source-unreadable", 30, "the file could not be read"),
    ("tagger-lookup-unavailable", 41, "the catalogue did not answer"),
)
"""

EVASION_A_TUPLE_OF_DATACLASSES = DECLARES_ITS_CAUSES + """
from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    cause: str
    code: int
    note: str


RESERVATIONS = (
    Entry("tagger-source-unreadable", 30, "the file could not be read"),
    Entry("tagger-art-rejected", 30, "the artwork failed validation"),
)
"""

EVASION_A_TABLE_KEYED_BY_KEYWORD = DECLARES_ITS_CAUSES + """
from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    cause: str
    code: int


RESERVATIONS = (Entry(cause="tagger-art-rejected", code=41),)
"""

EVASION_KEYWORD_EXPANSION = """
CODES = dict(**{"rclone-missing": 30})
"""

EVASION_A_READ_ONLY_WRAPPER = """
from types import MappingProxyType

CODES = MappingProxyType(dict(**{"rclone-missing": 30}))
"""

EVASION_AN_UPDATE = """
CODES = {}
CODES.update({"rclone-missing": 30})
"""

EVASION_AN_IMPLICITLY_CONCATENATED_KEY = """
CODES = {"rclone-" "missing": 30}
"""

# ── A second opinion about a slug only the CLOSED REGISTRY reserves ─────────
#
# Most of ``core.cause.REASONS`` lies outside the reserved table, and a module
# contradicting one of those is the same defect. Derive the counts rather than
# reading them here: ``len(REASONS)`` and its overlap with ``RESERVED_CAUSES``.
# The sixteen shapes below are ordinary Python and each a second opinion; the
# tiered rule of round four reported two of them, the wide rule all sixteen.

EVASION_A_NAMED_CODE_FOR_A_REGISTRY_SLUG = """
from cratekit.core.exit_codes import ExitCode

CODES = {"config-unusable": ExitCode.LIBRARY_UNAVAILABLE}
"""

EVASION_A_CONVERSION_ON_A_REGISTRY_SLUG = """
from cratekit.core.exit_codes import ExitCode

CODES = {"credential-missing": int(ExitCode.PRECONDITION)}
"""

# The residual "The tiers were bought with a number that does not exist"
# said tier two accepted a conversion round the vocabulary. These two are that
# spelling, the second from the residual "One check in this unit is unreachable".
EVASION_A_CONSTRUCTOR_ON_A_REGISTRY_SLUG = """
from cratekit.core.exit_codes import ExitCode

CODES = {"config-unusable": ExitCode(30)}
"""

EVASION_A_CONSTRUCTOR_THROUGH_THE_MODULE_ON_A_REGISTRY_SLUG = """
from cratekit.core import exit_codes

CODES = {"config-unusable": exit_codes.ExitCode(30)}
"""

# A module declaring its OWN status enum is the most flagrant second table.
EVASION_ITS_OWN_ENUM_FOR_A_REGISTRY_SLUG = """
from enum import IntEnum


class Code(IntEnum):
    PRECONDITION = 30


CODES = {"doctor-check-failed": Code.PRECONDITION}
"""

EVASION_A_NAMED_CONSTANT_FOR_A_REGISTRY_SLUG = """
PRECONDITION = 30

CODES = {"module-extras-missing": PRECONDITION}
"""

EVASION_ARITHMETIC_FOR_A_REGISTRY_SLUG = """
BASE = 30

CODES = {"anlz-modified": BASE + 3}
"""

# The input round four used to reject narrowing to the live integers: a
# registry-only slug and a code no ``ExitCode`` member uses.
EVASION_AN_INVENTED_CODE_FOR_A_REGISTRY_SLUG = """
CODES = {"tree-registry-unusable": 33}
"""

EVASION_A_BARE_CODE_FOR_A_REGISTRY_SLUG = """
CODES = {"config-unusable": 22}
"""

EVASION_A_REGISTRY_SLUG_TABLE_AS_A_TUPLE = """
TABLE = (
    ("config-unusable", 30, "the configuration could not be read"),
    ("credential-missing", 41, "no credential was recorded"),
)
"""

EVASION_A_REGISTRY_SLUG_TABLE_FILLED_A_KEY_AT_A_TIME = """
CODES = {}
CODES["config-unusable"] = 30
"""

EVASION_A_REGISTRY_SLUG_TABLE_BY_COMPREHENSION = """
CODES = {slug: 30 for slug in ("config-unusable", "credential-missing")}
"""

EVASION_A_REGISTRY_SLUG_TABLE_ZIPPED = """
SLUGS = ("config-unusable", "credential-missing")
STATUSES = (30, 41)

CODES = dict(zip(SLUGS, STATUSES))
"""

EVASION_A_REGISTRY_SLUG_IF_CHAIN = """
def status(cause):
    if cause == "config-unusable":
        return 30
    return 1
"""

EVASION_A_REGISTRY_SLUG_MATCH_STATEMENT = """
def status(cause):
    match cause:
        case "config-unusable":
            return 30
        case _:
            return 1
"""

EVASION_A_REGISTRY_SLUG_CODE_HELD_ON_A_CLASS = """
class Status:
    PRECONDITION = 30


CODES = {"config-unusable": Status.PRECONDITION}
"""

# ── An ``ExitCode`` member held in a NAME, which is what a careful author writes ──
#
# ``resolve_int``'s attribute branch reads only classes this source defines, so
# an imported enum member held in a name needs its own reading.

EVASION_A_VOCABULARY_MEMBER_HELD_IN_A_CONSTANT = """
from cratekit.core.exit_codes import ExitCode

CODE = ExitCode.PRECONDITION

CODES = {"rclone-missing": CODE}
"""

EVASION_A_VOCABULARY_MEMBER_ASSIGNED_THEN_RETURNED = """
from cratekit.core.exit_codes import ExitCode


def status(cause):
    if cause == "rclone-missing":
        code = ExitCode.PRECONDITION
        return code
    return 1
"""

# The deepest spelling the hop bound promises: named, named again, adjusted.
# Three hops, which is ``MAX_HOPS``.
EVASION_A_CODE_NAMED_TWICE_THEN_ADJUSTED = DECLARES_ITS_CAUSES + """
BASE = 30
OFFSET = BASE

CODES = {"tagger-art-rejected": OFFSET + 1}
"""

# ── Ordinary code keyed on a registry slug, with integers that MATTER ───────
#
# THIS IS THE RESIDUAL, not a silence: a poll interval of 30 keyed on a cause
# slug reads as a reservation of 30, and is reported. One genuinely not a
# reservation is a decision recorded here, never a comment on the line.

RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS = """
POLL_SECONDS = {"session-lock-held": 30, "write-lock-held": 15}

DISPLAY_ORDER = {
    "credential-missing": 10,
    "config-unusable": 20,
    "internal-error": 30,
}

COLUMN_WIDTHS = (("decision-required", 40), ("decision-stale", 24))

SCHEMA_VERSIONS = {"job-schema-mismatch": 11, "review-schema-mismatch": 12}

RETENTION_DAYS = {"backup-facts-unreadable": 30}

SHARE_PERCENT = {"library-database-missing": 50}

WEIGHTS = (("library-volume-unmounted", 30), ("cloud-sync-active", 20))

DELAYS = {}
DELAYS["cloud-sync-unreadable"] = 30
DELAYS.setdefault("canary-read-failed", 15)

SLOW_DELAYS = {name: 30 for name in ("smoke-test-failed", "doctor-check-failed")}

SENTENCES = {
    "internal-error": "report this as a defect",
    "credential-missing": "record the credential and try again",
}


def wait_for(cause):
    if cause == "unavailable-transient":
        seconds = 45
        return seconds
    return 0
"""

#: THE SAME RESIDUAL, KEYED ON A NAME rather than an inline string, the tree's
#: own dominant idiom. ``TrackOutcome`` is copied from
#: ``src/cratekit/acquire/adapter.py``, a ``StrEnum`` of registry causes. Kept
#: as a fixture: a key rule that read the string and not the name holding it
#: would answer one question two ways by spelling.
RESIDUAL_ORDINARY_DATA_KEYED_ON_A_NAME = """
from enum import StrEnum


class TrackOutcome(StrEnum):
    ACQUIRED = "acquired"
    UNAVAILABLE_PERMANENT = "unavailable-permanent"
    UNAVAILABLE_TRANSIENT = "unavailable-transient"


class Reason:
    LOCK = "session-lock-held"
    STALE = "decision-stale"


CONFIG_UNUSABLE = "config-unusable"

RETRY_SECONDS = {TrackOutcome.UNAVAILABLE_TRANSIENT: 30}

DISPLAY_ORDER = {Reason.LOCK: 10, Reason.STALE: 20}

COLUMN_WIDTH = {CONFIG_UNUSABLE: 40}

PANEL = Panel(CONFIG_UNUSABLE, 40)

SLOW_DELAYS = {slug: 30 for slug in (CONFIG_UNUSABLE, Reason.STALE)}


def wait_for(cause):
    if cause == TrackOutcome.UNAVAILABLE_TRANSIENT:
        return 45
    return 0
"""

#: THE SAME CONSTRUCTS WITH THE OLD ESCAPE COMMENT ON EACH, all still reported,
#: so any per-line off switch that comes back fails here.
COMMENTED_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS = """
POLL_SECONDS = {"session-lock-held": 30, "write-lock-held": 15}  # not-a-reservation: seconds

DISPLAY_ORDER = {  # not-a-reservation: the order the causes are listed in
    "credential-missing": 10,
    "config-unusable": 20,
    "internal-error": 30,
}

COLUMN_WIDTHS = (  # not-a-reservation: characters
    ("decision-required", 40),
    ("decision-stale", 24),
)

SCHEMA_VERSIONS = {"job-schema-mismatch": 11, "review-schema-mismatch": 12}  # not-a-reservation: on-disk schema versions

RETENTION_DAYS = {"backup-facts-unreadable": 30}  # not-a-reservation: days

SHARE_PERCENT = {"library-database-missing": 50}  # not-a-reservation: percent

WEIGHTS = (  # not-a-reservation: progress weights
    ("library-volume-unmounted", 30),
    ("cloud-sync-active", 20),
)

DELAYS = {}
DELAYS["cloud-sync-unreadable"] = 30  # not-a-reservation: seconds
DELAYS.setdefault("canary-read-failed", 15)  # not-a-reservation: seconds

SLOW_DELAYS = {name: 30 for name in ("smoke-test-failed", "doctor-check-failed")}  # not-a-reservation: seconds


def wait_for(cause):
    if cause == "unavailable-transient":  # not-a-reservation: seconds
        seconds = 45
        return seconds
    return 0
"""

#: THE THREE SPELLINGS THAT MADE THE ESCAPE AN OFF SWITCH: a one line ``def``,
#: a semicolon, and one comment on a mapping's opening line. All reported now.
COMMENT_ON_A_ONE_LINE_FUNCTION = """
def build(): return {"config-unusable": 30}  # not-a-reservation: honest
"""

COMMENT_ON_TWO_STATEMENTS_AT_ONCE = """
A = {"config-unusable": 30}; B = {"credential-missing": 40}  # not-a-reservation: one reason
"""

COMMENT_ON_THE_OPENING_LINE_OF_A_TABLE = """
CODES = {  # not-a-reservation: this is not a table, honest
    "config-unusable": 30,
    "credential-missing": 40,
    "internal-error": 50,
}
"""

# ── The relative import shapes, which is how a SIBLING reaches the vocabulary ──
#
# A module in ``core`` writing ``from .exit_codes import ExitCode`` is the most
# natural spelling, and the likeliest place for a second table.

EVASION_A_SIBLING_RELATIVE_IMPORT = """
from .exit_codes import ExitCode

CODES = {"rclone-missing": ExitCode.PRECONDITION}
"""

EVASION_A_SIBLING_BOUND_AS_A_MODULE = """
from . import exit_codes

CODES = {"rclone-missing": exit_codes.ExitCode.PRECONDITION}
"""

EVASION_A_RELATIVE_IMPORT_TWO_LEVELS_UP = """
from ..core.exit_codes import ExitCode

CODES = {"rclone-missing": ExitCode.PRECONDITION}
"""

CORRECT_A_RELATIVE_IMPORT_READS_THE_TABLE = """
from . import exit_codes


def status(cause):
    return exit_codes.code_for(cause)
"""

CORRECT_A_RELATIVE_IMPORT_AND_A_MAPPING_OF_SENTENCES = """
from .exit_codes import ExitCode

MESSAGES = {"rclone-missing": "install rclone and run doctor"}


def status(cause):
    return ExitCode.PRECONDITION if cause in MESSAGES else ExitCode.OK
"""

# A level Python refuses: five dots from a three-element package walks off the
# top, where a negative slice hands back a shorter package rather than raising.

EVASION_A_RELATIVE_IMPORT_THAT_WALKS_OFF_THE_TOP = """
from .....exit_codes import ExitCode

CODES = {"rclone-missing": ExitCode.PRECONDITION}
"""

# ── The conversion spellings the unreachability residual called unreachable ──

EVASION_A_CONVERSION_THROUGH_THE_MODULE_NAME = """
from cratekit.core import exit_codes

CODES = {"rclone-missing": exit_codes.ExitCode(30)}
"""

CORRECT_A_TWO_ARGUMENT_CALL_IS_NOT_A_CONVERSION = """
from cratekit.core.exit_codes import ExitCode

CODES = {"rclone-missing": ExitCode(30, "the remote tool is missing")}
"""

EVASION_A_STATUS_WITH_A_CONVERSION_ROUND_IT = """
import sys

PRECONDITION = 30


def refuse():
    sys.exit(int(PRECONDITION))
"""

# ── A branch table one indent deeper ────────────────────────────────────────
#
# Checking something else before answering is how a table's second case gets written.

EVASION_A_BRANCH_ONE_INDENT_DEEPER = DECLARES_ITS_CAUSES + """
def status(cause, ready):
    if cause == "tagger-art-rejected":
        if ready:
            return 30
    return 1
"""

EVASION_A_BRANCH_INSIDE_A_LOOP = DECLARES_ITS_CAUSES + """
def status(cause, attempts):
    if cause == "tagger-source-unreadable":
        for _ in attempts:
            return 41
    return 1
"""

CORRECT_A_HELPER_INSIDE_A_BRANCH_HAS_ITS_OWN_RETURN = """
def render(cause):
    if cause == "rekordbox-running":
        def column_width():
            return 30

        return "quit rekordbox".ljust(column_width())
    return ""
"""

MUTUALLY_RECURSIVE_CONSTANTS = """
A = B
B = A

CODES = {"rekordbox-running": A}
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

EVASION_EXIT_IMPORTED_AS_A_SYMBOL = """
from sys import exit

def refuse():
    exit(30)
"""

EVASION_EXIT_IMPORTED_UNDER_ANOTHER_NAME = """
from sys import exit as leave

def refuse():
    leave(30)
"""

EVASION_THE_UNDERLYING_EXIT = """
from os import _exit

def refuse():
    _exit(30)
"""

EVASION_AN_EXIT_HELD_IN_A_VARIABLE = """
import sys

def refuse():
    stop = sys.exit
    stop(30)
"""

EVASION_THE_EXCEPTION_UNDER_ANOTHER_NAME = """
Stop = SystemExit

def refuse():
    raise Stop(30)
"""

EVASION_A_SUBCLASS_OF_THE_EXCEPTION = """
class Refusal(SystemExit):
    pass

def refuse():
    raise Refusal(30)
"""

EVASION_EXIT_FETCHED_BY_GETATTR = """
import sys

def refuse():
    getattr(sys, "exit")(30)
"""

EVASION_A_FETCHED_EXIT_HELD_IN_A_NAME = """
import sys

_LEAVE = getattr(sys, "exit")

def refuse():
    _LEAVE(30)
"""

EVASION_THE_MODULE_REBOUND = """
import sys

system = sys

def refuse():
    system.exit(30)
"""

EVASION_THE_MODULE_IMPORTED_BY_NAME = """
import importlib

def refuse():
    importlib.import_module("sys").exit(30)
"""

EVASION_THE_MODULE_REACHED_THROUGH_ANOTHER = """
import os

def refuse():
    os.sys.exit(30)
"""

EVASION_THE_EXCEPTION_THROUGH_BUILTINS = """
import builtins

def refuse():
    raise builtins.SystemExit(30)
"""

EVASION_A_STATUS_HELD_IN_A_CONSTANT = """
import sys

PRECONDITION = 30

def refuse():
    sys.exit(PRECONDITION)
"""

EVASION_A_STATUS_ASSIGNED_THEN_EXITED = """
import sys

def refuse():
    code = 41
    sys.exit(code)
"""

CORRECT_A_PARAMETER_SHADOWS_A_CONSTANT = """
import sys

STATUS = 30

def refuse(STATUS):
    sys.exit(STATUS)
"""

CORRECT_A_PARAMETER_SHADOWS_AN_EXIT = """
import sys

stop = sys.exit

def drive(stop):
    stop(30)
"""

CORRECT_GETATTR_ON_SOMEBODY_ELSE = """
class Runner:
    def exit(self, code):
        return code

def drive(runner):
    getattr(runner, "exit")(21)
"""

CORRECT_EXITS_THROUGH_A_SYMBOL_IMPORT = """
from sys import exit

from cratekit.cli.exit_codes import code_for

def main(cause):
    exit(int(code_for(cause)))
"""

CORRECT_RAISES_A_STATUS_IT_LOOKED_UP = """
from cratekit.cli.exit_codes import code_for

def main(cause):
    raise SystemExit(int(code_for(cause)))
"""

CORRECT_RAISES_A_STATUS_IT_WAS_GIVEN = """
def main(status):
    raise SystemExit(status)
"""

# ── A NEGATIVE STATUS ──────────────────────────────────────────────────────
#
# The shell and ``subprocess.returncode`` read a negative status differently,
# and ``cli/exit_codes.py`` reserves nothing negative.

# ── Four binding shapes ProcessExits handles, each found unwatched by a mutation table ──

#: The fixed point matters here: ``_walk_scope`` yields a scope's statements in
#: reverse, so a chain in dependency order, ``later = sys.exit`` then
#: ``stop = later``, reaches the binder backwards and needs the second pass.
EVASION_AN_EXIT_ALIASED_A_SECOND_TIME = """
import sys

later = sys.exit
stop = later

def refuse():
    stop(30)
"""

#: ``importlib.import_module`` held in a NAME, which the binding walk records as
#: an importer.
EVASION_AN_IMPORTER_HELD_IN_A_NAME = """
import importlib

load = importlib.import_module

def refuse():
    load("sys").exit(30)
"""

EVASION_THE_EXCEPTION_IMPORTED_FROM_BUILTINS = """
from builtins import SystemExit as Stop

def refuse():
    raise Stop(30)
"""

EVASION_A_TRACKED_MODULE_IMPORTED_AS_A_SYMBOL = """
from os import sys

def refuse():
    sys.exit(30)
"""

#: TWO ARGUMENTS IS NOT A STATUS. ``SystemExit(30, "detail")`` sets ``code`` to
#: the tuple and exits 1, so "status 30" would be a status never returned.
CORRECT_A_TWO_ARGUMENT_SYSTEMEXIT_IS_NOT_A_STATUS = """
def refuse():
    raise SystemExit(30, "the detail")
"""

EVASION_A_NEGATIVE_STATUS = """
import sys

def refuse():
    sys.exit(-1)
"""

EVASION_A_NEGATIVE_STATUS_HELD_IN_A_CONSTANT = """
import sys

TERMINATED = 15

def refuse():
    sys.exit(-TERMINATED)
"""

EVASION_A_NEGATIVE_STATUS_RAISED = """
def refuse():
    raise SystemExit(-1)
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
        CORRECT_A_RETRY_FLAG_PER_CAUSE,
        CORRECT_A_BACKOFF_PER_CAUSE,
        CORRECT_A_DISPLAY_ORDER_PER_REMEDY,
        CORRECT_AN_ATTEMPT_BUDGET,
        CORRECT_A_SEVERITY_RANKING,
        CORRECT_A_COUNTER,
        CORRECT_A_BRANCH_THAT_WAITS,
        CORRECT_LOGGING_LEVELS,
        CORRECT_COLUMN_WIDTHS,
        CORRECT_TIMEOUTS_AND_BUDGETS,
        CORRECT_A_THRESHOLD_AND_A_VERSION,
        CORRECT_A_FUNCTION_RETURNING_A_WIDTH,
        CORRECT_A_PROGRESS_WEIGHT_PER_STEP,
        CORRECT_A_RELATIVE_IMPORT_READS_THE_TABLE,
        CORRECT_A_RELATIVE_IMPORT_AND_A_MAPPING_OF_SENTENCES,
        CORRECT_A_HELPER_INSIDE_A_BRANCH_HAS_ITS_OWN_RETURN,
    ],
)
def test_the_second_table_guard_stays_silent_on_correct_code(source):
    """P7: silent on correct code, aliased imports, own data and small integers on remedy tokens."""
    assert reserved_code_tables(source, CAUSES, RANGE) == []


@pytest.mark.parametrize(
    "source",
    [
        EVASION_BARE_INTEGER_TABLE,
        EVASION_ALIASED_MODULE_IMPORT,
        EVASION_ALIASED_CLASS_IMPORT,
        EVASION_FROM_THE_PACKAGE,
        EVASION_KEYWORD_EXPANSION,
        EVASION_A_READ_ONLY_WRAPPER,
        EVASION_AN_UPDATE,
        EVASION_AN_IMPLICITLY_CONCATENATED_KEY,
    ],
)
def test_the_second_table_guard_bites_every_shape_of_second_opinion(source):
    """Including the two aliased shapes, which is what defeated the armed guards once."""
    assert reserved_code_tables(source, CAUSES, RANGE)


@pytest.mark.parametrize(
    "source",
    [
        EVASION_A_NEW_MODULE_DECIDES_ITS_OWN_CODES,
        EVASION_A_TUPLE_OF_PAIRS,
        EVASION_A_COMPREHENSION_OVER_PAIRS,
        EVASION_A_COMPREHENSION_OVER_SLUGS,
        EVASION_ZIPPED_FROM_TWO_SEQUENCES,
        EVASION_FILLED_A_KEY_AT_A_TIME,
        EVASION_AN_ORDERED_DICT,
        EVASION_SETDEFAULT,
        EVASION_A_MATCH_STATEMENT,
        EVASION_AN_IF_CHAIN,
        EVASION_A_CODE_WITH_A_CONVERSION_ROUND_IT,
        EVASION_A_CODE_HELD_IN_A_CONSTANT,
        EVASION_A_CODE_HELD_ON_A_CLASS,
        EVASION_A_CODE_IN_THE_MODULES_OWN_ENUM,
        EVASION_A_CODE_REACHED_BY_ARITHMETIC,
        EVASION_A_CODE_ASSIGNED_THEN_RETURNED,
        EVASION_A_TUPLE_LONGER_THAN_A_PAIR,
        EVASION_A_TUPLE_OF_DATACLASSES,
        EVASION_A_TABLE_KEYED_BY_KEYWORD,
        EVASION_A_BRANCH_ONE_INDENT_DEEPER,
        EVASION_A_BRANCH_INSIDE_A_LOOP,
    ],
)
def test_the_second_table_guard_bites_a_module_reserving_causes_of_its_own(source):
    """A module deciding codes for causes nobody has reserved, in eleven ordinary shapes."""
    assert reserved_code_tables(source, CAUSES, RANGE)


def test_an_enum_is_recognized_by_its_base_and_each_clause_has_its_own_case():
    """An enum is recognized by what the source bound its base to, or by the base's spelling.

    ``from enum import StrEnum as Vocabulary`` is answered only by the import
    clause; ``class Refusal(CratekitEnum)`` against our own base only by the
    spelling clause. A plain class of string constants is not a declaration (P7).
    """
    assert reserved_code_tables(
        DECLARES_ITS_CAUSES_ON_AN_ALIASED_BASE, CAUSES, RANGE
    ) == ["line 9: 'tagger-art-rejected' -> status 41"], (
        "an enum whose base is imported under another name declares its causes "
        "exactly as the unaliased spelling does, or one `as` keyword decides "
        "whether the guard can see a module's whole vocabulary"
    )
    assert reserved_code_tables(
        DECLARES_ITS_CAUSES_ON_A_BASE_OF_OUR_OWN, CAUSES, RANGE
    ) == ["line 9: 'tagger-art-rejected' -> status 41"], (
        "a base named in another of our modules is the shape the spelling clause "
        "exists for, and narrowing that clause to the three names the enum "
        "module exports silences it"
    )
    assert reserved_code_tables(
        DECLARES_ITS_CAUSES_THROUGH_THE_ENUM_MODULE, CAUSES, RANGE
    ) == ["line 9: 'tagger-art-rejected' -> status 41"], (
        "the module-qualified spelling is answered by the SPELLING clause, "
        "because the last dotted part of `vocabularies.StrEnum` ends in Enum. "
        "It is here as the control that says so, not as the import clause's case"
    )
    assert reserved_code_tables(
        CORRECT_A_PLAIN_CLASS_DECLARES_NOTHING, CAUSES, RANGE
    ) == [], (
        "a plain class holding strings is not a vocabulary, and reading one as a "
        "declaration would let any module invent a cause by writing a constant"
    )


def test_renaming_the_enum_or_the_name_holding_it_changes_nothing():
    """Renaming the enum, its base alias or the name holding it changes nothing."""
    original = reserved_code_tables(DECLARES_ITS_CAUSES_ON_AN_ALIASED_BASE, CAUSES, RANGE)
    assert original, "the fixture stopped reporting, so the renames below prove nothing"

    for before, after in (
        ("class Refusal(", "class SomethingElseEntirely("),
        ("CODES = {", "TABLE = {"),
        ("ART_REJECTED", "WHATEVER"),
        ("Vocabulary", "Anything"),
    ):
        renamed = DECLARES_ITS_CAUSES_ON_AN_ALIASED_BASE.replace(before, after)
        assert renamed != DECLARES_ITS_CAUSES_ON_AN_ALIASED_BASE, (
            f"{before!r} is not in the fixture any more, so this rename renamed "
            f"nothing and the assertion below would pass over an unchanged source"
        )
        # The base alias is spelled twice, so renaming it means renaming both or the
        # fixture stops being valid Python.
        assert (
            reserved_code_tables(renamed, CAUSES, RANGE) == original
        ), f"renaming {before!r} changed what the guard reports"


@pytest.mark.parametrize(
    "source",
    [
        EVASION_A_SIBLING_RELATIVE_IMPORT,
        EVASION_A_SIBLING_BOUND_AS_A_MODULE,
        EVASION_A_RELATIVE_IMPORT_TWO_LEVELS_UP,
    ],
)
def test_the_second_table_guard_reads_every_relative_import_shape(source):
    """``from .exit_codes import ExitCode`` and ``from . import exit_codes`` are read too."""
    assert reserved_code_tables(source, CAUSES, RANGE)


def test_a_relative_import_is_resolved_against_the_package_the_file_sits_in():
    """A relative import resolves against its own package: from . import exit_codes in cli."""
    assert reserved_code_tables(
        EVASION_A_SIBLING_RELATIVE_IMPORT, CAUSES, RANGE, "cratekit.core"
    ) == ["line 4: 'rclone-missing' -> ExitCode.PRECONDITION"]
    assert (
        reserved_code_tables(
            EVASION_A_SIBLING_RELATIVE_IMPORT, CAUSES, RANGE, "cratekit.cli"
        )
        == []
    )
    assert reserved_code_tables(
        EVASION_A_RELATIVE_IMPORT_TWO_LEVELS_UP, CAUSES, RANGE, "cratekit.modules"
    )
    assert (
        reserved_code_tables(
            EVASION_A_RELATIVE_IMPORT_TWO_LEVELS_UP, CAUSES, RANGE, "cratekit"
        )
        == []
    ), (
        "two dots from the top package walks off it, so Python imports nothing "
        "either. This does NOT prove the off the top clause: with the clause "
        "removed the negative slice leaves a base that matches nothing here "
        "either, so it stays silent for the wrong reason. The test below is the "
        "one that proves it"
    )


def test_a_relative_import_that_walks_off_the_top_names_nothing():
    """A relative import walking off the top names nothing, in the resolver and in the guard.

    The base slice goes negative and Python hands back a shorter package, so
    without the check five dots from ``cratekit.core.sub`` would resolve onto
    ``cratekit.core`` and report a module that cannot import.
    """
    off_the_top = [
        ("cratekit.core.sub", 4),
        ("cratekit.core.sub", 5),
        ("cratekit.core", 3),
        ("cratekit", 2),
    ]
    for package, level in off_the_top:
        node = ast.ImportFrom(module="exit_codes", names=[], level=level)
        assert _guards._relative_module(node, package) is None, (
            f"{level} dots from {package} walks off the top of the tree, which "
            f"Python refuses to import, so it names no module here either"
        )

    node = ast.ImportFrom(module="exit_codes", names=[], level=5)
    parts = "cratekit.core.sub".split(".")
    assert parts[: len(parts) - (node.level - 1)] == ["cratekit", "core"], (
        "the negative slice is what makes this dangerous rather than merely "
        "wrong, and if Python ever stops silently shortening the base here the "
        "clause is no longer load bearing and this test should say so"
    )
    assert (
        reserved_code_tables(
            EVASION_A_RELATIVE_IMPORT_THAT_WALKS_OFF_THE_TOP,
            CAUSES,
            RANGE,
            "cratekit.core.sub",
        )
        == []
    ), (
        "an import Python refuses resolved onto the vocabulary module, so the "
        "guard reports a second reservation table in a module that cannot even "
        "be imported"
    )


def test_a_boolean_is_not_an_integer_here():
    """A boolean is not an integer here; the first entry of the residual
    "One check in this unit is unreachable".
    """
    assert _guards.resolve_int(ast.parse("True").body[0].value, {}, {}) is None
    assert _guards.resolve_int(ast.parse("False").body[0].value, {}, {}) is None
    assert _guards.resolve_int(ast.parse("30").body[0].value, {}, {}) == 30
    assert reserved_code_tables(CORRECT_A_RETRY_FLAG_PER_CAUSE, CAUSES, RANGE) == []


def test_a_conversion_is_read_through_the_module_name_as_well_as_the_class_name():
    """``exit_codes.ExitCode(30)`` is a conversion too; the fourth entry of the residual
    "One check in this unit is unreachable".
    """
    assert reserved_code_tables(
        EVASION_A_CONVERSION_THROUGH_THE_MODULE_NAME, CAUSES, RANGE
    ) == ["line 4: 'rclone-missing' -> exit_codes.ExitCode(30)"]


def test_a_two_argument_call_is_not_a_conversion():
    """A call taking a code and a sentence is a constructor, not a conversion (P7).

    The third entry of the residual "One check in this unit is unreachable":
    dropping ``len(node.args) == 1`` reports this fixture.
    """
    assert (
        reserved_code_tables(CORRECT_A_TWO_ARGUMENT_CALL_IS_NOT_A_CONVERSION, CAUSES, RANGE)
        == []
    )


def test_a_status_with_a_conversion_round_it_still_reaches_the_shell():
    """``sys.exit(int(PRECONDITION))`` exits 30 as ``sys.exit(30)`` does, and is reported.

    The second entry of the residual "One check in this unit is unreachable".
    """
    assert process_status_literals(EVASION_A_STATUS_WITH_A_CONVERSION_ROUND_IT) == [
        "line 8: sys.exit(int(PRECONDITION)) (status 30)"
    ]


def test_the_derivation_refuses_to_answer_from_an_incomplete_walk():
    """Handed a short walk, the derivation refuses rather than answer.

    The sixth entry of the residual "One check in this unit is unreachable".
    """
    with pytest.MonkeyPatch.context() as short_walk:
        short_walk.setitem(
            globals(),
            "imported_package_modules",
            lambda: ([], {"cratekit.modules.tools.backup": "No module named 'boto3'"}),
        )
        with pytest.raises(AssertionError, match="invisible to the completeness"):
            structured_refusal_causes()
    assert structured_refusal_causes(), "the walk did not come back after the swap"


def test_the_guard_bites_through_the_derivation_when_the_file_declares_nothing():
    """With the local enum stripped, the guard still bites through the package-wide derivation."""
    source = EVASION_A_NEW_MODULE_DECIDES_ITS_OWN_CODES.replace(DECLARES_ITS_CAUSES, "")
    assert "Refusal" not in source
    assert reserved_code_tables(source, CAUSES, RANGE) == []
    elsewhere = CAUSES | frozenset({"tagger-source-unreadable", "tagger-art-rejected"})
    assert reserved_code_tables(source, elsewhere, RANGE)


def test_a_mutually_recursive_pair_of_constants_resolves_to_nothing():
    """A mutually recursive pair of constants resolves to nothing rather than raising.

    This is ``MAX_HOPS``'s ceiling, which bounds the walk so ``A = B`` beside
    ``B = A`` cannot hang the suite with a ``RecursionError``.
    """
    tree = ast.parse("A = B\nB = A\n")
    names = _guards._module_level_literals(tree)
    assert set(names) == {"A", "B"}
    assert _guards.resolve_int(names["A"], names, {}) is None
    assert _guards.resolve_int(names["B"], names, {}) is None
    assert _guards.MAX_HOPS < sys.getrecursionlimit(), (
        "the bound is above the interpreter's own, so the pair above raises "
        "RecursionError instead of resolving to nothing and the suite dies "
        "rather than the guard staying silent"
    )
    assert reserved_code_tables(MUTUALLY_RECURSIVE_CONSTANTS, CAUSES, RANGE) == []


def test_the_residual_is_pinned_rather_than_discovered():
    """Once a string IS a cause, a duration in range reads as a status, reported on purpose.

    Matching on the variable's name instead would be a guard a rename defeats.
    """
    hits = reserved_code_tables(RESIDUAL_A_BACKOFF_ON_A_REAL_CAUSE, CAUSES, RANGE)
    assert hits == ["line 2: 'rekordbox-running' -> status 30"]


#: Every shape a module would plausibly use to give a registry-only slug a code
#: of its own. See the residual
#: "The tiers were bought with a number that does not exist".
REGISTRY_SLUG_SECOND_TABLES = (
    EVASION_A_NAMED_CODE_FOR_A_REGISTRY_SLUG,
    EVASION_A_CONVERSION_ON_A_REGISTRY_SLUG,
    EVASION_A_CONSTRUCTOR_ON_A_REGISTRY_SLUG,
    EVASION_A_CONSTRUCTOR_THROUGH_THE_MODULE_ON_A_REGISTRY_SLUG,
    EVASION_ITS_OWN_ENUM_FOR_A_REGISTRY_SLUG,
    EVASION_A_NAMED_CONSTANT_FOR_A_REGISTRY_SLUG,
    EVASION_ARITHMETIC_FOR_A_REGISTRY_SLUG,
    EVASION_AN_INVENTED_CODE_FOR_A_REGISTRY_SLUG,
    EVASION_A_BARE_CODE_FOR_A_REGISTRY_SLUG,
    EVASION_A_REGISTRY_SLUG_TABLE_AS_A_TUPLE,
    EVASION_A_REGISTRY_SLUG_TABLE_FILLED_A_KEY_AT_A_TIME,
    EVASION_A_REGISTRY_SLUG_TABLE_BY_COMPREHENSION,
    EVASION_A_REGISTRY_SLUG_TABLE_ZIPPED,
    EVASION_A_REGISTRY_SLUG_IF_CHAIN,
    EVASION_A_REGISTRY_SLUG_MATCH_STATEMENT,
    EVASION_A_REGISTRY_SLUG_CODE_HELD_ON_A_CLASS,
)


@pytest.mark.parametrize("source", REGISTRY_SLUG_SECOND_TABLES)
def test_the_wide_key_set_reports_what_the_tiers_missed(source):
    """The sixteen shapes the tiered key set of round four left silent, all reported now.

    Measured by re-implementing that gate over this tuple: it reported two. See
    the residual "The tiers were bought with a number that does not exist".
    """
    assert reserved_code_tables(source, declared_causes(), RANGE)


def test_the_alternative_is_not_rejected_for_a_flaw_this_scheme_shares():
    """The input that rejected narrowing to the live integers is reported by this scheme."""
    assert "tree-registry-unusable" in registry_only_causes()
    assert 33 not in {int(code) for code in ExitCode}
    assert reserved_code_tables(
        EVASION_AN_INVENTED_CODE_FOR_A_REGISTRY_SLUG, declared_causes(), RANGE
    ) == ["line 2: 'tree-registry-unusable' -> status 33"]


@pytest.mark.parametrize(
    "source",
    [
        EVASION_A_VOCABULARY_MEMBER_HELD_IN_A_CONSTANT,
        EVASION_A_VOCABULARY_MEMBER_ASSIGNED_THEN_RETURNED,
    ],
)
def test_a_vocabulary_member_held_in_a_name_is_still_a_code(source):
    """``CODE = ExitCode.PRECONDITION`` beside ``{"rclone-missing": CODE}`` is a code."""
    assert reserved_code_tables(source, CAUSES, RANGE)


def test_the_reported_text_keeps_both_spellings_of_a_code_reached_by_name():
    """A hit a reader can chase needs the name AND what it held."""
    assert reserved_code_tables(
        EVASION_A_VOCABULARY_MEMBER_HELD_IN_A_CONSTANT, CAUSES, RANGE
    ) == ["line 6: 'rclone-missing' -> ExitCode.PRECONDITION as CODE"]


#: THE KEY SIDE OF THE SAME QUESTION: a cause held in a module constant or a
#: class attribute, the tree's own idiom.
EVASION_A_KEY_HELD_IN_A_MODULE_CONSTANT = """
from cratekit.core.exit_codes import ExitCode

CONFIG_UNUSABLE = "config-unusable"
CODES = {CONFIG_UNUSABLE: 30}
"""

EVASION_A_KEY_HELD_ON_A_CLASS = """
class Slug:
    CONFIG_UNUSABLE = "config-unusable"


CODES = {Slug.CONFIG_UNUSABLE: 30}
"""

#: A name that is NOT a cause stays not a cause.
CORRECT_A_KEY_HELD_IN_A_CONSTANT_THAT_IS_NOT_A_CAUSE = """
COLUMN = "column-width"
WIDTHS = {COLUMN: 40}
"""

#: The record written as a mapping, the dict spelling of the house style.
EVASION_A_LIST_OF_RECORD_DICTS = """
RESERVATIONS = [
    {"cause": "config-unusable", "code": 30},
    {"cause": "credential-missing", "code": 40},
]
"""

#: The vocabulary reached by a string, ``getattr``.
EVASION_A_CODE_FETCHED_BY_GETATTR = """
from cratekit.core.exit_codes import ExitCode

CODES = {"config-unusable": getattr(ExitCode, "PRECONDITION")}
"""

CORRECT_GETATTR_FOR_A_CODE_ON_SOMEBODY_ELSE = """
import settings

CODES = {"config-unusable": getattr(settings, "PRECONDITION")}
"""

#: ``//`` and ``%``, read as ``+``, ``-`` and ``*`` are.
EVASION_A_CODE_REACHED_BY_FLOOR_DIVISION = """
BASE = 60
CODES = {"config-unusable": BASE // 2}
"""

EVASION_A_CODE_REACHED_BY_A_REMAINDER = """
BASE = 130
CODES = {"config-unusable": BASE % 100}
"""

#: SUBTRACTION AND MULTIPLICATION, in range, each limb driven by a reported case.
EVASION_A_CODE_REACHED_BY_SUBTRACTION = """
BASE = 71
CODES = {"config-unusable": BASE - 41}
"""

EVASION_A_CODE_REACHED_BY_MULTIPLICATION = """
BASE = 15
CODES = {"config-unusable": BASE * 2}
"""

#: A DIVISION THAT DOES NOT RUN resolves to nothing; without ``right != 0`` the
#: walk raises ``ZeroDivisionError``.
CORRECT_A_DIVISION_BY_ZERO_RESOLVES_TO_NOTHING = """
BASE = 60
CODES = {"config-unusable": BASE // 0}
"""

#: A CODE HELD IN AN ANNOTATED CONSTANT, the house style of
#: ``REASONS: Mapping[str, ExitCode] = MappingProxyType(``.
EVASION_A_CODE_HELD_IN_AN_ANNOTATED_CONSTANT = """
PRECONDITION: int = 30

CODES = {"config-unusable": PRECONDITION}
"""

EVASION_A_CODE_HELD_ON_AN_ANNOTATED_CLASS_ATTRIBUTE = """
class Status:
    PRECONDITION: int = 30


CODES = {"config-unusable": Status.PRECONDITION}
"""

#: AN ANNOTATED ENUM MEMBER, a member exactly as the unannotated spelling is.
EVASION_AN_ANNOTATED_ENUM_MEMBER_IS_A_DECLARATION = """
from enum import StrEnum


class Refusal(StrEnum):
    ART_REJECTED: str = "tagger-art-rejected"


CODES = {"tagger-art-rejected": 41}
"""

#: A KEY held three aliases deep, at the key side's own bound.
A_KEY_CHAIN_THE_HOP_BOUND_READS = """
S0 = "config-unusable"
S1 = S0

CODES = {S1: 30}
"""

A_KEY_CHAIN_THE_HOP_BOUND_GIVES_UP = """
S0 = "config-unusable"
S1 = S0
S2 = S1
S3 = S2

CODES = {S3: 30}
"""

#: A duplicate key inside a SECOND table is reported once, so the count is right.
EVASION_A_DUPLICATE_KEY_IN_A_SECOND_TABLE = """
CODES = {"config-unusable": 30, "config-unusable": 30}
"""

#: What ``MAX_HOPS`` at three buys and gives up: two aliases resolve and three
#: do not. Both pinned.
A_CHAIN_THE_HOP_BOUND_READS = """
A0 = 30
A1 = A0
CODES = {"config-unusable": A1}
"""

A_CHAIN_THE_HOP_BOUND_GIVES_UP = """
A0 = 30
A1 = A0
A2 = A1
A3 = A2
CODES = {"config-unusable": A3}
"""

# ── The two constructs the key widening reached past ────────────────────────
#
# The ``if`` arm of ``_branches`` and a dict comprehension's iterable each
# filtered to ``ast.Constant`` before asking ``cause_key``. The pairs below are
# kept together: a spelling that goes quiet alone is this shape coming back.

EVASION_A_BRANCH_COMPARING_AGAINST_A_CLASS_ATTRIBUTE = """
class Slug:
    CONFIG_UNUSABLE = "config-unusable"


def code(cause):
    if cause == Slug.CONFIG_UNUSABLE:
        return 30
    return 0
"""

EVASION_A_BRANCH_COMPARING_AGAINST_A_MODULE_CONSTANT = """
CONFIG_UNUSABLE = "config-unusable"


def code(cause):
    if cause == CONFIG_UNUSABLE:
        return 30
    return 0
"""

#: The direct twin of the first one, which was reported.
EVASION_A_MATCH_AGAINST_A_CLASS_ATTRIBUTE = """
class Slug:
    CONFIG_UNUSABLE = "config-unusable"


def code(cause):
    match cause:
        case Slug.CONFIG_UNUSABLE:
            return 30
    return 0
"""

#: The literal spelling, the control that the branch machinery is live.
CONTROL_A_BRANCH_COMPARING_AGAINST_A_LITERAL = """
def code(cause):
    if cause == "config-unusable":
        return 30
    return 0
"""

EVASION_A_COMPREHENSION_OVER_NAMED_SLUGS = """
CONFIG_UNUSABLE = "config-unusable"
SMOKE_TEST_FAILED = "smoke-test-failed"
CODES = {slug: 30 for slug in (CONFIG_UNUSABLE, SMOKE_TEST_FAILED)}
"""

CONTROL_A_COMPREHENSION_OVER_LITERAL_SLUGS = """
CODES = {slug: 30 for slug in ("config-unusable", "smoke-test-failed")}
"""

# ── The vocabulary at a value the reserved range does not cover ─────────────
#
# ``ExitCode.SUCCESS`` and ``ExitCode(0)`` are one code, so both are reported.

EVASION_A_CONSTRUCTOR_ON_A_CODE_BELOW_THE_RANGE = """
from cratekit.core.exit_codes import ExitCode

CODES = {"config-unusable": ExitCode(0)}
"""

EVASION_A_CONSTRUCTOR_ON_A_CODE_ABOVE_THE_RANGE = """
from cratekit.core.exit_codes import ExitCode

CODES = {"config-unusable": ExitCode(126)}
"""

#: The narrowing that keeps the widening off ordinary code: ``cli/output.py``
#: reads a recorded status back like this and reserves nothing.
CORRECT_A_CONSTRUCTOR_ON_A_RUNTIME_VALUE = """
from cratekit.core.exit_codes import ExitCode


def read(document):
    return {"config-unusable": ExitCode(document["exit_code"])}
"""

#: An INTEGER out of range, reached three ways, silent by the range decision.
RESIDUAL_A_BARE_INTEGER_OUT_OF_RANGE = """
CODES = {"config-unusable": 5}
"""

RESIDUAL_A_NAMED_CONSTANT_OUT_OF_RANGE = """
BASE = 70
CODES = {"config-unusable": BASE}
"""

RESIDUAL_ARITHMETIC_OUT_OF_RANGE = """
BASE = 35
CODES = {"config-unusable": BASE * 2}
"""


@pytest.mark.parametrize(
    "source,line",
    [
        (EVASION_A_KEY_HELD_IN_A_MODULE_CONSTANT, 5),
        (EVASION_A_KEY_HELD_ON_A_CLASS, 6),
    ],
)
def test_a_key_held_in_a_name_is_still_a_cause(source, line):
    """A key held in a name or a class attribute is a cause, as a value held in one is a code."""
    assert reserved_code_tables(source, declared_causes(), RANGE) == [
        f"line {line}: 'config-unusable' -> status 30"
    ]


@pytest.mark.parametrize(
    "source,line",
    [
        (EVASION_A_BRANCH_COMPARING_AGAINST_A_CLASS_ATTRIBUTE, 7),
        (EVASION_A_BRANCH_COMPARING_AGAINST_A_MODULE_CONSTANT, 6),
        (EVASION_A_MATCH_AGAINST_A_CLASS_ATTRIBUTE, 8),
        (CONTROL_A_BRANCH_COMPARING_AGAINST_A_LITERAL, 3),
    ],
)
def test_a_branch_table_reads_its_key_the_same_way_whichever_branch_it_is(source, line):
    """A branch table reads its key alike in the ``match`` arm and the ``if`` arm."""
    assert reserved_code_tables(source, declared_causes(), RANGE) == [
        f"line {line}: 'config-unusable' -> status 30"
    ]


@pytest.mark.parametrize(
    "source,line",
    [
        (EVASION_A_COMPREHENSION_OVER_NAMED_SLUGS, 4),
        (CONTROL_A_COMPREHENSION_OVER_LITERAL_SLUGS, 2),
    ],
)
def test_a_comprehension_reads_named_slugs_and_inlined_slugs_alike(source, line):
    """A comprehension over named slugs reads them as one over inlined slugs does."""
    assert reserved_code_tables(source, declared_causes(), RANGE) == [
        f"line {line}: 'config-unusable' -> status 30",
        f"line {line}: 'smoke-test-failed' -> status 30",
    ]


@pytest.mark.parametrize(
    "source,spelled",
    [
        (EVASION_A_CONSTRUCTOR_ON_A_CODE_BELOW_THE_RANGE, "ExitCode(0)"),
        (EVASION_A_CONSTRUCTOR_ON_A_CODE_ABOVE_THE_RANGE, "ExitCode(126)"),
    ],
)
def test_a_constructor_on_the_vocabulary_is_a_code_at_any_value(source, spelled):
    """A constructor on the vocabulary is a code at any value; the range gates integers only."""
    assert reserved_code_tables(source, declared_causes(), RANGE) == [
        f"line 4: 'config-unusable' -> {spelled}"
    ]


def test_a_constructor_wrapping_a_runtime_value_reserves_nothing():
    """A one-argument call on the vocabulary reserves only when its argument resolves (P7)."""
    assert (
        reserved_code_tables(
            CORRECT_A_CONSTRUCTOR_ON_A_RUNTIME_VALUE, declared_causes(), RANGE
        )
        == []
    )


@pytest.mark.parametrize(
    "source",
    [
        RESIDUAL_A_BARE_INTEGER_OUT_OF_RANGE,
        RESIDUAL_A_NAMED_CONSTANT_OUT_OF_RANGE,
        RESIDUAL_ARITHMETIC_OUT_OF_RANGE,
    ],
)
def test_an_integer_outside_the_reserved_range_is_silent_however_it_is_spelled(source):
    """An integer outside the reserved range is silent, spelled as a constant or arithmetic.

    Widening past the range would report every count, width and percent in the
    package. The residual "The tiers were bought with a number that does not exist"
    once described this rule wrongly; this drives it at its boundary.
    """
    assert reserved_code_tables(source, declared_causes(), RANGE) == []


def test_resolving_the_key_widens_what_is_read_and_not_what_is_a_cause():
    """A name resolving to an undeclared string answers as the undeclared literal does."""
    assert reserved_code_tables(
        CORRECT_A_KEY_HELD_IN_A_CONSTANT_THAT_IS_NOT_A_CAUSE, declared_causes(), RANGE
    ) == []
    assert "column-width" not in declared_causes()


def test_a_record_written_as_a_mapping_is_still_a_record():
    """A record written ``{"cause": ..., "code": ...}`` is read as the tuple and constructor are."""
    assert reserved_code_tables(
        EVASION_A_LIST_OF_RECORD_DICTS, declared_causes(), RANGE
    ) == [
        "line 3: 'config-unusable' -> status 30",
        "line 4: 'credential-missing' -> status 40",
    ]


def test_a_code_fetched_by_getattr_is_still_a_code():
    """``getattr`` on the imported vocabulary is a code, as ``getattr(sys, "exit")`` is an exit.

    Narrowed to the class this source imported.
    """
    assert reserved_code_tables(
        EVASION_A_CODE_FETCHED_BY_GETATTR, declared_causes(), RANGE
    ) == ["line 4: 'config-unusable' -> getattr(ExitCode, 'PRECONDITION')"]
    assert reserved_code_tables(
        CORRECT_GETATTR_FOR_A_CODE_ON_SOMEBODY_ELSE, declared_causes(), RANGE
    ) == []


@pytest.mark.parametrize(
    "source,spelled",
    [
        (EVASION_A_CODE_REACHED_BY_FLOOR_DIVISION, "BASE // 2"),
        (EVASION_A_CODE_REACHED_BY_A_REMAINDER, "BASE % 100"),
        (EVASION_A_CODE_REACHED_BY_SUBTRACTION, "BASE - 41"),
        (EVASION_A_CODE_REACHED_BY_MULTIPLICATION, "BASE * 2"),
    ],
)
def test_the_arithmetic_the_resolver_reads_is_the_whole_set(source, spelled):
    """All five arithmetic operators resolve, each limb driven by a reported case."""
    assert reserved_code_tables(source, declared_causes(), RANGE) == [
        f"line 3: 'config-unusable' -> status 30 as {spelled}"
    ]


def test_a_zip_of_one_sequence_is_not_a_pair_of_sequences():
    """``dict(zip(SLUGS))`` is ordinary Python and does not raise ``IndexError`` out of the walk."""
    assert reserved_code_tables(CORRECT_A_ZIP_OF_ONE_SEQUENCE, CAUSES, RANGE) == []


def test_a_division_by_zero_resolves_to_nothing_rather_than_raising():
    """A division by zero resolves to nothing rather than raising ``ZeroDivisionError``."""
    assert reserved_code_tables(
        CORRECT_A_DIVISION_BY_ZERO_RESOLVES_TO_NOTHING, declared_causes(), RANGE
    ) == []


def test_the_house_style_of_an_annotated_assignment_is_read_on_both_sides():
    """``NAME: type = value``, the house way of writing a table, read by all three collectors."""
    assert reserved_code_tables(
        EVASION_A_CODE_HELD_IN_AN_ANNOTATED_CONSTANT, declared_causes(), RANGE
    ) == ["line 4: 'config-unusable' -> status 30 as PRECONDITION"]
    assert reserved_code_tables(
        EVASION_A_CODE_HELD_ON_AN_ANNOTATED_CLASS_ATTRIBUTE, declared_causes(), RANGE
    ) == ["line 6: 'config-unusable' -> status 30 as Status.PRECONDITION"]
    assert reserved_code_tables(
        EVASION_AN_ANNOTATED_ENUM_MEMBER_IS_A_DECLARATION, CAUSES, RANGE
    ) == ["line 9: 'tagger-art-rejected' -> status 41"], (
        "an annotated enum member IS a member to the interpreter, so a module "
        "declaring its vocabulary that way declares its causes exactly as the "
        "unannotated spelling does"
    )


def test_the_key_side_carries_its_own_hop_bound_and_this_is_where_it_stops():
    """The key side reads two aliases and gives up on three, as the value side does."""
    assert reserved_code_tables(
        A_KEY_CHAIN_THE_HOP_BOUND_READS, declared_causes(), RANGE
    ) == ["line 5: 'config-unusable' -> status 30"]
    assert reserved_code_tables(
        A_KEY_CHAIN_THE_HOP_BOUND_GIVES_UP, declared_causes(), RANGE
    ) == [], (
        "the key side now reads three aliases, which is a different boundary "
        "from the value side's. Say where the new one is and pin both"
    )


def test_a_duplicate_key_in_a_second_table_is_reported_once():
    """A duplicate key in a second table is reported once, so the count is right.

    Covered by the dedupe; see the residual "One check in this unit is unreachable".
    """
    assert reserved_code_tables(
        EVASION_A_DUPLICATE_KEY_IN_A_SECOND_TABLE, declared_causes(), RANGE
    ) == ["line 2: 'config-unusable' -> status 30"]


def test_the_hop_bound_is_a_coverage_dial_and_this_is_what_it_gives_up():
    """``MAX_HOPS`` is a coverage dial, and this pins what it gives up at three.

    Any value below the recursion limit stops the hang; the value decides how
    long an alias chain is read. Swept 2 to 6: two aliases are read at all, three
    only from 4. Raising it fails this test and demands the new boundary.
    """
    assert _guards.MAX_HOPS == 3
    assert reserved_code_tables(
        A_CHAIN_THE_HOP_BOUND_READS, declared_causes(), RANGE
    ) == ["line 4: 'config-unusable' -> status 30 as A1"]
    assert reserved_code_tables(
        A_CHAIN_THE_HOP_BOUND_GIVES_UP, declared_causes(), RANGE
    ) == [], (
        "the bound now reaches three aliases, which is more coverage and a "
        "different boundary, so say where the new one is and pin it here"
    )


@pytest.mark.parametrize(
    "source",
    [
        CORRECT_READS_THE_TABLE,
        CORRECT_EXITS_THROUGH_THE_ENVELOPE,
        CORRECT_SOMEBODY_ELSE_HAS_AN_EXIT,
        CORRECT_USES_THE_VOCABULARY,
        CORRECT_EXITS_THROUGH_A_SYMBOL_IMPORT,
        CORRECT_RAISES_A_STATUS_IT_LOOKED_UP,
        CORRECT_RAISES_A_STATUS_IT_WAS_GIVEN,
        CORRECT_A_PARAMETER_SHADOWS_AN_EXIT,
        CORRECT_A_PARAMETER_SHADOWS_A_CONSTANT,
        CORRECT_GETATTR_ON_SOMEBODY_ELSE,
        CORRECT_A_TWO_ARGUMENT_SYSTEMEXIT_IS_NOT_A_STATUS,
    ],
)
def test_the_bare_status_guard_stays_silent_on_correct_code(source):
    """P7 for the bare-status guard, in the import shapes the evasions use."""
    assert process_status_literals(source) == []


@pytest.mark.parametrize(
    "source",
    [
        EVASION_ALIASED_SYS_EXIT,
        EVASION_RAISES_A_STATUS,
        EVASION_EXIT_IMPORTED_AS_A_SYMBOL,
        EVASION_EXIT_IMPORTED_UNDER_ANOTHER_NAME,
        EVASION_THE_UNDERLYING_EXIT,
        EVASION_AN_EXIT_HELD_IN_A_VARIABLE,
        EVASION_THE_EXCEPTION_UNDER_ANOTHER_NAME,
        EVASION_A_SUBCLASS_OF_THE_EXCEPTION,
        EVASION_EXIT_FETCHED_BY_GETATTR,
        EVASION_A_FETCHED_EXIT_HELD_IN_A_NAME,
        EVASION_THE_MODULE_REBOUND,
        EVASION_THE_MODULE_IMPORTED_BY_NAME,
        EVASION_THE_MODULE_REACHED_THROUGH_ANOTHER,
        EVASION_THE_EXCEPTION_THROUGH_BUILTINS,
        EVASION_A_STATUS_HELD_IN_A_CONSTANT,
        EVASION_A_STATUS_ASSIGNED_THEN_EXITED,
        EVASION_AN_EXIT_ALIASED_A_SECOND_TIME,
        EVASION_AN_IMPORTER_HELD_IN_A_NAME,
        EVASION_THE_EXCEPTION_IMPORTED_FROM_BUILTINS,
        EVASION_A_TRACKED_MODULE_IMPORTED_AS_A_SYMBOL,
    ],
)
def test_the_bare_status_guard_bites_a_module_that_returns_a_raw_literal(source):
    """``from sys import exit`` needs no attribute access, and is caught."""
    assert process_status_literals(source)


def test_a_negative_status_is_a_bare_status_too():
    """A negative status is a bare status too, and the worst one.

    The shell truncates ``exit(-1)`` to 255 and ``subprocess.returncode`` reads a
    negative as a signal death. Two edits blinded the guard to every negative,
    dropping ``resolve_int``'s unary minus or widening ``status == 0`` to
    ``status <= 0``. The three spellings are the literal, a name and a raise.
    """
    assert process_status_literals(EVASION_A_NEGATIVE_STATUS) == [
        "line 5: sys.exit(-1)"
    ]
    assert process_status_literals(EVASION_A_NEGATIVE_STATUS_HELD_IN_A_CONSTANT) == [
        "line 7: sys.exit(-TERMINATED) (status -15)"
    ]
    assert process_status_literals(EVASION_A_NEGATIVE_STATUS_RAISED) == [
        "line 3: SystemExit(-1)"
    ]

    assert process_status_literals("import sys\nsys.exit(-0)\n") == [], (
        "negative zero is zero, which is success spelled oddly and not a refusal"
    )


def test_a_negative_is_outside_the_reserved_range_on_the_table_side():
    """A second table mapping a cause to a negative is silent, by the reserved range.

    So the unary-minus branch serves only the bare-status guard above.
    """
    assert reserved_code_tables(
        'CODES = {"config-unusable": -30}\n', declared_causes(), RANGE
    ) == []


def declared_causes() -> frozenset[str]:
    """Every string anybody in this repository has declared to be a refusal cause.

    One key set and one value rule; the tree has zero offenders under it outside
    the two table owners. Three declarations feed it: the reservation table, the
    causes the completeness walk derived, and ``core.cause.REASONS``. A fourth
    arrives per file, a source's own enum, which ``ReservedCodeTable`` adds.

    The derived term is empty in the tree today;
    ``test_the_key_set_is_the_union_of_all_three_declarations`` drives it.
    ``preflight.MountState`` spells its states with underscores and is outside the
    key set; the residual
    "Two refusal vocabularies stay outside the second-table guard's key set"
    records why.
    """
    derived = structured_refusal_causes()
    return CAUSES | frozenset().union(*derived.values()) | frozenset(REASONS)


def registry_only_causes() -> frozenset[str]:
    """The slugs the closed registry reserves and the reserved table does not."""
    return frozenset(REASONS) - CAUSES


def package_of(relative: str) -> str:
    """The dotted package a module's relative imports resolve against, as Python resolves it.

    ``cli/render.py`` and ``cli/__init__.py`` both answer ``cratekit.cli``.
    """
    return ".".join(["cratekit"] + relative.split("/")[:-1])


#: Every residual cited by TITLE anywhere the rule below reaches. A residual
#: number can mean different findings on two branches in flight; a title
#: survives a merge. Declared and scanned titles are asserted EQUAL, so an
#: invented or drifted title fails.
CITED_RESIDUALS = (
    "A pink row outside the named playlist is not swept",
    "Five accepted findings from the U38 reviews",
    "Two copies of one import walk still carry a relative-import defect",
    "One check in this unit is unreachable",
    "Two refusal vocabularies stay outside the second-table guard's key set",
    "The conversion proof shows that a conversion exists, not that it keeps anything",
    "The tiers were bought with a number that does not exist",
    "The mutation table for this unit's guards, written into the repository",
    "The backup restore is not yet bound to the destructive-session gates",
    "A negative process status is reserved against in prose and was covered by nothing",
    "Six of this unit's own rules recognize a builtin by the text of its name",
    "One entry in the not-a-cause whitelist covers an enum the walk never reaches",
    # Declared on the U38 merge for U34, cited from tests/modules/test_reports.py.
    # The rule is repository wide, so another unit's title is declared here too.
    "A class rebound after its own definition is no longer reachable by name",
    # Declared on the U59 merge, both once cited by number in tests/_source_guards.py.
    # Declared on relay/111, cited above the kebab-literal pin.
    "`crate sync favorites` declares a local colour and tag write it never performs",
    "Guard whitelists assert what is forbidden, never what is permitted",
    "What the soft-delete guard cannot see, and two gaps in the gate contract",
    # Declared on relay/54, cited from tests/modules/test_reports.py.
    "The reports allowlist audit is one hop deep",
    # Declared on the restore sidecar fix, cited from tests/modules/test_tools.py.
    "A restore from a snapshot taken with rekordbox closed always reports failure",
    # Declared on the outbound rename, cited from the population re-pin below.
    "A swept playlist is never marked on the account",
    # Declared on relay/171. A leading phrase, since the heading quotes a sentence
    # and a citation ends at the first double quote.
    "Five places where",
    # Declared on the repair rows unit, cited from two population re-pins. A
    # leading phrase.
    "A row the native landing creates leaves rekordbox's own defaults empty",
)

#: WHAT A CITATION LOOKS LIKE: the word ``residual``, then only whitespace and
#: comment prefixes, then the TITLE in double quotes. Prose naming a title any
#: other way is invisible to the scan and has to be rewritten into this form.
CITATION = re.compile(r"\bresiduals?\b[\s#:]*\"([^\"\n]+)\"")

#: The authored surface the citation rule is scanned over, vendored code excluded.
AUTHORED_GLOBS = ("src/**/*.py", "tests/**/*.py", "scripts/**/*.py", "docs/**/*.md")

#: The residual document, always covered: it defines the titles.
FINDINGS_DOCUMENT = "docs/residual-findings.md"


def findings_documents() -> list[str]:
    """The residual document's archives by number range (U314), then the document."""
    archives = sorted((REPO_ROOT / "docs" / "ledger").glob("*.md"))
    return [path.relative_to(REPO_ROOT).as_posix() for path in archives] + [FINDINGS_DOCUMENT]


def authored_sources() -> list[tuple[str, str]]:
    """Every file the citation rule is allowed to look at, as (relative, text)."""
    found: dict[str, str] = {}
    for pattern in AUTHORED_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            if "_vendor" in path.parts:
                continue
            found[path.relative_to(REPO_ROOT).as_posix()] = path.read_text()
    return sorted(found.items())


def owned_sources() -> list[str]:
    """The files the citation rule covers: every file that adopted it, plus the residual documents.

    Derived, so a file cannot fall out by being forgotten. Not the branch's
    changed files, which go empty at merge. A file citing a residual only by
    number (``src/cratekit/modules/tools/backup.py``) has adopted nothing.
    """
    found = set(findings_documents())
    for relative, text in authored_sources():
        if "residual" in text and CITATION.search(text):
            found.add(relative)
    return sorted(found)


def residual_headings() -> list[tuple[str, str]]:
    """Every heading in the findings documents, as (number, title), in order.

    A list, never a set, so two byte identical headings stay two.
    """
    document = "".join((REPO_ROOT / name).read_text() for name in findings_documents())
    found = []
    for line in document.splitlines():
        if line.startswith("## R-") and ". " in line:
            number, _, title = line[3:].partition(". ")
            found.append((number.strip(), title.strip()))
    return found


def test_a_residual_heading_names_exactly_one_finding():
    """No two findings share a title, and no two share a number, read off a list."""
    headings = residual_headings()
    assert headings, (
        "no residual headings were found in docs/residual-findings.md or its "
        "archives, so every "
        "citation check below would pass over nothing"
    )
    titles = [title for _number, title in headings]
    numbers = [number for number, _title in headings]
    repeated_titles = sorted({title for title in titles if titles.count(title) > 1})
    repeated_numbers = sorted({number for number in numbers if numbers.count(number) > 1})
    assert repeated_titles == [], (
        f"these residual TITLES name more than one finding: {repeated_titles}. A "
        f"title is the identifier this unit's citations use, so a duplicate title "
        f"is the collision the convention exists to prevent, arriving through the "
        f"identifier that replaced the colliding one"
    )
    assert repeated_numbers == [], (
        f"these residual NUMBERS name more than one finding: {repeated_numbers}"
    )


def test_every_residual_this_unit_cites_is_cited_by_title():
    """Every residual is cited by title, never by a number that can change subject at merge.

    1. Every declared title resolves to exactly one heading.
    2. Every title written in a covered file is declared.
    3. No covered file carries a bare residual number.
    """
    headings = residual_headings()
    # Matched as a prefix, resolving to exactly ONE heading, so a leading phrase
    # can never later fit two findings.
    resolved = {
        title: [heading for _number, heading in headings if heading.startswith(title)]
        for title in CITED_RESIDUALS
    }
    unresolved = {
        title: matches for title, matches in resolved.items() if len(matches) != 1
    }
    assert unresolved == {}, (
        f"these cited titles do not name exactly one heading in "
        f"{FINDINGS_DOCUMENT}: {unresolved}. A citation that names nothing "
        f"is worse than a number, because it looks resolved"
    )

    # The reverse direction catches the typo the forward one cannot see.
    covered = set(owned_sources())
    authored = authored_sources()
    written: dict[str, set[str]] = {}
    for relative, source in authored:
        if relative not in covered:
            continue
        for title in CITATION.findall(source):
            written.setdefault(title, set()).add(relative)
    undeclared = {
        title: sorted(files)
        for title, files in written.items()
        if title not in set(CITED_RESIDUALS)
    }
    assert undeclared == {}, (
        f"these titles are cited as residuals and are not declared in "
        f"CITED_RESIDUALS: {undeclared}. A citation nobody declared is a citation "
        f"nothing checks, which is what a number was"
    )
    assert set(CITED_RESIDUALS) == set(written), (
        f"CITED_RESIDUALS and the citations actually written disagree. Declared "
        f"and never written: {sorted(set(CITED_RESIDUALS) - set(written))}. "
        f"Written and never declared: {sorted(set(written) - set(CITED_RESIDUALS))}"
    )

    numbered = {}
    documents = set(findings_documents())
    for relative, source in authored:
        # The residual documents are exempt from the number ban only: since numbers
        # became append only (2026-08-10) a number there never moves. The ban still
        # covers code.
        if relative not in covered or relative in documents:
            continue
        hits = [
            match
            for line in source.splitlines()
            # A heading DEFINES a number. Only a reference to one is a citation.
            if not line.startswith("## R-")
            for match in re.findall(r"R-\d+(?:\.\d+)?", line)
        ]
        if hits:
            numbered[relative] = sorted(set(hits))
    assert numbered == {}, (
        f"these files cite a residual by NUMBER: {numbered}. Six numbers collide "
        f"across the branches in flight, so a number silently changes subject at "
        f"merge. Cite the title from CITED_RESIDUALS instead"
    )


def test_the_covered_file_set_is_derived_and_reaches_what_the_unit_touched():
    """A positive control: the covered set reaches the unit's files and the residual document."""
    covered = set(owned_sources())
    assert {
        "tests/test_reserved_causes.py",
        "tests/_source_guards.py",
        "tests/test_review_queue.py",
        "src/cratekit/cli/exit_codes.py",
        "tests/modules/test_tools.py",
        *findings_documents(),
    } <= covered, (
        f"the derivation lost a file that carries citations: {sorted(covered)}"
    )


def test_the_package_scan_reaches_the_modules_it_claims_to():
    """A positive control on the scanner: files at three depths, and modules, not just inits.

    The two tree-wide guards assert absence, so a scan narrowed from ``rglob``
    to ``glob`` would pass both. The size is a floor, so a new module needs no edit.
    """
    scanned = {relative for relative, _ in package_sources()}
    for reached in (
        "__init__.py",
        "cli/exit_codes.py",
        "core/cause.py",
        "modules/tools/backup.py",
    ):
        assert reached in scanned, (
            f"the scan no longer reaches {reached}, so every guard driven over "
            f"package_sources is silent about it and says so by finding nothing"
        )
    assert len(scanned) >= 51, f"the scan collapsed to {len(scanned)} files"
    modules = {relative for relative in scanned if not relative.endswith("__init__.py")}
    assert len(modules) >= 43, (
        f"the scan reaches {len(scanned)} files but only {len(modules)} of them "
        f"are modules, so it is counting package inits and looking at less code "
        f"than the count suggests"
    )
    assert all(relative.endswith(".py") for relative in scanned)
    assert not [relative for relative in scanned if relative.startswith("_vendor/")]
    assert TABLE_OWNERS <= scanned, (
        "the guard exempts files the scan does not reach, which is an exemption "
        "for nothing and a scan that shrank"
    )


# ═══════════════════════════════════════════════════════════════════════════
# The at-risk population, measured on ONE basis and pinned
#
# Every count is over the files ``package_sources()`` returns that are not
# table owners, with the shipped ``cause_key`` asked of every ``ast.Name`` and
# ``ast.Attribute``.
# ═══════════════════════════════════════════════════════════════════════════


def population_under_measurement(
    sources: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    """The non-owner files every count in this section is taken over.

    ``sources`` is one reading of ``package_sources()`` by the test asking, so
    every count one test takes is over one reading of the package (U258).
    """
    return [
        (relative, source)
        for relative, source in sources
        if relative not in TABLE_OWNERS
    ]


def modules_holding_a_named_cause(
    sources: list[tuple[str, str]], *, own_declarations: bool
) -> dict[str, list[str]]:
    """Modules where a NAME or a class attribute resolves to a declared cause.

    ``own_declarations`` adds each file's own enum declarations, as
    ``ReservedCodeTable`` reads them; the gap between the two answers is the
    effect of the key-side widening.
    """
    causes = declared_causes()
    found: dict[str, list[str]] = {}
    for relative, source in population_under_measurement(sources):
        tree = parsed(source)
        table = _guards.ReservedCodeTable(tree, causes, RANGE, package_of(relative))
        if not own_declarations:
            table.causes = set(causes)
        hits = {
            slug
            for node in _guards._walk(tree)
            if isinstance(node, (ast.Name, ast.Attribute))
            for slug in [table.cause_key(node)]
            if slug
        }
        if hits:
            found[relative] = sorted(hits)
    return found


def modules_holding_a_cause_literal(
    sources: list[tuple[str, str]],
) -> dict[str, list[str]]:
    """The same population under the OLD constant-only key rule, for comparison."""
    causes = declared_causes()
    found: dict[str, list[str]] = {}
    for relative, source in population_under_measurement(sources):
        hits = {
            node.value
            for node in _guards._walk(parsed(source))
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and node.value in causes
        }
        if hits:
            found[relative] = sorted(hits)
    return found


def holds_an_in_range_integer(source: str) -> bool:
    """Whether a source contains an integer literal inside the reserved range."""
    low, high = RANGE
    return any(
        isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
        and low <= node.value < high
        for node in _guards._walk(parsed(source))
    )


def kebab_shaped_literals() -> set[str]:
    """Every cause-shaped string literal anywhere in the package."""
    return {
        node.value
        for _, source in package_sources()
        for node in _guards._walk(parsed(source))
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and _guards.CAUSE_SLUG.match(node.value)
    }


# Residuals this file still cites since U125 retired the shared re-pin ledger,
# kept as title citations so the citation test agrees with CITED_RESIDUALS.
# residual "A pink row outside the named playlist is not swept"
# residual "A row the native landing creates leaves rekordbox's own defaults empty"
# residual "A swept playlist is never marked on the account"
# residual "Five places where"
# residual "`crate sync favorites` declares a local colour and tag write it never performs"

def kebab_literals_by_module(sources: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Kebab-shaped string literals in each package module, sorted, one entry per module."""
    found: dict[str, list[str]] = {}
    for relative, source in sources:
        hits = sorted(
            {
                node.value
                for node in _guards._walk(parsed(source))
                if isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and _guards.CAUSE_SLUG.match(node.value)
            }
        )
        if hits:
            found[relative] = hits
    return found



@shares_parses
def test_pinned_populations_derive_totals_and_key_by_module():
    """U125: totals derive from per-module pins, so parallel cards edit different lines.

    Since U296 the pins are one file per package under
    ``tests/ratchets/reserved_causes/``, read by ``_pinned_reserved_populations.py``.
    """
    causes = declared_causes()
    non_reserved = causes - CAUSES
    scanned = package_sources()
    by_module = kebab_literals_by_module(scanned)
    literals = (
        frozenset().union(*(frozenset(v) for v in by_module.values()))
        if by_module
        else frozenset()
    )
    without = modules_holding_a_named_cause(scanned, own_declarations=False)
    with_own = modules_holding_a_named_cause(scanned, own_declarations=True)
    literal_holders = modules_holding_a_cause_literal(scanned)
    sources = dict(scanned)
    both = [
        relative
        for relative in with_own
        if holds_an_in_range_integer(sources[relative])
    ]
    literal_both = [
        relative
        for relative in literal_holders
        if holds_an_in_range_integer(sources[relative])
    ]
    pinned_literals = (
        frozenset().union(
            *(frozenset(v) for v in PINNED_KEBAB_LITERALS_BY_MODULE.values())
        )
        if PINNED_KEBAB_LITERALS_BY_MODULE
        else frozenset()
    )

    # Derived totals from the pins equal the figures measured on the tree.
    assert (
        PINNED_RESERVED_CAUSE_COUNT + len(PINNED_NON_RESERVED_CAUSES),
        len(PINNED_NON_RESERVED_CAUSES),
        PINNED_RESERVED_CAUSE_COUNT,
    ) == (len(causes), len(non_reserved), len(CAUSES)), (
        "derived cause totals from the pins disagree with the tree"
    )
    assert len(pinned_literals) == len(literals), (
        f"derived kebab-literal total {len(pinned_literals)} disagrees with "
        f"the tree's {len(literals)}"
    )
    assert (
        len(PINNED_NAMED_WITHOUT_OWN),
        len(PINNED_NAMED_WITH_OWN),
        len(PINNED_NAMED_WITH_INTEGER),
    ) == (len(without), len(with_own), len(both)), (
        "derived named at-risk totals from the pins disagree with the tree"
    )
    assert (
        len(PINNED_LITERAL_HOLDERS),
        len(PINNED_LITERAL_HOLDERS_WITH_INTEGER),
    ) == (len(literal_holders), len(literal_both)), (
        "derived literal-holder totals from the pins disagree with the tree"
    )

    # Structural: integer-holders are subsets; pin keys are module paths.
    assert PINNED_NAMED_WITH_INTEGER <= frozenset(PINNED_NAMED_WITH_OWN)
    assert PINNED_LITERAL_HOLDERS_WITH_INTEGER <= frozenset(PINNED_LITERAL_HOLDERS)
    assert all(key.endswith(".py") for key in PINNED_KEBAB_LITERALS_BY_MODULE)
    assert all(isinstance(slug, str) and slug for slug in PINNED_NON_RESERVED_CAUSES)


@shares_parses
def test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned():
    """The population figures the residuals argue from, recomputed from the tree and pinned.

    See the residual "The tiers were bought with a number that does not exist".
    When this fails, look, then update the pin for the module or slug that moved,
    and the residual's prose if a total it argues from moved. Never widen the
    assertion or bring back a whole-repository total tuple, the merge hotspot
    U125 removed. Both halves are measured on the one basis above.
    """
    causes = declared_causes()
    # One slug per line in PINNED_NON_RESERVED_CAUSES plus the table size, so
    # cards appending different causes merge cleanly.
    non_reserved = causes - CAUSES
    assert non_reserved == PINNED_NON_RESERVED_CAUSES, (
        "the non-reserved cause set moved; named members that joined: "
        f"{sorted(non_reserved - PINNED_NON_RESERVED_CAUSES)}; left: "
        f"{sorted(PINNED_NON_RESERVED_CAUSES - non_reserved)}. Update only those "
        "slugs in PINNED_NON_RESERVED_CAUSES, measured on the merged tree"
    )
    assert len(CAUSES) == PINNED_RESERVED_CAUSE_COUNT, (
        f"the reserved table moved to {len(CAUSES)}; update "
        "PINNED_RESERVED_CAUSE_COUNT and name what joined or left"
    )
    assert (len(causes), len(non_reserved), len(CAUSES)) == (
        PINNED_RESERVED_CAUSE_COUNT + len(PINNED_NON_RESERVED_CAUSES),
        len(PINNED_NON_RESERVED_CAUSES),
        PINNED_RESERVED_CAUSE_COUNT,
    ), "derived cause totals must equal the pinned parts"

    scanned = package_sources()
    sources = dict(scanned)
    by_module = kebab_literals_by_module(scanned)
    assert by_module == PINNED_KEBAB_LITERALS_BY_MODULE, (
        "kebab literals moved in at least one module; joined modules or literals: "
        f"{ {k: sorted(set(by_module.get(k, [])) - set(PINNED_KEBAB_LITERALS_BY_MODULE.get(k, []))) for k in sorted(set(by_module) | set(PINNED_KEBAB_LITERALS_BY_MODULE)) if set(by_module.get(k, [])) != set(PINNED_KEBAB_LITERALS_BY_MODULE.get(k, [])) } }. "
        "Update only those module entries in KEBAB_LITERALS, " + _PIN_FILES
    )
    literals = frozenset().union(*(frozenset(v) for v in by_module.values())) if by_module else frozenset()
    pinned_literals = (
        frozenset().union(*(frozenset(v) for v in PINNED_KEBAB_LITERALS_BY_MODULE.values()))
        if PINNED_KEBAB_LITERALS_BY_MODULE
        else frozenset()
    )
    assert literals == pinned_literals
    assert (len(literals), len(literals - set(causes))) == (
        len(pinned_literals),
        len(pinned_literals - set(causes)),
    ), (
        f"the kebab-literal population moved to {len(literals)} distinct with "
        f"{len(literals - set(causes))} that are not keys"
    )

    widened = frozenset(set(causes) | literals)
    wide = {
        relative: reserved_code_tables_in(
            parsed(source), widened, RANGE, package_of(relative)
        )
        for relative, source in population_under_measurement(scanned)
    }
    assert {relative: hits for relative, hits in wide.items() if hits} == {}, (
        "the wide rule has a headroom problem now: adding every kebab-shaped "
        "literal in the package to the key set reports an offender, and the "
        "argument for one key set rests on it reporting none"
    )

    without = modules_holding_a_named_cause(scanned, own_declarations=False)
    with_own = modules_holding_a_named_cause(scanned, own_declarations=True)
    literal_holders = modules_holding_a_cause_literal(scanned)
    both = [
        relative
        for relative in with_own
        if holds_an_in_range_integer(sources[relative])
    ]
    literal_both = [
        relative
        for relative in literal_holders
        if holds_an_in_range_integer(sources[relative])
    ]
    assert without == PINNED_NAMED_WITHOUT_OWN, (
        "the named without-own population moved; update only the modules that "
        f"joined or left in NAMED_WITHOUT_OWN, {_PIN_FILES}: joined "
        f"{sorted(set(without) - set(PINNED_NAMED_WITHOUT_OWN))}, left "
        f"{sorted(set(PINNED_NAMED_WITHOUT_OWN) - set(without))}"
    )
    assert with_own == PINNED_NAMED_WITH_OWN, (
        "the named with-own population moved; update only the modules that "
        f"joined or left in NAMED_WITH_OWN, {_PIN_FILES}: joined "
        f"{sorted(set(with_own) - set(PINNED_NAMED_WITH_OWN))}, left "
        f"{sorted(set(PINNED_NAMED_WITH_OWN) - set(with_own))}"
    )
    assert frozenset(both) == PINNED_NAMED_WITH_INTEGER, (
        "the named-with-integer population moved; update "
        "NAMED_WITH_INTEGER for the modules that joined or left, " + _PIN_FILES
    )
    assert (len(without), len(with_own), len(both)) == (
        len(PINNED_NAMED_WITHOUT_OWN),
        len(PINNED_NAMED_WITH_OWN),
        len(PINNED_NAMED_WITH_INTEGER),
    ), (
        f"the named at-risk population moved: {len(without)} modules hold a name "
        f"resolving to a cause declared elsewhere, {len(with_own)} once each "
        f"file's own enum declarations count, {len(both)} of those also hold an "
        f"in-range integer. Update the residual"
    )
    assert literal_holders == PINNED_LITERAL_HOLDERS, (
        "the literal-holder population moved; update only the modules that "
        f"joined or left in LITERAL_HOLDERS, {_PIN_FILES}: joined "
        f"{sorted(set(literal_holders) - set(PINNED_LITERAL_HOLDERS))}, left "
        f"{sorted(set(PINNED_LITERAL_HOLDERS) - set(literal_holders))}"
    )
    assert frozenset(literal_both) == PINNED_LITERAL_HOLDERS_WITH_INTEGER, (
        "the literal-holders-with-integer population moved; update "
        "LITERAL_HOLDERS_WITH_INTEGER for the modules that joined or left, " + _PIN_FILES
    )
    assert (len(literal_holders), len(literal_both)) == (
        len(PINNED_LITERAL_HOLDERS),
        len(PINNED_LITERAL_HOLDERS_WITH_INTEGER),
    ), (
        f"the literal at-risk population moved to {len(literal_holders)} modules, "
        f"{len(literal_both)} of them also holding an in-range integer"
    )
    assert len(with_own) < len(literal_holders), (
        "the named surface the key widening added is now LARGER than the literal "
        "surface that predates it, which is the comparison the decision to keep "
        "the widening rests on. Re-argue it or narrow the key side"
    )

    sharpest = sources["core/exit_codes.py"]
    declared_in_its_own_enum = _guards._declared_enum_values(parsed(sharpest))
    low, high = RANGE
    integers = [
        node.value
        for node in ast.walk(parsed(sharpest))
        if isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
        and low <= node.value < high
    ]
    # Re-pinned on the U27 merge (GRANT_PATH_ACCESS, REMOUNT_WRITABLE, UNLOCK_PATH,
    # the first also a reserved cause) and by U138 (RUN_BACKUP, not one). The
    # integers stay at 28.
    assert (
        len(declared_in_its_own_enum),
        len(declared_in_its_own_enum & CAUSES),
        len(integers),
    ) == (46, 7, 28), (
        "core/exit_codes.py is the sharpest case in the residual and its figures "
        "moved. It declares cause-shaped strings in its own Remedy enum, some of "
        "which are also reserved-table causes, and it holds in-range integers "
        "while not being a table owner"
    )


def test_the_static_enum_rule_agrees_with_the_interpreter_over_the_whole_package():
    """Every class the interpreter calls an enum is one the static rule found, with its members.

    The static rule reads base names only, so a ``class Cause(Vocabulary)``
    against a base of ours fails here, naming the file. One direction only:
    reading more than the interpreter is the safe side.
    """
    modules, unimportable = imported_package_modules()
    assert not unimportable
    static = {
        relative: _guards._declared_enum_values(parsed(source))
        for relative, source in package_sources()
    }
    missed: dict[str, list[str]] = {}
    checked = 0
    for module in modules:
        source_file = getattr(module, "__file__", None)
        if source_file is None:
            continue
        relative = Path(source_file).resolve().relative_to(PACKAGE_ROOT).as_posix()
        if relative not in static:
            continue
        for value in vars(module).values():
            if not (isinstance(value, type) and issubclass(value, enum.Enum)):
                continue
            if value.__module__ != module.__name__:
                continue
            declared = {
                member.value
                for member in value
                if isinstance(member.value, str)
                and _guards.CAUSE_SLUG.match(member.value)
            }
            if declared:
                checked += 1
            unseen = sorted(declared - static[relative])
            if unseen:
                missed[f"{relative}:{value.__name__}"] = unseen
    assert checked >= 15, (
        f"only {checked} enums declaring a cause-shaped value were reached at "
        f"runtime, so the agreement below is being measured over almost nothing. "
        f"The tree holds 45 enums and 19 of them declare one"
    )
    assert not missed, (
        f"the interpreter says these are enums declaring cause-shaped values and "
        f"the static rule did not see them, so every one of those causes is out "
        f"of the key set for its own file: {missed}"
    )


def test_no_module_in_the_package_keeps_a_second_reservation_table():
    """Over the real tree, only the two table owners may map a refusal cause to a code."""
    causes = declared_causes()
    found = {
        relative: reserved_code_tables(source, causes, RANGE, package_of(relative))
        for relative, source in package_sources()
        if relative not in TABLE_OWNERS
    }
    offenders = {relative: hits for relative, hits in found.items() if hits}
    assert not offenders, f"a second reservation table: {offenders}"


def test_the_table_owner_escape_is_exactly_these_two_files():
    """``TABLE_OWNERS`` is pinned by exact membership, each entry a file that holds a table.

    It switches the guard off for a whole file, so widening it is the cheapest
    way to stop the guard looking; the rule is from the residual
    "Two copies of one import walk still carry a relative-import defect", and
    "The mutation table for this unit's guards, written into the repository"
    carries the row.
    """
    assert TABLE_OWNERS == frozenset({"cli/exit_codes.py", "core/cause.py"}), (
        "the second-table guard is off for every file named here, so widening "
        "this set is how the guard gets switched off one file at a time. Adding "
        "an entry needs a reason written beside it and this assertion updated, "
        "which is the review this set never had"
    )
    causes = declared_causes()
    sources = dict(package_sources())
    for owner in TABLE_OWNERS:
        assert owner in sources, f"{owner} is exempted and is not in the package"
        assert reserved_code_tables(
            sources[owner], causes, RANGE, package_of(owner)
        ), (
            f"{owner} is exempted from the second-table guard and maps no cause "
            f"to a code, so the exemption covers nothing and the file it was "
            f"written for has moved"
        )


def test_the_closed_reason_registry_is_in_the_one_key_set():
    """The registry's slugs are keys: answers differ with and without the registry in the set."""
    assert "config-unusable" in REASONS
    assert "config-unusable" not in CAUSES, (
        "pick a slug only the registry declares, or this proves nothing about "
        "the registry's contribution to the key set"
    )
    assert "config-unusable" in declared_causes()

    reported = reserved_code_tables(
        EVASION_A_NAMED_CODE_FOR_A_REGISTRY_SLUG, declared_causes(), RANGE
    )
    assert reported == ["line 4: 'config-unusable' -> ExitCode.LIBRARY_UNAVAILABLE"]
    assert (
        reserved_code_tables(EVASION_A_NAMED_CODE_FOR_A_REGISTRY_SLUG, CAUSES, RANGE)
        == []
    ), (
        "the registry is what puts this key in the set, so dropping it has to "
        "silence the hit. If it does not, the reservation was being found some "
        "other way and this test is measuring nothing"
    )
    assert reserved_code_tables(
        EVASION_A_CONVERSION_ON_A_REGISTRY_SLUG, declared_causes(), RANGE
    ) == ["line 4: 'credential-missing' -> int(ExitCode.PRECONDITION)"]


def _reported_key_kinds(source: str) -> dict[str, int]:
    """What kind of expression each reported key is, off the syntax tree.

    A slug reads the same inline or through a constant, so a fixture claiming to
    cover names needs this to fail when rewritten into literals. Deduplicated as
    ``reserved_code_tables`` deduplicates.
    """
    tree = ast.parse(source)
    table = _guards.ReservedCodeTable(tree, declared_causes(), RANGE, None)
    counted: dict[str, int] = {}
    seen: set[tuple[int, str, str]] = set()
    for key, value, label in table.pairs():
        slug = table.cause_key(key)
        if slug is None:
            continue
        status = label if label is not None else table.status(value)
        if status is None:
            continue
        entry = (key.lineno, slug, status)
        if entry in seen:
            continue
        seen.add(entry)
        kind = type(key).__name__
        counted[kind] = counted.get(kind, 0) + 1
    return counted


def _construct_shapes(source: str) -> dict[str, int]:
    """How many of each table shape a source is written with, off the syntax tree.

    A list of hits cannot express a shape, so swapping a construct for another
    with the same slugs and values on the same lines needs this to fail. The
    residual fixture is eighteen hits from eleven constructs, tallied as thirteen
    nodes: ``SENTENCES`` and the empty ``DELAYS`` produce no hit.
    """
    counted: dict[str, int] = {}

    def tally(shape: str) -> None:
        counted[shape] = counted.get(shape, 0) + 1

    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Dict):
            tally("dict literal")
        elif isinstance(node, ast.DictComp):
            tally("dict comprehension")
        elif (
            isinstance(node, ast.Tuple)
            and node.elts
            and all(isinstance(element, ast.Tuple) for element in node.elts)
        ):
            tally("tuple of pairs")
        elif isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Subscript) for target in node.targets
        ):
            tally("subscript assignment")
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "setdefault"
        ):
            tally("setdefault call")
        elif isinstance(node, ast.If):
            tally("branch returning a value")
    return counted


def test_ordinary_data_keyed_on_a_cause_slug_is_the_residual_the_wide_rule_pays():
    """The wide rule's false alarms, listed rather than narrowed away. See the residual
    "The tiers were bought with a number that does not exist".

    Each costs one look and a recorded decision; the other side of the trade is
    a second table nothing notices. The tree has zero offenders today, even with
    every kebab literal in the package added to the key set.
    """
    hits = reserved_code_tables(
        RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS, declared_causes(), RANGE
    )
    assert hits == [
        "line 10: 'decision-required' -> status 40",
        "line 10: 'decision-stale' -> status 24",
        "line 12: 'job-schema-mismatch' -> status 11",
        "line 12: 'review-schema-mismatch' -> status 12",
        "line 14: 'backup-facts-unreadable' -> status 30",
        "line 16: 'library-database-missing' -> status 50",
        "line 18: 'cloud-sync-active' -> status 20",
        "line 18: 'library-volume-unmounted' -> status 30",
        "line 21: 'cloud-sync-unreadable' -> status 30",
        "line 22: 'canary-read-failed' -> status 15",
        "line 24: 'doctor-check-failed' -> status 30",
        "line 24: 'smoke-test-failed' -> status 30",
        "line 2: 'session-lock-held' -> status 30",
        "line 2: 'write-lock-held' -> status 15",
        "line 33: 'unavailable-transient' -> status 45 as seconds",
        "line 5: 'credential-missing' -> status 10",
        "line 6: 'config-unusable' -> status 20",
        "line 7: 'internal-error' -> status 30",
    ], (
        "eighteen HITS from ELEVEN ordinary constructs, every integer inside "
        "the reserved range and every key a registry slug. The three counts "
        "here are different numbers and the round before wrote one of them for "
        "all three: eighteen hits, eleven constructs that produce a hit, and "
        "thirteen nodes in the shape tally below, which counts two dict "
        "literals that produce none. If this list shrinks, the fixture has "
        "drifted and the residual is smaller than it is written down as"
    )

    # THE SHAPE HALF: the list above pins keys, values and lines, not how each
    # construct is written.
    assert _construct_shapes(RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS) == {
        "dict literal": 7,
        "tuple of pairs": 2,
        "subscript assignment": 1,
        "setdefault call": 1,
        "dict comprehension": 1,
        "branch returning a value": 1,
    }, (
        "the fixture is here to cover distinct construct shapes, so swapping one "
        "for another that reports the same slugs and values has to fail rather "
        "than pass quietly"
    )

    # THE KEY-KIND HALF: every key above is an inline string.
    assert _reported_key_kinds(RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS) == {
        "Constant": 18
    }, (
        "this fixture is the LITERAL half of the residual. If a named key appears "
        "here it belongs in the fixture below, where the named half is pinned"
    )


def test_ordinary_data_keyed_on_a_NAME_is_the_same_residual_in_the_tree_s_own_idiom():
    """The same residual keyed on NAMES, the tree's own idiom, which the resolver widening moved.

    ``TrackOutcome`` is copied from ``src/cratekit/acquire/adapter.py``. The
    tree still reports zero offenders with the resolver on; the at-risk
    population it moved is pinned by the population test.
    """
    hits = reserved_code_tables(
        RESIDUAL_ORDINARY_DATA_KEYED_ON_A_NAME, declared_causes(), RANGE
    )
    assert hits == [
        "line 18: 'unavailable-transient' -> status 30",
        "line 20: 'decision-stale' -> status 20",
        "line 20: 'session-lock-held' -> status 10",
        "line 22: 'config-unusable' -> status 40",
        "line 24: 'config-unusable' -> status 40",
        "line 26: 'config-unusable' -> status 30",
        "line 26: 'decision-stale' -> status 30",
        "line 30: 'unavailable-transient' -> status 45",
    ], (
        "eight HITS from six ordinary constructs, none of them keyed on an inline "
        "string. If this list shrinks the resolver has been narrowed and the "
        "named spelling of a second table went quiet with it"
    )

    # THE ANTI-VACUITY HALF: named and inline keys report identically, so the key
    # kinds are what keep this fixture distinct from the one above.
    assert _reported_key_kinds(RESIDUAL_ORDINARY_DATA_KEYED_ON_A_NAME) == {
        "Attribute": 5,
        "Name": 3,
    }, (
        "no reported key here may be an inline string. This fixture exists to "
        "cover the spelling the key widening reached, and a Constant appearing "
        "in it means the coverage drifted back to the spelling already covered"
    )

    # THE SHAPES, so a construct cannot be swapped for another on the same lines.
    assert _construct_shapes(RESIDUAL_ORDINARY_DATA_KEYED_ON_A_NAME) == {
        "dict literal": 3,
        "dict comprehension": 1,
        "branch returning a value": 1,
    }


def test_a_comment_cannot_silence_a_reservation():
    """The per-line escape hatch is deleted, and this fails if it comes back.

    ``# not-a-reservation: <reason>`` silenced a one line ``def`` body, two
    statements on one line, and a whole registry from one comment (61
    reservations to 0). It was never used, and the wide rule has no false alarms
    in the tree to make cheap, so a reservation is answered by a recorded
    decision instead.
    """
    def without_lines(hits: list[str]) -> set[str]:
        """The slug and the status, because the two copies wrap differently."""
        return {hit.split(": ", 1)[1] for hit in hits}

    hits = reserved_code_tables(
        COMMENTED_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS, declared_causes(), RANGE
    )
    assert without_lines(hits) == without_lines(
        reserved_code_tables(
            RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS, declared_causes(), RANGE
        )
    ), (
        "a comment changed what the guard reports, so a per-line off switch is "
        "back and the residual can be silenced one line at a time again"
    )
    assert len(hits) == 18

    assert reserved_code_tables(
        COMMENT_ON_A_ONE_LINE_FUNCTION, declared_causes(), RANGE
    ) == ["line 2: 'config-unusable' -> status 30"], (
        "a one line def with the comment on it is silent, which is the escape "
        "covering a whole function body while claiming it never covers one"
    )
    assert reserved_code_tables(
        COMMENT_ON_TWO_STATEMENTS_AT_ONCE, declared_causes(), RANGE
    ) == [
        "line 2: 'config-unusable' -> status 30",
        "line 2: 'credential-missing' -> status 40",
    ], "one reason silenced two statements"
    assert reserved_code_tables(
        COMMENT_ON_THE_OPENING_LINE_OF_A_TABLE, declared_causes(), RANGE
    ) == [
        "line 3: 'config-unusable' -> status 30",
        "line 4: 'credential-missing' -> status 40",
        "line 5: 'internal-error' -> status 50",
    ], (
        "a comment on the opening line of a mapping silenced every key below it, "
        "which is how one comment took the sixty one entry registry to zero"
    )


#: The one call a source string is allowed to reach in the guard module.
THE_ONLY_SINK = "ast.parse"


def text_the_guard_module_reads(source: str) -> list[str]:
    """Every place the guard module does anything with raw source text but parse it.

    A comment exists only in the text; ``ast.parse`` discards it, so a guard
    that never touches the text cannot have a per-line off switch. Each
    module-level ``source: str`` parameter is a seed, tainting names it is
    assigned to and parameters of this module's functions it is passed to. The
    only permitted use is as the single argument of ``ast.parse``. A function
    reading text of its own is not seeded; the import whitelist closes that route.
    """
    tree = ast.parse(source)
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    def positional(function: ast.AST) -> list[str]:
        arguments = function.args
        return [
            argument.arg
            for argument in list(arguments.posonlyargs) + list(arguments.args)
        ]

    def seeds(function: ast.AST) -> set[str]:
        arguments = function.args
        every = (
            list(arguments.posonlyargs)
            + list(arguments.args)
            + list(arguments.kwonlyargs)
        )
        return {
            argument.arg
            for argument in every
            if argument.arg == "source"
            and argument.annotation is not None
            and "str" in ast.unparse(argument.annotation)
        }

    tainted = {name: seeds(function) for name, function in functions.items()}
    if not any(tainted.values()):
        return [
            "no function takes a `source: str` parameter, so this rule is "
            "seeded on nothing and proves nothing"
        ]

    changed = True
    while changed:
        changed = False
        for name, function in functions.items():
            for node in ast.walk(function):
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Name):
                    if node.value.id in tainted[name]:
                        for target in node.targets:
                            if (
                                isinstance(target, ast.Name)
                                and target.id not in tainted[name]
                            ):
                                tainted[name].add(target.id)
                                changed = True
                if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
                    continue
                callee = functions.get(node.func.id)
                if callee is None:
                    continue
                landing = positional(callee)
                for index, argument in enumerate(node.args):
                    if not (
                        isinstance(argument, ast.Name) and argument.id in tainted[name]
                    ):
                        continue
                    if index < len(landing) and landing[index] not in tainted[node.func.id]:
                        tainted[node.func.id].add(landing[index])
                        changed = True
                for keyword in node.keywords:
                    if (
                        keyword.arg
                        and isinstance(keyword.value, ast.Name)
                        and keyword.value.id in tainted[name]
                        and keyword.arg not in tainted[node.func.id]
                    ):
                        tainted[node.func.id].add(keyword.arg)
                        changed = True

    found: list[str] = []
    for name, function in functions.items():
        parents: dict[ast.AST, ast.AST] = {}
        for node in ast.walk(function):
            for child in ast.iter_child_nodes(node):
                parents[child] = node
        for node in ast.walk(function):
            if not (isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)):
                continue
            if node.id not in tainted[name]:
                continue
            parent = parents.get(node)
            if isinstance(parent, ast.Call):
                if node is parent.func:
                    found.append(f"{name}: line {node.lineno}: the source text is CALLED")
                    continue
                spelled = ast.unparse(parent.func)
                if (
                    spelled == THE_ONLY_SINK
                    and len(parent.args) == 1
                    and parent.args[0] is node
                ):
                    continue
                if isinstance(parent.func, ast.Name) and parent.func.id in functions:
                    continue
                found.append(
                    f"{name}: line {node.lineno}: the source text is handed to {spelled}"
                )
            elif isinstance(parent, ast.Assign) and parent.value is node:
                continue
            else:
                found.append(
                    f"{name}: line {node.lineno}: the source text reaches "
                    f"{type(parent).__name__}"
                )
    return sorted(found)


def _without_comments(source: str) -> str:
    """The same program with every comment gone, whatever the comment said."""
    return ast.unparse(ast.parse(source))


def _slugs_and_statuses(hits: list[str]) -> list[str]:
    """A hit list with the line numbers dropped, because unparsing moves lines."""
    return sorted(hit.split(": ", 1)[1] for hit in hits)


#: Markers a FRESH per-line escape hatch would plausibly be spelled with, none
#: the deleted one: the rule below must not depend on the spelling.
FRESH_ESCAPE_MARKERS = (
    "# ordinary-data: seconds",
    "# noqa: reservation",
    "# cratekit: not-a-table",
    "# pragma: no-reserve",
    "# this is a timeout and not a code",
)


def _guard_module_source() -> str:
    """The guard module's own text, read from the file the suite imported."""
    return Path(_guards.__file__).read_text()


def _with_a_fresh_hatch_wired_in(source: str) -> str:
    """The guard module with a NEW per-line escape hatch, wired in where the old one was.

    A different marker, no ``tokenize`` and none of the deleted hatch's names.
    """
    hatched = source.replace(
        "    tree = ast.parse(source)\n    table = ReservedCodeTable(",
        "    tree = ast.parse(source)\n"
        "    quiet = _hushed(source)\n"
        "    table = ReservedCodeTable(",
    ).replace(
        "def reserved_code_tables(",
        "def _hushed(text: str) -> set[int]:\n"
        "    marked = set()\n"
        "    for number, line in enumerate(text.splitlines(), start=1):\n"
        '        if "# ordinary-data" in line:\n'
        "            marked.add(number)\n"
        "    return marked\n"
        "\n"
        "\n"
        "def reserved_code_tables(",
        1,
    )
    assert hatched != source and "_hushed" in hatched, (
        "the hatch could not be wired in, so the assertion it exists for would "
        "be measuring an unchanged file. The anchors moved: repair them"
    )
    return hatched


def test_a_comment_cannot_change_what_the_guard_reports_whatever_it_says():
    """The guard's answer cannot depend on a comment: a source and its comment-free twin agree.

    Forbidding the last hatch's symbol names forbids that implementation, not
    the feature. Driven over the two table owners, the only files reporting
    anything, as well as the fixtures.
    """
    causes = declared_causes()
    for owner in sorted(TABLE_OWNERS):
        source = dict(package_sources())[owner]
        package = package_of(owner)
        with_comments = reserved_code_tables(source, causes, RANGE, package)
        assert len(with_comments) >= 22, (
            f"{owner} reports {len(with_comments)} reservations, so the "
            f"comparison below is being made over almost nothing"
        )
        assert _slugs_and_statuses(with_comments) == _slugs_and_statuses(
            reserved_code_tables(_without_comments(source), causes, RANGE, package)
        ), (
            f"{owner} reports differently once its comments are gone, so a "
            f"comment is an input to this guard and a per-line off switch is "
            f"back, whatever it is called"
        )

    for marker in FRESH_ESCAPE_MARKERS:
        marked = "\n".join(
            f"{line}  {marker}" if line.strip() else line
            for line in RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS.splitlines()
        )
        assert _slugs_and_statuses(
            reserved_code_tables(marked, causes, RANGE)
        ) == _slugs_and_statuses(
            reserved_code_tables(
                RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS, causes, RANGE
            )
        ), (
            f"{marker!r} on every line changed what the guard reports, so a "
            f"per-line escape exists under a name this test does not have to know"
        )


def test_the_guard_cannot_be_given_a_comment_because_it_cannot_read_the_text():
    """The structural half: the guard module's source parameters reach only ``ast.parse``.

    Both directions: the module as shipped answers clean, and with a fresh hatch
    wired in it answers with the hatch's line.
    """
    source = _guard_module_source()
    assert text_the_guard_module_reads(source) == [], (
        "the guard module does something with its raw source text other than "
        "parse it, which is the one way a comment can reach a rule that should "
        "only be able to see the syntax tree"
    )
    reported = text_the_guard_module_reads(_with_a_fresh_hatch_wired_in(source))
    assert reported, (
        "a per-line escape hatch reading the source text was wired into the "
        "guard module and this rule did not see it, so it is measuring nothing"
    )
    assert any("_hushed" in entry for entry in reported), reported


def test_the_guard_module_imports_only_what_reading_a_syntax_tree_needs():
    """The guard module imports exactly ``ast`` and ``re``, so nothing that sees a comment gets in.

    Adding an import costs one line here and the review it brings.
    """
    imported: set[str] = set()
    for node in ast.walk(ast.parse(_guard_module_source())):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            imported.add(node.module.split(".")[0])
    assert imported == {"__future__", "ast", "re"}, (
        f"the guard module imports {sorted(imported)}. Everything the guards ask "
        f"is a question about a syntax tree, so an import beyond the tree and the "
        f"slug shape is how something that can see a comment gets in"
    )


def test_nobody_in_the_package_writes_the_marker_that_was_deleted():
    """Nobody in the package writes the deleted ``# not-a-reservation:`` marker."""
    marked = [
        relative
        for relative, source in package_sources()
        if "not-a-reservation" in source
    ]
    assert marked == [], (
        f"a deleted escape is written in {marked}, so somebody is expecting it "
        f"to work and the guard is silently ignoring them"
    )


def test_the_key_set_is_the_union_of_all_three_declarations():
    """The key set is the union of all three declarations; the empty derived term is driven.

    The derived term is empty in the tree, so subset assertions were tautologies.
    """
    derived = frozenset().union(*structured_refusal_causes().values())
    assert derived, "the walk found nothing, so the guard's key set collapsed to the table"
    assert derived == CAUSES, (
        "the derived term is no longer empty against the table, so the swap "
        "below is not the only thing driving it and this docstring is stale"
    )
    assert CAUSES < declared_causes(), "the registry has to widen the key set"
    assert registry_only_causes() < declared_causes()

    invented = "invented-cause-nobody-declared"
    assert invented not in declared_causes()
    original = globals()["structured_refusal_causes"]
    globals()["structured_refusal_causes"] = lambda: {
        "cratekit.pretend": frozenset({invented})
    }
    try:
        assert invented in declared_causes(), (
            "a cause the package-wide walk derives has to reach the key set, or "
            "a module reserving codes for causes it declares somewhere else is "
            "invisible to the guard"
        )
        assert reserved_code_tables(
            f'CODES = {{"{invented}": 30}}\n', declared_causes(), RANGE
        )
    finally:
        globals()["structured_refusal_causes"] = original
    assert invented not in declared_causes()


def test_the_package_a_relative_import_resolves_against_is_derived():
    """``package_of``, driven directly, since the absence-asserting scans it feeds cannot drive it.

    One level up from a module and from a package's ``__init__`` is the same place.
    """
    assert package_of("cli/render.py") == "cratekit.cli"
    assert package_of("cli/__init__.py") == "cratekit.cli"
    assert package_of("__init__.py") == "cratekit"
    assert package_of("modules/tools/backup.py") == "cratekit.modules.tools"
    scanned = dict(package_sources())
    for relative in ("cli/render.py", "cli/__init__.py", "modules/tools/backup.py"):
        assert relative in scanned, f"{relative} left the tree, so this proves nothing"

    # END TO END: a sibling of the vocabulary module resolves onto it from
    # ``cratekit.core`` only, and ``package_of`` supplies that over a real file.
    assert reserved_code_tables(
        EVASION_A_SIBLING_RELATIVE_IMPORT, CAUSES, RANGE, package_of("core/session.py")
    )
    assert (
        reserved_code_tables(
            EVASION_A_SIBLING_RELATIVE_IMPORT, CAUSES, RANGE, package_of("session.py")
        )
        == []
    )


def test_the_module_and_the_class_are_named_once_each(monkeypatch):
    """The vocabulary's module leaf and class name are derived from the constants at use.

    Moving ``EXIT_CODE_MODULE`` moves every binding with it; the rule is from the
    residual "Two copies of one import walk still carry a relative-import defect".
    """
    with pytest.MonkeyPatch.context() as moved_module:
        moved_module.setattr(_guards, "EXIT_CODE_MODULE", "cratekit.core.statuses")
        moved = """
from cratekit.core import statuses

CODES = {"rclone-missing": statuses.ExitCode.PRECONDITION}
"""
        assert reserved_code_tables(moved, CAUSES, RANGE) == [
            "line 4: 'rclone-missing' -> statuses.ExitCode.PRECONDITION"
        ]
        assert (
            reserved_code_tables(EVASION_A_SIBLING_BOUND_AS_A_MODULE, CAUSES, RANGE) == []
        ), "the module moved and the binding did not follow it"

    monkeypatch.setattr(_guards, "EXIT_CODE_CLASS", "Status")
    renamed = """
from cratekit.core.exit_codes import Status

CODES = {"rclone-missing": Status.PRECONDITION}
"""
    assert reserved_code_tables(renamed, CAUSES, RANGE) == [
        "line 4: 'rclone-missing' -> Status.PRECONDITION"
    ]
    assert (
        reserved_code_tables(EVASION_A_SIBLING_RELATIVE_IMPORT, CAUSES, RANGE) == []
    ), "the class was renamed and the walk still answers for the old name"


def test_the_hop_bound_is_the_depth_of_the_deepest_spelling(monkeypatch):
    """``MAX_HOPS`` is the deepest promised spelling's depth: resolved at it, silent below."""
    assert _guards.MAX_HOPS == 3
    assert reserved_code_tables(
        EVASION_A_CODE_NAMED_TWICE_THEN_ADJUSTED, CAUSES, RANGE
    ) == ["line 14: 'tagger-art-rejected' -> status 31 as OFFSET + 1"]

    monkeypatch.setattr(_guards, "MAX_HOPS", _guards.MAX_HOPS - 1)
    assert (
        reserved_code_tables(EVASION_A_CODE_NAMED_TWICE_THEN_ADJUSTED, CAUSES, RANGE)
        == []
    ), (
        "one hop below the bound the deepest promised spelling still resolves, "
        "so the bound is higher than anything needs and the number is decoration"
    )


def test_no_module_in_the_package_turns_a_bare_integer_into_a_status():
    found = {relative: process_status_literals(source) for relative, source in package_sources()}
    offenders = {relative: hits for relative, hits in found.items() if hits}
    assert not offenders, (
        f"these bypass the vocabulary entirely and exit with an integer nobody "
        f"reserved: {offenders}"
    )
