---
title: A handler key doubling as a verb name fails layering for a second, independent reason
date: 2026-09-01
category: workflow-issues
module: src/cratekit/cli/handlers.py
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: workflow_improvement
applies_when:
  - A brief names a core/ file to hold a table that references cli-declared handler_key or verb-name strings
  - A table's values are strings that also serve as Entry.name in the CLI registry
  - test_layering.py's string-scanning rule (not just its import rule) has not been run against the proposed module
  - A verb module (modules-ranked) needs to reach a cli-ranked table such as src/cratekit/cli/registry.py or a sibling dispatch table
  - Fixing the obvious import-boundary violation is being treated as sufficient before landing
symptoms:
  - tests/test_layering.py fails on a core/ module for holding a verb-name-shaped string, with no import statement anywhere in the file
  - Moving the import out of core/ (deferring or aliasing it) still fails layering because the string itself, not an import, is what the checker flags
  - A verb module (modules-ranked) cannot import the cli-ranked table directly, so per-verb direct imports of the handler table also fail layering
  - The brief's specified file path (src/cratekit/core/handlers.py) does not match where the code can legally land (src/cratekit/cli/handlers.py)
related_components:
  - testing_framework
  - documentation
tags:
  - layering
  - test-layering
  - registry
  - handler-key
  - core-cli-boundary
  - verb-path
  - silent-failure
  - brief-vs-landing-path
---

# A handler key doubling as a verb name fails layering for a second, independent reason

## Context

U46 (issue #64) closed the half of residual R-198 a single unit can close: a
handler key needed to resolve to the function `cratekit.core.jobs.drive` calls
per queued item, so a long-running verb's queued work actually runs from
`pending` to `done` instead of sitting there forever. That meant landing a new
table mapping `handler_key -> implementation`. The brief named its file as
`src/cratekit/core/handlers.py`.

That placement is illegal, and it is illegal twice over, for two independent
reasons enforced by the same guard, `tests/test_layering.py`. Both are stated
directly in the landed module's own docstring (`src/cratekit/cli/handlers.py:35-41`):

> **WHY THE DRIVER LIVES HERE RATHER THAN IN `core`.** Issue #64 asked for
> `core/handlers.py` and the layering guard refuses it twice: a core module
> may not import `cratekit.cli.registry`, and it may not hold a string that
> is a verb name or that names a feature package, which every handler key
> and every declaration below is. The verbs cannot import this module
> either, for the mirrored reason: a verb is modules-ranked and this is
> CLI-ranked. They reach `run_job` through `Context.run_job` instead, which
> is the one route the ladder allows.

The task session (relay/64) did not take the reviewer's word for this. It
loaded `test_layering` directly and confirmed the rank of `cratekit.master.cli`
(`modules`) against `cratekit.cli.handlers` (`cli`) before acting, and the
first plan draft, produced by `ce-plan` against the brief and only then
caught by an adversarial `ce-doc-review` pass, had targeted `core/handlers.py`
before this was known (auto memory [claude]).

## Guidance

When a plan asks you to land a table that maps a CLI-declared key (a verb
name, a handler key, anything the CLI layer owns the vocabulary for) to an
implementation, do not assume a layering guard's only rule is "no import of
the higher layer." Check whether the guard *also* forbids the values
themselves, written as plain strings, from appearing in the lower layer. A
"config as strings instead of imports" workaround is the natural first
instinct once you know rule 1 exists, and it is exactly the shape rule 2 is
built to catch.

Concretely, in this repo's `tests/test_layering.py`:

- **Rule 1, import direction (KTD23).** `import_direction_violations`
  (`tests/test_layering.py:238`) walks the whole AST, not just the module
  header, specifically because both live violations it was built to catch
  were lazy, function-body imports. A core module (rank `infrastructure`)
  importing `cratekit.cli.registry` (rank `cli`) trips this the moment the
  import exists anywhere in the file, deferred or not.
- **Rule 2, a lower layer never names a higher-layer concept as a string**
  (`tests/test_layering.py:315`, function `higher_concept_violations`). For
  any module ranked below `modules`
  (`LAYERS = ("foundation", "domain", "infrastructure", "write", "modules",
  "cli")`, `tests/test_layering.py:57`), the checker walks every
  `ast.Constant` string literal in the source and fails if the value starts
  with a dotted path whose second segment names a feature-module package
  (`MODULE_PACKAGES`), or **is itself a verb name**, checked against
  `verb_names()` (`tests/test_layering.py:162`), which reads
  `cratekit.cli.registry.VERB_NAMES`.

  This is why a handler table cannot dodge rule 1 by holding
  `"cratekit.master.cli:handle"` as a plain string instead of an import: the
  string check fires independently, and it fires on the *key* side too, not
  just the module-path side, because every `handler_key` in this registry is
  also a verb name.

The reason rule 2 catches the key side is a real invariant in
`src/cratekit/cli/registry.py`: every `Entry` sets `handler_key=` to the same
string as `name=` (confirmed across the ~64 `handler_key=` assignments in the
file, e.g. `name="master"` at `registry.py:1475`). A handler-key table built
in `core/` would therefore be a core module holding, as dict keys, a list of
strings that are *also* the CLI's verb vocabulary — precisely what rule 2's
"names the verb" branch exists to forbid, independent of whether the table
also imports anything.

There is a third wrinkle, and it is peer-layer rather than core-vs-cli: verb
modules themselves (e.g. `cratekit.master.cli`) cannot import
`cratekit.cli.handlers` either, even though `cratekit.cli.handlers` is not
`core`. The layer ladder ranks a verb module as `modules` (the catch-all rule
`^cratekit\.[a-z_]+\.` -> `modules`), while `cratekit.cli.handlers` is ranked
`cli` (`^cratekit\.cli\.` -> `cli`). `modules` sits below `cli`, so a verb
importing the handler table is the same upward-import violation as core
importing `cli.registry`, just one layer over. This is why the landed design
does not have verbs call the handler module directly at all; they reach it
through `Context.run_job` (`src/cratekit/cli/__init__.py:100`, called from
`src/cratekit/master/cli.py:214` as `ctx.run_job(store, job)`), which lives in
`cratekit.cli` itself, so no module-ranked file ever names
`cratekit.cli.handlers`. The method's own docstring says this explicitly:
"THE ONLY ROUTE A VERB HAS TO THE DRIVER, and it is a method rather than an
import for a reason the layering guard enforces. A verb module is
modules-ranked and `cratekit.cli.handlers` is CLI-ranked."

**The practice, stated plainly: before trusting a placement for a table like
this, run the checker's own functions (`import_direction_violations`,
`higher_concept_violations`) against the proposed module and its planned
contents, rather than reading the rule prose and reasoning about it from
memory.** Reading the prose tells you rule 1 is about imports; it does not
surface that rule 2 treats a verb name written as a plain string exactly the
way rule 1 treats an import statement. Only running the checker, or carefully
tracing what `ast.Constant` values it walks, surfaces that the "strings
instead of imports" escape hatch is closed too.

## Why This Matters

A plan that looks compliant on a prose read of a layering document can still
be illegal, because real layering checkers commonly encode two different
kinds of rules that do not compose the way intuition suggests:

1. a **structural rule** over the import graph (who imports whom), and
2. a **content rule** over string/name literals (who *names* whom, even
   without importing).

Rule 1 alone would make "hold the target as a string instead of an import"
look like a valid workaround. Rule 2 exists specifically because that
workaround is a real upward dependency wearing a disguise —
`importlib.import_module` on a string is exactly as much of an upward
dependency as a static import, just invisible to an import-graph walk.
Missing that a second rule exists, or assuming both rules are "really" the
same rule, costs a redone plan-and-implementation cycle: in this unit's case,
the first-draft placement (`core/handlers.py`) had to be caught and moved to
`cli/handlers.py` before the work could land, and the same reasoning also
ruled out the seemingly safer "verbs import the table directly" design,
forcing the `Context.run_job` indirection instead.

## When to Apply

Any time a repository has an automated layering or dependency-direction
guard (a `test_layering.py`, an import-linter config, an architecture-fitness
test, or equivalent) and new code needs to reference an identifier, key, or
string that is *owned* by a higher or peer layer, not just import a module
from it. Specifically:

- Building a registry, dispatch table, or config block in a lower layer that
  maps a higher layer's vocabulary (verb names, command names, route names,
  feature flags) to something the lower layer executes.
- Any design that reaches for "use a string instead of an import" to satisfy
  an import-direction rule — treat that as a trigger to check whether a
  string-scanning rule exists before assuming the workaround is clean.
- Placing a new module and needing to decide its layer rank when its natural
  home (by directory convention) conflicts with what it is allowed to name.

## Examples

**Before (the brief, issue #64):** `src/cratekit/core/handlers.py`, a
`core`-ranked module holding a `handler_key -> "module:function"` table.
Illegal twice: importing `cratekit.cli.registry` from `core` violates rule 1
(KTD23 import direction), and the handler keys, being identical to verb names
by the `Entry.name == Entry.handler_key` invariant, violate rule 2
(`higher_concept_violations`'s "names the verb" branch) even if the import
were removed.

**After (landed, `b0cee3c`/`3b690d2`, merged `e0b851e`):**
`src/cratekit/cli/handlers.py`, ranked `cli`, so it is legal for it to name
verbs and sit beside `cli.registry`. It holds two plain-string mappings,
`HANDLERS` (handler_key to `"dotted.module:function"`) and
`HANDLERS_NOT_YET_BOUND` (handler_key to a reason string), and exactly one
function, `resolve()` (`cli/handlers.py:170`), performs the one
`importlib.import_module` call, only after the key has been validated against
`HANDLERS`. `run_job()` (`cli/handlers.py:210`) is the one caller of
`cratekit.core.jobs.drive`. The one bound entry as of this unit is
`"master": "cratekit.master.cli:handle"`; the other queued verbs are listed in
`HANDLERS_NOT_YET_BOUND` with a residual-tagged reason each (recorded as
residual R-203).

Verb modules reach this not by importing `cratekit.cli.handlers` (which would
repeat the same violation one layer over) but through `Context.run_job`
(`src/cratekit/cli/__init__.py:100`), called from
`src/cratekit/master/cli.py:214` as `ctx.run_job(store, job)`.
`Context.run_job` does the import of `cratekit.cli.handlers` locally, inside
the method body, both because it is the only layer-legal place to hold that
reference and, separately, to avoid an unrelated import cycle through
`cratekit.core.jobs`.

Driving the seam end to end, rather than only wiring it, surfaced three real
defects in the same unit, none of them layering-related: the master handler
read the recording path from the job payload instead of the per-item entry,
so a multi-item job re-mastered the same file for every item; the encoder
wrote straight to its final destination, so a killed run left a partial file
there that poisoned every later resume; and the frozen output directory could
be left relative instead of absolutized (auto memory [claude]).

## Related

- [The brief Files line is not the landing path](the-brief-files-line-is-not-the-landing-path.md):
  the closest existing sibling. Same mechanism — `test_layering` surprises an
  author who only reads its rules on paper rather than running them, and a
  brief's stated file path disagreed with where the code could legally
  land. Different content: that doc is about `registry.Entry.module` staying
  out of sync with a brief's `Files:` line (a bookkeeping mismatch); this one
  is about a table's *keys*, not its own module path, tripping a
  string-scanning rule that a naive "hold it as a string instead of an
  import" fix does not anticipate. Worth reading together when placing any
  new cross-cutting table, not because either supersedes the other.
- `docs/residual-findings.md`, entry "R-198. Nothing calls the job driver":
  the residual this unit closes. R-203 through R-209 are the residuals this
  unit opened, including the eighteen verbs still listed in
  `HANDLERS_NOT_YET_BOUND`.
