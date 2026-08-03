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

WHAT THE REVIEW FOUND, because it is the reason half of this file exists. A
plausible next module, ``modules/tools/tagger.py``, was written with three
unreserved refusal causes, its own reservation table, and two bare integer
process exits, and this suite stayed green over all of it. The table was sound
and every check ON the table was real; the three things that LOOK at the rest of
the tree were not.

* The second-table guard was keyed on the causes already reserved, so a module
  deciding codes for causes NOBODY has reserved was invisible, which is not a
  corner of the problem but the whole of it. It also read dict literals only,
  while its docstring said "every mapping in this source".
* The same guard fired on correct code in seven of eight fixtures, reporting
  things like ``'rekordbox-running' -> bare status False``, and a guard that
  fires on correct code is one somebody adds an exemption for.
* The bare-status guard walked ``ast.Import`` alone, so ``from sys import exit``
  went straight past it, which is the one shape that needs no attribute access.
* The completeness walk could not read ``Refusal | None``, a discriminator
  imported under ``if TYPE_CHECKING:``, a module that raises on import, or the
  canonical ``Remedy``, and it demanded that any package enum on a constructor be
  reserved, so an exception carrying a ``Scope`` broke it with a nonsense demand.

Each of those now has fixtures in BOTH directions beside it, and that module is
the acceptance test: it fails three assertions by name.
"""

from __future__ import annotations

import ast
import enum
import importlib
import pkgutil
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
from tests._source_guards import process_status_literals, reserved_code_tables

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "src" / "cratekit"

#: The only two files in the package that may map a refusal cause to a code.
#: One is the reservation itself; the other is the closed reason registry that
#: predates it. A test below asserts the two AGREE wherever they overlap, which
#: is the alternative to pretending only one of them exists.
TABLE_OWNERS = frozenset({"cli/exit_codes.py", "core/cause.py"})

CAUSES = frozenset(reserved_codes.RESERVED_CAUSES)

#: The range the guard measures a bare integer against, taken from the table
#: rather than repeated, so the two cannot drift.
RANGE = reserved_codes.RESERVED_RANGE

#: The constructor parameters that carry a refusal's structured CAUSE.
#:
#: Read by name, and the reason is that the annotation alone cannot tell the two
#: apart. ``scope: Scope`` and ``refusal: Refusal`` are both a package enum on an
#: exception's constructor, and only one of them is the reason the refusal
#: happened; the other is context travelling with it. A derivation that accepted
#: any package enum demanded that ``['item', 'run', 'session', 'source']`` be
#: reserved as exit codes, which is a nonsense the next author would have had to
#: argue their way out of. These four names are how every module in this
#: repository already spells the role.
DISCRIMINATOR_PARAMETERS = frozenset({"refusal", "remedy", "reason", "cause"})

#: The refusals whose discriminator this table deliberately does NOT reserve,
#: and the conversion that already gives each one a code and a remediation.
#:
#: NAMED, not accidental, and that is the whole change. Both of these were
#: excluded before by the shape of their annotation rather than by a decision:
#: their discriminator is written ``Remedy | None``, the derivation could not
#: read a union, and so the exclusion held only until somebody tightened an
#: unrelated annotation. An exclusion nobody wrote down is an exclusion nobody
#: can review.
#:
#: ``test_every_exclusion_names_a_refusal_something_already_converts`` proves
#: each entry rather than trusting it: it finds the except clause in this package
#: that catches the type and reads its remedy. A refusal nobody converts is
#: exactly what this table is for, so an entry that stops being true fails here.
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
    }
)


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
    """The test above drives ``_index`` directly, which proves the check and not WHEN.

    "At import" is a structural property of the module and is asserted as one:
    the published mapping is built by a module-level call, so a reservation that
    the index refuses cannot load at all. A guard that ran only when the suite
    ran would ship the duplicate to anybody who imports the package without it.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The reserved range, enforced rather than described
# ═══════════════════════════════════════════════════════════════════════════


def test_every_reserved_code_sits_inside_the_reserved_range():
    """10 through 59, and a test that fails on anything else.

    A range nothing enforces is a comment, and the next unit picks a code inside
    it. Below 10 is the process band: 0 is success, 1 is a defect, and 2 belongs
    to the argument parser, which is the one property the whole KTD25 fix rests
    on. At or above MAX_CODE is the shell's own territory, where 126 means not
    executable, 127 means not found, 128 plus a signal number covers 129 to 192
    on a platform whose real-time signals run to a SIGRTMAX of 64, and anything
    past a byte truncates to something it did not mean. The job engine reads the
    same statuses through subprocess.returncode, which is the NEGATIVE signal
    number on POSIX rather than 128 plus it, and this range is clear of both.
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
    """60 through 63 is the room a class nobody has met yet claims.

    Asserting that no reservation sits there cannot fail while the range check
    above already forbids it, so that assertion is not the test. The two that can
    fail are these: the reserved range STOPS where the growth band starts, and
    the status vocabulary itself has no member inside it. Adding an ``ExitCode``
    at 61 is how the room disappears, and it fails here.
    """
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
    """A permission set wider than the range is a permission nobody granted.

    ``RESERVED_BANDS`` lists five bands and today's reservations use three, so
    nothing about the reservations can tell whether the other two are deliberate
    or leftover. They are derived from the range here, which makes widening
    either one without the other fail.
    """
    low, high = reserved_codes.RESERVED_RANGE
    spanned = {band.name for band in BANDS if band.start < high and band.stop > low}
    assert reserved_codes.RESERVED_BANDS == spanned, (
        f"the permitted bands are {sorted(reserved_codes.RESERVED_BANDS)} and the "
        f"range {low} to {high - 1} spans {sorted(spanned)}"
    )


@pytest.mark.parametrize("value", [0, 1, 2, 3, 60, 63, 64, 126, 127, 130, 255])
def test_a_code_outside_the_range_cannot_be_reserved(value):
    """The range enforced at import, driven with the exact integers it excludes.

    EVERY value here reaches ``_index``, which was not true when this test read
    as coverage it did not have: six of the nine had no ``ExitCode`` member, so
    the body returned before touching the index and asserted only that the member
    was missing. A reservation naming a bare integer is now refused by name, so
    the values with no member drive the index too, and the shape a future author
    would actually write is the shape that fails.
    """
    member = next((code for code in ExitCode if int(code) == value), None)
    if member is None:
        assert value not in {int(code) for code in ExitCode}
    candidate = reserved_codes.Reservation(
        cause="invented",
        code=member if member is not None else value,
        note="outside the range on purpose",
        steps=("nothing",),
    )
    with pytest.raises(ValueError) as excinfo:
        reserved_codes._index((candidate,))
    assert "invented" in str(excinfo.value)


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


def test_the_two_tables_spell_two_conditions_twice_and_still_agree():
    """The overlap check compares SPELLING, so these two pairs are invisible to it.

    ``library-root-absent`` here and ``library-directory-missing`` in the closed
    registry are one condition with two names, and so are ``database-absent`` and
    ``library-database-missing``. They agree on 22 today and nothing was asserting
    it, because the derived overlap can only see ``rekordbox-running``.

    They are not renamed into one. A slug is persisted inside a stored cause and
    crosses a process boundary when the job engine re-invokes the command line,
    so by this repository's own rule renaming one is a breaking change to
    anything holding it. The duplication is recorded and pinned instead.
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
    """One symbol, two meanings, pinned rather than papered over.

    The module docstring used to claim the symbol keeps one meaning wherever it
    is read. It does not: an unreadable FACT file written by a newer build is an
    acknowledgment gate at 32, and a CONFIGURATION file written by a newer build
    is ``config-unusable`` at 30. Both readings are asserted here, so the day
    somebody makes them the same value it is a decision rather than a drift.
    """
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


_NAMESPACES: dict[str, dict[str, object]] = {}


def _annotation_namespace(module: ModuleType | None) -> dict[str, object]:
    """Every name this module's IMPORT STATEMENTS bind, TYPE_CHECKING included.

    ``get_type_hints`` resolves an annotation against what a module holds at
    RUNTIME, and a discriminator imported under ``if TYPE_CHECKING:`` is not
    there, so the call raises ``NameError``. The first version of this walk
    swallowed that, which meant the more carefully a module avoided an import
    cycle, the less of it the derivation could see. The import statements are
    read from the SOURCE instead, which sees a guarded import exactly the way a
    person reading the file does.
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


def _declared_enums(hint: object, owner: str, packages: tuple[str, ...]) -> Iterator[type]:
    """Every enum THIS REPOSITORY declares that an annotation can carry.

    Recursive, because ``Refusal | None`` is not a type and ``isinstance(hint,
    type)`` is False for it. An optional discriminator is the ordinary shape for
    a base exception that lets each raise override a class default, and reading
    only the bare-type spelling made the most common shape in the package the one
    the walk could not see.

    ``ExitCode`` and only ``ExitCode`` is excluded. A STATUS is not a cause, so
    an exception carrying one has nothing to reserve. Excluding the whole module
    it lives in, which is what this did first, made the canonical ``Remedy``
    invisible too, so the more closely a module followed this repository's own
    "stay a subset" convention, the less of it was checked.
    """
    if isinstance(hint, type) and issubclass(hint, enum.Enum):
        if hint is ExitCode:
            return
        if hint.__module__ == owner or hint.__module__.split(".")[0] in packages:
            yield hint
        return
    for argument in typing.get_args(hint):
        yield from _declared_enums(argument, owner, packages)


def refusal_causes_in(
    module: ModuleType, *, packages: tuple[str, ...] = ("cratekit",)
) -> dict[str, frozenset[str]]:
    """The structured refusal causes ONE module declares, as producer -> slugs.

    DERIVED, and the derivation is the specification of what this table owes.

    A ``CratekitError`` already carries a ``Cause`` whose reason comes from the
    closed registry, so its code is reserved by construction and it is not the
    gap. The gap is every OTHER exception in the package that carries a
    structured discriminator, because there is nothing downstream that turns one
    of those into a status. Those are found by their shape: an exception defined
    in this module, not a ``CratekitError``, whose constructor takes a parameter
    NAMED for the discriminator role and annotated with an enum this repository
    declares.

    WHAT THIS SHAPE CANNOT SEE, said plainly rather than presented as a rule.
    ``core.secrets`` carries its remedy as a CLASS ATTRIBUTE and subclasses per
    meaning, so the exception TYPE is the discriminator and no constructor
    parameter names one. That is genuinely outside a constructor walk. It is
    recorded in ``docs/residual-findings.md`` rather than papered over, because a
    credential failure reaching any caller other than the one that converts it
    still becomes ``internal-error`` today.
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
            f"{base.__module__}.{base.__qualname__}" in CONVERTED_ELSEWHERE
            for base in value.__mro__
        ):
            continue
        initializer = value.__init__
        owner = sys.modules.get(getattr(initializer, "__module__", ""), namespace_owner)
        try:
            hints = typing.get_type_hints(initializer, localns=_annotation_namespace(owner))
        except Exception as exc:  # noqa: BLE001 - re-raised, never swallowed
            raise AssertionError(
                f"{module.__name__}.{value.__name__} has an annotation this walk "
                f"cannot resolve ({type(exc).__name__}: {exc}). Swallowing it "
                f"would make the exception invisible to the completeness check "
                f"rather than failing, which is how a refusal ships with no "
                f"reserved code and nobody finds out"
            ) from exc
        slugs: set[str] = set()
        for name, hint in hints.items():
            if name not in DISCRIMINATOR_PARAMETERS:
                continue
            for declared in _declared_enums(hint, value.__module__, packages):
                slugs.update(str(member.value) for member in declared)
        if slugs:
            found[f"{module.__name__}.{value.__name__}"] = frozenset(slugs)
    return found


def imported_package_modules() -> tuple[list[ModuleType], dict[str, str]]:
    """Every module in the package, imported, and the ones that would not import.

    The failures are RETURNED rather than skipped. A walk that quietly drops a
    module it cannot import is a walk whose coverage depends on which optional
    extras happen to be installed on the machine running it, so the same suite
    proves less under a slim profile than under a full one and says nothing about
    the difference. That is P3's own lesson pointed at the derivation itself.
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


def _converted_exception_names() -> set[str]:
    """Exception class names this package CATCHES and whose remedy it then reads.

    Per module rather than per flow, and that limit is deliberate: an except
    clause binds a name and the handler hands it to a helper in the same file as
    often as it reads it inline, so requiring the read inside the handler body
    would have missed the acquisition layer entirely. What it will not accept is
    a catch that never looks at the remedy at all, which is the difference
    between a conversion and a swallow.
    """
    names: set[str] = set()
    for _, source in package_sources():
        tree = ast.parse(source)
        reads = {
            node.value.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Attribute)
            and node.attr == "remedy"
            and isinstance(node.value, ast.Name)
        }
        for node in ast.walk(tree):
            if not isinstance(node, ast.ExceptHandler):
                continue
            if node.name is None or node.type is None or node.name not in reads:
                continue
            caught = node.type.elts if isinstance(node.type, ast.Tuple) else [node.type]
            names.update(ast.unparse(entry).split(".")[-1] for entry in caught)
    return names


def test_every_exclusion_names_a_refusal_something_already_converts():
    """An exclusion is a claim about the tree, so it is checked against the tree.

    The two entries were excluded before by the accident of a union annotation
    the walk could not read, under a stated reason that was false of one of them.
    Now they are named, and each has to earn it: something in this package
    catches the type and carries its remedy onward. An entry that stops being
    true fails here rather than quietly widening what this table does not cover.
    """
    converted = _converted_exception_names()
    modules, _ = imported_package_modules()
    for qualname, reason in CONVERTED_ELSEWHERE.items():
        assert reason, f"{qualname} is excluded and says nothing about why"
        module_name, _, class_name = qualname.rpartition(".")
        excluded = getattr(importlib.import_module(module_name), class_name)
        family = {
            candidate.__name__
            for module in modules
            for candidate in vars(module).values()
            if isinstance(candidate, type)
            and issubclass(candidate, Exception)
            and issubclass(candidate, excluded)
        }
        assert family & converted, (
            f"{qualname} is excluded from the completeness walk because something "
            f"already converts it, and nothing in this package catches it and "
            f"reads its remedy. Either the conversion went away, in which case "
            f"the exclusion has to go too, or the entry was never true"
        )


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


# ═══════════════════════════════════════════════════════════════════════════
# The derivation itself, driven against modules written to defeat it (P7)
# ═══════════════════════════════════════════════════════════════════════════
#
# The completeness check is only as good as the walk under it, and the walk is
# the part that was silently blind. These build a real module from source, so
# every shape is exercised through the same path the package takes: annotations
# resolved the way Python resolves them, class hierarchies real, and the
# TYPE_CHECKING fixture genuinely unresolvable at runtime without the fix.

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

UNSEEN_CONTEXT_RATHER_THAN_A_CAUSE = """
from __future__ import annotations

from cratekit.core.cause import Scope


class ProbeProblem(Exception):
    def __init__(self, message: str, scope: Scope = Scope.RUN) -> None:
        super().__init__(message)
        self.scope = scope
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
        (SEEN_DISCRIMINATOR_IMPORTED_FOR_TYPING_ONLY, {"repair-backup-facts", "upgrade-cratekit"}),
        (SEEN_A_DATACLASS_EXCEPTION, {"tagger-art-rejected"}),
        (SEEN_A_TYPE_CALL, {"tagger-art-rejected"}),
        (SEEN_A_FACTORY, {"tagger-art-rejected"}),
    ],
)
def test_the_walk_sees_every_shape_a_refusal_is_actually_written_in(
    module_from, source, expected
):
    """Four of these were invisible, and one of the four is live in the tree.

    ``Refusal | None`` is the shape ``core/config.py`` already uses and the shape
    the reviewer's next module used, so the walk was blind to the most ordinary
    way to write a base exception with a per-raise override. The typing-only
    import was invisible because the resolution failure was swallowed, which
    punished the module that avoided an import cycle.
    """
    module = module_from("subject", source)
    derived = refusal_causes_in(module, packages=FIXTURE_PACKAGES)
    assert derived, "the walk saw nothing"
    assert frozenset().union(*derived.values()) == expected


def test_the_walk_sees_a_refusal_whose_base_lives_in_another_module(module_from):
    module_from("upstream", UPSTREAM_FOR_THE_SUBCLASS)
    module = module_from("child", SEEN_A_BASE_IN_ANOTHER_MODULE)
    derived = refusal_causes_in(module, packages=FIXTURE_PACKAGES)
    assert derived == {"u38fix.child.TaggingRefused": frozenset({"tagger-art-rejected"})}


def test_the_walk_demands_the_whole_vocabulary_a_module_claims(module_from):
    """A module that annotates the CANONICAL Remedy has claimed all of it.

    Excluding the whole of ``core.exit_codes`` made this invisible, so a module
    following this repository's own "stay a subset" convention was the one shape
    nothing checked. It is seen now, and what it owes is every token it declared
    it can carry. The way to owe less is to declare a narrower enum, which is
    what four modules in the package already do.
    """
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
    """P7 for the derivation. A demand that makes no sense is how a check is deleted.

    The first of these is the one that mattered: a correct exception carrying a
    ``Scope`` made the completeness test fail demanding that ``item``, ``run``,
    ``session`` and ``source`` be reserved as exit codes. Nobody reserves those,
    so the only way out was to weaken the check.
    """
    module = module_from("subject", source)
    assert refusal_causes_in(module, packages=FIXTURE_PACKAGES) == {}


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

# ── Correct code keyed on a cause slug and mapped to an INTEGER ─────────────
#
# The failure mode these close is the one this repository has already paid for
# once: a guard fires on a correct module, somebody adds the file to the owners
# set to make the build green, and the guard is switched off for that whole file
# from then on. Six of the reserved keys are also remediation tokens, so a
# display order, a retry budget and a backoff are all a cause slug mapped to a
# small integer, and none of them is a reservation.

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
def wait_for(cause):
    if cause == "rclone-missing":
        seconds = 30
        return seconds
    return 0
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
# The case the table exists to prevent, and the case a guard keyed on the
# existing registry cannot see: a new module deciding its own codes. Every one
# of these passed the first version of the guard.

EVASION_A_NEW_MODULE_DECIDES_ITS_OWN_CODES = """
from cratekit.core.exit_codes import ExitCode

CODES = {
    "tagger-source-unreadable": ExitCode.PRECONDITION,
    "tagger-art-rejected": 30,
    "tagger-lookup-unavailable": 41,
}
"""

EVASION_A_TUPLE_OF_PAIRS = """
CODES = (
    ("tagger-source-unreadable", 30),
    ("tagger-art-rejected", 41),
)
"""

EVASION_A_COMPREHENSION_OVER_PAIRS = """
CODES = {cause: code for cause, code in (("tagger-art-rejected", 30),)}
"""

EVASION_A_COMPREHENSION_OVER_SLUGS = """
CODES = {cause: 30 for cause in ("tagger-art-rejected", "tagger-source-unreadable")}
"""

EVASION_ZIPPED_FROM_TWO_SEQUENCES = """
SLUGS = ("tagger-art-rejected", "tagger-source-unreadable")
STATUSES = (30, 41)

CODES = dict(zip(SLUGS, STATUSES))
"""

EVASION_FILLED_A_KEY_AT_A_TIME = """
CODES = {}
CODES["tagger-art-rejected"] = 30
"""

EVASION_AN_ORDERED_DICT = """
from collections import OrderedDict

CODES = OrderedDict([("tagger-art-rejected", 30)])
"""

EVASION_SETDEFAULT = """
CODES = {}

def reserve():
    CODES.setdefault("tagger-art-rejected", 30)
"""

EVASION_A_MATCH_STATEMENT = """
def status(cause):
    match cause:
        case "tagger-art-rejected":
            return 30
        case "tagger-source-unreadable":
            return 41
        case _:
            return 1
"""

EVASION_AN_IF_CHAIN = """
def status(cause):
    if cause == "tagger-art-rejected":
        return 30
    if cause == "tagger-source-unreadable":
        return 41
    return 1
"""

EVASION_A_CODE_WITH_A_CONVERSION_ROUND_IT = """
from cratekit.core.exit_codes import ExitCode

CODES = {
    "tagger-art-rejected": int(ExitCode.PRECONDITION),
    "tagger-source-unreadable": ExitCode(30),
}
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

    The seven integer maps are the ones the first version got wrong, and it got
    them wrong in the direction that switches a guard off rather than the one
    that lets a defect through: it reported ``'rekordbox-running' -> bare status
    False``. Six reserved keys are also remediation tokens, so ordering them for
    display, counting them, or giving each a backoff is ordinary code, and the
    only integers that can be a reservation are the ones inside the range.
    """
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
    ],
)
def test_the_second_table_guard_bites_a_module_reserving_causes_of_its_own(source):
    """The case the table exists to prevent, and the case the guard could not see.

    Keying on the causes ALREADY reserved made the guard blind to a module that
    decides codes for causes nobody has reserved, which is not a corner of the
    problem, it is the problem. Eleven shapes, every one of them ordinary Python
    somebody would write without meaning to evade anything, and every one of them
    silent before.
    """
    assert reserved_code_tables(source, CAUSES, RANGE)


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
    ],
)
def test_the_bare_status_guard_stays_silent_on_correct_code(source):
    """The three added fixtures are the same import shapes the evasions use.

    Recognizing ``from sys import exit`` must not make every module that imports
    it a suspect, which is the half of P7 that gets skipped.
    """
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
    ],
)
def test_the_bare_status_guard_bites_a_module_that_returns_a_raw_literal(source):
    """``from sys import exit`` needs no attribute access, so it needed no evasion.

    The guard walked ``ast.Import`` alone, so the one import shape that binds the
    function directly went straight past it: the refusal reached the shell as 30
    with no envelope and no remediation, which is the precise defect this exists
    to stop. Both sibling classes in the same file already handled
    ``ast.ImportFrom``.
    """
    assert process_status_literals(source)


def test_no_module_in_the_package_keeps_a_second_reservation_table():
    """The guards, over the real tree.

    Exactly two files may map a refusal cause to a code, and both are named
    above. Anywhere else is a second opinion that will eventually disagree with
    the first, which is the argument this repository has already made about its
    duplicate taxonomy resolvers.
    """
    offenders = {
        relative: reserved_code_tables(source, CAUSES, RANGE)
        for relative, source in package_sources()
        if relative not in TABLE_OWNERS and reserved_code_tables(source, CAUSES, RANGE)
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
