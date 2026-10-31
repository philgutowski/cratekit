---
title: A rehearsal's plan lines are JSON values, so a path with an accent prints as an escape on the refusal and the gate screen
found: at the review of #399, U188, 2026-10-31.
issue: no
---

**The mechanism.** `rehearsal.lines` dumps every leaf with `json.dumps`, whose
default escapes each character outside ASCII and each quote. U188 maps the
area's plan as values before it is printed, so the comparison is right, but a
line the refusal or the live gate's `differs from the rehearsal` list prints
still spells `café` as `café`, and the person reading it decodes it by
eye.

**Measured cost.** Driven with a batch named `2026-09-29_café`: the comparison
is equal and nothing is shown. Shown only when the plans really differ, as an
escape, which is hard to read and not false. Changing the dump changes the
recorded lines of every kept rehearsal, which compare by digest and are
unaffected, so the fix is cheap.

**Closes when:** `rehearsal.lines` dumps with `ensure_ascii=False`, with a test
that a refusal names an accented path as written. Ledger only.
