---
title: A job cancelled from another terminal under a live foreground drive ends as a defect report, or queued again
found: at the review of #403, U192, 2026-11-01.
issue: no
---

**The mechanism.** `crate job cancel` reconciles and cancels a job without asking whether a live driver holds it. A foreground drive of that job keeps claiming and finishing items, and at the end `jobs.drive` asks to move the job from cancelled to succeeded, which the engine refuses as `internal-error` with the remedy to report a defect. If the same drive is then stopped with Ctrl-C, `modules.foreground.settle` reads the job as cancelled and re-arms it with `jobs.retry`, so a job somebody cancelled on purpose comes back queued.

**Measured cost.** Driven by the review: a handler that ran the cancel verb's two calls on item 2 left all four items done, the job recorded cancelled, and an exit 1 telling the person to report a defect over a sweep that finished. With a SIGINT in the same handler the job came back queued with 1 of 4 settled. The first shape predates U192 on every `--job` drive; U192 widens its window, since every hand run of the three tail verbs is now a live drive. The second needs a concurrent cancel and a Ctrl-C inside one item. A queued job drives nothing on its own.

**Closes when:** `job cancel` refuses, or signals, a job a live driver holds (`jobs.assert_free` before `jobs.cancel`), so the two endings cannot meet. Ledger only: the producer is a concurrent act in a second terminal.
