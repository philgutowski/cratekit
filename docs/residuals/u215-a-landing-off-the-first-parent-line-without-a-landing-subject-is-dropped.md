---
title: A landing behind a local merge of main whose subject is not in the landing form, and that no pull request claims, is left out of a release
found: at the review of #529, U215, 2026-11-05.
issue: no
---

**The mechanism.** Off the first parent line, `landings_since` lists an
unclaimed merge only under a `merge(uN): ...` or `merge(r-N): ...` subject,
since every other off line merge in the history is a branch sync. A merge that
reached `origin/main` under another subject, with no pull request whose merge
commit or head claims it, and then went behind a local `Merge branch 'main' of
...`, is not listed.

**Measured cost.** Not produced. Over all of `origin/main`, the three local
syncs ever made are on the first parent line, every landing since U158 has a
pull request record whose merge commit is in the history (79 of 79), and the
over a hundred off line merges without a landing subject are branch syncs.

**Closes when:** the off line walk follows each local sync's second parent
first parent line and reads it as a stretch of `main`, so a landing there is
judged as one on the line is. Ledger only.
