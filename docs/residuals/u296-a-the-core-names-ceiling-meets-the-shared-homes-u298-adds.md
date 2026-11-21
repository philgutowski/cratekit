---
title: The ceiling on core names feature packages use, 437, is met by any card that gives a helper one home in core, which is what U298 is for
found: while building #853, U296, 2026-11-21.
issue: no
---

**The mechanism.** U296's brief asks that the count of distinct core names
feature packages use, 437 on `ff8e5ec`, be printed and not grow, and
`tests/test_import_rules.py` holds it as `CORE_NAMES_CEILING`. U298 (#855)
gives config loading, gate lookup, job reports, artifact paths, locks and the
provider helpers one home each, in core or in the three foundation modules of
the shell. A helper homed in core and called from a feature package is one
more core name, and the copies it replaces used names other code still uses,
so the count rises by about the number of new helpers while duplication
falls. Making a private name public does not move the count: the private
spelling leaves as the public one joins.

**Measured cost.** Not driven, since U298 is not built. Read from the survey:
38 clusters of whole functions in two or more files, in about seven families,
so the rise is of the order of ten to twenty names against a ceiling with no
slack. A maintainer facing cost only: U298's battery is red on a rule its own
brief does not name, until its thread decides which of these it is. The
options are that U298 homes its helpers in the shell's foundation modules
where the layer allows it, which adds no core name; that it removes as many
uses as it adds; or that the ceiling is restated for that one card with the
names it added listed in its record. The third breaks the rule that an
allowance only shrinks, so it is the coordinator's call or Phillip's, not a
build thread's.

**Closes when:** U298 lands with the count at or under the ceiling, or the
ceiling's rule is restated on #847. Ledger only.
