---
title: The metadata refusal's step spells a whole location_prefix_map assignment, which a configuration holding a rule refuses to load
found: at the review of #672, U243, 2026-11-12.
issue: no
---

**The mechanism.** ``write/metadata_cli.py`` tells a person to add
``library.location_prefix_map = [{ from = ..., to = ... }]`` to the
configuration by hand. Setup always writes the key, so following the step
literally assigns it twice, and ``config.load`` refuses with ``ConfigCorrupt``
(driven by round two). U243 corrected the same wording in the deletion pass's
refusal; this one predates it.

**Measured cost.** A person who follows the step gets a configuration that
will not load, until they merge the two lists by hand.

**Closes when:** the step names one entry to add to the existing list, as the
deletion refusal now does. Ledger only.
