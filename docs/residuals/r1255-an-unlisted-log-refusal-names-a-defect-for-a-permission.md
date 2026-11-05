---
title: A refusal over a session log this account cannot list tells a person to report a defect, where the fix is a permission
found: at the review of #526, R-1255, 2026-11-05.
issue: no
---

**The mechanism.** Every refusal over an unlisted session log, the gate's in
`assert_no_unresolved_session` and the reporting reader's in
`session.records`, carries `Remedy.REPORT_DEFECT`, so the human rendering
says "fix: this is a defect; report it with the cause identifier below". The
message itself names the directory and the account, and the project has
`path-permission-denied` with its grant access remedy for this shape.

**Measured cost.** Driven in round two as a second account over a chmod 000
log: `crate restore list`, `restore run` and `session release` each print the
defect remedy beside a sentence naming the permission. A label, not a wrong
sentence; nobody is sent to change anything wrong.

**Closes when:** the refusals over an unlisted log carry the access remedy,
decided once for the gate and the reader together, with the rendering pinned.
