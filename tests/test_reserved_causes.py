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

WHAT TWO REVIEWS FOUND, because it is the reason most of this file exists. A
plausible next module, ``modules/tools/tagger.py``, was written with three
unreserved refusal causes, its own reservation table, and two bare integer
process exits, and this suite stayed green over all of it. The table was sound
and every check ON the table was real; the three things that LOOK at the rest of
the tree were not.

ROUND ONE closed four:

* The second-table guard was keyed on the causes already reserved, so a module
  deciding codes for causes NOBODY has reserved was invisible, which is not a
  corner of the problem but the whole of it. It also read dict literals only,
  while its docstring said "every mapping in this source".
* The same guard fired on correct code in seven of eight fixtures, reporting
  things like ``'rekordbox-running' -> bare status False``.
* The bare-status guard walked ``ast.Import`` alone, so ``from sys import exit``
  went straight past it, which is the one shape that needs no attribute access.
* The completeness walk could not read ``Refusal | None``, a discriminator
  imported under ``if TYPE_CHECKING:``, a module that raises on import, or the
  canonical ``Remedy``.

ROUND TWO was the same module again, respelled three ordinary ways, each one
silencing exactly one assertion and all three together making the whole battery
green over it:

* THE ROLE WAS READ FROM THE PARAMETER NAME, which is a rename and not a rule. It
  had already lost a live refusal, ``preflight.LibraryVolumeError`` and its seven
  unreserved states, because that one calls its parameter ``status`` and hides
  the enum one field down inside a record. Renaming an unrelated parameter to
  ``reason`` put the ``Scope`` nonsense straight back. The classification lives
  on the ENUM now (``NOT_A_CAUSE``), so neither rename changes anything.
* A CODE HELD IN A NAME was invisible to both source guards, so ``PRECONDITION =
  30`` beside ``{"tagger-art-rejected": PRECONDITION}`` and ``sys.exit(
  PRECONDITION)`` were silent while the inlined 30 fired. The guards rewarded the
  careless spelling and excused the careful one.
* ``getattr(sys, "exit")`` disarmed the bare-status guard on its own, and so did
  rebinding the module, importing it by name, reaching it through ``os``, or
  naming the exception through ``builtins``.
* THE KEY RULE was a SHAPE, so any kebab string mapped to an integer in range
  counted: a logging level, a column width, a timeout, a retention in days. The
  key is a DECLARATION now, from the registry, the package-wide walk, or this
  file's own enums, and the derivation and the guard share one answer to what a
  cause is.
* The guard could not read U38's OWN idiom. ``cli/exit_codes.py`` declares its
  table as a tuple of three-field dataclasses, and the guard accepted a pair and
  nothing longer, so the second module to copy the house style was the one shape
  it could not see.

ROUND THREE stopped writing the module and pointed the same question at the
guards themselves: what does reverting this line kill? Seven answers were "nothing",
and each one was a different way of not looking:

* THE KEY RULE LOST THE CLOSED REGISTRY. Round two replaced a shape with a
  declaration and enumerated three sources, omitting ``core.cause.REASONS``,
  which is the other mapping in this repository that gives a slug a code. Sixty
  of its sixty one slugs were outside the key set, so a module writing
  ``{"config-unusable": 22}`` against a registry entry that says 30 reported
  nothing. Round one's rule reported it. The sharpest form: ``TABLE_OWNERS``
  "exempts" ``core/cause.py`` while the guard could see one of its sixty one
  mappings, which is exclusion by blindness rather than by decision.
* ``TABLE_OWNERS`` COULD BE WIDENED FOR FREE. Adding ``core/session.py`` switched
  the guard off for that whole file and the suite stayed green. Every assertion
  about that set was about what it forbids, and only exact membership catches a
  widening, which is what the residual
  "Two copies of one import walk still carry a relative-import defect" on ``main``
  said in another module's terms.
* ONE RELATIVE IMPORT SHAPE OUT OF THREE. ``from ..core.exit_codes import
  ExitCode`` was recognized and ``from .exit_codes import ExitCode`` was not,
  because the rule matched a two-element suffix a sibling import does not have.
  That is the spelling a module beside ``core/exit_codes.py`` would use.
* A BRANCH TABLE ONE INDENT DEEPER. The branch walk read the body's top level, so
  a return behind any further condition was silent. No evasion needed.
* THE CONVERSION PROOF'S SECOND HALF was still name matching: it asked whether
  the bound name appeared with an attribute read anywhere in the FILE, which
  nearly every handler satisfies because nearly every handler calls its binding
  ``exc``.
* THE TREE SCAN HAD NO POSITIVE CONTROL. Narrowing ``package_sources`` from
  ``rglob`` to ``glob`` killed nothing, because both tree-wide tests assert the
  ABSENCE of an offender. That is this file's own signature defect pointed at its
  own scanner.
* THE RECORD HOP READ A DATACLASS AND NOT A NAMED TUPLE, so the identical refusal
  was seen or invisible depending on which keyword its author reached for.

Each of those now has fixtures in BOTH directions beside it, and that module is
the acceptance test: every respelling of it, alone and combined, fails all three
assertions by name.

ROUND FOUR answered the first of those by splitting the key set into two tiers,
and ROUND FIVE removed the split, because the number that bought it was taken
from a hand written fixture rather than from this repository. Measured under the
wide rule against the 51 files the package scan reaches, 43 modules and 8
package ``__init__.py``: ZERO offenders outside the two table owners. Measured
against the sixteen fixtures the split silenced, by re-implementing round four's
gate and running it over them: the tiers report TWO and are silent on FOURTEEN,
and the residual "The tiers were bought with a number that does not exist"
carried a description of its own rule that was wrong about five spellings. The
trade
runs on error costs rather than on preference. A miss is a module quietly
disagreeing with the registry about what a refusal exits with, and nothing else
in this suite would notice. That residual carries the measurement, and the
residual
"The mutation table for this unit's guards, written into the repository"
carries the mutation table.

ROUND SIX deleted the per-line escape the fifth round shipped with it. Every
claim made for ``# not-a-reservation: <reason>`` was false when measured: it
silenced a one line ``def`` body, it silenced two statements on one reason, and
one comment on the opening line of ``core/cause.py``'s registry took that file
from 61 reported reservations to 0. It had never been used, and it was never
needed: adding every kebab shaped string literal in the package to the key set,
189 distinct with 108 that are not keys, still measures zero offenders. Round six
also found the guard resolving the VALUE of a pair through names for three rounds
while never resolving the KEY, which was the largest hole it had.

ROUND FIVE also found the shape this file is named for pointed at ITSELF, twice.
the review-side import fix from the residual
"Two copies of one import walk still carry a relative-import defect" shipped with zero
tests holding it: reverting it
left the suite green, because no fixture anywhere in ``tests/`` contained
``from .review import`` or ``from . import review`` while the exit-code half of
the same unification had three. And ``MAX_HOPS``'s docstring made a checkable
claim, "lowering it kills seven tests", that was false at every value.
"""

from __future__ import annotations

import ast
import dataclasses
import enum
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

#: The package enums that are NOT a refusal cause vocabulary, and why each one
#: is not. Every OTHER package enum reaching an exception's constructor is one.
#:
#: BY ENUM IDENTITY, never by the name of the parameter holding it, and the round
#: before this proved why. Reading the role from the parameter name looked like a
#: narrowing and was a rename: ``status: MountStatus`` on
#: ``preflight.LibraryVolumeError`` fell out of the walk entirely, taking seven
#: unreserved refusal causes with it, while renaming an unrelated parameter from
#: ``scope`` to ``reason`` put the ``Scope`` nonsense straight back. A filter a
#: rename can flip in either direction is not a filter, it is a coin.
#:
#: The cost of identity is that a new enum on an exception has to be classified
#: by a person. That is the right cost: the failure is a loud demand to classify
#: it, and going silent takes a deliberate edit to this table with a reason
#: written beside it. ``test_every_enum_declared_not_a_cause_exists`` keeps the
#: entries honest, so a renamed or deleted enum cannot leave a stale excuse here.
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


def _candidate(code) -> reserved_codes.Reservation:
    return reserved_codes.Reservation(
        cause="invented", code=code, note="outside the range on purpose", steps=("nothing",)
    )


@pytest.mark.parametrize("value", [0, 1, 2])
def test_a_code_the_vocabulary_has_but_the_range_excludes_cannot_be_reserved(value):
    """The RANGE, driven with the only three integers that can actually test it.

    ``ExitCode`` has a member at 0, 1 and 2 and nowhere else outside 10 to 59, so
    these are the whole of what a range check can be driven with, and the
    assertion is on the message naming the range rather than on any ValueError.
    The eleven-value version of this test read as coverage it did not have:
    eight of its values had no member and failed through the bare-integer
    refusal below, which says nothing about the range and would still pass if the
    range were widened to 255.
    """
    member = next(code for code in ExitCode if int(code) == value)
    with pytest.raises(ValueError) as excinfo:
        reserved_codes._index((_candidate(member),))
    assert "outside the reserved range" in str(excinfo.value)
    assert "invented" in str(excinfo.value)


@pytest.mark.parametrize("value", [3, 60, 63, 64, 126, 127, 130, 255])
def test_a_bare_integer_cannot_be_reserved_whatever_integer_it_is(value):
    """The other half, and what it proves is the vocabulary rather than the range.

    None of these has an ``ExitCode`` member, which is itself an answer: a
    reservation can only name a member. Writing one anyway is the bare-status
    mistake the guards forbid everywhere else, so the index refuses it by name
    rather than dying on an attribute error while trying to describe it.
    """
    assert value not in {int(code) for code in ExitCode}
    with pytest.raises(ValueError) as excinfo:
        reserved_codes._index((_candidate(value),))
    assert "not a member of the one status vocabulary" in str(excinfo.value)


def test_the_range_is_pinned_where_the_reservations_are_checked_against_it():
    """Named so nobody reads the two tests above as pinning the range itself."""
    assert reserved_codes.RESERVED_RANGE == (10, 60)
    assert reserved_codes.RESERVED_RANGE[1] <= MAX_CODE


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


def _is_a_record(hint: type) -> bool:
    """A dataclass or a ``NamedTuple``: the two ways this repository writes a record.

    Both are a fixed set of named, annotated fields, and the argument for looking
    one field down into a refusal's diagnosis is the same for either. Matching
    only the dataclass meant the identical exception was seen or invisible
    depending on which keyword its author reached for.

    ``NamedTuple`` leaves no marker class behind, so it is recognized the way the
    standard library recognizes one: a tuple subclass carrying ``_fields``.
    """
    if dataclasses.is_dataclass(hint):
        return True
    return issubclass(hint, tuple) and hasattr(hint, "_fields")


def _declared_enums(
    hint: object, owner: str, packages: tuple[str, ...], hops: int = 0
) -> Iterator[type]:
    """Every enum THIS REPOSITORY declares that an annotation can carry.

    Recursive over three things, and each one was a live blind spot.

    UNIONS, because ``Refusal | None`` is not a type and ``isinstance(hint,
    type)`` is False for it. An optional discriminator is the ordinary shape for
    a base exception that lets each raise override a class default, and reading
    only the bare-type spelling made the most common shape in the package the one
    the walk could not see.

    ONE FIELD INTO A RECORD, because ``preflight.LibraryVolumeError`` takes a
    ``MountStatus``, which is a record holding the ``MountState`` that is the
    actual cause. A refusal that wraps its diagnosis in a record with the paths
    it compared is BETTER code than one that passes the bare enum, and it was the
    one shape the walk could not read. One hop only: further needs a graph, and
    the exceptions that would need it do not exist.

    A RECORD IS A DATACLASS OR A NAMED TUPLE, because the argument for the hop
    says nothing about which of the two a module picked.
    ``dataclasses.is_dataclass`` is False for a ``NamedTuple``, so the identical
    refusal was seen in one spelling and invisible in the other, which is a rule
    a keyword defeats. Not live in the tree today, and this walk has been wrong
    twice about what "not live today" is worth.

    ``ExitCode`` and only ``ExitCode`` is excluded here. A STATUS is not a cause,
    so an exception carrying one has nothing to reserve. Excluding the whole
    module it lives in, which is what this did first, made the canonical
    ``Remedy`` invisible too, so the more closely a module followed this
    repository's own "stay a subset" convention, the less of it was checked.
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

    DERIVED, and the derivation is the specification of what this table owes.

    A ``CratekitError`` already carries a ``Cause`` whose reason comes from the
    closed registry, so its code is reserved by construction and it is not the
    gap. The gap is every OTHER exception in the package that carries a
    structured discriminator, because there is nothing downstream that turns one
    of those into a status. Those are found by their shape: an exception defined
    in this module, not a ``CratekitError``, whose constructor takes a parameter
    annotated with an enum this repository declares and has not declared to be
    something other than a cause.

    THE ROLE IS READ FROM THE ENUM, NOT FROM THE PARAMETER. Reading it from the
    parameter name looked like a narrowing and behaved like a rename: it lost
    ``preflight.LibraryVolumeError``, whose parameter is called ``status``, and
    it caught ``reason: Scope`` the moment somebody spelled an unrelated
    parameter that way. ``NOT_A_CAUSE`` carries the classification instead, by
    identity, with a reason per entry.

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
    # Duplicated on purpose by ``test_every_module_in_the_package_imports_so_the
    # _walk_can_see_it``, which is why deleting this line kills nothing. It stays
    # because the standalone test proves the tree imports and this one refuses to
    # let any CALLER of the derivation read a short answer as a complete one. A
    # reader should not mistake it for the only place the check lives. See the
    # residual "One check in this unit is unreachable".
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


def _local_function_names(tree: ast.AST) -> set[str]:
    """Every function and method THIS source defines, by name.

    Used to tell a helper from a builtin. ``_stop_with_failure(exc)`` hands the
    refusal to something in this file that can read it; ``str(exc)`` hands it to
    something that reads nothing off it, which is the difference between a
    conversion and a swallow.
    """
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _handler_uses_what_it_bound(handler: ast.ExceptHandler, helpers: set[str]) -> bool:
    """Whether THIS handler uses the exception it bound, rather than discarding it.

    SCOPED TO THE HANDLER, and the round before this scoped it to the FILE. That
    version asked whether the bound NAME appeared with an attribute read anywhere
    in the module, which is a different question with a much larger yes: a
    handler that binds ``exc`` and throws it away satisfied it as long as any
    ``exc.anything`` appeared somewhere else in the same file, and ``exc`` is
    what nearly every handler in this package calls its binding. Removing the
    rule entirely killed nothing.

    Two uses count and both are conversions:

    * reading an ATTRIBUTE off the bound name, which is how a handler reads a
      remedy or a discriminator;
    * handing the bound name to a function THIS FILE defines, which is what
      ``acquire/download.py`` does, and a rule demanding the read inline would
      have called the one real conversion in that layer a swallow.

    ``str(exc)`` is neither. It reads nothing off the exception and hands it to a
    builtin, so it stays a swallow, which is the distinction the docstring above
    claimed and the module-wide version could not make.
    """
    bound = handler.name
    for node in ast.walk(handler):
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
        for node in ast.walk(tree)
        if isinstance(node, ast.ExceptHandler)
        and node.name is not None
        and node.type is not None
        and _handler_uses_what_it_bound(node, helpers)
    ]


def _converted_exception_types() -> set[type]:
    """Exception CLASSES this package catches and then inspects, resolved for real.

    RESOLVED, not name-matched, and the difference is the whole check. The first
    version harvested the bare text after the last dot from any except clause,
    which meant its answer included ``Exception``, ``BaseException`` and
    ``ImportError``, and meant one unrelated module defining its OWN
    ``ConfigError``, catching it, discarding it, and reading ``exc.remedy``
    somewhere else was enough to keep an exclusion alive after the real
    conversion had gone. Each clause is resolved against the globals of the
    module that wrote it, so it answers for the class and not for the spelling.

    "Inspects" is answered by ``_handler_uses_what_it_bound``, per HANDLER. It
    used to be answered per module, which was the same hole one level up and is
    the half of this proof the class resolution left behind.

    WHAT THIS STILL CANNOT PROVE, and the residual
    "The conversion proof shows that a conversion exists, not that it keeps anything"
    records it. A conversion that EXISTS
    is not a conversion that is lossless. The worked example was
    ``core/session.py``, which caught ``BackupFactsUnreadable``, read
    ``exc.path`` and then named the remedy itself, discarding the one the
    exception carried; that was item 2 of the residual
    "Five accepted findings from the U38 reviews", and U48 closed it, so the
    example is now a HISTORICAL one rather than a live reading of the tree.

    The hole it illustrated did not close with it. That handler satisfied this
    proof while losing a field, and it still would, because the alternative is a
    rule about which attributes a handler must read, and that is a rule a
    refactor breaks. Do not read the closure as evidence this check got
    stronger: nothing here would notice the next handler that does the same
    thing.
    """
    found: set[type] = set()
    modules, _ = imported_package_modules()
    for module in modules:
        source_file = getattr(module, "__file__", None)
        if source_file is None or "_vendor" in source_file:
            continue
        tree = ast.parse(Path(source_file).read_text())
        for node in converting_handlers(tree):
            caught = node.type.elts if isinstance(node.type, ast.Tuple) else [node.type]
            for entry in caught:
                resolved = _resolve_in(module, ast.unparse(entry))
                if isinstance(resolved, type) and issubclass(resolved, BaseException):
                    found.add(resolved)
    return found


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
    """A handler that discards what it caught is a swallow, whatever the file does elsewhere.

    ``A_HANDLER_THAT_DISCARDS_IT`` is the case the module-wide rule got wrong,
    and it is written the way the real one is: the file has a helper that reads
    ``exc.remedy``, the handler binds ``exc`` and logs it, and the two have
    nothing to do with each other. Nearly every handler in this package calls its
    binding ``exc``, so one attribute read anywhere kept every exclusion in the
    table alive.
    """
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
    """An exclusion is a claim about the tree, so it is checked against the tree.

    Two of the three entries were excluded before by the accident of a union
    annotation the walk could not read, and the third by the accident of a
    parameter name. Now they are named, and each has to earn it: something in
    this package catches THAT CLASS, not something spelled like it, and inspects
    what it carries. An entry that stops being true fails here rather than
    quietly widening what this table does not cover.
    """
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
    """The hole the first proof had, closed and pinned.

    A bare name match said yes to any module that caught anything ending in the
    right word, so it also said yes to ``Exception``, ``BaseException`` and
    ``ImportError``, and an unrelated module defining its own ``ConfigError``
    would have kept an exclusion alive after the real conversion had gone.
    """
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
        # Three members rather than two since the U27 merge, 2026-08-15, which
        # appended GRANT_PATH_ACCESS to backup_facts.Remedy. The fixture derives
        # the whole enum, so this set is re-measured and re-pinned when a unit
        # adds a member, never widened to stop noticing.
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


def test_the_hop_into_a_record_reads_a_named_tuple_and_not_only_a_dataclass(module_from):
    """The same refusal, spelled with the other keyword, and it was invisible.

    ``dataclasses.is_dataclass`` is False for a ``NamedTuple``, so a module that
    wraps its diagnosis in one reserved nothing and the completeness check said
    so by finding nothing. The unit's own argument for looking one field down is
    about a record holding the enum, and it does not mention which of the two
    ways to declare one the author picked.
    """
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


@pytest.mark.parametrize("parameter", ["scope", "reason", "cause", "refusal", "remedy"])
def test_renaming_a_parameter_cannot_turn_context_into_a_cause(module_from, parameter):
    """The false positive was not killed last round, it was MOVED to the name.

    Reading the role from the parameter name made the answer depend on a word.
    Spelling this exception's parameter ``reason`` made the walk demand that
    ``item``, ``run``, ``session`` and ``source`` be reserved as exit codes, and
    the only way out of a nonsense demand is to weaken the check. The
    classification lives on the ENUM now, so all five spellings agree.
    """
    module = module_from("context", _context_carried_on_a_refusal(parameter))
    assert refusal_causes_in(module, packages=FIXTURE_PACKAGES) == {}


@pytest.mark.parametrize("parameter", ["status", "verdict", "refusal", "problem"])
def test_renaming_a_parameter_cannot_hide_a_cause_either(module_from, parameter):
    """And the other direction, which is the one that lost a live refusal.

    ``preflight.LibraryVolumeError`` calls its parameter ``status``, so a
    name filter dropped it and seven unreserved refusal causes with it, silently.
    """
    source = SEEN_A_DISCRIMINATOR_NOBODY_CALLED_REFUSAL.replace("verdict", parameter)
    module = module_from("named", source)
    derived = refusal_causes_in(module, packages=FIXTURE_PACKAGES)
    assert frozenset().union(*derived.values()) == {"tagger-art-rejected"}


def test_the_live_refusal_a_name_filter_dropped_is_seen_again():
    """Excluded by DECISION now, and the decision is provable by lifting it.

    ``LibraryVolumeError`` takes a ``MountStatus``, a record holding the
    ``MountState`` that is the actual cause, and its parameter is called
    ``status``. It was missed twice over and the result was silence: seven
    refusal causes, none of them reserved, and no test with anything to say. With
    the exclusion lifted the walk sees it, which is what makes the entry in
    ``CONVERTED_ELSEWHERE`` an argument rather than an accident.
    """
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
    """An exclusion that names nothing is an excuse nobody can check.

    Classifying by enum identity only works while the identities are real. A
    renamed or deleted enum would otherwise leave its reason sitting here looking
    like a decision somebody still stands behind.
    """
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
def wait_for(step):
    if step == "library-scan":
        seconds = 30
        return seconds
    return 0
"""

# ── Correct code whose integers sit INSIDE the reserved range ───────────────
#
# The round before this narrowed a bare integer to 10 through 59 and shipped
# seven fixtures that all used integers BELOW ten, so the narrowing was never
# tested against the case it was supposed to decide. Every one of these keys is
# kebab-shaped and none of them is a cause anybody declared, which is what keeps
# the guard silent. Under the shape-only rule every single one fired.

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
# Once a string IS a declared cause, an integer in the reserved range beside it
# cannot be told from a reservation by shape alone. This one is a backoff and it
# is reported. Pinned as a fixture so the limit is a decision somebody made and
# can find, rather than a surprise the next author meets in a failing build.

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
# The case the table exists to prevent, and the case a guard keyed on the
# existing registry cannot see: a new module deciding its own codes. Every one
# of these passed the first version of the guard.
#
# Each one DECLARES its causes, in its own enum, exactly as the four modules in
# the tree that carry a refusal vocabulary do. That declaration is what makes the
# key a cause rather than a kebab-shaped string, and it is why the guard can see
# a module whose exception nobody has written yet. The other route in, the
# package-wide derivation, is driven separately below over the same source with
# the declaration removed.

DECLARES_ITS_CAUSES = """
from enum import StrEnum


class Refusal(StrEnum):
    SOURCE_UNREADABLE = "tagger-source-unreadable"
    ART_REJECTED = "tagger-art-rejected"
    LOOKUP_UNAVAILABLE = "tagger-lookup-unavailable"

"""

# ── HOW AN ENUM IS RECOGNIZED, in the two spellings that tell the rules apart ──
#
# Every enum base written anywhere in `tests/` was one of three, `Enum`,
# `StrEnum` and `IntEnum`, so the shipped rule, "the base's spelling ends in
# Enum", could not be told apart by measurement from an exact list of those
# three: narrowing it to that list killed ZERO of 3379 while the docstring beside
# it rejected exactly that kind of rule. These two fixtures are the disagreeing
# cases, one for each clause, and each one is silent under the other clause
# alone.

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

#: A ZIP THAT IS NOT A PAIR OF SEQUENCES. ``_zipped`` refuses any call whose
#: argument count is not two, and nothing drove it: dropping the refusal left the
#: suite green while this source raises ``IndexError`` out of the walk, because
#: the second argument it then reads is not there. ``zip`` of one iterable is
#: ordinary Python and a source somebody writes.
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
#
# A bare 30 in a mapping tells a reader nothing about which band it belongs to,
# so the natural spelling puts it behind a constant. Every one of these was
# silent while the inlined integer fired, which is the guard rewarding the
# careless spelling and excusing the careful one.

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
# cli/exit_codes.py declares its table as a TUPLE OF DATACLASSES with a note on
# each entry. A guard that accepted a two-element pair and nothing longer could
# not see the house style it was written to protect.

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
# ``core.cause.REASONS`` gives a code to one hundred and twenty eight slugs and
# this table repeats seventeen of them, so one hundred and eleven of the
# registry's reservations are outside the reserved table entirely. A module
# contradicting one of those is the same defect as a module contradicting this
# table.
#
# THESE THREE NUMBERS WERE MEASURED, and the two they replace had drifted a long
# way. This comment said sixty one, one and sixty, which were the values when it
# was written and were already wrong by sixty, by nine and by fifty one before
# U44 appended anything. Derive them rather than reading them here: the counts
# are ``len(REASONS)``, ``len(set(REASONS) & set(reserved_codes.RESERVED_CAUSES))``
# and the difference. U44's seven mastering slugs are the last to move them, and
# they moved the first two only, because all seven were already reserved.
#
# THE SIXTEEN SHAPES BELOW ARE WHAT THE TIERS COST. Round four accepted only an
# ``ExitCode`` member or a conversion round one for these sixty keys, on the
# strength of an over fire that does not occur in this repository. Every shape
# here is ordinary Python a module would write and every one of them is a second
# opinion about a live registry reservation. Measured by re-implementing round
# four's gate and running it over this exact tuple: it reports TWO of the sixteen
# and is silent on FOURTEEN. The wide rule reports all sixteen.

EVASION_A_NAMED_CODE_FOR_A_REGISTRY_SLUG = """
from cratekit.core.exit_codes import ExitCode

CODES = {"config-unusable": ExitCode.LIBRARY_UNAVAILABLE}
"""

EVASION_A_CONVERSION_ON_A_REGISTRY_SLUG = """
from cratekit.core.exit_codes import ExitCode

CODES = {"credential-missing": int(ExitCode.PRECONDITION)}
"""

# The residual "The tiers were bought with a number that does not exist"
# said tier two accepted "a conversion wrapped round" the vocabulary. It did
# not. These two ARE that spelling and both were silent, and the second is the
# fixture round four added for the fourth entry of the residual
# "One check in this unit is unreachable", only ever run with a key the
# narrow tier did not apply to.
EVASION_A_CONSTRUCTOR_ON_A_REGISTRY_SLUG = """
from cratekit.core.exit_codes import ExitCode

CODES = {"config-unusable": ExitCode(30)}
"""

EVASION_A_CONSTRUCTOR_THROUGH_THE_MODULE_ON_A_REGISTRY_SLUG = """
from cratekit.core import exit_codes

CODES = {"config-unusable": exit_codes.ExitCode(30)}
"""

# A module declaring its OWN status enum is the most flagrant second table there
# is, and for sixty of the eighty two keys it was invisible.
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

# The input round four used to REJECT narrowing to the eighteen live integers,
# with the flaw its own scheme had: a registry-only slug and a code no
# ``ExitCode`` member uses.
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
# The class docstring claimed verbatim that "a code reached through a NAME, a
# class attribute ... all of which resolve here, because naming a constant is
# what a careful author does". Neither tier resolved either of these, with a
# fully reserved cause, because ``resolve_int``'s attribute branch reads only
# classes defined in THIS source and an imported enum member is not one. No
# evasion is needed to write them.

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

# The deepest spelling the hop bound promises to read: a code named, named
# again, and then adjusted. Three hops, which is what ``MAX_HOPS`` is set to.
EVASION_A_CODE_NAMED_TWICE_THEN_ADJUSTED = DECLARES_ITS_CAUSES + """
BASE = 30
OFFSET = BASE

CODES = {"tagger-art-rejected": OFFSET + 1}
"""

# ── Ordinary code keyed on a registry slug, with integers that MATTER ───────
#
# THIS IS THE RESIDUAL, not a silence. Every construct here is ordinary and every
# one of them is reported, because a poll interval of 30 keyed on a cause slug is
# indistinguishable by shape from a reservation of 30. Round four made these
# silent by narrowing the key set, and measured against the sixteen fixtures in
# ``REGISTRY_SLUG_SECOND_TABLES`` that narrowing reported two and went silent on
# fourteen. They are loud instead, and the answer to one that is genuinely not a
# reservation is a decision recorded here, not a comment on the line.

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

#: THE SAME RESIDUAL, KEYED ON A NAME RATHER THAN ON AN INLINE STRING, which is
#: the tree's own dominant idiom and which the fixture above does not contain one
#: instance of.
#:
#: Measured off the syntax tree, every hit-producing construct in
#: ``RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS`` uses an inline string key,
#: so the fixture that documents the wide rule's false alarm surface documented
#: exactly the half of it that predates the key widening. The widening moved the
#: RESOLVER, and the measurement that justified it, 189 kebab literals with 108
#: not keys and zero new offenders, was taken on the KEY SET.
#:
#: ``TrackOutcome`` is not invented. It is copied from
#: ``src/cratekit/acquire/adapter.py``, where a ``StrEnum`` declares cause-shaped
#: values that the registry also reserves. Measured on the shipped tree, TEN
#: modules hold a name the key side resolves to a registry-declared cause and
#: FOURTEEN hold one once a source's own enum declarations are counted, four of
#: those fourteen also holding an in-range integer literal. The tree has zero
#: offenders today and one ordinary mapping in any of those four is what an
#: offender looks like.
#:
#: KEPT AS A FIXTURE RATHER THAN NARROWED AWAY for the same reason as the one
#: above: the alternative is a key rule that reads an inline string and not the
#: name holding it, which is one question with two answers decided by spelling.
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

#: THE SAME CONSTRUCTS WITH THE ROUND-BEFORE'S ESCAPE COMMENT ON EACH, and every
#: one of them is still reported. The comment is text now. It is kept as a
#: fixture rather than deleted because deleting it would leave nothing watching
#: the deletion: this source is what fails if any per-line off switch comes back,
#: in this spelling or another.
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

#: THE THREE SPELLINGS THAT MADE THE ESCAPE AN OFF SWITCH FOR THE WHOLE GUARD.
#: Each was measured against the round before's implementation and each is here
#: so the measurement is repeatable rather than a sentence in a commit message:
#: the one line ``def`` silenced its own body, the semicolon silenced two
#: statements on one reason, and one comment on the opening line of a sixty key
#: mapping silenced every key in it. All three are reported now.
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
# The two-level spelling was recognized and the one-level spellings were not,
# because the rule matched the last two elements of a name a sibling import does
# not have. A module inside ``core`` writing ``from .exit_codes import ExitCode``
# is the most natural spelling there is, and it is the neighbourhood a second
# table would most plausibly appear in.

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

# A level Python refuses outright. Five dots from a three-element package walks
# off the top of the tree, and the resolver has to say so, because the slice that
# computes the base is NEGATIVE at that point and Python's slicing hands back a
# shorter package rather than raising. See the test below for what that base
# happens to be.

EVASION_A_RELATIVE_IMPORT_THAT_WALKS_OFF_THE_TOP = """
from .....exit_codes import ExitCode

CODES = {"rclone-missing": ExitCode.PRECONDITION}
"""

# ── The conversion spellings the unreachability residual called unreachable ──
#
# Both of these are ordinary Python that no fixture happened to write, which is
# not the same thing as unreachable, and round three's comments said the second
# while meaning the first.

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
# The branch walk read the body's TOP LEVEL statements, so a return behind any
# further condition was silent while the flat spelling fired. No evasion is
# needed to write this: checking something else before answering is the ordinary
# way the second case of a table gets written.

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

# ── A NEGATIVE STATUS, which nothing in this suite could see until now ──────
#
# `cli/exit_codes.py` argues about negative statuses at length: the shell reader
# and the job engine's `subprocess.returncode` reader disagree about what one
# MEANS, and the module's answer is that nothing it reserves is ever negative.
# The only guard watching for a bare status could be blinded to every negative
# by either of two one-line edits, and both were silent, because no fixture
# anywhere wrote one.

# ── Four binding shapes ProcessExits handles and no fixture drove ──────────
#
# Each of these was found by the eighth round's mutation table: the arm that
# reads it could be deleted with ZERO deaths, so the shape was handled by code
# nothing watched.

#: The fixed point matters here and nowhere else in the suite, and WHICH
#: spelling needs it is the opposite of the obvious one. ``_walk_scope`` pops its
#: stack, so it yields a scope's statements in REVERSE source order, and the
#: assignments arrive at the binder backwards. A chain written in dependency
#: order, ``later = sys.exit`` and then ``stop = later``, therefore reaches the
#: binder as ``stop`` first, learns nothing about it on the first pass, and needs
#: the second. The version of this fixture written the other way round, which
#: looks like the one that needs a fixed point, is settled in a single pass and
#: measured ZERO deaths.
EVASION_AN_EXIT_ALIASED_A_SECOND_TIME = """
import sys

later = sys.exit
stop = later

def refuse():
    stop(30)
"""

#: ``importlib.import_module`` held in a NAME, which the binding walk records as
#: an importer. Only the inline spelling was driven.
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

#: TWO ARGUMENTS IS NOT A STATUS, and this one is a correctness fixture rather
#: than an evasion. ``SystemExit(30, "detail")`` sets ``code`` to the TUPLE, and
#: a process raising it exits 1 with the tuple printed, so reporting it as
#: "status 30" would name a status the program never returns.
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
    """The case the table exists to prevent, and the case the guard could not see.

    Keying on the causes ALREADY reserved made the guard blind to a module that
    decides codes for causes nobody has reserved, which is not a corner of the
    problem, it is the problem. Eleven shapes, every one of them ordinary Python
    somebody would write without meaning to evade anything, and every one of them
    silent before.
    """
    assert reserved_code_tables(source, CAUSES, RANGE)


def test_an_enum_is_recognized_by_its_base_and_each_clause_has_its_own_case():
    """The rule that could not be told apart from a list of three names.

    ``_declared_enum_values`` decides what a module has DECLARED to be a cause,
    and everything downstream of that decision, the whole key set for a module
    whose exception nobody has written yet, rests on how it recognizes an enum.
    It recognized one by the SPELLING of the base, ``endswith("Enum")``, and its
    docstring set that against a rule "a rename changes nothing" while being one:
    an aliased import defeats a spelling. Measurement could not see the
    difference either, because every enum base written anywhere in ``tests/`` was
    ``Enum``, ``StrEnum`` or ``IntEnum``: narrowing the suffix to exactly those
    three killed zero of 3379.

    So there are two clauses and each one has the case only it answers.

    * ``from enum import StrEnum as Vocabulary`` binds the base to a name no
      spelling rule matches. Only the IMPORT clause answers it, and that clause
      is what the rest of this file already does everywhere else: ask what the
      source BOUND, never what it spelled.
    * ``class Refusal(CratekitEnum)`` against a base defined in another of our
      modules imports nothing from ``enum`` at all. Only the SPELLING clause
      answers it, and it is the clause the three-name narrowing removed.

    The plain class is the P7 direction. A class body full of string constants is
    ordinary, it is what ``EVASION_A_KEY_HELD_ON_A_CLASS`` is built on, and
    reading one as a declaration would let any module invent causes by writing
    constants.
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
    """The docstring's own claim, driven rather than asserted.

    ``_declared_enum_values`` claims it matches on the base and not on what the
    class or the variable was called. Nothing measured that, and the claim is
    exactly the kind this file's own record keeps finding to be false. Each
    rename below is applied to a fixture whose ONLY route into the key set is its
    own declaration, so a rename that broke the rule would take the hit with it.
    """
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
        # The base alias is spelled twice, at the import and at the base, and
        # renaming it means renaming BOTH or the fixture stops being valid
        # Python. That is why the pair above is the bare name rather than the
        # ``as`` clause: a substitution that renamed only the import would leave
        # a base bound to nothing and would prove the wrong thing.
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
    """One recognized relative spelling out of three is a bug, not a scope decision.

    The rule matched the last two elements of the imported name, which a sibling
    import does not have: ``from .exit_codes import ExitCode`` records
    ``exit_codes`` and ``from . import exit_codes`` records nothing at all. So
    the two spellings a module sitting BESIDE ``core/exit_codes.py`` would
    actually use were the two the guard could not read, while the two-level
    spelling from further away worked. Each of these maps a fully reserved cause
    to a real code and reported nothing.
    """
    assert reserved_code_tables(source, CAUSES, RANGE)


def test_a_relative_import_is_resolved_against_the_package_the_file_sits_in():
    """Resolving the level is what makes the relative answer match the absolute one.

    ``from . import exit_codes`` means a different module in ``core`` than it
    does in ``cli``, and the second one binds the reservation table, which this
    guard has always left alone because reading the table is the sanctioned path.
    A suffix match cannot tell those apart. Resolving the level can, and it is
    the same answer Python gives.
    """
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
    """The clause the assertion above was credited with covering, driven properly.

    ``_relative_module`` computes its base as ``parts[:len(parts) - (level - 1)]``
    and Python's slicing does not raise when that index goes negative: it hands
    back a SHORTER package. With a file in ``cratekit.core.sub`` and five dots
    the index is ``-1``, the base becomes ``cratekit.core``, and the walk would
    resolve an import the interpreter refuses outright onto the exact module it
    is hunting. Not silence, and not a stray extra line either: a REPORTED
    offender in a module that cannot import.

    Both halves are here because the unit answer and the end to end answer fail
    differently. The resolver has to return None, and the guard built on it has
    to stay quiet, and round three's version of this proof asserted neither.
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
    """The first entry of the residual
    "One check in this unit is unreachable", asserted rather than
    reasoned about.

    ``isinstance(True, int)`` is True in this language, and the guards ask for
    integers. Round three's comment said nothing in the tree or the fixtures maps
    a cause to a boolean; ``CORRECT_A_RETRY_FLAG_PER_CAUSE`` maps one cause to
    ``True`` and another to ``False``, and instrumenting the line counted 464
    booleans arriving in a single suite run. What was true is that it changes no
    outcome, because 1 and 0 are both below the reserved range, which is a fact
    about the RANGE and not about this line. Asserted here so the line is covered
    by something other than an argument about the range.
    """
    assert _guards.resolve_int(ast.parse("True").body[0].value, {}, {}) is None
    assert _guards.resolve_int(ast.parse("False").body[0].value, {}, {}) is None
    assert _guards.resolve_int(ast.parse("30").body[0].value, {}, {}) == 30
    assert reserved_code_tables(CORRECT_A_RETRY_FLAG_PER_CAUSE, CAUSES, RANGE) == []


def test_a_conversion_is_read_through_the_module_name_as_well_as_the_class_name():
    """The fourth entry of the residual
    "One check in this unit is unreachable", which was ordinary
    Python nobody had written down.

    ``exit_codes.ExitCode(30)`` is the module-qualified spelling of the same
    conversion as ``ExitCode(30)``, and a module that imported the vocabulary as
    a module rather than a class writes it that way without thinking about it.
    Without the module-qualified branch the call is not a conversion, the guard
    falls through to resolving a ``Call`` as an integer, gets nothing, and says
    nothing about a table that reserved 30 for a fully reserved cause.
    """
    assert reserved_code_tables(
        EVASION_A_CONVERSION_THROUGH_THE_MODULE_NAME, CAUSES, RANGE
    ) == ["line 4: 'rclone-missing' -> exit_codes.ExitCode(30)"]


def test_a_two_argument_call_is_not_a_conversion():
    """The third entry of the residual
    "One check in this unit is unreachable": the narrowing that keeps
    this off somebody's constructor.

    A conversion takes one argument. A call taking a code and a sentence is a
    constructor, and reading its first argument as a status would report a module
    that reserved nothing, which is the false positive that gets a guard switched
    off for a whole file (P7). Round three called this narrowing unreachable and
    said widening it killed nothing; both halves were wrong, and dropping the
    ``len(node.args) == 1`` test reports this fixture.
    """
    assert (
        reserved_code_tables(CORRECT_A_TWO_ARGUMENT_CALL_IS_NOT_A_CONVERSION, CAUSES, RANGE)
        == []
    )


def test_a_status_with_a_conversion_round_it_still_reaches_the_shell():
    """The second entry of the residual
    "One check in this unit is unreachable", and the one that is a live
    bypass rather than a nicety.

    ``sys.exit(int(PRECONDITION))`` ends the process with 30 exactly as
    ``sys.exit(30)`` does. ``process_status_literals`` resolves the argument of
    every single-argument call it walks, so the conversion arrives at
    ``resolve_int`` rather than at the table guard's own conversion branch, and
    without the ``int(...)`` clause there it resolves to nothing and the guard
    goes quiet on a real bypass. Round three called that clause unreachable;
    instrumenting it counted 25 arrivals in one suite run.
    """
    assert process_status_literals(EVASION_A_STATUS_WITH_A_CONVERSION_ROUND_IT) == [
        "line 8: sys.exit(int(PRECONDITION)) (status 30)"
    ]


def test_the_derivation_refuses_to_answer_from_an_incomplete_walk(monkeypatch):
    """The sixth entry of the residual
    "One check in this unit is unreachable", driven by making the walk
    incomplete.

    The assertion inside ``structured_refusal_causes`` is duplicated by
    ``test_every_module_in_the_package_imports_so_the_walk_can_see_it``, so
    deleting it kept the suite green, which is exactly why it read as decoration.
    It is not decoration: it stops any CALLER of the derivation from reading a
    short answer as a complete one, and the only way to show that is to hand the
    caller a short answer.
    """
    monkeypatch.setitem(
        globals(),
        "imported_package_modules",
        lambda: ([], {"cratekit.modules.tools.backup": "No module named 'boto3'"}),
    )
    with pytest.raises(AssertionError, match="invisible to the completeness"):
        structured_refusal_causes()
    monkeypatch.undo()
    assert structured_refusal_causes(), "the walk did not come back after the swap"


def test_the_guard_bites_through_the_derivation_when_the_file_declares_nothing():
    """The second route to the same answer, with the local declaration removed.

    A module can keep its table in one file and its enum in another, so the key
    set is the union: what this file declares, plus what the package-wide walk
    derived. With the enum stripped out the source says nothing about what a
    cause is, and the guard still bites once the derived set reaches it.
    """
    source = EVASION_A_NEW_MODULE_DECIDES_ITS_OWN_CODES.replace(DECLARES_ITS_CAUSES, "")
    assert "Refusal" not in source
    assert reserved_code_tables(source, CAUSES, RANGE) == []
    elsewhere = CAUSES | frozenset({"tagger-source-unreadable", "tagger-art-rejected"})
    assert reserved_code_tables(source, elsewhere, RANGE)


def test_a_mutually_recursive_pair_of_constants_resolves_to_nothing():
    """``MAX_HOPS`` was load bearing downward only, and its docstring claims both.

    Lowering it stops the guard resolving the careful spellings and kills seven
    tests, so the floor was covered. The ceiling was not: the constant says it is
    bounded "so a mutually recursive pair of constants cannot hang the suite" and
    nothing drove such a pair, so raising it to anything above the interpreter's
    own recursion limit turned ``A = B`` beside ``B = A`` into a
    ``RecursionError`` that takes the run down, which is the failure the bound
    exists to prevent. Driven here in both halves: the pair resolves to nothing
    rather than raising, and a table keyed on it reports nothing rather than
    reporting a guess.
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
    """Once a string IS a cause, a duration in range reads as a status.

    Reported on purpose. The alternative is matching on the variable's name, and
    a guard a rename defeats is not a guard. What keeps this small is the key
    rule: it can only happen for a string somebody already declared to be a
    refusal cause, never for the 66 kebab-keyed pairs the tree holds today.
    """
    hits = reserved_code_tables(RESIDUAL_A_BACKOFF_ON_A_REAL_CAUSE, CAUSES, RANGE)
    assert hits == ["line 2: 'rekordbox-running' -> status 30"]


#: Every shape a module would plausibly use to give a registry-only slug a code
#: of its own. Measured against round four's gate re-implemented verbatim: TWO
#: are reported and FOURTEEN are silent, and the narrowing was bought with an
#: over fire the tree does not have. See the residual
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
    """The sixteen shapes, and fourteen of them were silent for a whole round.

    Round four carried the registry's sixty slugs in a tier that accepted only an
    ``ExitCode`` member or a conversion round one, and the residual
    "The tiers were bought with a number that does not exist" described that as
    "an ``ExitCode`` member in any import spelling or a conversion wrapped round
    one". Measured, the description was wrong about its own rule: ``ExitCode(30)``
    is a conversion wrapped round the vocabulary and was not reported, and
    neither was the module-qualified spelling of it that round four itself added
    as a fixture. A module declaring its own ``IntEnum`` was invisible. So was a
    named constant, so was arithmetic, so was every table shape this file already
    proves for the other twenty two keys.

    THE COUNT IS MEASURED, not counted by eye. Round five wrote three different
    numbers for this one measurement in one commit, thirteen, fifteen and
    "fifteen of fifteen with NONE reported", and none of them was right. Round
    four's gate re-implemented and run over this exact tuple reports the named
    code and the conversion, TWO, and is silent on the other FOURTEEN. All
    sixteen are reported now, which is what one key set and one value rule buys.
    """
    assert reserved_code_tables(source, declared_causes(), RANGE)


def test_the_alternative_is_not_rejected_for_a_flaw_this_scheme_shares():
    """The exact input used to reject narrowing to the eighteen live integers.

    ``ReservedCodeTable`` rejects that alternative because it "blinds the guard
    to a new module inventing 33". Under round four's tiers ``{"tree-registry-
    unusable": 33}`` was not reported either, for sixty of the eighty two keys,
    so the shipped scheme was rejecting an option for a hole it had itself.
    Driven here so the rejection stays honest.
    """
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
    """The capability the class docstring claimed and neither tier had.

    ``CODE = ExitCode.PRECONDITION`` beside ``{"rclone-missing": CODE}`` gave
    zero hits with a FULLY RESERVED cause. ``resolve_int`` chases a name to an
    integer and its attribute branch reads ``_class_level_literals``, which only
    records classes declared in the source being read, so a member of an imported
    enum resolved to nothing. Nobody has to intend that spelling as an evasion.
    It is what a careful author writes, and the docstring above the guard said it
    resolved for three rounds while it did not.
    """
    assert reserved_code_tables(source, CAUSES, RANGE)


def test_the_reported_text_keeps_both_spellings_of_a_code_reached_by_name():
    """A hit a reader can chase needs the name AND what it held."""
    assert reserved_code_tables(
        EVASION_A_VOCABULARY_MEMBER_HELD_IN_A_CONSTANT, CAUSES, RANGE
    ) == ["line 6: 'rclone-missing' -> ExitCode.PRECONDITION as CODE"]


#: THE KEY SIDE OF THE SAME QUESTION. The value rule chases a code through a
#: module constant and a class attribute because "a bare 30 in a mapping tells a
#: reader nothing". The key rule required a literal, so the identical spelling on
#: the other side of the colon was invisible. The package carries 37 class
#: attributes whose value is a declared cause, so this is the tree's own idiom.
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

#: A name that is NOT a cause stays not a cause. Resolving the key widens what
#: the guard can read, never what counts as a declaration.
CORRECT_A_KEY_HELD_IN_A_CONSTANT_THAT_IS_NOT_A_CAUSE = """
COLUMN = "column-width"
WIDTHS = {COLUMN: 40}
"""

#: The record written as a mapping, which is the house style with a dict instead
#: of a dataclass. ``cli/exit_codes.py`` declares its own table as a tuple of
#: three-field dataclasses and the guard reads that; the dict spelling of one
#: record was the third way to write it and the one way to write it unseen.
EVASION_A_LIST_OF_RECORD_DICTS = """
RESERVATIONS = [
    {"cause": "config-unusable", "code": 30},
    {"cause": "credential-missing", "code": 40},
]
"""

#: The vocabulary reached by a string. The bare-status guard has recognized
#: ``getattr(sys, "exit")`` since round two and called it the shape that matters
#: most; this half of the same file did not recognize the same shape.
EVASION_A_CODE_FETCHED_BY_GETATTR = """
from cratekit.core.exit_codes import ExitCode

CODES = {"config-unusable": getattr(ExitCode, "PRECONDITION")}
"""

CORRECT_GETATTR_FOR_A_CODE_ON_SOMEBODY_ELSE = """
import settings

CODES = {"config-unusable": getattr(settings, "PRECONDITION")}
"""

#: ``//`` and ``%``. The guard read ``+``, ``-`` and ``*`` and went silent on the
#: other two, which is one question answered two ways inside one function.
EVASION_A_CODE_REACHED_BY_FLOOR_DIVISION = """
BASE = 60
CODES = {"config-unusable": BASE // 2}
"""

EVASION_A_CODE_REACHED_BY_A_REMAINDER = """
BASE = 130
CODES = {"config-unusable": BASE % 100}
"""

#: SUBTRACTION AND MULTIPLICATION, in range. Both limbs shipped with nothing
#: driving them: the only multiplication fixture was
#: ``RESIDUAL_ARITHMETIC_OUT_OF_RANGE``, whose product is 70 and whose assertion
#: expects SILENCE, so deleting the limb changed nothing there, and there was no
#: subtraction fixture at all. A limb exercised only through an assertion that
#: expects nothing cannot die.
EVASION_A_CODE_REACHED_BY_SUBTRACTION = """
BASE = 71
CODES = {"config-unusable": BASE - 41}
"""

EVASION_A_CODE_REACHED_BY_MULTIPLICATION = """
BASE = 15
CODES = {"config-unusable": BASE * 2}
"""

#: A DIVISION THAT DOES NOT RUN. ``resolve_int``'s comment claims division by
#: zero "is a source that does not run, so it resolves to nothing rather than
#: raising inside a test", and nothing measured it: dropping the ``right != 0``
#: term left the whole suite green, because no fixture divided by zero. Without
#: the term this fixture raises ``ZeroDivisionError`` inside the walk.
CORRECT_A_DIVISION_BY_ZERO_RESOLVES_TO_NOTHING = """
BASE = 60
CODES = {"config-unusable": BASE // 0}
"""

#: A CODE HELD IN AN ANNOTATED CONSTANT, which is the house style: this
#: repository's own registry is written ``REASONS: Mapping[str, ExitCode] =
#: MappingProxyType(``. Both literal collectors read an ``ast.AnnAssign`` and
#: neither arm had a fixture, so both could be deleted in silence.
EVASION_A_CODE_HELD_IN_AN_ANNOTATED_CONSTANT = """
PRECONDITION: int = 30

CODES = {"config-unusable": PRECONDITION}
"""

EVASION_A_CODE_HELD_ON_AN_ANNOTATED_CLASS_ATTRIBUTE = """
class Status:
    PRECONDITION: int = 30


CODES = {"config-unusable": Status.PRECONDITION}
"""

#: AN ANNOTATED ENUM MEMBER, which the interpreter treats as a member exactly as
#: the unannotated spelling does. ``_declared_enum_values`` reads one and nothing
#: drove that arm either.
EVASION_AN_ANNOTATED_ENUM_MEMBER_IS_A_DECLARATION = """
from enum import StrEnum


class Refusal(StrEnum):
    ART_REJECTED: str = "tagger-art-rejected"


CODES = {"tagger-art-rejected": 41}
"""

#: A KEY held three aliases deep. ``_through_names`` carries its own bound and
#: ``resolve_int`` carries another; only the value side was ever driven at the
#: boundary, so raising the key side's bound alone changed nothing.
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

#: A duplicate key inside a SECOND table. Python resolves it silently and the
#: walk sees two pairs carrying the same line, slug and status, so without the
#: dedupe the guard reports the same reservation twice and the count in the
#: failure message is wrong.
EVASION_A_DUPLICATE_KEY_IN_A_SECOND_TABLE = """
CODES = {"config-unusable": 30, "config-unusable": 30}
"""

#: What ``MAX_HOPS`` at three buys and what it gives up. Two aliases resolve and
#: three do not, and the second is a COST of the number rather than a property of
#: the guard, so both are pinned.
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
# ``cause_key`` learned to read a name and FOUR constructs inherited it. Two did
# not, because each pre-filtered its own subtree to ``ast.Constant`` before
# asking: the ``if`` arm of ``_branches`` and a dict comprehension's iterable.
# The ``match`` arm passed its pattern value in unfiltered and did inherit it, so
# one table written two ways got two answers from one method. The pairs below are
# kept together on purpose: a spelling that goes quiet alone is what this shape
# looks like coming back.

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

#: The direct twin of the first one, and the one that WAS reported. Driven beside
#: it so the two cannot disagree again without failing.
EVASION_A_MATCH_AGAINST_A_CLASS_ATTRIBUTE = """
class Slug:
    CONFIG_UNUSABLE = "config-unusable"


def code(cause):
    match cause:
        case Slug.CONFIG_UNUSABLE:
            return 30
    return 0
"""

#: The literal spelling, which was reported throughout. It is the control that
#: says the branch machinery was live and only the KEY was unread.
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
# ``{"config-unusable": ExitCode.SUCCESS}`` was reported and
# ``{"config-unusable": ExitCode(0)}`` was silent, because the conversion branch
# only returned when the inner expression was ALREADY a status and an out of
# range integer is not one. One vocabulary, two answers, decided by the spelling.

EVASION_A_CONSTRUCTOR_ON_A_CODE_BELOW_THE_RANGE = """
from cratekit.core.exit_codes import ExitCode

CODES = {"config-unusable": ExitCode(0)}
"""

EVASION_A_CONSTRUCTOR_ON_A_CODE_ABOVE_THE_RANGE = """
from cratekit.core.exit_codes import ExitCode

CODES = {"config-unusable": ExitCode(126)}
"""

#: The narrowing that keeps the widening off ordinary code. ``cli/output.py``
#: writes exactly this, reading a recorded status back out of a document, and it
#: reserves nothing.
CORRECT_A_CONSTRUCTOR_ON_A_RUNTIME_VALUE = """
from cratekit.core.exit_codes import ExitCode


def read(document):
    return {"config-unusable": ExitCode(document["exit_code"])}
"""

#: An INTEGER out of range, reached three ways. All three are silent and that is
#: the range decision rather than a hole, so all three are pinned: the record
#: claimed a constant and arithmetic reaching an out of range value were still
#: reported, and arithmetic can produce nothing but an integer.
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
    """The largest hole this guard had, and it was on the side nobody looked at.

    ``cause_key`` required an ``ast.Constant``, so the guard resolved the VALUE
    through names, class attributes, a module's own enum and arithmetic, with
    three mutation rows driving it, and never resolved the KEY at all. The
    argument the round before made for reading the careful spelling of a code,
    that a bare 30 in a mapping tells a reader nothing, is symmetric and was
    applied to one side only. Both of these gave ZERO hits while their inlined
    spelling gave one.
    """
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
    """The fifteenth shape, and it is the direct twin of one already closed.

    ``_branches`` has two arms and they disagreed. The ``match`` arm passed its
    pattern value into ``cause_key`` unfiltered and inherited the key widening;
    the ``if`` arm filtered its test to ``ast.Constant`` first and did not.
    Measured on the shipped tree, ``case Slug.CONFIG_UNUSABLE`` was REPORTED and
    ``if cause == Slug.CONFIG_UNUSABLE`` was SILENT, which is one method
    answering one question two ways over a spelling difference that means
    nothing. All four are the same table.
    """
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
    """The sixteenth shape, and the second construct the widening reached past.

    ``{slug: 30 for slug in (CONFIG_UNUSABLE, SMOKE_TEST_FAILED)}`` was SILENT
    while the identical comprehension over inlined slugs reported both keys, for
    the same reason the ``if`` arm was silent: the iterable was filtered to
    ``ast.Constant`` before anything asked whether a name held a cause.
    """
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
    """The range gates an INTEGER. It never gated the vocabulary, and it did.

    ``{"config-unusable": ExitCode.SUCCESS}`` was reported and
    ``{"config-unusable": ExitCode(0)}`` was silent, because the conversion
    branch returned only when the inner expression was already a status and
    ``status`` answers None for an out of range integer. A member and its
    constructor spelling are the same code, so the range decision cannot apply to
    one of them.
    """
    assert reserved_code_tables(source, declared_causes(), RANGE) == [
        f"line 4: 'config-unusable' -> {spelled}"
    ]


def test_a_constructor_wrapping_a_runtime_value_reserves_nothing():
    """The narrowing that keeps the widening above off ordinary code.

    ``cli/output.py`` reads a recorded status back out of a document with exactly
    this call. A rule that read any one-argument call on the vocabulary as a
    reservation would report it, which is the false alarm that gets a guard
    switched off (P7). The argument has to RESOLVE to an integer.
    """
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
    """The recorded shape, pinned so the record cannot describe it wrongly again.

    The residual
    "The tiers were bought with a number that does not exist"
    said "an ``ExitCode`` member, a conversion, a constant or arithmetic reaching
    an out of range value is still reported". Measured, that sentence was false
    in three of its four clauses. The member is reported. The conversion is
    reported now and was not. The constant and the arithmetic are SILENT, and
    arithmetic can evaluate to nothing but an integer, so the arithmetic clause
    was unconditionally false rather than false in some cases.

    All three are the SAME rule seen three ways: an integer counts only inside
    the reserved range, because widening past it reports every count, width and
    percent in the package. This drives that rule at its boundary so the sentence
    describing it has to match it.
    """
    assert reserved_code_tables(source, declared_causes(), RANGE) == []


def test_resolving_the_key_widens_what_is_read_and_not_what_is_a_cause():
    """The direction that keeps the widening honest.

    A name resolving to a string nobody declared answers exactly as an undeclared
    literal does. Without this the fix would be a shape rule again, which is what
    round two deleted: any kebab string beside an in-range integer.
    """
    assert reserved_code_tables(
        CORRECT_A_KEY_HELD_IN_A_CONSTANT_THAT_IS_NOT_A_CAUSE, declared_causes(), RANGE
    ) == []
    assert "column-width" not in declared_causes()


def test_a_record_written_as_a_mapping_is_still_a_record():
    """The house style with a dict instead of a dataclass.

    ``_crossed`` reads a record as a tuple and as a constructor call because
    ``cli/exit_codes.py`` declares its own table as a tuple of dataclasses. The
    same record written ``{"cause": ..., "code": ...}`` was silent, so the guard
    could see two of the three ways to write one row.
    """
    assert reserved_code_tables(
        EVASION_A_LIST_OF_RECORD_DICTS, declared_causes(), RANGE
    ) == [
        "line 3: 'config-unusable' -> status 30",
        "line 4: 'credential-missing' -> status 40",
    ]


def test_a_code_fetched_by_getattr_is_still_a_code():
    """One question, two answers, inside one file. Both halves agree now.

    ``ProcessExits`` has recognized ``getattr(sys, "exit")`` since round two and
    its docstring calls it "the one that matters most, because it disarms the
    guard on its own". ``ReservedCodeTable`` did not recognize the identical
    shape aimed at the vocabulary. Narrowed to the class this source imported, so
    a fetch from somebody else's module is not a code.
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
    """``+``, ``-`` and ``*`` resolved and ``//`` and ``%`` did not.

    A guard that reads ``BASE + 3`` and goes silent on ``BASE // 2`` is answering
    one question two ways, which is the defect this file reports in other
    people's code. All five resolve to 30 and all five are reported.

    FIVE LIMBS AND TWO OF THEM WERE UNDRIVEN, which the eighth round's mutation
    table found: deleting the subtraction limb and deleting the multiplication
    limb each killed ZERO. There was no subtraction fixture anywhere, and the
    only multiplication fixture was ``RESIDUAL_ARITHMETIC_OUT_OF_RANGE``, whose
    product is 70 and whose assertion expects silence. A limb exercised only
    through an assertion that expects nothing cannot die, which is this file's
    own recurring defect wearing a different hat.
    """
    assert reserved_code_tables(source, declared_causes(), RANGE) == [
        f"line 3: 'config-unusable' -> status 30 as {spelled}"
    ]


def test_a_zip_of_one_sequence_is_not_a_pair_of_sequences():
    """The argument-count refusal in ``_zipped``, which nothing drove.

    ``dict(zip(SLUGS))`` is ordinary Python. Without the refusal the walk reads a
    second argument that is not there and raises ``IndexError`` into whatever
    called it, which for the tree-wide scan is every file at once.
    """
    assert reserved_code_tables(CORRECT_A_ZIP_OF_ONE_SEQUENCE, CAUSES, RANGE) == []


def test_a_division_by_zero_resolves_to_nothing_rather_than_raising():
    """The claim beside the ``right != 0`` term, which nothing measured.

    ``resolve_int`` says division by zero "is a source that does not run, so it
    resolves to nothing rather than raising inside a test". Dropping the term
    left the suite green because no fixture divided by zero, so the sentence was
    a claim about a path nothing took. Without the term this fixture raises
    ``ZeroDivisionError`` out of the walk and into whatever called it.
    """
    assert reserved_code_tables(
        CORRECT_A_DIVISION_BY_ZERO_RESOLVES_TO_NOTHING, declared_causes(), RANGE
    ) == []


def test_the_house_style_of_an_annotated_assignment_is_read_on_both_sides():
    """``NAME: type = value``, which is how this repository writes a table.

    ``core/cause.py`` declares its registry as
    ``REASONS: Mapping[str, ExitCode] = MappingProxyType(``, so the annotated
    spelling is the tree's own idiom rather than an invented one. Three arms read
    one: the module-level literal collector, the class-level one, and the enum
    declaration walk. All three could be deleted in silence, because every
    fixture in this file wrote the unannotated spelling.
    """
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
    """The boundary on the KEY side, which was never driven at its edge.

    ``_through_names`` chases a key through at most ``MAX_HOPS`` names and
    ``resolve_int`` chases a value through the same number by its own counter.
    Only the value side was pinned at the boundary, so raising the key side's
    bound alone changed nothing anywhere. Both sides read two aliases and give up
    on three, and that has to be one answer rather than two.
    """
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
    """The dedupe, driven rather than assumed. See the residual
    "One check in this unit is unreachable".

    A duplicate key in a mapping literal is the first defect this file's own
    suite hunts, and it reaches the walk as two pairs carrying the identical
    line, slug and status. Dropping the ``seen`` set left every test green
    because nothing wrote one, so the dedupe was code with nothing watching it.
    Reporting one reservation twice makes the count in the failure message wrong,
    and the count is what a reader uses to size the problem.
    """
    assert reserved_code_tables(
        EVASION_A_DUPLICATE_KEY_IN_A_SECOND_TABLE, declared_causes(), RANGE
    ) == ["line 2: 'config-unusable' -> status 30"]


def test_the_hop_bound_is_a_coverage_dial_and_this_is_what_it_gives_up():
    """``MAX_HOPS`` is not a correctness constant, and the docstring said nothing.

    The reduction from six to three was justified with "nothing in the suite
    needed more than two hops", which is absence read as evidence of absence
    applied to a coverage constant. Any finite value below the interpreter's
    recursion limit stops the hang the bound exists to prevent; the value decides
    how long a chain of aliases the guard can read.

    At three it reads at most TWO aliases before the literal. Swept across every
    value from 2 to 6: the two alias chain is reported at all of them, and the
    three alias chain is silent at 2 and 3 and reported at 4, 5 and 6. So the
    boundary sits exactly between 3 and 4, and the three alias chain below is a
    real evasion this guard does not see. That is the price of the number, pinned
    here rather than left to be discovered. Raising the constant to reach further
    fails this test and demands the new boundary be written down the same way.
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
    """``from sys import exit`` needs no attribute access, so it needed no evasion.

    The guard walked ``ast.Import`` alone, so the one import shape that binds the
    function directly went straight past it: the refusal reached the shell as 30
    with no envelope and no remediation, which is the precise defect this exists
    to stop. Both sibling classes in the same file already handled
    ``ast.ImportFrom``.
    """
    assert process_status_literals(source)


def test_a_negative_status_is_a_bare_status_too():
    """A live, wholly uncovered bypass, and the two edits that opened it.

    ``cli/exit_codes.py`` reasons about negative statuses in its own docstring:
    the shell truncates ``exit(-1)`` to 255, which that file closes off by name,
    and the job engine reads ``subprocess.returncode``, where a negative integer
    is the SIGNAL that killed the child. So a module writing ``sys.exit(-1)``
    produces a status that one reader calls the shell's own territory and the
    other calls a signal death, and neither is the refusal that was meant. It is
    the worst bare status in the file, and it was the one nothing wrote.

    TWO EDITS BLIND THE GUARD TO EVERY NEGATIVE, and before this test both were
    silent alone and silent together:

    * deleting ``resolve_int``'s unary-minus branch, after which every negative
      resolves to nothing and a status this cannot evaluate stays silent;
    * widening ``_scan_for_exits``'s ``status == 0`` to ``status <= 0``, after
      which every negative is read as success.

    The three spellings below are the three shapes a real module reaches for: the
    literal, the signal number held in a name, and the raised exception. The
    middle one is the only fixture in this file that drives the unary minus
    THROUGH a name, which is what makes the hop bound part of the answer too.
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
    """The other half of the negative question, and its answer is the range.

    Pinned beside the one above so the two are read together. A second table
    mapping a cause to a negative integer is NOT reported, because the value rule
    for a bare integer is the reserved range and no negative is inside it. That
    is the same rule that keeps 5 and 70 out, and it is why the unary-minus
    branch changes no answer here: with the branch deleted a negative resolves to
    nothing, and with it a negative resolves outside the range, and both are
    silence. The bare-status guard is the whole of what that branch is for, which
    is a composite rather than a sentence: the row that deletes it kills the test
    above and leaves this one green.
    """
    assert reserved_code_tables(
        'CODES = {"config-unusable": -30}\n', declared_causes(), RANGE
    ) == []


def declared_causes() -> frozenset[str]:
    """Every string anybody in this repository has declared to be a refusal cause.

    ONE KEY SET, eighty two strings, and one value rule for all of them. Round
    four split this into a wide declaration and a narrow ``registry_only_causes``
    tier on the strength of a measurement that does not hold: it reported that
    the wide rule fired on "twenty seven of twenty eight ordinary constructs",
    and that count came from a hand written fixture rather than from the package.
    Measured against the real tree under the wide rule, the number of offenders
    outside the two table owners is ZERO. What the split cost was not
    hypothetical, and ``test_the_wide_key_set_reports_what_the_tiers_missed``
    drives all sixteen shapes it was measured against, fourteen of which it
    silenced.

    Three declarations feed it:

    * the reservation table, which is what this file is about;
    * what the completeness walk derived from the package, so a module's table
      for its own brand new causes is seen the moment the module declares them;
    * the closed reason registry, ``core.cause.REASONS``, which
      ``cli/exit_codes.py``'s own docstring calls "the other mapping in this
      repository that gives a slug a code". One hundred and eleven of its one
      hundred and twenty eight slugs are outside the reserved table, so a module
      contradicting one of them is the same defect as a module contradicting
      this table. Both figures are measured; the pair this line used to carry,
      sixty and sixty one, had drifted by fifty one and by sixty.

    A fourth arrives per file rather than here: a cause-shaped string a source
    declares in its own enum, which ``ReservedCodeTable`` adds as it reads.

    THE SECOND ONE CONTRIBUTES NOTHING TODAY and is in the union anyway, which
    is a distinction round four's version could not make: the derived set equals
    ``CAUSES`` exactly, so collapsing this function to ``return CAUSES``
    killed nothing.  ``test_the_key_set_is_the_union_of_all_three_declarations``
    swaps a derivation that finds a new cause and asserts it arrives, which is
    the only way to drive a term that is empty in the tree.

    WHAT IS OUTSIDE THE KEY SET, said rather than implied. ``preflight.MountState``
    spells its seven states with underscores rather than this repository's
    hyphens, and ``core/session.py`` converts every one of them into a slug
    ``REASONS`` reserves before anything refuses. Adding them would put ``"ok"``
    in the key set. The residual
    "Two refusal vocabularies stay outside the second-table guard's key set"
    records the gap and the reason.
    """
    derived = structured_refusal_causes()
    return CAUSES | frozenset().union(*derived.values()) | frozenset(REASONS)


def registry_only_causes() -> frozenset[str]:
    """The sixty slugs the closed registry reserves and the reserved table does not.

    Not a tier any more. It is the part of the key set that round four's
    narrowing switched off, and it is named so the tests that measure what the
    narrowing cost can address exactly those keys.
    """
    return frozenset(REASONS) - CAUSES


def package_of(relative: str) -> str:
    """The dotted package a module's relative imports resolve against.

    ``cli/render.py`` and ``cli/__init__.py`` both answer ``cratekit.cli``,
    because one level up from a module and one level up from a package's own
    ``__init__`` are the same place, which is what Python does.

    Driven by ``test_the_package_a_relative_import_resolves_against_is_derived``
    rather than by the tree scan it feeds. Collapsing it to ``return "cratekit"``
    killed nothing: the scan asserts an absence, so a helper that answers wrongly
    everywhere makes it quieter, and this is the one thing that makes the
    relative-import half of the walk live over real files.
    """
    return ".".join(["cratekit"] + relative.split("/")[:-1])


#: Every residual cited by TITLE anywhere the rule below reaches.
#:
#: THE NUMBERS COLLIDE ACROSS BRANCHES. Six residual numbers currently mean one
#: thing on this branch and something else on another branch in flight, so a
#: citation by number is a citation that silently changes subject at merge. It
#: has already broken once in this wave. A title survives a renumbering; a number
#: does not survive a merge.
#:
#: DECLARED HERE AND SCANNED FOR, and the two are asserted EQUAL rather than one
#: being checked against the document alone. The round before proved every
#: declared title resolves to a heading and never proved that a title WRITTEN in
#: a file is declared, so an invented or drifted title passed silently in the one
#: direction that matters: seven citations existed, all seven resolved, and an
#: eighth with a typo would not have failed.
CITED_RESIDUALS = (
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
    # Declared on the U38 merge, 2026-08-10. This title belongs to U34 and is
    # cited from tests/modules/test_reports.py. The rule is repository wide by
    # design, not unit scoped: a file that adopts the convention is covered by
    # it, so a title another unit cites has to be declared here or the reverse
    # direction stops checking anything.
    "A class rebound after its own definition is no longer reachable by name",
    # Declared on the U59 merge, 2026-09-10, and the two are this rule proving
    # itself on a live case rather than on an argument. Both were cited by NUMBER
    # in tests/_source_guards.py on the conformance branch. One of the two
    # numbers named a finding the branch had filed itself, and that finding's
    # number had to MOVE at this merge, because the branch was cut when main's
    # highest was far below where main has since reached and append-only
    # numbering gives the incoming side fresh numbers. The citation would have
    # gone on pointing at whatever main had put in the vacated slot, silently and
    # with no test failing. Both are titles now.
    "Guard whitelists assert what is forbidden, never what is permitted",
    "What the soft-delete guard cannot see, and two gaps in the gate contract",
)

#: WHAT A CITATION LOOKS LIKE, as a form rather than as a convention: the word
#: ``residual``, then nothing but whitespace and comment prefixes, then the
#: finding's TITLE in double quotes.
#:
#: The form is what makes the REVERSE direction checkable. A citation a regular
#: expression cannot find is a citation this test cannot judge, so prose that
#: names a title without the word in front of it is not a citation and has to be
#: rewritten into one. That is not hypothetical: one of the eight titles above
#: was written two lines below a sentence ending "and", outside the form, and was
#: invisible to the scan until it was rewritten.
CITATION = re.compile(r"\bresiduals?\b[\s#:]*\"([^\"\n]+)\"")

#: The authored surface the citation rule is scanned over. Vendored code is
#: excluded for the reason the conformance suite excludes it.
AUTHORED_GLOBS = ("src/**/*.py", "tests/**/*.py", "scripts/**/*.py", "docs/**/*.md")

#: The residual document, which is always covered: it defines the titles and it
#: cross-references its own findings in prose, which is exactly where a citation
#: by number hides inside the letter of the rule.
FINDINGS_DOCUMENT = "docs/residual-findings.md"


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
    """The files the citation rule covers, DERIVED rather than hand listed.

    A FILE THAT HAS ADOPTED THE CONVENTION IS COVERED BY IT, plus the residual
    document itself. The round before carried a hand written tuple of four
    entries against the eight files this branch changes, so half of what the unit
    touched was outside a rule the unit wrote, and
    ``tests/modules/test_tools.py`` carried two bare number-only citations that the
    test could not see. Deriving it means a file cannot fall out of the rule by
    being forgotten, and a file that adopts the rule is inside it from the first
    citation.

    WHY NOT THE FILES THIS BRANCH CHANGES. That list is the honest description of
    "what the unit touches" and it is the wrong mechanism: derived from the diff
    against the base it goes EMPTY the moment the branch merges, at which point
    the rule covers nothing and passes, which is the shape
    "The tiers were bought with a number that does not exist" rejects for the key
    set. This derivation does not decay.

    WHAT IT DOES NOT REACH, said rather than implied: a file that cites a
    residual ONLY by number and never by title is outside it, because it has
    adopted nothing to be held to. ``src/cratekit/modules/tools/backup.py`` and
    ``tests/test_write_session.py`` are the live instances, both citing the backup
    restore residual by number, both
    belonging to that residual's owner rather than to this unit.
    """
    found = {FINDINGS_DOCUMENT}
    for relative, text in authored_sources():
        if CITATION.search(text):
            found.add(relative)
    return sorted(found)


def residual_headings() -> list[tuple[str, str]]:
    """Every heading in the findings document, as (number, title), IN ORDER.

    A LIST, NEVER A SET, and the difference is the whole convention. The round
    before collected the titles into a set, so two headings whose text is byte
    identical collapsed into one entry and the single collision the convention
    exists to prevent, one title naming two findings, was the one collision the
    test could not see. Measured: appending a second heading under an unused
    number, with
    text identical to a cited title left the check passing. A near duplicate that
    merely STARTED with a cited title was caught, so the rule it enforced was
    "exactly one distinct heading TEXT", not "exactly one heading", which is this
    repository's recurring identity defect inside the artifact built to stop it.
    """
    document = (REPO_ROOT / FINDINGS_DOCUMENT).read_text()
    found = []
    for line in document.splitlines():
        if line.startswith("## R-") and ". " in line:
            number, _, title = line[3:].partition(". ")
            found.append((number.strip(), title.strip()))
    return found


def test_a_residual_heading_names_exactly_one_finding():
    """IDENTITY THAT IS NOT UNIQUE, checked on the identifier the convention uses.

    The convention replaced a number with a title because numbers collide across
    branches. That trade only holds if a TITLE does not collide, and nothing
    asserted it: the round before read the headings into a ``set``, which makes
    two byte identical headings indistinguishable from one. Measured against the
    shipped test, appending a second heading under an unused number whose text
    equalled a
    cited title left it PASSING, while a near duplicate that merely started with
    a cited title failed. The check was over the distinct heading TEXTS and the
    prose describing it said headings.

    Both halves of the identity are asserted here, off a LIST: no two findings
    share a title, and no two share a number.
    """
    headings = residual_headings()
    assert headings, (
        "no residual headings were found in docs/residual-findings.md, so every "
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
    """A citation by number cannot survive a merge, and this wave proved it.

    Six residual numbers collide across the branches in flight, each meaning a
    different thing on each side. Source that cites a residual by its number
    alone, with no title beside it, is source that will
    point at somebody else's finding the moment two branches meet, and nothing
    fails when it does, which is this repository's own signature defect: a wrong
    answer that reads as a right one.

    THREE HALVES, and the round before had one and a half of them.

    1. Every DECLARED title resolves to exactly one heading, so a title that
       drifts fails here instead of dangling.
    2. Every title WRITTEN in a covered file is declared and resolves. This
       direction was missing entirely, so a citation carrying a typo or an
       invented title passed silently: seven citations existed and all seven
       resolved, which proved nothing about an eighth.
    3. No covered file carries a bare ``R-<number>``, so going back to numbers
       fails rather than passing quietly. The covered set is DERIVED now. The
       hand written tuple it replaced named four files against the eight this
       branch changes, and the residual document itself was outside it while
       citing four of its own findings by number in prose.
    """
    headings = residual_headings()
    # MATCHED AS A PREFIX, and it has to resolve to EXACTLY ONE heading. Two of
    # these headings carry a second clause that reads badly inline, so prose
    # cites the leading phrase; requiring exactly one match is what stops that
    # being a partial name that could later fit two findings.
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

    # THE REVERSE DIRECTION. Every title written down somewhere has to be one of
    # the declared ones, which is what catches the typo the forward direction
    # cannot see.
    covered = set(owned_sources())
    written: dict[str, set[str]] = {}
    for relative, source in authored_sources():
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
    for relative, source in authored_sources():
        # THE RESIDUAL DOCUMENT IS EXEMPT FROM THE NUMBER BAN, and only from that
        # half. Decided 2026-08-10, when residual numbers became APPEND ONLY: a
        # number never moves again, so the premise this ban rests on, that a number
        # silently changes subject at merge, is no longer true of it. The document
        # is where numbers legitimately live and where its own prose cross
        # references its own findings. The ban still covers CODE, which is the
        # surface where a citation could repoint at another unit's finding with
        # nothing failing. Both title halves above still cover this file.
        if relative not in covered or relative == FINDINGS_DOCUMENT:
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
    """The list that was hand maintained, and what deriving it changed.

    A POSITIVE CONTROL ON THE DERIVATION, because every assertion in the test
    above is an ABSENCE: a derivation that answers the empty set makes all three
    of them pass over nothing, which is this file's own recurring defect aimed at
    the file itself.

    The four files the hand written tuple named are still covered, the residual
    document is covered now and was not, and ``tests/modules/test_tools.py`` is
    covered now because its two bare number-only citations were rewritten as titles
    rather than left invisible.
    """
    covered = set(owned_sources())
    assert {
        "tests/test_reserved_causes.py",
        "tests/_source_guards.py",
        "tests/test_review_queue.py",
        "src/cratekit/cli/exit_codes.py",
        "tests/modules/test_tools.py",
        FINDINGS_DOCUMENT,
    } <= covered, (
        f"the derivation lost a file that carries citations: {sorted(covered)}"
    )


def test_the_package_scan_reaches_the_modules_it_claims_to():
    """A POSITIVE control on the scanner, which the two tree-wide tests cannot be.

    Both of those assert the ABSENCE of an offender, so narrowing
    ``package_sources`` from ``rglob`` to ``glob`` kills neither: the scan stops
    at the top level, finds nothing because it looks nowhere, and both pass. That
    is absence read as evidence of absence pointed at the scanner itself, which
    is the shape this whole file exists to catch.

    Named at three depths on purpose. One nested file would still be found by a
    scan narrowed to ``*/*.py``, so the deepest entry is what makes any narrowing
    at all go red.

    THE SIZE IS A MEASUREMENT, not a rounding. This scan returns 51 files: 43
    modules and 8 package ``__init__.py``, none of them empty. The round before
    described the same set as "all sixty plus real modules in the package" in two
    places, which overstates it by ten and counts package inits as modules. The
    floor below is a floor rather than the number, because a unit landing a
    module has to be able to add one without editing this line, and the composition
    is asserted so a scan that starts returning package inits only goes red.
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
# THE BASIS, written out because the round before measured its two halves on two
# different ones and compared them as if they were one. Every count below is
# taken over the SAME population, the files `package_sources()` returns that are
# not table owners, with the SAME resolver, the shipped `cause_key`, asked of
# every `ast.Name` and `ast.Attribute` in the file. Nothing here counts a file
# the guard exempts, and nothing here reads a key the shipped guard could not.
# ═══════════════════════════════════════════════════════════════════════════


def population_under_measurement() -> list[tuple[str, str]]:
    """The 49 non-owner files every count in this section is taken over."""
    return [
        (relative, source)
        for relative, source in package_sources()
        if relative not in TABLE_OWNERS
    ]


def modules_holding_a_named_cause(*, own_declarations: bool) -> dict[str, list[str]]:
    """Modules where a NAME or a class attribute resolves to a declared cause.

    ``own_declarations`` says whether the file's own enum declarations are in the
    cause set, which is the difference between what the registry declares and
    what ``ReservedCodeTable`` actually reads. Both are reported because the gap
    between them IS the effect of the key-side widening.
    """
    causes = declared_causes()
    found: dict[str, list[str]] = {}
    for relative, source in population_under_measurement():
        tree = ast.parse(source)
        table = _guards.ReservedCodeTable(tree, causes, RANGE, package_of(relative))
        if not own_declarations:
            table.causes = set(causes)
        hits = {
            slug
            for node in ast.walk(tree)
            if isinstance(node, (ast.Name, ast.Attribute))
            for slug in [table.cause_key(node)]
            if slug
        }
        if hits:
            found[relative] = sorted(hits)
    return found


def modules_holding_a_cause_literal() -> dict[str, list[str]]:
    """The same population under the OLD constant-only key rule, for comparison."""
    causes = declared_causes()
    found: dict[str, list[str]] = {}
    for relative, source in population_under_measurement():
        hits = {
            node.value
            for node in ast.walk(ast.parse(source))
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
        for node in ast.walk(ast.parse(source))
    )


def kebab_shaped_literals() -> set[str]:
    """Every cause-shaped string literal anywhere in the package."""
    return {
        node.value
        for _, source in package_sources()
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and _guards.CAUSE_SLUG.match(node.value)
    }


def test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned():
    """The numbers the residual argues from, recomputed here rather than recalled.

    Six places in the residual
    "The tiers were bought with a number that does not exist"
    carried a population figure and NO assertion held any of them. A justification
    that decays silently as the tree grows is the same defect as a docstring
    claiming a property nothing measures, and this unit has now filed that one
    against itself twice. So every load-bearing number is computed from the tree
    here, and a drift fails with the figure that moved.

    WHEN THIS FAILS, the fix is to look and then to update BOTH this line and the
    residual's prose, which is the review the numbers exist to trigger. It is not
    to widen the assertion.

    The comparison this pins is the whole argument for keeping the key-side
    widening: the named surface, which the widening added, is SMALLER than the
    literal surface the tree has carried and the suite has accepted since the
    fifth round. Both halves are measured on the one basis described above, which
    is the correction. The round before measured the named half over ALL files
    with a resolver wider than the shipped one, and the literal half over
    non-owners with the narrow one, then compared the two.
    """
    causes = declared_causes()
    # Re-pinned on the U38 merge, 2026-08-10. U24 and U34 landed causes, so the
    # population grew from 82 to 100 and the non-reserved half from 60 to 78.
    # Re-pinned again on the U16 merge, 2026-08-13, which appends exactly one
    # cause, intake-list-unusable, taking the population to 101 and the
    # non-reserved half to 79. The reserved half is UNCHANGED at 22 across both
    # re-pins, which is the half this pin exists to protect, so the comparison
    # the docstring argues is undisturbed by either merge.
    #
    # Re-pinned again on the U23 merge, 2026-08-14, which appends exactly two
    # causes, adoption-ledger-unusable and adoption-file-unidentifiable, taking
    # the population to 103 and the non-reserved half to 81. The reserved half
    # is UNCHANGED at 22 across all three re-pins, so the comparison the
    # docstring argues is still undisturbed.
    #
    # Re-pinned again on the U27 merge, 2026-08-15, and THIS IS THE FIRST RE-PIN
    # THAT MOVES THE RESERVED HALF, so it is not the routine bump the three above
    # are. U27 appends exactly five causes, named rather than counted:
    # grant-path-access, library-root-unreachable, path-locked,
    # path-permission-denied and path-read-only. Measured by asking git whether
    # each of the 108 appears anywhere in main's own `src` before the merge, not
    # by subtracting one total from another.
    #
    # Four of the five are ordinary and take the population to 108 and the
    # non-reserved half to 85. The fifth, grant-path-access, is a REMEDY token
    # that this merge had to reserve, because U27's branch was cut before U38
    # landed the registry and only the merged tree can see the obligation, so the
    # reserved half moves 22 to 23 for the first time. The comparison the
    # docstring argues is undisturbed by that: the reserved half growing makes the
    # named surface no larger relative to the literal one, and the literal
    # headroom assertion below still reports no offender, which is the check that
    # would notice if it had.
    #
    # Re-pinned on U22, 2026-08-17. Four slugs named rather than counted:
    # sync-watermark-unusable, sync-source-lookups-failed, sync-marks-blocked,
    # sync-artifacts-unusable. Population 108 to 112, non-reserved 85 to 89,
    # reserved half UNCHANGED at 23.
    # Re-pinned on U20, 2026-08-17. Six slugs named rather than counted:
    # cutover-open-run, cutover-xml-pending, cutover-export-missing,
    # cutover-snapshot-missing, rebuild-actor-required, rebuild-tree-not-native.
    # Population 112 to 118, non-reserved 89 to 95, reserved half UNCHANGED at 23.
    # Re-pinned on U37, 2026-08-17. Three slugs named rather than counted:
    # intake-export-is-stub, intake-recognition-unready, intake-staging-refused.
    # Population 118 to 121, non-reserved 95 to 98, reserved half UNCHANGED at 23.
    # Re-pinned on U26, 2026-08-17. Five slugs named rather than counted:
    # label-intent-unusable, label-name-invalid, label-unknown,
    # label-watermark-unusable, label-playlist-unreadable.
    # Population 121 to 126, non-reserved 98 to 103, reserved half UNCHANGED at 23.
    # Re-pinned on U33, 2026-08-17. Two slugs named rather than counted:
    # outbound-ledger-unusable, export-playlist-unknown.
    # Population 126 to 128, non-reserved 103 to 105, reserved half UNCHANGED at 23.
    # Re-pinned on U27's report shell, 2026-08-23. Two slugs named rather than
    # counted: governed-tree-absent, which is the routing tree missing from an
    # export, and report-as-of-invalid, which is an aging report handed a value
    # that is not a date. Population 128 to 130, non-reserved 105 to 107,
    # reserved half UNCHANGED at 23.
    # Re-pinned on U27's restore shell, 2026-08-23. ONE slug, named rather than
    # counted: restore-transfer-failed, which an independent review's blocking
    # finding bought. It is the first slug this unit adds to BOTH tables, which is
    # why the reserved half moves for the first time in eight re-pins: the eight
    # backup refusals landing in cause.REASONS alongside it were ALREADY reserved,
    # so they moved from the reserved-only side to the both side and left this
    # union unchanged. Population 130 to 131, non-reserved UNCHANGED at 107,
    # reserved half 23 to 24.
    # Re-pinned on U40, 2026-08-26. ONE slug, named rather than counted:
    # tag-retag-folder-unknown, which the genre correction verb raises when it is
    # handed an empty folder. It sits in cause.REASONS and NOT in the reserved
    # table, exactly as its sibling export-playlist-unknown does, so the reserved
    # half does not move. Population 131 to 132, non-reserved 107 to 108,
    # reserved half UNCHANGED at 24.
    #
    # THE SLUG EXISTED IN THE TREE BEFORE IT EXISTED HERE, and that is worth one
    # line because it is what this pin caught. ``cause.refuse`` raises
    # ``UnknownReason`` for an undeclared slug, so the verb's empty-folder branch
    # would have raised a KeyError at the boundary instead of refusing. No test in
    # the unit drove that branch; this population count is what reported it.
    #
    # Re-pinned on U43, 2026-08-26. THREE slugs, named rather than counted:
    # setbuild-anchor-unknown, setbuild-anchor-outside-library and
    # setbuild-anchor-not-indexed, which are the set builder's three refusals.
    # Measured by differencing this branch's REASONS literal against the one in
    # origin/main's own tree extracted to a scratch directory, rather than by
    # subtracting one total from another: three joined, none left. None of the
    # three is in the reserved table, exactly as their siblings
    # export-playlist-unknown and tag-retag-folder-unknown are not, so the
    # reserved half does not move. Population 132 to 135, non-reserved 108 to
    # 111, reserved half UNCHANGED at 24.
    #
    # Re-pinned on U45, 2026-08-29. TWO slugs, named rather than counted:
    # backup-transfer-failed and backup-nothing-ran, which are the backup shell's
    # whole-run verdict over the engine's per-portion report. Measured by
    # differencing this branch's declared_causes against the one derived from
    # origin/main's own tree in a scratch worktree, rather than by subtracting one
    # total from another: exactly two joined, none left. Neither is in the
    # reserved table, exactly as their siblings export-playlist-unknown,
    # tag-retag-folder-unknown and the three setbuild-anchor slugs are not, so the
    # reserved half does not move. Population 135 to 137, non-reserved 111 to 113,
    # reserved half UNCHANGED at 24.
    #
    # WHY NEITHER JOINS THE ENGINE'S Refusal ENUM, since eight backup slugs are
    # there already. Every member of that enum is a reason ONE PORTION will not
    # run, decided before anything is attempted, and run_backup reports those per
    # portion rather than raising. These two are the whole run's verdict over that
    # report, which is a command line's decision rather than an engine's.
    #
    # Re-pinned on U51, 2026-09-02. FIVE slugs, named rather than counted:
    # outbound-export-required, export-playlist-ambiguous and
    # export-playlist-empty, which are the three ways the two outbound verbs
    # cannot decide what their job items are; outbound-account-unbound, which is
    # this build having no streaming provider adapter to hand a worker; and
    # outbound-item-absent, which is a frozen export no longer carrying a track
    # its own job already queued. None of the five is in the reserved table,
    # exactly as their siblings export-playlist-unknown, tag-retag-folder-unknown
    # and the three setbuild-anchor slugs are not, so the reserved half does not
    # move. Population 137 to 142, non-reserved 113 to 118, reserved half
    # UNCHANGED at 24.
    #
    # WHY THE MISSING CREDENTIAL IS NOT A SIXTH. ``outbound.account.resolve``
    # raises TWO refusals and only one of them is new: no session stored reuses
    # ``credential-missing``, which this vocabulary already declares and which
    # doctor already has a remedy for. A second slug meaning the same thing would
    # have made a person who has not logged in read a different sentence
    # depending on which verb discovered it.
    #
    # Re-pinned on U55, 2026-09-02. TWO slugs, named rather than counted:
    # adopt-item-absent, which is the collection no longer holding a row the scan
    # job already queued as an item, and adopt-entries-failed, which is the apply
    # worker's whole-run verdict over the entries apply_plan RETURNED as failed
    # rather than raised on. Neither is in the reserved table, exactly as their
    # siblings outbound-item-absent and export-playlist-unknown are not, so the
    # reserved half does not move. Population 142 to 144, non-reserved 118 to 120,
    # reserved half UNCHANGED at 24.
    #
    # WHY THE STALE PLAN IS NOT A THIRD. The apply worker refuses a rebuilt plan
    # whose digest is not the frozen one, and that is ``decision-stale``, which
    # this vocabulary already declares and which the gate layer already raises for
    # the same fact. A second slug meaning the same thing would make a person read
    # a different sentence depending on whether the queueing or the drive noticed.
    #
    # Re-pinned on U56, 2026-09-03. TWO slugs, named rather than counted:
    # catalogue-unreachable, which the tagging searcher raises when none of
    # Beatport, Traxsource and Bandcamp could be READ, and catalogue-parse-broken,
    # which it raises when one of them answered and the page carried no shape this
    # product's parser recognises. Measured by differencing this branch's REASONS
    # literal against the one in main's own tree extracted to a scratch directory,
    # rather than by subtracting one total from another: exactly two joined, none
    # left. Neither is in the reserved table, exactly as their siblings
    # adopt-item-absent and export-playlist-unknown are not, so the reserved half
    # does not move. Population 144 to 146, non-reserved 120 to 122, reserved half
    # UNCHANGED at 24.
    #
    # WHY THEY ARE TWO SLUGS RATHER THAN ONE, since both mean the searcher learned
    # nothing. They send a person to two different places. A catalogue nobody could
    # read is a network, and it is transient. A page whose shape moved is this
    # parser, and it is permanent until somebody rewrites it, so riding the
    # transient slug would put a permanent break behind "retry later" for ever.
    # That is the specific mistake the unit's four-way outcome exists to prevent,
    # and collapsing the two slugs would reintroduce it one layer along.
    #
    # WHY THE VANISHED FILE IS NOT A THIRD. The tag.folder worker refuses an item
    # whose file is gone between the queueing and the drive, and that is
    # ``source-missing``, which this vocabulary already declares and whose reserved
    # remediation, nothing was read and nothing was written, is exactly what that
    # refusal promises. Its siblings adopt-item-absent and outbound-item-absent
    # each name a frozen SOURCE rather than a file on disk, so neither is the same
    # sentence. Reusing rather than adding is a judgement recorded in
    # docs/residual-findings.md rather than left implicit here.
    #
    # Re-pinned at the U52 merge, 2026-09-07. THREE slugs, named rather than
    # counted: label-catalogue-unbound, which is this build having no catalogue
    # adapter to hand the label package; label-registry-empty, which is a sweep
    # asked for with no favourite label registered; and label-sweep-incomplete,
    # which is an item that could not offer all of a label's releases and failed
    # rather than completing. U52 was built against a main whose population was
    # 142 and measured 145 there by differencing the REASONS literal against
    # main's own; the merge brings U55's two and U56's two in underneath it, so
    # the merged tree is 146 plus the same three. None of the three is in the
    # reserved table, exactly as their siblings export-playlist-unknown and
    # tag-retag-folder-unknown are not, so the reserved half does not move.
    # Population 146 to 149, non-reserved 122 to 125, reserved half UNCHANGED at
    # 24.
    #
    # WHY THE MISSING CREDENTIAL IS NOT A FOURTH, for the reason the outbound
    # paragraph above gives. label.catalogue.resolve raises TWO refusals and only
    # one of them is new: no session stored reuses credential-missing, which this
    # vocabulary already declares.
    #
    # Re-pinned on U58, 2026-09-07. THREE slugs, named rather than counted:
    # energy-calibration-missing, which is a restamp asked for over a library
    # that has never been calibrated; energy-calibration-unreadable, which is
    # a calibration file that exists and cannot be read, kept apart from
    # missing so a truncated file is never restamped over as "never
    # calibrated"; and analysis-write-failed, which is an analysed track whose
    # tag write or rename did not land. None is in the reserved table, so the
    # reserved half does not move. Population 149 to 152, non-reserved 125 to
    # 128, reserved half UNCHANGED at 24.
    #
    # Re-pinned on U57, 2026-09-09. TWO slugs, named rather than counted, and
    # measured by differencing the REASONS literal against main's own: exactly
    # two joined, none left. intake-recognition-spend-bound is recognition
    # refusing to spend, whether this build's own bound or the service
    # answering that the account's quota is used up, kept apart from a miss
    # because a miss is a fact about the audio and this is a fact about money.
    # intake-recognition-failed is the service unreachable or answering in a
    # shape this build cannot classify. Neither is in the reserved table, so
    # the reserved half does not move. Population 152 to 154, non-reserved
    # 128 to 130, reserved half UNCHANGED at 24.
    #
    # WHY THE REJECTED CREDENTIAL IS NOT A THIRD. The service answering that
    # the key or the signing key is wrong reuses auth-failed, which this
    # vocabulary already declares with the exit code that means exactly that.
    assert (len(causes), len(causes - CAUSES), len(CAUSES)) == (154, 130, 24)

    literals = kebab_shaped_literals()
    # Re-pinned on the U38 merge, 2026-08-10, same reason as the pin above:
    # U24 and U34 landed literals. 189 to 239 distinct, 108 to 140 non-keys.
    # Re-pinned again on the U16 merge, 2026-08-13: 239 to 256 distinct and 140
    # to 156 non-keys, which is the match and match_cli pair landing 17 kebab
    # literals of which 16 are not causes. The headroom assertion below is what
    # those numbers are spent on, and it still reports no offender.
    # Re-pinned again on the U23 merge, 2026-08-14: 256 to 270 distinct and 156
    # to 168 non-keys. The adoption package lands 14 kebab literals of which 12
    # are not causes, the two that are being the pair re-pinned above. The
    # headroom assertion below still reports no offender, which is what these
    # numbers are bought for and the only reason moving them is safe.
    # Re-pinned again on the U27 merge, 2026-08-15: 270 to 282 distinct and 168
    # to 175 non-keys. Twelve kebab literals land with the wizard, the doctor and
    # the login verb, of which five are the causes named in the pin above and
    # seven are not causes at all. Nothing was lost in either direction, measured
    # rather than inferred from the totals moving by the right amount. The
    # headroom assertion below still reports no offender.
    # Re-pinned on U22, 2026-08-17: 282 to 286 distinct, non-keys stay 175,
    # because the four new literals are the four causes named above.
    # Re-pinned on U20, 2026-08-17: 286 to 292 distinct, non-keys stay 175,
    # because the six new literals are the six causes named above.
    # Re-pinned on U37, 2026-08-17: 292 to 297 distinct, 175 to 177 non-keys.
    # Three new literals are the causes named above. The two that are not
    # causes are has-genre and no-hit, the skip markers on a tagging result.
    # Re-pinned on U25, 2026-08-17: 297 to 299 distinct, 177 to 179 non-keys.
    # The two that joined are skipped-prefixed and skipped-no-key, the resume
    # and no-detect markers on an analysis result. Neither is a cause.
    # Re-pinned on U26, 2026-08-17: 299 to 305 distinct, 179 to 180 non-keys.
    # Five new literals are the causes named above. The one that is not a
    # cause is harvested-label, the harvest offer kind. label-release was
    # already the review queue slug.
    # Re-pinned on U33, 2026-08-17: 305 to 307 distinct, non-keys stay 180,
    # because the two new literals are the two causes named above.
    # Re-pinned on U27's report shell, 2026-08-23: 307 to 309 distinct, non-keys
    # stay 180, because the two new literals are the two causes named above.
    # Re-pinned on U27's restore shell, 2026-08-23: 309 to 310 distinct, 180 to
    # 181 non-keys. EXACTLY ONE literal joined and NOTHING left, differenced as
    # SETS against `origin/main`'s own `src` tree extracted into a scratch
    # directory rather than inferred from the totals moving by one, because a
    # module joining while another leaves reads identically in a count. The one
    # that joined is `off-machine`, which names one HALF of a restore in the
    # offer and in the report; it is kebab shaped and it is not a cause, which is
    # the whole reason the non-key count moves with it. The eight backup refusal
    # slugs this unit adds to `cause.REASONS` were ALREADY literals in the tree,
    # in `modules/tools/backup.py`'s own `Refusal` enum, so they move from the
    # non-key side to the key side and the distinct total does not see them.
    # Re-pinned again in U27's second fix round, 2026-08-23: 310 to 311 distinct,
    # non-keys UNCHANGED at 181. The one that joined is `restore-transfer-failed`,
    # differenced as SETS against `origin/main` the same way, and it is a KEY on
    # both sides, so the non-key half does not move with it. Nothing left.
    # Re-pinned on U40, 2026-08-26: 311 to 318 distinct, 181 to 187 non-keys.
    # SEVEN literals joined and NOTHING left, differenced as SETS against
    # `origin/main`'s own `src` tree extracted into a scratch directory rather
    # than inferred from the totals moving by seven, because a module joining
    # while another leaves reads identically in a count. Named:
    # `tag-retag-folder-unknown`, which is a KEY on this side and is why the
    # non-key half moves by six rather than seven; and six that are not causes at
    # all, `coarse-genre`, the review item kind, plus `no-genre`,
    # `genre-specific`, `no-answer`, `answer-too-coarse` and `declined-in-review`,
    # the reason markers on a retag result. They are the same shape as `has-genre`
    # and `no-hit`, the tagging result markers the U37 re-pin above names.
    # Re-pinned on U43, 2026-08-26: 318 to 321 distinct, non-keys UNCHANGED at
    # 187. THREE literals joined and NOTHING left, differenced as SETS against
    # `origin/main`'s own `src` tree extracted into a scratch directory rather
    # than inferred from the total moving by three. Named:
    # `setbuild-anchor-unknown`, `setbuild-anchor-outside-library` and
    # `setbuild-anchor-not-indexed`. All three are KEYS on this side, which is why
    # the non-key half does not move at all: the set builder's shell introduces no
    # cause-shaped literal that is not a declared cause.
    # Re-pinned on U42, 2026-08-28: 321 to 326 distinct, 187 to 192 non-keys.
    # FIVE literals joined and NOTHING left, differenced as SETS against
    # `origin/main`'s own `src` tree extracted into a scratch directory rather
    # than inferred from the total moving by five. Named: `lossy-under-strict`,
    # `lossy-unmarked`, `marked-lossless`, `format-undecided` and
    # `path-unreadable`, the five finding kinds the acquisition audit reports.
    # None is a cause, which is why both halves move together by the same five.
    #
    # THIS PIN IS WHAT CAUGHT THE RENAME, and it is worth saying because the
    # number is otherwise just a number. The audit's strict-policy kind was
    # written as `lossy-refused` first, and that string is a declared CAUSE key
    # raised by `intake.pipeline.acquire_lossy_or_refuse` for the same policy at
    # acquisition time. So the first measurement here read four joined literals
    # with one of them a key, which is the signature of a payload kind wearing a
    # cause slug: one symbol meaning two things in two modules, which METHOD
    # lists among the things a green suite cannot see. Nothing else in the
    # battery noticed. It was renamed to `lossy-under-strict`, and the fifth
    # literal appearing on the non-key side is the rename being visible.
    # Re-pinned on U45, 2026-08-29: 326 to 328 distinct, non-keys UNCHANGED at
    # 192. TWO literals joined and NOTHING left, differenced as SETS against
    # `origin/main`'s own `src` tree extracted into a scratch worktree rather than
    # inferred from the total moving by two. Named: `backup-transfer-failed` and
    # `backup-nothing-ran`. Both are KEYS on this side, which is why the non-key
    # half does not move at all: the backup shell introduces no cause-shaped
    # literal that is not a declared cause. The two ways it names an EXISTING
    # cause, `backup-facts-unreadable` and `config-unusable`, were already
    # literals in the tree, in `core/session.py` and in every other shell, so the
    # distinct total does not see them either.
    # Re-pinned on U48, 2026-09-02: 328 to 330 distinct, 192 to 194 non-keys.
    # TWO literals joined and NOTHING left, differenced as SETS against
    # `origin/main`'s own `src` tree read blob by blob rather than inferred from
    # the total moving by two, because a literal joining while another leaves
    # reads identically in a count. Named: `archive-listing-failed` and
    # `archive-purge-failed`, the two conditions a portion reports about an
    # archive rotation that did not happen. Neither is a cause, which is why both
    # halves move together by the same two: a rotation that failed after the
    # mirror in its portion succeeded is an advisory on a run that completed,
    # and every member of the engine's `Refusal` enum is instead a reason one
    # portion will NOT run, decided before anything is attempted.
    # Re-pinned on U51, 2026-09-02: 330 to 339 distinct, 194 to 198 non-keys.
    # NINE literals joined and NOTHING left, differenced as SETS against `main`'s
    # own `src` tree read blob by blob rather than inferred from the total moving
    # by nine. FIVE are keys, the causes the two outbound workers raise, and they
    # are named at the population assertion above. The other FOUR are not causes
    # and each is worth naming, because a non-cause wearing a cause slug is
    # exactly the shape the `lossy-refused` incident above was:
    # `outbound-artifacts` and `outbound-staging` are DIRECTORY names under the
    # queue root, and `playlist-track-missing` and `playlist-track-repeated` are
    # WARNING codes on the queued envelope, the same kind of literal as
    # `config-drift`. None of the four collides with a declared cause, and none
    # describes a refusal: a warning that a playlist named a track the collection
    # does not carry is an advisory on a job that queued successfully, and every
    # declared cause is instead a reason something did NOT happen.
    # Re-pinned on U55, 2026-09-02: 339 to 347 distinct, 198 to 204 non-keys.
    # EIGHT literals joined and NOTHING left, differenced as SETS against `main`'s
    # own `src` tree read blob by blob rather than inferred from the total moving
    # by eight. TWO are keys, `adopt-item-absent` and `adopt-entries-failed`, and
    # both are named at the population assertion above. The other SIX are not
    # causes and each is worth naming, because a non-cause wearing a cause slug is
    # exactly the shape the `lossy-refused` incident above was:
    # `adopt-artifacts` and `adopt-staging` are DIRECTORY names under the queue
    # root, the same kind of literal as `outbound-artifacts` and
    # `outbound-staging`; `collection-empty`, `collection-all-tombstones` and
    # `adoption-nothing-applicable` are WARNING codes on an envelope that reports
    # a correct no-op, the same kind of literal as `config-drift`; and `no-op` is
    # the `state` field on that same payload, which is a job_state value rather
    # than a slug. None of the six collides with a declared cause, and none
    # describes a refusal: an empty library is a fact about the library, not a
    # reason something did not happen.
    #
    # Re-pinned on U56, 2026-09-03: 347 to 358 distinct, 204 to 213 non-keys.
    # ELEVEN literals joined and NOTHING left, differenced as SETS against `main`'s
    # own `src` tree in a scratch worktree rather than inferred from the total
    # moving by nine. TWO are keys, `catalogue-unreachable` and
    # `catalogue-parse-broken`, and both are named at the population assertion
    # above. The other NINE are not causes and each is worth naming, for the
    # reason the U55 entry gives: a non-cause wearing a cause slug is the shape the
    # `lossy-refused` incident above was.
    # `tag-artifacts` and `tag-staging` are DIRECTORY names under the queue root,
    # the same kind of literal as `adopt-artifacts` and `outbound-staging`;
    # `tag-folder-absent`, `tag-folder-no-audio`, `tag-folder-unnamed`,
    # `tag-retag-folder-absent` and `tag-retag-nothing-coarse` are WARNING codes on
    # an envelope that reports a correct no-op, the same kind of literal as
    # `collection-empty`; `unmapped-genre` is a SKIP REASON on one file's tagging
    # result, sitting beside `has-genre` and `no-hit`, which the tree has carried
    # since the tagging engine landed; and `parse-break` is the name of one member
    # of the searcher's per source outcome enum. None of the nine collides with a
    # declared cause, and none describes a refusal: a folder holding no audio is a
    # fact about the folder rather than a reason something did not happen, which is
    # precisely why those five are warnings on a NO_OP and not refusals. The one
    # place this verb family DOES refuse over an argument, an unnamed folder, has a
    # declared slug already, `tag-retag-folder-unknown`, and it is not new.
    #
    # Re-pinned at the U52 merge, 2026-09-07: 358 to 361 distinct, non-keys
    # UNCHANGED at 213. THREE literals joined and NOTHING left, measured on the
    # branch against its own base by repointing this module's PACKAGE_ROOT at
    # main's src tree extracted into a scratch directory, and carried through the
    # merge as the same three on top of U56's 358. All three are the causes named
    # at the population assertion above, so they are KEYS on this side and the
    # non-key half does not move at all: the catalogue seam introduces no
    # cause-shaped literal that is not a declared cause. The protocol it declares
    # carries no slug of any kind, because it is a type rather than a table.
    #
    # Re-pinned on U58, 2026-09-07: 361 to 374 distinct, 213 to 223 non-keys.
    # THIRTEEN literals joined and NOTHING left, differenced as SETS against
    # `main`'s own `src` tree extracted into a scratch directory, once on the
    # build and again after the review's fix round. Three are the causes named
    # at the population assertion above. The ten that are not causes:
    # analysis-artifacts and analysis-staging, the two directory names under
    # the queue root; no-audio and folder-absent, the two honest zero states a
    # queued analysis verb reports, told apart so an unmounted volume is not
    # read as an empty folder; db-metadata-not-written, the warning every
    # restamp carries for the database half the registry declares and this
    # build does not write; features-unavailable, the energy status for a
    # track that could not be measured; skipped-undecodable, the head's
    # terminal for a file the decoder could not read, kept apart from keyless;
    # and the three reasons a vocal pass reports for not scoring a track,
    # vocal-audio-undecodable, vocal-head-terminal and vocal-model-unavailable.
    # Re-pinned in U58's second fix round, 2026-09-08: 374 to 376 distinct, 223
    # to 225 non-keys. TWO literals joined and NOTHING left, differenced as
    # SETS against `main`'s own `src` tree extracted into a scratch directory.
    # Neither is a cause: skipped-unanalysable, the head's terminal for a file
    # that decoded and then raised inside the analyser, kept apart from
    # keyless as undecodable is; and vocal-inference-failed, the reason the
    # vocal pass reports when the loaded model raised on a track's samples,
    # so the key and tempo the head found are kept rather than the item
    # failing as a defect.
    # Re-pinned on U54, 2026-09-08: 376 to 377 distinct, 225 to 226 non-keys.
    # ONE literal joined and NOTHING left, differenced as SETS against `main`'s
    # own `src` tree extracted into a scratch directory. It is not a cause:
    # no-tracks, the honest zero state a queued download reports when the list
    # document it read declares no tracks, beside the analysis verbs' no-audio.
    # Every refusal the acquisition worker raises reuses a slug the table
    # already reserves, so the reserved half does not move.
    # Re-pinned on U57, 2026-09-09: 377 to 385 distinct, 226 to 232 non-keys.
    # EIGHT literals joined and NOTHING left, differenced as SETS against
    # `main`'s own `src` tree extracted into a scratch directory, once on the
    # build and again after the review's fix round. Two are the causes named
    # at the population assertion above. The six that are not causes:
    # intake-artifacts and intake-staging, the two directory names under the
    # queue root the intake worker's reports land in; nothing-identified, the
    # honest zero state a set reports when recognition named no track, beside
    # the download verb's no-tracks; per-run and provider-quota, the two KINDS
    # a spend refusal carries in its detail so a reader can tell this build's
    # own bound from the service's answer without parsing the sentence; and
    # recognition-incomplete, the WARNING code a set queued over chunks that
    # got no answer carries, a warning and not a cause because the set did
    # queue. The monthly kind is one word, so it is not cause-shaped and this
    # population never held it.
    # Re-pinned on U53, 2026-09-10: 385 to 389 distinct, 232 to 236 non-keys.
    # FOUR literals joined and NOTHING left, differenced as SETS against `main`'s
    # own `src` tree extracted into a scratch directory rather than inferred from
    # the total moving by four. NONE of the four is a cause, so the reserved half
    # does not move at all: route-inbox and route-resort are WORKFLOW names, the
    # string a write records itself under in the session log, the same kind of
    # literal as deferred-routing and tree-rebuild which this population has
    # carried since U19 and U36; no-native-tree is the state a queued rebuild or
    # resort reports when the library has flipped no tree and it therefore filed
    # no job at all, a job_state value beside no-op, and it is the same word the
    # reason field carries when a plan says the same thing; and inbox-empty is
    # the plan reason a confirmed intake apply carries over an empty folder, the
    # same kind of literal as no-tracks and nothing-identified. Every refusal
    # these two verbs raise reuses a slug the table already reserves.
    assert (len(literals), len(literals - set(causes))) == (389, 236), (
        f"the kebab-literal population moved to {len(literals)} distinct with "
        f"{len(literals - set(causes))} that are not keys"
    )

    widened = frozenset(set(causes) | literals)
    assert {
        relative: reserved_code_tables(source, widened, RANGE, package_of(relative))
        for relative, source in population_under_measurement()
        if reserved_code_tables(source, widened, RANGE, package_of(relative))
    } == {}, (
        "the wide rule has a headroom problem now: adding every kebab-shaped "
        "literal in the package to the key set reports an offender, and the "
        "argument for one key set rests on it reporting none"
    )

    without = modules_holding_a_named_cause(own_declarations=False)
    with_own = modules_holding_a_named_cause(own_declarations=True)
    literal_holders = modules_holding_a_cause_literal()
    both = [
        relative
        for relative in with_own
        if holds_an_in_range_integer(dict(package_sources())[relative])
    ]
    literal_both = [
        relative
        for relative in literal_holders
        if holds_an_in_range_integer(dict(package_sources())[relative])
    ]
    # Re-pinned on the U38 merge, 2026-08-10. Same cause as the two pins above:
    # U24 and U34 landed modules. The without-own half is UNCHANGED at 8.
    # Re-pinned again on the U16 merge, 2026-08-13: acquire/match.py is the one
    # module added, taking the with-own half from 17 to 18 and the also-holds-an
    # -integer half from 9 to 10. The without-own half is STILL 8 across both
    # re-pins, so nothing gained a name resolving to a cause declared elsewhere.
    # Re-pinned again on the U23 merge, 2026-08-14: the adoption package takes
    # the with-own half from 18 to 20 and the also-holds-an-integer half from 10
    # to 11. THE WITHOUT-OWN HALF IS STILL 8, now across four measurements and
    # three merges. That is the half worth watching: it is the count of modules
    # holding a name resolving to a cause declared somewhere else, which is the
    # shape that would say the one key set had stopped holding, and no merge has
    # ever moved it.
    # Re-pinned again on the U27 merge, 2026-08-15: core/preflight.py is the one
    # module added, taking the with-own half from 20 to 21 and the also-holds-an
    # -integer half from 11 to 12. Named rather than counted, and measured by
    # running this same derivation over main's own tree in a scratch worktree and
    # differencing the two SETS, because a count moving by one says a module
    # joined and does not say which, and a module leaving while another joined
    # reads identically. THE WITHOUT-OWN HALF IS STILL 8, now across five
    # measurements and four merges.
    #
    # Re-pinned on U56, 2026-09-03, and THIS IS THE RE-PIN WHERE THE WITHOUT-OWN
    # HALF FINALLY MOVED, 8 to 9, after five measurements and four merges holding
    # it. Named rather than counted, and measured by running this same derivation
    # over main's own tree in a scratch worktree and differencing the two SETS:
    # exactly one module joined, `tagging/searchers.py`, and nothing left. It
    # joined all three halves at once, so with-own goes 21 to 22 and the
    # also-holds-an-integer half 12 to 13.
    #
    # WHAT MOVED IT, AND WHY IT IS NOT THE FAILURE THIS HALF WATCHES FOR. The
    # searcher names its two slugs once, as `UNREACHABLE_REASON` and
    # `PARSE_BREAK_REASON`, and raises through them rather than repeating a string
    # at each of two raise sites. Both resolve to causes `cause.py` declares, which
    # is the definition of this half. The half exists to catch a module that has
    # started keeping its own opinion about a reserved code, and this is the
    # opposite shape: the module keeps no table, both raises go through
    # `cause.refuse` with an explicit remedy, and the names exist so the two
    # strings cannot drift apart between the raise site and the test that asserts
    # them. Eight of the nine modules here have exactly that shape already,
    # `core/jobs.py` among them.
    #
    # WHY IT ALSO JOINED THE INTEGER HALF, which is the more interesting half of
    # the answer. `holds_an_in_range_integer` is true of this module because it
    # declares a fifteen second request timeout and a thirty second rate limit
    # base wait, and the reserved code range happens to contain 15 and 30. Neither
    # number is an exit code and neither is near one. That is the false positive
    # this composite exists to make visible rather than to hide: a module holding
    # a cause name AND an in-range integer is worth a look, and the look is what
    # says a duration is not a code.
    assert (len(without), len(with_own), len(both)) == (9, 22, 13), (
        f"the named at-risk population moved: {len(without)} modules hold a name "
        f"resolving to a cause declared elsewhere, {len(with_own)} once each "
        f"file's own enum declarations count, {len(both)} of those also hold an "
        f"in-range integer. Update the residual"
    )
    # Re-pinned on the U38 merge, 2026-08-10, same cause as the pins above, and
    # again on the U16 merge, 2026-08-13: 36 to 38 holders, 11 to 12 of them also
    # holding an in-range integer. The literal side grew by two while the named
    # side grew by one, so the comparison asserted just below widened rather than
    # narrowed, which is the direction that keeps the decision it rests on intact.
    # Re-pinned again on the U23 merge, 2026-08-14: 38 to 42 holders, 12 to 13
    # also holding an in-range integer. The literal side grew by four while the
    # named side grew by two, so the comparison just below widened again rather
    # than narrowed, which is the direction that keeps the decision intact. That
    # comparison is the whole reason these four numbers are measured, and it has
    # now widened at every one of the three merges that moved them.
    # Re-pinned again on the U27 merge, 2026-08-15: 42 to 45 holders, 13 to 14
    # also holding an in-range integer. The three are the three modules the unit
    # lands, cli/doctor.py, cli/setup.py and cli/verbs/login.py, and of those only
    # cli/doctor.py also holds an in-range integer. The literal side grew by three
    # while the named side grew by one, so the comparison just below widened for
    # the fourth time out of four. It has never narrowed, and the day it does is
    # the day the decision this rests on has to be re-argued rather than re-pinned.
    # Re-pinned on U22, 2026-08-17: 45 to 50 holders. The five are the five
    # sync package modules: artifacts.py, cli.py, marks.py, run.py, watermarks.py.
    # The also-holds-an-integer half stays 14; run.py's newest-N default sits
    # above the reserved range so it is not a status-shaped integer.
    # Re-pinned on U20, 2026-08-17: 50 to 52 holders. The two are cli/rebuild.py
    # and write/routing_cli.py. The also-holds-an-integer half stays 14.
    # Re-pinned on U37, 2026-08-17: 52 to 61 holders. The nine are
    # intake/cli.py, intake/collection_xml.py, intake/ingest.py,
    # intake/normalize.py, intake/pipeline.py, intake/recognize.py,
    # intake/repair_cli.py, tagging/cli.py, write/naming_cli.py.
    # The also-holds-an-integer half stays 14.
    # Re-pinned on U25, 2026-08-17: 61 to 62 holders. The one is
    # analysis/cli.py, which names config-unusable the same way the other
    # shells do. The also-holds-an-integer half stays 14.
    # Re-pinned on U24's leftover shell, 2026-08-17: 62 to 63 holders.
    # The one is deletion/cli.py, which names config-unusable the same
    # way the other shells do. It also holds 16, the SQLite header length
    # used to tell a synthetic database from an encrypted one, so the
    # also-holds-an-integer half moves 14 to 15.
    # Re-pinned on U26, 2026-08-17: 63 to 66 holders. The three are
    # label/cli.py, label/marks.py and label/registry.py. The
    # also-holds-an-integer half stays 15.
    # Re-pinned on U33, 2026-08-17: 66 to 69 holders. The three are
    # export/cli.py, favorites/cli.py and modules/outbound/ledger.py.
    # The also-holds-an-integer half stays 15.
    # Re-pinned on U27's report shell, 2026-08-23: 69 to 71 holders. The two are
    # cli/reports.py, which names config-unusable the same way every other shell
    # does, and modules/reports/coverage.py, which names its own refusal. The
    # also-holds-an-integer half stays 15.
    # Re-pinned on U27's adopt.apply shell, 2026-08-23: 71 to 72 holders. The one
    # is adopt/apply_cli.py, which names config-unusable the same way every other
    # shell does and internal-error for a verb declaring no plan-digested gate.
    # The also-holds-an-integer half stays 15: the module holds no bare integer
    # at all. NAMED BY DIFFERENCING THE TWO SETS, measured by running this same
    # derivation over origin/main's own src tree extracted into a scratch
    # directory, because a count moving by one says a module joined and does not
    # say which, and a module leaving while another joined reads identically.
    # Nothing left the set. The literal side grew by one while the named side
    # stayed at 21 and the without-own half stayed at 8, so the comparison just
    # below widened rather than narrowed, for the ninth time out of nine.
    # Re-pinned on U27's restore shell, 2026-08-23: 72 to 73 holders. The one is
    # session/restore_cli.py, which names config-unusable the same way every
    # other shell does, internal-error for a verb declaring no plan-digested
    # gate, restore-record-unusable for a session identifier nothing recorded,
    # and off-machine, which is not a cause and is the literal the distinct
    # count above moved for. The also-holds-an-integer half stays 15: the module
    # holds no bare integer at all. NAMED BY DIFFERENCING THE TWO SETS, measured
    # by running this same derivation over origin/main's own src tree extracted
    # into a scratch directory, for the reason the entry above gives. Nothing
    # left the set, and the named side stayed at 21 with the without-own half at
    # 8, so the comparison just below widened rather than narrowed, for the
    # tenth time out of ten.
    # Re-pinned on U28, 2026-08-23: 73 to 74 holders, and the distinct literal
    # population above does NOT move with it, which is the whole shape of this
    # entry. skills/cli.py joined because it names path-permission-denied for a
    # target directory it cannot create, and that slug was already in the tree, so
    # a module joined the holder set while the literal set stood still. A pin that
    # only watched the totals would have read this as nothing happening. Differenced
    # as SETS against origin/main's own src tree, the same way as the entries above:
    # exactly one module joined, none left, and the named side stayed at 21 with the
    # without-own half at 8. The also-holds-an-integer half stays 15: the module
    # holds no bare integer at all.
    # Re-pinned on U40, 2026-08-26: 74 to 75 holders. tagging/retag_cli.py joined,
    # naming config-unusable the way every other shell does, refused-by-policy for
    # an entry declaring no plan-digested gate, and tag-retag-folder-unknown for an
    # empty folder argument. Differenced as SETS against origin/main's own src tree
    # extracted into a scratch directory, the same way as every entry above:
    # exactly one module joined and none left. The also-holds-an-integer half stays
    # 15, because the module holds no bare integer at all. tagging/retag.py is NOT
    # in the set: its six new kebab literals are result markers rather than causes,
    # which is why the distinct population moved by seven and the holder set by one.
    # Re-pinned on U43, 2026-08-26: 75 to 76 holders. setbuilder/cli.py joined,
    # naming config-unusable the way every other shell does, library-root-absent
    # for a configured root that is not a directory, and its own three anchor
    # refusals. Differenced as SETS by repointing this module's PACKAGE_ROOT at
    # origin/main's own src tree extracted into a scratch directory, the same way
    # as every entry above: exactly one module joined and none left. The
    # also-holds-an-integer half stays 15, because the module's only bare integers
    # are a sequence start and a minimum count, both far below the reserved range.
    # The named halves did NOT move, staying at 8 and 21, because every cause this
    # module names it names as a literal rather than through a symbol, so the
    # comparison just below widened for the eleventh time out of eleven.
    # Re-pinned on U44, 2026-08-27: 76 to 77 holders. master/cli.py joined,
    # naming config-unusable the way every other shell does and source-missing
    # for an empty recording argument. Differenced as SETS by repointing this
    # module's PACKAGE_ROOT at origin/main's own src tree extracted into a
    # scratch directory, the same way as every entry above: exactly one module
    # joined and none left. The also-holds-an-integer half stays 15, because the
    # module holds no bare integer at all. The named halves did NOT move,
    # staying at 21 and 8, because both causes it names it names as literals, so
    # the comparison just below widened for the twelfth time out of twelve.
    # modules/tools/mastering.py is NOT in the set and did not join it despite
    # this unit editing it: its refusals are Refusal enum members reached through
    # a symbol, and the seven slugs U44 added to core.cause.REASONS were already
    # in that module's own tree. A pin that watched the edited files rather than
    # the derived set would have expected a second module here.
    # Re-pinned on U42, 2026-08-28: 77 to 78 holders. acquire/cli.py joined,
    # naming config-unusable the way every other shell does. Differenced as SETS
    # by repointing this module's PACKAGE_ROOT at origin/main's own src tree
    # extracted into a scratch directory, the same way as every entry above:
    # exactly one module joined and none left. The also-holds-an-integer half
    # stays 15, measured rather than assumed, because the module holds no bare
    # integer at all. The named halves did NOT move, staying at 21 and 8,
    # because the one cause it names it names as a literal, so the comparison
    # just below widened for the thirteenth time out of thirteen.
    #
    # The five finding kinds this module also adds are NOT causes and do not
    # reach this population, which is the distinction the rename above is about:
    # a module holding five cause-shaped literals that are not causes is exactly
    # the shape this pin exists to make visible rather than absorb.
    # Re-pinned on U45, 2026-08-29: 78 to 79 holders. backup/cli.py joined,
    # naming config-unusable the way every other shell does plus the three
    # backup-prefixed slugs it raises. Differenced as SETS by repointing this
    # module's PACKAGE_ROOT at origin/main's own src tree extracted into a scratch
    # worktree, the same way as every entry above: exactly one module joined and
    # none left. The also-holds-an-integer half stays 15, measured by differencing
    # that set too rather than assumed, because the module holds no bare integer
    # at all. The named halves did NOT move, staying at 21 and 8, and that was
    # measured rather than inferred: both causes the shell declares it names as
    # literals, and the engine refusals it re-raises travel through
    # ``str(exc.refusal)``, which resolves to a Refusal member and not to a
    # declared cause name. So the comparison just below widened for the
    # fourteenth time out of fourteen.
    #
    # modules/tools/backup.py is NOT in the set and did not join it despite this
    # unit becoming its first caller: it declares its refusals as enum members
    # reached through a symbol, and this unit edits none of them. A pin that
    # watched the touched files rather than the derived set would have expected a
    # second module here.
    # Re-pinned on U46, 2026-09-01: 79 to 80 holders. cli/handlers.py joined,
    # naming internal-error as a literal at its four refusal sites, which is what
    # every registry-shaped lookup in this package raises for a key the build does
    # not declare. Differenced as SETS by repointing this module's PACKAGE_ROOT at
    # origin/main's own src tree extracted into a scratch directory, the same way
    # as every entry above: exactly one module joined and none left. The
    # also-holds-an-integer half stays 15, measured by differencing that set too
    # rather than assumed, because the module holds no bare integer at all. The
    # named halves did NOT move, staying at 21 and 8, and that was measured rather
    # than inferred: the module names its one cause as a literal. So the
    # comparison just below widened for the fifteenth time out of fifteen.
    #
    # master/cli.py is NOT a new holder despite this unit adding two refusal sites
    # to it: it was already in the set, and the output-exists slug its new handler
    # raises travels through ``str(mastering.Refusal.OUTPUT_EXISTS)``, which
    # resolves to an enum member and not to a literal at all.
    # Re-pinned on U49, 2026-09-02: 80 to 81 holders. session/cli.py joined,
    # naming config-unusable the way every other shell does, internal-error for
    # an entry declaring no gate under the name its handler asks for, and
    # backup-facts-unreadable for a fact file it can reach and cannot read.
    # Differenced as SETS by repointing this module's PACKAGE_ROOT at
    # origin/main's own src tree extracted into a scratch directory, the same way
    # as every entry above: exactly one module joined and none left. The
    # also-holds-an-integer half stays 15, because the module holds no bare
    # integer at all. The named halves did NOT move, staying at 21 and 8, and
    # that was measured on the same differencing rather than inferred: every
    # cause this module names it names as a literal. So the comparison just below
    # widened for the sixteenth time out of sixteen.
    #
    # cli/gates.py is NOT a new holder despite this unit changing its explicit
    # gate refusal: the condition moved and the cause it raises did not, so a pin
    # watching the touched files rather than the derived set would have expected a
    # second module here.
    # Re-pinned on U51, 2026-09-02: 81 to 84 holders. THREE modules joined and
    # none left, and all three are new files. modules/outbound/source.py names the
    # three ways the outbound item derivation cannot decide what a job's items
    # are. modules/outbound/account.py names the missing credential and the
    # missing provider adapter. modules/outbound/shell.py names config-unusable,
    # which the two outbound verbs used to spell once each, and
    # outbound-account-unbound as the WARNING code on the queued envelope.
    # Differenced as SETS by re-deriving this module's own predicate over the
    # working tree and comparing it against `main`'s, rather than inferred from
    # the total moving by three. The also-holds-an-integer half stays 15: none of
    # the three holds a bare integer anywhere near the reserved range. The named
    # halves did NOT move, staying at 21 and 8, measured rather than inferred.
    #
    # export/cli.py and favorites/cli.py are NOT new holders despite this unit
    # rewriting both: each already named export-playlist-unknown or
    # config-unusable on main.
    #
    # ONE OF THE NEW LITERALS IS DELIBERATE ALIGNMENT RATHER THAN THE
    # `lossy-refused` COLLISION THIS FILE RECORDS ABOVE. shell.py's
    # outbound-account-unbound is both a warning code on a queued envelope and a
    # declared cause, on purpose: the warning names the cause the job will end
    # with. Two names for that would let the warning and the failure describe one
    # outcome differently, which is the defect, not the fix.
    # Re-pinned on U55, 2026-09-02: 84 to 85 holders. ONE module joined and none
    # left, and it is a new file. adopt/shell.py names internal-error, which is
    # the refusal both adoption verbs raise for a job queued with no items and
    # which each of them used to spell separately. Differenced as SETS by
    # re-deriving this module's own predicate over the working tree and comparing
    # it against `main`'s, rather than inferred from the total moving by one. The
    # also-holds-an-integer half stays 15: the new module holds no bare integer
    # anywhere near the reserved range. The named halves did NOT move, staying at
    # 21 and 8, measured rather than inferred.
    #
    # adopt/collection.py, adopt/artifacts.py and adopt/apply_cli.py are NOT new
    # holders despite this unit writing two of them and rewriting the third: the
    # first two name no cause at all, and apply_cli already named config-unusable
    # on main.
    # Re-pinned on U56, 2026-09-03: 85 to 87 holders. TWO modules joined and none
    # left, and both are new files. tagging/searchers.py names its own two slugs,
    # catalogue-unreachable and catalogue-parse-broken, once each as a module
    # constant; tagging/shell.py names internal-error, which is the refusal both
    # tagging verbs raise for a job queued with no items, exactly as its sibling
    # adopt/shell.py does one merge earlier. Differenced as SETS by re-deriving
    # this module's own predicate over the working tree and comparing it against
    # `main`'s in a scratch worktree, rather than inferred from the total moving by
    # two. The also-holds-an-integer half moves 15 to 16, and only the searcher
    # joins it, because that module declares a fifteen second request timeout and a
    # thirty second rate limit base wait and the reserved range contains 15 and 30.
    # Neither number is an exit code; the composite is doing its job by making a
    # module worth one look, and the look says a duration is not a code.
    #
    # tagging/tag.py, tagging/artifacts.py and tagging/cli.py are NOT new holders
    # despite this unit writing two of them and rewriting the third: the first two
    # name no cause at all, and cli.py already named config-unusable on main.
    #
    # Re-pinned at the U52 merge, 2026-09-07: 87 to 88 holders. ONE module joined
    # and none left, and it is a new file. label/catalogue.py names
    # credential-missing for a provider session nothing recorded and
    # label-catalogue-unbound for a build with no adapter to hand the label
    # package. Differenced as SETS on the branch against its own base, the same
    # way as every entry above, and carried through the merge on top of U56's 87.
    # The also-holds-an-integer half stays 16, because the module holds no bare
    # integer at all. The named halves did NOT move, staying at 21 and 8: every
    # cause it names it names as a literal, and the Remedy and Scope members it
    # reaches through symbols resolve to remediation tokens rather than to
    # declared causes, exactly as modules/outbound/account.py's do.
    #
    # label/cli.py and label/sweep.py are NOT new holders despite this unit
    # rewriting both: each already named a cause on main.
    #
    # Re-pinned on U58, 2026-09-07: 88 to 89 holders. ONE module joined and
    # none left, and it is a new file. analysis/energy.py names
    # energy-calibration-unreadable for a calibration file that cannot be
    # read and analysis-write-failed for an undo log that cannot be locked.
    # analysis/cli.py, analysis/artifacts.py and analysis/vocals.py are NOT
    # new holders: cli.py already named config-unusable on main, and the other
    # two name no declared cause at all, the vocal pass's three reasons being
    # statuses rather than causes. The also-holds-an-integer half moves 16 to
    # 18, measured by applying this module's own predicate to main's copy of
    # each file and to the working tree's. cli.py joins it because it declares
    # a minimum of ten measured tracks for a calibration, and energy.py because
    # a level runs to ten and the decile percentiles are multiples of ten; the
    # reserved range contains 10. A track count, a level and a percentile are
    # not codes; the composite made both modules worth one look, and the look
    # says so.
    #
    # Re-pinned on U57, 2026-09-09: 89 to 90 holders. ONE module joined and
    # none left, and it is a new file. intake/acrcloud.py names
    # intake-recognition-spend-bound, intake-recognition-failed, auth-failed
    # and intake-recognition-unready, each at a raise that goes through
    # cause.refuse. Differenced as SETS by running this module's own derivation
    # over main's src tree extracted into a scratch directory. intake/cli.py
    # and core/artifacts.py are NOT new holders: cli.py already named
    # config-unusable on main, and artifacts.py names no cause at all. The
    # also-holds-an-integer half moves 18 to 19: acrcloud.py joins it because
    # a chunk is twelve seconds, the grid is twenty five, the request timeout
    # thirty and the stop on unanswered calls five, and the reserved range
    # contains 12, 25 and 30. A duration is not a code; the composite made the
    # module worth one look, and the look says so. intake/cli.py held a
    # sixteen for one build, the width of a recognised track's identifier,
    # and the review's fix round replaced it with the match module's own
    # digest, so it never reached a pinned measurement.
    assert (len(literal_holders), len(literal_both)) == (90, 19), (
        f"the literal at-risk population moved to {len(literal_holders)} modules, "
        f"{len(literal_both)} of them also holding an in-range integer"
    )
    assert len(with_own) < len(literal_holders), (
        "the named surface the key widening added is now LARGER than the literal "
        "surface that predates it, which is the comparison the decision to keep "
        "the widening rests on. Re-argue it or narrow the key side"
    )

    sharpest = dict(package_sources())["core/exit_codes.py"]
    declared_in_its_own_enum = _guards._declared_enum_values(ast.parse(sharpest))
    low, high = RANGE
    integers = [
        node.value
        for node in ast.walk(ast.parse(sharpest))
        if isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
        and low <= node.value < high
    ]
    # Re-pinned on the U27 merge, 2026-08-15: 42 to 45 declared enum values and 6
    # to 7 of them also reserved-table causes. The integers are UNCHANGED at 28,
    # which is the half that makes this the sharpest case, so the shape of the
    # finding is exactly as it was. The three new members are the three acts
    # round eight split one instruction into, GRANT_PATH_ACCESS,
    # REMOUNT_WRITABLE and UNLOCK_PATH, none of which existed in main's own
    # core/exit_codes.py before the merge. Only the first is also a reserved
    # cause, which is this merge's own reservation and is the seventh.
    assert (
        len(declared_in_its_own_enum),
        len(declared_in_its_own_enum & CAUSES),
        len(integers),
    ) == (45, 7, 28), (
        "core/exit_codes.py is the sharpest case in the residual and its figures "
        "moved. It declares cause-shaped strings in its own Remedy enum, some of "
        "which are also reserved-table causes, and it holds in-range integers "
        "while not being a table owner"
    )


def test_the_static_enum_rule_agrees_with_the_interpreter_over_the_whole_package():
    """The classifier checked against the language, over the tree, not a fixture.

    ``_declared_enum_values`` decides from the SOURCE whether a class is an enum,
    and its two clauses are both readings of a base's NAME: one bound from the
    ``enum`` module, one spelled with an ``Enum`` suffix. Neither can read a base
    defined in another of our modules whose name is neither, and that limit is
    written into the function's docstring. A limit nobody measures is a limit
    that quietly becomes a hole as the tree grows.

    So the interpreter is asked the same question. Every class the package
    actually defines that IS an ``enum.Enum`` at runtime must be one the static
    rule found, with its cause-shaped members. A future module writing
    ``class Cause(Vocabulary)`` against a base of ours fails HERE, naming the
    file, rather than silently dropping that module's whole vocabulary out of the
    key set and making the guard quieter.

    One direction only, deliberately. The static rule reading MORE than the
    interpreter is the safe direction for a guard whose false alarm costs one
    look, and the fixtures above pin what it may not read.
    """
    modules, unimportable = imported_package_modules()
    assert not unimportable
    static = {
        relative: _guards._declared_enum_values(ast.parse(source))
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
    """The guards, over the real tree.

    Exactly two files may map a refusal cause to a code, and both are named
    above. Anywhere else is a second opinion that will eventually disagree with
    the first, which is the argument this repository has already made about its
    duplicate taxonomy resolvers.
    """
    causes = declared_causes()
    offenders = {
        relative: reserved_code_tables(source, causes, RANGE, package_of(relative))
        for relative, source in package_sources()
        if relative not in TABLE_OWNERS
        and reserved_code_tables(source, causes, RANGE, package_of(relative))
    }
    assert not offenders, f"a second reservation table: {offenders}"


def test_the_table_owner_escape_is_exactly_these_two_files():
    """The whitelist rule from the residual
    "Two copies of one import walk still carry a relative-import defect", applied to the one
    whitelist this unit ships.

    ``TABLE_OWNERS`` switches the second-table guard off for a WHOLE FILE, so
    adding a name to it is the cheapest way there is to stop the guard looking.
    Verified when it was written: adding ``core/session.py`` left the whole
    suite green. It kills exactly ONE test now, this one, and
"The mutation table for this unit's guards, written into the repository"
    carries the row. Round one's own commit named that failure mode and shipped nothing that
    would catch it, because every assertion about this set was about what it
    forbids.

    That residual on ``main`` settles the general form: a guard whitelist
    asserts what is
    FORBIDDEN and never what is permitted, and only EXACT MEMBERSHIP catches a
    widening. So the membership is pinned here, and each entry has to be a file
    that genuinely holds a table, so a decorative exemption fails too.
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
    """The registry's sixty other slugs are keys, driven by removing them.

    ``config-unusable`` is reserved by ``core.cause.REASONS`` at ``PRECONDITION``
    and is one of the sixty slugs the reserved table does not repeat. A module
    giving it a DIFFERENT code is the exact second opinion this guard exists to
    report, and round two, with the registry outside the key set entirely,
    returned empty over it.

    NOT VACUOUS, and the way to check that is to remove the term rather than to
    reason about it. Each assertion is driven with the registry in the key set
    and again with only the reserved table's own causes, and the two answers
    differ, which is what a version keyed on the reserved range alone could not
    have shown.
    """
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
    """What KIND of expression each reported key is, off the syntax tree.

    The anti-vacuity half of a fixture that claims to cover the NAMED spelling of
    the residual. A list of hits says which slugs and which lines, and a slug
    reads identically whether it was written inline or reached through a
    constant, so a fixture claiming to cover names can be rewritten entirely into
    literals with every assertion still true. That is not hypothetical: measured
    off the syntax tree, ``RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS``
    contains ZERO non-literal keys while it was the fixture documenting the false
    alarm surface of a rule whose whole change was the resolver.

    Deduplicated the way ``reserved_code_tables`` deduplicates, so a construct
    reaching the walk twice counts once.
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
    """How many of each TABLE SHAPE a source is written with.

    The residual assertion below pins slugs, values and line numbers, and a list
    of hits cannot express a SHAPE. Round four's version listed eighteen hits and
    claimed the fixture's value was that it "covers eleven distinct construct
    shapes"; measured, swapping a construct for a different shape carrying the
    same slugs and values on the same lines left every assertion true, four
    swaps out of four. This is the missing half, read off the syntax tree rather
    than off the report, so a swap changes the counts and fails.

    THREE DIFFERENT NUMBERS DESCRIBE ONE FIXTURE and the round before used one
    word for all three. The residual is EIGHTEEN hits, produced by ELEVEN
    constructs, and this tally counts THIRTEEN nodes: the two extra are the
    ``SENTENCES`` mapping, whose values are sentences, and the empty ``DELAYS``
    literal that the two statements below it fill. Both are dict literals and
    neither produces a hit, which is exactly why the tally is taken off the tree
    rather than off the report.
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
    """The false alarms, listed rather than narrowed away. See the residual
    "The tiers were bought with a number that does not exist".

    Every integer here is inside 10 to 59 and every key is a registry slug, so
    every one of these ordinary constructs is reported. That is the price of one
    key set and one value rule, and it is the CHEAP side of an asymmetric trade:
    each of these costs one developer one look and a decision that gets recorded.
    The other side, which round four bought with these, is a module shipping a
    second reservation table that nothing notices.

    NOT A COST THE TREE PAYS TODAY, and that is measured rather than hoped for.
    Under this exact rule the real package has zero offenders outside the two
    table owners, and it still has zero when every kebab shaped string literal in
    the package is added to the key set: 189 distinct literals, 108 of them not
    keys today. The residual is what a FUTURE ordinary mapping would meet, and
    the answer to it is a review rather than a comment, because the comment the
    round before shipped could silence sixty one reservations at once.
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

    # THE SHAPE HALF. The list above pins keys, values and line numbers and says
    # nothing about how each construct is written, so a tuple of pairs rewritten
    # as a dict literal on the same lines leaves it identical. The fixture's
    # stated value is the SHAPES, so the shapes are asserted.
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

    # THE KEY-KIND HALF, and it is what says this fixture covers the SPELLING it
    # was written for and not the other one. Every key above is an inline string.
    assert _reported_key_kinds(RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS) == {
        "Constant": 18
    }, (
        "this fixture is the LITERAL half of the residual. If a named key appears "
        "here it belongs in the fixture below, where the named half is pinned"
    )


def test_ordinary_data_keyed_on_a_NAME_is_the_same_residual_in_the_tree_s_own_idiom():
    """The half of the false alarm surface the resolver widening actually moved.

    THE MEASUREMENT THAT JUSTIFIED THE WIDENING WAS TAKEN ON THE KEY SET. It
    added 189 kebab shaped literals, 108 of them not keys today, and measured
    zero new offenders. That is a measurement over what counts as a CAUSE. What
    the round changed was the RESOLVER, and the fixture documenting the residual
    contained zero non-literal keys, so the surface the change created was not
    covered by the artifact built to cover it.

    Every construct here is silent before the widening and reported after it, and
    ``TrackOutcome`` is copied from ``src/cratekit/acquire/adapter.py`` rather
    than invented.

    THE HEADROOM, RE-TAKEN AGAINST THE RESOLVER and measured on this tree rather
    than argued: with the resolver ON, the package still reports ZERO offenders
    outside the two table owners, and still zero with all 189 kebab literals in
    the key set. The population at risk is what moved: TEN modules hold a name
    the key side resolves to a registry-declared cause, FOURTEEN once a source's
    own enum declarations count, and FOUR of those fourteen also hold an in-range
    integer literal. The pre-existing literal-key surface is larger, at 25
    non-owner modules holding a cause literal of which five also hold an in-range
    integer, so the widening added a second spelling to an accepted surface
    rather than a new class of false alarm. That is why it is documented here
    instead of narrowed away.
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

    # THE ANTI-VACUITY HALF, and it is the whole point of this fixture existing
    # beside the one above. A named key and an inline key report identically, so
    # nothing in the list above would fail if every construct here were rewritten
    # into literals, at which point this fixture would duplicate the other one.
    assert _reported_key_kinds(RESIDUAL_ORDINARY_DATA_KEYED_ON_A_NAME) == {
        "Attribute": 5,
        "Name": 3,
    }, (
        "no reported key here may be an inline string. This fixture exists to "
        "cover the spelling the key widening reached, and a Constant appearing "
        "in it means the coverage drifted back to the spelling already covered"
    )

    # THE SHAPES, so a construct cannot be swapped for another carrying the same
    # slugs and values on the same lines, which is the defect the tally beside
    # the literal fixture was added for.
    assert _construct_shapes(RESIDUAL_ORDINARY_DATA_KEYED_ON_A_NAME) == {
        "dict literal": 3,
        "dict comprehension": 1,
        "branch returning a value": 1,
    }


def test_a_comment_cannot_silence_a_reservation():
    """THE ESCAPE HATCH IS DELETED, and this is what fails if it comes back.

    The round before answered the residual with ``# not-a-reservation: <reason>``
    on a line, and claimed three things about it: one statement, never a ``def``
    body, blast radius visible from where it is written. All three were false
    when measured, and the third was false by two orders of magnitude.

    * ``def build(): return {"config-unusable": 30}  # not-a-reservation: honest``
      silenced the body. The mark and the body are the same physical line, and
      ``pyproject.toml`` selects ``E9``, ``F`` and ``I`` only, so ``E704`` is off
      and a one line ``def`` passes the battery.
    * ``A = {...}; B = {...}  # not-a-reservation: one reason`` silenced BOTH
      statements on one reason.
    * One comment appended to ``src/cratekit/core/cause.py`` line 158, the line
      ``REASONS: Mapping[str, ExitCode] = MappingProxyType(``, took that file
      from 61 reported reservations to 0. The furthest silenced line was 214
      below the mark, and the failure message that names a use reported the line
      and the reason and never how many reservations went quiet.

    WHY DELETION RATHER THAN REPAIR. The hatch existed to make the wide rule's
    false alarms cheap, and the wide rule has no false alarms here to make cheap.
    Measured over the 51 files the scan reaches: zero offenders outside the two
    table owners, and still zero when every kebab shaped string literal in the
    package is added to the key set, 189 distinct with 108 that are not keys
    today. It was never used once. Dropping ``TABLE_OWNERS`` instead is not the
    alternative: each owner's reservations sit inside ONE statement, so two
    comments would have covered both files, which is the third bullet again.

    So the residual is reported and the answer to it is a decision recorded in
    this file, which is the review a silenced guard never gets otherwise.
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

    THE RULE, and it is about the shape of the module rather than about any
    implementation of a hatch. A comment exists only in the TEXT of a program:
    ``ast.parse`` throws every one of them away, so no rule built on a syntax
    tree can be influenced by one. Therefore a guard that cannot touch the text
    cannot have a per-line off switch, whatever anybody calls it.

    The text is followed from where it enters. Each module-level function's
    ``source: str`` parameter is a seed; a seed assigned to another name taints
    that name; a seed passed to another function OF THIS MODULE taints the
    parameter it lands on, so a helper cannot launder it. The only permitted use
    of a tainted name is as the single argument of ``ast.parse``. An attribute
    read, a subscript, a comparison, an f-string, or a call to anything outside
    this module is reported with its line.

    WHAT THIS DOES NOT COVER, said rather than implied. A function that opens a
    file and reads text of its OWN is not seeded, because it takes no source
    parameter. Nothing in the guard module can do that with the file under
    analysis, since the questions are handed a string and never a path, and the
    import whitelist in
    ``test_the_guard_module_imports_only_what_reading_a_syntax_tree_needs``
    closes the rest of that route.
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
    """The same program with every comment gone and nothing else changed.

    A comment cannot survive a round trip through the syntax tree, so this is the
    comment-free twin of any source, whatever the comment SAID. That is what
    makes the property below independent of a marker: it does not have to know
    what spelling a future escape hatch would use.
    """
    return ast.unparse(ast.parse(source))


def _slugs_and_statuses(hits: list[str]) -> list[str]:
    """A hit list with the line numbers dropped, because unparsing moves lines."""
    return sorted(hit.split(": ", 1)[1] for hit in hits)


#: Markers a FRESH per-line escape hatch would plausibly be spelled with. None of
#: them is the one that was deleted, which is the point: the rule below must not
#: depend on knowing the spelling.
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

    A different marker, no ``tokenize``, and none of the three names the deleted
    hatch used. This is the source the rule below has to reject, and it is
    constructed rather than described so the rejection is measured.
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
    """THE PROPERTY, where the round before pinned the deleted hatch's fingerprint.

    That test asserted ``_annotated_lines``, ``_silenced_lines`` and
    ``NOT_A_RESERVATION`` are absent and that ``tokenize`` is not imported. Those
    are the names the last implementation happened to use, so what they forbid is
    that implementation and not the feature: a fresh per-line escape with a
    different marker, no ``tokenize`` and none of those three names ships GREEN,
    wired in exactly where the deleted one was. Generalised, and it is worth
    carrying past this file: a test that forbids a feature by naming the last
    implementation's symbols forbids that implementation, not the feature.

    The property is that the guard's answer cannot depend on a comment at all.
    Comments do not survive a round trip through the syntax tree, so the
    comment-free twin of any source is one ``ast.unparse`` away, and the two
    answers have to match whatever the comment says. No marker appears in the
    rule.

    DRIVEN OVER THE TREE AND NOT ONLY OVER A FIXTURE, because a fix justified by
    a fixture somebody wrote beside it is this wave's fourth named defect. The
    two table owners are the only files in the package that report anything at
    all, 22 hits and 61, and both are compared against their own comment-free
    twins.
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
    """The STRUCTURAL half, so a future hatch is impossible rather than undetected.

    The behavioural property above is one measurement per comment somebody
    thought of. This is the rule underneath it: a comment can only reach a guard
    through the RAW TEXT of the source, because the syntax tree does not carry
    one. So the text is followed from the parameter that receives it to
    everything it touches, and the only thing it may touch is ``ast.parse``.

    A source parameter flows into another function of the module by being passed
    to it, and that function's parameter is tainted in turn, so a helper cannot
    launder it. Anything else, an attribute read, a subscript, a comparison, a
    call to something outside this module, is reported by line.

    Both directions, because a rule that only ever answers "clean" is a rule
    nobody has checked: the guard module as it ships answers clean, and the same
    module with a fresh hatch wired in answers with the hatch's line.
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
    """EXACT MEMBERSHIP, which is the whitelist rule this unit already lives by.

    The other route to a comment is a library that can see one: ``tokenize``,
    ``io`` wrapped round the text, ``linecache``, a source-reading helper out of
    ``inspect``. Naming those is the fingerprint mistake again, so what is pinned
    is what the module MAY import. Two names, and each is here for a reason a
    reader can check: ``ast`` is the syntax tree and ``re`` is the cause-slug
    shape.

    Adding an import is not forbidden. It costs one line here and the review that
    line brings, which is exactly the review the deleted escape hatch never got.
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
    """A fingerprint on purpose, and it is about PEOPLE rather than the guard.

    The property tests above cover the guard. This one covers the person who
    remembers ``# not-a-reservation:`` from the round it shipped in, writes it,
    and is silently ignored. It is deliberately the exact deleted spelling,
    because that is the only spelling anybody could be expecting to work.
    """
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
    """Two answers to one question is the drift the derivation exists to prevent.

    The guard reads a module's own enum declarations as well, so it bites a
    module whose exception has not been written yet, but the derived set has to
    reach it or a module reserving codes for causes it declares somewhere ELSE
    goes unseen.

    THE DERIVED TERM IS EMPTY IN THIS TREE, which is why the two assertions round
    four shipped here proved nothing: ``derived <= declared_causes()`` and
    ``CAUSES <= declared_causes()`` are both tautologies when
    ``declared_causes()`` is a union containing them, and replacing the whole
    function body with ``return CAUSES`` killed nothing. The only honest way to
    drive a term that is empty in the tree is to make it non-empty, so the walk
    is swapped for one that finds a cause nobody has declared and the union is
    asked for it.
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
    """``package_of``, driven directly, because the scan it feeds cannot drive it.

    The tree-wide scans assert an ABSENCE, so collapsing this to
    ``return "cratekit"`` makes them quieter and greener: every relative import
    in the package resolves against the wrong package, matches nothing, and the
    walk goes silent about all of it. It is the helper that makes the relative
    half of ``_import_targets`` live over real files, and nothing held it.

    The ``__init__`` case is the one with a rule in it: one level up from a
    module and one level up from a package's own ``__init__`` are the same place,
    which is what Python does and what the docstring claims.
    """
    assert package_of("cli/render.py") == "cratekit.cli"
    assert package_of("cli/__init__.py") == "cratekit.cli"
    assert package_of("__init__.py") == "cratekit"
    assert package_of("modules/tools/backup.py") == "cratekit.modules.tools"
    scanned = dict(package_sources())
    for relative in ("cli/render.py", "cli/__init__.py", "modules/tools/backup.py"):
        assert relative in scanned, f"{relative} left the tree, so this proves nothing"

    # END TO END, because the unit answer and the walk's answer fail differently.
    # A sibling of the vocabulary module resolves onto it from ``cratekit.core``
    # and onto nothing from anywhere else, and ``package_of`` is what supplies
    # the difference over a real file.
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
    """The rule from the residual
    "Two copies of one import walk still carry a relative-import defect", applied to the spellings
    it left behind.

    That residual deleted a second constant holding the vocabulary's PACKAGE
    and left the
    module's leaf written out as ``"exit_codes"`` and the class as ``"ExitCode"``
    four separate times, one line from the constants they belong to. Moving
    ``EXIT_CODE_MODULE`` moved the resolver and left every binding behind, which
    is the same one fact in two spellings that residual says it deleted.

    Both are derived at USE now, and the way to show a derivation is a derivation
    is to move the thing it derives from and watch the answer follow. Hard coding
    either leaf back makes this fail.
    """
    monkeypatch.setattr(_guards, "EXIT_CODE_MODULE", "cratekit.core.statuses")
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
    monkeypatch.undo()

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
    """``MAX_HOPS``, pinned at its value rather than described.

    Its docstring used to say "Lowering it ... kills seven tests". Measured
    across the whole suite at every lower value: 0 kills nine, 1 kills two, and
    2, 3, 4 and 5 each kill NOTHING. The claim was checkable and false at every
    value, and the constant was over provisioned by four because nothing needed
    more than two hops.

    So the constant is now the depth of the deepest spelling this guard promises
    to read, and that spelling is a fixture: a code named, named again, and then
    adjusted. It resolves AT the bound and goes silent one below it, so moving
    the constant without moving the promise fails in one direction or the other.
    """
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
    offenders = {
        relative: process_status_literals(source)
        for relative, source in package_sources()
        if process_status_literals(source)
    }
    assert not offenders, (
        f"these bypass the vocabulary entirely and exit with an integer nobody "
        f"reserved: {offenders}"
    )
