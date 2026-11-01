---
title: The go after a stopped tail asks its gate over nothing before saying nothing is to be done
found: at the review of #401, U190, 2026-11-01.
issue: no
---

**The mechanism.** A go whose tail stopped has already settled its answers
and finished its download, so the next `crate label sync --go` summarises no
answer and no job to resume, and still asks `label.sync.confirm` ("Download
every release the saved answers took?") over a count of zero. U190's refusal
names the rest of the tail as the way on, so a person who follows it never
meets this, but one who runs the go again does.

**Measured cost.** Driven by the review: one empty gate to answer, then
nothing downloaded and no tail. Nothing is lost or written. The empty gate is
the go's behaviour before U190.

**Closes when:** a go with no answer and no job to resume ends NO_OP before
the gate, saying so, with a test. Ledger only, a wording and a step.
