---
title: The core dependency import guard counts an import anywhere under src, so a core line only an extra's module imports passes it
found: at the review of #698, U269, 2026-11-12.
issue: no
---

**The mechanism.** `tests/test_packaging.py::test_every_core_dependency_is_imported_by_the_package`
sweeps every module under `src/cratekit` for imports and passes a core
dependency any of them names. A module that only runs with an extra installed
(the analysis, vocals, web or desktop modules) counts the same as a core
module, so a dependency that belongs in an extra but sits in the core list is
read as used. The review drove it: `numpy>=1.24` added to the core list passes
this guard (the existing heavy package guard catches numpy, but a light
package only an extra's module imports, such as one the web module alone
uses, would pass both).

**Measured cost.** None today: every core line is imported by a core module.
The cost is a future core line that belongs in an extra, downloaded by every
slim install, with this guard green.

**Closes when:** the guard reads only the modules the slim profile can import,
or the registry's module to extra mapping is used to exclude an extra's
modules from the sweep. Ledger only: maintainer facing and unreached.
