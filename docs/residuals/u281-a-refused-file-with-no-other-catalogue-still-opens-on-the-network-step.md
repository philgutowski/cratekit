---
title: A file every asked catalogue refused fails catalogue-unreachable with "check this machine's network connection" as its first step
found: at the review of #796, U281, 2026-11-13.
issue: no
---

**The mechanism.** When Beatport refuses this client and Discogs is not asked
(no token) or is unread too, `searchers._decide` raises
`catalogue-unreachable`, whose first step tells the person to check this
machine's network connection. The refusal is named only in the second step
and the cause's detail. Every file of such a sweep fails that way, the job
fails, and the sweep carries no `tag-folder-sources-unread` warning, because
the files left no report to count. The step text came in with R-791; U281
only reads Beatport's 403 as a refusal, so this is now the shape a refusing
Beatport with no Discogs token produces on every file.

**Measured cost.** Driven by U281's review: five files, Beatport answering a
Cloudflare 403, Discogs with no token. Exit 1, three Beatport requests, all
five items `catalogue-unreachable`, no warning, step one the network. A person
is sent to their network over a refusal no network check moves.

**Closes when:** a refusal on every asked catalogue is said as a refusal
first, and the pass's handling of it is decided. Ledger only: what a pass does
when every catalogue is blocked is #790's question (U279), which already
holds a card on the board.
