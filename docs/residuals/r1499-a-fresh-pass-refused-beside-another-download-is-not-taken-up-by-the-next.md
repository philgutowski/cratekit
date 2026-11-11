---
title: A fresh sync pass refused beside another download is not taken up by the next fresh pass
found: at the review of #665, R-1499, round one, 2026-11-11.
issue: no
---

**The mechanism.** `crate sync land` reads the staging folder before its download, which is after `sync all` queued the pass's intake jobs and wrote its list. A pass refused there leaves those jobs settled, and a later plain `crate sync land` finds "sync all queued nothing new" and names no earlier pass, so the refused pass is continued only by the `--pass-run` command its refusal printed.

**Measured cost.** Driven at round one (d14): with the other download moved out, a fresh `crate sync land` exited 0, fetched nothing and said nothing of the earlier pass. Nothing is lost and the refusal's own last step is the way on; a session that loses that step does not get the account's new tracks until someone continues the pass.

**Closes when:** a fresh pass reads the folder before `sync all` (it can own nothing there yet), or a fresh pass that queued nothing names an earlier pass refused beside another download. Ledger only.
