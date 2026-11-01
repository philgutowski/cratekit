---
title: The doctor's run scan and crate run retire raise on a run record of the wrong shape
found: at the second review of #380, U183, 2026-11-01.
issue: no
---

**The mechanism.** `RunState.from_json` in `src/cratekit/cli/gates.py` checks the
schema version and nothing else, so a record that is an object but lacks
`run_id`, or holds a string where `pending_human_action` or a list where `pins`
or `decisions` should be a mapping, raises `KeyError`, `TypeError` or
`AttributeError`. The doctor's run scan and `crate run retire` catch only the
gates module's own refusal, so one such file ends either verb with an internal
error. U183 made `gates.load` refuse a record that is not an object at all, and
made the sync land resolver read any misshapen record as no land run; the other
two readers keep the old shape.

**Measured cost.** Driven with a hand written file in the run directory: the
doctor and `run retire` both raise. The producer was not driven: the one writer,
`gates.save`, writes `to_json` through an atomic write and cannot emit these
shapes, so the cost needs a hand edit or a foreign file.

**Closes when:** `from_json` validates each field's type and raises the gates
module's unreadable record refusal, so every reader gets one refusal it already
handles. Ledger only: no shipped verb produces the input.
